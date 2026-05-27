"""Comprehensive tests for fm_research package."""

import pytest
from datetime import date

from fm_research import Paper, ResearchSearch, KeyExtractor, Synthesizer, ResearchCatalog
from fm_research.paper import Citation


# ─── Paper Tests ───

class TestCitation:
    def test_str_with_all_fields(self):
        c = Citation(authors=["Alice", "Bob"], title="Test Paper", year=2024, source="Nature")
        assert "Alice" in str(c)
        assert "2024" in str(c)
        assert "Nature" in str(c)

    def test_str_empty(self):
        c = Citation()
        assert "Unknown" in str(c)


class TestPaper:
    def _make_paper(self, **kwargs):
        defaults = dict(
            title="Constraint Theory in Forgemaster",
            authors=["Ada Lovelace", "Alan Turing"],
            abstract="We propose a novel constraint framework.",
            content="This paper presents a constraint-based approach to the Forgemaster system. "
                    "We find that constraint deadbands significantly improve convergence. "
                    "Our results show 40% improvement in lattice stability.",
            keywords=["constraint", "forgemaster", "lattice"],
            topics=["constraint-theory"],
        )
        defaults.update(kwargs)
        return Paper(**defaults)

    def test_id_deterministic(self):
        p1 = self._make_paper()
        p2 = self._make_paper()
        assert p1.id == p2.id

    def test_id_differs_for_different_papers(self):
        p1 = self._make_paper(title="Paper A")
        p2 = self._make_paper(title="Paper B")
        assert p1.id != p2.id

    def test_word_count(self):
        p = self._make_paper()
        assert p.word_count > 0

    def test_citation_count(self):
        p = self._make_paper(citations=[Citation(title="ref1"), Citation(title="ref2")])
        assert p.citation_count == 2

    def test_is_empty(self):
        assert Paper().is_empty
        assert not self._make_paper().is_empty

    def test_matches_keyword(self):
        p = self._make_paper()
        assert p.matches_keyword("forgemaster")
        assert not p.matches_keyword("quantum")
        assert p.matches_keyword("FORGEMASTER", case_sensitive=False)
        assert not p.matches_keyword("FORGEMASTER", case_sensitive=True)

    def test_summary_from_abstract(self):
        p = self._make_paper()
        s = p.summary(max_length=30)
        assert len(s) <= 33  # allow ellipsis
        assert s.endswith("…") or len(p.abstract) <= 30

    def test_summary_from_content_when_no_abstract(self):
        p = self._make_paper(abstract="", content="A" * 100)
        s = p.summary(max_length=50)
        assert s.endswith("…")

    def test_to_dict(self):
        p = self._make_paper(date=date(2024, 1, 15))
        d = p.to_dict()
        assert d["title"] == "Constraint Theory in Forgemaster"
        assert d["date"] == "2024-01-15"
        assert "id" in d

    def test_repr(self):
        p = self._make_paper()
        r = repr(p)
        assert "Constraint Theory" in r


# ─── Search Tests ───

class TestResearchSearch:
    @pytest.fixture
    def search_engine(self):
        papers = [
            Paper(title="Deadband Monads in Constraint Systems", content="Deadband monads formalize tolerance in constraint evaluation.",
                  keywords=["deadband", "monad"]),
            Paper(title="Eigenstructure of Lattice Shells", content="We compute the eigenstructure of hexagonal lattice shells.",
                  keywords=["eigenstructure", "lattice"]),
            Paper(title="Snap Dynamics in Forgemaster", content="Snap transitions occur when constraint tension exceeds the deadband threshold.",
                  keywords=["snap", "forgemaster"]),
        ]
        return ResearchSearch(papers)

    def test_keyword_search_finds_match(self, search_engine):
        results = search_engine.keyword_search("deadband")
        assert len(results) >= 2  # appears in two papers
        assert results[0].score >= results[1].score  # sorted by score

    def test_keyword_search_no_results(self, search_engine):
        results = search_engine.keyword_search("quantum teleportation")
        assert len(results) == 0

    def test_semantic_search(self, search_engine):
        results = search_engine.semantic_search("constraint lattice eigenstructure")
        assert len(results) > 0
        assert results[0].match_type == "semantic"

    def test_combined_search(self, search_engine):
        results = search_engine.search("lattice eigenstructure")
        assert len(results) > 0

    def test_add_and_search(self, search_engine):
        search_engine.add(Paper(title="Quantum Constraints", content="Quantum constraint systems."))
        results = search_engine.keyword_search("quantum")
        assert len(results) == 1

    def test_remove(self, search_engine):
        pid = search_engine.papers[0].id
        assert search_engine.remove(pid)
        assert len(search_engine) == 2

    def test_remove_nonexistent(self, search_engine):
        assert not search_engine.remove("nonexistent")

    def test_len(self, search_engine):
        assert len(search_engine) == 3

    def test_max_results(self, search_engine):
        results = search_engine.keyword_search("constraint", max_results=1)
        assert len(results) <= 1


