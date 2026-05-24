import numpy as np
import json

print("=== Experiment 35: Quantum-Inspired Creativity ===\n")
print("Ideas exist in superposition until measured (committed to).\n")

np.random.seed(42)

# Part 1: Superposition of musical ideas
print("--- Part 1: Superposition of Creative States ---")

N_ideas = 12  # pitch classes
N_measurements = 1000

# A "creative state" is a superposition over pitch classes
# |ψ⟩ = Σ αᵢ|i⟩ where αᵢ are complex amplitudes

def create_creative_state(constraint_strength=0.5):
    """Create a superposition state with constraint bias."""
    # Unconstrained: uniform superposition
    amplitudes = np.ones(N_ideas) + 0j
    
    # Constraint: bias toward certain pitches (e.g., C major scale)
    scale = [0, 2, 4, 5, 7, 9, 11]  # C major
    for i in range(N_ideas):
        if i in scale:
            amplitudes[i] += constraint_strength
    
    # Normalize
    amplitudes /= np.sqrt(np.sum(np.abs(amplitudes)**2))
    return amplitudes

def measure(state, n_times=1):
    """Collapse superposition — Born rule."""
    probs = np.abs(state)**2
    probs /= probs.sum()
    return np.random.choice(N_ideas, size=n_times, p=probs)

# Test different constraint strengths
for cs in [0.0, 0.5, 1.0, 2.0, 5.0, 10.0]:
    state = create_creative_state(cs)
    measurements = measure(state, N_measurements)
    
    # Entropy of output (creative diversity)
    counts = np.bincount(measurements, minlength=N_ideas)
    probs = counts / counts.sum()
    entropy = -np.sum([p * np.log(p) for p in probs if p > 0])
    max_entropy = np.log(N_ideas)
    
    print(f"  constraint={cs:.1f}: entropy={entropy:.3f}/{max_entropy:.3f} ({entropy/max_entropy*100:.1f}%), "
          f"scale notes={sum(counts[i] for i in [0,2,4,5,7,9,11])}/{N_measurements}")

# Part 2: Entanglement between two creative agents
print("\n--- Part 2: Entangled Creative Agents ---")
# Two agents with correlated creative states
# If entangled, measuring one instantly constrains the other

def entangled_measure(agent1_state, agent2_state, correlation=0.5):
    """Measure two agents with quantum correlation."""
    m1 = measure(agent1_state, 1)[0]
    
    # Agent 2's state is modified by the measurement of agent 1
    modified = agent2_state.copy()
    # Boost the same note (positive correlation = agree)
    modified[m1] += correlation
    # Suppress opposite note
    modified[(m1 + 6) % N_ideas] -= correlation * 0.5
    modified = np.maximum(np.abs(modified), 0.01)
    modified /= np.sqrt(np.sum(np.abs(modified)**2))
    
    m2 = measure(modified, 1)[0]
    return m1, m2

state1 = create_creative_state(1.0)
state2 = create_creative_state(0.5)  # different constraint levels

for corr in [0.0, 0.3, 0.7, 1.0, 2.0, 5.0]:
    agreements = 0
    total = 500
    
    m1_history = []
    m2_history = []
    
    for _ in range(total):
        m1, m2 = entangled_measure(state1, state2, corr)
        if m1 == m2:
            agreements += 1
        m1_history.append(m1)
        m2_history.append(m2)
    
    # Mutual information
    joint = np.zeros((N_ideas, N_ideas))
    for a, b in zip(m1_history, m2_history):
        joint[a, b] += 1
    joint /= joint.sum()
    
    mi = 0
    for i in range(N_ideas):
        for j in range(N_ideas):
            if joint[i,j] > 0:
                mi += joint[i,j] * np.log(joint[i,j] / ((joint[i,:].sum() + 1e-10) * (joint[:,j].sum() + 1e-10)))
    
    print(f"  correlation={corr:.1f}: agreement={agreements}/{total} ({agreements/total*100:.1f}%), MI={mi:.4f}")

# Part 3: Uncertainty principle for creativity
print("\n--- Part 3: Creative Uncertainty Principle ---")
# Can't simultaneously know both WHAT you'll create and HOW creative it is
# Δposition × Δmomentum ≥ ℏ/2
# Analog: Δpitch × Δcreativity ≥ threshold

