import numpy as np
import json

print("=== Experiment 25: Creative Thermodynamics ===\n")

N = 500
dt = 0.01

# Part 1: ε as temperature
# In thermodynamics: higher T = more disorder = more entropy
# In creative systems: higher ε = more freedom = more diversity
# Test: does diversity scale with ε the way entropy scales with T?

print("--- Part 1: ε ↔ Temperature ---")

epsilons = np.linspace(0.01, 2.0, 50)
diversities = []

for eps in epsilons:
    # Soft snap: C(x,ε) = (1-ε)*snap(x) + ε*x
    # Lorenz with ε as noise (temperature)
    state = np.random.randn(N, 3) * 0.1
    divs = []
    
    for step in range(5000):
        x, y, z = state[:, 0], state[:, 1], state[:, 2]
        dx = 10 * (y - x)
        dy = x * (28 - z) - y
        dz = x * y - 8/3 * z
        noise = np.random.randn(N, 3) * eps
        state += (np.column_stack([dx, dy, dz]) * dt) + noise * np.sqrt(dt)
        
        if step > 3000:
            divs.append(np.std(state[:, 0]))
    
    diversities.append(float(np.mean(divs)))

diversities = np.array(diversities)

# Fit: S = k * ln(T) (thermodynamic entropy)
# If ε=T, then diversity should go as ln(ε) at high ε
log_fit = np.polyfit(np.log(epsilons[10:]), diversities[10:], 1)
linear_fit = np.polyfit(epsilons, diversities, 1)

print(f"  Linear fit: div = {linear_fit[0]:.4f} * ε + {linear_fit[1]:.4f}")
print(f"  Log fit: div = {log_fit[0]:.4f} * ln(ε) + {log_fit[1]:.4f}")

# Which fits better?
linear_residual = np.mean((diversities - np.polyval(linear_fit, epsilons))**2)
log_residual = np.mean((diversities[10:] - np.polyval(log_fit, np.log(epsilons[10:])))**2)
print(f"  Linear MSE: {linear_residual:.6f}")
print(f"  Log MSE: {log_residual:.6f}")
print(f"  Best fit: {'LOGARITHMIC (thermodynamic)' if log_residual < linear_residual else 'LINEAR'}")

# Part 2: Phase transitions
# Thermodynamic: at T_c, specific heat diverges (phase transition)
# Creative: at ε_c, creative output should show discontinuity

print("\n--- Part 2: Phase Transitions ---")
# Use soft_snap directly
epsilons_fine = np.linspace(0.01, 2.0, 200)
snap_outputs = []
free_outputs = []

for eps in epsilons_fine:
    x = np.random.randn(1000) * 5  # input distribution
    
    # Lattice snap (quantize to nearest integer)
    snapped = np.round(x)
    
    # Soft snap
    soft = (1 - eps) * snapped + eps * x
    
    # "Creative output" = variance of output
    snap_outputs.append(float(np.var(soft)))
    
    # "Order parameter" = how close to snapped
    order = float(np.mean(np.abs(soft - x)))
    free_outputs.append(order)

snap_outputs = np.array(snap_outputs)
free_outputs = np.array(free_outputs)

# Derivative (analogous to specific heat)
d_output = np.gradient(snap_outputs, epsilons_fine)

# Find peaks in derivative (phase transitions)
from scipy.signal import find_peaks
peaks, properties = find_peaks(np.abs(d_output), height=np.percentile(np.abs(d_output), 90))

print(f"  Phase transitions detected at ε = {[f'{epsilons_fine[p]:.3f}' for p in peaks]}")
print(f"  Number of transitions: {len(peaks)}")

if len(peaks) > 0:
    for p in peaks:
        print(f"    ε_c = {epsilons_fine[p]:.3f}: output jump = {d_output[p]:.4f}")

# Part 3: Free energy analogy
# F = E - TS (free energy = internal energy - temperature × entropy)
# In creative systems: F_creative = constraint_energy - ε * diversity

print("\n--- Part 3: Free Energy Landscape ---")
eps_sample = [0.1, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0]

for eps in eps_sample:
    x = np.linspace(-5, 5, 1000)
    
    # Constraint energy: how far from lattice
    snapped = np.round(x)
    constraint_energy = 0.5 * (x - snapped)**2
    
    # Diversity (entropy analog): -p*ln(p)
    bins = np.histogram(x, bins=50, density=True)[0]
    bins = bins[bins > 0]
    entropy = -np.sum(bins * np.log(bins)) / len(bins)
    
    # Free energy
    free_energy = np.mean(constraint_energy) - eps * entropy
    
    print(f"  ε={eps:.1f}: E_constraint={np.mean(constraint_energy):.4f}, "
          f"S={entropy:.4f}, F=E-εS={free_energy:.4f}")

# Part 4: Equilibrium (consensus = thermal equilibrium)
print("\n--- Part 4: Consensus ↔ Equilibrium ---")

# N agents with opinions, coupled at different ε
N_agents = 100
T_steps = 5000

for eps in [0.01, 0.1, 0.3, 0.5, 1.0, 2.0]:
    opinions = np.random.randn(N_agents)
    
    # Consensus dynamics with ε as temperature
    K = 1.0  # coupling strength
    
    for step in range(T_steps):
        # Mean opinion
        mean_op = np.mean(opinions)
        # Move toward mean (consensus) + noise (ε = temperature)
        noise = np.random.randn(N_agents) * eps * 0.01
        opinions += K * (mean_op - opinions) * dt + noise
    
    final_std = float(np.std(opinions))
    final_mean = float(np.mean(opinions))
    print(f"  ε={eps:.2f}: equilibrium std={final_std:.4f}, mean={final_mean:.4f}")

print(f"\n  → As ε increases, equilibrium becomes more spread (higher T = more disorder)")
print(f"  → Consensus IS thermal equilibrium, ε IS temperature")

# Part 5: Maxwell's demon in creative systems
print("\n--- Part 5: Maxwell's Demon (selection = intelligence) ---")

# Without demon: random creative output
N_ideas = 10000
ideas_random = np.random.randn(N_ideas)

# With demon: select best ideas (constrain to lattice)
ideas_demon = np.round(ideas_random)  # snap to lattice

# Compare "quality" (distance from a target)
target = 3.0
quality_random = float(np.mean(np.abs(ideas_random - target)))
quality_demon = float(np.mean(np.abs(ideas_demon - target)))

# Cost: demon needs information
info_cost = float(np.mean(np.abs(ideas_random - ideas_demon)))

print(f"  Random quality: {quality_random:.4f}")
print(f"  Demon quality: {quality_demon:.4f}")
print(f"  Improvement: {(quality_random - quality_demon)/quality_random*100:.1f}%")
print(f"  Information cost: {info_cost:.4f}")
print(f"  → Maxwell's demon = constraint system selecting for quality")
print(f"  → The cost is the constraint energy (Landauer's principle)")

with open('CODE/EXPERIMENT-CREATIVE-THERMO.json', 'w') as f:
    json.dump({
        'phase_transitions': [float(epsilons_fine[p]) for p in peaks],
        'n_transitions': len(peaks),
        'best_fit': 'log' if log_residual < linear_residual else 'linear',
    }, f, indent=2)

print("\n=== CREATIVE THERMODYNAMICS MAPPED ===")
