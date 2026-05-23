#!/usr/bin/env python3
"""
Consensus Scaling — How many voices can consensus handle?

Generate compositions with 2, 3, 4, 5, 6, 8, 12, 16 voices.
Measure: consensus convergence time, harmonic coherence, computational cost.

Hypothesis: Laman rigidity should keep coherence even at high voice counts.
"""

import csv
import math
import os
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "constraint-theory-core"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "flux-tensor-midi"))

from constraint_theory_core.rigidity import is_laman, henneberg_construct, optimal_coupling
from constraint_theory_core.lattice import snap, covering_radius
from constraint_theory_core.temporal import TemporalAgent


# ---------------------------------------------------------------------------
# Consensus simulation
# ---------------------------------------------------------------------------

def simulate_consensus(
    n_voices: int,
    bpm: float = 120.0,
    n_ticks: int = 200,
    seed: int = 42,
) -> Dict:
    """Simulate distributed metronome consensus for n_voices.

    Each voice starts with a random phase offset and converges via
    Laman-coupled agreement.

    Returns convergence metrics.
    """
    rng = np.random.RandomState(seed)

    # Build Laman graph via Henneberg construction
    if n_voices < 2:
        return {
            "n_voices": n_voices,
            "convergence_tick": 0,
            "final_coherence": 1.0,
            "computational_time_s": 0.0,
            "is_laman": True,
            "n_edges": 0,
            "coupling_strength": 0.0,
        }

    edges = henneberg_construct(n_voices)
    laman = is_laman(n_voices, edges)

    # Compute optimal coupling strength
    try:
        coupling = optimal_coupling(n_voices, edges)
    except Exception:
        coupling = 0.1  # fallback

    # Initialize voice phases with random offsets
    phases = rng.uniform(0, 2 * np.pi, n_voices)
    periods = np.full(n_voices, 60.0 / bpm)  # All start at target BPM

    # Add slight tempo variations
    periods += rng.normal(0, 0.01, n_voices)

    # Build adjacency from edges
    adjacency = defaultdict(list)
    for i, j in edges:
        adjacency[i].append(j)
        adjacency[j].append(i)

    # Run consensus
    convergence_tick = None
    convergence_threshold = 0.01  # radians
    coherence_history = []
    anomaly_counts = np.zeros(n_voices, dtype=int)

    t_start = time.time()

    for tick in range(n_ticks):
        # Each voice advances by its period
        phases = (phases + 2 * np.pi * (1.0 / periods) * (60.0 / bpm)) % (2 * np.pi)

        # Agreement step: pull toward neighbor average
        new_phases = phases.copy()
        for v in range(n_voices):
            neighbors = adjacency[v]
            if not neighbors:
                continue
            neighbor_phases = phases[neighbors]
            # Circular mean
            sin_sum = np.sum(np.sin(neighbor_phases))
            cos_sum = np.sum(np.cos(neighbor_phases))
            mean_phase = np.arctan2(sin_sum, cos_sum) % (2 * np.pi)

            # Pull toward consensus with coupling strength
            diff = mean_phase - phases[v]
            # Wrap to [-π, π]
            diff = (diff + np.pi) % (2 * np.pi) - np.pi
            new_phases[v] = (phases[v] + coupling * diff) % (2 * np.pi)

            # Check for anomaly
            if abs(diff) > 1.0:
                anomaly_counts[v] += 1

        phases = new_phases

        # Measure coherence (phase alignment)
        sin_mean = np.mean(np.sin(phases))
        cos_mean = np.mean(np.cos(phases))
        coherence = np.sqrt(sin_mean**2 + cos_mean**2)
        coherence_history.append(coherence)

        # Check convergence
        if convergence_tick is None and coherence > 0.99:
            convergence_tick = tick

    computational_time = time.time() - t_start

    return {
        "n_voices": n_voices,
        "convergence_tick": convergence_tick or n_ticks,
        "final_coherence": round(coherence_history[-1], 6),
        "computational_time_s": round(computational_time, 6),
        "is_laman": laman,
        "n_edges": len(edges),
        "coupling_strength": round(coupling, 6),
        "total_anomalies": int(anomaly_counts.sum()),
        "coherence_history": coherence_history,
    }


# ---------------------------------------------------------------------------
# Harmonic coherence
# ---------------------------------------------------------------------------

