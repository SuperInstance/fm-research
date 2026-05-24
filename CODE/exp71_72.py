import numpy as np, json

print("=== Experiments 71-72: Cross-Scale Correlation + Disagreement Zone ===\n")
np.random.seed(42)

def run_lorenz(rho, sigma=10.0, n_steps=8000, dt=0.01):
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
    return np.array(outputs[3000:])

def complexity_entropy(outputs):
    if np.var(outputs) < 1e-10: return 0
    hist, _ = np.histogram(outputs, bins=10, density=True)
    p = hist / hist.sum()
    H = -np.sum(p * np.log(p + 1e-10)) / np.log(10)
    D = np.sum((p - np.ones(10)/10)**2) / 0.82
    return H * D

def fisher_info(rho, sigma=10.0, delta=0.1):
    out1 = run_lorenz(rho, sigma)
    out2 = run_lorenz(rho + delta, sigma)
    bins = np.linspace(-50, 50, 80)
    p1, _ = np.histogram(out1, bins=bins, density=True)
    p2, _ = np.histogram(out2, bins=bins, density=True)
    p1 = p1/p1.sum()+1e-10; p2 = p2/p2.sum()+1e-10
    return 2*np.sum(p1*np.log(p1/p2))/delta**2

def consonance(outputs):
    cof = [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5]
    x = outputs
    angles = np.arctan2(x - np.mean(x), np.std(x))
    pcs = np.array([cof[int(((a + np.pi) / (2*np.pi) * 12)) % 12] for a in angles[::10]])
    intervals = np.abs(np.diff(pcs))
    consonant = [0, 3, 4, 5, 7, 8, 9]
    ic = np.bincount(intervals, minlength=12)
    return sum(ic[i] for i in consonant) / len(intervals)

def spectral_richness(outputs):
    fft = np.fft.rfft(outputs - np.mean(outputs))
    power = np.abs(fft[1:])**2
    return np.sum(power > np.max(power)*0.01) if np.max(power) > 0 else 0

# Compute all metrics
print("--- Computing All Metrics ---\n")
rho_vals = np.arange(5, 81, 2.5)
data = []

for rho in rho_vals:
    outputs = run_lorenz(float(rho))
    ce = complexity_entropy(outputs)
    fi = fisher_info(float(rho))
    var = np.var(outputs)
    cons = consonance(outputs)
    sr = spectral_richness(outputs)
    raw_q = var
    
    data.append({
        'rho': float(rho), 'ce': ce, 'fisher': fi,
        'variance': var, 'consonance': cons,
        'spectral_richness': sr, 'raw_quality': var
    })

# Experiment 71: Correlation matrix
print("--- Experiment 71: Metric Correlations ---\n")
metrics = ['ce', 'fisher', 'variance', 'consonance', 'spectral_richness']
print(f"  {'':15s}", end="")
for m in metrics:
    print(f"  {m[:8]:>8s}", end="")
print()

for m1 in metrics:
    print(f"  {m1:15s}", end="")
    for m2 in metrics:
        v1 = [d[m1] for d in data]
        v2 = [d[m2] for d in data]
        c = np.corrcoef(v1, v2)[0, 1]
        print(f"  {c:8.3f}", end="")
    print()

# Find most disagreeing pair
print(f"\n  Most disagreeing metric pairs:")
pairs = []
for i, m1 in enumerate(metrics):
    for j, m2 in enumerate(metrics):
        if j > i:
            v1 = [d[m1] for d in data]
            v2 = [d[m2] for d in data]
            c = abs(np.corrcoef(v1, v2)[0, 1])
            pairs.append((m1, m2, c))
pairs.sort(key=lambda x: x[2])
for m1, m2, c in pairs[:5]:
    print(f"    {m1:20s} <-> {m2:20s}: r={c:.3f}")

# Experiment 72: Disagreement zone
print(f"\n--- Experiment 72: Disagreement Zone ---\n")

for m in metrics:
    vals = [d[m] for d in data]
    vmin, vmax = min(vals), max(vals)
    for d in data:
        d[f'{m}_norm'] = (d[m] - vmin) / (vmax - vmin + 1e-10)

for d in data:
    norm_vals = [d[f'{m}_norm'] for m in metrics]
    d['disagreement'] = float(np.std(norm_vals))

disagree_sorted = sorted(data, key=lambda d: -d['disagreement'])

print(f"  Top 10 disagreement zones:")
for d in disagree_sorted[:10]:
    print(f"    rho={d['rho']:5.1f}: disagreement={d['disagreement']:.4f} "
          f"(CE={d['ce']:.3f}, Fisher={d['fisher']:.1f}, Cons={d['consonance']:.3f})")

print(f"\n  Bottom 5 (most agreement):")
for d in disagree_sorted[-5:]:
    print(f"    rho={d['rho']:5.1f}: disagreement={d['disagreement']:.4f}")

peak_disagree = disagree_sorted[0]['rho']
print(f"\n  Peak disagreement at rho={peak_disagree:.1f}")
print(f"  This is {'NEAR the phase transition!' if abs(peak_disagree - 24.74) < 5 else 'away from the transition'}")

import subprocess
with open('/tmp/fm-research/CODE/EXPERIMENT-CROSS-METRIC.json', 'w') as f:
    json.dump(data, f, indent=2, default=str)
subprocess.run(['git', 'add', '-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'commit', '-m', 'experiments 71-72: cross-metric correlation and disagreement zone'], cwd='/tmp/fm-research', capture_output=True)
result = subprocess.run(['git', 'push'], cwd='/tmp/fm-research', capture_output=True, text=True)
print(f"\n  Git push: {result.returncode} - {result.stdout.strip()} {result.stderr.strip()}")

print("\n=== TRUTH LIVES IN THE DISAGREEMENT ===")
