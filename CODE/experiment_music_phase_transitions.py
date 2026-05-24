import numpy as np
import json

print("=== Experiment 39: Phase Transitions in Musical Structures ===\n")

np.random.seed(42)

# Part 1: Simulate different musical styles as different ρ regimes
print("--- Part 1: Musical Styles as Lorenz Regimes ---")

styles = {
    'Gregorian Chant': {'rho': 3, 'sigma': 5, 'description': 'Minimal ornamentation, single line'},
    'Bach Fugue': {'rho': 15, 'sigma': 10, 'description': 'Structured but with freedom'},
    'Mozart Sonata': {'rho': 18, 'sigma': 10, 'description': 'Balanced, periodic'},
    'Beethoven (late)': {'rho': 25, 'sigma': 10, 'description': 'Pushing into chaos'},
    'Coltrane (Giant Steps)': {'rho': 35, 'sigma': 12, 'description': 'Harmonic chaos, rhythmic order'},
    'Cecil Taylor (free jazz)': {'rho': 45, 'sigma': 15, 'description': 'Full chaos'},
    'Xenakis': {'rho': 55, 'sigma': 15, 'description': 'Stochastic, mathematical'},
    'Drone music': {'rho': 1, 'sigma': 3, 'description': 'Fixed point, minimal'},
}

N = 200
dt = 0.01

for style, params in styles.items():
    state = np.random.randn(N, 3) * 0.1
    outputs = []
    
    for step in range(8000):
        x, y, z = state[:, 0], state[:, 1], state[:, 2]
        dx = params['sigma'] * (y - x)
        dy = x * (params['rho'] - z) - y
        dz = x * y - 8/3 * z
        state += np.column_stack([dx, dy, dz]) * dt
        
        if step > 4000:
            outputs.append(float(np.mean(state[:, 0])))
    
    outputs = np.array(outputs)
    var = np.var(outputs)
    std = np.std(outputs)
    
    # Autocorrelation (structure measure)
    ac = np.corrcoef(outputs[:-1], outputs[1:])[0, 1]
    
    # Spectral entropy (complexity measure)
    fft = np.abs(np.fft.rfft(outputs))
    fft_norm = fft / (fft.sum() + 1e-10)
    spec_entropy = -np.sum([p * np.log(p) for p in fft_norm if p > 0])
    max_entropy = np.log(len(fft_norm))
    norm_entropy = spec_entropy / max_entropy
    
    regime = "FIXED" if params['rho'] < 5 else "PERIODIC" if params['rho'] < 24.74 else "CHAOTIC"
    
    print(f"  {style:25s} (ρ={params['rho']:3d}): σ={std:.3f}, AC={ac:.3f}, "
          f"entropy={norm_entropy:.3f}, regime={regime}")

# Part 2: Transition within a piece (development section)
print("\n--- Part 2: Simulated Development Section ---")
# Classical sonata: exposition (ordered) → development (chaotic) → recapitulation (ordered)

N = 300
total_steps = 30000

