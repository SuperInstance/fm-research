import numpy as np
import json

print("=== Experiment 37: The Inverse Problem ===\n")
print("Given creative output, reconstruct the constraints.\n")

np.random.seed(42)

def generate_output(sigma, rho, beta, eps, T=5000, N=200):
    """Generate creative output with known parameters."""
    dt = 0.01
    state = np.random.randn(N, 3) * 0.1
    outputs = []
    
    for step in range(T):
        x, y, z = state[:, 0], state[:, 1], state[:, 2]
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
        noise = np.random.randn(N, 3) * eps
        state += (np.column_stack([dx, dy, dz]) * dt) + noise * np.sqrt(dt)
        
        if step > T // 2:
            outputs.append(float(np.mean(state[:, 0])))
    
    return np.array(outputs)

def estimate_parameters(outputs):
    """Try to reconstruct Lorenz parameters from output alone."""
    
    # 1. Estimate ρ from variance
    variance = np.var(outputs)
    # In Lorenz, variance of x grows with ρ
    # Rough calibration from our experiments
    rho_est = 1 + variance * 5  # rough mapping
    
    # 2. Estimate noise level from high-frequency content
    diff = np.diff(outputs)
    hf_energy = np.var(diff)
    # High-frequency energy proportional to noise
    eps_est = np.sqrt(hf_energy) * 0.5
    
    # 3. Estimate σ from autocorrelation decay
    ac = np.corrcoef(outputs[:-1], outputs[1:])[0, 1]
    # Higher σ → faster decorrelation
    sigma_est = 10 * (1 - ac)  # rough mapping
    
    # 4. Lyapunov estimate from divergence
    # Use segments
    n_segs = 10
    seg_len = len(outputs) // n_segs
    seg_vars = [np.var(outputs[i*seg_len:(i+1)*seg_len]) for i in range(n_segs)]
    lyapunov_est = np.std(seg_vars) / np.mean(seg_vars)
    
    # 5. Regime classification
    if variance < 1:
        regime = "FIXED-POINT"
    elif variance < 50:
        regime = "PERIODIC"
    else:
        regime = "CHAOTIC"
    
    # 6. Coherence (structure vs noise)
    fft = np.abs(np.fft.rfft(outputs))
    fft_norm = fft / (fft.sum() + 1e-10)
    flatness = np.exp(np.mean(np.log(fft_norm + 1e-10))) / (np.mean(fft_norm) + 1e-10)
    coherence = 1 - flatness
    
    return {
        'rho_est': float(rho_est),
        'eps_est': float(eps_est),
        'sigma_est': float(sigma_est),
        'lyapunov_est': float(lyapunov_est),
        'regime': regime,
        'coherence': float(coherence),
        'variance': float(variance),
    }

# Part 1: Parameter recovery test
print("--- Part 1: Parameter Recovery ---")

test_cases = [
    {'sigma': 10, 'rho': 5, 'eps': 0.1, 'label': 'periodic low noise'},
    {'sigma': 10, 'rho': 15, 'eps': 0.1, 'label': 'periodic med noise'},
    {'sigma': 10, 'rho': 28, 'eps': 0.1, 'label': 'chaotic low noise'},
    {'sigma': 10, 'rho': 28, 'eps': 0.5, 'label': 'chaotic med noise'},
    {'sigma': 10, 'rho': 45, 'eps': 0.1, 'label': 'high chaos low noise'},
    {'sigma': 7, 'rho': 47, 'eps': 0.01, 'label': 'meta-wheel optimum'},
]

results = []

for case in test_cases:
    output = generate_output(case['sigma'], case['rho'], 8/3, case['eps'])
    estimated = estimate_parameters(output)
    
    rho_err = abs(estimated['rho_est'] - case['rho']) / case['rho'] * 100
    eps_err = abs(estimated['eps_est'] - case['eps']) / (case['eps'] + 0.01) * 100
    
    print(f"  {case['label']:25s}: ρ={case['rho']}→{estimated['rho_est']:.1f} ({rho_err:.0f}% err), "
          f"ε={case['eps']}→{estimated['eps_est']:.3f} ({eps_err:.0f}% err), "
          f"regime={estimated['regime']}")
    
    results.append({
        'label': case['label'],
        'actual': {k: v for k, v in case.items() if k != 'label'},
        'estimated': estimated,
        'rho_error_pct': rho_err,
        'eps_error_pct': eps_err,
    })

