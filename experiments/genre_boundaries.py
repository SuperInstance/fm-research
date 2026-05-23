#!/usr/bin/env python3
"""
Genre Boundaries — Where do genres blur?

Interpolate between genre presets in 20 steps (jazz→blues, jazz→classical,
electronic→hiphop, etc.). At each step, generate a composition and analyze.

Find: where does it stop sounding like genre A and start sounding like genre B?
Output: boundary heatmap.
Discovery: are there "no-genre" zones?
"""

import csv
import math
import os
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "flux-tensor-midi"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "constraint-theory-core"))

from flux_tensor_midi.genre_brain import GenreBrain


# ---------------------------------------------------------------------------
# Genre interpolation
# ---------------------------------------------------------------------------

def interpolate_presets(genre_a: str, genre_b: str, t: float) -> Dict:
    """Linearly interpolate between two genre presets.

    t=0 → pure genre A, t=1 → pure genre B.
    Returns interpolated preset dict.
    """
    brain_a = GenreBrain(genre_a)
    brain_b = GenreBrain(genre_b)
    preset_a = brain_a.get_preset()
    preset_b = brain_b.get_preset()

    result = {}

    # Interpolate numeric fields
    for key in ["default_bpm", "base_note", "grid_resolution", "loop_bars", "ewma_alpha"]:
        va = preset_a.get(key, 0)
        vb = preset_b.get(key, 0)
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            result[key] = va * (1 - t) + vb * t
        else:
            result[key] = va

    # Interpolate salience profiles (average across voices)
    sal_a = np.array(preset_a["salience_profiles"])
    sal_b = np.array(preset_b["salience_profiles"])
    result["salience"] = np.mean(sal_a * (1 - t) + sal_b * t, axis=0).tolist()

    # Interpolate tolerance profiles
    tol_a = np.array(preset_a["tolerance_profiles"])
    tol_b = np.array(preset_b["tolerance_profiles"])
    result["tolerance"] = np.mean(tol_a * (1 - t) + tol_b * t, axis=0).tolist()

    result["genre_a"] = genre_a
    result["genre_b"] = genre_b
    result["t"] = t

    return result


def shannon_entropy(pitches: List[int]) -> float:
    if not pitches:
        return 0.0
    counts = Counter(pitches)
    total = len(pitches)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def generate_interpolated_composition(preset: Dict, seed: int) -> Dict:
    """Generate a composition from an interpolated genre preset."""
    rng = np.random.RandomState(seed)

    bpm = int(preset.get("default_bpm", 120))
    base_note = int(preset.get("base_note", 60))
    grid_res = int(preset.get("grid_resolution", 4))
    n_bars = int(preset.get("loop_bars", 8))
    salience = preset.get("salience", [0.5] * 9)
    tolerance = preset.get("tolerance", [0.2] * 9)

    # Chromatic scale
    scale = list(range(25))

    total_beats = n_bars * 4
    pitches = []
    events = []

    for beat in range(total_beats):
        beat_pos = beat / grid_res
        # Activity level driven by salience
        activity = np.mean(salience[:6])
        n_notes = max(1, int(rng.poisson(activity * 3)))

        for _ in range(n_notes):
            if rng.random() > activity:
                continue

            # Pitch driven by tolerance: high tolerance → wider jumps
            max_jump = int(3 + np.mean(tolerance[:6]) * 20)
            if pitches:
                last = pitches[-1]
                pitch = last + rng.randint(-max_jump, max_jump + 1)
                pitch = max(base_note - 12, min(base_note + 36, pitch))
            else:
                pitch = base_note + rng.randint(0, 13)

            jitter = rng.normal(0, np.mean(tolerance[:6]) * 0.05)
            events.append({
                "pitch": pitch,
                "beat_position": beat_pos + jitter,
            })
            pitches.append(pitch)

    return {"pitches": pitches, "events": events}


def genre_distance_metrics(comp: Dict, genre: str) -> Dict:
    """Compute how 'close' a composition is to a specific genre."""
    brain = GenreBrain(genre)
    preset = brain.get_preset()

    pitches = comp["pitches"]
    base = int(preset.get("base_note", 60))

    # Pitch center distance
    if pitches:
        pitch_center = np.mean(pitches)
        center_dist = abs(pitch_center - base) / 12.0
    else:
        center_dist = 5.0

    # Scale conformance (approximate)
    genre_scales = {
        "jazz": {0, 2, 3, 5, 7, 9, 10},
        "hiphop": {0, 3, 5, 7, 10},
        "electronic": {0, 3, 5, 7, 10},
        "classical": {0, 2, 4, 5, 7, 9, 11},
        "math": {0, 2, 4, 7, 9},
    }
    scale = genre_scales.get(genre, {0, 2, 4, 5, 7, 9, 11})

    if pitches:
        in_scale = sum(1 for p in pitches if (p - base) % 12 in scale) / len(pitches)
    else:
        in_scale = 0.0

    return {
        "center_distance": round(center_dist, 4),
        "scale_conformance": round(in_scale, 4),
        "genre": genre,
    }


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

TRANSITIONS = [
    ("jazz", "classical"),
    ("jazz", "hiphop"),
    ("electronic", "hiphop"),
    ("classical", "math"),
    ("electronic", "classical"),
    ("jazz", "math"),
]


