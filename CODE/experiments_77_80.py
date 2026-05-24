import numpy as np, json

print("=== Experiments 77-80 ===\n")
np.random.seed(42)

def run(rho, sigma=10.0, n=5000, dt=0.01):
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

def fisher(rho, sigma=10.0, delta=0.1):
    o1 = run(rho,sigma); o2 = run(rho+delta,sigma)
    bins = np.linspace(-50,50,60)
    p1,_=np.histogram(o1,bins=bins,density=True); p2,_=np.histogram(o2,bins=bins,density=True)
    p1=p1/p1.sum()+1e-10; p2=p2/p2.sum()+1e-10
    return 2*np.sum(p1*np.log(p1/p2))/delta**2

def consonance(outputs):
    cof = [0,7,2,9,4,11,6,1,8,3,10,5]
    a = np.arctan2(outputs-np.mean(outputs), np.std(outputs))
    pcs = np.array([cof[int(((x+np.pi)/(2*np.pi)*12))%12] for x in a[::10]])
    ints = np.abs(np.diff(pcs))
    cons = [0,3,4,5,7,8,9]
    ic = np.bincount(ints,minlength=12)
    return sum(ic[i] for i in cons)/len(ints) if len(ints)>0 else 0

# EXP 77: Paradigm Timeline
print("--- Exp 77: Paradigm Timeline ---\n")
paradigms = [
    ("Constraint Theory", 1, 18, "fixed-point"),
    ("Attractor Theory", 19, 50, "periodic"),
    ("Metric Theory", 51, 60, "chimera"),
    ("Structure Theory", 61, 80, "chimera"),
]
durations = [p[2]-p[1]+1 for p in paradigms]
print(f"  Paradigm durations: {durations}")
print(f"  Acceleration: {' → '.join(str(d) for d in durations)}")
print(f"  Predicted next: ~{max(5, durations[-1]//2)} experiments")

# EXP 78: Bandwidth Conservation
print(f"\n--- Exp 78: Bandwidth Conservation ---\n")
for eps_low, eps_high in [(0.01, 1.0), (0.1, 1.0), (0.5, 1.0), (0.01, 0.01), (1.0, 1.0)]:
    out_low = run(15.0)
    snap_low = (1-eps_low)*np.round(out_low) + eps_low*out_low
    out_high = run(47.0)
    snap_high = (1-eps_high)*np.round(out_high) + eps_high*out_high
    combined = snap_low + snap_high
    bw = np.std(combined)
    upper_ce = ce(snap_high)
    print(f"  ε_low={eps_low:.2f}, ε_high={eps_high:.2f}: bandwidth={bw:.2f}, upper CE={upper_ce:.4f}")

# EXP 79: Knowledge Transfer
print(f"\n--- Exp 79: Knowledge Transfer ---\n")
trained = run(28.0, n=10000)
fresh_alone = run(28.0, n=5000)
fresh_trained = run(28.0, n=5000)
trained_ce = ce(trained[-3000:])
fresh_alone_ce = ce(fresh_alone[-3000:])
print(f"  Trained CE: {trained_ce:.4f}")
print(f"  Fresh alone CE: {fresh_alone_ce:.4f}")
print(f"  Same attractor = same CE? {'Yes (CE identical)' if abs(trained_ce-fresh_alone_ce)<0.01 else 'No'}")

# EXP 80: Multi-Objective Landscape (Pareto Front)
print(f"\n--- Exp 80: Multi-Objective Pareto Front ---\n")

data = []
for rho in np.arange(5, 81, 2.5):
    out = run(float(rho))
    c = ce(out)
    f = fisher(float(rho))
    co = consonance(out)
    data.append({'rho': float(rho), 'ce': c, 'fisher': f, 'consonance': co})

def dominates(a, b):
    return (a['ce'] >= b['ce'] and a['fisher'] >= b['fisher'] and a['consonance'] >= b['consonance'] and
            (a['ce'] > b['ce'] or a['fisher'] > b['fisher'] or a['consonance'] > b['consonance']))

pareto = []
for d in data:
    if not any(dominates(other, d) for other in data if other is not d):
        pareto.append(d)

print(f"  Pareto front ({len(pareto)} points):")
for p in sorted(pareto, key=lambda x: x['rho']):
    print(f"    ρ={p['rho']:5.1f}: CE={p['ce']:.4f}, Fisher={p['fisher']:.2f}, Cons={p['consonance']:.3f}")

import subprocess
with open('/tmp/fm-research/CODE/EXPERIMENT-77-80.json', 'w') as f:
    json.dump({'pareto': pareto, 'paradigm_durations': durations}, f, indent=2, default=str)
subprocess.run(['git','add','-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git','commit','-m','experiments 77-80: paradigms, bandwidth, transfer, pareto'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git','push'], cwd='/tmp/fm-research', capture_output=True)

print("\n=== 80 EXPERIMENTS ===")