# ─── Extractor Tests ───

class TestKeyExtractor:
    def test_extract_results(self):
        text = "We find that constraint deadbands improve convergence. Our results show 40% improvement."
        findings = KeyExtractor().extract_from_text(text)
        assert len(findings) > 0
        categories = {f.category for f in findings}
        assert "result" in categories

    def test_extract_methods(self):
        text = "We propose a novel eigenstructure decomposition. We use lattice constraints."
        findings = KeyExtractor().extract_from_text(text)
        method_findings = [f for f in findings if f.category == "method"]
        assert len(method_findings) > 0

    def test_extract_claims(self):
        text = "We show that the deadband monad forms a monoid. We prove convergence."
        findings = KeyExtractor().extract_from_text(text)
        claim_findings = [f for f in findings if f.category == "claim"]
        assert len(claim_findings) > 0

    def test_extract_observations(self):
        text = "Interestingly, the snap threshold depends on lattice geometry. We observe periodic bifurcation."
        findings = KeyExtractor().extract_from_text(text)
        obs = [f for f in findings if f.category == "observation"]
        assert len(obs) > 0

    def test_min_confidence_filter(self):
        ext = KeyExtractor(min_confidence=0.99)  # very high threshold
        text = "We find that things work. Our results show improvement."
        findings = ext.extract_from_text(text)
        # Should get very few or none
        assert all(f.confidence >= 0.99 for f in findings)

    def test_extract_from_paper(self):
        p = Paper(
            title="Test",
            content="We find that snaps are stable. We propose a new metric.",
            keywords=["snap"],
        )
        findings = KeyExtractor().extract_from_paper(p)
        assert len(findings) >= 2

    def test_extract_key_sentences(self):
        text = "We find that the system converges. Our results show stability. Interestingly, the rate doubles."
        ext = KeyExtractor()
        sentences = ext.extract_key_sentences(text, max_sentences=2)
        assert len(sentences) <= 2

    def test_deduplication(self):
        text = "We find that constraint systems converge. We find that constraint systems converge."
        findings = KeyExtractor().extract_from_text(text)
        # Dedup should reduce duplicates
        assert len(findings) <= 2

    def test_boost_for_key_terms(self):
        text = "We find that the forgemaster deadband lattice is stable."
        findings = KeyExtractor().extract_from_text(text)
        for f in findings:
            if "forgemaster" in f.text.lower():
                assert f.confidence >= 0.75  # boosted


# ─── Synthesizer Tests ───

class TestSynthesizer:
    def test_synthesize_papers(self):
        papers = [
            Paper(title="Deadband Theory", content="We find that deadbands improve stability. We propose a tolerance framework."),
            Paper(title="Lattice Dynamics", content="Our results show lattice convergence. We use hexagonal constraints."),
        ]
        synth = Synthesizer().synthesize_papers(papers)
        assert synth.source_count == 2
        assert len(synth.key_findings) > 0
        assert synth.summary
        assert "2 source" in synth.summary

    def test_synthesize_texts(self):
        texts = [
            "We find that snaps occur at thresholds. Our method uses eigenstructure analysis.",
            "We show that constraint tension matters. Interestingly, the dynamics are periodic.",
        ]
        synth = Synthesizer().synthesize_texts(texts, labels=["paper_a", "paper_b"])
        assert synth.source_count == 2
        assert synth.source_ids == ["paper_a", "paper_b"]

    def test_themes_identified(self):
        papers = [
            Paper(title="A", content="We find constraint deadband stability in lattice systems. Constraint lattice analysis."),
            Paper(title="B", content="We propose lattice constraint methods for eigenstructure. Eigenstructure lattice constraints."),
        ]
        synth = Synthesizer().synthesize_papers(papers)
        # Should identify recurring terms as themes
        assert len(synth.themes) > 0

    def test_empty_input(self):
        synth = Synthesizer().synthesize_papers([])
        assert synth.source_count == 0
        assert "No key findings" in synth.summary


# ─── Catalog Tests ───

