import numpy as np, json

print("=== EXPERIMENTS 101-105: THE MYTHOLOGICAL ROUND ===\n")
np.random.seed(42)

def run(rho, sigma=10.0, n=6000, dt=0.01, perturbation_times=None, perturbation_strength=0):
    s = np.array([1.0,1.0,1.0])
    out = []
    for step in range(n):
        x,y,z = s; beta = 8.0/3.0
        k1 = np.array([sigma*(y-x), x*(rho-z)-y, x*y-beta*z])
        s2 = s+0.5*dt*k1
        k2 = np.array([sigma*(s2[1]-s2[0]), s2[0]*(rho-s2[2])-s2[1], s2[0]*s2[1]-beta*s2[2]])
        s3 = s+0.5*dt*k2
        k3 = np.array([sigma*(s3[1]-s3[0]), s3[0]*(rho-s3[2])-s3[1], s3[0]*s3[1]-beta*s3[2]])
        s4 = s+dt*k3
        k4 = np.array([sigma*(s4[1]-s4[0]), s4[0]*(rho-s4[2])-s4[1], s4[0]*s4[1]-beta*s4[2]])
        s = s+(dt/6)*(k1+2*k2+2*k3+k4)
        if perturbation_times and step in perturbation_times:
            s += np.random.randn(3) * perturbation_strength
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

def fisher(rho, sigma=10.0, delta=0.1):
    o1 = run(rho,sigma); o2 = run(rho+delta,sigma)
    bins = np.linspace(-50,50,60)
    p1,_=np.histogram(o1,bins=bins,density=True); p2,_=np.histogram(o2,bins=bins,density=True)
    p1=p1/p1.sum()+1e-10; p2=p2/p2.sum()+1e-10
    return 2*np.sum(p1*np.log(p1/p2))/delta**2

# EXP 101: Hero's Journey
print("--- Exp 101: The Hero's Journey (ρ=1 to 100) ---\n")
journey = []
for rho in [1, 5, 10, 15, 20, 23, 23.5, 24, 24.5, 25, 28, 35, 47, 60, 80, 100]:
    out = run(float(rho))
    c = ce(out); f = fisher(float(rho)); co = consonance(out)
    std = np.std(out)
    
    if std < 0.1: stage = "Innocence (Fixed Point)"
    elif std < 1: stage = "Call to Adventure"
    elif std < 5: stage = "Crossing the Threshold"
    elif std < 15: stage = "The Ordeal (Chaos)"
    else: stage = "Return with Elixir"
    
    journey.append({'rho': rho, 'ce': c, 'fisher': f, 'cons': co, 'std': std, 'stage': stage})
    print(f"  ρ={rho:5.1f}: {stage:30s} CE={c:.4f} Fisher={f:.2f} Cons={co:.3f}")

# EXP 102: The Trickster
print(f"\n--- Exp 102: Trickster Perturbations ---\n")
for rho in [15, 20, 24, 28, 47]:
    base = run(float(rho))
    base_mus = ce(base) * consonance(base)
    
    kick_times = np.random.choice(4000, 20, replace=False) + 2000
    tricked = run(float(rho), perturbation_times=kick_times.tolist(), perturbation_strength=1.0)
    tricked_mus = ce(tricked) * consonance(tricked)
    
    impact = (tricked_mus - base_mus) / base_mus * 100 if base_mus > 0 else 0
    print(f"  ρ={rho:3d}: base={base_mus:.4f}, tricked={tricked_mus:.4f} ({impact:+.1f}%) {'Trickster helps!' if impact > 0 else 'Trickster hurts'}")

# EXP 103: The Shadow (time-reversed)
print(f"\n--- Exp 103: The Shadow (Reverse Time) ---\n")
for rho in [20, 24, 28]:
    out_fwd = run(float(rho))
    
    s = np.array([1.0,1.0,1.0])
    out_rev = []
    for _ in range(6000):
        x,y,z = s; sigma=10.0; beta=8.0/3.0
        k1 = np.array([sigma*(y-x), x*(rho-z)-y, x*y-beta*z])
        s2 = s-0.5*0.01*k1
        k2 = np.array([sigma*(s2[1]-s2[0]), s2[0]*(rho-s2[2])-s2[1], s2[0]*s2[1]-beta*s2[2]])
        s3 = s-0.5*0.01*k2
        k3 = np.array([sigma*(s3[1]-s3[0]), s3[0]*(rho-s3[2])-s3[1], s3[0]*s3[1]-beta*s3[2]])
        s4 = s-0.01*k3
        k4 = np.array([sigma*(s4[1]-s4[0]), s4[0]*(rho-s4[2])-s4[1], s4[0]*s4[1]-beta*s4[2]])
        s = s-(0.01/6)*(k1+2*k2+2*k3+k4)
        if np.any(np.abs(s) > 200): s = np.clip(s, -200, 200)
        out_rev.append(s[0])
    out_rev = np.array(out_rev[2000:])
    
    fwd_mus = ce(out_fwd) * consonance(out_fwd)
    rev_mus = ce(out_rev) * consonance(out_rev)
    fwd_std = np.std(out_fwd); rev_std = np.std(out_rev)
    
    print(f"  ρ={rho}: forward σ={fwd_std:.3f} mus={fwd_mus:.4f} | shadow σ={rev_std:.3f} mus={rev_mus:.4f}")

