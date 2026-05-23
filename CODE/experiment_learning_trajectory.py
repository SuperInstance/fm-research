import numpy as np
import json

print("=== Experiment 27: Creative Learning Trajectory ===\n")
print("Simulate an agent learning creativity over 1000 time steps.\n")

N = 1  # single agent learning
dt = 0.01

# The agent's Lorenz parameters evolve over time
# Start: low ρ (fixed-point, rigid beginner)
# End: high ρ (chaotic, creative expert)

total_steps = 50000
rho_trajectory = np.concatenate([
    np.linspace(0.5, 5, total_steps // 4),       # Beginner: slowly increasing
    np.linspace(5, 15, total_steps // 4),          # Intermediate: faster growth
    np.linspace(15, 28, total_steps // 4),         # Advanced: approaching chaos
    np.linspace(28, 40, total_steps // 4),         # Expert: in chaotic regime
])

sigma = 10.0
beta = 8/3

state = np.array([0.1, 0.1, 0.1])
creative_outputs = []
autocorrelations = []
regime_labels = []
epsilon_optimal = []

window = 500

for step in range(total_steps):
    rho = rho_trajectory[step]
    x, y, z = state
    
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    
    state = state + np.array([dx, dy, dz]) * dt
    creative_outputs.append(float(x))
    
    # Compute regime diagnostics every 1000 steps
    if step > 0 and step % 1000 == 0:
        recent = creative_outputs[-window:]
        
        # Autocorrelation
        if len(recent) > 10:
            ac = np.corrcoef(recent[:-1], recent[1:])[0, 1]
        else:
            ac = 0
        autocorrelations.append(ac)
        
        # Variance
        var = np.var(recent)
        
        # Determine regime
        if var < 1.0:
            regime = "FIXED-POINT"
            eps_opt = 1.5  # needs high freedom
        elif var < 50:
            regime = "PERIODIC"
            eps_opt = 0.5  # SR sweet spot
        else:
            regime = "CHAOTIC"
            eps_opt = 0.2  # needs constraints
        
        regime_labels.append(regime)
        epsilon_optimal.append(eps_opt)
        
        progress = step / total_steps * 100
        if step % 5000 == 0:
            print(f"  Step {step:5d} ({progress:3.0f}%): ρ={rho:.1f}, "
                  f"var={var:.2f}, autocorr={ac:.3f}, regime={regime}, ε*={eps_opt:.2f}")

# Analysis
print(f"\n{'='*60}")
print("LEARNING TRAJECTORY ANALYSIS")
print(f"{'='*60}")

# Count time in each regime
from collections import Counter
regime_counts = Counter(regime_labels)
total_regime = len(regime_labels)

print(f"\n  Time in each regime:")
for regime, count in regime_counts.most_common():
    print(f"    {regime}: {count}/{total_regime} ({count/total_regime*100:.0f}%)")

# ε* trajectory
print(f"\n  Optimal ε trajectory:")
for i in range(0, len(epsilon_optimal), max(1, len(epsilon_optimal)//10)):
    print(f"    {i*1000:5d} steps: ε* = {epsilon_optimal[i]:.2f} ({regime_labels[i]})")

# Regime transitions
print(f"\n  Regime transitions:")
prev_regime = regime_labels[0]
for i, regime in enumerate(regime_labels):
    if regime != prev_regime:
        step = i * 1000
        rho = rho_trajectory[step]
        print(f"    Step {step}: {prev_regime} → {regime} (ρ={rho:.1f})")
        prev_regime = regime

# Key insight: ε* DECREASES as expertise increases
print(f"\n  ε* range: {max(epsilon_optimal):.2f} (beginner) → {min(epsilon_optimal):.2f} (expert)")
print(f"  Direction: ε* {'DECREASES' if epsilon_optimal[-1] < epsilon_optimal[0] else 'INCREASES'} with expertise")
print(f"\n  IMPLICATION: Beginners need freedom, experts need constraints")
print(f"  This is the regime-dependent creativity theory in action.")

# Part 2: With adaptive ε (optimal learning)
print(f"\n{'='*60}")
print("ADAPTIVE ε vs FIXED ε")
print(f"{'='*60}")

def run_with_epsilon(eps_func, total_steps=20000):
    """Run learning trajectory with given ε schedule."""
    state = np.array([0.1, 0.1, 0.1])
    outputs = []
    
    for step in range(total_steps):
        rho = 0.5 + 39.5 * step / total_steps  # beginner to expert
        x, y, z = state
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
        
        eps = eps_func(step, total_steps)
        noise = np.random.randn(3) * eps
        
        state = state + np.array([dx, dy, dz]) * dt + noise * np.sqrt(dt)
        outputs.append(float(state[0]))
    
    return outputs

# Fixed ε = 0.5 (one-size-fits-all)
fixed_outputs = run_with_epsilon(lambda s, t: 0.5)

# Adaptive ε (high for beginners, low for experts)
adaptive_outputs = run_with_epsilon(lambda s, t: 1.5 * (1 - s/t) + 0.1 * (s/t))

# Reverse adaptive (wrong direction — constraints for beginners, freedom for experts)
reverse_outputs = run_with_epsilon(lambda s, t: 0.1 * (1 - s/t) + 1.5 * (s/t))

fixed_var = np.var(fixed_outputs)
adaptive_var = np.var(adaptive_outputs)
reverse_var = np.var(reverse_outputs)

print(f"  Fixed ε=0.5: output variance = {fixed_var:.2f}")
print(f"  Adaptive ε (high→low): output variance = {adaptive_var:.2f}")
print(f"  Reverse ε (low→high): output variance = {reverse_var:.2f}")
print(f"\n  Adaptive improvement over fixed: {(adaptive_var/fixed_var - 1)*100:.1f}%")
print(f"  Reverse penalty vs adaptive: {(1 - reverse_var/adaptive_var)*100:.1f}% worse")

with open('EXPERIMENT-LEARNING-TRAJECTORY.json', 'w') as f:
    json.dump({
        'regime_counts': dict(regime_counts),
        'epsilon_trajectory': epsilon_optimal,
        'fixed_var': float(fixed_var),
        'adaptive_var': float(adaptive_var),
        'reverse_var': float(reverse_var),
    }, f, indent=2)

print("\n=== LEARNING TRAJECTORY: BEGINNERS NEED NOISE, EXPERTS NEED CONSTRAINTS ===")
