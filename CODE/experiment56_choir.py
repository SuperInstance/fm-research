import numpy as np
import json

print("=== Experiment 56: The Attractor Choir ===")
print("1000 Lorenz systems as a polyphonic instrument\n")

np.random.seed(42)

N_VOICES = 1000
DT = 0.01
N_STEPS = 10000
RECORD_FROM = 5000

# Each voice has slightly different ρ (distributed around the creative peak)
rho_values = np.concatenate([
    np.random.uniform(5, 20, 100),     # 100 Crystal voices
    np.random.uniform(20, 24.74, 100), # 100 Pendulum voices  
    np.random.uniform(24.74, 35, 300), # 300 moderate Chimera
    np.random.uniform(35, 55, 300),    # 300 high Chimera
    np.random.uniform(55, 100, 200),   # 200 extreme Chimera
])
np.random.shuffle(rho_values)

sigma_values = np.full(N_VOICES, 10.0)
beta_values = np.full(N_VOICES, 8.0/3.0)

# States: [N, 3] — x, y, z for each voice
states = np.random.uniform(-1, 1, (N_VOICES, 3))

# Map each voice to a pitch (MIDI note)
base_pitches = np.clip(36 + (rho_values - 5) * 0.8, 36, 96).astype(int)

print(f"  {N_VOICES} voices, ρ range [{rho_values.min():.1f}, {rho_values.max():.1f}]")
print(f"  Pitch range: {base_pitches.min()} - {base_pitches.max()}")

# Vectorized Lorenz step
def lorenz_step_vectorized(states, rho, sigma, beta, dt):
    x, y, z = states[:, 0], states[:, 1], states[:, 2]
    
    # RK4 (vectorized)
    def deriv(s):
        x, y, z = s[:, 0], s[:, 1], s[:, 2]
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
        return np.stack([dx, dy, dz], axis=1)
    
    k1 = deriv(states)
    k2 = deriv(states + 0.5 * dt * k1)
    k3 = deriv(states + 0.5 * dt * k2)
    k4 = deriv(states + dt * k3)
    
    new_states = states + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
    
    # Clamp to prevent divergence
    new_states = np.clip(new_states, -200, 200)
    
    return new_states

# Run the choir
print(f"\n  Running {N_STEPS} steps...")
outputs = np.zeros((N_STEPS - RECORD_FROM, N_VOICES))

for step in range(N_STEPS):
    states = lorenz_step_vectorized(states, rho_values, sigma_values, beta_values, DT)
    
    if step >= RECORD_FROM:
        outputs[step - RECORD_FROM] = states[:, 0]  # x-coordinate as output

print(f"  Done. Output shape: {outputs.shape}")

# ANALYSIS

# Part 1: Voice activity — how many voices are "alive" (std > threshold)
print("\n--- Part 1: Voice Activity ---")
voice_stds = np.std(outputs, axis=0)
alive = voice_stds > 1.0
print(f"  Alive voices: {alive.sum()}/{N_VOICES} ({alive.sum()/N_VOICES*100:.1f}%)")
print(f"  Crystal alive: {np.sum(alive[:100])}/100")
print(f"  Pendulum alive: {np.sum(alive[100:200])}/100")
print(f"  Moderate Chimera alive: {np.sum(alive[200:500])}/300")
print(f"  High Chimera alive: {np.sum(alive[500:800])}/300")
print(f"  Extreme Chimera alive: {np.sum(alive[800:])}/200")

# Part 2: Emergent harmony — what intervals appear between voices?
print("\n--- Part 2: Emergent Harmony ---")
loudness = np.abs(outputs)
top_voices = np.argsort(loudness, axis=1)[:, -6:]  # top 6 loudest

all_intervals = []
for t in range(0, len(outputs), 10):
    voices = top_voices[t]
    pitches = base_pitches[voices]
    for i in range(len(pitches)):
        for j in range(i+1, len(pitches)):
            interval = abs(pitches[i] - pitches[j]) % 12
            all_intervals.append(interval)

interval_counts = np.bincount(all_intervals, minlength=12)
interval_names = ['unison', 'min2', 'maj2', 'min3', 'maj3', 'perf4', 'tritone', 'perf5', 'min6', 'maj6', 'min7', 'maj7']

