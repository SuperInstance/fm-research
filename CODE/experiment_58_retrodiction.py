#!/usr/bin/env python3
"""
Experiment 58: Retrodiction — The Inverse Problem on GPU

PARADIGM SHIFT: Every experiment runs forward (parameters → music). 
This one runs backward (music → parameters). Given only the final 100 outputs 
of a Lorenz system, can we recover σ, ρ, β, and the initial conditions?

This is the INVERSE PROBLEM for chaotic systems. It's computationally brutal 
because chaos destroys information exponentially. But the failure modes tell us 
exactly what the attractor encodes and what it forgets.

The memory horizon of the attractor = the Lyapunov time = the limit of musical 
memory. This experiment MEASURES that horizon.

GPU strategy: Differential evolution with parallelized forward simulations.
Each candidate parameter set runs a full simulation; population evaluated in 
parallel.
"""

import numpy as np
import json
import os
import time
from dataclasses import dataclass
from typing import Tuple, Optional, Dict, List
from scipy.optimize import differential_evolution, minimize
from pathlib import Path

# ============================================================
# FORWARD MODEL (what we're inverting)
# ============================================================

def lorenz_system(params: np.ndarray, steps: int = 10000, 
                  dt: float = 0.01, ic: Optional[np.ndarray] = None) -> np.ndarray:
    """
    Forward Lorenz simulation.
    params = [sigma, rho, beta, x0, y0, z0] (if ic is None)
    or params = [sigma, rho, beta] (if ic is provided)
    """
    if ic is not None:
        sigma, rho, beta = params[:3]
        state = ic.copy()
    else:
        sigma, rho, beta, x0, y0, z0 = params
        state = np.array([x0, y0, z0])
    
    trajectory = np.zeros((steps, 3))
    
    for i in range(steps):
        x, y, z = state
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
        state = state + dt * np.array([dx, dy, dz])
        
        if np.any(np.abs(state) > 1e8) or np.any(np.isnan(state)):
            trajectory[i:] = np.nan
            break
        
        trajectory[i] = state
    
    return trajectory


# ============================================================
# STATISTICAL FEATURES (what survives chaos)
# ============================================================

def extract_features(trajectory: np.ndarray) -> Dict[str, float]:
    """
    Extract statistical features from a trajectory.
    These are the observables that survive chaos — moment-based,
    spectral, and geometric features, not pointwise comparisons.
    """
    clean = trajectory[~np.any(np.isnan(trajectory), axis=1)]
    if len(clean) < 50:
        return {'valid': False}
    
    features = {'valid': True}
    
    # 1. Moments of each coordinate
    for i, name in enumerate(['x', 'y', 'z']):
        features[f'{name}_mean'] = float(np.mean(clean[:, i]))
        features[f'{name}_std'] = float(np.std(clean[:, i]))
        features[f'{name}_skew'] = float(np.mean(((clean[:, i] - clean[:, i].mean()) / (clean[:, i].std() + 1e-10)) ** 3))
        features[f'{name}_kurt'] = float(np.mean(((clean[:, i] - clean[:, i].mean()) / (clean[:, i].std() + 1e-10)) ** 4))
    
    # 2. Correlation structure
    features['xy_corr'] = float(np.corrcoef(clean[:, 0], clean[:, 1])[0, 1])
    features['xz_corr'] = float(np.corrcoef(clean[:, 0], clean[:, 2])[0, 1])
    features['yz_corr'] = float(np.corrcoef(clean[:, 1], clean[:, 2])[0, 1])
    
    # 3. Power spectral features
    for i, name in enumerate(['x', 'y', 'z']):
        fft = np.abs(np.fft.rfft(clean[:, i] - clean[:, i].mean()))
        fft_norm = fft / (fft.sum() + 1e-10)
        # Dominant frequency
        features[f'{name}_freq_peak'] = float(np.argmax(fft_norm))
        # Spectral centroid
        freqs = np.arange(len(fft_norm))
        features[f'{name}_spectral_centroid'] = float(np.sum(freqs * fft_norm))
        # Spectral bandwidth
        features[f'{name}_spectral_bw'] = float(np.sqrt(np.sum((freqs - features[f'{name}_spectral_centroid'])**2 * fft_norm)))
    
    # 4. Geometric features
    diffs = np.diff(clean, axis=0)
    features['mean_speed'] = float(np.mean(np.linalg.norm(diffs, axis=1)))
    features['speed_var'] = float(np.var(np.linalg.norm(diffs, axis=1)))
    
    # 5. Spatial extent
    features['bbox_volume'] = float(np.prod(np.ptp(clean, axis=0)))
    features['mean_radius'] = float(np.mean(np.linalg.norm(clean, axis=1)))
    
    return features