for cs in [0.1, 0.5, 1.0, 2.0, 5.0]:
    state = create_creative_state(cs)
    
    # Pitch certainty (inverse of entropy)
    probs = np.abs(state)**2
    pitch_certainty = 1 - (-np.sum([p*np.log(p) for p in probs if p > 0])) / np.log(N_ideas)
    
    # Creative certainty: variance of measurement outcomes over repeated runs
    creative_vars = []
    for trial in range(100):
        m = measure(state, 100)
        # "Creativity" = distance from mean pitch
        creative_var = float(np.var(m))
        creative_vars.append(creative_var)
    
    creative_uncertainty = float(np.std(creative_vars))
    product = pitch_certainty * creative_uncertainty
    
    print(f"  constraint={cs:.1f}: pitch_certainty={pitch_certainty:.3f}, "
          f"creative_uncertainty={creative_uncertainty:.3f}, product={product:.4f}")

# Part 4: Quantum tunneling in creative space
print("\n--- Part 4: Creative Quantum Tunneling ---")
# An idea that's "blocked" by a barrier can still appear through tunneling

def tunneling_probability(barrier_height, barrier_width, energy):
    """Quantum tunneling probability."""
    kappa = np.sqrt(max(0, 2 * (barrier_height - energy)))
    if kappa == 0:
        return 1.0
    return float(np.exp(-2 * kappa * barrier_width))

# "Barrier" = how far outside the scale
# "Energy" = creative drive (ε)
# "Width" = how many constraint violations needed

barriers = {
    'chromatic_passing': {'height': 0.5, 'width': 1},
    'outside_note': {'height': 2.0, 'width': 1},
    'key_change': {'height': 3.0, 'width': 3},
    'genre_transformation': {'height': 5.0, 'width': 5},
    'paradigm_shift': {'height': 10.0, 'width': 10},
}

print("  Creative act → Tunneling probability at different ε:")
for name, barrier in barriers.items():
    print(f"  {name:25s}:", end="")
    for eps in [0.5, 1.0, 2.0, 5.0]:
        p = tunneling_probability(barrier['height'], barrier['width'], eps)
        print(f" ε={eps:.1f}:{p:.4f}", end="")
    print()

# Part 5: Grover's algorithm for creative search
print("\n--- Part 5: Creative Search (Grover-like) ---")
# Grover's algorithm: search N items in O(√N) steps
# Creative analog: finding the "best" idea in a space of N ideas

N_search = 1024  # creative possibilities
n_target = 1  # one "good" idea

classical_steps = N_search / 2  # average
grover_steps = int(np.pi / 4 * np.sqrt(N_search))

print(f"  Search space: {N_search} ideas")
print(f"  Classical search: ~{classical_steps:.0f} steps")
print(f"  Grover-like search: ~{grover_steps} steps")
print(f"  Speedup: {classical_steps/grover_steps:.1f}×")

# Simulate: constraint system as amplitude amplification
print("\n  Constraint-as-amplitude-amplification:")
for n_iterations in [1, 5, 10, grover_steps, 50]:
    # Each iteration amplifies "good" ideas
    amplitudes = np.ones(N_search)
    target = 42  # the "good" idea
    
    for _ in range(n_iterations):
        # Oracle: mark target
        amplitudes[target] *= -1
        # Diffusion: invert about mean
        mean = np.mean(amplitudes)
        amplitudes = 2 * mean - amplitudes
    
    probs = amplitudes**2
    probs = np.abs(probs)
    probs /= probs.sum()
    target_prob = probs[target]
    
    print(f"    {n_iterations:3d} iterations: P(good idea) = {target_prob:.4f} ({target_prob*100:.1f}%)")

with open('CODE/EXPERIMENT-QUANTUM-CREATIVITY.json', 'w') as f:
    json.dump({
        'tunneling': {k: tunneling_probability(v['height'], v['width'], 1.0) for k, v in barriers.items()},
        'grover_speedup': classical_steps / grover_steps,
    }, f, indent=2)

print("\n=== QUANTUM CREATIVITY: SUPERPOSITION, ENTANGLEMENT, TUNNELING, SEARCH ===")
