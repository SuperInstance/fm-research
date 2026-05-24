import numpy as np
import json
from flux_tensor_midi.creative_engine import CreativeSystem, QualityMetrics

print("=== Experiment 52: Attractor Zoology ===\n")
print("Cataloging the species of creative dynamics.\n")

np.random.seed(42)

def analyze_attractor(sys, name, n_warmup=5000, n_sample=5000):
    """Deep analysis of a single attractor."""
    # Warm up
    for _ in range(n_warmup): sys.step()
    
    # Sample
    outputs = []
    states = []
    for _ in range(n_sample):
        out = sys.step()
        outputs.append(out)
        states.append(sys.state.copy())
    
    outputs = np.array(outputs)
    states = np.array(states)
    
    # Basic stats
    mean = np.mean(outputs)
    std = np.std(outputs)
    minimum = np.min(outputs)
    maximum = np.max(outputs)
    
    # Autocorrelation at different lags
    acf_1 = np.corrcoef(outputs[:-1], outputs[1:])[0, 1]
    acf_10 = np.corrcoef(outputs[:-10], outputs[10:])[0, 1]
    acf_100 = np.corrcoef(outputs[:-100], outputs[100:])[0, 1] if len(outputs) > 100 else 0
    
    # Spectral analysis
    fft = np.fft.rfft(outputs - np.mean(outputs))
    power = np.abs(fft) ** 2
    freqs = np.fft.rfftfreq(len(outputs))
    
    # Dominant frequency
    dominant_freq = freqs[np.argmax(power[1:]) + 1] if len(power) > 1 else 0
    
    # Spectral entropy
    psd = power / np.sum(power)
    spectral_entropy = -np.sum(psd * np.log(psd + 1e-10))
    
    # Lyapunov-like measure: divergence rate
    divs = []
    for i in range(0, min(1000, len(outputs) - 100), 10):
        d = abs(outputs[i+100] - outputs[i])
        divs.append(d)
    avg_divergence = np.mean(divs) if divs else 0
    
    # Regime classification
    if std < 0.5:
        regime = "FIXED POINT"
        species = "Crystal"
    elif std < 2 and acf_1 > 0.9:
        regime = "PERIODIC"
        species = "Pendulum"
    elif std < 5 and acf_1 > 0.5:
        regime = "QUASI-PERIODIC"
        species = "Spiral"
    elif std > 5 and acf_1 < 0.3:
        regime = "CHAOTIC"
        species = "Butterfly"
    else:
        regime = "TRANSITIONAL"
        species = "Chimera"
    
    # Quality
    q = QualityMetrics.from_outputs(outputs).quality
    
    # Rough fractal dimension (box-counting on 2D projection)
    x = states[:, 0]
    y = states[:, 2]
    n_boxes = []
    for eps in [0.1, 0.5, 1.0, 2.0, 5.0]:
        boxes = set()
        for i in range(0, len(x), 10):
            bx = int(x[i] / eps)
            by = int(y[i] / eps)
            boxes.add((bx, by))
        n_boxes.append(len(boxes))
    
    # Fractal dimension estimate
    if len(n_boxes) >= 2:
        log_eps = np.log([0.1, 0.5, 1.0, 2.0, 5.0][:len(n_boxes)])
        log_n = np.log(n_boxes)
        if len(log_eps) > 1:
            fd = -np.polyfit(log_eps, log_n, 1)[0]
        else:
            fd = 0
    else:
        fd = 0
    
    return {
        'name': name,
        'regime': regime,
        'species': species,
        'quality': float(q),
        'mean': float(mean),
        'std': float(std),
        'range': float(maximum - minimum),
        'acf_1': float(acf_1),
        'acf_10': float(acf_10),
        'acf_100': float(acf_100),
        'dominant_freq': float(dominant_freq),
        'spectral_entropy': float(spectral_entropy),
        'divergence': float(avg_divergence),
        'fractal_dim': float(fd),
    }

# Catalog attractors across ρ landscape
print("--- The Attractor Bestiary ---\n")

attractors = []
for rho in [0.5, 1, 2, 3, 5, 8, 10, 12, 15, 18, 20, 22, 24, 24.74, 25, 26, 28, 30, 35, 40, 45, 47, 50, 55, 60, 70, 80, 100]:
    sys = CreativeSystem(rho=float(rho))
    result = analyze_attractor(sys, f"ρ={rho}")
    attractors.append(result)

# Print the bestiary
print(f"  {'Name':>10s} {'Species':>14s} {'Quality':>10s} {'σ':>8s} {'ACF(1)':>8s} {'ACF(100)':>9s} {'Freq':>8s} {'Entropy':>9s} {'FracDim':>9s}")
print(f"  {'-'*90}")

for a in attractors:
    print(f"  {a['name']:>10s} {a['species']:>14s} {a['quality']:10.4f} {a['std']:8.3f} {a['acf_1']:8.3f} {a['acf_100']:9.3f} {a['dominant_freq']:8.4f} {a['spectral_entropy']:9.3f} {a['fractal_dim']:9.2f}")

# Species count
from collections import Counter
species_counts = Counter(a['species'] for a in attractors)
print(f"\n  Species census:")
for species, count in species_counts.most_common():
    print(f"    {species}: {count}")

# Phase transition boundaries
print(f"\n  Phase transitions:")
prev_regime = attractors[0]['regime']
for a in attractors[1:]:
    if a['regime'] != prev_regime:
        print(f"    {prev_regime} → {a['regime']} at {a['name']}")
        prev_regime = a['regime']

# Best per species
print(f"\n  Best of each species:")
for species in species_counts:
    members = [a for a in attractors if a['species'] == species]
    best = max(members, key=lambda a: a['quality'])
    print(f"    {species}: {best['name']} (quality={best['quality']:.4f})")

# Quality vs fractal dimension
print(f"\n  Quality × Fractal Dimension:")
for a in attractors:
    if a['fractal_dim'] > 0:
        print(f"    {a['name']:>10s}: D={a['fractal_dim']:.2f}, Q={a['quality']:.4f}")

# Save
import subprocess
with open('/tmp/fm-research/CODE/EXPERIMENT-ATTRACTOR-ZOOLOGY.json', 'w') as f:
    json.dump(attractors, f, indent=2, default=str)
subprocess.run(['git', 'add', '-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'commit', '-m', 'experiment 52: attractor zoology — catalog creative species'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'push'], cwd='/tmp/fm-research', capture_output=True)

print("\n=== THE ATTRACTOR BESTIARY IS COMPLETE ===")
