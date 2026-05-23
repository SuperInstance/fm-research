import numpy as np
import json

print("=== Experiment 34: Regime × Quality Surface ===\n")
print("Full 2D map of quality(ρ, ε)\n")

np.random.seed(42)
N = 200
dt = 0.01

rho_range = np.linspace(1, 50, 25)
eps_range = np.linspace(0.01, 2.0, 25)

surface = []

for i, rho in enumerate(rho_range):
    for j, eps in enumerate(eps_range):
        state = np.random.randn(N, 3) * 0.1
        outputs = []
        
        for step in range(8000):
            x, y, z = state[:, 0], state[:, 1], state[:, 2]
            dx = 10 * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - 8/3 * z
            noise = np.random.randn(N, 3) * eps
            state += (np.column_stack([dx, dy, dz]) * dt) + noise * np.sqrt(dt)
            
            if step > 4000:
                outputs.append(float(np.mean(state[:, 0])))
        
        # Quality = novelty × coherence
        arr = np.array(outputs)
        novelty = float(np.std(arr))
        fft = np.abs(np.fft.rfft(arr))
        fft_norm = fft / (fft.sum() + 1e-10)
        flatness = np.exp(np.mean(np.log(fft_norm + 1e-10))) / (np.mean(fft_norm) + 1e-10)
        coherence = 1 - flatness
        quality = novelty * coherence
        
        diversity = novelty
        
        surface.append({
            'rho': float(rho),
            'eps': float(eps),
            'quality': quality,
            'diversity': diversity,
            'coherence': coherence,
        })

# Find the global optimum
best = max(surface, key=lambda s: s['quality'])
best_div = max(surface, key=lambda s: s['diversity'])
best_coh = max(surface, key=lambda s: s['coherence'])

print(f"  Best quality: ρ={best['rho']:.1f}, ε={best['eps']:.2f}, quality={best['quality']:.6f}")
print(f"  Best diversity: ρ={best_div['rho']:.1f}, ε={best_div['eps']:.2f}, diversity={best_div['diversity']:.4f}")
print(f"  Best coherence: ρ={best_coh['rho']:.1f}, ε={best_coh['eps']:.2f}, coherence={best_coh['coherence']:.4f}")

# Find optimal ε for each ρ
print(f"\n  Optimal ε by ρ:")
for rho in rho_range[::3]:
    rho_points = [s for s in surface if abs(s['rho'] - rho) < 1]
    best_at_rho = max(rho_points, key=lambda s: s['quality'])
    regime = "CHAOTIC" if rho > 24.74 else "PERIODIC"
    print(f"    ρ={rho:5.1f} [{regime:8s}]: ε*={best_at_rho['eps']:.2f}, quality={best_at_rho['quality']:.6f}")

# Find optimal ρ for each ε
print(f"\n  Optimal ρ by ε:")
for eps in eps_range[::3]:
    eps_points = [s for s in surface if abs(s['eps'] - eps) < 0.1]
    best_at_eps = max(eps_points, key=lambda s: s['quality'])
    print(f"    ε={eps:.2f}: ρ*={best_at_eps['rho']:.1f}, quality={best_at_eps['quality']:.6f}")

# The ridge line
print(f"\n  The CREATIVE RIDGE (optimal path through the surface):")
ridge = []
for rho in rho_range:
    rho_points = [s for s in surface if abs(s['rho'] - rho) < 1]
    best_at_rho = max(rho_points, key=lambda s: s['quality'])
    ridge.append(best_at_rho)

for r in ridge[::3]:
    regime = "CHAOTIC" if r['rho'] > 24.74 else "PERIODIC"
    print(f"    ρ={r['rho']:5.1f} [{regime:8s}]: ε*={r['eps']:.2f}")

# Does ε* change with ρ?
eps_stars = [r['eps'] for r in ridge]
rhos = [r['rho'] for r in ridge]
corr = np.corrcoef(rhos, eps_stars)[0, 1]
print(f"\n  ρ ↔ ε* correlation: {corr:.3f}")
if corr > 0.3:
    print(f"  ε* INCREASES with ρ (experts need MORE freedom??)")
elif corr < -0.3:
    print(f"  ε* DECREASES with ρ (experts need LESS freedom — matches regime theory!)")
else:
    print(f"  ε* is INDEPENDENT of ρ")

with open('CODE/EXPERIMENT-REGIME-QUALITY-SURFACE.json', 'w') as f:
    json.dump({
        'surface': surface,
        'best_quality': best,
        'ridge': ridge,
        'rho_eps_correlation': float(corr),
    }, f, indent=2)

print("\n=== REGIME × QUALITY SURFACE MAPPED ===")
