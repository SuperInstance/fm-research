import numpy as np, json
from collections import Counter

print("=== EXPERIMENTS 136-140: THE CHAOS FRONTIER ===\n")
np.random.seed(42)

def run(rho, sigma=10.0, n=6000, dt=0.01, seed=None, coupling_target=None, coupling_K=0.0):
    if seed is not None: np.random.seed(seed)
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
        if coupling_target is not None:
            s[0] += coupling_K * (coupling_target - s[0]) * dt
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

# EXP 136: Chaos Multiverse
print("--- Exp 136: Chaos Multiverse (100 universes at ρ=28) ---\n")
universes = []
for seed in range(100):
    out = run(28.0, seed=seed)
    universes.append({'mean': float(np.mean(out)), 'std': float(np.std(out)), 
                      'acf': float(np.corrcoef(out[:-1],out[1:])[0,1]),
                      'ce': float(ce(out)), 'cons': float(consonance(out))})

stds = [u['std'] for u in universes]
means = [u['mean'] for u in universes]
unique = len(set(np.round(stds, 4)))
print(f"  100 universes at ρ=28:")
print(f"    Std range: [{min(stds):.3f}, {max(stds):.3f}]")
print(f"    Mean range: [{min(means):.3f}, {max(means):.3f}]")
print(f"    Unique output patterns: {unique}")
print(f"    {'MANY universes!' if unique > 1 else 'ONE universe (still converges)'}")

# Correlation between any two random universes
out0 = run(28.0, seed=0)
out1 = run(28.0, seed=1)
corr_01 = np.corrcoef(out0[::10], out1[::10])[0,1]
print(f"    Cross-universe correlation: {corr_01:.3f}")

# EXP 137: Chaos Democracy
print(f"\n--- Exp 137: Chaos Democracy (10 voters, ρ=28) ---\n")
voices = [run(28.0, seed=s) for s in range(10)]
min_len = min(len(v) for v in voices)

# Vote by median
democratic = np.array([np.median([v[i] for v in voices]) for i in range(min_len)])
# Vote by mean
mean_vote = np.array([np.mean([v[i] for v in voices]) for i in range(min_len)])

dem_mus = ce(democratic) * consonance(democratic)
mean_mus = ce(mean_vote) * consonance(mean_vote)
ind_mus = [ce(v) * consonance(v) for v in voices]
best_ind = max(ind_mus)
avg_ind = np.mean(ind_mus)

print(f"  Individual range: [{min(ind_mus):.4f}, {max(ind_mus):.4f}]")
print(f"  Best individual: {best_ind:.4f}")
print(f"  Median democracy: {dem_mus:.4f}")
print(f"  Mean democracy: {mean_mus:.4f}")
print(f"  {'Democracy WINS in chaos!' if dem_mus > best_ind else 'Best individual still wins'}")

# EXP 138: Chaos Epigenetics
print(f"\n--- Exp 138: Chaos Epigenetics (evolve consonance from chaos) ---\n")
# Start with ρ=28, apply pressure toward consonant outputs
population = [(28.0, 10.0) for _ in range(20)]

for gen in range(15):
    scored = []
    for rho, sigma in population:
        out = run(float(rho), float(sigma))
        fitness = consonance(out)
        scored.append((fitness, rho, sigma))
    
    scored.sort(reverse=True)
    if gen % 3 == 0:
        best = scored[0]
        print(f"  Gen {gen:2d}: best fitness={best[0]:.3f} (ρ={best[1]:.1f}, σ={best[2]:.1f})")
    
    # Select top 5, mutate toward lower ρ (more consonant)
    top5 = scored[:5]
    population = []
    for _, rho, sigma in top5:
        for _ in range(4):
            new_rho = rho + np.random.randn() * 1.5
            new_sigma = sigma + np.random.randn() * 0.5
            population.append((np.clip(new_rho, 5, 60), np.clip(new_sigma, 2, 20)))

