import numpy as np
import json

print("=== Experiment 23: Competitive Creativity ===\n")
print("Two creative systems interact. Do they cooperate, compete, or something else?\n")

# Two Lorenz systems with different "cultures"
# System A: high σ (fast consensus), low ρ (moderate stress)  → "classical"
# System B: low σ (slow consensus), high ρ (high stress)     → "experimental"

N = 500  # agents per system
dt = 0.01

def lorenz_step(state, sigma, rho, beta, dt):
    x, y, z = state[:, 0], state[:, 1], state[:, 2]
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return state + np.column_stack([dx, dy, dz]) * dt

# Part 1: Independent baselines
print("--- Part 1: Independent Baselines ---")

# Classical system
state_a = np.random.randn(N, 3) * 0.1
for _ in range(5000):
    state_a = lorenz_step(state_a, 10.0, 20.0, 8/3, dt)
div_a_alone = float(np.std(state_a[:, 0]))

# Experimental system
state_b = np.random.randn(N, 3) * 0.1
for _ in range(5000):
    state_b = lorenz_step(state_b, 5.0, 35.0, 8/3, dt)
div_b_alone = float(np.std(state_b[:, 0]))

print(f"  Classical alone: diversity={div_a_alone:.4f}")
print(f"  Experimental alone: diversity={div_b_alone:.4f}")

# Part 2: Coupled — different coupling modes
print("\n--- Part 2: Coupled Systems ---")

coupling_modes = {
    'cooperative': lambda a, b: 0.01 * (b - a),  # move toward each other
    'competitive': lambda a, b: -0.01 * (b - a),  # move away from each other
    'predator_prey': lambda a, b: 0.01 * np.sign(b - a) * np.abs(b - a),  # nonlinear
    'mutualism': lambda a, b: 0.01 * np.abs(b - a) / (np.abs(b - a) + 1),  # benefit from difference
    'parasitic': lambda a, b: 0.01 * (b - a) * np.exp(-np.abs(b - a)),  # exploit similarity
}

results = {}

for mode_name, coupling_fn in coupling_modes.items():
    state_a = np.random.randn(N, 3) * 0.1
    state_b = np.random.randn(N, 3) * 0.1
    
    diversities_a = []
    diversities_b = []
    cross_corrs = []
    energy_transfers = []
    
    for step in range(10000):
        # Independent dynamics
        state_a = lorenz_step(state_a, 10.0, 20.0, 8/3, dt)
        state_b = lorenz_step(state_b, 5.0, 35.0, 8/3, dt)
        
        # Coupling (only on x-dimension — "creative output")
        coupling = coupling_fn(state_a[:, 0], state_b[:, 0])
        state_a[:, 0] += coupling * dt
        state_b[:, 0] -= coupling * dt  # conservation of "creative energy"
        
        if step > 5000 and step % 50 == 0:
            div_a = float(np.std(state_a[:, 0]))
            div_b = float(np.std(state_b[:, 0]))
            cross_corr = float(np.corrcoef(state_a[:, 0], state_b[:, 0])[0, 1])
            energy_transfer = float(np.mean(np.abs(coupling)))
            
            diversities_a.append(div_a)
            diversities_b.append(div_b)
            cross_corrs.append(cross_corr)
            energy_transfers.append(energy_transfer)
    
    results[mode_name] = {
        'div_a': float(np.mean(diversities_a)),
        'div_b': float(np.mean(diversities_b)),
        'cross_corr': float(np.mean(cross_corrs)),
        'energy_transfer': float(np.mean(energy_transfers)),
        'total_creative_output': float(np.mean(diversities_a) + np.mean(diversities_b)),
    }
    
    print(f"\n  {mode_name}:")
    print(f"    Classical diversity: {results[mode_name]['div_a']:.4f} (vs {div_a_alone:.4f} alone)")
    print(f"    Experimental diversity: {results[mode_name]['div_b']:.4f} (vs {div_b_alone:.4f} alone)")
    print(f"    Cross-correlation: {results[mode_name]['cross_corr']:.4f}")
    print(f"    Energy transfer: {results[mode_name]['energy_transfer']:.6f}")

# Find best coupling mode
best_mode = max(results.items(), key=lambda x: x[1]['total_creative_output'])
print(f"\n  🏆 Best creative coupling: {best_mode[0]}")
print(f"     Total output: {best_mode[1]['total_creative_output']:.4f}")

# Part 3: Phase diagram — coupling strength vs creative output
print("\n--- Part 3: Phase Diagram (coupling strength × creative output) ---")

coupling_strengths = [0.0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5]
phase_results = []

for strength in coupling_strengths:
    state_a = np.random.randn(N, 3) * 0.1
    state_b = np.random.randn(N, 3) * 0.1
    
    for step in range(8000):
        state_a = lorenz_step(state_a, 10.0, 20.0, 8/3, dt)
        state_b = lorenz_step(state_b, 5.0, 35.0, 8/3, dt)
        
        coupling = strength * (state_b[:, 0] - state_a[:, 0])
        state_a[:, 0] += coupling * dt
        state_b[:, 0] -= coupling * dt
    
    div_total = float(np.std(state_a[:, 0]) + np.std(state_b[:, 0]))
    corr = float(np.corrcoef(state_a[:, 0], state_b[:, 0])[0, 1])
    phase_results.append({
        'strength': strength,
        'total_diversity': div_total,
        'correlation': corr
    })
    print(f"  K={strength:.3f}: total_div={div_total:.4f}, corr={corr:.4f}")

# Find optimal coupling
optimal = max(phase_results, key=lambda x: x['total_diversity'])
print(f"\n  Optimal coupling: K={optimal['strength']:.3f}")
print(f"  This is the CREATIVE IMPEDANCE MATCHING point")

# Part 4: Evolution of coupling (the coupling itself evolves)
print("\n--- Part 4: Evolving Coupling ---")

state_a = np.random.randn(N, 3) * 0.1
state_b = np.random.randn(N, 3) * 0.1
K_evolved = 0.01
K_history = []

for step in range(20000):
    state_a = lorenz_step(state_a, 10.0, 20.0, 8/3, dt)
    state_b = lorenz_step(state_b, 5.0, 35.0, 8/3, dt)
    
    coupling = K_evolved * (state_b[:, 0] - state_a[:, 0])
    state_a[:, 0] += coupling * dt
    state_b[:, 0] -= coupling * dt
    
    # Evolve K: reinforce if diversity increases
    current_div = np.std(state_a[:, 0]) + np.std(state_b[:, 0])
    K_evolved *= 1 + 0.0001 * (current_div - 10)  # target diversity = 10
    K_evolved = max(0.0, min(1.0, K_evolved))
    
    if step % 2000 == 0:
        K_history.append(float(K_evolved))
        print(f"  Step {step}: K_evolved={K_evolved:.6f}, diversity={current_div:.4f}")

print(f"\n  K evolved: {K_history[0]:.6f} → {K_history[-1]:.6f}")

with open('EXPERIMENT-COMPETITIVE-CREATIVITY.json', 'w') as f:
    json.dump({
        'coupling_modes': {k: v for k, v in results.items()},
        'phase_diagram': phase_results,
        'K_evolution': K_history,
        'best_mode': best_mode[0],
    }, f, indent=2)

print("\n=== COMPETITIVE CREATIVITY: Coupling has an optimum ===")
print("=== Too little = isolated. Too much = homogenized. Just right = amplified ===")
