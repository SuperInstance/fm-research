import numpy as np
import json

print("=== Experiment 57: Equation Archaeology ===")
print("Searching for NEW attractors that make music\n")

np.random.seed(42)

TERMS = {
    'x': lambda s: s[0],
    'y': lambda s: s[1],
    'z': lambda s: s[2],
    'xy': lambda s: s[0]*s[1],
    'xz': lambda s: s[0]*s[2],
    'yz': lambda s: s[1]*s[2],
    'x2': lambda s: s[0]**2,
    'y2': lambda s: s[1]**2,
    'z2': lambda s: s[2]**2,
    'sinx': lambda s: np.sin(s[0]),
    'siny': lambda s: np.sin(s[1]),
    'sinz': lambda s: np.sin(s[2]),
}

TERM_NAMES = list(TERMS.keys())

def make_system_random():
    coeffs = []
    for _ in range(3):
        eq = {}
        for term in TERM_NAMES:
            if np.random.random() < 0.25:
                eq[term] = np.random.uniform(-10, 10)
        coeffs.append(eq)
    return coeffs

def evaluate_system(coeffs, n_steps=3000, dt=0.01):
    state = np.array([1.0, 1.0, 1.0])
    outputs = []
    for _ in range(n_steps):
        try:
            derivs = []
            for eq in coeffs:
                d = sum(c * TERMS[t](state) for t, c in eq.items())
                derivs.append(d)
            derivs = np.array(derivs)
            state = state + dt * derivs
            if np.any(np.abs(state) > 500) or np.any(np.isnan(state)):
                return None, -1000
            outputs.append(state[0])
        except:
            return None, -1000
    outputs = np.array(outputs)
    std = np.std(outputs[-2000:])
    if std < 0.01:
        return outputs, -100
    if std > 100:
        return outputs, -50
    hist, _ = np.histogram(outputs[-2000:], bins=30, density=True)
    hist = hist / hist.sum()
    entropy = -np.sum(hist * np.log(hist + 1e-10))
    acf1 = np.corrcoef(outputs[-2000:-1], outputs[-1999:])[0, 1]
    output_range = np.ptp(outputs[-2000:])
    score = entropy * (1 - abs(acf1)) * min(1.0, output_range / 20)
    return outputs, float(score)

print(f"  Searching 500 random ODE systems...")
N_SEARCH = 500
best_systems = []

for i in range(N_SEARCH):
    coeffs = make_system_random()
    outputs, score = evaluate_system(coeffs)
    if outputs is not None and score > 0:
        best_systems.append((score, coeffs, outputs[-1000:].tolist()))
    if (i+1) % 100 == 0:
        n_viable = len(best_systems)
        best_score = max((s[0] for s in best_systems), default=0)
        print(f"    {i+1}/{N_SEARCH}: {n_viable} viable systems, best score={best_score:.4f}")

best_systems.sort(key=lambda x: -x[0])
print(f"\n  Found {len(best_systems)} viable systems out of {N_SEARCH}")

print(f"\n--- Top 5 Discovered Attractors ---\n")
for rank, (score, coeffs, outputs) in enumerate(best_systems[:5]):
    print(f"  #{rank+1} (score={score:.4f}):")
    for i, (eq_name, eq) in enumerate(zip(['dx/dt', 'dy/dt', 'dz/dt'], coeffs)):
        terms = [f"{c:.2f}·{t}" for t, c in sorted(eq.items()) if abs(c) > 0.01]
        print(f"    {eq_name} = {' + '.join(terms)}")
    full_out, full_score = evaluate_system(coeffs, n_steps=5000)
    if full_out is not None:
        std = np.std(full_out)
        output_range = np.ptp(full_out)
        acf1 = np.corrcoef(full_out[-2000:-1], full_out[-1999:])[0, 1]
        print(f"    Stats: σ={std:.2f}, range={output_range:.2f}, ACF(1)={acf1:.3f}")
    print()

print(f"  Reference (Lorenz, ρ=28):")
lorenz = [
    {'x': -10.0, 'y': 10.0},
    {'x': 28.0, 'xz': -1.0, 'y': -1.0},
    {'xy': 1.0, 'z': -8.0/3.0},
]
ref_out, ref_score = evaluate_system(lorenz, n_steps=5000)
if ref_out is not None:
    print(f"    Score: {ref_score:.4f}")
    print(f"    σ={np.std(ref_out):.2f}, range={np.ptp(ref_out):.2f}")

print(f"\n  Structural comparison with Lorenz:")
lorenz_terms = set()
for eq in lorenz:
    lorenz_terms.update(eq.keys())
for rank, (score, coeffs, _) in enumerate(best_systems[:3]):
    discovered_terms = set()
    for eq in coeffs:
        discovered_terms.update(eq.keys())
    overlap = len(lorenz_terms & discovered_terms)
    novel = discovered_terms - lorenz_terms
    print(f"    #{rank+1}: {overlap} shared terms, novel terms: {novel if novel else 'none'}")

with open('/tmp/fm-research/CODE/EXPERIMENT-EQUATION-ARCHAEOLOGY.json', 'w') as f:
    json.dump({
        'n_searched': N_SEARCH,
        'n_viable': len(best_systems),
        'top_systems': [{
            'score': s,
            'equations': [{t: float(c) for t, c in eq.items()} for eq in coeffs],
        } for s, coeffs, _ in best_systems[:10]],
    }, f, indent=2)

import subprocess
subprocess.run(['git', 'add', '-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'commit', '-m', 'experiment 57: equation archaeology — discover new attractors'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'push'], cwd='/tmp/fm-research', capture_output=True)

print("\n=== NEW ATTRACTORS DISCOVERED ===")