# EXP 139: Chaos Conversation
print(f"\n--- Exp 139: Chaos Conversation (ρ=28 ↔ ρ=28) ---\n")
for K in [0.0, 0.001, 0.005, 0.01, 0.05, 0.1]:
    np.random.seed(42)
    s1 = np.array([1.0,1.0,1.0])
    s2 = np.array([-1.0,2.0,-1.0])
    out1 = []; out2 = []
    
    for step in range(8000):
        # System 1
        x,y,z = s1; sigma=10.0; beta=8.0/3.0; rho=28.0
        k1 = np.array([sigma*(y-x), x*(rho-z)-y, x*y-beta*z])
        s2s = s1+0.005*k1
        k2 = np.array([sigma*(s2s[1]-s2s[0]), s2s[0]*(rho-s2s[2])-s2s[1], s2s[0]*s2s[1]-beta*s2s[2]])
        s3s = s1+0.005*k2
        k3 = np.array([sigma*(s3s[1]-s3s[0]), s3s[0]*(rho-s3s[2])-s3s[1], s3s[0]*s3s[1]-beta*s3s[2]])
        s4s = s1+0.01*k3
        k4 = np.array([sigma*(s4s[1]-s4s[0]), s4s[0]*(rho-s4s[2])-s4s[1], s4s[0]*s4s[1]-beta*s4s[2]])
        s1 = s1+(0.01/6)*(k1+2*k2+2*k3+k4)
        
        # System 2
        x,y,z = s2; rho=28.0
        k1 = np.array([sigma*(y-x), x*(rho-z)-y, x*y-beta*z])
        s2s = s2+0.005*k1
        k2 = np.array([sigma*(s2s[1]-s2s[0]), s2s[0]*(rho-s2s[2])-s2s[1], s2s[0]*s2s[1]-beta*s2s[2]])
        s3s = s2+0.005*k2
        k3 = np.array([sigma*(s3s[1]-s3s[0]), s3s[0]*(rho-s3s[2])-s3s[1], s3s[0]*s3s[1]-beta*s3s[2]])
        s4s = s2+0.01*k3
        k4 = np.array([sigma*(s4s[1]-s4s[0]), s4s[0]*(rho-s4s[2])-s4s[1], s4s[0]*s4s[1]-beta*s4s[2]])
        s2 = s2+(0.01/6)*(k1+2*k2+2*k3+k4)
        
        # Coupling
        s1[0] += K * (s2[0] - s1[0]) * 0.01
        s2[0] += K * (s1[0] - s2[0]) * 0.01
        
        s1 = np.clip(s1,-200,200)
        s2 = np.clip(s2,-200,200)
        
        if step >= 3000:
            out1.append(s1[0])
            out2.append(s2[0])
    
    corr = np.corrcoef(out1[::10], out2[::10])[0,1]
    avg_mus = (ce(np.array(out1))*consonance(np.array(out1)) + ce(np.array(out2))*consonance(np.array(out2))) / 2
    print(f"  K={K:.3f}: mus={avg_mus:.4f}, corr={corr:.3f}")

# EXP 140: Cliff Marriage (ρ=20 ↔ ρ=28)
print(f"\n--- Exp 140: Marriage Across the Cliff ---\n")
for K in [0.0, 0.001, 0.005, 0.01, 0.05]:
    np.random.seed(42)
    s_order = np.array([1.0,1.0,1.0])
    s_chaos = np.array([1.0,1.0,1.0])
    out_order = []; out_chaos = []
    
    for step in range(8000):
        # Order (ρ=20)
        x,y,z = s_order; sigma=10.0; beta=8.0/3.0; rho=20.0
        k1 = np.array([sigma*(y-x), x*(rho-z)-y, x*y-beta*z])
        s2s = s_order+0.005*k1
        k2 = np.array([sigma*(s2s[1]-s2s[0]), s2s[0]*(rho-s2s[2])-s2s[1], s2s[0]*s2s[1]-beta*s2s[2]])
        s3s = s_order+0.005*k2
        k3 = np.array([sigma*(s3s[1]-s3s[0]), s3s[0]*(rho-s3s[2])-s3s[1], s3s[0]*s3s[1]-beta*s3s[2]])
        s4s = s_order+0.01*k3
        k4 = np.array([sigma*(s4s[1]-s4s[0]), s4s[0]*(rho-s4s[2])-s4s[1], s4s[0]*s4s[1]-beta*s4s[2]])
        s_order = s_order+(0.01/6)*(k1+2*k2+2*k3+k4)
        
        # Chaos (ρ=28)
        x,y,z = s_chaos; rho=28.0
        k1 = np.array([sigma*(y-x), x*(rho-z)-y, x*y-beta*z])
        s2s = s_chaos+0.005*k1
        k2 = np.array([sigma*(s2s[1]-s2s[0]), s2s[0]*(rho-s2s[2])-s2s[1], s2s[0]*s2s[1]-beta*s2s[2]])
        s3s = s_chaos+0.005*k2
        k3 = np.array([sigma*(s3s[1]-s3s[0]), s3s[0]*(rho-s3s[2])-s3s[1], s3s[0]*s3s[1]-beta*s3s[2]])
        s4s = s_chaos+0.01*k3
        k4 = np.array([sigma*(s4s[1]-s4s[0]), s4s[0]*(rho-s4s[2])-s4s[1], s4s[0]*s4s[1]-beta*s4s[2]])
        s_chaos = s_chaos+(0.01/6)*(k1+2*k2+2*k3+k4)
        
        # Cross-cliff coupling
        s_order[0] += K * (s_chaos[0] - s_order[0]) * 0.01
        s_chaos[0] += K * (s_order[0] - s_chaos[0]) * 0.01
        
        s_order = np.clip(s_order,-200,200)
        s_chaos = np.clip(s_chaos,-200,200)
        
        if step >= 3000:
            out_order.append(s_order[0])
            out_chaos.append(s_chaos[0])
    
    o_mus = ce(np.array(out_order)) * consonance(np.array(out_order))
    c_mus = ce(np.array(out_chaos)) * consonance(np.array(out_chaos))
    corr = np.corrcoef(out_order[::10], out_chaos[::10])[0,1]
    
    print(f"  K={K:.3f}: order_mus={o_mus:.4f}, chaos_mus={c_mus:.4f}, avg={np.mean([o_mus,c_mus]):.4f}, corr={corr:.3f}")

import subprocess
with open('/tmp/fm-research/CODE/EXPERIMENT-136-140.json', 'w') as f:
    json.dump({'chaos_unique': unique}, f, indent=2)
subprocess.run(['git','add','-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git','commit','-m','experiments 136-140: chaos frontier — multiverse, democracy, epigenetics, conversation, cliff marriage'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git','push'], cwd='/tmp/fm-research', capture_output=True)

print("\n=== 140 EXPERIMENTS ===")