class TestResearchCatalog:
    @pytest.fixture
    def catalog(self):
        cat = ResearchCatalog("test-catalog")
        cat.add_paper(Paper(
            title="Deadband Monad Proof",
            content="We prove the deadband monad forms a complete lattice.",
            keywords=["deadband", "proof"],
            topics=["formal-proofs"],
        ))
        cat.add_paper(Paper(
            title="Snap Dynamics",
            content="We find that snap transitions obey power-law scaling.",
            keywords=["snap", "dynamics"],
            topics=["dynamics"],
        ))
        cat.add_paper(Paper(
            title="Hexagonal Constraint Lattice",
            content="We propose hexagonal lattice structures for constraint systems.",
            keywords=["hexagonal", "lattice"],
            topics=["geometry", "constraint-theory"],
        ), topics=["geometry", "constraint-theory"])
        return cat

    def test_add_and_get(self, catalog):
        assert catalog.total_papers == 3
        papers = list(catalog.papers.values())
        assert any("Deadband" in p.title for p in papers)

    def test_remove(self, catalog):
        pid = list(catalog.papers.keys())[0]
        assert catalog.remove_paper(pid)
        assert catalog.total_papers == 2

    def test_remove_nonexistent(self, catalog):
        assert not catalog.remove_paper("fake-id")

    def test_topics(self, catalog):
        topics = catalog.list_topics()
        assert "formal-proofs" in topics
        assert "dynamics" in topics
        assert "geometry" in topics

    def test_get_papers_by_topic(self, catalog):
        proofs = catalog.get_papers_by_topic("formal-proofs")
        assert len(proofs) == 1
        assert "Deadband" in proofs[0].title

    def test_topic_stats(self, catalog):
        stats = catalog.topic_stats("formal-proofs")
        assert stats is not None
        assert stats.paper_count == 1
        assert stats.total_words > 0

    def test_topic_stats_nonexistent(self, catalog):
        assert catalog.topic_stats("nonexistent") is None

    def test_assign_topic(self, catalog):
        pid = list(catalog.papers.keys())[0]
        catalog.assign_topic(pid, "new-topic")
        assert "new-topic" in catalog.list_topics()

    def test_unassign_topic(self, catalog):
        pid = list(catalog.papers.keys())[0]
        # Assign then unassign
        catalog.assign_topic(pid, "temp-topic")
        catalog.unassign_topic(pid, "temp-topic")
        assert "temp-topic" not in catalog.list_topics()

    def test_search(self, catalog):
        results = catalog.search("lattice")
        assert len(results) > 0

    def test_extract_findings_all(self, catalog):
        findings = catalog.extract_findings()
        assert len(findings) > 0

    def test_extract_findings_by_topic(self, catalog):
        findings = catalog.extract_findings(topic="formal-proofs")
        assert len(findings) > 0

    def test_overview(self, catalog):
        overview = catalog.overview()
        assert "test-catalog" in overview
        assert "3" in overview  # 3 papers

    def test_total_words(self, catalog):
        assert catalog.total_words > 0

    def test_repr(self, catalog):
        r = repr(catalog)
        assert "test-catalog" in r

    def test_add_papers_batch(self):
        cat = ResearchCatalog("batch")
        papers = [
            Paper(title=f"Paper {i}", content=f"Content {i}")
            for i in range(5)
        ]
        ids = cat.add_papers(papers)
        assert len(ids) == 5
        assert cat.total_papers == 5


# ─── Integration Test ───

class TestIntegration:
    def test_full_pipeline(self):
        # Create catalog
        cat = ResearchCatalog("integration-test")

        # Add papers
        p1 = Paper(
            title="Constraint Deadband Theory",
            authors=["Ada"],
            content="We find that deadband constraints stabilize the lattice. "
                    "Our results show 50% improvement. We propose tolerance zones.",
            keywords=["deadband", "constraint", "lattice"],
            topics=["theory"],
        )
        p2 = Paper(
            title="Empirical Snap Measurements",
            authors=["Bob"],
            content="We observe snap transitions in hexagonal systems. "
                    "We use constraint monitors to measure tension. "
                    "Interestingly, snap frequency follows a power law.",
            keywords=["snap", "empirical", "measurement"],
            topics=["experiments"],
        )
        cat.add_paper(p1, topics=["theory"])
        cat.add_paper(p2, topics=["experiments"])

        # Search
        results = cat.keyword_search("constraint")
        assert len(results) >= 1

        # Semantic search
        sem = cat.semantic_search("lattice stability deadband")
        assert len(sem) >= 1

        # Extract findings
        findings = cat.extract_findings()
        assert len(findings) >= 3  # multiple findings from both papers

        # Synthesize
        synth = Synthesizer().synthesize_papers([p1, p2])
        assert synth.source_count == 2
        assert len(synth.themes) > 0

        # Catalog stats
        assert cat.total_papers == 2
        overview = cat.overview()
        assert "integration-test" in overview
