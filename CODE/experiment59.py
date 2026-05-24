import numpy as np
import json

print("=== Experiment 59: The 10,000 System Sweep ===")
print("Full parameter space exploration\n")

np.random.seed(42)

N_SYSTEMS = 10000
DT = 0.01
N_STEPS = 3000
RECORD_FROM = 1000

# Parameter grid: ρ ∈ [1, 100], σ ∈ [2, 20]
rho_grid = np.random.uniform(1, 100, N_SYSTEMS)
sigma_grid = np.random.uniform(2, 20, N_SYSTEMS)
beta = np.full(N_SYSTEMS, 8.0/3.0)

# Initial states
states = np.random.uniform(-1, 1, (N_SYSTEMS, 3))

print(f"  Running {N_SYSTEMS} systems for {N_STEPS} steps...")

# Vectorized RK4
def lorenz_deriv(s, rho, sigma, beta):
    x, y, z = s[:, 0], s[:, 1], s[:, 2]
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return np.stack([dx, dy, dz], axis=1)

outputs = np.zeros((N_STEPS - RECORD_FROM, N_SYSTEMS))

for step in range(N_STEPS):
    k1 = lorenz_deriv(states, rho_grid, sigma_grid, beta)
    k2 = lorenz_deriv(states + 0.5*DT*k1, rho_grid, sigma_grid, beta)
    k3 = lorenz_deriv(states + 0.5*DT*k2, rho_grid, sigma_grid, beta)
    k4 = lorenz_deriv(states + DT*k3, rho_grid, sigma_grid, beta)
    states = states + (DT/6) * (k1 + 2*k2 + 2*k3 + k4)
    states = np.clip(states, -500, 500)
    
    if step >= RECORD_FROM:
        outputs[step - RECORD_FROM] = states[:, 0]

print(f"  Done. Shape: {outputs.shape}")

# Analysis
print(f"\n--- Per-System Analysis ---")

stds = np.std(outputs, axis=0)
means = np.mean(outputs, axis=0)
ranges = np.ptp(outputs, axis=0)

# Autocorrelation (vectorized)
acf1 = np.array([np.corrcoef(outputs[:-1, i], outputs[1:, i])[0, 1] for i in range(N_SYSTEMS)])

# Spectral flatness (vectorized approximation)
flatness = np.zeros(N_SYSTEMS)
for i in range(N_SYSTEMS):
    fft = np.fft.rfft(outputs[:, i] - means[i])
    power = np.abs(fft[1:])**2
    if np.mean(power) > 0:
        flatness[i] = np.exp(np.mean(np.log(power + 1e-10))) / np.mean(power)

# Classify regimes
regime = np.full(N_SYSTEMS, 'unknown', dtype='U20')
regime[stds < 0.5] = 'Crystal'
regime[(stds >= 0.5) & (stds < 3) & (acf1 > 0.9)] = 'Pendulum'
regime[(stds >= 3) & (acf1 > 0.95)] = 'Chimera'
regime[(stds >= 3) & (acf1 <= 0.95)] = 'Butterfly'
regime[(stds > 50)] = 'Explosion'

regime_counts = dict(zip(*np.unique(regime, return_counts=True)))
print(f"  Regime census:")
for r, c in sorted(regime_counts.items(), key=lambda x: -x[1]):
    print(f"    {r:12s}: {c:5d} ({c/N_SYSTEMS*100:.1f}%)")

# Part 2: Quality landscape (normalized!)
print(f"\n--- Quality Landscape (Variance-Normalized) ---")

# Shape quality: entropy × spectral_flatness / std
entropy = np.zeros(N_SYSTEMS)
for i in range(N_SYSTEMS):
    hist, _ = np.histogram(outputs[:, i], bins=30, density=True)
    hist = hist / hist.sum()
    entropy[i] = -np.sum(hist * np.log(hist + 1e-10))

shape_quality = entropy * flatness / (stds + 0.01)

# Find the top 10 by shape quality
top10 = np.argsort(shape_quality)[-10:][::-1]

print(f"  Top 10 by shape quality:")
for rank, idx in enumerate(top10):
    print(f"    #{rank+1}: ρ={rho_grid[idx]:.1f}, σ={sigma_grid[idx]:.1f}, "
          f"shape_q={shape_quality[idx]:.4f}, std={stds[idx]:.2f}, "
          f"regime={regime[idx]}, flat={flatness[idx]:.4f}")

# Part 3: Phase transition boundary
print(f"\n--- Phase Transition Boundary ---")
# Find where Crystal → non-Crystal
crystal_mask = regime == 'Crystal'
if crystal_mask.any() and (~crystal_mask).any():
    crystal_rho_max = rho_grid[crystal_mask].max()
    noncrystal_rho_min = rho_grid[~crystal_mask].min()
    print(f"  Crystal → alive transition: ρ ∈ [{noncrystal_rho_min:.1f}, {crystal_rho_max:.1f}]")

# Find where Chimera → Butterfly
chimera_mask = regime == 'Chimera'
butterfly_mask = regime == 'Butterfly'
if chimera_mask.any() and butterfly_mask.any():
    print(f"  Chimera ρ range: [{rho_grid[chimera_mask].min():.1f}, {rho_grid[chimera_mask].max():.1f}]")
    print(f"  Butterfly ρ range: [{rho_grid[butterfly_mask].min():.1f}, {rho_grid[butterfly_mask].max():.1f}]")

# Part 4: Best σ for each ρ band
print(f"\n--- Best σ per ρ Band ---")
for rho_lo, rho_hi in [(1,10), (10,20), (20,30), (30,45), (45,60), (60,100)]:
    mask = (rho_grid >= rho_lo) & (rho_grid < rho_hi)
    if mask.any():
        best_local = np.argmax(shape_quality * mask)
        if shape_quality[best_local] > 0:
            print(f"  ρ∈[{rho_lo},{rho_hi}): best σ={sigma_grid[best_local]:.1f}, "
                  f"shape_q={shape_quality[best_local]:.4f}")

# Part 5: σ effect on creativity
print(f"\n--- σ Effect at Fixed ρ≈28 ---")
rho28_mask = (rho_grid >= 25) & (rho_grid <= 31)
if rho28_mask.any():
    sigma_vals = sigma_grid[rho28_mask]
    shape_vals = shape_quality[rho28_mask]
    corr = np.corrcoef(sigma_vals, shape_vals)[0, 1]
    print(f"  σ ↔ shape_quality correlation at ρ≈28: {corr:.3f}")
    best_sigma_idx = np.argmax(shape_vals)
    print(f"  Best σ at ρ≈28: {sigma_vals[best_sigma_idx]:.1f} (shape_q={shape_vals[best_sigma_idx]:.4f})")

# Save
import subprocess
with open('/tmp/fm-research/CODE/EXPERIMENT-10K-SWEEP.json', 'w') as f:
    json.dump({
        'n_systems': N_SYSTEMS,
        'regime_counts': {k: int(v) for k, v in regime_counts.items()},
        'top10': [{'rho': float(rho_grid[i]), 'sigma': float(sigma_grid[i]),
                    'shape_q': float(shape_quality[i]), 'std': float(stds[i]),
                    'regime': str(regime[i])} for i in top10],
    }, f, indent=2)

subprocess.run(['git', 'add', '-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'commit', '-m', 'experiment 59: 10K system sweep'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'push'], cwd='/tmp/fm-research', capture_output=True)

print("\n=== 10,000 SYSTEMS MAPPED ===")
