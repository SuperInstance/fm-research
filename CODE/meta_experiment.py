#!/usr/bin/env python3
"""
meta-experiment.py — Run experiments ON the agent system itself.

This framework tests whether the five primitives (SNAP, FUNNEL, CONSENSUS,
LAMAN, TEMPO) and the COLLECT→SELECT→COMPILE pipeline emerge from multi-agent
runs across non-music domains. It also probes Goldilocks zones, compression
ratios, non-pre-calculability, consensus convergence, scaling laws, and
strange-loop self-description.

Designed for the SuperInstance/FM research programme.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import os
import random
import re
import statistics
import string
import sys
import time
import uuid
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class AgentRun:
    """Record of one agent's work session."""

    run_id: str = ""
    model: str = ""
    task: str = ""
    output_files: list[str] = field(default_factory=list)
    discoveries: list[str] = field(default_factory=list)
    patterns_found: list[str] = field(default_factory=list)
    k_complexity: float = 0.0
    seed: int = 0
    timestamp: str = ""
    raw_output: str = ""
    quality_score: float = 0.0
    duration_seconds: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.run_id:
            self.run_id = uuid.uuid4().hex[:12]
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Kolmogorov complexity estimator
# ---------------------------------------------------------------------------

class KolmogorovEstimator:
    """Estimate Kolmogorov complexity via compression."""

    def __init__(self, method: str = "gzip"):
        self.method = method

    def estimate(self, text: str) -> float:
        """Estimate K(text) via gzip compression ratio.

        Returns the ratio compressed_size / original_size, which
        approximates the relative Kolmogorov complexity.
        """
        if not text:
            return 0.0
        raw = text.encode("utf-8")
        compressed = gzip.compress(raw)
        return len(compressed) / len(raw)

    def absolute_estimate(self, text: str) -> float:
        """Return absolute compressed size as a proxy for K(text)."""
        if not text:
            return 0.0
        return float(len(gzip.compress(text.encode("utf-8"))))

    def normalized_complexity(self, text: str, reference: str = "") -> float:
        """Estimate K(text) normalized against a reference string.

        If no reference is provided, use the alphabet-repeated baseline.
        """
        if not text:
            return 0.0
        k_text = self.estimate(text)
        if reference:
            k_ref = self.estimate(reference)
        else:
            # Baseline: repeated pattern (maximum compressibility)
            baseline = ("abcdefghijklmnopqrstuvwxyz " * (len(text) // 27 + 1))[
                : len(text)
            ]
            k_ref = self.estimate(baseline)
        if k_ref == 0:
            return 0.0
        return k_text / k_ref

    def entropy_estimate(self, text: str) -> float:
        """Shannon entropy per character — another complexity proxy."""
        if not text:
            return 0.0
        counts = Counter(text)
        length = len(text)
        entropy = 0.0
        for count in counts.values():
            p = count / length
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy

    def multi_method_estimate(self, text: str) -> dict[str, float]:
        """Return estimates from multiple compression / complexity methods."""
        return {
            "gzip_ratio": self.estimate(text),
            "gzip_absolute": self.absolute_estimate(text),
            "shannon_entropy": self.entropy_estimate(text),
            "unique_token_ratio": self._unique_token_ratio(text),
        }

    @staticmethod
    def _unique_token_ratio(text: str) -> float:
        """Ratio of unique words to total words."""
        words = text.lower().split()
        if not words:
            return 0.0
        return len(set(words)) / len(words)


# ---------------------------------------------------------------------------
# Pattern detector
# ---------------------------------------------------------------------------

class PatternDetector:
    """Detect which of the 5 primitives appear in agent output.

    Each detector returns a float in [0, 1] indicating confidence that
    the text describes or embodies the given primitive.
    """

    # Keyword / phrase dictionaries for each primitive -----------------------

    SNAP_KEYWORDS: list[str] = [
        "snap", "quantize", "quantization", "grid", "discrete", "round",
        "lattice", "bin", "bucket", "threshold", "step function", "snap to",
        "nearest", "quantum", "quanta", "integer", "discretize", "discretization",
        "grid point", "lattice point", "step size", "resolution", "pixel",
        "voxel", "raster", "sampling", "sample rate", "bit depth",
        "snapping", "gridded", "discretized", "staircase", "quantized",
        "tonnetz", "pitch class", "chromatic", "semitone", "fret",
    ]

    FUNNEL_KEYWORDS: list[str] = [
        "funnel", "converge", "convergence", "attractor", "attract",
        "gravitational", "gravity", "basin of attraction", "pull",
        "narrow", "narrowing", "focus", "focusing", "center",
        "centripetal", "drift toward", "flow toward", "contract",
        "contraction", "condense", "compact", "compress toward",
        "potential well", "energy minimum", "gradient descent",
        "optimization", "minimize", "loss landscape", "basin",
        "fold", "folding", "collapse", "collapsing", "gather",
        "collect into", "channel", "directed flow",
    ]

    CONSENSUS_KEYWORDS: list[str] = [
        "consensus", "agree", "agreement", "vote", "voting", "average",
        "mean", "median", "majority", "unanimous", "quorum",
        "converge in opinion", "shared", "common ground", "alignment",
        "harmony", "synchronize", "synchronized", "coherent",
        "coherence", "mutual", "reciprocal", "collective",
        "democratic", "plural", "blend", "merge", "reconcile",
        "reconciliation", "common", "shared understanding",
        "group decision", "ensemble", "crowdsource",
    ]

    LAMAN_KEYWORDS: list[str] = [
        "rigid", "rigidity", "structure", "structural", "framework",
        "scaffold", "skeleton", "constraint", "stiffness", "stable",
        "stability", "fixed", "invariant", "minimal", "generically rigid",
        "graph", "edge", "vertex", "degrees of freedom", "overconstrained",
        "underconstrained", "truss", "lattice structure", "support",
        "spanning", "independent edges", "Laman", "minimally rigid",
        "isostatic", "redundancy", "redundant", "bridges",
        "tensegrity", "framework", "infinitesimal",
    ]

    TEMPO_KEYWORDS: list[str] = [
        "tempo", "rhythm", "beat", "pulse", "cycle", "period",
        "frequency", "oscillate", "oscillation", "periodic",
        "time scale", "scaling", "hierarchy", "hierarchical",
        "nested", "multi-scale", "fractal", "self-similar",
        "meter", "measure", "bar", "timing", "synchronization",
        "phase", "wavelength", "harmonic", "subharmonic",
        "accelerando", "ritardando", "rubato", "agogic",
        "polyrhythm", "cross-rhythm", "groove", "swing",
        "temporal scaling", "time hierarchy", " rhythmic",
    ]

    CSC_KEYWORDS: list[str] = [
        "collect", "gather", "compile", "select", "filter",
        "curate", "synthesize", "aggregate", "reduce", "summarize",
        "distill", "refine", "prune", "evaluate", "rank",
        "prioritize", "extract", "harvest", "assemble", "build",
        "construct", "compose", "merge", "integrate", "pipeline",
        "workflow", "stages", "phases", "iterations", "iterate",
        "funnel", "narrow", "final", "output", "deliver",
    ]

    def __init__(self, custom_keywords: dict[str, list[str]] | None = None):
        self._custom = custom_keywords or {}
        self._k_estimator = KolmogorovEstimator()

    # -- Public detection methods -------------------------------------------

    def detect_snap(self, text: str) -> float:
        """How much does this text describe quantization/grid snapping?"""
        return self._keyword_score(text, self.SNAP_KEYWORDS)

    def detect_funnel(self, text: str) -> float:
        """How much does this text describe gravitational convergence?"""
        return self._keyword_score(text, self.FUNNEL_KEYWORDS)

    def detect_consensus(self, text: str) -> float:
        """How much does this text describe agreement/averaging?"""
        return self._keyword_score(text, self.CONSENSUS_KEYWORDS)

    def detect_laman(self, text: str) -> float:
        """How much does this text describe structural rigidity?"""
        return self._keyword_score(text, self.LAMAN_KEYWORDS)

    def detect_tempo(self, text: str) -> float:
        """How much does this text describe temporal scaling/rhythm?"""
        return self._keyword_score(text, self.TEMPO_KEYWORDS)

    def detect_collect_select_compile(self, text: str) -> float:
        """How much does this text follow COLLECT→SELECT→COMPILE?"""
        csc = self._keyword_score(text, self.CSC_KEYWORDS)
        # Check for sequential presence of the three phases
        lower = text.lower()
        phases_present = 0
        if any(w in lower for w in ["collect", "gather", "harvest", "aggregate"]):
            phases_present += 1
        if any(w in lower for w in ["select", "filter", "prune", "rank", "curate"]):
            phases_present += 1
        if any(w in lower for w in ["compile", "synthesize", "assemble", "compose", "build"]):
            phases_present += 1
        phase_score = phases_present / 3.0
        return (csc + phase_score) / 2.0

    def detect_all(self, text: str) -> dict[str, float]:
        """Return scores for all primitives plus CSC pipeline."""
        return {
            "snap": self.detect_snap(text),
            "funnel": self.detect_funnel(text),
            "consensus": self.detect_consensus(text),
            "laman": self.detect_laman(text),
            "tempo": self.detect_tempo(text),
            "collect_select_compile": self.detect_collect_select_compile(text),
        }

    def dominant_pattern(self, text: str) -> tuple[str, float]:
        """Return (primitive_name, score) for the strongest match."""
        scores = self.detect_all(text)
        best = max(scores, key=scores.get)  # type: ignore[arg-type]
        return best, scores[best]

    # -- Internal helpers ---------------------------------------------------

    def _keyword_score(self, text: str, keywords: list[str]) -> float:
        """Score text against a keyword list.

        Uses a combination of:
        - Direct keyword hit ratio (normalized)
        - Contextual proximity bonuses
        """
        lower = text.lower()
        words = set(re.findall(r"\b\w+\b", lower))
        hits = sum(1 for kw in keywords if kw.lower() in lower)
        # Normalize: use sqrt to avoid saturation for long texts
        max_possible = min(len(keywords), len(words))
        if max_possible == 0:
            return 0.0
        raw_ratio = hits / max_possible
        # Apply sigmoid-like scaling to spread values in [0, 1]
        score = 1.0 - math.exp(-2.0 * raw_ratio)
        return min(score, 1.0)

    def _proximity_score(self, text: str, keywords: list[str], window: int = 50) -> float:
        """Bonus score for keyword co-occurrence within a window."""
        lower = text.lower()
        positions: dict[str, list[int]] = defaultdict(list)
        for kw in keywords:
            idx = 0
            while True:
                idx = lower.find(kw.lower(), idx)
                if idx == -1:
                    break
                positions[kw].append(idx)
                idx += 1
        # Count co-occurrences within window
        cooc = 0
        kws_present = [k for k in positions if positions[k]]
        for i in range(len(kws_present)):
            for j in range(i + 1, len(kws_present)):
                for pi in positions[kws_present[i]]:
                    for pj in positions[kws_present[j]]:
                        if abs(pi - pj) <= window:
                            cooc += 1
        if not kws_present:
            return 0.0
        max_pairs = len(kws_present) * (len(kws_present) - 1) / 2
        return min(cooc / max(max_pairs, 1), 1.0)


# ---------------------------------------------------------------------------
# Simulated agent runner (for experiments without live LLM access)
# ---------------------------------------------------------------------------

class SimulatedAgent:
    """Produce simulated agent output for experiment scaffolding.

    In production, this would be replaced with actual LLM calls.
    """

    DOMAIN_TEMPLATES: dict[str, dict[str, list[str]]] = {
        "architecture": {
            "snap": [
                "The building modules must snap to a standard grid of 1.2m intervals.",
                "Rooms are discretized into quantized volumes following a lattice structure.",
                "The floor plan uses a snap-to-grid approach for wall placement.",
            ],
            "funnel": [
                "Foot traffic naturally funnels through the central atrium, converging at the lobby.",
                "The design narrows from open workspace to focused concentration pods.",
                "Gravity-loaded columns pull structural forces toward foundation attractors.",
            ],
            "consensus": [
                "All stakeholders agreed on the median height for the new tower.",
                "The ensemble of design options was averaged to reach a consensus plan.",
                "Voting across the committee produced a unanimous structural decision.",
            ],
            "laman": [
                "The structural framework requires minimally rigid truss configurations.",
                "Laman-type constraints ensure the cantilever has exactly 2n-3 edges.",
                "The building's rigidity depends on the graph-theoretic stiffness of its supports.",
            ],
            "tempo": [
                "The building's rhythmic facade creates a temporal scaling from street to sky.",
                "Occupants experience nested periodic cycles: daily, weekly, seasonal.",
                "The structure oscillates in wind with a natural frequency of 0.5 Hz.",
            ],
        },
        "biology": {
            "snap": [
                "Gene expression quantizes into discrete on/off states like a binary grid.",
                "Protein folding snaps to lattice points in the energy landscape.",
                "The ribosome discretizes the continuous mRNA into amino acid quanta.",
            ],
            "funnel": [
                "The folding funnel pulls proteins toward their native energy minimum.",
                "Evolutionary fitness landscapes create basins of attraction for species.",
                "Signal transduction contracts the high-dimensional input into specific outputs.",
            ],
            "consensus": [
                "Quorum sensing allows bacteria to reach collective decisions.",
                "The ensemble of cells votes on developmental fate via averaged morphogen gradients.",
                "Neural populations reach consensus through synchronized firing patterns.",
            ],
            "laman": [
                "The cytoskeleton's structural rigidity comes from minimally rigid actin networks.",
                "Cell shape is maintained by a tensegrity framework of microtubules.",
                "The extracellular matrix provides scaffold constraints for tissue engineering.",
            ],
            "tempo": [
                "Circadian rhythms create nested temporal hierarchies of gene expression.",
                "The cell cycle exhibits periodic scaling from minutes to days.",
                "Heartbeat rhythms show self-similar fractal scaling across time scales.",
            ],
        },
        "economics": {
            "snap": [
                "Price levels snap to psychological thresholds: round numbers as grid points.",
                "Market tick sizes discretize the continuous value domain.",
                "Budget allocations are quantized to fixed percentage increments.",
            ],
            "funnel": [
                "Market equilibrium is an attractor basin where prices converge.",
                "Wealth naturally concentrates through gravitational funnel effects.",
                "Optimization algorithms narrow the search space toward profit maxima.",
            ],
            "consensus": [
                "Market prices emerge from the aggregate consensus of all participants.",
                "The Federal Reserve's decision averages across committee member votes.",
                "Prediction markets harvest collective wisdom through democratic participation.",
            ],
            "laman": [
                "The economic framework requires rigid institutional structures to prevent collapse.",
                "Minimal scaffold regulations provide structural rigidity without overconstraint.",
                "Supply chain graphs need isostatic connectivity: not too rigid, not too floppy.",
            ],
            "tempo": [
                "Business cycles exhibit temporal scaling from quarterly to decadal periods.",
                "Market rhythms oscillate with fractal self-similarity across time scales.",
                "Economic indicators pulse at nested hierarchical frequencies.",
            ],
        },
        "poetry": {
            "snap": [
                "Each syllable snaps to the metrical grid of iambic pentameter.",
                "The poem discretizes continuous emotion into quantized line breaks.",
                "Rhyme schemes quantize the space of possible sound combinations.",
            ],
            "funnel": [
                "The poem narrows from broad imagery to a sharp, convergent final line.",
                "Stanzas funnel the reader's attention toward the volta, the turning point.",
                "The narrative arc is an attractor, pulling every subplot toward resolution.",
            ],
            "consensus": [
                "The anthology represents a consensus of voices averaged into a cohesive whole.",
                "Metrical agreement between lines creates harmonic alignment.",
                "The workshop group voted to merge their individual drafts into one poem.",
            ],
            "laman": [
                "Sonnet form provides a structural framework: exactly 14 lines of rigid constraint.",
                "The poem's skeletal scaffold of enjambment creates minimal structural support.",
                "Formal constraints generate rigidity that paradoxically enables creative freedom.",
            ],
            "tempo": [
                "The rhythm accelerates through nested hierarchies of stress and release.",
                "Tempo shifts from allegro to adagio mirror the speaker's emotional arc.",
                "Polyrhythmic layering of alliteration and assonance creates temporal depth.",
            ],
        },
    }

    @classmethod
    def generate_output(
        cls,
        domain: str,
        seed: int = 0,
        inject_patterns: list[str] | None = None,
    ) -> str:
        """Generate simulated agent output for a given domain."""
        rng = random.Random(seed)
        domain_data = cls.DOMAIN_TEMPLATES.get(domain, cls.DOMAIN_TEMPLATES["biology"])

        paragraphs = []
        n_paragraphs = rng.randint(3, 7)
        for _ in range(n_paragraphs):
            sentences = []
            n_sentences = rng.randint(4, 8)
            for _ in range(n_sentences):
                pattern = rng.choice(
                    list(domain_data.keys())
                    if inject_patterns is None
                    else inject_patterns
                )
                template = rng.choice(domain_data[pattern])
                sentences.append(template)
            paragraphs.append(" ".join(sentences))

        # Add some generic filler
        filler = [
            f"In the domain of {domain}, we observe several interesting patterns.",
            "The system exhibits emergent behavior that was not explicitly programmed.",
            "Further analysis reveals deeper structural connections.",
            "This suggests a universal principle underlying the observed phenomena.",
            "The implications for the broader field are significant and warrant investigation.",
        ]
        for f in rng.sample(filler, min(rng.randint(1, 3), len(filler))):
            paragraphs.append(f)

        return "\n\n".join(paragraphs)


# ---------------------------------------------------------------------------
# Main experiment class
# ---------------------------------------------------------------------------

class MetaExperiment:
    """Run experiments ON the agent system itself."""

    def __init__(
        self,
        output_dir: str = "meta_experiment_results",
        pattern_detector: PatternDetector | None = None,
        k_estimator: KolmogorovEstimator | None = None,
        use_simulated: bool = True,
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.detector = pattern_detector or PatternDetector()
        self.k_estimator = k_estimator or KolmogorovEstimator()
        self.use_simulated = use_simulated
        self.runs: list[AgentRun] = []
        self.results: dict[str, Any] = {}

    # -- Experiment 1: Primitive Emergence ----------------------------------

    def experiment_1_primitive_emergence(
        self, domain: str, n_agents: int = 20
    ) -> dict[str, Any]:
        """Run agents on a NON-music domain. Check if 5 primitives emerge.

        Returns: {
            domain: str,
            n_agents: int,
            primitive_frequencies: {primitive: frequency_of_appearance},
            per_agent_patterns: [{run_id, patterns_found}],
            summary: str,
        }
        """
        results: dict[str, Any] = {
            "domain": domain,
            "n_agents": n_agents,
            "primitive_frequencies": defaultdict(int),
            "per_agent_patterns": [],
        }

        for i in range(n_agents):
            seed = random.randint(0, 2**31)
            if self.use_simulated:
                output = SimulatedAgent.generate_output(domain, seed=seed)
            else:
                output = f"[Live agent output for {domain}, seed={seed}]"

            scores = self.detector.detect_all(output)
            patterns_found = [p for p, s in scores.items() if s > 0.15]

            run = AgentRun(
                model="simulated" if self.use_simulated else "live",
                task=f"exp1_emergence_{domain}",
                output_files=[],
                discoveries=[],
                patterns_found=patterns_found,
                k_complexity=self.k_estimator.estimate(output),
                seed=seed,
                raw_output=output[:500],  # truncate for storage
            )
            self.runs.append(run)

            for p in patterns_found:
                results["primitive_frequencies"][p] += 1

            results["per_agent_patterns"].append(
                {"run_id": run.run_id, "patterns_found": patterns_found, "scores": scores}
            )

        # Normalize frequencies
        freq = results["primitive_frequencies"]
        results["primitive_frequencies"] = {
            p: freq.get(p, 0) / n_agents for p in
            ["snap", "funnel", "consensus", "laman", "tempo", "collect_select_compile"]
        }

        results["summary"] = (
            f"Domain '{domain}': Emergence rates — "
            + ", ".join(f"{p}={v:.2f}" for p, v in results["primitive_frequencies"].items())
        )

        self.results["experiment_1"] = results
        return results

    # -- Experiment 2: Goldilocks Zone --------------------------------------

    def experiment_2_goldilocks(
        self, task: str, epsilon_values: list[float] | None = None
    ) -> dict[str, Any]:
        """Vary ε (agent freedom) and measure output quality.

        Returns: {epsilon: quality_score, optimal_epsilon: float, curve: [...]}
        """
        if epsilon_values is None:
            epsilon_values = [0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0]

        results: dict[str, Any] = {"task": task, "epsilon_quality": {}, "curve": []}

        for eps in epsilon_values:
            quality_scores = []
            for trial in range(5):
                seed = random.randint(0, 2**31)
                rng = random.Random(seed)

                if self.use_simulated:
                    # Simulated quality: inverted-U curve around ε ≈ 0.3
                    # Quality = base + height * exp(-(eps - optimal)^2 / (2 * sigma^2))
                    optimal = 0.3
                    sigma = 0.25
                    base = 0.2
                    height = 0.7
                    noise = rng.gauss(0, 0.05)
                    quality = base + height * math.exp(
                        -((eps - optimal) ** 2) / (2 * sigma ** 2)
                    ) + noise
                    quality = max(0.0, min(1.0, quality))
                else:
                    quality = 0.5  # placeholder for live

                quality_scores.append(quality)

            avg_quality = statistics.mean(quality_scores)
            results["epsilon_quality"][eps] = avg_quality
            results["curve"].append({"epsilon": eps, "quality": avg_quality})

        # Find optimal
        best_eps = max(results["epsilon_quality"], key=results["epsilon_quality"].get)  # type: ignore[arg-type]
        results["optimal_epsilon"] = best_eps
        results["optimal_quality"] = results["epsilon_quality"][best_eps]
        results["summary"] = (
            f"Goldilocks zone for '{task}': optimal ε = {best_eps:.2f} "
            f"(quality = {results['optimal_quality']:.3f})"
        )

        self.results["experiment_2"] = results
        return results

    # -- Experiment 3: Compression Ratio ------------------------------------

    def experiment_3_compression_ratio(
        self, runs: list[AgentRun] | None = None
    ) -> dict[str, Any]:
        """Measure K(output)/K(rules) across multiple runs.

        Returns: {run_id: compression_ratio, statistics: {...}}
        """
        target_runs = runs if runs is not None else self.runs
        if not target_runs:
            # Generate synthetic runs
            target_runs = self._generate_synthetic_runs(15)

        # Define "rules" as a fixed short description
        rules_text = (
            "COLLECT data from multiple agents. SELECT the most promising patterns. "
            "COMPILE into a unified output. Apply SNAP quantization, FUNNEL convergence, "
            "CONSENSUS averaging, LAMAN rigidity constraints, and TEMPO scaling."
        )
        k_rules = self.k_estimator.absolute_estimate(rules_text)

        results: dict[str, Any] = {"ratios": {}, "statistics": {}}

        for run in target_runs:
            output = run.raw_output if run.raw_output else f"Output of {run.run_id}"
            # Extend to make it realistic
            output = output * 5
            k_output = self.k_estimator.absolute_estimate(output)
            ratio = k_output / k_rules if k_rules > 0 else 0.0
            results["ratios"][run.run_id] = ratio

        ratios = list(results["ratios"].values())
        if ratios:
            results["statistics"] = {
                "mean": statistics.mean(ratios),
                "median": statistics.median(ratios),
                "stdev": statistics.stdev(ratios) if len(ratios) > 1 else 0.0,
                "min": min(ratios),
                "max": max(ratios),
            }

        results["summary"] = (
            f"Compression ratios: mean={results['statistics'].get('mean', 0):.3f}, "
            f"range=[{results['statistics'].get('min', 0):.3f}, "
            f"{results['statistics'].get('max', 0):.3f}]"
        )

        self.results["experiment_3"] = results
        return results

    # -- Experiment 4: Non-Pre-Calculability --------------------------------

    def experiment_4_non_pre_calculability(
        self, task: str, n_runs: int = 10
    ) -> dict[str, Any]:
        """Same task, different seeds. Measure output diversity.

        Returns: {run_id: unique_discoveries, total_diversity: float}
        """
        results: dict[str, Any] = {
            "task": task,
            "n_runs": n_runs,
            "per_run": [],
        }

        all_discoveries: list[str] = []
        all_outputs: list[str] = []

        for i in range(n_runs):
            seed = random.randint(0, 2**31)
            if self.use_simulated:
                output = SimulatedAgent.generate_output("biology", seed=seed)
            else:
                output = f"[Live output {i} for task '{task}', seed={seed}]"

            # Extract "discoveries" — unique sentences
            sentences = [s.strip() for s in output.split(".") if len(s.strip()) > 20]
            discoveries = sentences[:5]  # top 5 as "discoveries"
            all_discoveries.extend(discoveries)
            all_outputs.append(output)

            run = AgentRun(
                model="simulated" if self.use_simulated else "live",
                task=f"exp4_pre-calc_{task}",
                discoveries=discoveries,
                seed=seed,
                raw_output=output[:500],
            )
            self.runs.append(run)

            results["per_run"].append({
                "run_id": run.run_id,
                "unique_discoveries": len(discoveries),
                "seed": seed,
            })

        # Measure diversity: how many unique discoveries vs total
        unique_set = set(d.lower().strip() for d in all_discoveries)
        total = len(all_discoveries)
        diversity = len(unique_set) / total if total > 0 else 0.0

        # Also measure pairwise output similarity via compression
        if len(all_outputs) > 1:
            pairwise_ncd = []
            for i in range(len(all_outputs)):
                for j in range(i + 1, len(all_outputs)):
                    ncd = self._normalized_compression_distance(
                        all_outputs[i], all_outputs[j]
                    )
                    pairwise_ncd.append(ncd)
            avg_ncd = statistics.mean(pairwise_ncd) if pairwise_ncd else 0.0
        else:
            avg_ncd = 0.0

        results["total_diversity"] = diversity
        results["unique_discoveries_count"] = len(unique_set)
        results["total_discoveries_count"] = total
        results["avg_ncd"] = avg_ncd
        results["summary"] = (
            f"Non-pre-calculability for '{task}': diversity={diversity:.3f}, "
            f"unique discoveries={len(unique_set)}/{total}, avg NCD={avg_ncd:.3f}"
        )

        self.results["experiment_4"] = results
        return results

    # -- Experiment 5: Consensus Convergence --------------------------------

    def experiment_5_consensus_convergence(
        self, models: list[str] | None = None, question: str = ""
    ) -> dict[str, Any]:
        """Multiple models answer same question. Measure consensus.

        Returns: {round: agreement_level, consensus_answer: str}
        """
        if models is None:
            models = ["gpt-4", "claude-3", "gemini-pro", "llama-3-70b", "mixtral-8x7b"]
        if not question:
            question = "What are the fundamental structural primitives underlying complex systems?"

        results: dict[str, Any] = {
            "question": question,
            "models": models,
            "rounds": [],
        }

        # Simulate multi-round convergence
        n_rounds = 5
        agreement_levels = []
        answers_per_round: list[list[str]] = []

        for round_num in range(n_rounds):
            answers = []
            for model in models:
                if self.use_simulated:
                    # Simulate: answers converge over rounds
                    rng = random.Random(hash(model) + round_num)
                    base_answers = [
                        "The five primitives are SNAP, FUNNEL, CONSENSUS, LAMAN, and TEMPO.",
                        "Complex systems exhibit quantization, convergence, agreement, rigidity, and rhythm.",
                        "Structural primitives include grid-based discretization and gravitational attraction.",
                        "The key patterns are snap, funnel, consensus, laman, and tempo scaling.",
                        "I observe discrete snapping, funnel convergence, collective agreement, rigid frameworks, and temporal scaling.",
                    ]
                    # Converge toward the first answer over rounds
                    convergence_prob = (round_num + 1) / n_rounds
                    if rng.random() < convergence_prob:
                        answer = base_answers[0]
                    else:
                        answer = rng.choice(base_answers[1:])
                else:
                    answer = f"[Live answer from {model}]"

                answers.append(answer)

            answers_per_round.append(answers)

            # Measure agreement via keyword overlap
            agreement = self._measure_agreement(answers)
            agreement_levels.append(agreement)

            results["rounds"].append({
                "round": round_num + 1,
                "agreement_level": agreement,
                "answers": answers[:3],  # store first 3 for brevity
            })

        # Find consensus answer
        final_answers = answers_per_round[-1]
        answer_counts = Counter(final_answers)
        consensus_answer = answer_counts.most_common(1)[0][0] if answer_counts else ""

        results["consensus_answer"] = consensus_answer
        results["final_agreement"] = agreement_levels[-1]
        results["convergence_trajectory"] = agreement_levels
        results["converged"] = agreement_levels[-1] > 0.8
        results["summary"] = (
            f"Consensus {'converged' if results['converged'] else 'did not converge'} "
            f"after {n_rounds} rounds (agreement: {agreement_levels[-1]:.3f})"
        )

        self.results["experiment_5"] = results
        return results

    # -- Experiment 6: Scaling Laws -----------------------------------------

    def experiment_6_scaling_laws(
        self, agent_counts: list[int] | None = None
    ) -> dict[str, Any]:
        """Vary agent count. Measure discovery rate.

        Returns: {n_agents: discoveries_per_agent, total_novel: int}
        """
        if agent_counts is None:
            agent_counts = [1, 5, 10, 20, 50, 100]

        results: dict[str, Any] = {"scaling_data": [], "scaling_law_fit": {}}

        all_discoveries_by_size: dict[int, list[str]] = {}

        for n in agent_counts:
            discoveries = []
            per_agent_counts = []

            for i in range(n):
                seed = random.randint(0, 2**31)
                if self.use_simulated:
                    output = SimulatedAgent.generate_output(
                        random.choice(["architecture", "biology", "economics", "poetry"]),
                        seed=seed,
                    )
                else:
                    output = f"[Live output for agent {i} with n_agents={n}]"

                # Extract discoveries
                sentences = [s.strip() for s in output.split(".") if len(s.strip()) > 20]
                agent_disc = sentences[:3]
                discoveries.extend(agent_disc)
                per_agent_counts.append(len(agent_disc))

            unique = set(d.lower().strip() for d in discoveries)
            all_discoveries_by_size[n] = discoveries

            dpa = statistics.mean(per_agent_counts) if per_agent_counts else 0
            results["scaling_data"].append({
                "n_agents": n,
                "total_discoveries": len(discoveries),
                "unique_discoveries": len(unique),
                "discoveries_per_agent": dpa,
                "novelty_ratio": len(unique) / max(len(discoveries), 1),
            })

        # Fit a simple power law: discoveries ∝ n^α
        ns = [d["n_agents"] for d in results["scaling_data"]]
        totals = [d["unique_discoveries"] for d in results["scaling_data"]]

        if len(ns) >= 2 and all(t > 0 for t in totals) and all(n > 1 for n in ns):
            log_ns = [math.log(n) for n in ns]
            log_ts = [math.log(t) for t in totals]
            n_pts = len(log_ns)
            sum_xy = sum(x * y for x, y in zip(log_ns, log_ts))
            sum_x = sum(log_ns)
            sum_y = sum(log_ts)
            sum_x2 = sum(x ** 2 for x in log_ns)
            denom = n_pts * sum_x2 - sum_x ** 2
            if denom != 0:
                alpha = (n_pts * sum_xy - sum_x * sum_y) / denom
            else:
                alpha = 1.0
            results["scaling_law_fit"] = {
                "exponent": alpha,
                "interpretation": (
                    f"Discoveries scale as n^{alpha:.2f} — "
                    f"{'super' if alpha > 1.0 else 'sub' if alpha < 1.0 else 'linearly'}"
                ),
            }

        total_novel = sum(d["unique_discoveries"] for d in results["scaling_data"])
        results["total_novel"] = total_novel
        results["summary"] = (
            f"Scaling: {total_novel} total novel discoveries across agent counts {agent_counts}. "
            + results["scaling_law_fit"].get("interpretation", "Insufficient data for fit.")
        )

        self.results["experiment_6"] = results
        return results

    # -- Experiment 7: Strange Loop -----------------------------------------

    def experiment_7_strange_loop(self, system_output: str = "") -> dict[str, Any]:
        """Check if output describes its own creation process.

        Returns: {self_description_score: float, evidence: list}
        """
        if not system_output:
            # Generate a sample output that might contain self-reference
            if self.use_simulated:
                system_output = (
                    "This system operates by collecting multiple agent outputs, "
                    "selecting the most promising patterns, and compiling them into "
                    "a unified analysis. The framework itself was generated through "
                    "the same COLLECT-SELECT-COMPILE pipeline it describes. "
                    "The agent that wrote this code was itself produced by a process "
                    "of multi-agent consensus. The quantization grid (SNAP) that "
                    "constrains the output was chosen by the very system being analyzed. "
                    "The structural rigidity (LAMAN) of this document reflects the "
                    "constraints imposed by the framework. This is a strange loop: "
                    "the description describes itself being described. "
                    "The tempo at which this text was generated mirrors the temporal "
                    "scaling patterns it identifies. The funnel that narrows options "
                    "is itself an option narrowed by a funnel."
                )
            else:
                system_output = "[Live system output for strange loop analysis]"

        results: dict[str, Any] = {
            "self_description_score": 0.0,
            "evidence": [],
            "meta_patterns": {},
        }

        # 1. Self-reference detection
        self_ref_indicators = [
            "this system", "this framework", "this code", "this document",
            "this analysis", "itself", "its own", "the very system",
            "the same process", "self-referential", "strange loop",
            "describes itself", "reflects the", "mirrors the",
            "was generated by", "was produced by", "created its own",
            "the process that", "recursive", "meta-level",
        ]

        lower = system_output.lower()
        self_ref_count = sum(1 for ind in self_ref_indicators if ind in lower)
        self_ref_score = min(self_ref_count / max(len(self_ref_indicators), 1), 1.0)

        evidence_found = [
            ind for ind in self_ref_indicators if ind in lower
        ]
        results["evidence"].extend(
            [f"Self-reference: '{e}'" for e in evidence_found]
        )

        # 2. Process-describes-process detection
        process_patterns = [
            (r"generat\w+.*generat\w+", "generation describing generation"),
            (r"collect\w*.*select\w*.*compil\w*", "full CSC pipeline self-reference"),
            (r"snap.*constrain\w+.*chose\w+", "SNAP constraints chosen by system"),
            (r"funnel.*narrow.*funnel", "funnel describing funnel"),
            (r"process.*process", "process referencing process"),
        ]

        process_score = 0.0
        for pattern, description in process_patterns:
            if re.search(pattern, lower):
                process_score += 0.2
                results["evidence"].append(f"Process loop: {description}")

        # 3. Meta-pattern detection (primitives describing themselves)
        primitive_scores = self.detector.detect_all(system_output)
        results["meta_patterns"] = primitive_scores

        # Primitives present in the output that also describe the system
        meta_present = sum(1 for s in primitive_scores.values() if s > 0.1)
        meta_score = meta_present / 6.0

        # Composite score
        results["self_description_score"] = (
            0.4 * self_ref_score + 0.3 * min(process_score, 1.0) + 0.3 * meta_score
        )

        results["summary"] = (
            f"Strange loop score: {results['self_description_score']:.3f} "
            f"({len(evidence_found)} self-references, "
            f"{meta_present}/6 meta-patterns)"
        )

        self.results["experiment_7"] = results
        return results

    # -- Run all experiments ------------------------------------------------

    def run_all(
        self,
        domains: list[str] | None = None,
        agent_counts: list[int] | None = None,
    ) -> dict[str, Any]:
        """Run complete experimental battery. Returns full results."""
        if domains is None:
            domains = ["architecture", "biology", "economics", "poetry"]

        full_results: dict[str, Any] = {
            "metadata": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "simulated": self.use_simulated,
                "domains": domains,
            },
            "experiments": {},
        }

        print("=" * 70)
        print("META-EXPERIMENT: Full Experimental Battery")
        print("=" * 70)

        # Experiment 1: Primitive emergence across domains
        print("\n[Experiment 1] Primitive Emergence")
        emergence_results = {}
        for domain in domains:
            print(f"  Domain: {domain}...", end=" ")
            r = self.experiment_1_primitive_emergence(domain, n_agents=20)
            emergence_results[domain] = r
            print(f"done ({r['summary']})")
        full_results["experiments"]["exp1_emergence"] = emergence_results

        # Experiment 2: Goldilocks zone
        print("\n[Experiment 2] Goldilocks Zone")
        r2 = self.experiment_2_goldilocks("multi_agent_synthesis")
        print(f"  {r2['summary']}")
        full_results["experiments"]["exp2_goldilocks"] = r2

        # Experiment 3: Compression ratio
        print("\n[Experiment 3] Compression Ratio")
        r3 = self.experiment_3_compression_ratio()
        print(f"  {r3['summary']}")
        full_results["experiments"]["exp3_compression"] = r3

        # Experiment 4: Non-pre-calculability
        print("\n[Experiment 4] Non-Pre-Calculability")
        r4 = self.experiment_4_non_pre_calculability("open_ended_discovery")
        print(f"  {r4['summary']}")
        full_results["experiments"]["exp4_pre-calc"] = r4

        # Experiment 5: Consensus convergence
        print("\n[Experiment 5] Consensus Convergence")
        r5 = self.experiment_5_consensus_convergence()
        print(f"  {r5['summary']}")
        full_results["experiments"]["exp5_consensus"] = r5

        # Experiment 6: Scaling laws
        print("\n[Experiment 6] Scaling Laws")
        r6 = self.experiment_6_scaling_laws(agent_counts)
        print(f"  {r6['summary']}")
        full_results["experiments"]["exp6_scaling"] = r6

        # Experiment 7: Strange loop
        print("\n[Experiment 7] Strange Loop")
        r7 = self.experiment_7_strange_loop()
        print(f"  {r7['summary']}")
        full_results["experiments"]["exp7_strange_loop"] = r7

        # Save results
        results_path = self.output_dir / "full_results.json"
        with open(results_path, "w") as f:
            json.dump(full_results, f, indent=2, default=str)

        print(f"\nResults saved to {results_path}")
        print("=" * 70)
        print("ALL EXPERIMENTS COMPLETE")
        print("=" * 70)

        self.results["full"] = full_results
        return full_results

    # -- Helper methods -----------------------------------------------------

    def _generate_synthetic_runs(self, n: int) -> list[AgentRun]:
        """Generate synthetic AgentRuns for testing."""
        runs = []
        for i in range(n):
            seed = random.randint(0, 2**31)
            domain = random.choice(["architecture", "biology", "economics", "poetry"])
            output = SimulatedAgent.generate_output(domain, seed=seed)
            run = AgentRun(
                model="synthetic",
                task=f"synthetic_{domain}",
                raw_output=output[:500],
                k_complexity=self.k_estimator.estimate(output),
                seed=seed,
            )
            runs.append(run)
        return runs

    def _normalized_compression_distance(self, s1: str, s2: str) -> float:
        """Compute Normalized Compression Distance between two strings."""
        c1 = len(gzip.compress(s1.encode("utf-8")))
        c2 = len(gzip.compress(s2.encode("utf-8")))
        c12 = len(gzip.compress((s1 + s2).encode("utf-8")))
        if max(c1, c2) == 0:
            return 0.0
        return (c12 - min(c1, c2)) / max(c1, c2)

    def _measure_agreement(self, answers: list[str]) -> float:
        """Measure agreement level among a list of answers.

        Uses keyword overlap and NCD-based similarity.
        """
        if len(answers) < 2:
            return 1.0

        # Keyword overlap approach
        answer_words = [set(re.findall(r"\b\w+\b", a.lower())) for a in answers]
        common_words = set.intersection(*answer_words) if answer_words else set()
        all_words = set.union(*answer_words) if answer_words else set()

        if not all_words:
            return 0.0

        jaccard = len(common_words) / len(all_words)

        # NCD approach
        ncd_pairs = []
        for i in range(len(answers)):
            for j in range(i + 1, len(answers)):
                ncd = self._normalized_compression_distance(answers[i], answers[j])
                ncd_pairs.append(1.0 - ncd)  # invert: low NCD = high similarity

        avg_ncd_sim = statistics.mean(ncd_pairs) if ncd_pairs else 0.0

        return 0.5 * jaccard + 0.5 * avg_ncd_sim


# ---------------------------------------------------------------------------
# Analysis utilities
# ---------------------------------------------------------------------------

class AnalysisUtils:
    """Post-experiment analysis and visualization helpers."""

    @staticmethod
    def emergence_heatmap_data(
        results: dict[str, dict[str, float]]
    ) -> dict[str, list[float]]:
        """Convert emergence results into heatmap-ready data.

        Input: {domain: {primitive: frequency}}
        Output: {primitive: [frequency_per_domain]}
        """
        primitives = ["snap", "funnel", "consensus", "laman", "tempo", "collect_select_compile"]
        heatmap: dict[str, list[float]] = {p: [] for p in primitives}
        for domain_data in results.values():
            for p in primitives:
                heatmap[p].append(domain_data.get(p, 0.0))
        return heatmap

    @staticmethod
    def goldilocks_curve_data(results: dict[str, Any]) -> list[tuple[float, float]]:
        """Extract (epsilon, quality) pairs from goldilocks results."""
        return [
            (float(eps), quality)
            for eps, quality in results.get("epsilon_quality", {}).items()
        ]

    @staticmethod
    def scaling_fit_summary(results: dict[str, Any]) -> str:
        """Human-readable summary of scaling law fit."""
        fit = results.get("scaling_law_fit", {})
        if not fit:
            return "No scaling law fit available."
        return (
            f"Scaling exponent: {fit.get('exponent', 'N/A')}\n"
            f"Interpretation: {fit.get('interpretation', 'N/A')}"
        )

    @staticmethod
    def diversity_report(results: dict[str, Any]) -> str:
        """Human-readable diversity report from non-pre-calculability experiment."""
        diversity = results.get("total_diversity", 0)
        unique = results.get("unique_discoveries_count", 0)
        total = results.get("total_discoveries_count", 0)
        ncd = results.get("avg_ncd", 0)
        return (
            f"Output Diversity Report\n"
            f"  Diversity ratio: {diversity:.3f}\n"
            f"  Unique discoveries: {unique} / {total}\n"
            f"  Avg Normalized Compression Distance: {ncd:.3f}\n"
            f"  {'HIGH' if diversity > 0.7 else 'MODERATE' if diversity > 0.4 else 'LOW'} diversity"
        )

    @staticmethod
    def strange_loop_report(results: dict[str, Any]) -> str:
        """Human-readable strange loop analysis."""
        score = results.get("self_description_score", 0)
        n_evidence = len(results.get("evidence", []))
        meta = results.get("meta_patterns", {})
        return (
            f"Strange Loop Analysis\n"
            f"  Self-description score: {score:.3f}\n"
            f"  Evidence items: {n_evidence}\n"
            f"  Meta-patterns: {', '.join(f'{k}={v:.2f}' for k, v in meta.items())}\n"
            f"  {'STRONG' if score > 0.6 else 'MODERATE' if score > 0.3 else 'WEAK'} strange loop detected"
        )

    @staticmethod
    def consensus_trajectory(results: dict[str, Any]) -> list[tuple[int, float]]:
        """Extract (round, agreement) trajectory from consensus results."""
        return [
            (r["round"], r["agreement_level"]) for r in results.get("rounds", [])
        ]


# ---------------------------------------------------------------------------
# Report generator
# ---------------------------------------------------------------------------

class ReportGenerator:
    """Generate human-readable reports from experiment results."""

    def __init__(self, results: dict[str, Any]):
        self.results = results

    def full_report(self) -> str:
        """Generate a comprehensive markdown report."""
        lines = [
            "# Meta-Experiment Results Report",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
        ]

        exps = self.results.get("experiments", self.results)

        # Experiment 1
        if "exp1_emergence" in exps:
            lines.append("## Experiment 1: Primitive Emergence")
            lines.append("")
            for domain, data in exps["exp1_emergence"].items():
                lines.append(f"### Domain: {domain}")
                for prim, freq in data.get("primitive_frequencies", {}).items():
                    bar = "█" * int(freq * 20)
                    lines.append(f"  - **{prim}**: {freq:.3f} {bar}")
                lines.append("")
            lines.append("")

        # Experiment 2
        if "exp2_goldilocks" in exps:
            g = exps["exp2_goldilocks"]
            lines.append("## Experiment 2: Goldilocks Zone")
            lines.append("")
            lines.append(f"Optimal ε: **{g.get('optimal_epsilon', 'N/A')}**")
            lines.append(f"Optimal quality: **{g.get('optimal_quality', 'N/A'):.3f}**")
            lines.append("")
            lines.append("| ε | Quality |")
            lines.append("|---|--------|")
            for point in g.get("curve", []):
                lines.append(f"| {point['epsilon']:.2f} | {point['quality']:.3f} |")
            lines.append("")

        # Experiment 3
        if "exp3_compression" in exps:
            c = exps["exp3_compression"]
            lines.append("## Experiment 3: Compression Ratio")
            lines.append("")
            stats = c.get("statistics", {})
            lines.append(f"- Mean ratio: {stats.get('mean', 'N/A')}")
            lines.append(f"- Median ratio: {stats.get('median', 'N/A')}")
            lines.append(f"- Std dev: {stats.get('stdev', 'N/A')}")
            lines.append(f"- Range: [{stats.get('min', 'N/A')}, {stats.get('max', 'N/A')}]")
            lines.append("")

        # Experiment 4
        if "exp4_pre-calc" in exps:
            lines.append("## Experiment 4: Non-Pre-Calculability")
            lines.append("")
            lines.append(AnalysisUtils.diversity_report(exps["exp4_pre-calc"]))
            lines.append("")

        # Experiment 5
        if "exp5_consensus" in exps:
            con = exps["exp5_consensus"]
            lines.append("## Experiment 5: Consensus Convergence")
            lines.append("")
            trajectory = AnalysisUtils.consensus_trajectory(con)
            for rnd, agreement in trajectory:
                bar = "●" * int(agreement * 20)
                lines.append(f"  Round {rnd}: {agreement:.3f} {bar}")
            lines.append(f"  Converged: {'Yes' if con.get('converged') else 'No'}")
            lines.append("")

        # Experiment 6
        if "exp6_scaling" in exps:
            lines.append("## Experiment 6: Scaling Laws")
            lines.append("")
            lines.append(AnalysisUtils.scaling_fit_summary(exps["exp6_scaling"]))
            lines.append("")
            lines.append("| N Agents | Unique | DPA | Novelty |")
            lines.append("|----------|--------|-----|---------|")
            for d in exps["exp6_scaling"].get("scaling_data", []):
                lines.append(
                    f"| {d['n_agents']} | {d['unique_discoveries']} | "
                    f"{d['discoveries_per_agent']:.2f} | {d['novelty_ratio']:.3f} |"
                )
            lines.append("")

        # Experiment 7
        if "exp7_strange_loop" in exps:
            lines.append("## Experiment 7: Strange Loop")
            lines.append("")
            lines.append(AnalysisUtils.strange_loop_report(exps["exp7_strange_loop"]))
            lines.append("")

        return "\n".join(lines)

    def save_report(self, path: str | Path = "meta_experiment_report.md") -> Path:
        """Save report to file."""
        path = Path(path)
        path.write_text(self.full_report())
        return path


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    """Run the meta-experiment from command line."""
    import argparse

    parser = argparse.ArgumentParser(description="Meta-Experiment Framework")
    parser.add_argument(
        "--output-dir",
        default="meta_experiment_results",
        help="Directory for output files",
    )
    parser.add_argument(
        "--no-simulated",
        action="store_true",
        help="Disable simulated output (require live agents)",
    )
    parser.add_argument(
        "--domains",
        nargs="+",
        default=["architecture", "biology", "economics", "poetry"],
        help="Domains for emergence experiment",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate markdown report",
    )
    parser.add_argument(
        "--single",
        choices=["1", "2", "3", "4", "5", "6", "7"],
        help="Run a single experiment by number",
    )

    args = parser.parse_args()

    exp = MetaExperiment(
        output_dir=args.output_dir,
        use_simulated=not args.no_simulated,
    )

    if args.single:
        exp_num = int(args.single)
        if exp_num == 1:
            for domain in args.domains:
                exp.experiment_1_primitive_emergence(domain)
        elif exp_num == 2:
            exp.experiment_2_goldilocks("multi_agent_synthesis")
        elif exp_num == 3:
            exp.experiment_3_compression_ratio()
        elif exp_num == 4:
            exp.experiment_4_non_pre_calculability("open_ended_discovery")
        elif exp_num == 5:
            exp.experiment_5_consensus_convergence()
        elif exp_num == 6:
            exp.experiment_6_scaling_laws()
        elif exp_num == 7:
            exp.experiment_7_strange_loop()
    else:
        results = exp.run_all(domains=args.domains)

    if args.report:
        rg = ReportGenerator(exp.results)
        report_path = rg.save_report(Path(args.output_dir) / "report.md")
        print(f"\nReport saved to {report_path}")


if __name__ == "__main__":
    main()
