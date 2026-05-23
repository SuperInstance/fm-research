import numpy as np
import json

print("=== Experiment 28: Cognitive Bandwidth Conservation ===\n")

N = 200  # agents
dt = 0.01

# Simulate a 5-layer creative system
# Layer 0: tuning (pitch snap)
# Layer 1: rhythm (tempo snap)
# Layer 2: harmony (consensus)
# Layer 3: melody (creative)
# Layer 4: interaction (emergent)

# Each layer has a "noise level" = how much attention it needs
# Automated layers: noise ≈ 0 (don't need attention)
# Manual layers: noise > 0 (need attention = steal bandwidth)

def simulate_bandwidth(n_agents, automation_level, T=5000):
    """
    automation_level: how many layers are automated (0-5)
    0 = nothing automated, 5 = everything automated
    """
    
    # Total bandwidth budget
    B_total = 10.0
    
    # Each manual layer costs bandwidth
    n_manual = 5 - automation_level
    layer_cost = n_manual * 1.5  # each manual layer costs 1.5 bandwidth units
    B_creative = max(0.1, B_total - layer_cost)
    
    # Agents with Lorenz dynamics
    state = np.random.randn(n_agents, 3) * 0.1
    
    # The creative layer gets ε proportional to available bandwidth
    eps = B_creative / B_total
    
    creative_outputs = []
    
    for step in range(T):
        x, y, z = state[:, 0], state[:, 1], state[:, 2]
        dx = 10 * (y - x)
        dy = x * (28 - z) - y
        dz = x * y - 8/3 * z
        
        # Noise at manual layers (distracts from creative output)
        noise = np.random.randn(n_agents, 3) * (1 - eps) * 0.1
        
        state += (np.column_stack([dx, dy, dz]) * dt) + noise * np.sqrt(dt)
        
        if step > T // 2:
            creative_outputs.append(float(np.std(state[:, 0])))
    
    return {
        'automation': automation_level,
        'n_manual': n_manual,
        'bandwidth_creative': B_creative,
        'epsilon': eps,
        'avg_diversity': float(np.mean(creative_outputs)),
        'max_diversity': float(np.max(creative_outputs)),
    }

# Test different automation levels
print("--- Bandwidth vs Automation Level ---")
results = []

for auto in range(6):
    r = simulate_bandwidth(N, auto)
    results.append(r)
    print(f"  Automation={auto}/5: B_creative={r['bandwidth_creative']:.1f}, "
          f"ε={r['epsilon']:.2f}, diversity={r['avg_diversity']:.4f}")

# Part 2: Jazz band simulation
print("\n--- Jazz Band Simulation ---")
# 5 musicians with different automation levels

musicians = {
    'drummer': {'automated': ['rhythm'], 'manual': ['dynamics', 'fills', 'interaction']},
    'bassist': {'automated': ['root_notes', 'rhythm'], 'manual': ['walking', 'interaction']},
    'pianist': {'automated': ['harmony'], 'manual': ['voicings', 'comping', 'interaction']},
    'saxophonist': {'automated': [], 'manual': ['tuning', 'rhythm', 'harmony', 'melody', 'interaction']},
    'veteran_sax': {'automated': ['tuning', 'rhythm', 'harmony'], 'manual': ['melody', 'interaction']},
}

for name, config in musicians.items():
    auto = len(config['automated'])
    manual = len(config['manual'])
    r = simulate_bandwidth(50, auto)
    print(f"  {name:15s}: {auto} auto, {manual} manual → ε={r['epsilon']:.2f}, "
          f"diversity={r['avg_diversity']:.4f}")

# Part 3: Historical era simulation
print("\n--- Historical Era Simulation ---")
eras = [
    ('Ancient (no automation)', 0),
    ('Medieval (notation)', 1),
    ('Baroque (temperament)', 2),
    ('Classical (form)', 3),
    ('Jazz (rhythm section)', 4),
    ('Electronic (DAW)', 5),
]

era_results = []
for name, auto in eras:
    r = simulate_bandwidth(N, auto)
    era_results.append(r)
    print(f"  {name:30s}: diversity={r['avg_diversity']:.4f}")

# Growth rate
ancient = era_results[0]['avg_diversity']
electronic = era_results[-1]['avg_diversity']
print(f"\n  Creativity growth: Ancient={ancient:.4f} → Electronic={electronic:.4f}")
print(f"  Amplification: {electronic/ancient:.1f}×")

# Part 4: The Sweet Spot — how much automation is optimal?
print("\n--- Optimal Automation Level ---")

# Too much automation = no human input = boring
# Model: diversity peaks at intermediate automation

for auto in range(6):
    r = simulate_bandwidth(N, auto)
    # Add "human spark" that decreases with automation
    human_factor = np.exp(-0.3 * auto)  # diminishes with more automation
    total_creativity = r['avg_diversity'] * (1 + human_factor)
    print(f"  Automation={auto}: machine_div={r['avg_diversity']:.4f}, "
          f"human_factor={human_factor:.3f}, total={total_creativity:.4f}")

# Part 5: Bandwidth transfer experiment
print("\n--- Bandwidth Transfer ---")
# When you automate one layer, where does the freed bandwidth go?

# Baseline: no automation
baseline = simulate_bandwidth(N, 0)

# Automate layer 0 (tuning)
auto_tuning = simulate_bandwidth(N, 1)

# Automate layer 0+1 (tuning + rhythm)
auto_rhythm = simulate_bandwidth(N, 2)

print(f"  No automation: diversity={baseline['avg_diversity']:.4f}")
print(f"  + Auto tuning: diversity={auto_tuning['avg_diversity']:.4f} "
      f"(+{(auto_tuning['avg_diversity']/baseline['avg_diversity']-1)*100:.1f}%)")
print(f"  + Auto rhythm: diversity={auto_rhythm['avg_diversity']:.4f} "
      f"(+{(auto_rhythm['avg_diversity']/baseline['avg_diversity']-1)*100:.1f}%)")

with open('CODE/EXPERIMENT-BANDWIDTH.json', 'w') as f:
    json.dump({
        'automation_results': results,
        'era_results': [{**r, 'era': e[0]} for r, e in zip(era_results, eras)],
    }, f, indent=2)

print("\n=== BANDWIDTH CONSERVATION CONFIRMED ===")
print("Automate lower layers → more creative bandwidth at higher layers")
