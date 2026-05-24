#!/usr/bin/env python3
"""
Experiment 54: Genetic Algorithms ON the Attractor — Evolving Lorenz Equations

PARADIGM SHIFT: Instead of searching within the parameter space of the Lorenz 
system (σ, ρ, β), we evolve the STRUCTURE of the equations themselves. We mutate
terms, add nonlinearities, remove couplings. This searches a meta-space of 
dynamical systems, not a parameter space within one system.

The question: Are there attractors more musical than Lorenz? More creative? 
More structured? We can't find them by tuning Lorenz's dials — we need to 
evolve new equations entirely.

GPU-ready: Population-level simulation parallelized via NumPy vectorization.
CUDA version would use one thread block per genome.
"""

import numpy as np
import json
import os
import time
import copy
import random
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from pathlib import Path

# ============================================================
# GENOME REPRESENTATION
# ============================================================

@dataclass
class Term:
    """A single term in a differential equation: coeff * x^p1 * y^p2 * z^p3"""
    coeff: float
    powers: Tuple[float, float, float]  # powers for x, y, z
    
    def evaluate(self, state: np.ndarray) -> float:
        x, y, z = state
        return self.coeff * (x ** self.powers[0]) * (y ** self.powers[1]) * (z ** self.powers[2])
    
    def mutate(self, rate: float = 0.1) -> 'Term':
        new_coeff = self.coeff
        new_powers = list(self.powers)
        
        if random.random() < rate:
            new_coeff *= np.random.normal(1.0, 0.3)
        if random.random() < rate:
            idx = random.randint(0, 2)
            new_powers[idx] = max(0.0, new_powers[idx] + np.random.normal(0, 0.5))
        
        return Term(new_coeff, tuple(new_powers))


@dataclass
class EquationGenome:
    """A complete 3D dynamical system encoded as evolvable equations.
    
    genes[0] = list of terms for dx/dt
    genes[1] = list of terms for dy/dt  
    genes[2] = list of terms for dz/dt
    """
    genes: List[List[Term]]
    fitness: float = float('-inf')
    generation_born: int = 0
    
    def derivative(self, state: np.ndarray) -> np.ndarray:
        """Compute dx/dt, dy/dt, dz/dt for this genome."""
        return np.array([
            sum(term.evaluate(state) for term in eq)
            for eq in self.genes
        ])
    
    def mutate(self, rate: float = 0.15) -> 'EquationGenome':
        """Structural mutation: change coefficients, powers, add/remove terms."""
        new_genes = []
        for eq in self.genes:
            new_eq = []
            for term in eq:
                if random.random() < 0.8:  # 80% chance to keep each term
                    new_eq.append(term.mutate(rate))
            new_genes.append(new_eq)
            
            # Chance to add a new term
            if random.random() < rate:
                var = random.randint(0, 2)
                powers = [0.0, 0.0, 0.0]
                powers[var] = random.choice([0.5, 1.0, 1.5, 2.0])
                coeff = np.random.normal(0, 5.0)
                new_genes[-1].append(Term(coeff, tuple(powers)))
            
            # Chance to add a cross-term
            if random.random() < rate * 0.5:
                v1, v2 = random.sample(range(3), 2)
                powers = [0.0, 0.0, 0.0]
                powers[v1] = 1.0
                powers[v2] = 1.0
                coeff = np.random.normal(0, 2.0)
                new_genes[-1].append(Term(coeff, tuple(powers)))
        
        return EquationGenome(new_genes, generation_born=self.generation_born + 1)
    
    def crossover(self, other: 'EquationGenome') -> 'EquationGenome':
        """Crossover: take equations from each parent."""
        new_genes = []
        for i in range(3):
            if random.random() < 0.5:
                new_genes.append(copy.deepcopy(self.genes[i]))
            else:
                new_genes.append(copy.deepcopy(other.genes[i]))
        return EquationGenome(new_genes)
    
    def to_dict(self) -> dict:
        return {
            'genes': [
                [{'coeff': t.coeff, 'powers': list(t.powers)} for t in eq]
                for eq in self.genes
            ],
            'fitness': self.fitness,
        }
    
    def __repr__(self):
        var_names = ['x', 'y', 'z']
        equations = []
        for i, eq in enumerate(self.genes):
            terms_str = ' + '.join(
                f"{t.coeff:.2f}·{'·'.join(f'{var_names[j]}^{t.powers[j]}' for j in range(3) if t.powers[j] != 0) or '1'}"
                for t in eq
            )
            equations.append(f"d{var_names[i]}/dt = {terms_str}")
        return '\n'.join(equations)


