import numpy as np, json, subprocess
from collections import Counter

print("=== EXPERIMENTS 121-125 ===\n")
np.random.seed(42)

def run(rho, sigma=10.0, n=6000, dt=0.01, seed=None):
    if seed is not None: np.random.seed(seed)
    s = np.array([1.0,1.0,1.0])
    out = []
    for _ in range(n):
        x,y,z = s; beta = 8.0/3.0
        k1 = np.array([sigma*(y-x), x*(rho-z)-y, x*y-beta*z])
        s2 = s+0.5*dt*k1
        k2 = np.array([sigma*(s2[1]-s2[0]), s2[0]*(rho-s2[2])-s2[1], s2[0]*s2[1]-beta*s2[2]])
        s3 = s+0.5*dt*k2
        k3 = np.array([sigma*(s3[1]-s3[0]), s3[0]*(rho-s3[2])-s3[1], s3[0]*s3[1]-beta*s3[2]])
        s4 = s+dt*k3
        k4 = np.array([sigma*(s4[1]-s4[0]), s4[0]*(rho-s4[2])-s4[1], s4[0]*s4[1]-beta*s4[2]])
        s = s+(dt/6)*(k1+2*k2+2*k3+k4)
        s = np.clip(s,-200,200)
        out.append(s[0])
    return np.array(out[2000:])

def ce(outputs):
    if np.var(outputs) < 1e-10: return 0
    h,_ = np.histogram(outputs, bins=10, density=True)
    p = h/h.sum()
    H = -np.sum(p*np.log(p+1e-10))/np.log(10)
    D = np.sum((p-np.ones(10)/10)**2)/0.82
    return H*D

def consonance(outputs):
    cof = [0,7,2,9,4,11,6,1,8,3,10,5]
    a = np.arctan2(outputs-np.mean(outputs), max(np.std(outputs),1e-10))
    pcs = np.array([cof[int(((x+np.pi)/(2*np.pi)*12))%12] for x in a[::10]])
    ints = np.abs(np.diff(pcs))
    if len(ints)==0: return 0
    ic = np.bincount(ints,minlength=12)
    return sum(ic[i] for i in [0,3,4,5,7,8,9])/len(ints)

nn = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

# EXP 121: The Sacrifice
print("--- Exp 121: The Sacrifice ---\n")
best_rho = 0; best_mus = 0; best_config = {}
for rho in np.arange(10, 30, 0.5):
    for sigma in [5, 8, 10, 12, 15]:
        out = run(float(rho), float(sigma))
        c = ce(out); co = consonance(out); std = np.std(out)
        mus = c * co
        if mus > best_mus:
            best_mus = mus; best_rho = rho; best_config = {'rho': rho, 'sigma': sigma, 'ce': c, 'cons': co, 'std': std}
print(f"  Best unconstrained: rho={best_rho:.1f}, sigma={best_config['sigma']:.0f}, mus={best_mus:.4f}")
print(f"    CE={best_config['ce']:.4f}, Cons={best_config['cons']:.3f}, std={best_config['std']:.4f}")

# Now find best with constraints
print(f"\n  Constrained optimization:")
for min_ce, min_cons in [(0.1, 0.5), (0.15, 0.7), (0.2, 0.9)]:
    best_c_mus = 0; best_c_rho = 0
    for rho in np.arange(10, 30, 0.5):
        out = run(float(rho))
        c = ce(out); co = consonance(out)
        if c >= min_ce and co >= min_cons:
            mus = c * co
            if mus > best_c_mus:
                best_c_mus = mus; best_c_rho = rho
    if best_c_mus > 0:
        print(f"    CE>={min_ce}, Cons>={min_cons}: rho={best_c_rho:.1f}, mus={best_c_mus:.4f}")
    else:
        print(f"    CE>={min_ce}, Cons>={min_cons}: INFEASIBLE")

# EXP 122: The Oracle
print(f"\n--- Exp 122: The Oracle (Prediction) ---\n")
X = []
y = []
for rho in np.arange(5, 50, 2):
    out = run(float(rho))
    std = np.std(out)
    acf = np.corrcoef(out[:-1], out[1:])[0,1]
    zc = np.sum(np.abs(np.diff(np.sign(out - np.mean(out)))) > 0) / len(out)
    fft = np.fft.rfft(out - np.mean(out))
    power = np.abs(fft[1:])**2
    centroid = np.sum(np.arange(len(power)) * power) / (np.sum(power) + 1e-10) if np.sum(power) > 0 else 0
    
    X.append([std, acf, zc, centroid])
    y.append(ce(out) * consonance(out))

X = np.array(X); y = np.array(y)

X_norm = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-10)
weights = np.linalg.lstsq(X_norm, y, rcond=None)[0]
predictions = X_norm @ weights
errors = np.abs(predictions - y)

print(f"  Features: std, ACF, zero-crossing rate, spectral centroid")
print(f"  Training points: {len(X)}")
print(f"  Mean absolute error: {np.mean(errors):.4f}")
print(f"  Max error: {np.max(errors):.4f}")
print(f"  Feature weights: std={weights[0]:.3f}, ACF={weights[1]:.3f}, ZCR={weights[2]:.3f}, centroid={weights[3]:.3f}")

print(f"\n  Test predictions:")
for rho in [12, 17, 22, 26, 33, 44]:
    out = run(float(rho))
    actual = ce(out) * consonance(out)
    std = np.std(out); acf = np.corrcoef(out[:-1], out[1:])[0,1]
    zc = np.sum(np.abs(np.diff(np.sign(out - np.mean(out)))) > 0) / len(out)
    fft = np.fft.rfft(out - np.mean(out))
    power = np.abs(fft[1:])**2
    centroid = np.sum(np.arange(len(power)) * power) / (np.sum(power) + 1e-10) if np.sum(power) > 0 else 0
    
    features = np.array([std, acf, zc, centroid])
    features_norm = (features - X.mean(axis=0)) / (X.std(axis=0) + 1e-10)
    predicted = float(features_norm @ weights)
    
    err = abs(predicted - actual)
    print(f"    rho={rho:3d}: predicted={predicted:.4f}, actual={actual:.4f}, error={err:.4f}")

