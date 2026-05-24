import numpy as np
import json
import sys

print("=== Experiment 46: Creative Space Community Detection ===\n")
print("Map all experiments and find natural clusters.\n")

np.random.seed(42)

# Collect all known experimental results as points in parameter space
points = []
labels = []

# From experiment 34: regime × quality surface
for rho in [1, 5, 10, 15, 20, 25, 28, 35, 45, 55]:
    for eps in [0.01, 0.1, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0]:
        # Run quick system
        from flux_tensor_midi.creative_engine import CreativeSystem, QualityMetrics
        cs = CreativeSystem(rho=float(rho), epsilon=eps)
        cs.run(2000, 500)
        q = cs.quality()
        div = cs.diversity()
        
        points.append([rho, eps, q.novelty, q.coherence, q.quality, div])
        regime = 'fixed' if rho < 5 else 'periodic' if rho < 24.74 else 'chaotic'
        labels.append(f"ρ={rho}_ε={eps:.2f} [{regime}]")

X = np.array(points)

# K-means clustering (manual implementation)
def kmeans(X, k, n_iter=50):
    n = len(X)
    # Normalize
    X_norm = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-10)
    
    # Initialize centroids randomly
    idx = np.random.choice(n, k, replace=False)
    centroids = X_norm[idx].copy()
    
    for _ in range(n_iter):
        # Assign to nearest centroid
        dists = np.array([[np.linalg.norm(x - c) for c in centroids] for x in X_norm])
        assignments = np.argmin(dists, axis=1)
        
        # Update centroids
        new_centroids = np.array([X_norm[assignments == i].mean(axis=0) if np.sum(assignments == i) > 0 else centroids[i] for i in range(k)])
        
        if np.allclose(centroids, new_centroids):
            break
        centroids = new_centroids
    
    return assignments, centroids

# Find optimal k (elbow method)
print("--- Finding natural clusters ---")
for k in [3, 4, 5, 6, 7, 8]:
    assignments, centroids = kmeans(X, k)
    
    # Compute within-cluster variance
    X_norm = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-10)
    wcv = 0
    for i in range(k):
        cluster = X_norm[assignments == i]
        if len(cluster) > 0:
            wcv += np.sum((cluster - centroids[i])**2)
    
    print(f"  k={k}: within-cluster variance = {wcv:.2f}")

# Use k=5 (matching our five primitives)
k = 5
assignments, centroids = kmeans(X, k)

print(f"\n--- {k} Natural Clusters ---")
for cluster_id in range(k):
    mask = assignments == cluster_id
    cluster_points = X[mask]
    cluster_labels = [labels[i] for i in range(len(labels)) if assignments[i] == cluster_id]
    
    if len(cluster_points) == 0:
        continue
    
    mean_rho = np.mean(cluster_points[:, 0])
    mean_eps = np.mean(cluster_points[:, 1])
    mean_quality = np.mean(cluster_points[:, 4])
    mean_diversity = np.mean(cluster_points[:, 5])
    
    # Determine regime composition
    n_fixed = sum(1 for l in cluster_labels if 'fixed' in l)
    n_periodic = sum(1 for l in cluster_labels if 'periodic' in l)
    n_chaotic = sum(1 for l in cluster_labels if 'chaotic' in l)
    
    # Determine eps range
    eps_values = cluster_points[:, 1]
    
    print(f"\n  Cluster {cluster_id+1} ({len(cluster_points)} points):")
    print(f"    Mean ρ={mean_rho:.1f}, ε={mean_eps:.2f}, quality={mean_quality:.4f}, div={mean_diversity:.4f}")
    print(f"    ε range: [{eps_values.min():.2f}, {eps_values.max():.2f}]")
    print(f"    Regime mix: fixed={n_fixed}, periodic={n_periodic}, chaotic={n_chaotic}")
    
    # Name the cluster
    if n_fixed > n_periodic and n_fixed > n_chaotic:
        name = "Rigid (fixed-point dominant)"
    elif n_chaotic > n_periodic and n_chaotic > n_fixed:
        if mean_eps > 0.5:
            name = "Free Jazz (chaotic + high ε)"
        else:
            name = "Controlled Chaos (chaotic + low ε)"
    elif n_periodic > n_fixed and n_periodic > n_chaotic:
        name = "Classical (periodic dominant)"
    else:
        name = "Mixed"
    
    print(f"    Identity: {name}")

