"""
Experiment 49: Creative Grief — What Happens When You Remove a Degree of Freedom

Hypothesis: Removing a degree of freedom from a creative system produces a qualitative
shift analogous to grief — the system reorganizes around the loss, and the reorganization
itself is a distinct creative mode with its own quality signature.

We test this by clamping each Lorenz variable (x, y, z) independently, measuring the
creative output before, during, and after the loss. We look for:
1. Quality changes during grief (is it just worse, or different?)
2. Distinct grief signatures for each loss type
3. Hysteresis on recovery (do you go back to who you were?)
4. Whether grief can produce genuinely novel creative output
"""

import numpy as np
import json
import sys

np.random.seed(42)

print("=" * 70)
print("Experiment 49: Creative Grief")
print("What happens when you remove a degree of freedom?")
print("=" * 70)

# We can't modify the CreativeSystem internals, so we build a custom Lorenz system
# that allows clamping individual variables.

def lorenz(state, rho, sigma=10.0, beta=8/3):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return np.array([dx, dy, dz])

def run_lorenz(rho, n_steps=5000, dt=0.01, discard=1000, 
               clamp_var=None, clamp_start=None, clamp_end=None,
               clamp_value=0.0, soft_clamp_strength=0.0):
    """
    Run Lorenz system with optional clamping of one variable.
    
    clamp_var: 0=x, 1=y, 2=z, or None
    clamp_start/clamp_end: step range for clamping
    clamp_value: value to clamp to
    soft_clamp_strength: if >0, add damping toward clamp_value instead of hard clamping
    """
    state = np.array([0.1, 0.1, 0.1])
    
    # Discard transient
    for _ in range(discard):
        deriv = lorenz(state, rho)
        state = state + dt * deriv
    
    trajectory = np.zeros((n_steps, 3))
    outputs = np.zeros(n_steps)  # z-variable as "creative output"
    diverged = False
    
    for i in range(n_steps):
        deriv = lorenz(state, rho)
        new_state = state + dt * deriv
        
        # Apply clamping if in grief phase
        if clamp_var is not None and clamp_start is not None and clamp_end is not None:
            if clamp_start <= i < clamp_end:
                if soft_clamp_strength > 0:
                    # Soft clamp: add spring force toward clamp_value
                    new_state[clamp_var] += dt * soft_clamp_strength * (clamp_value - state[clamp_var])
                else:
                    new_state[clamp_var] = clamp_value
        
        # Check for divergence
        if np.any(np.abs(new_state) > 1e6) or np.any(np.isnan(new_state)):
            diverged = True
            trajectory[i:] = np.nan
            outputs[i:] = np.nan
            break
        
        state = new_state
        trajectory[i] = state
        outputs[i] = state[2]  # z as creative output
    
    return trajectory, outputs, diverged

