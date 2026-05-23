#!/usr/bin/env python3
"""
Epsilon Sweep — THE core experiment.

Sweep epsilon (constraint tightness) from 0.01 to 1.0 in 20 steps.
For each epsilon, generate 10 compositions in each genre.
Measure: unique pitches, entropy, syncopation, constraint violations, generation time.

Hypothesis: inverted-U curve of musical "interest" vs constraint tightness.
Too tight → boring/repetitive. Too loose → chaotic/noisy. Sweet spot in the middle.

Usage:
    python experiments/epsilon_sweep.py
"""

import csv
import math
import os
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

# Add parent dirs to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "flux-tensor-midi"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "constraint-theory-core"))

from flux_tensor_midi.genre_brain import GenreBrain
from flux_tensor_midi.core.flux import FluxVector
from flux_tensor_midi.core.room import RoomMusician
from constraint_theory_core.lattice import snap, covering_radius
from constraint_theory_core.temporal import TemporalAgent


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def shannon_entropy(pitches: List[int]) -> float:
    """Compute Shannon entropy of pitch distribution."""
    if not pitches:
        return 0.0
    counts = Counter(pitches)
    total = len(pitches)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def unique_pitch_count(pitches: List[int]) -> int:
    return len(set(pitches))


def syncopation_score(events: List[Dict], grid_resolution: int = 4) -> float:
    """Measure syncopation: how often events fall OFF the main grid.

    Syncopation = fraction of events not on strong beats.
    """
    if not events:
        return 0.0
    off_grid = 0
    for e in events:
        beat_pos = e.get("beat_position", 0.0)
        # Strong beats are at integer and half-integer positions
        if grid_resolution == 4:
            grid_pos = round(beat_pos * 4) / 4
        else:
            grid_pos = round(beat_pos * grid_resolution) / grid_resolution
        if abs(beat_pos - grid_pos) > 0.05:
            off_grid += 1
    return off_grid / len(events)


def constraint_violations(pitches: List[int], epsilon: float) -> int:
    """Count how many pitch intervals violate the Eisenstein snap within epsilon."""
    if len(pitches) < 2:
        return 0
    violations = 0
    for i in range(1, len(pitches)):
        interval = (pitches[i] - pitches[i - 1]) / 12.0  # Normalize to octaves
        # Snap to Eisenstein lattice
        pt, err = snap(interval, 0.0)
        if err > epsilon * covering_radius():
            violations += 1
    return violations


# ---------------------------------------------------------------------------
# Composition generator
# ---------------------------------------------------------------------------

