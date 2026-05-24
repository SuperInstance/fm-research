import numpy as np, json, subprocess

print("=== EXPERIMENTS 106-110: THE ARCHETYPE EXPERIMENTS ===\n")
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
    a = np.arctan2(outputs-np.mean(outputs), max(np.std(outputs),1e-10))
    pcs = np.array([cof[int(((x+np.pi)/(2*np.pi)*12))%12] for x in a[::10]])
    ints = np.abs(np.diff(pcs))
    if len(ints)==0: return 0
    ic = np.bincount(ints,minlength=12)
    return sum(ic[i] for i in [0,3,4,5,7,8,9])/len(ints)

nn = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

def make_melody(outputs, scale, archetype_rules=None):
    mean_o = np.mean(outputs); std_o = max(np.std(outputs), 1e-10)
    melody = []; t = 0
    for i in range(0, len(outputs)-30, 30):
        seg = outputs[i:i+30]
        seg_mean = np.mean(seg)
        norm = (seg_mean - mean_o) / std_o
        pc_idx = int(np.clip((norm + 3) / 6 * len(scale), 0, len(scale)-1))
        pc = scale[pc_idx]
        octave = 5 if norm > 0.5 else 4
        midi = pc + octave * 12
        
        pos = len(melody)
        if archetype_rules:
            vel, dur = archetype_rules(pos, norm, seg, mean_o)
        else:
            vel = 80; dur = 2
        
        melody.append({'note': midi, 'pc': pc, 'octave': octave, 'vel': vel, 'dur': dur, 'tick': t})
        t += dur
    return melody

# EXP 106: WARRIOR
print("--- Exp 106: The Warrior ---")
warrior_rules = lambda pos, norm, seg, mean: (
    min(127, 100 + int(abs(norm) * 30)),
    1 if pos % 4 < 2 else 2
)
out_warrior = run(47.0, 12.0)
mel_warrior = make_melody(out_warrior, [0,3,5,6,7,10], warrior_rules)
warrior_mus = ce(out_warrior) * consonance(out_warrior)
print(f"  ρ=47, σ=12, blues scale, aggressive dynamics")
print(f"  {len(mel_warrior)} notes, musicality={warrior_mus:.4f}")
print(f"  First 15: {' '.join(nn[m['pc']]+str(m['octave']) for m in mel_warrior[:15])}")

# EXP 107: LOVER
print(f"\n--- Exp 107: The Lover ---")
lover_rules = lambda pos, norm, seg, mean: (
    max(40, 70 + int(norm * 10)),
    4 if pos % 3 == 0 else 2
)
out_lover = run(15.0, 5.0)
mel_lover = make_melody(out_lover, [0,2,4,7,9], lover_rules)
lover_mus = ce(out_lover) * consonance(out_lover)
print(f"  ρ=15, σ=5, pentatonic, gentle dynamics")
print(f"  {len(mel_lover)} notes, musicality={lover_mus:.4f}")
print(f"  First 15: {' '.join(nn[m['pc']]+str(m['octave']) for m in mel_lover[:15])}")

# EXP 108: MAGICIAN
print(f"\n--- Exp 108: The Magician ---")
s = np.array([1.0,1.0,1.0])
magic_out = []
for step in range(8000):
    if step < 2000: rho = 15
    elif step < 3500: rho = 28
    elif step < 5000: rho = 47
    elif step < 6500: rho = 15
    else: rho = 24
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
    if step >= 3000: magic_out.append(s[0])

magician_rules = lambda pos, norm, seg, mean: (
    80 + int(abs(norm) * 20),
    [4,2,2,1,2][pos % 5]
)
mel_magic = make_melody(np.array(magic_out), [0,1,4,5,7,8,11], magician_rules)
magic_mus = ce(np.array(magic_out)) * consonance(np.array(magic_out))
print(f"  ρ cycles: 15→28→47→15→24, mixolydian, varied rhythm")
print(f"  {len(mel_magic)} notes, musicality={magic_mus:.4f}")

# EXP 109: KING/QUEEN
print(f"\n--- Exp 109: The Sovereign ---")
sovereign_rules = lambda pos, norm, seg, mean: (
    85 + int(np.sin(pos * 0.3) * 15),
    2 if pos % 2 == 0 else 1
)
out_sov = run(20.0, 10.0)
mel_sov = make_melody(out_sov, [0,2,4,5,7,9,11], sovereign_rules)
sov_mus = ce(out_sov) * consonance(out_sov)
print(f"  ρ=20, σ=10, major scale, measured dynamics")
print(f"  {len(mel_sov)} notes, musicality={sov_mus:.4f}")

# EXP 110: THE FOOL
print(f"\n--- Exp 110: The Fool ---")
fool_out = []
s = np.array([1.0,1.0,1.0])
for step in range(8000):
    rho = np.random.choice([5, 15, 28, 47, 80])
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
    if step >= 3000: fool_out.append(s[0])

fool_rules = lambda pos, norm, seg, mean: (
    np.random.randint(50, 120),
    np.random.choice([1,2,4])
)
mel_fool = make_melody(np.array(fool_out), list(range(12)), fool_rules)
fool_mus = ce(np.array(fool_out)) * consonance(np.array(fool_out))
print(f"  Random ρ walk, chromatic, random dynamics")
print(f"  {len(mel_fool)} notes, musicality={fool_mus:.4f}")

# Comparison
print(f"\n{'='*50}")
print("ARCHETYPE COMPARISON")
print(f"{'='*50}")
results = [
    ('Warrior', warrior_mus, len(mel_warrior)),
    ('Lover', lover_mus, len(mel_lover)),
    ('Magician', magic_mus, len(mel_magic)),
    ('Sovereign', sov_mus, len(mel_sov)),
    ('Fool', fool_mus, len(mel_fool)),
]
for name, mus, n_notes in sorted(results, key=lambda x: -x[1]):
    bar = '█' * int(mus * 100)
    print(f"  {name:12s}: musicality={mus:.4f} {bar}")

winner = max(results, key=lambda x: x[1])
print(f"\n  The {winner[0]} archetype makes the best music.")
print(f"  (But the Fool might be the most interesting.)")

with open('/tmp/fm-research/CODE/EXPERIMENT-106-110.json', 'w') as f:
    json.dump({'archetypes': {name: mus for name, mus, _ in results}}, f, indent=2)
subprocess.run(['git','add','-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git','commit','-m','experiments 106-110: archetype experiments'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git','push'], cwd='/tmp/fm-research', capture_output=True)

print("\n=== 110 EXPERIMENTS — FIVE ARCHETYPES ===")