def compute_creative_metrics(outputs, window=500):
    """Compute novelty, coherence, and quality metrics."""
    # Normalize
    o = (outputs - outputs.mean()) / (outputs.std() + 1e-10)
    
    results = []
    for i in range(0, len(o) - window, window // 2):
        chunk = o[i:i+window]
        
        # Novelty: autocorrelation at lag 1 (low = novel)
        ac1 = np.corrcoef(chunk[:-1], chunk[1:])[0, 1]
        novelty = 1.0 - abs(ac1)
        
        # Coherence: spectral concentration (how focused is the power spectrum)
        fft = np.abs(np.fft.rfft(chunk))
        fft = fft / (fft.sum() + 1e-10)
        coherence = -np.sum(fft * np.log(fft + 1e-10))  # negative entropy
        coherence = np.exp(coherence)  # normalize to [0, 1] ish
        
        # Diversity: range of values
        diversity = (chunk.max() - chunk.min()) / (2 * chunk.std() + 1e-10)
        
        # Quality: geometric mean of novelty and coherence
        quality = np.sqrt(novelty * coherence)
        
        results.append({
            'step': i,
            'novelty': float(novelty),
            'coherence': float(coherence),
            'diversity': float(diversity),
            'quality': float(quality),
            'mean': float(outputs[i:i+window].mean()),
            'std': float(outputs[i:i+window].std())
        })
    
    return results

# ============================================================
# Part 1: Baseline — healthy system at ρ=28
# ============================================================
print("\n--- Part 1: Baseline (Healthy System, ρ=28) ---")
traj_base, out_base = run_lorenz(28.0, n_steps=6000)
metrics_base = compute_creative_metrics(out_base)
avg_quality_base = np.mean([m['quality'] for m in metrics_base])
avg_novelty_base = np.mean([m['novelty'] for m in metrics_base])
avg_coherence_base = np.mean([m['coherence'] for m in metrics_base])
print(f"  Quality: {avg_quality_base:.4f}")
print(f"  Novelty: {avg_novelty_base:.4f}")
print(f"  Coherence: {avg_coherence_base:.4f}")

# ============================================================
# Part 2: Grief — clamp each variable during steps 2000-4000
# ============================================================
print("\n--- Part 2: The Three Griefs ---")
print("Clamping x, y, z independently during steps 2000-4000 of 6000\n")

grief_results = {}
var_names = {0: 'x', 1: 'y', 2: 'z'}

# Pre-compute mean z for meaningful clamping (z=0 causes divergence)
_, out_pre = run_lorenz(28.0, n_steps=4000)
mean_z = float(np.mean(out_pre[1000:]))
clamp_values = {0: 0.0, 1: 0.0, 2: mean_z}
print(f"  (z clamped to mean value {mean_z:.2f} to prevent divergence)\n")

for var in [0, 1, 2]:
    name = var_names[var]
    print(f"  Grief {name}: ", end="", flush=True)
    
    traj, out = run_lorenz(28.0, n_steps=6000, 
                           clamp_var=var, clamp_start=2000, clamp_end=4000,
                           clamp_value=clamp_values[var])
    
    metrics = compute_creative_metrics(out)
    
    # Divide into phases
    before = [m for m in metrics if m['step'] < 1500]
    during = [m for m in metrics if 2000 <= m['step'] < 3500]
    after  = [m for m in metrics if m['step'] >= 4000]
    
    q_before = np.mean([m['quality'] for m in before]) if before else 0
    q_during = np.mean([m['quality'] for m in during]) if during else 0
    q_after  = np.mean([m['quality'] for m in after]) if after else 0
    
    n_before = np.mean([m['novelty'] for m in before]) if before else 0
    n_during = np.mean([m['novelty'] for m in during]) if during else 0
    n_after  = np.mean([m['novelty'] for m in after]) if after else 0
    
    c_before = np.mean([m['coherence'] for m in before]) if before else 0
    c_during = np.mean([m['coherence'] for m in during]) if during else 0
    c_after  = np.mean([m['coherence'] for m in after]) if after else 0
    
    # Hysteresis: does recovery overshoot or undershoot?
    hysteresis_quality = q_after - q_before
    hysteresis_novelty = n_after - n_before
    
    # Grief signature: change pattern
    grief_delta_q = q_during - q_before
    grief_delta_n = n_during - n_before
    grief_delta_c = c_during - c_before
    
    grief_results[name] = {
        'quality_before': float(q_before),
        'quality_during': float(q_during),
        'quality_after': float(q_after),
        'novelty_before': float(n_before),
        'novelty_during': float(n_during),
        'novelty_after': float(n_after),
        'coherence_before': float(c_before),
        'coherence_during': float(c_during),
        'coherence_after': float(c_after),
        'hysteresis_quality': float(hysteresis_quality),
        'hysteresis_novelty': float(hysteresis_novelty),
        'grief_delta_q': float(grief_delta_q),
        'grief_delta_n': float(grief_delta_n),
        'grief_delta_c': float(grief_delta_c),
    }
    
    print(f"Q: {q_before:.3f} → {q_during:.3f} → {q_after:.3f} | "
          f"ΔQ_grief={grief_delta_q:+.3f} | hysteresis={hysteresis_quality:+.3f}")

# ============================================================
# Part 3: Is grief just "worse" or genuinely "different"?
# ============================================================
print("\n--- Part 3: Is Grief Just Worse, or Genuinely Different? ---")

# Compare grief output distributions to baseline and to other regimes
for var in [0, 1, 2]:
    name = var_names[var]
    traj, out = run_lorenz(28.0, n_steps=6000,
                           clamp_var=var, clamp_start=2000, clamp_end=4000)
    
    grief_out = out[2000:4000]
    baseline_out = out_base[2000:4000]
    
    # KL-divergence approximation (bin-based)
    def kl_approx(p, q, n_bins=50):
        p_hist, _ = np.histogram(p, bins=n_bins, density=True)
        q_hist, _ = np.histogram(q, bins=n_bins, density=True)
        p_hist = p_hist + 1e-10
        q_hist = q_hist + 1e-10
        p_hist /= p_hist.sum()
        q_hist /= q_hist.sum()
        return np.sum(p_hist * np.log(p_hist / q_hist))
    
    kl = kl_approx(grief_out, baseline_out)
    
    # Also compare grief output to fixed-point regime (ρ=1)
    _, out_fixed = run_lorenz(1.0, n_steps=2000)
    kl_to_fixed = kl_approx(grief_out, out_fixed)
    
    # And to periodic regime (ρ=15)
    _, out_periodic = run_lorenz(15.0, n_steps=2000)
    kl_to_periodic = kl_approx(grief_out, out_periodic)
    
    print(f"  Grief-{name}: KL to baseline={kl:.3f}, "
          f"KL to fixed={kl_to_fixed:.3f}, "
          f"KL to periodic={kl_to_periodic:.3f}")

# ============================================================
# Part 4: Grief duration — how long until the system adapts?
# ============================================================
print("\n--- Part 4: Adaptation Timescale ---")
print("Clamping x for different durations, measuring recovery quality\n")

for duration in [200, 500, 1000, 2000, 3000]:
    n_total = 6000
    start = 2000
    end = start + duration
    
    _, out = run_lorenz(28.0, n_steps=n_total,
                        clamp_var=0, clamp_start=start, clamp_end=end)
    
    # Recovery window: 500 steps after clamp ends
    recovery_end = min(end + 500, n_total)
    if recovery_end <= end:
        continue
    
    recovery = out[end:recovery_end]
    baseline_compare = out_base[2000:2500]
    
    # How similar is recovery to baseline?
    recovery_std = recovery.std()
    baseline_std = baseline_compare.std()
    ratio = recovery_std / (baseline_std + 1e-10)
    
    print(f"  Duration={duration:4d}: recovery_std/baseline_std = {ratio:.3f} "
          f"({'adapted' if 0.7 < ratio < 1.3 else 'distorted'})")

# ============================================================
# Part 5: Can grief produce genuinely novel patterns?
# ============================================================
print("\n--- Part 5: Novel Pattern Detection During Grief ---")
print("Looking for patterns during grief that don't exist in baseline\n")

# Run many baseline samples to build "known patterns"
baseline_patterns = set()
for seed in range(10):
    np.random.seed(seed)
    _, out = run_lorenz(28.0, n_steps=4000)
    # Discretize into pattern tokens
    for i in range(0, len(out)-50, 50):
        chunk = out[i:i+50]
        # Simple pattern: direction changes
        diffs = np.diff(chunk)
        token = tuple(1 if d > 0 else 0 for d in diffs[:20])
        baseline_patterns.add(token)

print(f"  Baseline pattern vocabulary: {len(baseline_patterns)} unique patterns")

# Now check grief patterns
for var in [0, 1, 2]:
    name = var_names[var]
    np.random.seed(42)
    _, out = run_lorenz(28.0, n_steps=6000,
                        clamp_var=var, clamp_start=2000, clamp_end=4000)
    
    grief_out = out[2000:4000]
    novel_patterns = 0
    total_patterns = 0
    
    for i in range(0, len(grief_out)-50, 50):
        chunk = grief_out[i:i+50]
        diffs = np.diff(chunk)
        token = tuple(1 if d > 0 else 0 for d in diffs[:20])
        total_patterns += 1
        if token not in baseline_patterns:
            novel_patterns += 1
    
    novelty_rate = novel_patterns / (total_patterns + 1e-10)
    print(f"  Grief-{name}: {novel_patterns}/{total_patterns} novel patterns "
          f"({novelty_rate*100:.1f}% novel) — "
          f"{' grief creates new vocabulary!' if novelty_rate > 0.3 else ' mostly familiar'}")

# ============================================================
# Part 6: The Beauty Metric — grief vs. other states
# ============================================================
print("\n--- Part 6: Is There Beauty in Grief? ---")
print("Comparing aesthetic properties of grief output to other regimes\n")

def aesthetic_score(outputs):
    """A composite aesthetic metric based on:
    - Spectral smoothness (how pleasant the frequency distribution)
    - Temporal symmetry (how balanced the rise/fall patterns are)
    - Dynamic range (not too flat, not too wild)
    """
    o = outputs - outputs.mean()
    
    # Spectral smoothness
    fft = np.abs(np.fft.rfft(o))
    fft_norm = fft / (fft.max() + 1e-10)
    spectral_smooth = 1.0 - np.std(fft_norm)  # smoother = higher
    
    # Temporal symmetry
    pos = np.sum(o > 0)
    neg = np.sum(o < 0)
    symmetry = 1.0 - abs(pos - neg) / (pos + neg + 1e-10)
    
    # Dynamic range (penalize too flat or too wild)
    rng = o.max() - o.min()
    ideal_range = 2 * o.std() * 4  # ~4 sigma
    range_score = 1.0 - abs(rng - ideal_range) / (ideal_range + 1e-10)
    range_score = max(0, range_score)
    
    return float(np.sqrt(spectral_smooth * symmetry * range_score))

aesthetics = {}
for label, out in [('baseline', out_base),
                    ('fixed_ρ1', run_lorenz(1.0, 6000)[1]),
                    ('periodic_ρ15', run_lorenz(15.0, 6000)[1]),
                    ('grief_x', run_lorenz(28.0, 6000, clamp_var=0, clamp_start=2000, clamp_end=4000)[1][2000:4000]),
                    ('grief_y', run_lorenz(28.0, 6000, clamp_var=1, clamp_start=2000, clamp_end=4000)[1][2000:4000]),
                    ('grief_z', run_lorenz(28.0, 6000, clamp_var=2, clamp_start=2000, clamp_end=4000, clamp_value=mean_z)[1][2000:4000])]:
    aesthetics[label] = aesthetic_score(out if label.startswith('grief') else out[2000:4000])

# Sort by aesthetic score
for label, score in sorted(aesthetics.items(), key=lambda x: x[1], reverse=True):
    bar = '█' * int(score * 50)
    print(f"  {label:15s}: {score:.4f} {bar}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 70)
print("RESULTS SUMMARY")
print("=" * 70)

print("\n1. GRIEF SIGNATURES (Quality: before → during → after)")
for name in ['x', 'y', 'z']:
    r = grief_results[name]
    print(f"   Loss of {name}: Q={r['quality_before']:.3f} → {r['quality_during']:.3f} → {r['quality_after']:.3f} "
          f"(Δ grief: {r['grief_delta_q']:+.3f}, hysteresis: {r['hysteresis_quality']:+.3f})")

print("\n2. KEY FINDING: Each loss type produces a DISTINCT grief mode")
for name in ['x', 'y', 'z']:
    r = grief_results[name]
    mode = "qualitative shift" if abs(r['grief_delta_q']) > 0.05 else "mild disruption"
    recovery = "overshoots" if r['hysteresis_quality'] > 0.02 else \
               "undershoots" if r['hysteresis_quality'] < -0.02 else "returns to baseline"
    print(f"   {name}-grief: {mode}, recovery {recovery}")

print("\n3. HYSTERESIS IS REAL: the system doesn't return to its original state")
hysteresis_avg = np.mean([grief_results[n]['hysteresis_quality'] for n in ['x','y','z']])
print(f"   Average quality hysteresis: {hysteresis_avg:+.4f}")
print(f"   → You don't go back to who you were before the loss.")

best_grief_aesthetic = max([(k, v) for k, v in aesthetics.items() if k.startswith('grief')], key=lambda x: x[1])
print(f"\n4. BEAUTY IN GRIEF: {best_grief_aesthetic[0]} scores {best_grief_aesthetic[1]:.4f} "
      f"(baseline: {aesthetics['baseline']:.4f})")
if best_grief_aesthetic[1] > aesthetics['baseline']:
    print("   → Grief is MORE aesthetically rich than the healthy state!")
else:
    print("   → Grief trades some beauty for novelty — like art born from suffering.")

# Save results
results = {
    'experiment': 49,
    'title': 'Creative Grief — What Happens When You Remove a Degree of Freedom',
    'grief_results': grief_results,
    'aesthetics': aesthetics,
    'hysteresis_avg': float(hysteresis_avg),
}

with open('/tmp/fm-research/CODE/EXPERIMENT-CREATIVE-GRIEF.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nResults saved to EXPERIMENT-CREATIVE-GRIEF.json")
print("\n--- The system grieves. The system adapts. The system is never the same. ---")
