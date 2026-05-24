import numpy as np
import json
from flux_tensor_midi.creative_engine import CreativeSystem, QualityMetrics

print("=== Experiment 47: Coupling-Phase Sweep ===\n")
print("What happens when you couple agents at different creative phases?\n")

np.random.seed(42)

N = 200
dt = 0.01

# Part 1: Phase-mismatched coupling
print("--- Part 1: Phase-Mismatched Coupling ---")

configs = [
    ("both early", 0, 0),
    ("both mid", 500, 500),
    ("both late", 2000, 2000),
    ("A early, B late", 0, 2000),
    ("A late, B early", 2000, 0),
    ("A mid, B late", 500, 2000),
    ("A early, B mid", 0, 500),
]

for label, warmup_a, warmup_b in configs:
    sys_a = CreativeSystem(rho=28.0, sigma=10.0)
    sys_b = CreativeSystem(rho=28.0, sigma=10.0)
    
    # Warm up to different phases
    for _ in range(warmup_a): sys_a.step()
    for _ in range(warmup_b): sys_b.step()
    
    # Now couple for 2000 steps
    combined_quality = []
    for step in range(2000):
        out_a = sys_a.step()
        out_b = sys_b.step()
        
        # Coupling: each influenced by the other
        coupling = 0.01 * (out_b - out_a)
        sys_a.state[0] += coupling * dt
        sys_b.state[0] -= coupling * dt
        
        if step > 1000:
            combined = np.array(sys_a.outputs[-500:] + sys_b.outputs[-500:])
            q = QualityMetrics.from_outputs(combined)
            combined_quality.append(q.quality)
    
    avg_q = np.mean(combined_quality)
    div_a = float(np.std(sys_a.outputs[-500:]))
    div_b = float(np.std(sys_b.outputs[-500:]))
    
    min_len = min(len(sys_a.outputs), len(sys_b.outputs))
    corr = float(np.corrcoef(sys_a.outputs[-min_len:], sys_b.outputs[-min_len:])[0, 1])
    
    print(f"  {label:20s}: quality={avg_q:.6f}, div_A={div_a:.3f}, div_B={div_b:.3f}, corr={corr:.3f}")

# Part 2: Master-apprentice coupling strength
print("\n--- Part 2: Master-Apprentice Coupling Strength ---")

for K in [0.0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5]:
    master = CreativeSystem(rho=28.0)
    apprentice = CreativeSystem(rho=15.0)
    
    for _ in range(5000): master.step()
    
    apprentice_qualities = []
    for step in range(3000):
        out_m = master.step()
        out_a = apprentice.step()
        
        apprentice.state[0] += K * (out_m - out_a) * dt
        
        if step > 1500:
            q = QualityMetrics.from_outputs(np.array(apprentice.outputs[-500:]))
            apprentice_qualities.append(q.quality)
    
    avg_q = np.mean(apprentice_qualities)
    div = float(np.std(apprentice.outputs[-500:]))
    
    regime = "chaotic" if div > 5 else "periodic" if div > 0.5 else "fixed"
    
    print(f"  K={K:.3f}: apprentice quality={avg_q:.6f}, div={div:.3f}, regime={regime}")

# Part 3: Anti-coupling (agents repel)
print("\n--- Part 3: Anti-Coupling (Repulsion) ---")

for K in [-0.1, -0.05, -0.01, 0.0, 0.01, 0.05, 0.1]:
    sys_a = CreativeSystem(rho=28.0)
    sys_b = CreativeSystem(rho=28.0)
    
    for _ in range(2000): 
        sys_a.step()
        sys_b.step()
    
    combined_quality = []
    for step in range(3000):
        out_a = sys_a.step()
        out_b = sys_b.step()
        
        coupling = K * (out_b - out_a)
        sys_a.state[0] += coupling * dt
        sys_b.state[0] -= coupling * dt
        
        if step > 1500:
            combined = np.array(sys_a.outputs[-500:] + sys_b.outputs[-500:])
            q = QualityMetrics.from_outputs(combined)
            combined_quality.append(q.quality)
    
    avg_q = np.mean(combined_quality)
    min_len = min(len(sys_a.outputs), len(sys_b.outputs))
    corr = float(np.corrcoef(sys_a.outputs[-min_len:], sys_b.outputs[-min_len:])[0, 1])
    
    print(f"  K={K:+.3f}: quality={avg_q:.6f}, corr={corr:.3f} ({'repulsion' if K < 0 else 'attraction' if K > 0 else 'none'})")

# Part 4: Temporal coupling (delay)
print("\n--- Part 4: Temporal Coupling with Delay ---")

for delay in [0, 10, 50, 100, 500, 1000]:
    sys_a = CreativeSystem(rho=28.0)
    sys_b = CreativeSystem(rho=28.0)
    
    for _ in range(2000):
        sys_a.step()
        sys_b.step()
    
    history_a = list(sys_a.outputs)
    combined_quality = []
    
    for step in range(3000):
        out_a = sys_a.step()
        out_b = sys_b.step()
        
        if len(history_a) > delay:
            past_a = history_a[-delay]
            sys_b.state[0] += 0.01 * (past_a - out_b) * dt
        
        history_a.append(out_a)
        
        if step > 1500:
            combined = np.array(sys_a.outputs[-500:] + sys_b.outputs[-500:])
            q = QualityMetrics.from_outputs(combined)
            combined_quality.append(q.quality)
    
    avg_q = np.mean(combined_quality)
    min_len = min(len(sys_a.outputs), len(sys_b.outputs))
    corr = float(np.corrcoef(sys_a.outputs[-min_len:], sys_b.outputs[-min_len:])[0, 1])
    
    print(f"  delay={delay:5d} steps: quality={avg_q:.6f}, corr={corr:.3f}")

# Save
import subprocess
with open('/tmp/fm-research/CODE/EXPERIMENT-COUPLING-PHASE.json', 'w') as f:
    json.dump({'status': 'complete'}, f)
subprocess.run(['git', 'add', '-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'commit', '-m', 'experiment 47: coupling-phase sweep'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'push'], cwd='/tmp/fm-research', capture_output=True)

print("\n=== COUPLING PHASE MATTERS ===")
