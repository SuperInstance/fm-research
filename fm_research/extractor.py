"""Key finding extractor — pulls key findings from research text."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

from .paper import Paper


@dataclass
class Finding:
    """A single extracted finding."""
    text: str
    category: str  # "result", "method", "claim", "definition", "observation"
    confidence: float  # 0-1
    source_paper_id: str = ""
    source_location: str = ""  # line/paragraph hint

    def __repr__(self) -> str:
        snippet = self.text[:60] + "…" if len(self.text) > 60 else self.text
        return f"Finding({self.category}, conf={self.confidence:.2f}, {snippet!r})"


# Patterns that signal key findings
_RESULT_PATTERNS = [
    re.compile(r"(?:we find|we found|results show|our results|the result is)\b(.+?)(?:\.|$)", re.I),
    re.compile(r"(?:demonstrates?|confirms?|reveals?|indicates?)\b(.+?)(?:\.|$)", re.I),
]

_METHOD_PATTERNS = [
    re.compile(r"(?:we propose|we introduce|we use|we employ|our approach|our method)\b(.+?)(?:\.|$)", re.I),
    re.compile(r"(?:using|via|by means of|through)\b(.+?)(?:,|\.)", re.I),
]

_CLAIM_PATTERNS = [
    re.compile(r"(?:we show|we prove|we argue|it follows that|therefore)\b(.+?)(?:\.|$)", re.I),
]

_DEFINITION_PATTERNS = [
    re.compile(r"(?:is defined as|denotes?|refers? to|is a|are called)\b(.+?)(?:\.|$)", re.I),
]

_OBSERVATION_PATTERNS = [
    re.compile(r"(?:interestingly|notably|surprisingly|we observe|we note)\b(.+?)(?:\.|$)", re.I),
    re.compile(r"(?:this suggests|this implies|suggesting that)\b(.+?)(?:\.|$)", re.I),
]


def _extract_sentences(text: str, patterns: list[re.Pattern[str]]) -> list[tuple[str, float]]:
    """Extract matching sentences with base confidence."""
    hits: list[tuple[str, float]] = []
    for pat in patterns:
        for m in pat.finditer(text):
            sentence = m.group(0).strip()
            if len(sentence) > 15:  # skip trivially short
                hits.append((sentence, 0.7))
    return hits


class KeyExtractor:
    """Extract key findings, methods, claims, and definitions from text.

    Uses pattern-based extraction (no ML dependencies). Can operate on
    individual papers or raw text strings.
    """

    def __init__(self, min_confidence: float = 0.3):
        self.min_confidence = min_confidence

    def extract_from_text(self, text: str, source_id: str = "") -> list[Finding]:
        """Extract findings from a raw text string."""
        findings: list[Finding] = []

        categories = [
            ("result", _RESULT_PATTERNS),
            ("method", _METHOD_PATTERNS),
            ("claim", _CLAIM_PATTERNS),
            ("definition", _DEFINITION_PATTERNS),
            ("observation", _OBSERVATION_PATTERNS),
        ]

        for cat, patterns in categories:
            for sentence, conf in _extract_sentences(text, patterns):
                if conf >= self.min_confidence:
                    findings.append(Finding(
                        text=sentence,
                        category=cat,
                        confidence=conf,
                        source_paper_id=source_id,
                    ))

        # Boost confidence for findings that appear near key terms
        key_terms = {"constraint", "forgemaster", "snap", "deadband", "lattice", "eigenstructure"}
        for f in findings:
            lower = f.text.lower()
            matches = sum(1 for t in key_terms if t in lower)
            f.confidence = min(1.0, f.confidence + matches * 0.05)

        return findings

    def extract_from_paper(self, paper: Paper) -> list[Finding]:
        """Extract findings from a Paper object."""
        combined = "\n\n".join(filter(None, [paper.abstract, paper.content]))
        return self.extract_from_text(combined, source_id=paper.id)

    def extract_from_papers(self, papers: list[Paper]) -> list[Finding]:
        """Extract findings from multiple papers, deduplicated."""
        all_findings: list[Finding] = []
        for p in papers:
            all_findings.extend(self.extract_from_paper(p))
        return self._deduplicate(all_findings)

    def extract_key_sentences(self, text: str, max_sentences: int = 5) -> list[str]:
        """Return the top-N most confident findings as raw sentences."""
        findings = self.extract_from_text(text)
        findings.sort(key=lambda f: f.confidence, reverse=True)
        return [f.text for f in findings[:max_sentences]]

    @staticmethod
    def _deduplicate(findings: list[Finding], similarity_threshold: float = 0.8) -> list[Finding]:
        """Remove near-duplicate findings."""
        unique: list[Finding] = []
        seen_words: list[set[str]] = []
        for f in findings:
            words = set(f.text.lower().split())
            is_dup = False
            for existing in seen_words:
                overlap = len(words & existing) / max(len(words), len(existing), 1)
                if overlap >= similarity_threshold:
                    is_dup = True
                    break
            if not is_dup:
                unique.append(f)
                seen_words.append(words)
        return unique

    def __repr__(self) -> str:
        return f"KeyExtractor(min_confidence={self.min_confidence})"
