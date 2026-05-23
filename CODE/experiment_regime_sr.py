import numpy as np
import json

print("=== Experiment 24: Regime-Dependent Stochastic Resonance ===\n")
print("Hypothesis: SR works in ordered regimes, NOT in chaotic regimes.\n")

N = 500
dt = 0.01
T = 10000

def lorenz_step(state, sigma, rho, beta, dt):
    x, y, z = state[:, 0], state[:, 1], state[:, 2]
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return state + np.column_stack([dx, dy, dz]) * dt

# Test across different ρ regimes with different noise levels
rho_values = [0.5, 1.0, 5.0, 10.0, 15.0, 20.0, 24.74, 28.0, 35.0, 50.0]
noise_levels = [0.0, 0.001, 0.01, 0.05, 0.1, 0.5, 1.0]

results = []

for rho in rho_values:
    print(f"--- ρ = {rho:.2f} ---")
    
    for noise in noise_levels:
        state = np.random.randn(N, 3) * 0.1
        
        # Add a weak periodic signal (like the SR experiments)
        signal_freq = 0.5
        signal_amp = 0.1
        
        diversities = []
        signal_correlations = []
        
        for step in range(T):
            # Lorenz dynamics
            state = lorenz_step(state, 10.0, rho, 8/3, dt)
            
            # Add signal + noise
            t = step * dt
            signal = signal_amp * np.sin(2 * np.pi * signal_freq * t)
            noise_arr = np.random.randn(N, 3) * noise
            
            state[:, 0] += (signal + noise_arr[:, 0]) * dt
            
            if step > T // 2:
                diversities.append(np.std(state[:, 0]))
                # Correlation of x output with signal
                corr = np.abs(np.mean(np.sign(state[:, 0]) * np.sign(signal)))
                signal_correlations.append(corr)
        
        avg_div = float(np.mean(diversities))
        avg_corr = float(np.mean(signal_correlations))
        
        regime = "CHAOTIC" if rho > 24.74 else "PERIODIC" if rho > 1.0 else "FIXED"
        
        results.append({
            'rho': rho,
            'noise': noise,
            'diversity': avg_div,
            'signal_corr': avg_corr,
            'regime': regime
        })
        
        if noise in [0.0, 0.01, 0.1, 1.0]:
            print(f"  noise={noise:.3f}: div={avg_div:.4f}, signal_corr={avg_corr:.4f} [{regime}]")

# Analysis: find SR peak (max signal correlation) in each regime
print("\n=== SR PEAK BY REGIME ===")
for rho in rho_values:
    rho_results = [r for r in results if r['rho'] == rho]
    best = max(rho_results, key=lambda r: r['signal_corr'])
    baseline = [r for r in rho_results if r['noise'] == 0.0][0]
    improvement = (best['signal_corr'] - baseline['signal_corr']) / (baseline['signal_corr'] + 1e-10) * 100
    regime = best['regime']
    
    print(f"  ρ={rho:6.2f} [{regime:8s}]: best noise={best['noise']:.3f}, "
          f"corr={best['signal_corr']:.4f} (baseline={baseline['signal_corr']:.4f}, "
          f"+{improvement:.1f}%)")

# Key comparison: ordered vs chaotic SR effect
ordered = [r for r in results if r['rho'] < 24.74]
chaotic = [r for r in results if r['rho'] >= 24.74]

ordered_with_noise = [r for r in ordered if r['noise'] > 0]
chaotic_with_noise = [r for r in chaotic if r['noise'] > 0]

ordered_baseline = np.mean([r['signal_corr'] for r in ordered if r['noise'] == 0])
chaotic_baseline = np.mean([r['signal_corr'] for r in chaotic if r['noise'] == 0])

ordered_best = np.mean([max([r for r in ordered if r['noise'] > 0], 
                            key=lambda r: r['signal_corr'])['signal_corr'] 
                        for rho in set(r['rho'] for r in ordered)])
chaotic_best = np.mean([max([r for r in chaotic if r['noise'] > 0], 
                            key=lambda r: r['signal_corr'])['signal_corr'] 
                         for rho in set(r['rho'] for r in chaotic)])

print(f"\n  Ordered regime: baseline={ordered_baseline:.4f}, best with noise={ordered_best:.4f}")
print(f"  Chaotic regime: baseline={chaotic_baseline:.4f}, best with noise={chaotic_best:.4f}")
print(f"  SR effect (ordered): +{(ordered_best/ordered_baseline - 1)*100:.1f}%")
print(f"  SR effect (chaotic): +{(chaotic_best/chaotic_baseline - 1)*100:.1f}%")
print(f"\n  {'HYPOTHESIS CONFIRMED' if (ordered_best/ordered_baseline) > (chaotic_best/chaotic_baseline) else 'HYPOTHESIS REJECTED'}")

with open('CODE/EXPERIMENT-REGIME-SR.json', 'w') as f:
    json.dump({'results': results}, f, indent=2)

print("\n=== REGIME-DEPENDENT SR ===")
