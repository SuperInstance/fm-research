#!/usr/bin/env python3
"""
The Insight Wheel — GPU-accelerated iterative experiment engine.
Spins continuously, running novel experiments and extracting insights.
Each iteration builds on previous results.
"""

import numpy as np
import torch
import json
import time
import os
from itertools import product, combinations
from pathlib import Path

RESULTS_DIR = Path("/tmp/insight-wheel/results")
RESULTS_DIR.mkdir(exist_ok=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"🔥 Insight Wheel spinning on: {device}")

# ============================================================
# CORE: Lorenz-based creative system on GPU
# ============================================================

class LorenzCreativeEngine(torch.nn.Module):
    """Lorenz attractor mapped to creative dynamics, batched on GPU."""
    
    def __init__(self, batch_size=1000, device='cpu'):
        super().__init__()
        self.batch_size = batch_size
        self.device = device
        
        # Lorenz parameters (batched — each system can have different params)
        self.sigma = torch.full((batch_size,), 10.0, device=device)
        self.rho = torch.full((batch_size,), 28.0, device=device)
        self.beta = torch.full((batch_size,), 8/3, device=device)
        
        # State: [batch, 3] for (x, y, z)
        self.state = torch.randn(batch_size, 3, device=device) * 0.1
        
    def step(self, dt=0.01):
        """RK4 integration step on GPU."""
        x, y, z = self.state[:, 0], self.state[:, 1], self.state[:, 2]
        s, r, b = self.sigma, self.rho, self.beta
        
        def lorenz(x, y, z):
            dx = s * (y - x)
            dy = x * (r - z) - y
            dz = x * y - b * z
            return torch.stack([dx, dy, dz], dim=1)
        
        # RK4
        k1 = lorenz(x, y, z)
        s2 = self.state + 0.5 * dt * k1
        k2 = lorenz(s2[:, 0], s2[:, 1], s2[:, 2])
        s3 = self.state + 0.5 * dt * k2
        k3 = lorenz(s3[:, 0], s3[:, 1], s3[:, 2])
        s4 = self.state + dt * k3
        k4 = lorenz(s4[:, 0], s4[:, 1], s4[:, 2])
        
        self.state += (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)
        return self.state
    
    def creative_output(self):
        """Extract creative metrics from current state."""
        x, y, z = self.state[:, 0], self.state[:, 1], self.state[:, 2]
        
        # Divergence: how spread are the trajectories (creativity)
        divergence = torch.std(x)
        
        # Energy: total kinetic energy (creative power)
        energy = torch.mean(x**2 + y**2 + z**2)
        
        # Novelty: how far from initial conditions (exploration)
        novelty = torch.mean(torch.abs(x))
        
        # Complexity: entropy of binned positions
        x_binned = torch.histc(x, bins=50)
        x_binned = x_binned / (x_binned.sum() + 1e-10)
        complexity = -(x_binned * torch.log(x_binned + 1e-10)).sum()
        
        return {
            'divergence': float(divergence),
            'energy': float(energy),
            'novelty': float(novelty),
            'complexity': float(complexity)
        }

# ============================================================
# EXPERIMENT 1: ρ-Sweep with full metrics
# ============================================================

