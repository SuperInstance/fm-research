import numpy as np, json, subprocess

print("=== EXPERIMENTS 111-115: DEEP MYTHOLOGY ===\n")
np.random.seed(42)

def run(rho, sigma=10.0, n=6000, dt=0.01, initial_state=None):
    s = np.array(initial_state or [1.0,1.0,1.0])
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

def step(s, rho, sigma=10.0, dt=0.01):
    x,y,z = s; beta = 8.0/3.0
    k1 = np.array([sigma*(y-x), x*(rho-z)-y, x*y-beta*z])
    s2 = s+0.5*dt*k1
    k2 = np.array([sigma*(s2[1]-s2[0]), s2[0]*(rho-s2[2])-s2[1], s2[0]*s2[1]-beta*s2[2]])
    s3 = s+0.5*dt*k2
    k3 = np.array([sigma*(s3[1]-s3[0]), s3[0]*(rho-s3[2])-s3[1], s3[0]*s3[1]-beta*s3[2]])
    s4 = s+dt*k3
    k4 = np.array([sigma*(s4[1]-s4[0]), s4[0]*(rho-s4[2])-s4[1], s4[0]*s4[1]-beta*s4[2]])
    s = s+(dt/6)*(k1+2*k2+2*k3+k4)
    return np.clip(s,-200,200)

# EXP 111: The Underworld (ρ=0)
print("--- Exp 111: The Underworld (ρ≈0) ---\n")
for rho in [0, 0.1, 0.5, 1, 2, 5]:
    out = run(float(rho))
    std = np.std(out); c = ce(out); co = consonance(out)
    print(f"  ρ={rho:4.1f}: σ={std:.6f}, CE={c:.6f}, Cons={co:.3f}")
print(f"  The Underworld is perfect silence. No music in nothing.")

# EXP 112: The Apocalypse (ρ=100→1, hysteresis)
print(f"\n--- Exp 112: The Apocalypse (Hysteresis) ---\n")
s = np.array([1.0,1.0,1.0])
# Start chaotic at rho=100
for _ in range(3000):
    s = step(s, 100.0)
chaotic_state = s.copy()

# Now descend
for rho in [80, 60, 47, 35, 28, 24, 20, 15, 10, 5, 1]:
    for _ in range(1000):
        s = step(s, float(rho))
    from_chaos_std = np.std([s[0]])
    out_fresh = run(float(rho), initial_state=[1.0,1.0,1.0])
    fresh_std = np.std(out_fresh)
    diff_pct = (from_chaos_std - fresh_std) / fresh_std * 100 if fresh_std > 0 else 0
    print(f"  ρ={rho:3d}: from-chaos σ={from_chaos_std:.4f}, fresh σ={fresh_std:.4f}, hysteresis={diff_pct:+.1f}%")

# EXP 113: Resurrection
print(f"\n--- Exp 113: Resurrection (ρ=5→28) ---\n")
dead = run(5.0, n=3000)
dead_std = np.std(dead[-1000:])
print(f"  Dead (ρ=5): σ={dead_std:.6f}")

# Get final state from dead system
s = np.array([1.0,1.0,1.0])
for _ in range(3000):
    s = step(s, 5.0)

resurrected = run(28.0, n=5000, initial_state=s.tolist())
alive_std = np.std(resurrected[-1000:])
alive_ce = ce(resurrected)
print(f"  Resurrected (ρ=28): σ={alive_std:.4f}, CE={alive_ce:.4f}")
print(f"  Awakening ratio: {alive_std/dead_std if dead_std > 0 else 'inf':.1f}×")

# Compare to fresh ρ=28
fresh = run(28.0)
fresh_ce = ce(fresh)
print(f"  Fresh ρ=28: CE={fresh_ce:.4f}")
print(f"  Resurrection {'preserves' if abs(alive_ce - fresh_ce)/fresh_ce < 0.1 else 'transforms'} the attractor")

# EXP 114: The Trinity
print(f"\n--- Exp 114: The Trinity ---\n")
out_15 = run(15.0); out_20 = run(20.0); out_28 = run(28.0)

# Normalize
n15 = (out_15 - out_15.min())/(out_15.max()-out_15.min()+1e-10)
n20 = (out_20 - out_20.min())/(out_20.max()-out_20.min()+1e-10)
n28 = (out_28 - out_28.min())/(out_28.max()-out_28.min()+1e-10)

for combo_name, combo in [
    ('Father+Son (15+20)', n15 + n20),
    ('Father+Spirit (15+28)', n15 + n28),
    ('Son+Spirit (20+28)', n20 + n28),
    ('Trinity (15+20+28)', n15 + n20 + n28),
    ('Trinity product', n15 * n20 * n28),
]:
    c = ce(combo); co = consonance(combo)
    print(f"  {combo_name:25s}: CE={c:.4f}, Cons={co:.3f}, Mus={c*co:.4f}")

# EXP 115: The Mandala (round trip)
print(f"\n--- Exp 115: The Mandala ---\n")
s = np.array([1.0,1.0,1.0])
outward = []
for rho in range(1, 101, 2):
    for _ in range(200):
        s = step(s, float(rho))
    outward.append({'rho': rho, 'state': s.copy()})

return_state = s.copy()
print(f"  Outward journey: ρ 1→100")
print(f"  State at ρ=100: {s}")

# Return journey
for rho in range(99, 0, -2):
    for _ in range(200):
        s = step(s, float(rho))

initial_state = np.array([1.0,1.0,1.0])
displacement = np.linalg.norm(s - initial_state)
print(f"  Return journey: ρ 100→1")
print(f"  Final state: {s}")
print(f"  Initial state: {initial_state}")
print(f"  Displacement from origin: {displacement:.4f}")
print(f"  {'The mandala CLOSES' if displacement < 1 else 'The mandala DOES NOT CLOSE — the journey transforms you'}")

with open('/tmp/fm-research/CODE/EXPERIMENT-111-115.json', 'w') as f:
    json.dump({'mandala_displacement': float(displacement)}, f, indent=2)
subprocess.run(['git','add','-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git','commit','-m','experiments 111-115: deep mythology — underworld, apocalypse, resurrection, trinity, mandala'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git','push'], cwd='/tmp/fm-research', capture_output=True)

print("\n=== 115 EXPERIMENTS — DEEP MYTHOLOGY ===")
