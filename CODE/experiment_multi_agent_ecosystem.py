import numpy as np
import json

print("=== Experiment 32: Multi-Agent Creative Ecosystem ===\n")
print("10 agents with different expertise interact.\n")

np.random.seed(42)
dt = 0.01

class CreativeAgent:
    def __init__(self, name, expertise, role):
        self.name = name
        self.expertise = expertise  # 0-1 (beginner to master)
        self.role = role
        self.state = np.random.randn(3) * 0.1
        
        # Lorenz parameters based on expertise
        self.rho = 1 + expertise * 49  # beginner=1, master=50
        self.sigma = 10.0
        self.beta = 8/3
        
        # Automation level (higher expertise = more automated)
        self.automation = min(expertise, 0.9)
        
        # Creative bandwidth
        self.bandwidth = 1.0 - (1 - self.automation) * 0.3
        
        # Output history
        self.outputs = []
        self.quality_scores = []
    
    def step(self, coupling_signal=0.0, dt=0.01):
        x, y, z = self.state
        dx = self.sigma * (y - x)
        dy = x * (self.rho - z) - y
        dz = x * y - self.beta * z
        
        # Add coupling signal (from other agents)
        noise = np.random.randn(3) * (1 - self.automation) * 0.01
        
        self.state += np.array([dx, dy, dz]) * dt + noise * np.sqrt(dt)
        self.state[0] += coupling_signal * dt
        
        output = float(self.state[0])
        self.outputs.append(output)
        return output
    
    def get_quality(self):
        if len(self.outputs) < 100:
            return 0
        recent = np.array(self.outputs[-100:])
        novelty = float(np.std(recent))
        # Coherence
        fft = np.abs(np.fft.rfft(recent))
        fft_norm = fft / (fft.sum() + 1e-10)
        flatness = np.exp(np.mean(np.log(fft_norm + 1e-10))) / (np.mean(fft_norm) + 1e-10)
        coherence = 1 - flatness
        return novelty * coherence
    
    def get_diversity(self):
        if len(self.outputs) < 50:
            return 0
        return float(np.std(self.outputs[-50:]))

# Create the ecosystem
agents = [
    CreativeAgent("Beginner_1", 0.1, "student"),
    CreativeAgent("Beginner_2", 0.15, "student"),
    CreativeAgent("Intermediate_1", 0.35, "player"),
    CreativeAgent("Intermediate_2", 0.4, "player"),
    CreativeAgent("Advanced_1", 0.6, "soloist"),
    CreativeAgent("Advanced_2", 0.65, "soloist"),
    CreativeAgent("Expert_1", 0.8, "leader"),
    CreativeAgent("Expert_2", 0.85, "leader"),
    CreativeAgent("Master_1", 0.95, "director"),
    CreativeAgent("Master_2", 0.98, "director"),
]

# Part 1: Independent baselines
print("--- Part 1: Independent Baselines ---")

for agent in agents:
    for _ in range(5000):
        agent.step()
    div = agent.get_diversity()
    qual = agent.get_quality()
    print(f"  {agent.name:15s} (ρ={agent.rho:5.1f}): div={div:.4f}, quality={qual:.6f}")

# Part 2: Network coupling
print("\n--- Part 2: Coupled Ecosystem ---")

# Reset agents
for agent in agents:
    agent.state = np.random.randn(3) * 0.1
    agent.outputs = []

# Coupling matrix: who influences whom
# Structure: experts influence more, beginners receive more
coupling_matrix = np.zeros((10, 10))
for i, a1 in enumerate(agents):
    for j, a2 in enumerate(agents):
        if i != j:
            # Expertise-based coupling: experts broadcast, beginners receive
            coupling_matrix[i, j] = a2.expertise * 0.01

# Run coupled
T = 10000
for step in range(T):
    outputs = [agent.step() for agent in agents]
    
    # Apply coupling
    for i, agent in enumerate(agents):
        signal = sum(coupling_matrix[i, j] * outputs[j] for j in range(10) if j != i)
        agent.state[0] += signal * dt
    
    if step % 2000 == 0 and step > 0:
        print(f"\n  Step {step}:")
        for agent in agents:
            div = agent.get_diversity()
            qual = agent.get_quality()
            print(f"    {agent.name:15s}: div={div:.4f}, quality={qual:.6f}")

# Part 3: Ecosystem analysis
print("\n--- Part 3: Ecosystem Metrics ---")

# Correlation matrix
outputs_matrix = np.array([a.outputs[-1000:] for a in agents])
corr_matrix = np.corrcoef(outputs_matrix)

print("  Agent correlation matrix (last 1000 steps):")
for i, a1 in enumerate(agents):
    for j, a2 in enumerate(agents):
        if i < j and abs(corr_matrix[i, j]) > 0.5:
            print(f"    Strong: {a1.name} ↔ {a2.name}: r={corr_matrix[i,j]:.3f}")

# Who influenced whom most?
print("\n  Influence flow:")
for i, agent in enumerate(agents):
    total_influence = sum(coupling_matrix[j, i] for j in range(10) if j != i)
    influenced_by = sum(coupling_matrix[i, j] for j in range(10) if j != i)
    print(f"    {agent.name:15s}: broadcasts {total_influence:.3f}, receives {influenced_by:.3f}")

# Part 4: Quality by expertise level
print("\n--- Part 4: Quality vs Expertise ---")

expertise_quality = {}
for agent in agents:
    level = "beginner" if agent.expertise < 0.2 else "intermediate" if agent.expertise < 0.5 else \
            "advanced" if agent.expertise < 0.7 else "expert" if agent.expertise < 0.9 else "master"
    if level not in expertise_quality:
        expertise_quality[level] = []
    expertise_quality[level].append(agent.get_quality())

for level in ['beginner', 'intermediate', 'advanced', 'expert', 'master']:
    if level in expertise_quality:
        avg = np.mean(expertise_quality[level])
        print(f"  {level:15s}: avg quality = {avg:.6f}")

# Part 5: Ecosystem synergy
print("\n--- Part 5: Ecosystem Synergy ---")

# Compare: coupled vs uncoupled total quality
coupled_total = sum(a.get_quality() for a in agents)

# Reset and run uncoupled
for agent in agents:
    agent.state = np.random.randn(3) * 0.1
    agent.outputs = []

for step in range(T):
    for agent in agents:
        agent.step()

uncoupled_total = sum(a.get_quality() for a in agents)

synergy = (coupled_total / uncoupled_total - 1) * 100 if uncoupled_total > 0 else 0
print(f"  Coupled total quality: {coupled_total:.6f}")
print(f"  Uncoupled total quality: {uncoupled_total:.6f}")
print(f"  Synergy: {synergy:+.1f}%")
print(f"  {'ECOSYSTEM AMPLIFIES' if synergy > 0 else 'ECOSYSTEM DIMINISH'} output")

with open('CODE/EXPERIMENT-MULTI-AGENT-ECOSYSTEM.json', 'w') as f:
    json.dump({
        'correlation_matrix': corr_matrix.tolist(),
        'synergy_pct': float(synergy),
        'expertise_quality': {k: float(np.mean(v)) for k, v in expertise_quality.items()},
    }, f, indent=2)

print("\n=== MULTI-AGENT ECOSYSTEM ANALYSIS COMPLETE ===")
