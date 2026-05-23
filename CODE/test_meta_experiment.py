#!/usr/bin/env python3
"""
Tests for meta-experiment.py — 30+ tests covering all major components.

Run with: python -m pytest test_meta_experiment.py -v
"""

import gzip
import json
import math
import os
import random
import string
import tempfile
from pathlib import Path

import pytest

# Import the module under test
import sys

sys.path.insert(0, os.path.dirname(__file__))
from meta_experiment import (
    AgentRun,
    KolmogorovEstimator,
    PatternDetector,
    SimulatedAgent,
    MetaExperiment,
    AnalysisUtils,
    ReportGenerator,
)


# ============================================================
# AgentRun dataclass tests
# ============================================================


class TestAgentRun:
    def test_default_run_id_generated(self):
        run = AgentRun()
        assert run.run_id != ""
        assert len(run.run_id) == 12

    def test_timestamp_auto_set(self):
        run = AgentRun()
        assert run.timestamp != ""
        assert "T" in run.timestamp  # ISO format

    def test_custom_fields(self):
        run = AgentRun(model="gpt-4", task="test", discoveries=["found X"])
        assert run.model == "gpt-4"
        assert run.task == "test"
        assert run.discoveries == ["found X"]

    def test_default_lists_empty(self):
        run = AgentRun()
        assert run.output_files == []
        assert run.discoveries == []
        assert run.patterns_found == []

    def test_k_complexity_default_zero(self):
        run = AgentRun()
        assert run.k_complexity == 0.0


# ============================================================
# KolmogorovEstimator tests
# ============================================================


class TestKolmogorovEstimator:
    def setup_method(self):
        self.est = KolmogorovEstimator()

    def test_empty_string_returns_zero(self):
        assert self.est.estimate("") == 0.0

    def test_repetitive_low_complexity(self):
        text = "a" * 10000
        ratio = self.est.estimate(text)
        assert ratio < 0.1  # highly compressible

    def test_random_high_complexity(self):
        rng = random.Random(42)
        text = "".join(rng.choices("abcdefghijklmnopqrstuvwxyz ", k=10000))
        ratio = self.est.estimate(text)
        assert ratio > 0.3  # less compressible

    def test_complexity_ordering(self):
        """Random text should have higher K than repetitive text."""
        repetitive = "hello world " * 1000
        rng = random.Random(99)
        random_text = "".join(rng.choices(string.ascii_lowercase + " ", k=len(repetitive)))
        assert self.est.estimate(random_text) > self.est.estimate(repetitive)

    def test_absolute_estimate_positive(self):
        assert self.est.absolute_estimate("some text here") > 0

    def test_absolute_estimate_empty(self):
        assert self.est.absolute_estimate("") == 0.0

    def test_entropy_estimate(self):
        # Single character = 0 entropy
        assert self.est.entropy_estimate("aaaa") == 0.0
        # Two equal characters = 1 bit
        e = self.est.entropy_estimate("ab")
        assert abs(e - 1.0) < 0.01

    def test_entropy_empty(self):
        assert self.est.entropy_estimate("") == 0.0

    def test_normalized_complexity_returns_float(self):
        result = self.est.normalized_complexity("test text")
        assert isinstance(result, float)
        assert 0.0 <= result

    def test_multi_method_estimate_keys(self):
        result = self.est.multi_method_estimate("hello world test")
        assert "gzip_ratio" in result
        assert "gzip_absolute" in result
        assert "shannon_entropy" in result
        assert "unique_token_ratio" in result

    def test_unique_token_ratio(self):
        result = KolmogorovEstimator._unique_token_ratio("a b c d a b")
        # unique: {a, b, c, d} = 4, total: 6
        assert abs(result - 4 / 6) < 0.01

    def test_unique_token_ratio_empty(self):
        assert KolmogorovEstimator._unique_token_ratio("") == 0.0


# ============================================================
# PatternDetector tests
# ============================================================


