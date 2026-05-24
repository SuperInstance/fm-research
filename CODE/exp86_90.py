import numpy as np, json, subprocess

print("=== Experiments 86-90: The Sweet Spot ===\n")
np.random.seed(42)

def run(rho, sigma=10.0, n=6000, dt=0.01):
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
    a = np.arctan2(outputs-np.mean(outputs), np.std(outputs))
    pcs = np.array([cof[int(((x+np.pi)/(2*np.pi)*12))%12] for x in a[::10]])
    ints = np.abs(np.diff(pcs))
    if len(ints)==0: return 0
    ic = np.bincount(ints,minlength=12)
    return sum(ic[i] for i in [0,3,4,5,7,8,9])/len(ints)

def fisher(rho, sigma=10.0, delta=0.1):
    o1 = run(rho,sigma); o2 = run(rho+delta,sigma)
    bins = np.linspace(-50,50,60)
    p1,_=np.histogram(o1,bins=bins,density=True); p2,_=np.histogram(o2,bins=bins,density=True)
    p1=p1/p1.sum()+1e-10; p2=p2/p2.sum()+1e-10
    return 2*np.sum(p1*np.log(p1/p2))/delta**2

# EXP 86: Sweet Spot Deep Dive
print("--- Exp 86: Sweet Spot ρ∈[14,22] ---\n")
print(f"  {'ρ':>5s} {'CE':>8s} {'Fisher':>8s} {'Cons':>8s} {'σ':>8s} {'Musical':>8s} {'Species':>16s}")
for rho in np.arange(14, 22.1, 0.4):
    out = run(float(rho))
    c = ce(out); f = fisher(float(rho)); co = consonance(out)
    std = np.std(out); acf = np.corrcoef(out[:-1],out[1:])[0,1]
    mus = c * co
    if std < 0.1: sp = "Deep Crystal"
    elif std < 1: sp = "Surface Crystal"
    elif std < 3 and acf > 0.98: sp = "Pendulum"
    else: sp = "Pre-Chaos"
    print(f"  {rho:5.1f} {c:8.4f} {f:8.2f} {co:8.3f} {std:8.3f} {mus:8.4f} {sp:>16s}")

# EXP 87: Musical Output at sweet spots
print(f"\n--- Exp 87: Melodies at Sweet Spots ---\n")
cof = [0,7,2,9,4,11,6,1,8,3,10,5]
nn = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

for rho in [15, 17.5, 20]:
    out = run(float(rho))
    melody = []
    for i in range(0, min(len(out)-25,500),25):
        seg = out[i:i+25]
        a = np.arctan2(np.mean(seg)-np.mean(out), np.std(seg))
        pc = cof[int(((a+np.pi)/(2*np.pi)*12))%12]
        oct = int(np.clip(4+np.log1p(abs(np.mean(seg)))*1.5,3,6))
        melody.append(pc+oct*12)
    unique_pcs = len(set(m%12 for m in melody))
    notes_str = ' '.join(nn[m%12]+str(m//12) for m in melody[:15])
    print(f"  ρ={rho:5.1f}: {len(melody)} notes, {unique_pcs} PCs")
    print(f"    {notes_str}...")

# EXP 88: 15 vs 47
print(f"\n--- Exp 88: ρ=15 vs ρ=47 ---\n")
for rho in [15, 47]:
    out = run(float(rho))
    print(f"  ρ={rho}: CE={ce(out):.4f}, Cons={consonance(out):.3f}, σ={np.std(out):.3f}, "
          f"Mus={ce(out)*consonance(out):.4f}, Range={np.ptp(out):.2f}")
# Winner
c15 = ce(run(15))*consonance(run(15))
c47 = ce(run(47))*consonance(run(47))
print(f"  Winner: {'ρ=15' if c15>c47 else 'ρ=47'} (musicality {max(c15,c47):.4f} vs {min(c15,c47):.4f})")

# EXP 89: Adaptive ρ
print(f"\n--- Exp 89: Adaptive ρ ---\n")
# Compare fixed vs switching
out_fixed = run(20.0)
ce_fixed = ce(out_fixed)

# Adaptive: switch between 15 and 25 every 500 steps
s = np.array([1.0,1.0,1.0])
adaptive_out = []
for step in range(6000):
    rho = 15 if (step//500)%2==0 else 25
    x,y,z = s; sigma=10.0; beta=8.0/3.0
    k1 = np.array([sigma*(y-x), x*(rho-z)-y, x*y-beta*z])
    s2 = s+0.005*k1
    k2 = np.array([sigma*(s2[1]-s2[0]), s2[0]*(rho-s2[2])-s2[1], s2[0]*s2[1]-beta*s2[2]])
    s3 = s+0.005*k2
    k3 = np.array([sigma*(s3[1]-s3[0]), s3[0]*(rho-s3[2])-s3[1], s3[0]*s3[1]-beta*s3[2]])
    s4 = s+0.01*k3
    k4 = np.array([sigma*(s4[1]-s4[0]), s4[0]*(rho-s4[2])-s4[1], s4[0]*s4[1]-beta*s4[2]])
    s = s+(0.01/6)*(k1+2*k2+2*k3+k4)
    s = np.clip(s,-200,200)
    if step >= 2000: adaptive_out.append(s[0])

ce_adaptive = ce(np.array(adaptive_out))
co_adaptive = consonance(np.array(adaptive_out))
mus_adaptive = ce_adaptive * co_adaptive

print(f"  Fixed ρ=20: CE={ce_fixed:.4f}, Mus={ce_fixed*consonance(out_fixed):.4f}")
print(f"  Adaptive 15↔25: CE={ce_adaptive:.4f}, Mus={mus_adaptive:.4f}")
print(f"  {'Adaptive wins!' if mus_adaptive > ce_fixed*consonance(out_fixed) else 'Fixed wins!'}")

# EXP 90: Third Milestone
print(f"\n--- Exp 90: What 90 Experiments Teach ---\n")
print(f"  1. Quality = variance. Period. (Exp 53)")
print(f"  2. Fisher Information peaks at transition, uncorrelated with variance (Exp 62)")
print(f"  3. CE peaks at ρ≈15, anti-correlated with variance (Exp 60)")
print(f"  4. 5 species, fuzzy boundaries near transition (Exp 65)")
print(f"  5. Pareto front: 9 optimal ρ values, no single optimum (Exp 80)")
print(f"  6. Musicality peaks at ρ≈17.5 (Exp 81)")
print(f"  7. Evolution converges on low-ρ regime (Exp 85)")
print(f"  8. Coupling helps trajectory, not individual quality (Exp 63)")
print(f"  9. Attractors are self-discovering, no transfer needed (Exp 79)")
print(f"  10. The creative landscape is a multi-objective Pareto front")
print(f"  THE SHAPE OF CREATIVITY: a ridge from (ρ≈15, high structure) to (ρ≈40, high sensitivity)")

with open('/tmp/fm-research/CODE/EXPERIMENT-86-90.json', 'w') as f:
    json.dump({'status': 'complete', 'total_experiments': 90}, f)
subprocess.run(['git','add','-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git','commit','-m','experiments 86-90: sweet spot, 15v47, adaptive rho, third milestone'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git','push'], cwd='/tmp/fm-research', capture_output=True)

print("\n=== 90 EXPERIMENTS COMPLETE ===")