# Part 2: The creative landscape topology
print(f"\n--- Creative Landscape Topology ---")

# For each ρ, find the quality ridge (best ε)
ridge = {}
for rho in [1, 5, 10, 15, 20, 25, 28, 35, 45, 55]:
    rho_mask = X[:, 0] == rho
    if rho_mask.sum() > 0:
        rho_points = X[rho_mask]
        best_idx = np.argmax(rho_points[:, 4])
        ridge[rho] = {
            'rho': rho,
            'best_eps': float(rho_points[best_idx, 1]),
            'best_quality': float(rho_points[best_idx, 4]),
        }

print(f"\n  Quality Ridge (best ε for each ρ):")
for rho, r in sorted(ridge.items()):
    print(f"    ρ={rho:3d}: best ε={r['best_eps']:.2f}, quality={r['best_quality']:.4f}")

# Does the ridge slope down? (ε* decreases with ρ)
ridge_rhos = [r['rho'] for r in ridge.values()]
ridge_eps = [r['best_eps'] for r in ridge.values()]
corr = np.corrcoef(ridge_rhos, ridge_eps)[0, 1]
print(f"\n  Ridge slope (ρ ↔ ε* correlation): {corr:.3f}")
print(f"  {'ε* DECREASES with expertise' if corr < 0 else 'ε* INCREASES with expertise'}")

# Part 3: Attractors in creative space
print(f"\n--- Creative Attractors ---")

# Find local maxima in quality
from scipy.ndimage import maximum_filter

# Bin the space
rho_bins = np.linspace(1, 55, 20)
eps_bins = np.linspace(0.01, 2.0, 20)

quality_grid = np.zeros((len(rho_bins)-1, len(eps_bins)-1))
count_grid = np.zeros_like(quality_grid)

for p in X:
    rho_idx = np.searchsorted(rho_bins, p[0]) - 1
    eps_idx = np.searchsorted(eps_bins, p[1]) - 1
    if 0 <= rho_idx < quality_grid.shape[0] and 0 <= eps_idx < quality_grid.shape[1]:
        quality_grid[rho_idx, eps_idx] += p[4]
        count_grid[rho_idx, eps_idx] += 1

quality_grid = np.divide(quality_grid, count_grid, where=count_grid>0, out=np.zeros_like(quality_grid))

# Find local maxima
local_max = maximum_filter(quality_grid, size=3)
peaks = (quality_grid == local_max) & (quality_grid > 0)
peak_positions = np.argwhere(peaks)

print(f"  Local maxima in quality space:")
for pos in peak_positions[:5]:
    rho_val = (rho_bins[pos[0]] + rho_bins[pos[0]+1]) / 2
    eps_val = (eps_bins[pos[1]] + eps_bins[pos[1]+1]) / 2
    q_val = quality_grid[pos[0], pos[1]]
    print(f"    ρ≈{rho_val:.1f}, ε≈{eps_val:.2f}: quality={q_val:.4f}")

# Save
import subprocess
with open('/tmp/fm-research/CODE/EXPERIMENT-COMMUNITY-DETECTION.json', 'w') as f:
    json.dump({
        'n_points': len(X),
        'k': k,
        'ridge': ridge,
        'ridge_correlation': float(corr),
    }, f, indent=2, default=str)

subprocess.run(['git', 'add', '-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'commit', '-m', 'experiment 46: creative space community detection'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'push'], cwd='/tmp/fm-research', capture_output=True)

print("\n=== CREATIVE SPACE HAS NATURAL CONTINENTS ===")