def standard_lorenz_genome() -> EquationGenome:
    """The classic Lorenz system as a genome."""
    return EquationGenome([
        # dx/dt = σ(y - x)
        [Term(10.0, (0.0, 1.0, 0.0)), Term(-10.0, (1.0, 0.0, 0.0))],
        # dy/dt = x(ρ - z) - y = ρx - xz - y
        [Term(28.0, (1.0, 0.0, 0.0)), Term(-1.0, (1.0, 0.0, 1.0)), Term(-1.0, (0.0, 1.0, 0.0))],
        # dz/dt = xy - βz
        [Term(1.0, (1.0, 1.0, 0.0)), Term(-8.0/3.0, (0.0, 0.0, 1.0))],
    ])


# ============================================================
# SIMULATION (GPU-READY)
# ============================================================

def simulate_genome(genome: EquationGenome, steps: int = 10000, 
                    dt: float = 0.01, ic: Optional[np.ndarray] = None) -> Tuple[np.ndarray, bool]:
    """RK4 integration of a genome. Returns (trajectory, diverged)."""
    state = ic if ic is not None else np.array([1.0, 1.0, 1.0])
    trajectory = np.zeros((steps, 3))
    diverged = False
    
    for i in range(steps):
        k1 = genome.derivative(state)
        k2 = genome.derivative(state + 0.5 * dt * k1)
        k3 = genome.derivative(state + 0.5 * dt * k2)
        k4 = genome.derivative(state + dt * k3)
        
        state = state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        
        if np.any(np.abs(state) > 1e6) or np.any(np.isnan(state)):
            trajectory[i:] = np.nan
            diverged = True
            break
        
        trajectory[i] = state
    
    return trajectory, diverged


def simulate_population(genomes: List[EquationGenome], steps: int = 5000) -> List[Tuple[np.ndarray, bool]]:
    """Simulate entire population. In CUDA, each genome gets its own thread."""
    return [simulate_genome(g, steps) for g in genomes]


# ============================================================
# FITNESS FUNCTIONS
# ============================================================

def compute_lyapunov_exponent(trajectory: np.ndarray, dt: float = 0.01, 
                               genome: Optional[EquationGenome] = None) -> float:
    """Estimate largest Lyapunov exponent from trajectory."""
    if len(trajectory) < 100:
        return -1e6
    
    # Use divergence of nearby points in trajectory
    clean = trajectory[~np.any(np.isnan(trajectory), axis=1)]
    if len(clean) < 100:
        return -1e6
    
    # Find nearby pairs
    n = len(clean)
    lyap_sum = 0.0
    count = 0
    
    for i in range(0, n - 1, 10):
        d0 = np.linalg.norm(clean[min(i+1, n-1)] - clean[i])
        if d0 > 0:
            # Local stretching rate
            diffs = np.diff(clean[i:i+10], axis=0)
            if len(diffs) > 0:
                stretch = np.linalg.norm(diffs[-1]) / max(np.linalg.norm(diffs[0]), 1e-10)
                lyap_sum += np.log(max(stretch, 1e-10))
                count += 1
    
    return lyap_sum / max(count, 1)


