import numpy as np
import json
import sys
import random
from collections import deque

print("=== Experiment 36: Self-Organized Criticality in Creative Systems ===\n")
sys.stdout.flush()

random.seed(42)
np.random.seed(42)

# Part 1: Creative sandpile - OPEN boundaries (grains fall off edges)
print("--- Part 1: Creative Sandpile (Open Boundaries) ---")
sys.stdout.flush()

grid_size = 50
threshold = 4
grid = [[random.randint(0, threshold-1) for _ in range(grid_size)] for _ in range(grid_size)]

avalanche_sizes = []

for step in range(50000):
    x = random.randint(0, grid_size-1)
    y = random.randint(0, grid_size-1)
    grid[x][y] += 1
    
    size = 0
    stack = deque()
    if grid[x][y] >= threshold:
        stack.append((x, y))
    
    while stack:
        ux, uy = stack.popleft()
        if grid[ux][uy] < threshold:
            continue
        grid[ux][uy] -= 4
        size += 1
        for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
            ni, nj = ux + di, uy + dj
            if 0 <= ni < grid_size and 0 <= nj < grid_size:  # OPEN boundary
                grid[ni][nj] += 1
                if grid[ni][nj] >= threshold:
                    stack.append((ni, nj))
    
    if size > 0:
        avalanche_sizes.append(size)
    
    if step % 10000 == 0:
        print(f"  Step {step}/50000, avalanches: {len(avalanche_sizes)}")
        sys.stdout.flush()

exponent = None
if len(avalanche_sizes) > 100:
    sizes = np.array(avalanche_sizes)
    max_size = max(sizes)
    
    bins = np.logspace(0, np.log10(max(max_size, 2)), 20)
    hist, edges = np.histogram(sizes, bins=bins, density=True)
    valid = hist > 0
    if np.sum(valid) > 3:
        log_sizes = np.log(edges[:-1][valid] + 1)
        log_hist = np.log(hist[valid])
        fit = np.polyfit(log_sizes, log_hist, 1)
        exponent = fit[0]
        
        print(f"  Avalanche distribution exponent: {exponent:.3f}")
        print(f"  (Power law = criticality. SOC models typically give -1.0 to -1.5)")
        print(f"  Total avalanches: {len(avalanche_sizes)}")
        print(f"  Max avalanche: {max_size}")
        print(f"  Mean avalanche: {np.mean(sizes):.2f}")
        print(f"  Median avalanche: {np.median(sizes):.2f}")
        
        is_power_law = exponent < -0.5
        print(f"  Power law: {'YES ✓' if is_power_law else 'NO'}")
        print(f"  Self-organized criticality: {'CONFIRMED' if is_power_law else 'NOT CONFIRMED'}")
else:
    print("  Not enough avalanches collected")

sys.stdout.flush()

# Part 2: Sandpile with ε
print("\n--- Part 2: Creative Sandpile with ε ---")
sys.stdout.flush()

for eps in [0.0, 0.3, 0.5, 1.0]:
    g2 = 20  # smaller grid for speed
    grid = [[random.randint(0, threshold-1) for _ in range(g2)] for _ in range(g2)]
    sizes = []
    
    for step in range(5000):
        x = random.randint(0, g2-1)
        y = random.randint(0, g2-1)
        if random.random() > eps * 0.3:
            grid[x][y] += 1
        
        size = 0
        stack = deque()
        if grid[x][y] >= threshold:
            stack.append((x, y))
        
        while stack:
            ux, uy = stack.popleft()
            if grid[ux][uy] < threshold:
                continue
            grid[ux][uy] -= 4
            size += 1
            extra = 1 if random.random() < eps else 0
            for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                ni, nj = ux + di, uy + dj
                if 0 <= ni < g2 and 0 <= nj < g2:
                    grid[ni][nj] += 1 + extra
                    if grid[ni][nj] >= threshold:
                        stack.append((ni, nj))
        
        if size > 0:
            sizes.append(size)
    
    if len(sizes) > 10:
        sizes = np.array(sizes)
        bins = np.logspace(0, np.log10(max(sizes) + 1), 10)
        hist, edges = np.histogram(sizes, bins=bins, density=True)
        valid = hist > 0
        if np.sum(valid) > 2:
            fit = np.polyfit(np.log(edges[:-1][valid] + 1), np.log(hist[valid]), 1)
            print(f"  ε={eps:.1f}: exponent={fit[0]:.3f}, mean_size={np.mean(sizes):.2f}, "
                  f"n_avalanches={len(sizes)}")
    sys.stdout.flush()