class TestPatternDetector:
    def setup_method(self):
        self.detector = PatternDetector()

    def test_detect_snap_with_snap_text(self):
        text = "The system quantizes values into a grid lattice with snapping."
        score = self.detector.detect_snap(text)
        assert score > 0.1

    def test_detect_snap_without_snap_text(self):
        text = "The cat sat on the mat and looked at the moon."
        score = self.detector.detect_snap(text)
        assert score < 0.3

    def test_detect_funnel_with_funnel_text(self):
        text = "All paths converge and funnel toward the central attractor basin."
        score = self.detector.detect_funnel(text)
        assert score > 0.1

    def test_detect_consensus_with_agreement_text(self):
        text = "The committee reached consensus through democratic voting and averaging."
        score = self.detector.detect_consensus(text)
        assert score > 0.1

    def test_detect_laman_with_rigidity_text(self):
        text = "The structural framework requires rigid constraints for graph stability."
        score = self.detector.detect_laman(text)
        assert score > 0.1

    def test_detect_tempo_with_rhythm_text(self):
        text = "The rhythm oscillates with periodic tempo and hierarchical scaling."
        score = self.detector.detect_tempo(text)
        assert score > 0.1

    def test_detect_csc_with_pipeline_text(self):
        text = "First collect data, then select the best, then compile the results."
        score = self.detector.detect_collect_select_compile(text)
        assert score > 0.1

    def test_detect_all_returns_six_scores(self):
        scores = self.detector.detect_all("some text about snapping and convergence")
        assert len(scores) == 6
        for v in scores.values():
            assert 0.0 <= v <= 1.0

    def test_dominant_pattern_returns_tuple(self):
        name, score = self.detector.dominant_pattern("snap snap quantize grid")
        assert isinstance(name, str)
        assert isinstance(score, float)
        assert name == "snap"

    def test_empty_text_gives_zero(self):
        for method in [
            self.detector.detect_snap,
            self.detector.detect_funnel,
            self.detector.detect_consensus,
            self.detector.detect_laman,
            self.detector.detect_tempo,
        ]:
            assert method("") == 0.0

    def test_scores_bounded_between_0_and_1(self):
        long_text = " ".join(
            ["snap quantize funnel converge consensus agree rigid structure tempo rhythm"] * 100
        )
        for score in self.detector.detect_all(long_text).values():
            assert 0.0 <= score <= 1.0


# ============================================================
# SimulatedAgent tests
# ============================================================


class TestSimulatedAgent:
    def test_generate_output_returns_string(self):
        output = SimulatedAgent.generate_output("biology")
        assert isinstance(output, str)
        assert len(output) > 50

    def test_output_deterministic_with_seed(self):
        o1 = SimulatedAgent.generate_output("biology", seed=42)
        o2 = SimulatedAgent.generate_output("biology", seed=42)
        assert o1 == o2

    def test_output_varies_with_seed(self):
        o1 = SimulatedAgent.generate_output("biology", seed=1)
        o2 = SimulatedAgent.generate_output("biology", seed=2)
        assert o1 != o2

    def test_all_domains_work(self):
        for domain in ["architecture", "biology", "economics", "poetry"]:
            output = SimulatedAgent.generate_output(domain)
            assert len(output) > 0

    def test_unknown_domain_uses_default(self):
        output = SimulatedAgent.generate_output("quantum_mechanics")
        assert len(output) > 0  # falls back to biology


# ============================================================
# MetaExperiment tests
# ============================================================