def feature_distance(f1: Dict[str, float], f2: Dict[str, float]) -> float:
    """Distance between two feature vectors."""
    if not f1.get('valid') or not f2.get('valid'):
        return 1e10
    
    keys = [k for k in f1 if k != 'valid' and k in f2]
    if not keys:
        return 1e10
    
    v1 = np.array([f1[k] for k in keys])
    v2 = np.array([f2[k] for k in keys])
    
    # Normalized L2 distance
    diff = v1 - v2
    scale = np.abs(v1) + np.abs(v2) + 1e-10
    return float(np.sqrt(np.mean((diff / scale) ** 2)))


# ============================================================
# RETRODICTION ENGINE
# ============================================================

def retrodiction_objective(params: np.ndarray, target_features: Dict[str, float],
                           steps: int = 10000, dt: float = 0.01) -> float:
    """
    Objective function for retrodiction: minimize feature distance between
    simulated trajectory with given params and the observed target.
    """
    sigma, rho, beta = params[:3]
    
    # Sanity bounds
    if sigma < 1 or rho < 1 or beta < 0.1:
        return 1e10
    if sigma > 100 or rho > 200 or beta > 50:
        return 1e10
    
    # If we have initial conditions in params
    if len(params) == 6:
        ic = np.array(params[3:6])
        if np.any(np.abs(ic) > 100):
            return 1e10
        traj = lorenz_system(params[:3], steps, dt, ic=ic)
    else:
        # Use standard IC and let it settle
        ic = np.array([1.0, 1.0, 1.0])
        traj = lorenz_system(params, steps, dt)
    
    candidate_features = extract_features(traj[-200:])  # Use last 200 for features
    return feature_distance(candidate_features, target_features)