def fitness_attractor_quality(trajectory: np.ndarray, diverged: bool) -> float:
    """
    Multi-criteria fitness for evolved attractors:
    1. Must not diverge
    2. Must be chaotic (not fixed point or limit cycle)
    3. Must have interesting structure (high variance in derivatives)
    4. Must be bounded (compact attractor)
    """
    if diverged:
        return -1e6
    
    clean = trajectory[~np.any(np.isnan(trajectory), axis=1)]
    if len(clean) < 100:
        return -1e6
    
    # 1. Boundedness
    max_val = np.max(np.abs(clean))
    if max_val > 1e4:
        return -1e4
    bounded_score = 1.0 / (1.0 + max_val / 100.0)
    
    # 2. Complexity: variance in derivatives (reject fixed points)
    diffs = np.diff(clean, axis=0)
    deriv_var = np.mean(np.var(diffs, axis=0))
    if deriv_var < 1e-6:  # essentially constant
        return -1e3
    
    # 3. Spectral complexity: FFT of x-coordinate
    fft = np.abs(np.fft.rfft(clean[:, 0] - clean[:, 0].mean()))
    spectral_entropy = -np.sum((fft/fft.sum() + 1e-10) * np.log(fft/fft.sum() + 1e-10))
    spectral_score = min(spectral_entropy / 5.0, 1.0)  # normalized
    
    # 4. Spatial extent: use all 3 dimensions
    spatial_extent = np.mean(np.std(clean, axis=0))
    
    # 5. Autocorrelation decay (complex = fast decay)
    if len(clean) > 200:
        ac = np.correlate(clean[:200, 0] - clean[:200, 0].mean(), 
                         clean[:200, 0] - clean[:200, 0].mean(), mode='full')
        ac = ac[len(ac)//2:]
        ac = ac / (ac[0] + 1e-10)
        decay_point = np.argmax(ac < 0.5)
        decay_score = min(decay_point / 50.0, 1.0)
    else:
        decay_score = 0.5
    
    # Combined fitness
    fitness = (bounded_score * 0.2 + 
               np.log1p(deriv_var) * 0.3 + 
               spectral_score * 0.2 + 
               np.log1p(spatial_extent) * 0.15 + 
               decay_score * 0.15)
    
    return fitness


# ============================================================
# EVOLUTION ENGINE
# ============================================================

def run_evolution(
    population_size: int = 60,
    generations: int = 150,
    steps: int = 8000,
    mutation_rate: float = 0.15,
    seed_genome: Optional[EquationGenome] = None,
    elite_count: int = 3,
    output_dir: str = "/tmp/fm-research/CODE/results"
) -> Tuple[EquationGenome, List[float]]:
    """
    Evolve dynamical system equations.
    
    Args:
        population_size: Number of genomes per generation
        generations: Number of evolution rounds
        steps: Simulation steps per fitness evaluation
        mutation_rate: Probability of structural mutation per gene
        seed_genome: Starting genome (default: standard Lorenz)
        elite_count: Number of top genomes carried forward unchanged
        output_dir: Where to save results
    
    Returns:
        (best_genome, fitness_history)
    """
    os.makedirs(output_dir, exist_ok=True)
    
    if seed_genome is None:
        seed_genome = standard_lorenz_genome()
    
    # Initialize population: seed + mutated variants
    population = [seed_genome]
    for _ in range(population_size - 1):
        population.append(seed_genome.mutate(rate=0.3))
    
    fitness_history = []
    best_ever = None
    best_ever_fitness = float('-inf')
    
    print("=" * 70)
    print("EXPERIMENT 54: GENETIC ALGORITHMS ON THE ATTRACTOR")
    print("Evolving equation STRUCTURES, not parameters")
    print("=" * 70)
    print(f"Population: {population_size} | Generations: {generations}")
    print(f"Seed genome: Standard Lorenz (σ=10, ρ=28, β=8/3)")
    print()
    
    start_time = time.time()
    
    for gen in range(generations):
        # Evaluate fitness
        results = simulate_population(population, steps)
        fits = np.array([fitness_attractor_quality(traj, div) for traj, div in results])
        
        # Track best
        gen_best_idx = np.argmax(fits)
        gen_best_fit = fits[gen_best_idx]
        fitness_history.append({
            'generation': gen,
            'best': float(gen_best_fit),
            'mean': float(fits.mean()),
            'std': float(fits.std()),
            'surviving': int(np.sum(fits > -1e3)),
        })
        
        if gen_best_fit > best_ever_fitness:
            best_ever_fitness = gen_best_fit
            best_ever = copy.deepcopy(population[gen_best_idx])
            best_ever.fitness = gen_best_fit
        
        # Logging
        if gen % 10 == 0 or gen == generations - 1:
            elapsed = time.time() - start_time
            print(f"Gen {gen:3d}/{generations}: best={gen_best_fit:8.4f} "
                  f"mean={fits.mean():8.4f} std={fits.std():6.4f} "
                  f"surviving={np.sum(fits > -1e3):3d}/{population_size} "
                  f"[{elapsed:.1f}s]")
        
        # Selection: tournament + elitism
        sorted_indices = np.argsort(fits)[::-1]
        new_population = []
        
        # Elitism
        for i in range(min(elite_count, len(sorted_indices))):
            idx = sorted_indices[i]
            if fits[idx] > -1e3:
                new_population.append(copy.deepcopy(population[idx]))
        
        # Fill rest with tournament-selected + mutated offspring
        while len(new_population) < population_size:
            # Tournament selection (size 3)
            candidates = np.random.choice(len(population), size=3, replace=False)
            candidate_fits = fits[candidates]
            winner = candidates[np.argmax(candidate_fits)]
            
            # Mutate winner
            child = population[winner].mutate(mutation_rate)
            new_population.append(child)
        
        population = new_population
    
    # Final results
    print("\n" + "=" * 70)
    print("EVOLUTION COMPLETE")
    print("=" * 70)
    print(f"\nBest fitness: {best_ever_fitness:.4f}")
    print(f"\nEvolved equations:")
    print(best_ever)
    
    # Simulate best for longer
    print("\nSimulating best genome for 50000 steps...")
    best_traj, best_div = simulate_genome(best_ever, steps=50000)
    
    # Save results
    results_data = {
        'experiment': 'genetic_lorenz',
        'best_fitness': float(best_ever_fitness),
        'best_genome': best_ever.to_dict(),
        'fitness_history': fitness_history,
        'trajectory_stats': {
            'mean': best_traj[~np.any(np.isnan(best_traj), axis=1)].mean(axis=0).tolist(),
            'std': best_traj[~np.any(np.isnan(best_traj), axis=1)].std(axis=0).tolist(),
            'max': np.nanmax(np.abs(best_traj)).tolist(),
        }
    }
    
    results_path = os.path.join(output_dir, 'EXPERIMENT-GENETIC-LORENZ.json')
    with open(results_path, 'w') as f:
        json.dump(results_data, f, indent=2, default=str)
    print(f"\nResults saved to {results_path}")
    
    # Save trajectory
    traj_path = os.path.join(output_dir, 'genetic_lorenz_trajectory.npy')
    np.save(traj_path, best_traj)
    print(f"Trajectory saved to {traj_path}")
    
    # Compare with standard Lorenz
    print("\n--- COMPARISON WITH STANDARD LORENZ ---")
    standard_traj, _ = simulate_genome(standard_lorenz_genome(), steps=50000)
    standard_fit = fitness_attractor_quality(standard_traj, False)
    print(f"Standard Lorenz fitness: {standard_fit:.4f}")
    print(f"Evolved genome fitness:  {best_ever_fitness:.4f}")
    if best_ever_fitness > standard_fit:
        print(f"\n>>> EVOLVED GENOME OUTPERFORMS STANDARD LORENZ by {best_ever_fitness - standard_fit:.4f} <<<")
    else:
        print(f"\nStandard Lorenz still superior by {standard_fit - best_ever_fitness:.4f}")
    
    return best_ever, fitness_history


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)
    
    best, history = run_evolution(
        population_size=60,
        generations=150,
        steps=8000,
        mutation_rate=0.15,
    )
    
    print("\nDone. The attractor has evolved.")