def run_experiment(
    n_steps: int = 20,
    n_compositions: int = 5,
    transitions: List[Tuple[str, str]] = None,
    output_dir: str = None,
) -> Tuple[str, str]:
    transitions = transitions or TRANSITIONS
    output_dir = output_dir or str(Path(__file__).resolve().parent.parent / "experiments" / "output" / "genre_boundaries")
    os.makedirs(output_dir, exist_ok=True)
    fig_dir = os.path.join(output_dir, "figures")
    os.makedirs(fig_dir, exist_ok=True)

    ts = np.linspace(0, 1, n_steps)
    results = []

    print(f"GENRE BOUNDARIES: {len(transitions)} transitions × {n_steps} steps × {n_compositions} comps")
    print("=" * 70)

    for genre_a, genre_b in transitions:
        print(f"  {genre_a} → {genre_b}...", end="", flush=True)
        for t in ts:
            preset = interpolate_presets(genre_a, genre_b, t)
            for comp_idx in range(n_compositions):
                seed = int(t * 1000) * 100 + hash((genre_a, genre_b)) % 1000 + comp_idx * 13
                seed = abs(seed) % (2**31)

                comp = generate_interpolated_composition(preset, seed)
                pitches = comp["pitches"]

                metrics_a = genre_distance_metrics(comp, genre_a)
                metrics_b = genre_distance_metrics(comp, genre_b)

                results.append({
                    "genre_a": genre_a,
                    "genre_b": genre_b,
                    "t": round(t, 4),
                    "composition": comp_idx,
                    "n_events": len(comp["events"]),
                    "entropy": round(shannon_entropy(pitches), 4),
                    "unique_pitches": len(set(pitches)),
                    "scale_conf_a": metrics_a["scale_conformance"],
                    "scale_conf_b": metrics_b["scale_conformance"],
                    "center_dist_a": metrics_a["center_distance"],
                    "center_dist_b": metrics_b["center_distance"],
                })
        print(" done")

    # Write CSV
    csv_path = os.path.join(output_dir, "genre_boundaries_results.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"\nCSV saved: {csv_path}")

    _plot_results(results, transitions, n_steps, fig_dir)

    return csv_path, fig_dir


def _plot_results(results: List[Dict], transitions: List[Tuple[str, str]], n_steps: int, fig_dir: str):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Boundary crossover plot for each transition
    n_trans = len(transitions)
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("Genre Boundaries: Where Do Genres Blur?", fontsize=14, fontweight="bold")

    for idx, (ga, gb) in enumerate(transitions):
        ax = axes.flat[idx]
        subset = [r for r in results if r["genre_a"] == ga and r["genre_b"] == gb]

        # Group by t
        ts = sorted(set(r["t"] for r in subset))
        conf_a = [np.mean([r["scale_conf_a"] for r in subset if r["t"] == t]) for t in ts]
        conf_b = [np.mean([r["scale_conf_b"] for r in subset if r["t"] == t]) for t in ts]

        ax.plot(ts, conf_a, label=f"{ga} conformance", linewidth=2)
        ax.plot(ts, conf_b, label=f"{gb} conformance", linewidth=2)

        # Find crossover
        for i in range(len(ts) - 1):
            if (conf_a[i] - conf_b[i]) * (conf_a[i+1] - conf_b[i+1]) < 0:
                cross_t = ts[i] + (ts[i+1] - ts[i]) * 0.5
                ax.axvline(x=cross_t, color="red", linestyle="--", alpha=0.7)
                ax.annotate(f"boundary\n@t={cross_t:.2f}", xy=(cross_t, 0.5),
                           fontsize=7, ha="center", color="red")

        ax.set_xlabel("Interpolation (t)")
        ax.set_ylabel("Scale Conformance")
        ax.set_title(f"{ga} → {gb}")
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "genre_boundary_crossovers.png"), dpi=150)
    plt.close()

    # No-genre zone heatmap
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    genres = sorted(set(g for pair in transitions for g in pair))
    n = len(genres)
    boundary_matrix = np.zeros((n, n))

    genre_idx = {g: i for i, g in enumerate(genres)}
    for ga, gb in transitions:
        subset = [r for r in results if r["genre_a"] == ga and r["genre_b"] == gb]
        ts = sorted(set(r["t"] for r in subset))
        conf_a = [np.mean([r["scale_conf_a"] for r in subset if r["t"] == t]) for t in ts]
        conf_b = [np.mean([r["scale_conf_b"] for r in subset if r["t"] == t]) for t in ts]

        # Find the "no-genre zone" width: where both confidences are < 0.6
        no_genre_width = sum(1 for a, b in zip(conf_a, conf_b) if a < 0.6 and b < 0.6)
        no_genre_fraction = no_genre_width / max(len(ts), 1)

        i, j = genre_idx[ga], genre_idx[gb]
        boundary_matrix[i, j] = no_genre_fraction
        boundary_matrix[j, i] = no_genre_fraction

    im = ax2.imshow(boundary_matrix, cmap="YlOrRd", vmin=0, vmax=1, aspect="auto")
    ax2.set_xticks(range(n))
    ax2.set_yticks(range(n))
    ax2.set_xticklabels(genres, rotation=45, ha="right")
    ax2.set_yticklabels(genres)
    ax2.set_title("No-Genre Zone Width (fraction of interpolation where neither genre dominates)")
    plt.colorbar(im, ax=ax2, label="No-genre fraction")

    for i in range(n):
        for j in range(n):
            val = boundary_matrix[i, j]
            if val > 0:
                ax2.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "no_genre_heatmap.png"), dpi=150)
    plt.close()

    print(f"Figures saved to: {fig_dir}")


if __name__ == "__main__":
    csv_path, fig_dir = run_experiment()
    print(f"\nDone! Results: {csv_path}")
