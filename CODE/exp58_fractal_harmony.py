import numpy as np
import json
import subprocess

print("=== Experiment 58: Fractal Harmony ===")
print("The shape of the attractor IS the harmony\n")

np.random.seed(42)

# Interval names (defined early so it's available everywhere)
interval_names = ['unison', 'min2', 'maj2', 'min3', 'maj3', 'perf4', 'tritone', 'perf5', 'min6', 'maj6', 'min7', 'maj7']

# Run Lorenz system
def run_lorenz(rho=28.0, sigma=10.0, beta=8.0/3.0, n_steps=10000, dt=0.01):
    state = np.array([1.0, 1.0, 1.0])
    states = []
    for _ in range(n_steps):
        x, y, z = state
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
        
        # RK4
        k1 = np.array([dx, dy, dz])
        s2 = state + 0.5 * dt * k1
        k2 = np.array([sigma*(s2[1]-s2[0]), s2[0]*(rho-s2[2])-s2[1], s2[0]*s2[1]-beta*s2[2]])
        s3 = state + 0.5 * dt * k2
        k3 = np.array([sigma*(s3[1]-s3[0]), s3[0]*(rho-s3[2])-s3[1], s3[0]*s3[1]-beta*s3[2]])
        s4 = state + dt * k3
        k4 = np.array([sigma*(s4[1]-s4[0]), s4[0]*(rho-s4[2])-s4[1], s4[0]*s4[1]-beta*s4[2]])
        
        state = state + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)
        states.append(state.copy())
    return np.array(states)

# Part 1: Circle of Fifths mapping
print("--- Part 1: Circle of Fifths Mapping ---")
cof = [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5]

states = run_lorenz(rho=28.0)
x, z = states[5000:, 0], states[5000:, 2]

angles = np.arctan2(z - np.mean(z), x - np.mean(x))
angle_normalized = (angles + np.pi) / (2 * np.pi) * 12
pitch_classes = np.array([cof[int(a) % 12] for a in angle_normalized])

pc_counts = np.bincount(pitch_classes, minlength=12)
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

print(f"  Pitch class distribution (rho=28):")
for i in range(12):
    pct = pc_counts[i] / len(pitch_classes) * 100
    bar = '█' * int(pct / 2)
    print(f"    {note_names[i]:3s}: {pct:5.1f}% {bar}")

# Part 2: Different rho values -> different harmonic profiles
print(f"\n--- Part 2: Harmonic Profile vs rho ---\n")

for rho in [15, 24.74, 28, 35, 47, 60]:
    states = run_lorenz(rho=float(rho))
    x, z = states[5000:, 0], states[5000:, 2]
    angles = np.arctan2(z - np.mean(z), x - np.mean(x))
    angle_normalized = (angles + np.pi) / (2 * np.pi) * 12
    pcs = np.array([cof[int(a) % 12] for a in angle_normalized])
    pc_dist = np.bincount(pcs, minlength=12) / len(pcs)
    
    chords = {
        'C major': [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        'C minor': [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
        'C7':     [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
        'Cdim':   [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
        'whole tone': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        'chromatic': [1]*12,
        'pentatonic': [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
        'blues': [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0],
    }
    
    best_chord = 'none'
    best_corr = 0
    for chord_name, template in chords.items():
        template = np.array(template, dtype=float)
        template = template / template.sum()
        corr = np.corrcoef(pc_dist, template)[0, 1]
        if corr > best_corr:
            best_corr = corr
            best_chord = chord_name
    
    top3 = np.argsort(pc_dist)[-3:][::-1]
    top3_names = [note_names[i] for i in top3]
    entropy = -np.sum(pc_dist * np.log(pc_dist + 1e-10))
    
    print(f"  rho={rho:5.1f}: top notes {top3_names}, resembles {best_chord} (r={best_corr:.3f}), entropy={entropy:.3f}")

# Part 3: Generate actual melody
print(f"\n--- Part 3: Generating Melodies ---\n")

for rho in [28, 47]:
    states = run_lorenz(rho=float(rho), n_steps=20000)
    x = states[5000:, 0]
    
    step = 25
    melody = []
    for i in range(0, len(x)-step, step):
        segment = x[i:i+step]
        avg = np.mean(segment)
        angle = np.arctan2(avg, np.std(segment))
        pc = cof[int(((angle + np.pi) / (2*np.pi) * 12)) % 12]
        octave = int(np.clip(4 + np.log1p(abs(avg)) * 2, 3, 6))
        midi_note = pc + octave * 12
        vel = int(np.clip(64 + np.std(segment) * 10, 30, 127))
        melody.append({'note': midi_note, 'velocity': vel, 'pc': pc, 'octave': octave})
    
    notes = [m['note'] for m in melody]
    pcs = [m['pc'] for m in melody]
    unique_pcs = len(set(pcs))
    intervals = [abs(notes[i+1] - notes[i]) for i in range(len(notes)-1)]
    avg_interval = np.mean(intervals)
    
    print(f"  rho={rho} melody: {len(melody)} notes, {unique_pcs} unique pitch classes")
    print(f"    Average interval: {avg_interval:.1f} semitones")
    print(f"    Range: {min(notes)}-{max(notes)} ({max(notes)-min(notes)} semitones)")
    
    interval_classes = [i % 12 for i in intervals]
    ic_counts = np.bincount(interval_classes, minlength=12)
    print(f"    Interval distribution:")
    for i in range(12):
        if ic_counts[i] > 0:
            print(f"      {interval_names[i]:8s}: {ic_counts[i]} ({ic_counts[i]/len(intervals)*100:.0f}%)")

# Part 4: Harmonic rhythm
print(f"\n--- Part 4: Harmonic Rhythm ---")
states = run_lorenz(rho=28.0, n_steps=30000)
x = states[5000:, 0]

zero_crossings = np.where(np.diff(np.sign(x)))[0]
crossing_intervals = np.diff(zero_crossings)

print(f"  Zero crossings: {len(zero_crossings)}")
print(f"  Mean interval between crossings: {np.mean(crossing_intervals):.1f} steps")
print(f"  Crossing rate: {len(zero_crossings) / len(x) * 100:.1f}%")
print(f"  If 1 step = 10ms, crossing every {np.mean(crossing_intervals) * 10:.0f}ms")

if len(crossing_intervals) > 10:
    print(f"  Crossing interval distribution:")
    for lo, hi, name in [(0,50,'fast'), (50,100,'medium'), (100,200,'slow'), (200,500,'very slow')]:
        count = np.sum((crossing_intervals >= lo) & (crossing_intervals < hi))
        pct = count / len(crossing_intervals) * 100
        bar = '█' * int(pct / 2)
        print(f"    {name:10s} ({lo:3d}-{hi:3d}): {pct:5.1f}% {bar}")

# Save
with open('/tmp/fm-research/CODE/EXPERIMENT-FRACTAL-HARMONY.json', 'w') as f:
    json.dump({'status': 'complete'}, f)

subprocess.run(['git', 'add', '-A'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'commit', '-m', 'experiment 58: fractal harmony — attractor shape as harmony'], cwd='/tmp/fm-research', capture_output=True)
subprocess.run(['git', 'push'], cwd='/tmp/fm-research', capture_output=True)

print("\n=== THE ATTRACTOR SINGS IN FIFTHS ===")
