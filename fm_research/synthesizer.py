"""Synthesizer — combines findings from multiple sources into coherent summaries."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .paper import Paper
from .extractor import Finding, KeyExtractor


@dataclass
class Synthesis:
    """Result of synthesizing multiple sources."""
    summary: str
    key_findings: list[Finding]
    themes: list[str]
    source_count: int
    source_ids: list[str] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"Synthesis(themes={len(self.themes)}, findings={len(self.key_findings)}, sources={self.source_count})"


class Synthesizer:
    """Combine multiple papers/sources into a coherent synthesis.

    Pipeline:
    1. Extract findings from each source.
    2. Group findings by category (result, method, claim, etc.).
    3. Identify recurring themes via keyword co-occurrence.
    4. Generate a structured summary.
    """

    def __init__(self, extractor: Optional[KeyExtractor] = None):
        self.extractor = extractor or KeyExtractor()

    def synthesize_papers(self, papers: list[Paper]) -> Synthesis:
        """Synthesize a list of papers into a single summary."""
        findings = self.extractor.extract_from_papers(papers)
        themes = self._identify_themes(findings)
        summary = self._build_summary(findings, themes, len(papers))

        return Synthesis(
            summary=summary,
            key_findings=findings,
            themes=themes,
            source_count=len(papers),
            source_ids=[p.id for p in papers],
        )

    def synthesize_texts(self, texts: list[str], labels: Optional[list[str]] = None) -> Synthesis:
        """Synthesize raw text strings."""
        findings: list[Finding] = []
        for i, text in enumerate(texts):
            label = labels[i] if labels and i < len(labels) else f"source_{i}"
            findings.extend(self.extractor.extract_from_text(text, source_id=label))

        themes = self._identify_themes(findings)
        summary = self._build_summary(findings, themes, len(texts))

        return Synthesis(
            summary=summary,
            key_findings=findings,
            themes=themes,
            source_count=len(texts),
            source_ids=labels or [f"source_{i}" for i in range(len(texts))],
        )

    def _identify_themes(self, findings: list[Finding]) -> list[str]:
        """Find recurring themes across findings via word frequency."""
        from collections import Counter
        import re

        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "can", "shall", "to", "of", "in", "for",
            "on", "with", "at", "by", "from", "as", "into", "through", "during",
            "before", "after", "above", "below", "between", "out", "off", "over",
            "under", "again", "further", "then", "once", "and", "but", "or", "nor",
            "not", "so", "yet", "both", "either", "neither", "each", "every",
            "all", "any", "few", "more", "most", "other", "some", "such", "no",
            "only", "own", "same", "than", "too", "very", "just", "because",
            "this", "that", "these", "those", "it", "its", "we", "our", "which",
            "what", "there", "here", "when", "where", "how", "if", "then",
        }

        words: list[str] = []
        for f in findings:
            tokens = re.findall(r"[a-z]+", f.text.lower())
            words.extend(t for t in tokens if t not in stop_words and len(t) > 3)

        counter = Counter(words)
        # Return top themes as the most common meaningful words
        return [word for word, _ in counter.most_common(10)]

    def _build_summary(
        self, findings: list[Finding], themes: list[str], source_count: int
    ) -> str:
        """Build a structured summary from findings and themes."""
        if not findings:
            return "No key findings extracted from the provided sources."

        # Group by category
        by_category: dict[str, list[Finding]] = {}
        for f in findings:
            by_category.setdefault(f.category, []).append(f)

        parts: list[str] = []
        parts.append(f"Synthesis of {source_count} source(s), {len(findings)} findings extracted.")

        if themes:
            parts.append(f"\nKey themes: {', '.join(themes[:7])}.")

        category_labels = {
            "result": "Results",
            "method": "Methods",
            "claim": "Claims",
            "definition": "Definitions",
            "observation": "Observations",
        }

        for cat in ("result", "method", "claim", "definition", "observation"):
            items = by_category.get(cat, [])
            if not items:
                continue
            label = category_labels.get(cat, cat.title())
            # Pick top 3 by confidence
            top = sorted(items, key=lambda f: f.confidence, reverse=True)[:3]
            parts.append(f"\n{label}:")
            for item in top:
                parts.append(f"  • {item.text}")

        return "\n".join(parts)

    def __repr__(self) -> str:
        return f"Synthesizer(extractor={self.extractor})"