class TestMetaExperiment:
    def setup_method(self):
        self.tmpdir = tempfile.mkdtemp()
        self.exp = MetaExperiment(output_dir=self.tmpdir, use_simulated=True)

    def test_experiment_1_returns_expected_keys(self):
        result = self.exp.experiment_1_primitive_emergence("biology", n_agents=5)
        assert "domain" in result
        assert "n_agents" in result
        assert "primitive_frequencies" in result
        assert result["n_agents"] == 5

    def test_experiment_1_frequencies_normalized(self):
        result = self.exp.experiment_1_primitive_emergence("biology", n_agents=10)
        for freq in result["primitive_frequencies"].values():
            assert 0.0 <= freq <= 1.0

    def test_experiment_2_goldilocks_returns_curve(self):
        result = self.exp.experiment_2_goldilocks("test_task", epsilon_values=[0.1, 0.5, 0.9])
        assert "epsilon_quality" in result
        assert "optimal_epsilon" in result
        assert len(result["curve"]) == 3

    def test_experiment_2_goldilocks_quality_bounded(self):
        result = self.exp.experiment_2_goldilocks("test", epsilon_values=[0.1, 0.3, 0.5])
        for q in result["epsilon_quality"].values():
            assert 0.0 <= q <= 1.0

    def test_experiment_3_compression_with_runs(self):
        runs = [
            AgentRun(raw_output="Test output " * 20),
            AgentRun(raw_output="Different output " * 20),
        ]
        result = self.exp.experiment_3_compression_ratio(runs)
        assert "ratios" in result
        assert "statistics" in result
        assert "mean" in result["statistics"]

    def test_experiment_3_compression_without_runs(self):
        result = self.exp.experiment_3_compression_ratio()
        assert "ratios" in result

    def test_experiment_4_non_pre_calculability(self):
        result = self.exp.experiment_4_non_pre_calculability("test_task", n_runs=5)
        assert "total_diversity" in result
        assert "per_run" in result
        assert len(result["per_run"]) == 5
        assert 0.0 <= result["total_diversity"] <= 1.0

    def test_experiment_5_consensus_convergence(self):
        result = self.exp.experiment_5_consensus_convergence(
            models=["model_a", "model_b", "model_c"],
            question="What are the primitives?"
        )
        assert "rounds" in result
        assert "consensus_answer" in result
        assert "converged" in result

    def test_experiment_6_scaling_laws(self):
        result = self.exp.experiment_6_scaling_laws(agent_counts=[5, 10, 20])
        assert "scaling_data" in result
        assert len(result["scaling_data"]) == 3

    def test_experiment_7_strange_loop(self):
        result = self.exp.experiment_7_strange_loop()
        assert "self_description_score" in result
        assert "evidence" in result
        assert 0.0 <= result["self_description_score"] <= 1.0

    def test_run_all_completes(self):
        results = self.exp.run_all(
            domains=["biology"],
            agent_counts=[5, 10],
        )
        assert "experiments" in results
        assert "metadata" in results

    def test_run_all_saves_json(self):
        self.exp.run_all(domains=["biology"], agent_counts=[5])
        json_path = Path(self.tmpdir) / "full_results.json"
        assert json_path.exists()
        data = json.loads(json_path.read_text())
        assert "experiments" in data


# ============================================================
# AnalysisUtils tests
# ============================================================


class TestAnalysisUtils:
    def test_emergence_heatmap_data(self):
        results = {
            "bio": {"snap": 0.5, "funnel": 0.3},
            "arch": {"snap": 0.7, "funnel": 0.4},
        }
        heatmap = AnalysisUtils.emergence_heatmap_data(results)
        assert "snap" in heatmap
        assert len(heatmap["snap"]) == 2

    def test_goldilocks_curve_data(self):
        results = {"epsilon_quality": {0.1: 0.3, 0.5: 0.8, 0.9: 0.4}}
        curve = AnalysisUtils.goldilocks_curve_data(results)
        assert len(curve) == 3

    def test_scaling_fit_summary(self):
        result = AnalysisUtils.scaling_fit_summary(
            {"scaling_law_fit": {"exponent": 1.2, "interpretation": "super-linear"}}
        )
        assert "1.2" in result

    def test_diversity_report(self):
        report = AnalysisUtils.diversity_report(
            {"total_diversity": 0.8, "unique_discoveries_count": 40, "total_discoveries_count": 50, "avg_ncd": 0.6}
        )
        assert "0.800" in report
        assert "HIGH" in report

    def test_strange_loop_report(self):
        report = AnalysisUtils.strange_loop_report(
            {"self_description_score": 0.7, "evidence": ["a", "b"], "meta_patterns": {"snap": 0.5}}
        )
        assert "0.700" in report
        assert "STRONG" in report

    def test_consensus_trajectory(self):
        results = {"rounds": [{"round": 1, "agreement_level": 0.3}, {"round": 2, "agreement_level": 0.7}]}
        traj = AnalysisUtils.consensus_trajectory(results)
        assert len(traj) == 2
        assert traj[0] == (1, 0.3)


