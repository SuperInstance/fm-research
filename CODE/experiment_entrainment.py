import numpy as np
import json

print("=== Entrainment: How Rhythms Lock Together ===\n")

# Entrainment: when two oscillators with different natural frequencies
# are weakly coupled, they adjust to a common frequency.
# This is how:
# - Heartbeats sync with breathing
# - Walkers sync on a bridge
# - Musicians groove together
# - Cultures sync through shared rituals
# - Audiences clap in unison
# - Fireflies flash together

# Part 1: Two-oscillator entrainment
print("--- Part 1: Two Oscillator Entrainment ---")
omega1 = 1.0  # rad/s (natural freq of oscillator 1)
dt = 0.01
for omega2 in [0.5, 0.8, 0.95, 1.0, 1.05, 1.2, 2.0]:
    for K in [0.0, 0.1, 0.3, 0.5, 1.0]:
        theta1, theta2 = 0.0, 0.0
        
        for t in range(10000):
            coupling = K * np.sin(theta2 - theta1)
            theta1 += (omega1 + coupling) * dt
            theta2 += (omega2 - coupling) * dt
        
        # Phase difference
        phase_diff = (theta1 - theta2) % (2 * np.pi)
        
        locked = phase_diff < 0.1 or abs(phase_diff - 2*np.pi) < 0.1
        if K == 0.5:  # just show mid-coupling
            print(f"  ω1={omega1:.1f}, ω2={omega2:.2f}, K={K:.1f}: phase_diff={phase_diff:.3f}, {'LOCKED' if locked else 'FREE'}")

# Part 2: N-oscillator entrainment (audience clapping)
print("\n--- Part 2: Audience Clapping Synchronization ---")
N_people = 50
np.random.seed(42)
natural_freqs = np.random.normal(2.0, 0.3, N_people)  # ~2 Hz clapping, some variation

for coupling in [0.0, 0.1, 0.3, 0.5, 1.0, 2.0]:
    phases = np.random.uniform(0, 2*np.pi, N_people)
    omegas = natural_freqs.copy()
    
    for t in range(5000):
        mean_phase = np.angle(np.mean(np.exp(1j * phases)))
        for i in range(N_people):
            phases[i] += (omegas[i] + coupling * np.sin(mean_phase - phases[i])) * dt
    
    # Order parameter (0=desynchronized, 1=perfect sync)
    order = abs(np.mean(np.exp(1j * phases)))
    print(f"  K={coupling:.1f}: order parameter = {order:.4f} ({'SYNC' if order > 0.8 else 'PARTIAL' if order > 0.4 else 'CHAOS'})")

# Part 3: Entrainment cascade
print("\n--- Part 3: Entrainment Cascade ---")
# Start with 2 synchronized oscillators, add more one at a time
# How many new oscillators can the core absorb?

core_size = 5
newcomers = 20
total = core_size + newcomers

omegas = np.zeros(total)
omegas[:core_size] = 1.0  # core is perfectly synced
omegas[core_size:] = np.random.normal(1.0, 0.5, newcomers)  # newcomers are wild

phases = np.zeros(total)
phases[:core_size] = 0.0  # core in phase
phases[core_size:] = np.random.uniform(0, 2*np.pi, newcomers)

K = 0.3
for t in range(10000):
    mean_phase = np.angle(np.mean(np.exp(1j * phases)))
    for i in range(total):
        phases[i] += (omegas[i] + K * np.sin(mean_phase - phases[i])) * dt

order = abs(np.mean(np.exp(1j * phases)))
core_order = abs(np.mean(np.exp(1j * phases[:core_size])))
newcomer_order = abs(np.mean(np.exp(1j * phases[core_size:])))
locked_newcomers = sum(1 for i in range(core_size, total) 
                       if abs(np.sin(phases[i] - mean_phase)) < 0.3)

print(f"  Core sync: {core_order:.3f}")
print(f"  Newcomer sync: {newcomer_order:.3f}")
print(f"  Overall: {order:.3f}")
print(f"  Newcomers locked: {locked_newcomers}/{newcomers}")
print(f"  Cascade absorption rate: {locked_newcomers/newcomers:.1%}")

# Part 4: Cultural entrainment simulation
print("\n--- Part 4: Cultural Entrainment ---")
# Simulate a culture as an oscillator with frequency = rate of change
# Two cultures in contact: how long until they entrain?

cultures = {
    'Western': {'omega': 1.0, 'phase': 0.0},      # fast-changing
    'Eastern': {'omega': 0.6, 'phase': np.pi/4},   # slower-changing
    'African': {'omega': 0.8, 'phase': np.pi/2},   # medium
    'Indigenous': {'omega': 0.3, 'phase': np.pi},   # very slow
}

for c1_name, c1 in cultures.items():
    for c2_name, c2 in cultures.items():
        if c1_name >= c2_name:
            continue
        
        freq_diff = abs(c1['omega'] - c2['omega'])
        
        # Time to entrain (approximate)
        # t_entrain ~ 1/K × 1/Δω for weak coupling
        K = 0.2  # cultural contact strength
        t_entrain = 1.0 / (K * freq_diff) if freq_diff > 0 else 0
        
        print(f"  {c1_name:12s} ↔ {c2_name:12s}: Δω={freq_diff:.2f}, entrain_time={t_entrain:.1f} units")

# Part 5: The entrainment threshold
print("\n--- Part 5: Critical Coupling for Entrainment ---")
# For K > Δω, entrainment occurs. This is the entrainment threshold.
# This IS the same as Kuramoto Kc for 2 oscillators.

for freq_ratio in [0.5, 0.8, 0.9, 0.95, 1.0]:
    omega2 = freq_ratio
    delta_omega = abs(1.0 - omega2)
    K_critical = delta_omega  # exact for 2 oscillators
    
    print(f"  ω₂/ω₁ = {freq_ratio:.2f}: K_critical = {K_critical:.3f}")
    print(f"    Below K={K_critical:.3f}: free running (independent cultures)")
    print(f"    Above K={K_critical:.3f}: entrained (shared rhythm)")

print("\n=== ENTRAINMENT PRINCIPLE ===")
print("Entrainment is the mechanism of cultural transmission.")
print("K > Δω is the condition for cultural sync.")
print("The 'melting pot' has HIGH K (forced interaction).")
print("The 'salad bowl' has LOW K (coexistence, no sync).")
print("The sweet spot: enough K to share rhythm, enough Δω to preserve identity.")

with open('EXPERIMENT-ENTRAINMENT.json', 'w') as f:
    json.dump({'cascade_rate': locked_newcomers/newcomers}, f)
