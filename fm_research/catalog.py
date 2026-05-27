"""ResearchCatalog — organize papers by topic, search, and analyze."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional

from .paper import Paper
from .search import ResearchSearch
from .extractor import KeyExtractor, Finding


@dataclass
class TopicStats:
    """Statistics for a topic cluster."""
    topic: str
    paper_count: int
    total_words: int
    avg_citations: float
    top_keywords: list[str] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"TopicStats({self.topic!r}, papers={self.paper_count}, words={self.total_words})"


class ResearchCatalog:
    """Organize and analyze a research paper collection.

    Provides:
    - Topic-based organization (manual and auto).
    - Statistics per topic and overall.
    - Integration with ResearchSearch and KeyExtractor.
    """

    def __init__(self, name: str = "default"):
        self.name = name
        self.papers: dict[str, Paper] = {}  # id -> Paper
        self.topics: dict[str, set[str]] = defaultdict(set)  # topic -> paper ids
        self._search = ResearchSearch()
        self._extractor = KeyExtractor()

    # --- Paper management ---

    def add_paper(self, paper: Paper, topics: Optional[list[str]] = None) -> str:
        """Add a paper and optionally assign topics."""
        pid = paper.id
        self.papers[pid] = paper
        self._search.add(paper)
        for t in (topics or paper.topics or ["uncategorized"]):
            self.topics[t].add(pid)
        return pid

    def add_papers(self, papers: list[Paper]) -> list[str]:
        """Add multiple papers at once."""
        return [self.add_paper(p) for p in papers]

    def remove_paper(self, paper_id: str) -> bool:
        """Remove a paper by ID."""
        if paper_id not in self.papers:
            return False
        del self.papers[paper_id]
        self._search.remove(paper_id)
        for t in list(self.topics):
            self.topics[t].discard(paper_id)
            if not self.topics[t]:
                del self.topics[t]
        return True

    def get_paper(self, paper_id: str) -> Optional[Paper]:
        return self.papers.get(paper_id)

    # --- Topic operations ---

    def assign_topic(self, paper_id: str, topic: str) -> None:
        """Assign a paper to a topic."""
        if paper_id in self.papers:
            self.topics[topic].add(paper_id)

    def unassign_topic(self, paper_id: str, topic: str) -> None:
        self.topics[topic].discard(paper_id)
        if not self.topics[topic]:
            del self.topics[topic]

    def get_papers_by_topic(self, topic: str) -> list[Paper]:
        pids = self.topics.get(topic, set())
        return [self.papers[pid] for pid in pids if pid in self.papers]

    def list_topics(self) -> list[str]:
        return sorted(self.topics.keys())

    def topic_stats(self, topic: str) -> Optional[TopicStats]:
        """Compute statistics for a topic."""
        papers = self.get_papers_by_topic(topic)
        if not papers:
            return None
        total_words = sum(p.word_count for p in papers)
        avg_cites = sum(p.citation_count for p in papers) / len(papers)

        # Gather top keywords
        from collections import Counter
        kw_counter = Counter()
        for p in papers:
            kw_counter.update(p.keywords)
        top_kw = [k for k, _ in kw_counter.most_common(5)]

        return TopicStats(
            topic=topic,
            paper_count=len(papers),
            total_words=total_words,
            avg_citations=round(avg_cites, 1),
            top_keywords=top_kw,
        )

    # --- Search delegation ---

    def search(self, query: str, max_results: int = 20):
        """Search the catalog using the combined search engine."""
        return self._search.search(query, max_results)

    def keyword_search(self, query: str, **kwargs):
        return self._search.keyword_search(query, **kwargs)

    def semantic_search(self, query: str, **kwargs):
        return self._search.semantic_search(query, **kwargs)

    # --- Extraction ---

    def extract_findings(self, topic: Optional[str] = None) -> list[Finding]:
        """Extract key findings, optionally filtered by topic."""
        if topic:
            papers = self.get_papers_by_topic(topic)
        else:
            papers = list(self.papers.values())
        return self._extractor.extract_from_papers(papers)

    # --- Stats ---

    @property
    def total_papers(self) -> int:
        return len(self.papers)

    @property
    def total_words(self) -> int:
        return sum(p.word_count for p in self.papers.values())

    def overview(self) -> str:
        """Human-readable overview of the catalog."""
        lines = [
            f"Catalog: {self.name}",
            f"Papers: {self.total_papers}",
            f"Topics: {len(self.topics)}",
            f"Total words: {self.total_words:,}",
        ]
        for t in self.list_topics():
            stats = self.topic_stats(t)
            if stats:
                lines.append(f"  {t}: {stats.paper_count} papers, {stats.total_words:,} words")
        return "\n".join(lines)

    def __len__(self) -> int:
        return len(self.papers)

    def __repr__(self) -> str:
        return f"ResearchCatalog({self.name!r}, papers={self.total_papers}, topics={len(self.topics)})"
