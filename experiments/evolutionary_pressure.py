#!/usr/bin/env python3
"""
Evolutionary Pressure — Does evolution actually improve music?

Run 100 generations of the genome evolution system.
Track fitness over time.
Analyze best composition from gen 1, 25, 50, 75, 100.
Measure: is the improvement real or just fitting the fitness function?

Output: evolution trajectory + quality metrics.
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

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "flux-tensor-midi"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "constraint-theory-core"))

from flux_tensor_midi.genre_brain import GenreBrain
from constraint_theory_core.lattice import snap, covering_radius


# ---------------------------------------------------------------------------
# Musical genome
# ---------------------------------------------------------------------------

class MusicalGenome:
    """A genome encoding a musical composition.

    Genome structure:
    - scale_weights: 12 floats controlling pitch class probabilities
    - rhythm_density: float controlling note density
    - syncopation: float controlling off-beat tendency
    - interval_bias: float controlling melodic interval sizes
    - articulation: float controlling note lengths
    - dynamics_range: float controlling velocity variation
    """

    N_GENES = 18  # 12 scale + 6 params

    def __init__(self, genes: np.ndarray = None, rng: np.random.RandomState = None):
        if genes is not None:
            self.genes = np.array(genes, dtype=float)
        else:
            rng = rng or np.random.RandomState()
            # Scale weights + 6 params
            self.genes = rng.dirichlet(np.ones(12)).tolist() + rng.uniform(0.1, 0.9, 6).tolist()
            self.genes = np.array(self.genes)

    @property
    def scale_weights(self) -> np.ndarray:
        return self.genes[:12]

    @property
    def rhythm_density(self) -> float:
        return self.genes[12]

    @property
    def syncopation(self) -> float:
        return self.genes[13]

    @property
    def interval_bias(self) -> float:
        return self.genes[14]

    @property
    def articulation(self) -> float:
        return self.genes[15]

    @property
    def dynamics_range(self) -> float:
        return self.genes[16]

    @property
    def consonance_preference(self) -> float:
        return self.genes[17]

    def mutate(self, rate: float = 0.1, rng: np.random.RandomState = None) -> "MusicalGenome":
        rng = rng or np.random.RandomState()
        new_genes = self.genes.copy()
        for i in range(len(new_genes)):
            if rng.random() < rate:
                new_genes[i] += rng.normal(0, 0.1)
                new_genes[i] = np.clip(new_genes[i], 0.01, 1.0)
        # Renormalize scale weights
        new_genes[:12] /= new_genes[:12].sum()
        return MusicalGenome(new_genes)

    def crossover(self, other: "MusicalGenome", rng: np.random.RandomState = None) -> "MusicalGenome":
        rng = rng or np.random.RandomState()
        mask = rng.random(len(self.genes)) < 0.5
        child_genes = np.where(mask, self.genes, other.genes)
        # Renormalize scale weights
        child_genes[:12] /= child_genes[:12].sum()
        return MusicalGenome(child_genes)

    def to_dict(self) -> Dict:
        return {
            "scale_weights": self.scale_weights.tolist(),
            "rhythm_density": float(self.rhythm_density),
            "syncopation": float(self.syncopation),
            "interval_bias": float(self.interval_bias),
            "articulation": float(self.articulation),
            "dynamics_range": float(self.dynamics_range),
            "consonance_preference": float(self.consonance_preference),
        }


# ---------------------------------------------------------------------------
# Fitness functions
# ---------------------------------------------------------------------------

def fitness_function(genome: MusicalGenome, genre: str = "jazz") -> Tuple[float, Dict]:
    """Evaluate fitness of a genome for a given genre.

    Returns (fitness, metrics_dict).
    """
    weights = genome.scale_weights

    # 1. Scale conformance to genre
    genre_scales = {
        "jazz": [0.1, 0.02, 0.15, 0.12, 0.03, 0.12, 0.02, 0.1, 0.03, 0.15, 0.1, 0.06],
        "classical": [0.15, 0.02, 0.12, 0.02, 0.12, 0.12, 0.02, 0.15, 0.02, 0.12, 0.02, 0.12],
        "electronic": [0.12, 0.02, 0.03, 0.15, 0.02, 0.12, 0.02, 0.12, 0.02, 0.03, 0.15, 0.02],
        "hiphop": [0.15, 0.02, 0.03, 0.12, 0.02, 0.12, 0.02, 0.15, 0.02, 0.03, 0.15, 0.02],
        "math": [0.15, 0.05, 0.12, 0.02, 0.12, 0.02, 0.02, 0.15, 0.02, 0.12, 0.02, 0.02],
    }
    target = np.array(genre_scales.get(genre, genre_scales["jazz"]))
    scale_fitness = 1.0 - np.mean(np.abs(weights - target))

    # 2. Rhythmic variety (not too sparse, not too dense)
    density = genome.rhythm_density
    density_fitness = 1.0 - 2.0 * abs(density - 0.5)

    # 3. Syncopation balance (moderate is best)
    sync = genome.syncopation
    sync_fitness = 1.0 - 2.0 * abs(sync - 0.4)

    # 4. Interval variety (moderate intervals)
    interval = genome.interval_bias
    interval_fitness = 1.0 - 2.0 * abs(interval - 0.5)

    # 5. Consonance preference (genre-dependent sweet spot)
    cons = genome.consonance_preference
    cons_target = {"jazz": 0.5, "classical": 0.7, "electronic": 0.3, "hiphop": 0.4, "math": 0.6}
    cons_fitness = 1.0 - 2.0 * abs(cons - cons_target.get(genre, 0.5))

    # Weighted combination
    fitness = (
        0.30 * scale_fitness +
        0.20 * density_fitness +
        0.15 * sync_fitness +
        0.15 * interval_fitness +
        0.20 * cons_fitness
    )

    metrics = {
        "scale_fitness": round(scale_fitness, 4),
        "density_fitness": round(density_fitness, 4),
        "sync_fitness": round(sync_fitness, 4),
        "interval_fitness": round(interval_fitness, 4),
        "cons_fitness": round(cons_fitness, 4),
    }

    return fitness, metrics


# ---------------------------------------------------------------------------
# Quality metrics (independent of fitness function)
# ---------------------------------------------------------------------------

def independent_quality(genome: MusicalGenome, n_notes: int = 200, seed: int = 42) -> Dict:
    """Generate a composition and measure quality independently of fitness."""
    rng = np.random.RandomState(seed)

    # Generate notes from genome
    base = 60
    pitches = []
    for _ in range(n_notes):
        pc = rng.choice(12, p=genome.scale_weights)
        octave = rng.choice([0, 12, 24], p=[0.3, 0.5, 0.2])
        pitches.append(base + pc + octave)

    # Entropy
    counts = Counter(pitches)
    total = len(pitches)
    entropy = -sum((c / total) * math.log2(c / total) for c in counts.values())

    # Pitch range
    pitch_range = max(pitches) - min(pitches) if pitches else 0

    # Interval distribution
    intervals = [abs(pitches[i+1] - pitches[i]) for i in range(len(pitches) - 1)]
    interval_variety = len(set(intervals)) if intervals else 0

    # Consonance check (fraction of consonant intervals)
    consonant_intervals = {0, 3, 4, 5, 7, 8, 9, 12}
    consonant_frac = sum(1 for iv in intervals if iv % 12 in consonant_intervals) / max(len(intervals), 1)

    return {
        "entropy": round(entropy, 4),
        "pitch_range": pitch_range,
        "interval_variety": interval_variety,
        "consonant_fraction": round(consonant_frac, 4),
        "unique_pitches": len(set(pitches)),
    }


# ---------------------------------------------------------------------------
# Evolution
# ---------------------------------------------------------------------------

def run_evolution(
    n_generations: int = 100,
    pop_size: int = 50,
    genre: str = "jazz",
    seed: int = 42,
) -> Tuple[List[Dict], List[Dict]]:
    """Run evolutionary optimization.

    Returns (generation_results, best_per_generation).
    """
    rng = np.random.RandomState(seed)

    # Initialize population
    population = [MusicalGenome(rng=rng) for _ in range(pop_size)]

    generation_results = []
    best_at_checkpoints = []

    for gen in range(n_generations):
        # Evaluate fitness
        fitnesses = []
        all_metrics = []
        for genome in population:
            fit, metrics = fitness_function(genome, genre)
            fitnesses.append(fit)
            all_metrics.append(metrics)

        fitnesses = np.array(fitnesses)

        # Track stats
        best_idx = np.argmax(fitnesses)
        worst_idx = np.argmin(fitnesses)
        best_genome = population[best_idx]

        gen_result = {
            "generation": gen,
            "best_fitness": round(float(fitnesses[best_idx]), 6),
            "worst_fitness": round(float(fitnesses[worst_idx]), 6),
            "mean_fitness": round(float(np.mean(fitnesses)), 6),
            "std_fitness": round(float(np.std(fitnesses)), 6),
            "best_scale_fit": all_metrics[best_idx]["scale_fitness"],
            "best_density_fit": all_metrics[best_idx]["density_fitness"],
            "best_sync_fit": all_metrics[best_idx]["sync_fitness"],
        }
        generation_results.append(gen_result)

        # Checkpoint analysis
        if gen in [0, 24, 49, 74, 99]:
            quality = independent_quality(best_genome, seed=seed + gen)
            best_at_checkpoints.append({
                "generation": gen,
                "fitness": round(float(fitnesses[best_idx]), 6),
                **quality,
                **best_genome.to_dict(),
            })

        # Selection (tournament)
        new_population = [best_genome]  # Elitism
        while len(new_population) < pop_size:
            # Tournament selection
            t1, t2 = rng.choice(pop_size, 2, replace=False)
            parent1 = population[t1] if fitnesses[t1] > fitnesses[t2] else population[t2]
            t3, t4 = rng.choice(pop_size, 2, replace=False)
            parent2 = population[t3] if fitnesses[t3] > fitnesses[t4] else population[t4]

            # Crossover
            child = parent1.crossover(parent2, rng=rng)

            # Mutate (higher rate early, lower late)
            mutation_rate = 0.15 * (1.0 - gen / n_generations)
            child = child.mutate(rate=mutation_rate, rng=rng)

            new_population.append(child)

        population = new_population

    return generation_results, best_at_checkpoints


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_experiment(
    n_generations: int = 100,
    genres: List[str] = None,
    output_dir: str = None,
) -> Tuple[str, str]:
    genres = genres or ["jazz", "classical", "electronic"]
    output_dir = output_dir or str(Path(__file__).resolve().parent.parent / "experiments" / "output" / "evolutionary_pressure")
    os.makedirs(output_dir, exist_ok=True)
    fig_dir = os.path.join(output_dir, "figures")
    os.makedirs(fig_dir, exist_ok=True)

    all_results = []
    all_checkpoints = []

    print(f"EVOLUTIONARY PRESSURE: {n_generations} generations × {len(genres)} genres")
    print("=" * 70)

    for genre in genres:
        print(f"  Evolving {genre}...", end="", flush=True)
        t_start = time.time()

        gen_results, checkpoints = run_evolution(
            n_generations=n_generations, genre=genre, seed=hash(genre) % 10000
        )
        for r in gen_results:
            r["genre"] = genre
        for c in checkpoints:
            c["genre"] = genre

        all_results.extend(gen_results)
        all_checkpoints.extend(checkpoints)

        print(f" done ({time.time() - t_start:.2f}s)")

    # Write CSVs
    csv_path = os.path.join(output_dir, "evolution_results.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
        writer.writeheader()
        writer.writerows(all_results)

    ck_csv_path = os.path.join(output_dir, "checkpoint_quality.csv")
    with open(ck_csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_checkpoints[0].keys())
        writer.writeheader()
        writer.writerows(all_checkpoints)

    print(f"\nCSVs saved: {csv_path}, {ck_csv_path}")

    _plot_results(all_results, all_checkpoints, genres, n_generations, fig_dir)

    return csv_path, fig_dir


def _plot_results(results, checkpoints, genres, n_gen, fig_dir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Fitness trajectory
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Evolutionary Pressure: Does Evolution Improve Music?", fontsize=14, fontweight="bold")

    for genre in genres:
        subset = [r for r in results if r["genre"] == genre]
        gens = [r["generation"] for r in subset]
        bests = [r["best_fitness"] for r in subset]
        means = [r["mean_fitness"] for r in subset]
        stds = [r["std_fitness"] for r in subset]

        axes[0].plot(gens, bests, label=f"{genre} (best)", linewidth=2)
        axes[0].fill_between(gens,
                             [m - s for m, s in zip(means, stds)],
                             [m + s for m, s in zip(means, stds)],
                             alpha=0.1)

    axes[0].set_xlabel("Generation")
    axes[0].set_ylabel("Fitness")
    axes[0].set_title("Fitness Trajectory")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Independent quality at checkpoints
    check_gens = [0, 24, 49, 74, 99]
    for genre in genres:
        ck = [c for c in checkpoints if c["genre"] == genre]
        if ck:
            axes[1].plot([c["generation"] for c in ck],
                        [c["entropy"] for c in ck],
                        marker="o", label=f"{genre} entropy", linewidth=2)
            axes[1].plot([c["generation"] for c in ck],
                        [c["consonant_fraction"] for c in ck],
                        marker="s", label=f"{genre} consonance", linewidth=1.5, linestyle="--")

    axes[1].set_xlabel("Generation")
    axes[1].set_ylabel("Independent Quality Metric")
    axes[1].set_title("Independent Quality (not fitness function)")
    axes[1].legend(fontsize=7)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "evolution_trajectory.png"), dpi=150)
    plt.close()

    # Fitness vs Quality correlation
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    for genre in genres:
        ck = [c for c in checkpoints if c["genre"] == genre]
        if ck:
            ax2.scatter([c["fitness"] for c in ck],
                       [c["entropy"] for c in ck],
                       marker="o", s=100, label=genre)
            for c in ck:
                ax2.annotate(f"G{c['generation']}", (c["fitness"], c["entropy"]),
                            fontsize=7, ha="center", va="bottom")

    ax2.set_xlabel("Fitness Score")
    ax2.set_ylabel("Independent Entropy")
    ax2.set_title("Fitness vs Independent Quality: Is Improvement Real?")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "fitness_vs_quality.png"), dpi=150)
    plt.close()

    print(f"Figures saved to: {fig_dir}")


if __name__ == "__main__":
    csv_path, fig_dir = run_experiment()
    print(f"\nDone! Results: {csv_path}")
