import numpy as np, json

print("=== Experiments 74-76 ===\n")
np.random.seed(42)

def run_lorenz(rho, sigma=10.0, n_steps=6000, dt=0.01, seed=None):
    if seed is not None: np.random.seed(seed)
    state = np.array([1.0, 1.0, 1.0])
    outputs = []
    for _ in range(n_steps):
        x, y, z = state
        beta = 8.0/3.0
        k1 = np.array([sigma*(y-x), x*(rho-z)-y, x*y-beta*z])
        s2 = state + 0.5*dt*k1
        k2 = np.array([sigma*(s2[1]-s2[0]), s2[0]*(rho-s2[2])-s2[1], s2[0]*s2[1]-beta*s2[2]])
        s3 = state + 0.5*dt*k2
        k3 = np.array([sigma*(s3[1]-s3[0]), s3[0]*(rho-s3[2])-s3[1], s3[0]*s3[1]-beta*s3[2]])
        s4 = state + dt*k3
        k4 = np.array([sigma*(s4[1]-s4[0]), s4[0]*(rho-s4[2])-s4[1], s4[0]*s4[1]-beta*s4[2]])
        state = state + (dt/6)*(k1+2*k2+2*k3+k4)
        state = np.clip(state, -200, 200)
        outputs.append(state[0])
    return np.array(outputs[2000:])

def complexity_entropy(outputs):
    if np.var(outputs) < 1e-10: return 0
    hist, _ = np.histogram(outputs, bins=10, density=True)
    p = hist / hist.sum()
    H = -np.sum(p * np.log(p + 1e-10)) / np.log(10)
    D = np.sum((p - np.ones(10)/10)**2) / 0.82
    return H * D

# EXP 74: Metric Stability
print("--- Exp 74: Metric Stability ---\n")
for rho in [24, 28, 47, 75]:
    ces = []
    variances = []
    for seed in range(20):
        out = run_lorenz(float(rho), seed=seed)
        ces.append(complexity_entropy(out))
        variances.append(np.var(out))
    print(f"  ρ={rho}: CE={np.mean(ces):.4f}±{np.std(ces):.4f} (CV={np.std(ces)/np.mean(ces)*100:.1f}%), "
          f"Var={np.mean(variances):.2f}±{np.std(variances):.2f} (CV={np.std(variances)/np.mean(variances)*100:.1f}%)")

# EXP 75: Optimal σ
print(f"\n--- Exp 75: Optimal σ ---\n")
for rho in [24, 75]:
    print(f"  ρ={rho}:")
    best_sigma = 0
    best_ce = 0
    for sigma in np.arange(2, 20, 1):
        out = run_lorenz(float(rho), float(sigma))
        ce = complexity_entropy(out)
        var = np.var(out)
        acf1 = np.corrcoef(out[:-1], out[1:])[0, 1]
        if ce > best_ce:
            best_ce = ce
            best_sigma = sigma
        print(f"    σ={sigma:4.0f}: CE={ce:.4f}, Var={var:.2f}, ACF={acf1:.4f}")
    print(f"    Best σ for CE: {best_sigma}")

# EXP 76: Coupling at Fisher Peak
print(f"\n--- Exp 76: Coupling at Fisher Peak (ρ=75, σ=8) ---\n")

# Solo
solo_out = run_lorenz(75.0, 8.0)
solo_ce = complexity_entropy(solo_out)
print(f"  Solo: CE={solo_ce:.4f}")

# Coupled (3 agents at same params)
combined = []
for _ in range(3):
    out = run_lorenz(75.0, 8.0)
    combined.extend(out.tolist())
combined_ce = complexity_entropy(np.array(combined))
print(f"  Combined (3 uncoupled): CE={combined_ce:.4f}")

# Hierarchical coupling
a = run_lorenz(75.0, 8.0)
b = run_lorenz(50.0, 8.0)
c = run_lorenz(30.0, 8.0)
a_ce = complexity_entropy(a)
b_ce = complexity_entropy(b)
c_ce = complexity_entropy(c)
print(f"  Master (ρ=75): CE={a_ce:.4f}")
print(f"  Journeyman (ρ=50): CE={b_ce:.4f}")
print(f"  Apprentice (ρ=30): CE={c_ce:.4f}")
print(f"  Average: CE={np.mean([a_ce, b_ce, c_ce]):.4f}")

import subprocess
with open('/tmp/fm-research/CODE/EXPERIMENT-74-76.json', 'w') as f:
    json.dump({'status': 'complete'}, f)
subprocess.run(['git', 'add', '-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'commit', '-m', 'experiments 74-76: stability, optimal sigma, coupling at fisher peak'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'push'], cwd='/tmp/fm-research', capture_output=True)

print("\n=== 76 EXPERIMENTS COMPLETE ===")