def generate_composition(genre: str, epsilon: float, seed: int) -> Dict:
    """Generate a composition for a given genre and epsilon.

    Returns dict with pitches, events, timing info.
    """
    rng = np.random.RandomState(seed)
    brain = GenreBrain(genre)
    preset = brain.get_preset()

    n_bars = preset["loop_bars"]
    grid_res = preset["grid_resolution"]
    base_note = preset["base_note"]
    bpm = preset["default_bpm"]
    beats_per_bar = 4

    # Scale degrees for each genre (MIDI offsets from root)
    genre_scales = {
        "jazz": [0, 2, 3, 5, 7, 9, 10, 12, 14, 15],          # bebop scale
        "hiphop": [0, 3, 5, 7, 10, 12, 15, 17],                # minor pentatonic + blues
        "electronic": [0, 3, 5, 7, 10, 12, 15, 19, 22],        # extended minor
        "classical": [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17],  # major + extensions
        "math": [0, 2, 4, 7, 9, 12, 14, 16, 19, 21],          # pentatonic+ extensions
    }
    scale = genre_scales.get(genre, [0, 2, 4, 5, 7, 9, 11, 12])

    # Epsilon controls how much randomness is allowed
    # Low epsilon → constrained to scale, close intervals
    # High epsilon → can jump anywhere, ignore scale

    total_beats = n_bars * beats_per_bar
    events = []
    pitches = []

    for beat in range(total_beats):
        beat_position = beat / grid_res

        # Number of subdivisions per beat depends on epsilon
        n_subdivisions = max(1, int(1 + rng.poisson(epsilon * 2)))

        for sub in range(n_subdivisions):
            # Decide whether to place a note
            prob = 0.3 + 0.4 * (1.0 - epsilon)  # More notes at low epsilon
            if rng.random() > prob:
                continue

            # Pitch selection: constrained by epsilon
            if rng.random() < epsilon:
                # Epsilon allows breaking constraints
                pitch = base_note + rng.randint(0, 25)
            else:
                # Stay on scale
                degree = rng.choice(scale)
                octave = rng.choice([0, 12, 24])
                pitch = base_note + degree + octave

            # Snap to grid with epsilon-dependent jitter
            jitter = rng.normal(0, epsilon * 0.1)
            actual_pos = beat_position + sub / grid_res + jitter

            events.append({
                "pitch": int(pitch),
                "beat_position": actual_pos,
                "velocity": float(rng.uniform(0.3, 1.0)),
            })
            pitches.append(int(pitch))

    return {
        "pitches": pitches,
        "events": events,
        "genre": genre,
        "epsilon": epsilon,
        "seed": seed,
        "n_bars": n_bars,
        "bpm": bpm,
        "grid_resolution": grid_res,
    }


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_experiment(
    n_steps: int = 20,
    n_compositions: int = 10,
    genres: List[str] = None,
    output_dir: str = None,
) -> Tuple[str, str]:
    """Run the epsilon sweep experiment.

    Returns (csv_path, figure_dir).
    """
    genres = genres or ["jazz", "hiphop", "electronic", "classical", "math"]
    output_dir = output_dir or str(Path(__file__).resolve().parent.parent / "experiments" / "output" / "epsilon_sweep")
    os.makedirs(output_dir, exist_ok=True)
    fig_dir = os.path.join(output_dir, "figures")
    os.makedirs(fig_dir, exist_ok=True)

    epsilons = np.linspace(0.01, 1.0, n_steps)
    results = []

    print(f"EPSILON SWEEP: {n_steps} epsilons × {n_compositions} comps × {len(genres)} genres")
    print("=" * 70)

    for eps_idx, epsilon in enumerate(epsilons):
        print(f"  ε = {epsilon:.3f} ({eps_idx + 1}/{n_steps})...", end="", flush=True)
        t_start = time.time()

        for genre in genres:
            for comp_idx in range(n_compositions):
                seed = int(epsilon * 1000) * 10000 + hash(genre) % 10000 + comp_idx
                seed = abs(seed) % (2**31)

                t_gen_start = time.time()
                comp = generate_composition(genre, epsilon, seed)
                gen_time = time.time() - t_gen_start

                pitches = comp["pitches"]
                events = comp["events"]

                metrics = {
                    "epsilon": round(epsilon, 4),
                    "genre": genre,
                    "composition": comp_idx,
                    "unique_pitches": unique_pitch_count(pitches),
                    "entropy": round(shannon_entropy(pitches), 4),
                    "syncopation": round(syncopation_score(events, comp["grid_resolution"]), 4),
                    "constraint_violations": constraint_violations(pitches, epsilon),
                    "n_events": len(events),
                    "generation_time_s": round(gen_time, 6),
                }
                results.append(metrics)

        elapsed = time.time() - t_start
        print(f" done ({elapsed:.2f}s)")

    # Write CSV
    csv_path = os.path.join(output_dir, "epsilon_sweep_results.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"\nCSV saved: {csv_path}")

    # Generate plots
    _plot_results(results, epsilons, genres, fig_dir)

    return csv_path, fig_dir


def _plot_results(results: List[Dict], epsilons: np.ndarray, genres: List[str], fig_dir: str):
    """Generate matplotlib plots from results."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Group by (epsilon, genre)
    from collections import defaultdict
    grouped = defaultdict(list)
    for r in results:
        grouped[(r["epsilon"], r["genre"])].append(r)

    metrics_to_plot = ["unique_pitches", "entropy", "syncopation", "constraint_violations"]
    metric_labels = ["Unique Pitches", "Shannon Entropy", "Syncopation Score", "Constraint Violations"]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Epsilon Sweep: Musical Metrics vs Constraint Tightness", fontsize=14, fontweight="bold")

    for ax, metric, label in zip(axes.flat, metrics_to_plot, metric_labels):
        for genre in genres:
            xs = []
            ys = []
            for eps in epsilons:
                key = (round(eps, 4), genre)
                vals = [r[metric] for r in grouped.get(key, [])]
                if vals:
                    xs.append(eps)
                    ys.append(np.mean(vals))
            ax.plot(xs, ys, marker="o", markersize=3, label=genre, alpha=0.8)

        ax.set_xlabel("Epsilon (constraint tightness)")
        ax.set_ylabel(label)
        ax.set_title(label)
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "epsilon_sweep_metrics.png"), dpi=150)
    plt.close()

    # Inverted-U analysis: composite "interest" score
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    for genre in genres:
        xs = []
        interest = []
        for eps in epsilons:
            key = (round(eps, 4), genre)
            vals = grouped.get(key, [])
            if vals:
                avg_ent = np.mean([v["entropy"] for v in vals])
                avg_sync = np.mean([v["syncopation"] for v in vals])
                avg_unique = np.mean([v["unique_pitches"] for v in vals])
                # Normalize and combine
                interest_score = 0.4 * avg_ent / 5.0 + 0.3 * avg_sync + 0.3 * avg_unique / 25.0
                xs.append(eps)
                interest.append(interest_score)
        ax2.plot(xs, interest, marker="o", markersize=3, label=genre, linewidth=2)

    ax2.set_xlabel("Epsilon (constraint tightness)")
    ax2.set_ylabel("Composite Interest Score")
    ax2.set_title("Hypothesis Test: Inverted-U Curve of Musical Interest")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.axvline(x=0.3, color="gray", linestyle="--", alpha=0.5, label="Predicted sweet spot")

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "inverted_u_interest.png"), dpi=150)
    plt.close()

    # Generation time plot
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    for genre in genres:
        xs = []
        ys = []
        for eps in epsilons:
            key = (round(eps, 4), genre)
            vals = grouped.get(key, [])
            if vals:
                xs.append(eps)
                ys.append(np.mean([v["generation_time_s"] for v in vals]))
        ax3.plot(xs, ys, marker="o", markersize=3, label=genre)
    ax3.set_xlabel("Epsilon")
    ax3.set_ylabel("Generation Time (s)")
    ax3.set_title("Generation Time vs Constraint Tightness")
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "generation_time.png"), dpi=150)
    plt.close()

    print(f"Figures saved to: {fig_dir}")


if __name__ == "__main__":
    csv_path, fig_dir = run_experiment()
    print(f"\nDone! Results: {csv_path}")
    print(f"Figures: {fig_dir}")
