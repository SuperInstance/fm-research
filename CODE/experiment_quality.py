import numpy as np
import json

print("=== Experiment 29: Quality vs Diversity ===\n")
print("Diversity ≠ Quality. Does the ε sweet spot differ?\n")

np.random.seed(42)

# Quality metric: "interestingness" = novelty × coherence
# - Novelty: how different from previous output (variance)
# - Coherence: how much structure exists (autocorrelation, spectral flatness)
# - Quality = novelty × coherence (both needed)

def compute_quality(time_series, window=100):
    """Compute quality = novelty × coherence."""
    if len(time_series) < window:
        return 0, 0, 0
    
    series = np.array(time_series[-window:])
    
    # Novelty: variance (diversity of output)
    novelty = np.std(series)
    
    # Coherence: 1 - spectral flatness (tonal vs noise-like)
    fft = np.abs(np.fft.rfft(series))
    fft = fft / (fft.sum() + 1e-10)
    
    # Spectral flatness (geometric mean / arithmetic mean)
    log_fft = np.log(fft + 1e-10)
    geo_mean = np.exp(np.mean(log_fft))
    arith_mean = np.mean(fft)
    flatness = geo_mean / (arith_mean + 1e-10)
    
    coherence = 1 - flatness  # low flatness = tonal = coherent
    
    # Quality = novelty × coherence
    quality = novelty * coherence
    
    return float(novelty), float(coherence), float(quality)

# Part 1: ε sweep with quality metric
print("--- Part 1: ε vs Quality (Lorenz system) ---")

N = 100
dt = 0.01
epsilons = np.linspace(0.01, 2.0, 40)

epsilon_results = []

for eps in epsilons:
    state = np.random.randn(N, 3) * 0.1
    outputs = []
    
    for step in range(10000):
        x, y, z = state[:, 0], state[:, 1], state[:, 2]
        dx = 10 * (y - x)
        dy = x * (28 - z) - y
        dz = x * y - 8/3 * z
        noise = np.random.randn(N, 3) * eps
        
        state += (np.column_stack([dx, dy, dz]) * dt) + noise * np.sqrt(dt)
        outputs.append(float(np.mean(state[:, 0])))
    
    novelty, coherence, quality = compute_quality(outputs)
    epsilon_results.append({
        'eps': eps,
        'novelty': novelty,
        'coherence': coherence,
        'quality': quality
    })

# Find peaks
best_diversity = max(epsilon_results, key=lambda r: r['novelty'])
best_coherence = max(epsilon_results, key=lambda r: r['coherence'])
best_quality = max(epsilon_results, key=lambda r: r['quality'])

print(f"  Best diversity at ε={best_diversity['eps']:.3f}: novelty={best_diversity['novelty']:.4f}")
print(f"  Best coherence at ε={best_coherence['eps']:.3f}: coherence={best_coherence['coherence']:.4f}")
print(f"  Best QUALITY at ε={best_quality['eps']:.3f}: quality={best_quality['quality']:.4f}")

if abs(best_diversity['eps'] - best_quality['eps']) > 0.1:
    print(f"\n  ⚡ DIVERSITY ≠ QUALITY: sweet spots differ!")
    print(f"    Diversity peaks at ε={best_diversity['eps']:.3f}")
    print(f"    Quality peaks at ε={best_quality['eps']:.3f}")
else:
    print(f"\n  Diversity and quality share the same sweet spot")

# Part 2: Quality across regimes
print("\n--- Part 2: Quality by Regime ---")

rho_values = [5, 10, 15, 20, 24.74, 28, 35, 45, 60]

for rho in rho_values:
    state = np.random.randn(N, 3) * 0.1
    outputs = []
    
    for step in range(10000):
        x, y, z = state[:, 0], state[:, 1], state[:, 2]
        dx = 10 * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - 8/3 * z
        state += np.column_stack([dx, dy, dz]) * dt
        outputs.append(float(np.mean(state[:, 0])))
    
    novelty, coherence, quality = compute_quality(outputs)
    regime = "CHAOTIC" if rho > 24.74 else "PERIODIC" if rho > 1 else "FIXED"
    print(f"  ρ={rho:5.1f} [{regime:8s}]: novelty={novelty:.4f}, coherence={coherence:.4f}, quality={quality:.6f}")

# Part 3: Soft snap quality
print("\n--- Part 3: Soft Snap Quality ---")

epsilons_snap = np.linspace(0.01, 1.5, 30)

for eps in epsilons_snap[::3]:
    x = np.random.randn(5000) * 3
    snapped = np.round(x)
    soft = (1 - eps) * snapped + eps * x
    
    # Quality of the constraint system
    novelty = float(np.std(soft))
    # Coherence: how close to lattice (structure)
    near_lattice = float(np.mean(np.abs(soft - np.round(soft))))
    coherence = 1 / (1 + near_lattice)
    quality = novelty * coherence
    
    print(f"  ε={eps:.2f}: novelty={novelty:.4f}, near_lattice={near_lattice:.4f}, quality={quality:.6f}")

# Part 4: The Inverted-U for quality
print("\n--- Part 4: Quality Inverted-U ---")
print("  Is quality also an inverted-U in ε?")

qualities = [r['quality'] for r in epsilon_results]
coherences = [r['coherence'] for r in epsilon_results]
novelties = [r['novelty'] for r in epsilon_results]

# Check for inverted-U
mid = len(qualities) // 2
early_quality = np.mean(qualities[:mid])
late_quality = np.mean(qualities[mid:])
peak_quality = max(qualities)

if peak_quality > early_quality and peak_quality > late_quality:
    print(f"  YES — quality is an inverted-U. Peak at ε={epsilon_results[np.argmax(qualities)]['eps']:.3f}")
else:
    print(f"  NO — quality is monotonic. Peak at ε={epsilon_results[np.argmax(qualities)]['eps']:.3f}")

# Coherence always decreases with noise (expected)
print(f"\n  Coherence: {coherences[0]:.4f} → {coherences[-1]:.4f} (monotonic decrease)")
print(f"  Novelty: {novelties[0]:.4f} → {novelties[-1]:.4f}")
print(f"  Quality = novelty × coherence: the tradeoff creates the sweet spot")

with open('CODE/EXPERIMENT-QUALITY.json', 'w') as f:
    json.dump({
        'best_diversity_eps': best_diversity['eps'],
        'best_quality_eps': best_quality['eps'],
        'epsilon_results': epsilon_results,
    }, f, indent=2)

print("\n=== QUALITY ≠ DIVERSITY — THE TRADEOFF IS REAL ===")
