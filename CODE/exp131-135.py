import numpy as np, json
from collections import Counter

print("=== EXPERIMENTS 131-135 ===\n")
np.random.seed(42)

def run(rho, sigma=10.0, n=10000, dt=0.01, sigma_oscillation=None, initial_state=None):
    s = np.array(initial_state or [1.0,1.0,1.0])
    out = []; states = []
    for step in range(n):
        sig = sigma
        if sigma_oscillation:
            sig += sigma_oscillation['amp'] * np.sin(2*np.pi*step*sigma_oscillation['freq']*dt)
            sig = max(1, sig)
        x,y,z = s; beta = 8.0/3.0
        k1 = np.array([sig*(y-x), x*(rho-z)-y, x*y-beta*z])
        s2 = s+0.5*dt*k1
        k2 = np.array([sig*(s2[1]-s2[0]), s2[0]*(rho-s2[2])-s2[1], s2[0]*s2[1]-beta*s2[2]])
        s3 = s+0.5*dt*k2
        k3 = np.array([sig*(s3[1]-s3[0]), s3[0]*(rho-s3[2])-s3[1], s3[0]*s3[1]-beta*s3[2]])
        s4 = s+dt*k3
        k4 = np.array([sig*(s4[1]-s4[0]), s4[0]*(rho-s4[2])-s4[1], s4[0]*s4[1]-beta*s4[2]])
        s = s+(dt/6)*(k1+2*k2+2*k3+k4)
        s = np.clip(s,-200,200)
        out.append(s[0])
        states.append(s.copy())
    return np.array(out[3000:]), np.array(states[3000:])

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

# EXP 131: Emotional Trajectory
print("--- Exp 131: Emotional Trajectory ---\n")
out, states = run(20.0)
x = states[:,0]; z = states[:,2]

arousal = np.abs(x - np.mean(x))
valence = x - np.mean(x)

n = len(arousal)
quarters = ['Beginning', 'Rising Action', 'Climax', 'Resolution']
for i, name in enumerate(quarters):
    start = i * n // 4
    end = (i+1) * n // 4
    seg_arousal = np.mean(arousal[start:end])
    seg_valence = np.mean(valence[start:end])
    seg_energy = np.std(out[start:end])
    if seg_arousal < 0.001: emotion = "calm/serene"
    elif seg_valence > 0: emotion = "excited/happy"
    elif seg_valence < 0: emotion = "tense/anxious"
    else: emotion = "neutral"
    print(f"  {name:15s}: arousal={seg_arousal:.6f}, valence={seg_valence:.6f}, energy={seg_energy:.6f} → {emotion}")

# EXP 132: Narrative Arc
print(f"\n--- Exp 132: Narrative Arc ---\n")
acts = ['Setup', 'Inciting Incident', 'Rising Action', 'Climax', 'Denouement']
for i, act in enumerate(acts):
    start = i * n // 5
    end = (i+1) * n // 5
    seg = out[start:end]
    energy = np.std(seg)
    c = ce(seg); co = consonance(seg)
    print(f"  Act {i+1} ({act:20s}): energy={energy:.6f}, CE={c:.4f}, Cons={co:.3f}")

energies = [np.std(out[i*n//5:(i+1)*n//5]) for i in range(5)]
climax_act = np.argmax(energies) + 1
print(f"  Climax at Act {climax_act} ({acts[climax_act-1]})")
print(f"  {'Narrative arc EXISTS!' if climax_act in [3,4] else 'No clear arc'}")

# EXP 133: The Dream
print(f"\n--- Exp 133: The Dream ---\n")
out_normal, _ = run(20.0)
out_dream, _ = run(20.0, sigma_oscillation={'amp': 5.0, 'freq': 0.5})
out_deep, _ = run(20.0, sigma_oscillation={'amp': 10.0, 'freq': 0.2})

for name, out_data in [('Awake', out_normal), ('Dreaming', out_dream), ('Deep Dream', out_deep)]:
    c = ce(out_data); co = consonance(out_data); std = np.std(out_data)
    print(f"  {name:12s}: σ={std:.4f}, CE={c:.4f}, Cons={co:.3f}, Mus={c*co:.4f}")

# EXP 134: Memory Palace
print(f"\n--- Exp 134: Memory Palace ---\n")
rooms = [
    (5, "Deep Crystal — The Void Room"),
    (15, "Surface Crystal — The Library"),
    (22, "Pendulum — The Clock Room"),
    (23.8, "Edge — The Threshold"),
    (28, "Chimera — The Butterfly Garden"),
]

nn = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
cof = [0,7,2,9,4,11,6,1,8,3,10,5]
for rho, room_name in rooms:
    out_r, states_r = run(float(rho))
    std = np.std(out_r)
    a = np.arctan2(out_r-np.mean(out_r), max(std,1e-10))
    pcs = [nn[cof[int(((x+np.pi)/(2*np.pi)*12))%12]] for x in a[::20]]
    pc_dist = Counter(pcs)
    dominant = pc_dist.most_common(3)
    print(f"  {room_name}:")
    print(f"    Energy: {std:.4f}")
    print(f"    Dominant tones: {dominant}")

# EXP 135: The Mirror
print(f"\n--- Exp 135: The Mirror ---\n")
out1, _ = run(20.0, initial_state=[1.0, 1.0, 1.0])
out2, _ = run(20.0, initial_state=[10.0, -5.0, 20.0])
out3, _ = run(20.0, initial_state=[-10.0, 20.0, 50.0])

for name, out_data in [('Self', out1), ('Other A', out2), ('Other B', out3)]:
    std = np.std(out_data)
    mean = np.mean(out_data)
    print(f"  {name:10s}: mean={mean:.6f}, std={std:.6f}")

converged = False
for delay in [100, 500, 1000, 2000, 5000]:
    corr = np.corrcoef(out1[:delay], out2[:delay])[0,1]
    if abs(corr) > 0.8 and not converged:
        print(f"\n  Convergence at ~{delay} steps (r={corr:.3f})")
        converged = True

if not converged:
    print(f"\n  No convergence — mirrors show different faces")
    final_corr = np.corrcoef(out1, out2)[0,1]
    print(f"  Final correlation: {final_corr:.3f}")

import subprocess
with open('/tmp/fm-research/CODE/EXPERIMENT-131-135.json', 'w') as f:
    json.dump({'status': 'complete'}, f)
subprocess.run(['git','add','-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git','commit','-m','experiments 131-135: emotion, narrative, dream, memory palace, mirror'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git','push'], cwd='/tmp/fm-research', capture_output=True)

print("\n=== 135 EXPERIMENTS ===")
