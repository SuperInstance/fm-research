import numpy as np
import json

print("=== Chladni Patterns in Constraint Systems ===\n")

# A Chladni pattern emerges when:
# 1. A 2D plate vibrates at frequency f
# 2. Sand collects at NODES (zero displacement)
# 3. The pattern depends on f and the plate geometry

# For constraint systems:
# The "plate" = the constraint manifold
# The "frequency" = the constraint strength
# The "sand" = creative output
# The "nodes" = stable configurations where output collects

# Part 1: 2D constraint plate simulation
print("--- Part 1: Constraint Plate Chladni Patterns ---")
N = 50  # grid size
x = np.linspace(-1, 1, N)
y = np.linspace(-1, 1, N)
X, Y = np.meshgrid(x, y)

# Different "vibration modes" of the constraint plate
modes = {
    'fundamental': (0, 1),  # one axis
    'first_overtone': (1, 1),  # diagonal
    'second_overtone': (2, 1),  # triple
    'complex': (2, 3),  # higher mode
}

from scipy import ndimage

for name, (m, n) in modes.items():
    # Standing wave pattern
    Z = np.sin(m * np.pi * X) * np.sin(n * np.pi * Y)
    
    # Find nodal lines (where |Z| < threshold)
    nodes = np.abs(Z) < 0.1
    
    # Count distinct regions (creative attractors)
    labeled, n_regions = ndimage.label(nodes)
    
    # Measure pattern complexity
    node_fraction = np.sum(nodes) / nodes.size
    
    print(f"  {name} (m={m}, n={n}): {n_regions} regions, {node_fraction:.1%} nodal area")

# Part 2: Genre Chladni patterns
print("\n--- Part 2: Genre Chladni Patterns ---")
# Each genre creates a different vibration pattern on the constraint plate
# The "sand" (musical output) collects at different nodes

genre_modes = {
    'jazz': (3, 2, 0.5),       # complex, high ε
    'classical': (1, 1, 0.1),   # simple, low ε  
    'blues': (2, 1, 0.3),       # moderate complexity
    'electronic': (5, 4, 0.7),  # very complex, high ε
    'ambient': (1, 2, 0.9),     # sparse, very high ε
    'metal': (4, 3, 0.05),      # complex, very low ε
}

for genre, (m, n, eps) in genre_modes.items():
    Z = np.sin(m * np.pi * X) * np.sin(n * np.pi * Y)
    # ε adds noise/chaos to the pattern
    Z += eps * np.random.randn(N, N)
    
    nodes = np.abs(Z) < (0.1 + eps * 0.5)
    labeled, n_regions = ndimage.label(nodes)
    node_fraction = np.sum(nodes) / nodes.size
    
    print(f"  {genre:12s}: {n_regions:3d} creative attractors, {node_fraction:.1%} stable area")

# Part 3: Phase transition in patterns
print("\n--- Part 3: Phase Transition in Creative Patterns ---")
# As constraint strength increases, patterns undergo bifurcations
for constraint_strength in np.arange(0.1, 5.1, 0.5):
    m = max(1, int(constraint_strength))
    n = max(1, int(constraint_strength * 0.7))
    eps = 0.3 / constraint_strength  # ε inversely proportional to constraint
    
    Z = np.sin(m * np.pi * X) * np.sin(n * np.pi * Y) + eps * np.random.randn(N, N)
    nodes = np.abs(Z) < 0.15
    labeled, n_regions = ndimage.label(nodes)
    
    print(f"  constraint={constraint_strength:.1f}: mode ({m},{n}), {n_regions:3d} regions, ε={eps:.3f}")

# Part 4: The creative Chladni theorem
print("\n--- Part 4: Creative Chladni Theorem ---")
print("For a constraint system with m constraints and ε freedom:")
print("  Number of creative attractors ≈ m × n (product of mode numbers)")
print("  Stability of each attractor ≈ 1/ε (inversely proportional to freedom)")
print("  Total creative output ∝ attractors × stability = (m×n) / ε")
print("  Maximum creativity at intermediate constraint (inverted-U from Chladni!)")

# Part 5: Find the most creative constraint configuration
print("\n--- Part 5: Finding Maximum Creativity ---")
best_creativity = 0
best_config = None

for m in range(1, 8):
    for n in range(1, 8):
        for eps in [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0]:
            Z = np.sin(m * np.pi * X) * np.sin(n * np.pi * Y) + eps * np.random.randn(N, N)
            nodes = np.abs(Z) < (0.1 + eps * 0.3)
            labeled, n_regions = ndimage.label(nodes)
            
            # Creativity = regions × stability / noise
            stability = 1.0 / (eps + 0.01)
            creativity = n_regions * stability / (1 + eps * 10)
            
            if creativity > best_creativity:
                best_creativity = creativity
                best_config = (m, n, eps, n_regions)

m, n, eps, regions = best_config
print(f"  Best: mode ({m},{n}), ε={eps:.2f}, {regions} attractors, creativity={best_creativity:.1f}")
print(f"  This is the Chladni sweet spot!")

# Save results
with open('EXPERIMENT-CHLADNI.json', 'w') as f:
    json.dump({'best_config': best_config, 'best_creativity': best_creativity}, f)
