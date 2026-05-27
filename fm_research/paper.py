"""Paper data model with metadata, citations, and summaries."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Citation:
    """A single citation reference."""
    authors: list[str] = field(default_factory=list)
    title: str = ""
    year: Optional[int] = None
    source: str = ""  # journal, conference, url, etc.

    def __str__(self) -> str:
        author_str = ", ".join(self.authors) if self.authors else "Unknown"
        year_str = f" ({self.year})" if self.year else ""
        return f"{author_str}{year_str}. {self.title}. {self.source}".rstrip(". ")


@dataclass
class Paper:
    """A research paper with full metadata.

    Attributes:
        title: Paper title.
        authors: List of author names.
        abstract: Paper abstract or summary text.
        content: Full text content.
        keywords: Topic keywords.
        citations: References cited by this paper.
        cited_by: Papers that cite this one.
        topics: High-level topic tags.
        date: Publication or creation date.
        source: Origin (arxiv, journal, internal, etc.).
        doi: Digital Object Identifier.
    """

    title: str = ""
    authors: list[str] = field(default_factory=list)
    abstract: str = ""
    content: str = ""
    keywords: list[str] = field(default_factory=list)
    citations: list[Citation] = field(default_factory=list)
    cited_by: list[str] = field(default_factory=list)  # paper IDs
    topics: list[str] = field(default_factory=list)
    date: Optional[date] = None
    source: str = ""
    doi: str = ""

    @property
    def id(self) -> str:
        """Deterministic ID from title + authors."""
        raw = f"{self.title}|{'|'.join(sorted(self.authors))}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    @property
    def word_count(self) -> int:
        return len(self.content.split())

    @property
    def citation_count(self) -> int:
        return len(self.citations)

    @property
    def is_empty(self) -> bool:
        return not self.title and not self.content

    def matches_keyword(self, keyword: str, case_sensitive: bool = False) -> bool:
        """Check if the paper matches a keyword anywhere in its metadata."""
        needle = keyword if case_sensitive else keyword.lower()
        fields = [
            self.title, self.abstract, self.content, self.source,
            *self.keywords, *self.topics, *self.authors,
        ]
        for f in fields:
            haystack = f if case_sensitive else f.lower()
            if needle in haystack:
                return True
        return False

    def summary(self, max_length: int = 200) -> str:
        """Return a short summary, preferring abstract over content."""
        text = self.abstract or self.content or ""
        if len(text) <= max_length:
            return text
        return text[:max_length].rsplit(" ", 1)[0] + "…"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors,
            "abstract": self.abstract,
            "keywords": self.keywords,
            "topics": self.topics,
            "date": self.date.isoformat() if self.date else None,
            "source": self.source,
            "doi": self.doi,
            "word_count": self.word_count,
            "citation_count": self.citation_count,
        }

    def __repr__(self) -> str:
        return f"Paper(title={self.title!r}, authors={len(self.authors)}, words={self.word_count})"
