#!/usr/bin/env python3
"""
Constraint Interaction — How do constraints interact?

Systematically vary pairs of constraint types (snap×funnel, consensus×tempo, etc.)
5×5 matrix of constraint combinations at low/medium/high tightness.

Discovery: find the COMBINATIONS that produce unexpected results.
"""

import csv
import math
import os
import sys
import time
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "flux-tensor-midi"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "constraint-theory-core"))

from constraint_theory_core.lattice import snap, covering_radius, A2Point
from constraint_theory_core.temporal import TemporalAgent, FunnelPhase
from constraint_theory_core.rigidity import is_laman, henneberg_construct


# ---------------------------------------------------------------------------
# Constraint types
# ---------------------------------------------------------------------------

CONSTRAINT_TYPES = ["snap", "funnel", "consensus", "tempo", "dissonance"]


def apply_snap_constraint(pitches: List[int], tightness: float, base: int = 60) -> List[int]:
    """Apply Eisenstein lattice snap constraint to pitch sequence.

    tightness=0 → no snapping, tightness=1 → full snap to nearest lattice point.
    """
    result = []
    for p in pitches:
        interval = (p - base) / 12.0
        pt, err = snap(interval, 0.0)
        # Interpolate between original and snapped
        snapped = base + int(round(pt.a + pt.b * 0.5)) * 12  # Simplified snap
        if tightness > 0:
            result.append(int(round(p * (1 - tightness) + snapped * tightness)))
        else:
            result.append(p)
    return result


def apply_funnel_constraint(events: List[Dict], tightness: float) -> List[Dict]:
    """Apply temporal funnel constraint — tightness narrows timing tolerance."""
    result = []
    for e in events:
        jitter = e.get("beat_position", 0.0) - round(e.get("beat_position", 0.0))
        reduced_jitter = jitter * (1.0 - tightness)
        new_event = dict(e)
        new_event["beat_position"] = round(e["beat_position"]) + reduced_jitter
        result.append(new_event)
    return result


def apply_consensus_constraint(pitches: List[int], tightness: float, rng=None) -> List[int]:
    """Apply consensus constraint — pull pitches toward the average pitch."""
    if not pitches:
        return pitches
    rng = rng or np.random.RandomState()
    mean_pitch = np.mean(pitches)
    result = []
    for p in pitches:
        pulled = p * (1 - tightness) + mean_pitch * tightness
        result.append(int(round(pulled)))
    return result


def apply_tempo_constraint(events: List[Dict], tightness: float) -> List[Dict]:
    """Apply tempo constraint — quantize beat positions to a grid."""
    grid = max(1, int(round(4 * (1 - tightness) + 1)))
    result = []
    for e in events:
        pos = e.get("beat_position", 0.0)
        quantized = round(pos * grid) / grid
        new_event = dict(e)
        new_event["beat_position"] = quantized
        result.append(new_event)
    return result


def apply_dissonance_constraint(pitches: List[int], tightness: float, base: int = 60) -> List[int]:
    """Apply dissonance constraint — remove pitches that create dissonant intervals."""
    consonant = {0, 3, 4, 5, 7, 8, 9, 12}
    result = []
    prev = base
    for p in pitches:
        interval = abs(p - prev) % 12
        if tightness < 0.5 or interval in consonant:
            result.append(p)
            prev = p
        else:
            # Replace with nearest consonant pitch
            best = prev
            best_dist = float("inf")
            for c in consonant:
                candidate = prev + c
                if abs(candidate - p) < best_dist:
                    best_dist = abs(candidate - p)
                    best = candidate
            result.append(best)
            prev = best
    return result


# ---------------------------------------------------------------------------
# Composition generation
# ---------------------------------------------------------------------------