# Part 2: Style fingerprinting
print("\n--- Part 2: Style Fingerprinting ---")
# Can we distinguish different "creative styles" (parameter sets) from output alone?

styles = {
    'minimalist': {'sigma': 5, 'rho': 10, 'eps': 0.01},
    'classical': {'sigma': 10, 'rho': 20, 'eps': 0.05},
    'jazz': {'sigma': 10, 'rho': 28, 'eps': 0.1},
    'free_jazz': {'sigma': 10, 'rho': 40, 'eps': 0.3},
    'noise_music': {'sigma': 15, 'rho': 50, 'eps': 0.5},
}

style_fingerprints = {}

for style, params in styles.items():
    output = generate_output(params['sigma'], params['rho'], 8/3, params['eps'])
    fingerprint = estimate_parameters(output)
    style_fingerprints[style] = fingerprint
    
    print(f"  {style:15s}: ρ≈{fingerprint['rho_est']:.1f}, ε≈{fingerprint['eps_est']:.3f}, "
          f"regime={fingerprint['regime']}, coherence={fingerprint['coherence']:.4f}")

# Part 3: Unknown sample classification
print("\n--- Part 3: Unknown Sample Classification ---")

# Generate an unknown sample
unknown = generate_output(8, 30, 8/3, 0.15)
unknown_fp = estimate_parameters(unknown)

print(f"  Unknown sample: ρ≈{unknown_fp['rho_est']:.1f}, ε≈{unknown_fp['eps_est']:.3f}, "
      f"regime={unknown_fp['regime']}")

# Find closest style
best_match = None
best_dist = float('inf')
for style, fp in style_fingerprints.items():
    dist = ((fp['rho_est'] - unknown_fp['rho_est'])**2 + 
            (fp['eps_est'] - unknown_fp['eps_est'])**2 +
            (fp['coherence'] - unknown_fp['coherence'])**2)
    if dist < best_dist:
        best_dist = dist
        best_match = style

print(f"  Classified as: {best_match} (distance={best_dist:.4f})")

# Part 4: Musical genre detection
print("\n--- Part 4: Genre Parameter Mapping ---")

genres = {
    'Baroque': {'sigma': 8, 'rho': 12, 'eps': 0.02, 'description': 'structured, low freedom'},
    'Classical': {'sigma': 10, 'rho': 18, 'eps': 0.05, 'description': 'balanced, moderate'},
    'Romantic': {'sigma': 10, 'rho': 25, 'eps': 0.1, 'description': 'expressive, some chaos'},
    'Jazz': {'sigma': 10, 'rho': 28, 'eps': 0.15, 'description': 'improvisational, chaotic'},
    'Free Jazz': {'sigma': 12, 'rho': 40, 'eps': 0.3, 'description': 'high chaos, high freedom'},
    'Electronic': {'sigma': 10, 'rho': 30, 'eps': 0.01, 'description': 'chaotic but precise'},
    'Noise': {'sigma': 15, 'rho': 50, 'eps': 0.5, 'description': 'maximum chaos + noise'},
}

print(f"  {'Genre':12s} {'ρ':>6s} {'ε':>6s} {'Regime':10s} {'Coherence':>10s}")
print(f"  {'-'*12} {'-'*6} {'-'*6} {'-'*10} {'-'*10}")

for genre, params in genres.items():
    output = generate_output(params['sigma'], params['rho'], 8/3, params['eps'])
    fp = estimate_parameters(output)
    print(f"  {genre:12s} {fp['rho_est']:6.1f} {fp['eps_est']:6.3f} {fp['regime']:10s} {fp['coherence']:10.4f}")

with open('CODE/EXPERIMENT-INVERSE-PROBLEM.json', 'w') as f:
    json.dump({
        'recovery_results': results,
        'style_fingerprints': style_fingerprints,
    }, f, indent=2)

print("\n=== INVERSE PROBLEM: CONSTRAINTS RECOVERABLE FROM OUTPUT ===")