def experiment_rho_sweep():
    """Sweep stress parameter ρ across 1000 systems simultaneously."""
    print("\n" + "="*60)
    print("EXPERIMENT 1: ρ-Sweep (1000 systems on GPU)")
    print("="*60)
    
    N = 1000
    engine = LorenzCreativeEngine(N, device)
    
    # Different ρ for each system (logarithmically spaced)
    rho_values = torch.logspace(-1, 2, N, device=device)
    engine.rho = rho_values
    engine.sigma = torch.full((N,), 10.0, device=device)
    engine.beta = torch.full((N,), 8/3, device=device)
    
    # Warm up (skip transient)
    for _ in range(5000):
        engine.step()
    
    # Collect data
    results = []
    for step in range(2000):
        state = engine.step()
        
        if step % 200 == 0:
            # Compute metrics for each ρ
            x = state[:, 0]
            for i in range(0, N, N//20):  # sample 20 points
                rho_val = float(rho_values[i])
                x_slice = x[max(0,i-5):min(N,i+5)]
                results.append({
                    'rho': rho_val,
                    'step': step,
                    'x_std': float(torch.std(x_slice)),
                    'x_range': float(torch.max(x_slice) - torch.min(x_slice)),
                })
    
    # Find phase transitions
    print("\n  ρ → creative regime:")
    rho_samples = sorted(set(r['rho'] for r in results))
    for rho in rho_samples:
        step0 = [r for r in results if r['rho'] == rho and r['step'] == 0]
        step1800 = [r for r in results if r['rho'] == rho and r['step'] == 1800]
        if step0 and step1800:
            regime = "CHAOTIC" if step1800[0]['x_std'] > 2.0 else "PERIODIC" if step1800[0]['x_std'] > 0.1 else "FIXED"
            print(f"    ρ={rho:7.2f}: σ_x={step1800[0]['x_std']:6.3f} → {regime}")
    
    return results

# ============================================================
# EXPERIMENT 2: Coupled creative systems
# ============================================================

def experiment_coupled_creativity():
    """Couple N creative systems through consensus and measure sync vs creativity."""
    print("\n" + "="*60)
    print("EXPERIMENT 2: Coupled Creative Systems (Kuramoto + Lorenz)")
    print("="*60)
    
    N = 500
    engine = LorenzCreativeEngine(N, device)
    engine.rho = torch.full((N,), 28.0, device=device)  # all chaotic
    
    # Different coupling strengths
    K_values = [0.0, 0.001, 0.01, 0.1, 0.5, 1.0]
    
    results = []
    for K in K_values:
        engine.state = torch.randn(N, 3, device=device) * 0.1
        
        # Warm up
        for _ in range(2000):
            state = engine.step()
        
        # Measure with coupling
        metrics_list = []
        for step in range(1000):
            state = engine.step()
            
            # Apply coupling (consensus: move toward mean)
            if K > 0:
                mean_state = state.mean(dim=0, keepdim=True)
                state += K * (mean_state - state) * 0.01
                engine.state = state
            
            if step % 100 == 0:
                x = state[:, 0]
                # Order parameter (sync measure)
                z = torch.exp(1j * x * 10)  # map to phase
                order = float(torch.abs(z.mean()))
                
                # Creativity (diversity)
                diversity = float(torch.std(x))
                
                metrics_list.append({
                    'step': step,
                    'sync': order,
                    'diversity': diversity,
                    'product': order * diversity  # sync × diversity = creative output
                })
        
        final = metrics_list[-1]
        print(f"  K={K:.3f}: sync={final['sync']:.3f}, diversity={final['diversity']:.3f}, "
              f"creative_output={final['product']:.4f}")
        results.append({'K': K, 'metrics': metrics_list})
    
    # Find sweet spot
    best = max(results, key=lambda r: r['metrics'][-1]['product'])
    print(f"\n  🏆 Optimal coupling: K={best['K']:.3f}")
    return results

# ============================================================
# EXPERIMENT 3: Stochastic resonance on GPU
# ============================================================

def experiment_stochastic_resonance_gpu():
    """Bistable systems with noise sweep, 10000 parallel."""
    print("\n" + "="*60)
    print("EXPERIMENT 3: Stochastic Resonance (10,000 parallel)")
    print("="*60)
    
    N = 10000
    dt = 0.01
    T = 100
    
    # Different noise levels
    D_values = torch.logspace(-3, 1, N, device=device)
    signal_amp = 0.3
    signal_freq = 0.1
    
    x = torch.full((N,), -1.0, device=device)
    
    signal_power = torch.zeros(N, device=device)
    total_power = torch.zeros(N, device=device)
    transitions = torch.zeros(N, device=device, dtype=torch.long)
    
    prev_sign = torch.sign(x)
    
    for step in range(int(T / dt)):
        t = step * dt
        
        # Bistable force + signal + noise
        force = x - x**3 + signal_amp * torch.cos(torch.tensor(signal_freq * t, device=device))
        noise = torch.sqrt(2 * D_values * dt) * torch.randn(N, device=device)
        x += force * dt + noise
        
        # Track transitions
        curr_sign = torch.sign(x)
        transitions += (curr_sign != prev_sign).long()
        prev_sign = curr_sign
        
        # Accumulate for FFT (simplified: track signal frequency component)
        signal_component = torch.cos(torch.tensor(signal_freq * t, device=device))
        signal_power += (x * signal_component) ** 2
        total_power += x ** 2
    
    # SNR
    snr = signal_power / (total_power - signal_power + 1e-10)
    
    # Find optimal noise
    optimal_idx = torch.argmax(snr)
    optimal_D = float(D_values[optimal_idx])
    optimal_snr = float(snr[optimal_idx])
    optimal_transitions = int(transitions[optimal_idx])
    
    print(f"\n  Optimal noise intensity: D={optimal_D:.4f}")
    print(f"  SNR at optimum: {optimal_snr:.4f}")
    print(f"  Transitions at optimum: {optimal_transitions}")
    
    # Sample points
    print(f"\n  D → SNR sweep:")
    for i in range(0, N, N//20):
        print(f"    D={float(D_values[i]):.4f}: SNR={float(snr[i]):.4f}, transitions={int(transitions[i])}")
    
    return {'optimal_D': optimal_D, 'optimal_snr': optimal_snr}

# ============================================================
# EXPERIMENT 4: Genre interaction matrix (GPU)
# ============================================================

def experiment_genre_dynamics_gpu():
    """Simulate 100 genres as Lorenz oscillators with impedance coupling."""
    print("\n" + "="*60)
    print("EXPERIMENT 4: Genre Dynamics (100 genres on GPU)")
    print("="*60)
    
    N = 100
    genres = ['jazz', 'classical', 'blues', 'rock', 'hiphop', 'electronic', 
              'ambient', 'metal', 'folk', 'country']
    
    # Each genre gets Lorenz params based on impedance profile
    sigmas = torch.tensor([3.0, 8.0, 2.5, 5.0, 6.0, 7.0, 1.5, 9.0, 2.0, 4.0] * 10, device=device)
    rhos = torch.tensor([28.0, 15.0, 25.0, 30.0, 35.0, 40.0, 12.0, 45.0, 20.0, 22.0] * 10, device=device)
    betas = torch.tensor([2.5, 3.0, 2.0, 2.5, 2.0, 3.5, 1.5, 3.0, 2.0, 2.5] * 10, device=device)
    
    engine = LorenzCreativeEngine(N, device)
    engine.sigma = sigmas
    engine.rho = rhos
    engine.beta = betas
    
    # Warm up
    for _ in range(3000):
        engine.step()
    
    # Run with genre interaction
    interactions = torch.zeros(10, 10, device=device)  # interaction matrix
    
    for step in range(5000):
        state = engine.step()
        x = state[:, 0]
        
        # Compute pairwise correlations (genre interaction)
        if step % 500 == 0:
            for i in range(10):
                for j in range(10):
                    xi = x[i*N//10:(i+1)*N//10]
                    xj = x[j*N//10:(j+1)*N//10]
                    # Correlation as interaction strength
                    xi_centered = xi - xi.mean()
                    xj_centered = xj - xj.mean()
                    corr = (xi_centered * xj_centered).sum() / (xi_centered.norm() * xj_centered.norm() + 1e-10)
                    interactions[i, j] += corr
    
    # Normalize
    interactions /= 10  # number of samples
    
    print("\n  Genre interaction matrix (correlation):")
    print(f"  {'':12s}", end="")
    for g in genres:
        print(f"  {g[:8]:>8s}", end="")
    print()
    
    for i, g1 in enumerate(genres):
        print(f"  {g1:12s}", end="")
        for j, g2 in enumerate(genres):
            val = float(interactions[i, j])
            print(f"  {val:8.3f}", end="")
        print()
    
    # Find strongest/weakest interactions
    for i in range(10):
        for j in range(i+1, 10):
            val = float(interactions[i, j])
            if val > 0.5:
                print(f"  🔗 Strong: {genres[i]} ↔ {genres[j]} ({val:.3f})")
    
    return {'interactions': interactions.cpu().tolist(), 'genres': genres}

# ============================================================
# EXPERIMENT 5: Evolution of creative systems
# ============================================================

def experiment_evolution():
    """Evolve Lorenz parameters over generations, selecting for creative output."""
    print("\n" + "="*60)
    print("EXPERIMENT 5: Creative Evolution (100 generations)")
    print("="*60)
    
    POP = 500
    N_GEN = 100
    engine = LorenzCreativeEngine(POP, device)
    
    # Initial random parameters
    sigma = torch.rand(POP, device=device) * 20 + 1
    rho = torch.rand(POP, device=device) * 50 + 1
    beta = torch.rand(POP, device=device) * 5 + 0.5
    
    history = []
    
    for gen in range(N_GEN):
        engine.sigma = sigma
        engine.rho = rho
        engine.beta = beta
        engine.state = torch.randn(POP, 3, device=device) * 0.1
        
        # Evaluate fitness: diversity × energy (creative output)
        for _ in range(1000):
            state = engine.step()
        
        x = state[:, 0]
        diversity = float(torch.std(x))
        energy = float(torch.mean(x**2))
        fitness = diversity * energy
        
        history.append({
            'gen': gen,
            'sigma_mean': float(sigma.mean()),
            'rho_mean': float(rho.mean()),
            'beta_mean': float(beta.mean()),
            'diversity': diversity,
            'energy': energy,
            'fitness': fitness
        })
        
        if gen % 20 == 0:
            print(f"  Gen {gen:3d}: σ={float(sigma.mean()):.2f}, ρ={float(rho.mean()):.2f}, "
                  f"β={float(beta.mean()):.2f}, fitness={fitness:.4f}")
        
        # Selection: keep top 50%
        fitness_scores = torch.abs(x)
        top_indices = torch.argsort(fitness_scores, descending=True)[:POP//2]
        
        # Breed: mutate top performers
        new_sigma = sigma[top_indices].clone()
        new_rho = rho[top_indices].clone()
        new_beta = beta[top_indices].clone()
        
        # Mutation
        new_sigma += torch.randn(POP//2, device=device) * 0.5
        new_rho += torch.randn(POP//2, device=device) * 2.0
        new_beta += torch.randn(POP//2, device=device) * 0.2
        
        # Crossover: shuffle and average pairs
        perm = torch.randperm(POP//2, device=device)
        new_sigma = (new_sigma + new_sigma[perm]) / 2
        new_rho = (new_rho + new_rho[perm]) / 2
        new_beta = (new_beta + new_beta[perm]) / 2
        
        # Duplicate to fill population
        sigma = new_sigma.repeat(2)[:POP]
        rho = new_rho.repeat(2)[:POP]
        beta = new_beta.repeat(2)[:POP]
    
    print(f"\n  Final: σ={float(sigma.mean()):.2f}, ρ={float(rho.mean()):.2f}, "
          f"β={float(beta.mean()):.2f}")
    print(f"  Fitness: {history[0]['fitness']:.4f} → {history[-1]['fitness']:.4f}")
    
    return history

# ============================================================
# EXPERIMENT 6: Iterative insight extraction
# ============================================================

def experiment_insight_wheel(iterations=50):
    """The wheel: run experiments, extract insights, design next experiment."""
    print("\n" + "="*60)
    print(f"EXPERIMENT 6: Insight Wheel ({iterations} iterations)")
    print("="*60)
    
    insights = []
    
    for iteration in range(iterations):
        # Each iteration: slightly different parameters
        N = 1000
        engine = LorenzCreativeEngine(N, device)
        
        # Vary parameters based on iteration
        engine.sigma = torch.full((N,), 10.0 + iteration * 0.5, device=device)
        engine.rho = torch.full((N,), 20.0 + iteration * 0.3, device=device)
        engine.beta = torch.full((N,), 8/3, device=device)
        
        # Add noise (stochastic resonance)
        noise_level = 0.01 * (iteration + 1)
        
        # Run
        for _ in range(3000):
            state = engine.step()
            if noise_level > 0:
                engine.state += torch.randn(N, 3, device=device) * noise_level * 0.01
        
        # Extract insight
        x = engine.state[:, 0]
        diversity = float(torch.std(x))
        energy = float(torch.mean(x**2))
        max_amplitude = float(torch.max(torch.abs(x)))
        
        # Lyapunov estimate: divergence of nearby trajectories
        perturbed = engine.state + torch.randn(N, 3, device=device) * 0.001
        engine2 = LorenzCreativeEngine(N, device)
        engine2.sigma = engine.sigma
        engine2.rho = engine.rho
        engine2.beta = engine.beta
        engine2.state = perturbed
        
        for _ in range(100):
            engine.step()
            engine2.step()
        
        divergence = float(torch.mean(torch.norm(engine.state - engine2.state, dim=1)))
        lyapunov_est = np.log(divergence + 1e-10) / (100 * 0.01)
        
        insight = {
            'iteration': iteration,
            'sigma': float(engine.sigma[0]),
            'rho': float(engine.rho[0]),
            'noise': noise_level,
            'diversity': diversity,
            'energy': energy,
            'max_amp': max_amplitude,
            'lyapunov_est': lyapunov_est,
        }
        insights.append(insight)
        
        if iteration % 10 == 0:
            print(f"  [{iteration:3d}/{iterations}] σ={insight['sigma']:.1f}, ρ={insight['rho']:.1f}, "
                  f"noise={insight['noise']:.3f}, div={diversity:.3f}, λ≈{lyapunov_est:.3f}")
    
    # Extract meta-insights
    print(f"\n  📊 META-INSIGHTS from {iterations} iterations:")
    
    # Correlation: noise vs diversity
    noises = [i['noise'] for i in insights]
    diversities = [i['diversity'] for i in insights]
    energies = [i['energy'] for i in insights]
    
    if len(noises) > 2:
        noise_div_corr = np.corrcoef(noises, diversities)[0, 1]
        div_energy_corr = np.corrcoef(diversities, energies)[0, 1]
        print(f"    noise ↔ diversity correlation: {noise_div_corr:.4f}")
        print(f"    diversity ↔ energy correlation: {div_energy_corr:.4f}")
    
    # Peak diversity
    peak = max(insights, key=lambda i: i['diversity'])
    print(f"    Peak diversity at iteration {peak['iteration']}: σ={peak['sigma']:.1f}, ρ={peak['rho']:.1f}, noise={peak['noise']:.3f}")
    
    # Phase transition detection
    for i in range(1, len(insights)):
        delta = abs(insights[i]['diversity'] - insights[i-1]['diversity'])
        if delta > 2.0:
            print(f"    ⚡ Phase transition at iteration {i}: diversity jumped {delta:.2f}")
    
    return insights

# ============================================================
# MAIN: Run everything
# ============================================================

if __name__ == "__main__":
    start = time.time()
    
    all_results = {}
    
    # Run all experiments
    all_results['rho_sweep'] = experiment_rho_sweep()
    all_results['coupled'] = experiment_coupled_creativity()
    all_results['stochastic_resonance'] = experiment_stochastic_resonance_gpu()
    all_results['genre_dynamics'] = experiment_genre_dynamics_gpu()
    all_results['evolution'] = experiment_evolution()
    all_results['insight_wheel'] = experiment_insight_wheel(50)
    
    elapsed = time.time() - start
    
    # Save all results
    # (convert tensors to floats for JSON)
    def serialize(obj):
        if isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, torch.Tensor):
            return obj.cpu().tolist()
        raise TypeError(f"Not serializable: {type(obj)}")
    
    with open(RESULTS_DIR / "all_results.json", 'w') as f:
        json.dump(all_results, f, indent=2, default=serialize)
    
    print(f"\n{'='*60}")
    print(f"🔥 INSIGHT WHEEL COMPLETE")
    print(f"   Time: {elapsed:.1f}s")
    print(f"   Device: {device}")
    print(f"   Results: {RESULTS_DIR / 'all_results.json'}")
    print(f"{'='*60}")