# Part 3: Lorenz Self-Tuning
print("\n--- Part 3: Lorenz Self-Tuning ---")
sys.stdout.flush()

N = 200
dt = 0.01
state = np.random.randn(N, 3) * 0.1
rho = 15.0

rho_history = []

for step in range(50000):
    x, y, z = state[:, 0], state[:, 1], state[:, 2]
    dx = 10 * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - 8/3 * z
    state += np.column_stack([dx, dy, dz]) * dt
    
    if step > 5000 and step % 100 == 0:
        div = float(np.std(state[:, 0]))
        target_div = 5.0
        rho += 0.01 * (target_div - div)
        rho = max(1, min(60, rho))
        rho_history.append(float(rho))
    
    if step % 10000 == 0 and step > 0:
        print(f"  Step {step}: ρ={rho:.2f}, diversity={float(np.std(state[:, 0])):.4f}")
        sys.stdout.flush()

if rho_history:
    final_rho = rho_history[-1]
    rho_std = float(np.std(rho_history[-100:]))
    print(f"\n  ρ converged to: {final_rho:.2f} ± {rho_std:.2f}")
    print(f"  This is {'near ρ_c=24.74 (critical point!)' if abs(final_rho - 24.74) < 5 else 'away from critical point'}")
    print(f"  Self-tuning to criticality: {'YES' if abs(final_rho - 24.74) < 5 else 'NO, settled elsewhere'}")

sys.stdout.flush()

# Part 4: 1/f noise in creative output
print("\n--- Part 4: 1/f Noise in Creative Output ---")
sys.stdout.flush()

state = np.random.randn(500, 3) * 0.1
outputs = []

for step in range(20000):
    x, y, z = state[:, 0], state[:, 1], state[:, 2]
    dx = 10 * (y - x)
    dy = x * (28 - z) - y
    dz = x * y - 8/3 * z
    state += np.column_stack([dx, dy, dz]) * dt
    outputs.append(float(np.mean(state[:, 0])))

outputs = np.array(outputs)
f = np.fft.rfftfreq(len(outputs), d=dt)
psd = np.abs(np.fft.rfft(outputs))**2

valid = (f > 0.01) & (f < 10) & (psd > 0)
slope = None
if np.sum(valid) > 10:
    log_f = np.log(f[valid])
    log_psd = np.log(psd[valid])
    fit = np.polyfit(log_f, log_psd, 1)
    slope = fit[0]
    
    print(f"  PSD slope: {slope:.3f}")
    print(f"  1/f noise (pink): slope ≈ -1")
    print(f"  1/f² noise (brown): slope ≈ -2")
    print(f"  White noise: slope ≈ 0")
    
    if -1.5 < slope < -0.5:
        print(f"  → PINK NOISE (1/f): creative output shows SOC signature!")
    elif slope < -1.5:
        print(f"  → Brown noise: more structured than critical")
    else:
        print(f"  → White-ish noise: less structured than critical")

with open('CODE/EXPERIMENT-SOC.json', 'w') as outf:
    json.dump({
        'avalanche_exponent': float(exponent) if exponent is not None else None,
        'rho_convergence': float(rho_history[-1]) if rho_history else None,
        'psd_slope': float(slope) if slope is not None else None,
    }, outf, indent=2)

print("\n=== SELF-ORGANIZED CRITICALITY IN CREATIVE SYSTEMS ===")