# EXP 123: The Ritual (reproducibility)
print(f"\n--- Exp 123: The Ritual ---\n")
ritual_mels = []
for seed in range(20):
    out = run(20.0, seed=seed)
    pentatonic = [0,2,4,7,9]
    mean_o = np.mean(out); std_o = max(np.std(out), 1e-10)
    pcs = []
    for i in range(0, len(out)-50, 50):
        seg = out[i:i+50]
        norm = (np.mean(seg) - mean_o) / std_o
        pc_idx = int(np.clip((norm + 3) / 6 * 5, 0, 4))
        pcs.append(pentatonic[pc_idx])
    ritual_mels.append(pcs)

agreements = []
for i in range(len(ritual_mels[0])):
    notes_at_pos = [m[i] for m in ritual_mels]
    most_common = Counter(notes_at_pos).most_common(1)[0]
    agreement = most_common[1] / len(ritual_mels)
    agreements.append(agreement)

print(f"  20 runs at rho=20, pentatonic mapping")
print(f"  Mean agreement: {np.mean(agreements):.3f}")
print(f"  Best agreement: {np.max(agreements):.3f}")
print(f"  Worst agreement: {np.min(agreements):.3f}")
print(f"  {'RITUAL EXISTS -- runs are similar' if np.mean(agreements) > 0.7 else 'NO RITUAL -- each run is unique'}")

# EXP 124: Sacred Geometry
print(f"\n--- Exp 124: Sacred Geometry ---\n")
s = np.array([1.0,1.0,1.0])
states = []
for _ in range(8000):
    x,y,z = s; sigma=10.0; beta=8.0/3.0; rho=20.0
    k1 = np.array([sigma*(y-x), x*(rho-z)-y, x*y-beta*z])
    s2 = s+0.005*k1
    k2 = np.array([sigma*(s2[1]-s2[0]), s2[0]*(rho-s2[2])-s2[1], s2[0]*s2[1]-beta*s2[2]])
    s3 = s+0.005*k2
    k3 = np.array([sigma*(s3[1]-s3[0]), s3[0]*(rho-s3[2])-s3[1], s3[0]*s3[1]-beta*s3[2]])
    s4 = s+0.01*k3
    k4 = np.array([sigma*(s4[1]-s4[0]), s4[0]*(rho-s4[2])-s4[1], s4[0]*s4[1]-beta*s4[2]])
    s = s+(0.01/6)*(k1+2*k2+2*k3+k4)
    s = np.clip(s,-200,200)
    states.append(s.copy())

states = np.array(states[3000:])
x, y, z = states[:,0], states[:,1], states[:,2]

print(f"  rho=20 attractor shape:")
print(f"    x range: [{x.min():.3f}, {x.max():.3f}]")
print(f"    y range: [{y.min():.3f}, {y.max():.3f}]")
print(f"    z range: [{z.min():.3f}, {z.max():.3f}]")
print(f"    x std: {np.std(x):.4f}")
print(f"    Is it a point? {'YES (fixed point)' if np.std(x) < 0.01 else 'NO'}")
xy_corr = np.corrcoef(x, y)[0,1]
print(f"    Is it a spiral? x-y correlation: {'YES (r='+str(xy_corr)+')' if abs(xy_corr) > 0.8 else 'NO (r='+str(xy_corr)+')'}")

xz_corr = np.corrcoef(x, z)[0,1]
print(f"    x-z correlation: {xz_corr:.3f}")
print(f"    At rho=20 (below transition), the attractor is {'a fixed point with tiny oscillations' if np.std(x) < 1 else 'a spiral converging to fixed point' if np.std(x) < 5 else 'a strange attractor'}")

# EXP 125: Prophecy
print(f"\n--- Exp 125: Ten Prophecies ---\n")
prophecies = [
    "1. Human listening tests will confirm rho~20 as the most musical, but rho~24-28 as most 'interesting'",
    "2. The ritual (reproducibility) will break down at the cliff -- each crossing is unique",
    "3. The Oracle (prediction model) will fail on the cliff region -- it's inherently unpredictable",
    "4. Coupling two systems at the cliff (rho~23.8) will produce genuinely emergent music",
    "5. The shadow (reverse time) at the cliff will NOT collapse -- the cliff has time-reversal symmetry",
    "6. The Fool archetype will WIN in blind listening tests -- randomness is more engaging than order",
    "7. A 7th species will be discovered at the cliff boundary (the 'Edge Dweller')",
    "8. The mandala displacement will INCREASE with more complex dynamics -- experienced artists change more",
    "9. Adding rhythm (from zero crossings) will shift the optimal rho upward by ~3 units",
    "10. The unified theory (from Claude Code) will predict the cliff at rho~23.81 +/- 0.5 without being told"
]
for p in prophecies:
    print(f"  {p}")

with open('/tmp/fm-research/CODE/EXPERIMENT-121-125.json', 'w') as f:
    json.dump({'prophecies': prophecies, 'ritual_agreement': float(np.mean(agreements))}, f, indent=2)
subprocess.run(['git','add','-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git','commit','-m','experiments 121-125: sacrifice, oracle, ritual, geometry, prophecy'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git','push'], cwd='/tmp/fm-research', capture_output=True)

print("\n=== 125 EXPERIMENTS ===")