# ============================================================
# ReportGenerator tests
# ============================================================


class TestReportGenerator:
    def test_full_report_contains_headers(self):
        results = {
            "experiments": {
                "exp1_emergence": {"bio": {"primitive_frequencies": {"snap": 0.5}}},
                "exp2_goldilocks": {"optimal_epsilon": 0.3, "optimal_quality": 0.8, "curve": []},
                "exp3_compression": {"statistics": {"mean": 1.5, "median": 1.4, "stdev": 0.2, "min": 1.0, "max": 2.0}},
                "exp4_pre-calc": {"total_diversity": 0.7, "unique_discoveries_count": 30, "total_discoveries_count": 50, "avg_ncd": 0.5},
                "exp5_consensus": {"rounds": [], "converged": True},
                "exp6_scaling": {"scaling_data": [], "scaling_law_fit": {"exponent": 1.1, "interpretation": "super"}},
                "exp7_strange_loop": {"self_description_score": 0.5, "evidence": [], "meta_patterns": {}},
            }
        }
        rg = ReportGenerator(results)
        report = rg.full_report()
        assert "# Meta-Experiment" in report
        assert "Experiment 1" in report

    def test_save_report_creates_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            rg = ReportGenerator({"experiments": {}})
            path = rg.save_report(os.path.join(tmpdir, "report.md"))
            assert path.exists()
            content = path.read_text()
            assert "Meta-Experiment" in content


# ============================================================
# Integration / cross-cutting tests
# ============================================================


class TestIntegration:
    def test_detector_on_simulated_output(self):
        """Simulated output should trigger at least some pattern detectors."""
        output = SimulatedAgent.generate_output("biology", seed=42)
        detector = PatternDetector()
        scores = detector.detect_all(output)
        assert any(v > 0.05 for v in scores.values())

    def test_kolmogorov_on_simulated_output(self):
        """Simulated output should have reasonable complexity."""
        output = SimulatedAgent.generate_output("architecture", seed=7)
        est = KolmogorovEstimator()
        ratio = est.estimate(output)
        assert 0.1 < ratio < 1.0

    def test_ncd_distinguishes_similar_vs_different(self):
        """NCD should be lower for similar texts."""
        exp = MetaExperiment.__new__(MetaExperiment)
        exp.k_estimator = KolmogorovEstimator()
        similar1 = "The cat sat on the mat and looked at the moon."
        similar2 = "The cat sat on the mat and looked at the star."
        different = "Quantum chromodynamics explains quark confinement in hadrons."
        ncd_sim = exp._normalized_compression_distance(similar1, similar2)
        ncd_diff = exp._normalized_compression_distance(similar1, different)
        assert ncd_sim < ncd_diff

    def test_agreement_measurement(self):
        """Identical answers should give high agreement."""
        exp = MetaExperiment.__new__(MetaExperiment)
        exp.k_estimator = KolmogorovEstimator()
        answers = ["The five primitives are snap funnel consensus laman tempo"] * 3
        agreement = exp._measure_agreement(answers)
        assert agreement > 0.8

    def test_single_agent_emergence(self):
        """Single agent should still produce patterns."""
        exp = MetaExperiment(output_dir=tempfile.mkdtemp(), use_simulated=True)
        result = exp.experiment_1_primitive_emergence("biology", n_agents=1)
        assert len(result["per_agent_patterns"]) == 1
