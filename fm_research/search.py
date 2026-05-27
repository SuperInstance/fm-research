"""Research search with keyword and semantic-style matching."""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional

from .paper import Paper


def _tokenize(text: str) -> list[str]:
    """Lowercase word tokenizer stripping punctuation."""
    return re.findall(r"[a-z0-9]+", text.lower())


def _tfidf_vector(tokens: list[str], idf: dict[str, float]) -> dict[str, float]:
    """Compute a TF-IDF vector for a token list given IDF weights."""
    counts = Counter(tokens)
    total = len(tokens) or 1
    return {t: (c / total) * idf.get(t, 0.0) for t, c in counts.items()}


def _cosine_sim(a: dict[str, float], b: dict[str, float]) -> float:
    """Cosine similarity between two sparse vectors."""
    common = set(a) & set(b)
    if not common:
        return 0.0
    dot = sum(a[k] * b[k] for k in common)
    mag_a = math.sqrt(sum(v * v for v in a.values()))
    mag_b = math.sqrt(sum(v * v for v in b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


@dataclass
class SearchResult:
    """A single search result with relevance score."""
    paper: Paper
    score: float
    match_type: str  # "keyword" or "semantic"
    matched_fields: list[str] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"SearchResult(paper={self.paper.title!r}, score={self.score:.3f}, type={self.match_type})"


class ResearchSearch:
    """Search engine over a collection of Paper objects.

    Supports:
    - **Keyword search**: exact or case-insensitive substring matching.
    - **Semantic search**: TF-IDF–based cosine similarity for fuzzy matching.
    """

    def __init__(self, papers: Optional[list[Paper]] = None):
        self.papers: list[Paper] = list(papers or [])
        self._idf: dict[str, float] = {}
        self._rebuild_index()

    def add(self, paper: Paper) -> None:
        self.papers.append(paper)
        self._rebuild_index()

    def add_all(self, papers: list[Paper]) -> None:
        self.papers.extend(papers)
        self._rebuild_index()

    def remove(self, paper_id: str) -> bool:
        before = len(self.papers)
        self.papers = [p for p in self.papers if p.id != paper_id]
        if len(self.papers) != before:
            self._rebuild_index()
            return True
        return False

    # --- Indexing ---

    def _rebuild_index(self) -> None:
        """Recompute IDF weights from all paper text."""
        doc_freq: Counter = Counter()
        n = len(self.papers)
        for p in self.papers:
            tokens = set(self._paper_tokens(p))
            for t in tokens:
                doc_freq[t] += 1
        self._idf = {
            t: math.log((n + 1) / (df + 1)) + 1
            for t, df in doc_freq.items()
        }

    @staticmethod
    def _paper_tokens(paper: Paper) -> list[str]:
        parts = [paper.title, paper.abstract, paper.content, " ".join(paper.keywords)]
        return _tokenize(" ".join(parts))

    # --- Keyword search ---

    def keyword_search(
        self,
        query: str,
        case_sensitive: bool = False,
        max_results: int = 20,
    ) -> list[SearchResult]:
        """Find papers where query appears in any text field."""
        results: list[SearchResult] = []
        for paper in self.papers:
            if paper.matches_keyword(query, case_sensitive):
                # Simple scoring: count of matches across fields
                needle = query if case_sensitive else query.lower()
                score = 0.0
                matched = []
                for fname in ("title", "abstract", "content"):
                    val = getattr(paper, fname, "")
                    haystack = val if case_sensitive else val.lower()
                    count = haystack.count(needle)
                    if count:
                        score += count * (3.0 if fname == "title" else 1.0)
                        matched.append(fname)
                for kw in paper.keywords:
                    kw_h = kw if case_sensitive else kw.lower()
                    if needle in kw_h:
                        score += 2.0
                        matched.append("keywords")
                        break
                results.append(SearchResult(paper, score, "keyword", matched))
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:max_results]

    # --- Semantic search ---

    def semantic_search(
        self,
        query: str,
        max_results: int = 20,
        min_score: float = 0.05,
    ) -> list[SearchResult]:
        """TF-IDF cosine similarity search."""
        query_tokens = _tokenize(query)
        query_vec = _tfidf_vector(query_tokens, self._idf)
        results: list[SearchResult] = []
        for paper in self.papers:
            doc_tokens = self._paper_tokens(paper)
            doc_vec = _tfidf_vector(doc_tokens, self._idf)
            score = _cosine_sim(query_vec, doc_vec)
            if score >= min_score:
                results.append(SearchResult(paper, score, "semantic"))
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:max_results]

    # --- Combined ---

    def search(
        self,
        query: str,
        max_results: int = 20,
        semantic_weight: float = 0.4,
    ) -> list[SearchResult]:
        """Combined keyword + semantic search with blended scoring."""
        kw_results = {r.paper.id: r for r in self.keyword_search(query, max_results=1000)}
        sem_results = {r.paper.id: r for r in self.semantic_search(query, max_results=1000)}

        all_ids = set(kw_results) | set(sem_results)
        blended: list[SearchResult] = []

        for pid in all_ids:
            kw = kw_results.get(pid)
            sem = sem_results.get(pid)
            kw_score = kw.score if kw else 0.0
            sem_score = sem.score if sem else 0.0
            # Normalize keyword score to 0-1 range roughly
            norm_kw = min(kw_score / 10.0, 1.0)
            combined = (1 - semantic_weight) * norm_kw + semantic_weight * sem_score
            match_type = "combined" if (kw and sem) else ("keyword" if kw else "semantic")
            matched = (kw.matched_fields if kw else []) + (sem.matched_fields if sem else [])
            blended.append(SearchResult(kw.paper if kw else sem.paper, combined, match_type, matched))

        blended.sort(key=lambda r: r.score, reverse=True)
        return blended[:max_results]

    def __len__(self) -> int:
        return len(self.papers)

    def __repr__(self) -> str:
        return f"ResearchSearch(papers={len(self.papers)})"
