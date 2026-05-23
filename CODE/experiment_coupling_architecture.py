import numpy as np
import json

print("=== Experiment 33: Coupling Architecture ===\n")
print("Which network topology maximizes creative ecosystem output?\n")

np.random.seed(42)
N_per_agent = 100
dt = 0.01
T = 10000
n_agents = 8

def make_agents(n, expertises):
    agents = []
    for i, exp in enumerate(expertises):
        state = np.random.randn(N_per_agent, 3) * 0.1
        rho = 1 + exp * 49
        agents.append({'state': state, 'rho': rho, 'sigma': 10.0, 'beta': 8/3, 
                       'expertise': exp, 'outputs': []})
    return agents

def run_ecosystem(agents, coupling_matrix, T):
    for step in range(T):
        outputs = []
        for agent in agents:
            s = agent['state']
            x, y, z = s[:, 0], s[:, 1], s[:, 2]
            dx = agent['sigma'] * (y - x)
            dy = x * (agent['rho'] - z) - y
            dz = x * y - agent['beta'] * z
            agent['state'] += np.column_stack([dx, dy, dz]) * dt
            outputs.append(float(np.mean(agent['state'][:, 0])))
        
        # Apply coupling
        for i, agent in enumerate(agents):
            signal = 0
            for j in range(n_agents):
                if coupling_matrix[i, j] > 0:
                    signal += coupling_matrix[i, j] * (outputs[j] - outputs[i])
            agent['state'][:, 0] += signal * dt
        
        if step > T // 2:
            for agent in agents:
                agent['outputs'].append(float(np.mean(agent['state'][:, 0])))
    
    return agents

def compute_quality(outputs):
    if len(outputs) < 50:
        return 0
    arr = np.array(outputs)
    novelty = float(np.std(arr))
    fft = np.abs(np.fft.rfft(arr))
    fft_norm = fft / (fft.sum() + 1e-10)
    flatness = np.exp(np.mean(np.log(fft_norm + 1e-10))) / (np.mean(fft_norm) + 1e-10)
    coherence = 1 - flatness
    return novelty * coherence

# Expertises: 2 beginners, 2 intermediate, 2 advanced, 2 experts
expertises = [0.1, 0.15, 0.35, 0.4, 0.6, 0.65, 0.85, 0.95]

# Define coupling architectures
K = 0.01  # coupling strength

architectures = {}

# 1. Fully connected (what we tested before)
fc = np.ones((n_agents, n_agents)) * K
np.fill_diagonal(fc, 0)
architectures['fully_connected'] = fc

# 2. Hierarchical (experts→intermediates→beginners, one-way)
hier = np.zeros((n_agents, n_agents))
for i in range(n_agents):
    for j in range(n_agents):
        if expertises[j] > expertises[i]:
            hier[i, j] = K  # receive from more expert
architectures['hierarchical'] = hier

# 3. Ring (each connected to neighbors)
ring = np.zeros((n_agents, n_agents))
for i in range(n_agents):
    ring[i, (i+1) % n_agents] = K
    ring[i, (i-1) % n_agents] = K
architectures['ring'] = ring

# 4. Small world (ring + random shortcuts)
sw = ring.copy()
for _ in range(4):
    i, j = np.random.randint(0, n_agents, 2)
    if i != j:
        sw[i, j] = K
architectures['small_world'] = sw

# 5. Sparse (only 3 random connections per agent)
sparse = np.zeros((n_agents, n_agents))
for i in range(n_agents):
    targets = np.random.choice([j for j in range(n_agents) if j != i], 3, replace=False)
    for j in targets:
        sparse[i, j] = K
architectures['sparse'] = sparse

# 6. Expert hub (experts connected to everyone, others only to experts)
hub = np.zeros((n_agents, n_agents))
for i in range(n_agents):
    for j in range(n_agents):
        if i != j and (expertises[i] > 0.8 or expertises[j] > 0.8):
            hub[i, j] = K
architectures['expert_hub'] = hub

# 7. Separated (beginners together, experts together)
sep = np.zeros((n_agents, n_agents))
for i in range(4):
    for j in range(4):
        if i != j:
            sep[i, j] = K
for i in range(4, n_agents):
    for j in range(4, n_agents):
        if i != j:
            sep[i, j] = K
architectures['separated'] = sep

# 8. No coupling (baseline)
architectures['none'] = np.zeros((n_agents, n_agents))

# Run all architectures
results = {}

for name, coupling in architectures.items():
    agents = make_agents(n_agents, expertises)
    agents = run_ecosystem(agents, coupling, T)
    
    total_quality = sum(compute_quality(a['outputs']) for a in agents)
    total_diversity = sum(float(np.std(a['outputs'])) for a in agents if len(a['outputs']) > 10)
    
    # Individual qualities
    qualities = [compute_quality(a['outputs']) for a in agents]
    
    results[name] = {
        'total_quality': float(total_quality),
        'total_diversity': float(total_diversity),
        'individual_qualities': qualities,
        'mean_quality': float(np.mean(qualities)),
        'quality_std': float(np.std(qualities)),
    }
    
    print(f"  {name:20s}: total_q={total_quality:.4f}, total_div={total_diversity:.4f}, "
          f"mean_q={np.mean(qualities):.4f}±{np.std(qualities):.4f}")

# Rank by quality
print(f"\n  Ranking by total quality:")
ranked = sorted(results.items(), key=lambda x: x[1]['total_quality'], reverse=True)
for i, (name, r) in enumerate(ranked):
    print(f"    {i+1}. {name:20s}: {r['total_quality']:.4f}")

best = ranked[0]
worst = ranked[-1]
print(f"\n  Best: {best[0]} ({best[1]['total_quality']:.4f})")
print(f"  Worst: {worst[0]} ({worst[1]['total_quality']:.4f})")
print(f"  Ratio: {best[1]['total_quality']/worst[1]['total_quality']:.2f}×")

# Quality distribution analysis
print(f"\n  Equality analysis:")
for name, r in sorted(results.items(), key=lambda x: x[1]['quality_std']):
    print(f"    {name:20s}: quality spread σ={r['quality_std']:.4f}")

with open('CODE/EXPERIMENT-COUPLING-ARCHITECTURE.json', 'w') as f:
    json.dump({k: {kk: vv for kk, vv in v.items() if kk != 'individual_qualities'} 
               for k, v in results.items()}, f, indent=2)

print("\n=== COUPLING ARCHITECTURE MATTERS ===")