print(f"  Interval distribution (pitch class):")
for i in range(12):
    pct = interval_counts[i] / sum(interval_counts) * 100
    bar = '█' * int(pct / 2)
    print(f"    {interval_names[i]:8s}: {pct:5.1f}% {bar}")

# Part 3: Temporal structure — does the choir breathe?
print("\n--- Part 3: Choir Breathing ---")
total_loudness = np.sum(np.abs(outputs), axis=1)
acf = np.correlate(total_loudness - np.mean(total_loudness), 
                   total_loudness - np.mean(total_loudness), mode='full')
acf = acf[len(acf)//2:]
acf = acf / acf[0]

from scipy.signal import find_peaks
peaks, _ = find_peaks(acf[:500], height=0.3, distance=10)
breathing_bpm = None
if len(peaks) > 0:
    breathing_period = peaks[0]
    breathing_bpm = 60.0 / (breathing_period * DT)
    print(f"  Breathing period: {breathing_period} steps ({breathing_bpm:.1f} BPM)")
    print(f"  The choir BREATHES at {breathing_bpm:.0f} BPM!")
else:
    print(f"  No clear breathing rhythm detected")
    print(f"  ACF decay: {acf[10]:.3f} at lag 10, {acf[100]:.3f} at lag 100")

# Part 4: Spectral analysis of the ensemble
print("\n--- Part 4: Ensemble Spectrum ---")
mean_output = np.mean(outputs, axis=1)
fft = np.fft.rfft(mean_output)
power = np.abs(fft) ** 2
freqs = np.fft.rfftfreq(len(mean_output), DT)

top5 = np.argsort(power[1:])[-5:][::-1] + 1
print(f"  Dominant frequencies:")
for idx in top5:
    hz = freqs[idx]
    bpm = hz * 60
    print(f"    {hz:.2f} Hz ({bpm:.1f} BPM): power={power[idx]:.1f}")

# Part 5: Register utilization
print("\n--- Part 5: Register Utilization ---")
for lo, hi, name in [(36,48,'Low'), (48,60,'Mid-Low'), (60,72,'Mid'), (72,84,'Mid-High'), (84,97,'High')]:
    mask = (base_pitches >= lo) & (base_pitches < hi)
    if mask.any():
        avg_loud = np.mean(loudness[:, mask])
        print(f"  {name} ({lo}-{hi}): {mask.sum()} voices, avg loudness={avg_loud:.3f}")

# Part 6: Novel output — MIDI-like sequence
print("\n--- Part 6: Generating MIDI Sequence ---")
n_sixteenths = 64
samples_per_16th = len(outputs) // n_sixteenths
midi_events = []

for s in range(n_sixteenths):
    start = s * samples_per_16th
    end = start + samples_per_16th
    segment = outputs[start:end]
    
    avg_loud_seg = np.mean(np.abs(segment), axis=0)
    top4 = np.argsort(avg_loud_seg)[-4:]
    
    for voice in top4:
        if avg_loud_seg[voice] > 1.0:
            velocity = min(127, int(avg_loud_seg[voice] * 5))
            midi_events.append({
                'tick': s,
                'pitch': int(base_pitches[voice]),
                'velocity': velocity,
                'voice': int(voice),
                'rho': float(rho_values[voice]),
            })

print(f"  Generated {len(midi_events)} MIDI events across {n_sixteenths} ticks")
print(f"  Unique pitches: {len(set(e['pitch'] for e in midi_events))}")
print(f"  Events per tick: {len(midi_events)/n_sixteenths:.1f}")

# Save
with open('/tmp/fm-research/CODE/EXPERIMENT-ATTRACTOR-CHOIR.json', 'w') as f:
    json.dump({
        'n_voices': N_VOICES,
        'n_events': len(midi_events),
        'interval_distribution': {interval_names[i]: int(interval_counts[i]) for i in range(12)},
        'breathing_bpm': float(breathing_bpm) if breathing_bpm else None,
        'midi_events': midi_events[:200],
    }, f, indent=2)

import subprocess
subprocess.run(['git', 'add', '-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'commit', '-m', 'experiment 56: attractor choir — 1000 voices'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'push'], cwd='/tmp/fm-research', capture_output=True)

print("\n=== 1000 VOICES SINGING IN PHASE SPACE ===")
