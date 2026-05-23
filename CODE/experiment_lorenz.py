import numpy as np
import json
from scipy.integrate import solve_ivp

print("=== Lorenz Attractor = Creative Manifold ===\n")

# Part 1: Integrate Lorenz equations at different ρ (stress)
print("--- Part 1: Lorenz Regimes ---")

def lorenz(t, state, sigma, rho, beta):
    x, y, z = state
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]

sigma = 10.0
beta = 8.0 / 3.0

for rho in [0.5, 1.0, 10.0, 24.0, 28.0, 50.0]:
    sol = solve_ivp(lorenz, [0, 50], [1.0, 1.0, 1.0], 
                    args=(sigma, rho, beta), max_step=0.01, dense_output=True)
    
    t = np.linspace(10, 50, 4000)  # skip transient
    xyz = sol.sol(t)
    
    x, y, z = xyz[0], xyz[1], xyz[2]
    
    # Measure regime
    x_std = np.std(x)
    x_range = np.max(x) - np.min(x)
    
    # Count zero crossings (proxy for period)
    crossings = np.sum(np.diff(np.sign(x)) != 0)
    
    # Check for chaos: is the trajectory bounded but non-periodic?
    if x_range < 0.1:
        regime = "FIXED POINT (no creativity)"
    elif crossings < 20:
        regime = "PERIODIC (repetitive creativity)"
    else:
        regime = "CHAOTIC (genuine creativity)"
    
    print(f"  ρ={rho:5.1f}: range={x_range:.2f}, crossings={crossings:4d}, regime={regime}")

# Part 2: Find the critical ρ
print("\n--- Part 2: Critical Stress Level ---")
rho_c = sigma * (sigma + beta + 3) / (sigma - beta - 1)
print(f"  Analytical ρ_c = σ(σ+β+3)/(σ-β-1) = {rho_c:.4f}")
print(f"  σ={sigma}, β={beta:.4f}")
print(f"  Below ρ_c: periodic (safe, conventional)")
print(f"  Above ρ_c: chaotic (creative, unpredictable)")
print(f"  The creative sweet spot is JUST above ρ_c")

# Part 3: Lyapunov exponent (measures non-pre-calculability)
print("\n--- Part 3: Lyapunov Exponent ---")

def lorenz_with_tangent(t, state, sigma, rho, beta):
    """Lorenz + tangent vector for Lyapunov computation."""
    x, y, z = state[:3]
    dx = [sigma*(y-x), x*(rho-z)-y, x*y - beta*z]
    
    # Jacobian
    J = [[-sigma, sigma, 0],
         [rho-z, -1, -x],
         [y, x, -beta]]
    
    # Tangent evolution
    dtx, dty, dtz = state[3], state[4], state[5]
    dtdx = J[0][0]*dtx + J[0][1]*dty + J[0][2]*dtz
    dtdy = J[1][0]*dtx + J[1][1]*dty + J[1][2]*dtz
    dtdz = J[2][0]*dtx + J[2][1]*dty + J[2][2]*dtz
    
    return dx + [dtdx, dtdy, dtdz]

for rho in [10, 20, 28, 50]:
    # Initial condition + random tangent
    state0 = [1.0, 1.0, 1.0, 0.1, 0.1, 0.1]
    
    lyap_sum = 0
    n_steps = 100
    dt = 1.0
    
    state = np.array(state0, dtype=float)
    for step in range(n_steps):
        sol = solve_ivp(lorenz_with_tangent, [0, dt], state,
                       args=(sigma, rho, beta), max_step=0.01)
        state = sol.y[:, -1]
        
        tangent = state[3:6]
        norm = np.linalg.norm(tangent)
        if norm > 0:
            lyap_sum += np.log(norm)
            state[3:6] /= norm  # renormalize
    
    lyapunov = lyap_sum / (n_steps * dt)
    predictability = 1.0 / lyapunov if lyapunov > 0 else float('inf')
    
    print(f"  ρ={rho:5.1f}: λ={lyapunov:.4f}, predictability horizon={predictability:.2f} time units")

# Part 4: Feigenbaum period doubling in creative systems
print("\n--- Part 4: Period Doubling Route to Chaos ---")
# Track period by counting distinct peaks
for rho in np.arange(24.0, 29.0, 0.2):
    sol = solve_ivp(lorenz, [0, 100], [1.0, 1.0, 1.0],
                    args=(sigma, rho, beta), max_step=0.01)
    
    x = sol.y[0, 5000:]  # skip transient
    z = sol.y[2, 5000:]
    
    # Find peaks in z (the "butterfly wing" indicator)
    peaks = []
    for i in range(1, len(z)-1):
        if z[i] > z[i-1] and z[i] > z[i+1]:
            peaks.append(z[i])
    
    # Count distinct peak heights
    if peaks:
        peaks = np.array(peaks)
        # Cluster peaks
        sorted_peaks = np.sort(peaks)
        n_clusters = 1
        threshold = 0.5
        for i in range(1, len(sorted_peaks)):
            if sorted_peaks[i] - sorted_peaks[i-1] > threshold:
                n_clusters += 1
    else:
        n_clusters = 0
    
    print(f"  ρ={rho:.1f}: {n_clusters} distinct peak heights")

# Part 5: Fractal dimension
print("\n--- Part 5: Fractal Dimension of Creative Space ---")
# Kaplan-Yorke dimension for Lorenz: D_KY ≈ 2.06 for ρ=28
# For general ρ, compute from Lyapunov spectrum

for rho in [28]:
    sol = solve_ivp(lorenz, [0, 200], [1.0, 1.0, 1.0],
                    args=(sigma, rho, beta), max_step=0.01)
    
    x = sol.y[0, 10000:]  # skip transient
    
    # Estimate correlation dimension
    # Sample random pairs and measure distances
    n_samples = min(5000, len(x))
    indices = np.random.choice(len(x), n_samples, replace=False)
    points = np.stack([sol.y[0, indices], sol.y[1, indices], sol.y[2, indices]], axis=1)
    
    from scipy.spatial.distance import pdist
    distances = pdist(points)
    
    # Box counting: how many balls of radius r cover the points?
    for r in [0.5, 1.0, 2.0, 5.0]:
        n_balls = 0
        covered = np.zeros(len(points), dtype=bool)
        while not covered.all():
            # Find uncovered point
            seed = np.argmax(~covered)
            dists = np.linalg.norm(points - points[seed], axis=1)
            covered |= (dists < r)
            n_balls += 1
        
        print(f"  r={r:.1f}: {n_balls} balls needed to cover attractor")

# Part 6: Creative mapping
print("\n--- Part 6: Lorenz ↔ Constraint Theory Mapping ---")
print("  σ (coupling)    → consensus strength (how fast agents sync)")
print("  ρ (stress×free) → crucible parameter (stress × ε)")
print("  β (dissipation) → constraint absorption (how fast structure forms)")
print("  ρ < 1           → fixed point: no creativity, one answer")
print("  1 < ρ < ρ_c    → periodic: conventional creativity, genres")
print("  ρ > ρ_c        → chaotic: genuine creativity, strange attractor")
print("  ρ_c             → the creative phase transition")
print("  λ > 0           → non-pre-calculability (Lyapunov)")
print("  D ≈ 2.06        → fractal creative space")

with open('EXPERIMENT-LORENZ.json', 'w') as f:
    json.dump({'rho_critical': rho_c, 'sigma': sigma, 'beta': beta}, f, indent=2)

print("\n=== THE LORENZ ATTRACTOR IS THE SHAPE OF CREATIVITY ===")
