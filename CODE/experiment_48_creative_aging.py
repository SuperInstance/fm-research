import numpy as np
import json
from flux_tensor_midi.creative_engine import CreativeSystem, QualityMetrics

print("=== Experiment 48: Creative Aging ===\n")
print("How does creative output change over a 'career'?\n")

np.random.seed(42)

N_SYSTEMS = 20
CAREER_LENGTH = 50000
CHECKPOINT_EVERY = 2500

results = []

for artist_id in range(N_SYSTEMS):
    rho = np.random.uniform(25, 35)
    sigma = np.random.uniform(8, 12)
    
    sys = CreativeSystem(rho=rho, sigma=sigma)
    
    career = []
    
    for step in range(CAREER_LENGTH):
        sys.step()
        
        if step > 0 and step % CHECKPOINT_EVERY == 0:
            recent = np.array(sys.outputs[-CHECKPOINT_EVERY:])
            q = QualityMetrics.from_outputs(recent)
            diversity = float(np.std(recent))
            ac = float(np.corrcoef(recent[:-1], recent[1:])[0, 1])
            mean_output = np.mean(sys.outputs) if len(sys.outputs) > 0 else 0
            novelty_rate = float(np.mean(np.abs(recent - mean_output) > 2 * np.std(recent)))
            
            career.append({
                'step': step,
                'age_pct': step / CAREER_LENGTH * 100,
                'quality': q.quality,
                'novelty': q.novelty,
                'coherence': q.coherence,
                'diversity': diversity,
                'autocorr': ac,
                'novelty_rate': novelty_rate,
            })
    
    peak = max(career, key=lambda c: c['quality'])
    
    results.append({
        'artist': artist_id,
        'rho': rho,
        'sigma': sigma,
        'peak_age': peak['age_pct'],
        'peak_quality': peak['quality'],
        'final_quality': career[-1]['quality'],
        'career': career,
    })

print("  Artist Careers:")
print(f"  {'Artist':>8s} {'ρ':>6s} {'σ':>6s} {'Peak Age':>10s} {'Peak Q':>10s} {'Final Q':>10s} {'Decline':>10s}")
print(f"  {'-'*60}")

for r in results:
    decline = r['peak_quality'] - r['final_quality']
    print(f"  {r['artist']:8d} {r['rho']:6.1f} {r['sigma']:6.1f} {r['peak_age']:10.1f}% {r['peak_quality']:10.4f} {r['final_quality']:10.4f} {decline:10.4f}")

peak_ages = [r['peak_age'] for r in results]
print(f"\n  Peak age distribution:")
print(f"    Mean: {np.mean(peak_ages):.1f}%")
print(f"    Median: {np.median(peak_ages):.1f}%")
print(f"    Range: {min(peak_ages):.1f}% — {max(peak_ages):.1f}%")

print(f"\n  Quality trajectory (averaged over {N_SYSTEMS} artists):")
ages = sorted(set(c['age_pct'] for r in results for c in r['career']))
for age in ages[::2]:
    qualities = [c['quality'] for r in results for c in r['career'] if c['age_pct'] == age]
    avg_q = np.mean(qualities)
    bar = '█' * int(avg_q * 2)
    print(f"    age={age:5.1f}%: quality={avg_q:.4f} {bar}")

print("\n--- Part 2: Mid-Career Crisis & Revival ---")

for perturbation in [0.0, 0.1, 0.5, 1.0, 2.0, 5.0]:
    sys = CreativeSystem(rho=28.0)
    
    for _ in range(25000): sys.step()
    
    q_before = QualityMetrics.from_outputs(np.array(sys.outputs[-2500:])).quality
    
    for _ in range(100):
        sys.state += np.random.randn(3) * perturbation
    
    for _ in range(25000): sys.step()
    
    q_after = QualityMetrics.from_outputs(np.array(sys.outputs[-2500:])).quality
    
    change = (q_after - q_before) / q_before * 100 if q_before > 0 else 0
    
    print(f"  Perturbation {perturbation:.1f}: quality {q_before:.4f} → {q_after:.4f} ({change:+.1f}%)")

print("\n--- Part 3: Wisdom (accumulated knowledge) ---")

sys_old = CreativeSystem(rho=28.0)
sys_young = CreativeSystem(rho=28.0)

for _ in range(50000): sys_old.step()
sys_old.outputs = []
for _ in range(5000): sys_old.step()

for _ in range(5000): sys_young.step()

q_old = sys_old.quality()
q_young = sys_young.quality()

print(f"  Old system (50K steps + fresh 5K): quality={q_old.quality:.6f}")
print(f"  Young system (5K steps): quality={q_young.quality:.6f}")
print(f"  {'Wisdom advantage' if q_old.quality > q_young.quality else 'Youth advantage'}")

import subprocess
with open('/tmp/fm-research/CODE/EXPERIMENT-CREATIVE-AGING.json', 'w') as f:
    json.dump({
        'peak_ages': peak_ages,
        'n_artists': N_SYSTEMS,
        'career_length': CAREER_LENGTH,
    }, f, indent=2)
subprocess.run(['git', 'add', '-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'commit', '-m', 'experiment 48: creative aging — career arcs'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'push'], cwd='/tmp/fm-research', capture_output=True)

print("\n=== CREATIVE CAREERS HAVE ARCS ===")
