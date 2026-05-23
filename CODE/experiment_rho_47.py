import numpy as np
import json

print("=== Experiment 30: ρ=47 vs ρ=28 — The Meta-Wheel Discovery ===\n")

N = 500
dt = 0.01
T = 10000

def run_lorenz(N, sigma, rho, beta, T, noise=0.0):
    state = np.random.randn(N, 3) * 0.1
    outputs = []
    
    for step in range(T):
        x, y, z = state[:, 0], state[:, 1], state[:, 2]
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
        n = np.random.randn(N, 3) * noise
        state += (np.column_stack([dx, dy, dz]) * dt) + n * np.sqrt(dt)
        
        if step > T // 2:
            outputs.append(state.copy())
    
    return state, outputs

# Part 1: Head-to-head comparison
print("--- Part 1: ρ=28 vs ρ=47 Head-to-Head ---")

configs = [
    ('Classic Lorenz (ρ=28, σ=10)', 10.0, 28.0, 8/3),
    ('Meta-wheel optimum (ρ=47, σ=7)', 7.0, 47.0, 8/3),
    ('High chaos (ρ=60, σ=10)', 10.0, 60.0, 8/3),
    ('Low chaos (ρ=15, σ=10)', 10.0, 15.0, 8/3),
    ('Wheel σ only (ρ=28, σ=7)', 7.0, 28.0, 8/3),
    ('Wheel ρ only (ρ=47, σ=10)', 10.0, 47.0, 8/3),
]

for name, sigma, rho, beta in configs:
    final, outputs = run_lorenz(N, sigma, rho, beta, T)
    
    x_all = [o[:, 0] for o in outputs]
    x_flat = np.concatenate(x_all)
    
    diversity = float(np.std(x_flat))
    
    # Lyapunov estimate (perturbation divergence)
    state2, _ = run_lorenz(N, sigma, rho, beta, T)
    state1_final = final
    
    state2_start = np.random.randn(N, 3) * 0.1
    state2_p = state2_start + np.random.randn(N, 3) * 0.001
    
    for _ in range(100):
        x1, y1, z1 = state2_start[:, 0], state2_start[:, 1], state2_start[:, 2]
        dx = sigma * (y1 - x1)
        dy = x1 * (rho - z1) - y1
        dz = x1 * y1 - beta * z1
        state2_start += np.column_stack([dx, dy, dz]) * dt
        
        x2, y2, z2 = state2_p[:, 0], state2_p[:, 1], state2_p[:, 2]
        dx = sigma * (y2 - x2)
        dy = x2 * (rho - z2) - y2
        dz = x2 * y2 - beta * z2
        state2_p += np.column_stack([dx, dy, dz]) * dt
    
    div = float(np.mean(np.linalg.norm(state2_start - state2_p, axis=1)))
    
    # Spectral analysis
    fft = np.abs(np.fft.rfft(x_flat[:1000]))
    spectral_centroid = float(np.mean(np.arange(len(fft)) * fft) / (np.sum(fft) + 1e-10))
    
    print(f"  {name:35s}: div={diversity:.4f}, perturb_div={div:.4f}, "
          f"spectral_centroid={spectral_centroid:.2f}")

# Part 2: Full ρ-σ grid search
print("\n--- Part 2: ρ-σ Grid Search ---")

rho_range = np.arange(20, 55, 5)
sigma_range = np.arange(5, 15, 2)

best_config = None
best_score = 0
grid_results = []

for rho in rho_range:
    for sigma in sigma_range:
        final, outputs = run_lorenz(100, sigma, rho, 8/3, 5000)
        x_flat = np.concatenate([o[:, 0] for o in outputs])
        diversity = float(np.std(x_flat))
        
        # Quality proxy: diversity × spectral richness
        fft = np.abs(np.fft.rfft(x_flat[:500]))
        n_peaks = int(np.sum(fft > np.mean(fft) + 2 * np.std(fft)))
        score = diversity * (1 + 0.1 * n_peaks)
        
        grid_results.append({
            'rho': int(rho), 'sigma': int(sigma),
            'diversity': diversity, 'n_spectral_peaks': n_peaks,
            'score': score
        })
        
        if score > best_score:
            best_score = score
            best_config = (rho, sigma)

print(f"  Best configuration: ρ={best_config[0]}, σ={best_config[1]}, score={best_score:.4f}")

# Part 3: Why ρ≈47? What's special about it?
print("\n--- Part 3: Why ρ≈47? ---")

# Check if ρ≈47 corresponds to any special dynamical property
for rho in [28, 35, 40, 45, 47, 50, 55]:
    final, outputs = run_lorenz(200, 7.0, rho, 8/3, 8000)
    x_flat = np.concatenate([o[:, 0] for o in outputs])
    
    # Statistics
    mean_x = float(np.mean(x_flat))
    std_x = float(np.std(x_flat))
    skew = float(np.mean(((x_flat - mean_x) / (std_x + 1e-10))**3))
    kurt = float(np.mean(((x_flat - mean_x) / (std_x + 1e-10))**4))
    
    print(f"  ρ={rho:3d}: mean={mean_x:7.2f}, std={std_x:.2f}, skew={skew:.3f}, kurt={kurt:.2f}")

# Part 4: The creative potential at ρ=47
print("\n--- Part 4: Creative Potential Comparison ---")

for rho in [28, 47]:
    state, outputs = run_lorenz(N, 7.0, rho, 8/3, T)
    x_flat = np.concatenate([o[:, 0] for o in outputs])
    
    # Coverage of state space
    n_bins = 50
    hist, _ = np.histogram(x_flat, bins=n_bins, density=True)
    coverage = float(np.sum(hist > 0)) / n_bins  # fraction of state space explored
    
    # Temporal structure
    ac1 = float(np.corrcoef(x_flat[:-1], x_flat[1:])[0, 1])
    ac10 = float(np.corrcoef(x_flat[:-10], x_flat[10:])[0, 1])
    ac100 = float(np.corrcoef(x_flat[:-100], x_flat[100:])[0, 1])
    
    print(f"  ρ={rho}: coverage={coverage:.3f}, AC(1)={ac1:.3f}, AC(10)={ac10:.3f}, AC(100)={ac100:.3f}")

with open('CODE/EXPERIMENT-RHO-47.json', 'w') as f:
    json.dump({
        'grid_search': grid_results,
        'best_config': {'rho': int(best_config[0]), 'sigma': int(best_config[1]), 'score': best_score},
    }, f, indent=2)

print("\n=== ρ≈47 INVESTIGATION COMPLETE ===")