def generate_base_composition(n_bars: int = 8, seed: int = 42) -> Dict:
    """Generate an unconstrained base composition."""
    rng = np.random.RandomState(seed)
    base = 60
    total_beats = n_bars * 4
    pitches = []
    events = []

    for beat in range(total_beats):
        n_notes = rng.poisson(2)
        for _ in range(n_notes):
            pitch = base + rng.randint(0, 25)
            pos = beat + rng.uniform(0, 1)
            events.append({"pitch": pitch, "beat_position": pos})
            pitches.append(pitch)

    return {"pitches": pitches, "events": events}


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def compute_surprise(pitches: List[int], events: List[Dict]) -> float:
    """Compute surprise score — how unexpected is the composition?

    High surprise = unusual interval patterns, timing irregularities.
    """
    if len(pitches) < 2:
        return 0.0

    # Interval surprise
    intervals = [pitches[i+1] - pitches[i] for i in range(len(pitches) - 1)]
    if not intervals:
        return 0.0

    interval_counts = Counter(intervals)
    # Surprise = how different from uniform distribution
    n_intervals = len(intervals)
    n_unique = len(interval_counts)
    max_entropy = math.log2(max(n_unique, 1))
    actual_entropy = -sum((c / n_intervals) * math.log2(c / n_intervals) for c in interval_counts.values())

    # Timing surprise
    positions = [e.get("beat_position", 0.0) for e in events]
    if len(positions) > 1:
        diffs = [positions[i+1] - positions[i] for i in range(len(positions) - 1)]
        diffs = [d for d in diffs if d > 0]
        if diffs:
            timing_var = np.var(diffs)
        else:
            timing_var = 0
    else:
        timing_var = 0

    surprise = 0.5 * (actual_entropy / max(max_entropy, 0.001)) + 0.5 * min(timing_var / 0.5, 1.0)
    return round(surprise, 4)