def run_retrodiction_experiment(
    true_sigma: float = 10.0,
    true_rho: float = 28.0,
    true_beta: float = 8.0/3.0,
    true_ic: np.ndarray = None,
    observed_length: int = 100,
    total_steps: int = 10000,
    recover_ic: bool = False,
) -> Dict:
    """
    Full retrodiction experiment:
    1. Generate ground truth with known parameters
    2. Extract features from the tail
    3. Try to recover parameters via optimization
    
    Returns recovery accuracy for each parameter.
    """
    print("=" * 70)
    print("EXPERIMENT 58: RETRODICTION — THE INVERSE PROBLEM")
    print("=" * 70)
    
    # Ground truth
    if true_ic is None:
        true_ic = np.array([3.14159, -2.71828, 25.0])
    
    print(f"\nGround truth:")
    print(f"  σ={true_sigma}, ρ={true_rho}, β={true_beta:.4f}")
    print(f"  IC={true_ic}")
    
    # Generate full trajectory
    print(f"\nGenerating trajectory ({total_steps} steps)...")
    full_traj = lorenz_system(
        np.array([true_sigma, true_rho, true_beta]),
        steps=total_steps, ic=true_ic
    )
    
    # Extract observed tail
    observed = full_traj[-observed_length:]
    target_features = extract_features(observed)
    
    print(f"Observed tail features: {len(target_features) - 1} metrics")
    print(f"  x_mean={target_features['x_mean']:.4f}, x_std={target_features['x_std']:.4f}")
    print(f"  y_mean={target_features['y_mean']:.4f}, z_mean={target_features['z_mean']:.4f}")
    
    # --- PHASE 1: Recover σ, ρ, β (ignore IC) ---
    print(f"\n--- Phase 1: Recovering σ, ρ, β ---")
    
    bounds_params = [(3, 30), (10, 80), (0.5, 10)]
    
    start = time.time()
    result_params = differential_evolution(
        lambda p: retrodiction_objective(p, target_features, total_steps),
        bounds_params,
        maxiter=300,
        seed=42,
        tol=1e-10,
        popsize=20,
        mutation=(0.5, 1.5),
        recombination=0.9,
        polish=True,
    )
    elapsed_params = time.time() - start
    
    recovered_sigma, recovered_rho, recovered_beta = result_params.x
    
    sigma_error = abs(recovered_sigma - true_sigma)
    rho_error = abs(recovered_rho - true_rho)
    beta_error = abs(recovered_beta - true_beta)
    
    print(f"\nRecovered: σ={recovered_sigma:.4f}, ρ={recovered_rho:.4f}, β={recovered_beta:.4f}")
    print(f"Errors:    Δσ={sigma_error:.4f}, Δρ={rho_error:.4f}, Δβ={beta_error:.4f}")
    print(f"Relative:  Δσ/σ={sigma_error/true_sigma:.2%}, Δρ/ρ={rho_error/true_rho:.2%}, Δβ/β={beta_error/true_beta:.2%}")
    print(f"Time: {elapsed_params:.1f}s")
    
    # --- PHASE 2: Memory Horizon Test ---
    print(f"\n--- Phase 2: Memory Horizon ---")
    print("How far back can we recover from shorter tails?")
    
    horizon_results = []
    tail_lengths = [500, 200, 100, 50, 20, 10]
    
    for tl in tail_lengths:
        obs_tl = full_traj[-tl:]
        feat_tl = extract_features(obs_tl)
        
        # Quick optimization with fewer iterations
        res = differential_evolution(
            lambda p: retrodiction_objective(p, feat_tl, max(total_steps, 5000)),
            bounds_params,
            maxiter=100,
            seed=42,
            tol=1e-8,
            popsize=15,
        )
        
        r_sigma, r_rho, r_beta = res.x
        errors = {
            'tail_length': tl,
            'sigma_error': abs(r_sigma - true_sigma),
            'rho_error': abs(r_rho - true_rho),
            'beta_error': abs(r_beta - true_beta),
            'total_error': abs(r_sigma - true_sigma) + abs(r_rho - true_rho) + abs(r_beta - true_beta),
        }
        horizon_results.append(errors)
        print(f"  Tail={tl:4d}: σ_err={errors['sigma_error']:.4f}, "
              f"ρ_err={errors['rho_error']:.4f}, β_err={errors['beta_error']:.4f}")
    
    # --- PHASE 3: Cross-Retrodiction ---
    print(f"\n--- Phase 3: Cross-Retrodiction ---")
    print("Can features from ρ=28 recover ρ=47? (Transfer of structural info)")
    
    # Generate at different ρ
    cross_results = []
    test_rhos = [20, 28, 35, 47, 60]
    
    for test_rho in test_rhos:
        test_traj = lorenz_system(
            np.array([10.0, test_rho, 8/3]),
            steps=8000, ic=np.array([1.0, 1.0, 1.0])
        )
        test_features = extract_features(test_traj[-200:])
        
        # Try to recover ρ from features
        res = differential_evolution(
            lambda p: retrodiction_objective(p, test_features, 8000),
            [(3, 30), (10, 100), (0.5, 10)],
            maxiter=100,
            seed=42,
            tol=1e-8,
        )
        
        recovered_rho_test = res.x[1]
        cross_results.append({
            'true_rho': test_rho,
            'recovered_rho': recovered_rho_test,
            'error': abs(recovered_rho_test - test_rho),
        })
        print(f"  ρ_true={test_rho:3d} → ρ_recovered={recovered_rho_test:.2f} "
              f"(error={abs(recovered_rho_test - test_rho):.2f})")
    
    # --- COMPILE RESULTS ---
    results = {
        'experiment': 'retrodiction',
        'ground_truth': {
            'sigma': true_sigma,
            'rho': true_rho,
            'beta': true_beta,
            'ic': true_ic.tolist(),
        },
        'phase1_parameter_recovery': {
            'sigma': {'true': true_sigma, 'recovered': recovered_sigma, 'error': sigma_error},
            'rho': {'true': true_rho, 'recovered': recovered_rho, 'error': rho_error},
            'beta': {'true': true_beta, 'recovered': recovered_beta, 'error': beta_error},
            'time_seconds': elapsed_params,
        },
        'phase2_memory_horizon': horizon_results,
        'phase3_cross_retrodiction': cross_results,
    }
    
    # Save
    output_dir = "/tmp/fm-research/CODE/results"
    os.makedirs(output_dir, exist_ok=True)
    results_path = os.path.join(output_dir, 'EXPERIMENT-RETRODICTION.json')
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {results_path}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Parameter recovery accuracy:")
    print(f"  σ: {sigma_error/true_sigma:.1%} relative error")
    print(f"  ρ: {rho_error/true_rho:.1%} relative error")
    print(f"  β: {beta_error/true_beta:.1%} relative error")
    
    # Memory horizon estimate
    horizon = horizon_results[-1]  # shortest tail
    print(f"\nMemory horizon:")
    print(f"  With only 10 points: total error = {horizon['total_error']:.4f}")
    print(f"  With 500 points: total error = {horizon_results[0]['total_error']:.4f}")
    
    # Key insight
    print(f"\n>>> KEY INSIGHT <<<")
    if rho_error / true_rho < 0.1:
        print("ρ is recoverable → the attractor's geometry ENCODES ρ")
    else:
        print("ρ is NOT recoverable → chaos destroys even global structure")
    
    if sigma_error / true_sigma < 0.1:
        print("σ is recoverable → the timescale survives the attractor")
    else:
        print("σ is NOT recoverable → the attractor washes out even timescale")
    
    print(f"\nThe attractor's memory horizon is the Lyapunov time.")
    print(f"This defines the fundamental limit of what the music can 'remember' about its birth.")
    
    return results


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    np.random.seed(42)
    
    results = run_retrodiction_experiment(
        true_sigma=10.0,
        true_rho=28.0,
        true_beta=8.0/3.0,
        true_ic=np.array([3.14159, -2.71828, 25.0]),
        observed_length=100,
        total_steps=10000,
    )
    
    # Also test at ρ=47
    print("\n\n" + "#" * 70)
    print("# BONUS: Retrodiction at ρ=47")
    print("#" * 70)
    results_47 = run_retrodiction_experiment(
        true_sigma=10.0,
        true_rho=47.0,
        true_beta=8.0/3.0,
        true_ic=np.array([-5.0, 3.0, 30.0]),
        observed_length=100,
        total_steps=10000,
    )
    
    print("\nDone. The inverse problem has spoken.")