# EXP 104: Anima/Animus (order × chaos)
print(f"\n--- Exp 104: Marriage of Order and Chaos ---\n")
order = run(15.0)
chaos = run(35.0)

norm_o = (order - order.min()) / (order.max() - order.min() + 1e-10)
norm_c = (chaos - chaos.min()) / (chaos.max() - chaos.min() + 1e-10)

for alpha in [0.0, 0.25, 0.5, 0.75, 1.0]:
    combined = alpha * norm_o + (1-alpha) * norm_c
    c = ce(combined); co = consonance(combined)
    print(f"  α={alpha:.2f} (order={alpha:.0%}, chaos={1-alpha:.0%}): CE={c:.4f}, Cons={co:.3f}, Mus={c*co:.4f}")

product = norm_o * norm_c
prod_mus = ce(product) * consonance(product)
print(f"  Product (order×chaos): CE={ce(product):.4f}, Cons={consonance(product):.3f}, Mus={prod_mus:.4f}")

# EXP 105: The Return
print(f"\n--- Exp 105: The Return (Melody with Wisdom) ---\n")
print(f"  Using: ρ=20 (sweet spot), σ=10 (not metric-optimal 6.3)")
print(f"  Adding: rhythmic variety from zero crossings")
print(f"  Scale: Major pentatonic [C D E G A]")
print(f"  Knowledge: vary dynamics deliberately, not from metric")

out105 = run(20.0, 10.0, n=12000)
pentatonic = [0,2,4,7,9]
nn = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

melody = []
t = 0
for i in range(0, len(out105)-30, 30):
    seg = out105[i:i+30]
    mean_o = np.mean(out105); std_o = max(np.std(out105), 1e-10)
    seg_mean = np.mean(seg)
    norm = (seg_mean - mean_o) / std_o
    
    pc_idx = int(np.clip((norm + 3) / 6 * 5, 0, 4))
    pc = pentatonic[pc_idx]
    octave = 5 if norm > 0.5 else 4
    midi = pc + octave * 12
    
    position_in_melody = len(melody)
    if position_in_melody % 16 < 4: vel = 100
    elif position_in_melody % 16 < 8: vel = 80
    elif position_in_melody % 16 < 12: vel = 60
    else: vel = 90
    
    zc = np.sum(np.abs(np.diff(np.sign(seg - mean_o))) > 0)
    if position_in_melody % 4 == 0: dur = 4
    elif zc > 2: dur = 1
    elif position_in_melody % 2 == 0: dur = 2
    else: dur = 1
    
    melody.append({'note': midi, 'pc': pc, 'oct': octave, 'vel': vel, 'dur': dur, 'tick': t})
    t += dur

print(f"  The Return: {len(melody)} notes")
print(f"  Pitch classes: {sorted(set(m['pc'] for m in melody))}")
pcs = [nn[m['pc']] for m in melody]
from collections import Counter
pc_counts = Counter(pcs)
print(f"  Distribution: {dict(pc_counts.most_common())}")
print(f"  First 25: {' '.join(nn[m['pc']]+str(m['oct'])+'({'+str(m['dur'])+\\'/\\'w\\'if m[\\'dur\\']==4 else \\'h\\'if m[\\'dur\\']==2 else \\'q\\'}\\')' for m in melody[:25])}")
print(f"\n  This melody carries 100 experiments in its bones.")
print(f"  It knows about the cliff, the Pareto front, the five species,")
print(f"  the failed metrics, the Deep Crystal, the Fisher peak,")
print(f"  and the irreducible gap between measurement and music.")

import subprocess
with open('/tmp/fm-research/CODE/EXPERIMENT-101-105.json', 'w') as f:
    json.dump({'journey': journey, 'total_experiments': 105}, f, indent=2, default=str)
subprocess.run(['git','add','-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git','commit','-m','experiments 101-105: mythological round — hero journey, trickster, shadow, marriage, return'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git','push'], cwd='/tmp/fm-research', capture_output=True)

print("\n=== 105 EXPERIMENTS — THE MYTHOLOGICAL ROUND ===")