def compute_musicality(pitches: List[int], events: List[Dict]) -> Dict:
    """Compute multiple musicality metrics."""
    if not pitches:
        return {"entropy": 0, "range": 0, "density": 0, "syncopation": 0, "surprise": 0}

    # Entropy
    counts = Counter(pitches)
    total = len(pitches)
    entropy = -sum((c / total) * math.log2(c / total) for c in counts.values())

    # Range
    range_ = max(pitches) - min(pitches)

    # Density (events per beat)
    positions = [e.get("beat_position", 0.0) for e in events]
    span = max(positions) - min(positions) if positions else 1
    density = len(events) / max(span, 1)

    # Syncopation
    on_beat = sum(1 for e in events if abs(e.get("beat_position", 0) - round(e.get("beat_position", 0))) < 0.05)
    syncopation = 1.0 - on_beat / max(len(events), 1)

    # Surprise
    surprise = compute_surprise(pitches, events)

    return {
        "entropy": round(entropy, 4),
        "range": range_,
        "density": round(density, 4),
        "syncopation": round(syncopation, 4),
        "surprise": surprise,
    }


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_experiment(
    tightness_levels: List[float] = None,
    n_trials: int = 5,
    output_dir: str = None,
) -> Tuple[str, str]:
    tightness_levels = tightness_levels or [0.2, 0.5, 0.8]
    output_dir = output_dir or str(Path(__file__).resolve().parent.parent / "experiments" / "output" / "constraint_interaction")
    os.makedirs(output_dir, exist_ok=True)
    fig_dir = os.path.join(output_dir, "figures")
    os.makedirs(fig_dir, exist_ok=True)

    constraint_pairs = list(product(CONSTRAINT_TYPES, CONSTRAINT_TYPES))
    # Filter to unique pairs (upper triangle)
    constraint_pairs = [(a, b) for a, b in constraint_pairs if CONSTRAINT_TYPES.index(a) <= CONSTRAINT_TYPES.index(b)]

    results = []
    n_total = len(constraint_pairs) * len(tightness_levels) * n_trials
    count = 0

    print(f"CONSTRAINT INTERACTION: {len(constraint_pairs)} pairs × {len(tightness_levels)} tightness × {n_trials} trials")
    print("=" * 70)

    for c_a, c_b in constraint_pairs:
        print(f"  {c_a} × {c_b}...", end="", flush=True)
        for tightness in tightness_levels:
            for trial in range(n_trials):
                seed = hash((c_a, c_b, tightness, trial)) % (2**31)
                seed = abs(seed)

                base_comp = generate_base_composition(seed=seed)
                pitches = list(base_comp["pitches"])
                events = list(base_comp["events"])

                # Apply constraint A
                if c_a == "snap":
                    pitches = apply_snap_constraint(pitches, tightness)
                elif c_a == "funnel":
                    events = apply_funnel_constraint(events, tightness)
                elif c_a == "consensus":
                    pitches = apply_consensus_constraint(pitches, tightness)
                elif c_a == "tempo":
                    events = apply_tempo_constraint(events, tightness)
                elif c_a == "dissonance":
                    pitches = apply_dissonance_constraint(pitches, tightness)

                # Apply constraint B
                if c_b == "snap":
                    pitches = apply_snap_constraint(pitches, tightness)
                elif c_b == "funnel":
                    events = apply_funnel_constraint(events, tightness)
                elif c_b == "consensus":
                    pitches = apply_consensus_constraint(pitches, tightness)
                elif c_b == "tempo":
                    events = apply_tempo_constraint(events, tightness)
                elif c_b == "dissonance":
                    pitches = apply_dissonance_constraint(pitches, tightness)

                # Synchronize pitches back into events
                for i, e in enumerate(events):
                    if i < len(pitches):
                        e["pitch"] = pitches[i]

                metrics = compute_musicality(pitches, events)

                results.append({
                    "constraint_a": c_a,
                    "constraint_b": c_b,
                    "tightness": tightness,
                    "trial": trial,
                    **metrics,
                })
                count += 1
        print(" done")

    # Write CSV
    csv_path = os.path.join(output_dir, "constraint_interaction_results.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"\nCSV saved: {csv_path}")

    _plot_results(results, constraint_pairs, tightness_levels, fig_dir)

    return csv_path, fig_dir


def _plot_results(results, constraint_pairs, tightness_levels, fig_dir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Interaction matrix — surprise scores
    n = len(CONSTRAINT_TYPES)
    for tightness in tightness_levels:
        fig, ax = plt.subplots(figsize=(8, 7))
        matrix = np.zeros((n, n))

        for r in results:
            if abs(r["tightness"] - tightness) < 0.01:
                i = CONSTRAINT_TYPES.index(r["constraint_a"])
                j = CONSTRAINT_TYPES.index(r["constraint_b"])
                matrix[i, j] += r["surprise"]
                if i != j:
                    matrix[j, i] += r["surprise"]

        # Average
        count_matrix = np.zeros((n, n))
        for r in results:
            if abs(r["tightness"] - tightness) < 0.01:
                i = CONSTRAINT_TYPES.index(r["constraint_a"])
                j = CONSTRAINT_TYPES.index(r["constraint_b"])
                count_matrix[i, j] += 1
                if i != j:
                    count_matrix[j, i] += 1
        matrix = np.divide(matrix, count_matrix, out=np.zeros_like(matrix), where=count_matrix > 0)

        im = ax.imshow(matrix, cmap="coolwarm", aspect="auto")
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.set_xticklabels(CONSTRAINT_TYPES, rotation=45, ha="right")
        ax.set_yticklabels(CONSTRAINT_TYPES)
        ax.set_title(f"Constraint Interaction Matrix (surprise) — tightness={tightness}")
        plt.colorbar(im, ax=ax, label="Surprise Score")

        for i in range(n):
            for j in range(n):
                ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", fontsize=9)

        plt.tight_layout()
        plt.savefig(os.path.join(fig_dir, f"interaction_matrix_t{tightness:.1f}.png"), dpi=150)
        plt.close()

    # Emergent properties: find combos with unexpected surprise
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    combo_labels = []
    surprise_values = []
    baseline_surprise = {}

    for ct in CONSTRAINT_TYPES:
        vals = [r["surprise"] for r in results if r["constraint_a"] == ct and r["constraint_b"] == ct]
        if vals:
            baseline_surprise[ct] = np.mean(vals)

    for c_a, c_b in constraint_pairs:
        if c_a == c_b:
            continue
        vals = [r["surprise"] for r in results if r["constraint_a"] == c_a and r["constraint_b"] == c_b]
        if vals:
            combined = np.mean(vals)
            expected = (baseline_surprise.get(c_a, 0) + baseline_surprise.get(c_b, 0)) / 2
            label = f"{c_a}×{c_b}"
            combo_labels.append(label)
            surprise_values.append(combined - expected)  # Deviation from expected

    colors = ["red" if v > 0 else "blue" for v in surprise_values]
    ax2.bar(range(len(combo_labels)), surprise_values, color=colors, alpha=0.7)
    ax2.set_xticks(range(len(combo_labels)))
    ax2.set_xticklabels(combo_labels, rotation=45, ha="right", fontsize=8)
    ax2.set_ylabel("Surprise Deviation (actual - expected)")
    ax2.set_title("Emergent Surprise: Combinations That Defy Expectation")
    ax2.axhline(y=0, color="black", linewidth=0.5)
    ax2.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "emergent_surprise.png"), dpi=150)
    plt.close()

    print(f"Figures saved to: {fig_dir}")


if __name__ == "__main__":
    csv_path, fig_dir = run_experiment()
    print(f"\nDone! Results: {csv_path}")
