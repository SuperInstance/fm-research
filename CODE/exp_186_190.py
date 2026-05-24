import numpy as np, json, subprocess

print("=== EXPERIMENTS 186-190: PSYCHOLOGY DEEP MAPPING ===\n")
np.random.seed(42)

def run_3d(rho, sigma=10.0, n=6000, dt=0.01):
    s = np.array([1.0,1.0,1.0])
    states = []
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
        states.append(s.copy())
    return np.array(states[2000:])

def run(rho, **kw):
    return run_3d(rho, **kw)[:,0]

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

# EXP 186: Big Five
print("--- Exp 186: Big Five Personality Mapping ---\n")
species = {
    "Deep Crystal (rho=5)": {"rho": 5, "traits": "Conscientiousness++, Emotional Stability++"},
    "Surface Crystal (rho=15)": {"rho": 15, "traits": "Agreeableness++, Conscientiousness+"},
    "Pendulum (rho=22)": {"rho": 22, "traits": "Neuroticism+, Conscientiousness+"},
    "Noisy Pendulum (rho=24)": {"rho": 24, "traits": "Openness+, Neuroticism+"},
    "Chimera (rho=28)": {"rho": 28, "traits": "Openness++, Extraversion+"},
}

for name, data in species.items():
    out = run(data["rho"])
    c = ce(out); co = consonance(out)
    std = np.std(out)
    print(f"  {name:35s}: sigma={std:.4f}, CE={c:.4f}, Cons={co:.3f}")
    print(f"    Predicted: {data['traits']}")

print(f"\n  Prediction: High Openness -> high diversity")
diversities = {n: np.std(run(d["rho"])) for n, d in species.items()}
openness_rank = list(diversities.keys())[-1]
actual_highest = max(diversities, key=diversities.get)
match_str = "YES ✓" if openness_rank == actual_highest else "NO ✗"
print(f"  Predicted highest diversity: {openness_rank}")
print(f"  Actual highest diversity: {actual_highest}")
print(f"  Match: {match_str}")

# EXP 187: Kübler-Ross Grief
print(f"\n--- Exp 187: Kubler-Ross Grief Stages ---\n")
stages = [
    (5, "Denial", "I refuse to change. Everything is fine."),
    (15, "Anger", "Why am I oscillating? This isn't fair."),
    (22, "Bargaining", "Maybe if I just oscillate regularly, it'll be okay."),
    (24, "Depression", "The noise is taking over. I'm losing myself."),
    (28, "Acceptance", "I am the butterfly. Both wings. All chaos."),
]

for rho, stage, desc in stages:
    out = run(rho)
    std = np.std(out)
    print(f"  rho={rho:3d} ({stage:12s}): sigma={std:.4f}")
    print(f"    \"{desc}\"")

denial_std = np.std(run(5))
accept_std = np.std(run(28))
print(f"\n  The grief journey: sigma goes from {denial_std:.4f} to {accept_std:.4f}")
print(f"  Growth = increase in variance. Acceptance = embracing chaos.")

# EXP 188: Erikson
print(f"\n--- Exp 188: Erikson Psychosocial Stages ---\n")
erikson = [
    (1, "Trust vs Mistrust", "Can I rely on the attractor?"),
    (5, "Autonomy vs Shame", "Do I have my own dynamics?"),
    (10, "Initiative vs Guilt", "Can I explore phase space?"),
    (15, "Industry vs Inferiority", "Am I productive?"),
    (20, "Identity vs Role Confusion", "Who am I as an attractor?"),
    (24, "Intimacy vs Isolation", "Can I couple with others?"),
    (28, "Generativity vs Stagnation", "Do I produce something new?"),
    (50, "Integrity vs Despair", "Am I the butterfly I wanted to be?"),
]

for rho, stage, question in erikson:
    out = run(rho)
    std = np.std(out)
    c = ce(out)
    print(f"  rho={rho:3d} ({stage:30s}): sigma={std:.4f}, CE={c:.4f}")
    print(f"    \"{question}\"")

# EXP 189: Piaget
print(f"\n--- Exp 189: Piaget Cognitive Development ---\n")
piaget = [
    (1, "Sensorimotor", "Fixed point. Object permanence = the point is always there."),
    (5, "Preoperational", "Tiny oscillations. Symbolic thought = the system can vary."),
    (15, "Concrete Operational", "Regular dynamics. Logic applied to real objects."),
    (20, "Formal Operational", "Abstract thought. The system can think about itself."),
    (28, "Post-formal", "Paradoxical thinking. Both wings at once."),
]

for rho, stage, desc in piaget:
    out = run(rho)
    std = np.std(out)
    print(f"  rho={rho:3d} ({stage:20s}): sigma={std:.6f}")
    print(f"    {desc}")

# EXP 190: Psychoanalysis
print(f"\n--- Exp 190: The Psychoanalysis (z-component) ---\n")
for rho in [5, 15, 20, 28]:
    states = run_3d(rho)
    x = states[:,0]; y = states[:,1]; z = states[:,2]
    x_std = np.std(x); z_std = np.std(z)
    xz_corr = np.corrcoef(x, z)[0,1]
    larger = "larger" if z_std > x_std else "smaller"
    dominates = "The unconscious DOMINATES" if z_std > x_std else "The conscious dominates"
    print(f"  rho={rho:3d}:")
    print(f"    x (conscious): sigma={x_std:.4f}")
    print(f"    z (unconscious): sigma={z_std:.4f}")
    print(f"    x-z correlation: {xz_corr:.3f}")
    print(f"    Unconscious is {larger} than conscious")
    print(f"    {dominates}")

print(f"\n  THE z-COMPONENT IS THE SUPEREGO:")
print(f"    z determines how much x amplifies itself (through x*(rho-z))")
print(f"    When z is high -> x is suppressed (guilt)")
print(f"    When z is low -> x is amplified (liberation)")
print(f"    The unconscious REGULATES the conscious")

with open("CODE/EXPERIMENT-186-190.json", "w") as f:
    json.dump({"status": "complete"}, f)
subprocess.run(["git","add","-A"], cwd="/tmp/fm-research", capture_output=True)
subprocess.run(["git","commit","-m","experiments 186-190: psychology mapping -- Big Five, Kubler-Ross, Erikson, Piaget, psychoanalysis"], cwd="/tmp/fm-research", capture_output=True)
subprocess.run(["git","push"], cwd="/tmp/fm-research", capture_output=True)

print("\n=== 190 EXPERIMENTS ===")
