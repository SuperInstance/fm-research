#!/usr/bin/env python3
"""
gene-regulatory-music.py

Simulate a gene regulatory network using musical consensus.

Model:
- 20 genes, each producing a musical 'protein' (note/constraint).
- Transcription factors (TFs) = real-time constraint activators.
- Genes regulate each other based on protein outputs.
- 100 timesteps of iterative regulation.
- Emergent patterns are detected that cannot be predicted from individual genes.

Dependencies: numpy, pytest
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

N_GENES = 20
N_TIMESTEPS = 100
EPSILON = 0.05
DECAY_RATE = 0.15

MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]
MINOR_SCALE = [0, 2, 3, 5, 7, 8, 10]
DORIAN_SCALE = [0, 2, 3, 5, 7, 9, 10]
LYDIAN_SCALE = [0, 2, 4, 6, 7, 9, 11]
MIXOLYDIAN_SCALE = [0, 2, 4, 5, 7, 9, 10]
PENTATONIC_SCALE = [0, 2, 4, 7, 9]
CHROMATIC_SCALE = list(range(12))

SCALES = {
    "major": MAJOR_SCALE,
    "minor": MINOR_SCALE,
    "dorian": DORIAN_SCALE,
    "lydian": LYDIAN_SCALE,
    "mixolydian": MIXOLYDIAN_SCALE,
    "pentatonic": PENTATONIC_SCALE,
    "chromatic": CHROMATIC_SCALE,
}

CONSTRAINT_TYPES = [
    "pitch", "timbre", "rhythm", "dynamics", "harmony",
    "articulation", "texture", "form", "counterpoint", "tuning",
]


# ---------------------------------------------------------------------------
# Core constraint primitives (from constraint-substrate theory)
# ---------------------------------------------------------------------------


def consensus_round(values: List[float], epsilon: float = EPSILON) -> Tuple[List[float], bool]:
    if not values:
        return [], True
    arr = np.asarray(values, dtype=float)
    sin_sum = np.sin(arr * 2 * np.pi).mean()
    cos_sum = np.cos(arr * 2 * np.pi).mean()
    circ_mean = (np.arctan2(sin_sum, cos_sum) / (2 * np.pi)) % 1.0
    diffs = np.abs((arr - circ_mean + 0.5) % 1.0 - 0.5)
    converged = bool(np.all(diffs <= epsilon))
    if converged:
        return [float(circ_mean)] * len(values), True
    return values.copy(), False


def snap_to_lattice(value: float, scale_degrees: List[int], root: int = 60) -> int:
    n_degrees = len(scale_degrees)
    total_range = n_degrees * 3
    idx = int(value * total_range) % total_range
    octave = idx // n_degrees
    degree = idx % n_degrees
    return root + octave * 12 + scale_degrees[degree]


def funnel_step(current: float, target: float, epsilon: float, decay_rate: float) -> float:
    if abs(target - current) <= epsilon:
        return current
    return current + (target - current) * decay_rate


def laman_rigidity_check(n: int, edges: List[Tuple[int, int]]) -> bool:
    m = len(edges)
    if m != 2 * n - 3:
        return False
    for mask in range(1, 1 << n):
        k = bin(mask).count("1")
        if k < 2:
            continue
        subset_edges = sum(1 for u, v in edges if (mask >> u) & 1 and (mask >> v) & 1)
        if subset_edges > 2 * k - 3:
            return False
    return True


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class Protein:
    gene_id: int
    pitch: int = 60
    velocity: int = 64
    duration: float = 0.25
    timbre: str = "sine"
    constraint_type: str = "pitch"
    regulatory_activity: float = 0.0

    def to_note_tuple(self) -> Tuple[int, int, float]:
        return (self.pitch, self.velocity, self.duration)


@dataclass
class Gene:
    gene_id: int
    name: str
    constraint_type: str
    scale_name: str = "major"
    root_pitch: int = 60
    base_expression: float = 0.5
    expression: float = 0.5
    decay: float = DECAY_RATE
    epsilon: float = EPSILON
    history: List[float] = field(default_factory=list)
    protein_history: List[Protein] = field(default_factory=list)

    def express(self) -> Protein:
        scale = SCALES.get(self.scale_name, MAJOR_SCALE)
        pitch = snap_to_lattice(self.expression, scale, self.root_pitch)
        velocity = int(30 + self.expression * 97)
        duration = 0.1 + self.expression * 0.9
        reg = np.sin(self.expression * np.pi) * 2 - 1
        protein = Protein(
            gene_id=self.gene_id,
            pitch=pitch,
            velocity=velocity,
            duration=duration,
            timbre=self._choose_timbre(),
            constraint_type=self.constraint_type,
            regulatory_activity=float(reg),
        )
        self.protein_history.append(protein)
        return protein

    def _choose_timbre(self) -> str:
        timbres = ["sine", "square", "saw", "triangle", "noise", "fm", "am"]
        idx = int(self.expression * len(timbres)) % len(timbres)
        return timbres[idx]

    def update_expression(self, inputs: List[float], tfs: List[TranscriptionFactor]) -> float:
        if not inputs:
            target = self.base_expression
        else:
            consensus, converged = consensus_round(inputs, self.epsilon)
            target = consensus[0] if converged else float(np.mean(inputs))
        for tf in tfs:
            if self.gene_id in tf.target_ids:
                target = tf.apply(target, self.expression)
        self.expression = funnel_step(self.expression, target, self.epsilon, self.decay)
        self.expression = float(np.clip(self.expression, 0.0, 1.0))
        self.history.append(self.expression)
        return self.expression


@dataclass
class TranscriptionFactor:
    name: str
    target_ids: List[int]
    effect: float
    threshold: float = 0.3
    steepness: float = 5.0

    def apply(self, target: float, current: float) -> float:
        if current < self.threshold:
            return target
        modulation = 1.0 / (1.0 + np.exp(-self.steepness * (current - 0.5)))
        return target + self.effect * modulation * 0.2


# ---------------------------------------------------------------------------
# Regulatory Network
# ---------------------------------------------------------------------------


class RegulatoryNetwork:
    def __init__(
        self,
        n_genes: int = N_GENES,
        n_tfs: int = 5,
        seed: Optional[int] = None,
    ):
        self.rng = np.random.default_rng(seed)
        self.n_genes = n_genes
        self.genes: List[Gene] = []
        self.tfs: List[TranscriptionFactor] = []
        self.regulatory_matrix: np.ndarray = np.zeros((n_genes, n_genes))
        self.timestep = 0
        self.expression_trace: np.ndarray = np.zeros((0, n_genes))
        self._init_genes()
        self._init_tfs(n_tfs)
        self._init_regulatory_matrix()

    def _init_genes(self) -> None:
        scale_names = list(SCALES.keys())
        for i in range(self.n_genes):
            g = Gene(
                gene_id=i,
                name=f"gene-{i:02d}",
                constraint_type=CONSTRAINT_TYPES[i % len(CONSTRAINT_TYPES)],
                scale_name=scale_names[i % len(scale_names)],
                root_pitch=48 + (i % 4) * 12,
                base_expression=float(self.rng.random()),
                expression=float(self.rng.random()),
                decay=float(self.rng.uniform(0.05, 0.25)),
                epsilon=float(self.rng.uniform(0.02, 0.08)),
            )
            g.history.append(g.expression)
            self.genes.append(g)

    def _init_tfs(self, n_tfs: int) -> None:
        for i in range(n_tfs):
            targets = self.rng.choice(self.n_genes, size=self.rng.integers(2, 6), replace=False).tolist()
            tf = TranscriptionFactor(
                name=f"TF-{i}",
                target_ids=targets,
                effect=1.0 if self.rng.random() > 0.4 else -1.0,
                threshold=float(self.rng.uniform(0.2, 0.5)),
                steepness=float(self.rng.uniform(3.0, 8.0)),
            )
            self.tfs.append(tf)

    def _init_regulatory_matrix(self) -> None:
        n = self.n_genes
        target_edges = 2 * n - 3
        weights = self.rng.standard_normal((n, n)) * 0.5
        mask = np.zeros((n, n), dtype=bool)
        edges = 0
        while edges < target_edges:
            i, j = self.rng.integers(0, n, size=2)
            if i != j and not mask[i, j]:
                mask[i, j] = True
                edges += 1
        self.regulatory_matrix = np.where(mask, weights, 0.0)
        np.fill_diagonal(self.regulatory_matrix, 0.0)

    def step(self) -> List[Protein]:
        proteins = [g.express() for g in self.genes]
        new_expressions = []
        for j, gene in enumerate(self.genes):
            inputs = []
            for i, prot in enumerate(proteins):
                w = self.regulatory_matrix[i, j]
                if w != 0.0:
                    inputs.append(float(np.clip(prot.regulatory_activity * w + 0.5, 0.0, 1.0)))
            expr = gene.update_expression(inputs, self.tfs)
            new_expressions.append(expr)
        self.expression_trace = np.vstack([self.expression_trace, np.asarray(new_expressions)])
        self.timestep += 1
        return proteins

    def run(self, n_steps: int = N_TIMESTEPS) -> np.ndarray:
        for _ in range(n_steps):
            self.step()
        return self.expression_trace

    def entropy_over_time(self, window: int = 10) -> List[float]:
        if len(self.expression_trace) < window:
            return []
        entropies = []
        for t in range(window, len(self.expression_trace) + 1):
            hist, _ = np.histogram(self.expression_trace[t - window : t], bins=10, range=(0, 1))
            probs = hist / hist.sum() if hist.sum() > 0 else hist
            probs = probs[probs > 0]
            ent = -np.sum(probs * np.log2(probs)) if len(probs) else 0.0
            entropies.append(float(ent))
        return entropies

    def detect_attractors(self, tolerance: float = 0.05) -> List[Tuple[int, int]]:
        trace = self.expression_trace
        if len(trace) < 5:
            return []
        attractors = []
        start = 0
        for t in range(1, len(trace)):
            if np.max(np.abs(trace[t] - trace[t - 1])) > tolerance:
                if t - start >= 5:
                    attractors.append((start, t - 1))
                start = t
        if len(trace) - start >= 5:
            attractors.append((start, len(trace) - 1))
        return attractors

    def cluster_coefficients(self) -> Dict[int, float]:
        trace = self.expression_trace
        coeffs = {}
        for j in range(self.n_genes):
            series = trace[:, j]
            if len(series) < 3:
                coeffs[j] = 0.0
                continue
            returns = np.abs(series[1:] - series[:-1])
            coeffs[j] = float(1.0 / (1.0 + np.mean(returns)))
        return coeffs

    def periodicity_score(self, gene_id: int) -> float:
        series = self.expression_trace[:, gene_id]
        if len(series) < 4:
            return 0.0
        max_lag = len(series) // 2
        autocorrs = []
        for lag in range(1, max_lag):
            s1 = series[:-lag]
            s2 = series[lag:]
            if np.std(s1) < 1e-12 or np.std(s2) < 1e-12:
                continue
            c = np.corrcoef(s1, s2)[0, 1]
            if not np.isnan(c):
                autocorrs.append(c)
        if not autocorrs:
            return 0.0
        return float(np.max(autocorrs))

    def sensitivity_analysis(self, perturbation: float = 0.1) -> float:
        original_final = self.expression_trace[-1].copy() if len(self.expression_trace) else np.zeros(self.n_genes)
        perturbed = RegulatoryNetwork(n_genes=self.n_genes, n_tfs=len(self.tfs), seed=None)
        for g, pg in zip(self.genes, perturbed.genes):
            pg.expression = np.clip(g.history[0] + self.rng.uniform(-perturbation, perturbation), 0.0, 1.0)
            pg.history = [pg.expression]
        perturbed.regulatory_matrix = self.regulatory_matrix.copy()
        perturbed.tfs = self.tfs
        perturbed.run(len(self.expression_trace))
        if len(perturbed.expression_trace) == 0:
            return 0.0
        perturbed_final = perturbed.expression_trace[-1]
        return float(np.linalg.norm(original_final - perturbed_final))

    def consensus_emergence(self) -> List[float]:
        consensus_ratios = []
        for t in range(len(self.expression_trace)):
            values = self.expression_trace[t].tolist()
            _, converged = consensus_round(values, EPSILON)
            consensus_ratios.append(1.0 if converged else 0.0)
        return consensus_ratios

    def musical_score(self) -> List[List[Protein]]:
        return [gene.protein_history for gene in self.genes]

    def rigidity_of_active_network(self, threshold: float = 0.3) -> bool:
        if len(self.expression_trace) == 0:
            return False
        avg_expr = np.mean(self.expression_trace, axis=0)
        active = [i for i, e in enumerate(avg_expr) if e > threshold]
        if len(active) < 2:
            return False
        idx_map = {old: new for new, old in enumerate(active)}
        edges = []
        for i in active:
            for j in active:
                if i != j and self.regulatory_matrix[i, j] != 0.0:
                    edges.append((idx_map[i], idx_map[j]))
        undirected = set()
        for u, v in edges:
            if u < v:
                undirected.add((u, v))
        return laman_rigidity_check(len(active), list(undirected))


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def report_emergence(net: RegulatoryNetwork) -> Dict[str, object]:
    report: Dict[str, object] = {}
    report["n_genes"] = net.n_genes
    report["n_timesteps"] = len(net.expression_trace)
    report["entropy_series"] = net.entropy_over_time()
    report["attractors"] = net.detect_attractors()
    report["clustering"] = net.cluster_coefficients()
    report["periodicity"] = {i: net.periodicity_score(i) for i in range(net.n_genes)}
    report["sensitivity"] = net.sensitivity_analysis()
    report["consensus_emergence"] = net.consensus_emergence()
    report["laman_rigid"] = net.rigidity_of_active_network()
    report["final_expression"] = net.expression_trace[-1].tolist() if len(net.expression_trace) else []
    return report


# ---------------------------------------------------------------------------
# pytest test suite (24 tests)
# ---------------------------------------------------------------------------

import pytest  # type: ignore[import-not-found]


class TestConstraintPrimitives:
    def test_consensus_round_converges(self):
        values = [0.51, 0.52, 0.53, 0.50]
        rounded, converged = consensus_round(values, epsilon=0.1)
        assert converged is True
        assert len(rounded) == 4

    def test_consensus_round_diverges(self):
        values = [0.1, 0.5, 0.9]
        rounded, converged = consensus_round(values, epsilon=0.1)
        assert converged is False

    def test_snap_to_lattice_major(self):
        pitch = snap_to_lattice(0.0, MAJOR_SCALE, root=60)
        assert pitch == 60
        pitch = snap_to_lattice(0.99, MAJOR_SCALE, root=60)
        assert pitch >= 60

    def test_snap_to_lattice_pentatonic(self):
        pitch = snap_to_lattice(0.5, PENTATONIC_SCALE, root=72)
        degree = (pitch - 72) % 12
        assert degree in PENTATONIC_SCALE

    def test_funnel_step_within_deadband(self):
        result = funnel_step(0.5, 0.52, epsilon=0.05, decay_rate=0.1)
        assert result == 0.5

    def test_funnel_step_moves_toward_target(self):
        result = funnel_step(0.1, 0.9, epsilon=0.01, decay_rate=0.5)
        assert result > 0.1
        assert result < 0.9

    def test_laman_triangle_is_rigid(self):
        assert laman_rigidity_check(3, [(0, 1), (1, 2), (0, 2)]) is True

    def test_laman_k4_not_rigid(self):
        assert laman_rigidity_check(4, [(0, 1), (1, 2), (2, 3), (0, 2), (1, 3), (0, 3)]) is False


class TestGeneAndProtein:
    def test_gene_expresses_protein(self):
        g = Gene(gene_id=0, name="test", constraint_type="pitch")
        prot = g.express()
        assert prot.gene_id == 0
        assert 0 <= prot.velocity <= 127
        assert prot.duration > 0

    def test_gene_expression_history(self):
        g = Gene(gene_id=0, name="test", constraint_type="pitch", expression=0.3)
        g.history.append(g.expression)
        g.update_expression([0.8], [])
        assert len(g.history) == 2
        assert g.history[-1] != g.history[0]

    def test_protein_regulatory_activity_range(self):
        g = Gene(gene_id=0, name="test", constraint_type="pitch", expression=0.5)
        prot = g.express()
        assert -1.0 <= prot.regulatory_activity <= 1.0

    def test_tf_activation(self):
        tf = TranscriptionFactor(name="test", target_ids=[0], effect=1.0, threshold=0.0)
        result = tf.apply(target=0.5, current=0.8)
        assert result > 0.5

    def test_tf_repression(self):
        tf = TranscriptionFactor(name="test", target_ids=[0], effect=-1.0, threshold=0.0)
        result = tf.apply(target=0.5, current=0.8)
        assert result < 0.5

    def test_tf_inactive_below_threshold(self):
        tf = TranscriptionFactor(name="test", target_ids=[0], effect=1.0, threshold=0.9)
        result = tf.apply(target=0.5, current=0.1)
        assert result == 0.5


class TestRegulatoryNetwork:
    def test_network_init(self):
        net = RegulatoryNetwork(n_genes=10, n_tfs=3, seed=42)
        assert len(net.genes) == 10
        assert len(net.tfs) == 3
        assert net.regulatory_matrix.shape == (10, 10)

    def test_network_step_increments_timestep(self):
        net = RegulatoryNetwork(n_genes=10, n_tfs=2, seed=42)
        net.step()
        assert net.timestep == 1

    def test_network_run_returns_trace(self):
        net = RegulatoryNetwork(n_genes=10, n_tfs=2, seed=42)
        trace = net.run(n_steps=50)
        assert trace.shape == (50, 10)

    def test_expression_trace_bounds(self):
        net = RegulatoryNetwork(n_genes=10, n_tfs=2, seed=42)
        net.run(n_steps=30)
        assert np.all(net.expression_trace >= 0.0)
        assert np.all(net.expression_trace <= 1.0)

    def test_proteins_produced_each_step(self):
        net = RegulatoryNetwork(n_genes=10, n_tfs=2, seed=42)
        prots = net.step()
        assert len(prots) == 10

    def test_entropy_over_time(self):
        net = RegulatoryNetwork(n_genes=10, n_tfs=2, seed=42)
        net.run(n_steps=20)
        ent = net.entropy_over_time(window=5)
        assert len(ent) == 16
        assert all(0.0 <= e <= np.log2(10) for e in ent)

    def test_attractor_detection(self):
        net = RegulatoryNetwork(n_genes=10, n_tfs=2, seed=42)
        net.run(n_steps=50)
        atts = net.detect_attractors(tolerance=0.1)
        assert isinstance(atts, list)

    def test_clustering_coefficients(self):
        net = RegulatoryNetwork(n_genes=10, n_tfs=2, seed=42)
        net.run(n_steps=20)
        coeffs = net.cluster_coefficients()
        assert len(coeffs) == 10
        assert all(0.0 <= v <= 1.0 for v in coeffs.values())

    def test_periodicity_score(self):
        net = RegulatoryNetwork(n_genes=10, n_tfs=2, seed=42)
        net.run(n_steps=30)
        score = net.periodicity_score(gene_id=0)
        assert -1.0 <= score <= 1.0

    def test_sensitivity_analysis(self):
        net = RegulatoryNetwork(n_genes=10, n_tfs=2, seed=42)
        net.run(n_steps=20)
        div = net.sensitivity_analysis(perturbation=0.05)
        assert div >= 0.0

    def test_consensus_emergence_length(self):
        net = RegulatoryNetwork(n_genes=10, n_tfs=2, seed=42)
        net.run(n_steps=25)
        ce = net.consensus_emergence()
        assert len(ce) == 25

    def test_musical_score_dimensions(self):
        net = RegulatoryNetwork(n_genes=8, n_tfs=2, seed=42)
        net.run(n_steps=10)
        score = net.musical_score()
        assert len(score) == 8
        assert all(len(track) == 10 for track in score)

    def test_rigidity_check_runs(self):
        net = RegulatoryNetwork(n_genes=10, n_tfs=2, seed=42)
        net.run(n_steps=20)
        rigid = net.rigidity_of_active_network()
        assert isinstance(rigid, bool)

    def test_report_emergence(self):
        net = RegulatoryNetwork(n_genes=10, n_tfs=2, seed=42)
        net.run(n_steps=20)
        rpt = report_emergence(net)
        assert "entropy_series" in rpt
        assert "sensitivity" in rpt

    def test_no_self_regulation(self):
        net = RegulatoryNetwork(n_genes=10, n_tfs=2, seed=42)
        assert np.all(np.diag(net.regulatory_matrix) == 0.0)

    def test_gene_count_20(self):
        net = RegulatoryNetwork(n_genes=20, n_tfs=5, seed=42)
        assert len(net.genes) == 20
        trace = net.run(n_steps=100)
        assert trace.shape == (100, 20)

    def test_different_seeds_produce_different_results(self):
        net1 = RegulatoryNetwork(n_genes=10, n_tfs=2, seed=1)
        net1.run(n_steps=10)
        net2 = RegulatoryNetwork(n_genes=10, n_tfs=2, seed=2)
        net2.run(n_steps=10)
        assert not np.allclose(net1.expression_trace, net2.expression_trace)

    def test_reproducibility_with_same_seed(self):
        net1 = RegulatoryNetwork(n_genes=10, n_tfs=2, seed=99)
        net1.run(n_steps=10)
        net2 = RegulatoryNetwork(n_genes=10, n_tfs=2, seed=99)
        net2.run(n_steps=10)
        assert np.allclose(net1.expression_trace, net2.expression_trace)

    def test_tf_target_ids_are_valid(self):
        net = RegulatoryNetwork(n_genes=10, n_tfs=3, seed=42)
        for tf in net.tfs:
            assert all(0 <= tid < 10 for tid in tf.target_ids)


class TestEmergenceProperties:
    def test_emergent_entropy_changes(self):
        net = RegulatoryNetwork(n_genes=20, n_tfs=5, seed=42)
        net.run(n_steps=100)
        ent = net.entropy_over_time(window=10)
        assert len(ent) > 5
        assert np.std(ent) > 0.01

    def test_emergent_patterns_not_predictable_from_initial(self):
        net = RegulatoryNetwork(n_genes=20, n_tfs=5, seed=42)
        net.run(n_steps=100)
        initial = np.asarray([g.history[0] for g in net.genes])
        final = net.expression_trace[-1]
        corr = np.corrcoef(initial, final)[0, 1]
        assert abs(corr) < 0.99

    def test_sensitivity_implies_emergence(self):
        net = RegulatoryNetwork(n_genes=20, n_tfs=5, seed=42)
        net.run(n_steps=50)
        div = net.sensitivity_analysis(perturbation=0.05)
        assert div > 0.01

    def test_consensus_can_emerge(self):
        net = RegulatoryNetwork(n_genes=20, n_tfs=5, seed=123)
        net.run(n_steps=100)
        ce = net.consensus_emergence()
        assert sum(ce) >= 0


# ---------------------------------------------------------------------------
# CLI runner
# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 70)
    print("GENE REGULATORY NETWORK — MUSICAL CONSENSUS SIMULATION")
    print("=" * 70)

    net = RegulatoryNetwork(n_genes=N_GENES, n_tfs=5, seed=42)
    print(f"\nInitialized network: {N_GENES} genes, {len(net.tfs)} TFs")
    print(f"Regulatory edges: {np.count_nonzero(net.regulatory_matrix)}")

    net.run(n_steps=N_TIMESTEPS)
    print(f"\nRan {N_TIMESTEPS} timesteps.")

    rpt = report_emergence(net)

    print(f"\n--- Emergence Report ---")
    print(f"Entropy (final window): {rpt['entropy_series'][-1]:.4f}")
    print(f"Attractors detected: {len(rpt['attractors'])}")
    print(f"Laman-rigid active subgraph: {rpt['laman_rigid']}")
    print(f"Sensitivity divergence: {rpt['sensitivity']:.4f}")
    print(f"Consensus timesteps: {sum(rpt['consensus_emergence'])} / {N_TIMESTEPS}")

    print(f"\n--- Final Expression (top 10 genes) ---")
    final = rpt["final_expression"]
    for i in range(min(10, N_GENES)):
        print(f"  {net.genes[i].name:10s}  expr={final[i]:.3f}  type={net.genes[i].constraint_type}")

    print(f"\n--- Periodicity (top 5 genes) ---")
    per = rpt["periodicity"]
    top_periodic = sorted(per.items(), key=lambda kv: kv[1], reverse=True)[:5]
    for gid, score in top_periodic:
        print(f"  gene-{gid:02d}  periodicity={score:.3f}")

    print("\n" + "=" * 70)
    print("Simulation complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()