def measure_harmonic_coherence(n_voices: int, seed: int = 42) -> float:
    """Generate a chord from n_voices and measure how consonant it is.

    Uses the constraint harmony system to evaluate.
    """
    rng = np.random.RandomState(seed)

    # Generate pitches in a constrained way
    consonant_ratios = [1.0, 9/8, 6/5, 5/4, 4/3, 3/2, 5/3, 15/8]
    base_freq = 261.626  # Middle C

    frequencies = []
    for _ in range(n_voices):
        ratio = rng.choice(consonant_ratios)
        octave = rng.choice([0.5, 1.0, 2.0, 4.0])
        frequencies.append(base_freq * ratio * octave)

    # Measure pairwise consonance
    total_dissonance = 0.0
    pairs = 0
    for i in range(len(frequencies)):
        for j in range(i + 1, len(frequencies)):
            ratio = frequencies[j] / frequencies[i]
            # Simple consonance: how close to a simple ratio?
            log_ratio = abs(math.log2(ratio))
            # Near-integer log2 values are consonant (octaves)
            near_octave = min(abs(log_ratio - round(log_ratio)), abs(log_ratio - round(log_ratio) - 1))
            # Near simple fractions
            for num, den in [(3, 2), (4, 3), (5, 4), (6, 5), (5, 3)]:
                target = math.log2(num / den)
                near_octave = min(near_octave, abs(log_ratio - target))
                near_octave = min(near_octave, abs(log_ratio - target - 1))
            total_dissonance += near_octave
            pairs += 1

    return 1.0 - (total_dissonance / max(pairs, 1))


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_experiment(
    voice_counts: List[int] = None,
    n_trials: int = 20,
    output_dir: str = None,
) -> Tuple[str, str]:
    """Run the consensus scaling experiment."""
    voice_counts = voice_counts or [2, 3, 4, 5, 6, 8, 12, 16]
    output_dir = output_dir or str(Path(__file__).resolve().parent.parent / "experiments" / "output" / "consensus_scaling")
    os.makedirs(output_dir, exist_ok=True)
    fig_dir = os.path.join(output_dir, "figures")
    os.makedirs(fig_dir, exist_ok=True)

    results = []

    print(f"CONSENSUS SCALING: {len(voice_counts)} voice counts × {n_trials} trials")
    print("=" * 70)

    for n_voices in voice_counts:
        print(f"  {n_voices} voices...", end="", flush=True)
        for trial in range(n_trials):
            seed = n_voices * 1000 + trial * 7 + 42
            result = simulate_consensus(n_voices, seed=seed)
            harmony = measure_harmonic_coherence(n_voices, seed=seed)

            results.append({
                "n_voices": n_voices,
                "trial": trial,
                "convergence_tick": result["convergence_tick"],
                "final_coherence": result["final_coherence"],
                "computational_time_s": result["computational_time_s"],
                "is_laman": result["is_laman"],
                "n_edges": result["n_edges"],
                "coupling_strength": result["coupling_strength"],
                "total_anomalies": result["total_anomalies"],
                "harmonic_coherence": round(harmony, 4),
            })
        print(f" done")

    # Write CSV
    csv_path = os.path.join(output_dir, "consensus_scaling_results.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"\nCSV saved: {csv_path}")

    # Plots
    _plot_results(results, voice_counts, fig_dir)

    return csv_path, fig_dir


def _plot_results(results: List[Dict], voice_counts: List[int], fig_dir: str):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Consensus Scaling: How Many Voices Can Consensus Handle?", fontsize=14, fontweight="bold")

    metrics = [
        ("convergence_tick", "Convergence Tick", axes[0, 0]),
        ("final_coherence", "Final Coherence", axes[0, 1]),
        ("computational_time_s", "Computational Time (s)", axes[1, 0]),
        ("harmonic_coherence", "Harmonic Coherence", axes[1, 1]),
    ]

    for metric, label, ax in metrics:
        xs = []
        means = []
        stds = []
        for nv in voice_counts:
            vals = [r[metric] for r in results if r["n_voices"] == nv]
            xs.append(nv)
            means.append(np.mean(vals))
            stds.append(np.std(vals))
        ax.errorbar(xs, means, yerr=stds, marker="o", capsize=5, linewidth=2)
        ax.set_xlabel("Number of Voices")
        ax.set_ylabel(label)
        ax.set_title(label)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "consensus_scaling.png"), dpi=150)
    plt.close()

    # Coherence trajectory plot
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    for nv in [3, 6, 8, 12, 16]:
        result = simulate_consensus(nv, seed=42)
        history = result["coherence_history"]
        ax2.plot(range(len(history)), history, label=f"{nv} voices", linewidth=1.5)
    ax2.set_xlabel("Tick")
    ax2.set_ylabel("Coherence (phase alignment)")
    ax2.set_title("Coherence Trajectory: Laman-Coupled Consensus")
    ax2.axhline(y=0.99, color="green", linestyle="--", alpha=0.5, label="Convergence threshold")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "coherence_trajectory.png"), dpi=150)
    plt.close()

    print(f"Figures saved to: {fig_dir}")


if __name__ == "__main__":
    csv_path, fig_dir = run_experiment()
    print(f"\nDone! Results: {csv_path}")