# ρ trajectory: low → high → low
rho_traj = np.concatenate([
    np.linspace(10, 10, total_steps // 3),      # Exposition
    np.linspace(10, 40, total_steps // 3),       # Development (phase transition!)
    np.linspace(40, 10, total_steps // 3),       # Recapitulation
])

state = np.random.randn(N, 3) * 0.1
outputs = []
section_labels = []

for step in range(total_steps):
    rho = rho_traj[step]
    x, y, z = state[:, 0], state[:, 1], state[:, 2]
    dx = 10 * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - 8/3 * z
    state += np.column_stack([dx, dy, dz]) * dt
    
    if step % 100 == 0:
        outputs.append(float(np.std(state[:, 0])))
        if step < total_steps // 3:
            section_labels.append('exposition')
        elif step < 2 * total_steps // 3:
            section_labels.append('development')
        else:
            section_labels.append('recapitulation')

outputs = np.array(outputs)

print(f"  Exposition: diversity={np.mean([o for o, l in zip(outputs, section_labels) if l=='exposition']):.4f}")
print(f"  Development: diversity={np.mean([o for o, l in zip(outputs, section_labels) if l=='development']):.4f}")
print(f"  Recapitulation: diversity={np.mean([o for o, l in zip(outputs, section_labels) if l=='recapitulation']):.4f}")

# Find the phase transition moment
expo_divs = [o for o, l in zip(outputs, section_labels) if l == 'exposition']
dev_divs = [o for o, l in zip(outputs, section_labels) if l == 'development']
trans_ratio = np.mean(dev_divs) / np.mean(expo_divs) if np.mean(expo_divs) > 0 else 0
print(f"  Development/Exposition ratio: {trans_ratio:.1f}×")
print(f"  Phase transition: {'DRAMATIC' if trans_ratio > 3 else 'gradual'}")

# Part 3: Musical tension curve
print("\n--- Part 3: Musical Tension as Divergence from Attractor ---")

# Tension = how far the system is from its "home" attractor
# In music: dissonance, modulation, rhythmic complexity

N = 200
state = np.random.randn(N, 3) * 0.1
rho_home = 15  # "home key"

# Simulate: modulation (ρ change) and return
modulations = [
    ('Home (tonic)', 15),
    ('Subdominant', 18),
    ('Dominant', 22),
    ('Distant key', 35),
    ('Maximum tension', 45),
    ('Resolution', 20),
    ('Home (tonic)', 15),
]

for label, rho in modulations:
    # Set ρ and run for a bit
    for step in range(2000):
        x, y, z = state[:, 0], state[:, 1], state[:, 2]
        dx = 10 * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - 8/3 * z
        state += np.column_stack([dx, dy, dz]) * dt
    
    tension = float(np.std(state[:, 0]))
    distance_from_home = float(np.mean(np.abs(state[:, 0] - np.mean(state[:, 0] / (np.std(state[:, 0]) + 1)))))
    
    print(f"  {label:20s} (ρ={rho:3d}): tension={tension:.4f}")

# Part 4: Rhythm as phase locking
print("\n--- Part 4: Rhythm as Phase Locking ---")

# Multiple metronomes on a shared surface
n_metro = 6
natural_freqs = np.array([1.0, 1.02, 0.98, 1.05, 0.97, 1.01])  # slightly different
phases = np.random.uniform(0, 2*np.pi, n_metro)

# Coupling through shared surface
for K in [0.0, 0.1, 0.5, 1.0, 5.0]:
    phases = np.random.uniform(0, 2*np.pi, n_metro)
    for step in range(10000):
        z = np.mean(np.exp(1j * phases))
        phases += (natural_freqs + K * np.imag(z * np.exp(-1j * phases))) * 0.01
    
    order = float(np.abs(np.mean(np.exp(1j * phases))))
    
    # Musical interpretation
    if order > 0.95:
        groove = "TIGHT groove (funk, electronic)"
    elif order > 0.8:
        groove = "Good feel (jazz, rock)"
    elif order > 0.5:
        groove = "Loose (free jazz, avant-garde)"
    else:
        groove = "No groove (chaos)"
    
    print(f"  K={K:.1f}: order={order:.4f} → {groove}")

# Part 5: Genre as basin of attraction
print("\n--- Part 5: Genre as Basin of Attraction ---")

genres = {
    'Blues': {'rho': 20, 'sigma': 8},
    'Jazz': {'rho': 28, 'sigma': 10},
    'Classical': {'rho': 15, 'sigma': 10},
    'Electronic': {'rho': 30, 'sigma': 8},
}

# Start from random initial conditions, see which genre it's closest to
for trial in range(5):
    state = np.random.randn(100, 3) * 5  # random start
    
    # Run for a bit
    for step in range(3000):
        x, y, z = state[:, 0], state[:, 1], state[:, 2]
        dx = 10 * (y - x)
        dy = x * (25 - z) - y  # middle-of-road ρ
        dz = x * y - 8/3 * z
        state += np.column_stack([dx, dy, dz]) * dt
    
    final_std = float(np.std(state[:, 0]))
    
    # Which genre is this closest to?
    # (In a real system, you'd use more sophisticated comparison)
    if final_std < 3:
        closest = 'Classical'
    elif final_std < 6:
        closest = 'Blues'
    elif final_std < 10:
        closest = 'Jazz'
    else:
        closest = 'Electronic'
    
    print(f"  Trial {trial+1}: diversity={final_std:.3f} → attracted to {closest}")

with open('CODE/EXPERIMENT-MUSIC-PHASE-TRANSITIONS.json', 'w') as f:
    json.dump({
        'development_ratio': float(trans_ratio),
        'style_regimes': {k: v['rho'] for k, v in styles.items()},
    }, f, indent=2)

print("\n=== MUSIC IS PHASE TRANSITIONS BETWEEN CREATIVE REGIMES ===")
