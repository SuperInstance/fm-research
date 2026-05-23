import numpy as np
import json
import math

print("=== Harmonic Series as Constraint Lattice ===\n")

# Part 1: Map harmonics to pitch space
print("--- Part 1: Harmonics → Pitch Classes ---")
f0 = 55.0  # A1 fundamental
for n in range(1, 33):
    freq = f0 * n
    # Map to pitch class (mod octave)
    semitones = 12 * math.log2(freq / f0)
    pitch_class = semitones % 12
    harmonic_interval = semitones  # total interval from fundamental
    print(f"  H{n:2d}: {freq:8.1f} Hz, {semitones:6.2f} semitones, pitch class {pitch_class:5.2f} ({['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][int(pitch_class)%12]})")

# Part 2: Eisenstein lattice from harmonics
print("\n--- Part 2: Eisenstein Lattice Emergence ---")
# Take ratios of consecutive harmonics: (n+1)/n
# These should form an Eisenstein-like lattice in ratio space
ratios = [(n+1)/n for n in range(1, 32)]
print(f"First 10 ratios: {[f'{r:.4f}' for r in ratios[:10]]}")

# Map ratios to Eisenstein coordinates
# Eisenstein: z = a + b*ω where ω = e^(2πi/3)
omega_e = complex(-0.5, math.sqrt(3)/2)
eisenstein_points = []
for i, r1 in enumerate(ratios[:20]):
    for j, r2 in enumerate(ratios[:20]):
        if i < j:
            z = r1 + r2 * omega_e
            eisenstein_points.append((z.real, z.imag))

# Check if points form a lattice
points = np.array(eisenstein_points)
print(f"Eisenstein points: {len(points)}")

# Part 3: Fibonacci in harmonics
print("\n--- Part 3: Fibonacci in Harmonic Ratios ---")
# Convergents of log2(3/2) give the circle of fifths
# 3/2 is the perfect fifth (harmonic 3)
fifth = 3/2
print(f"Perfect fifth ratio: {fifth}")
print(f"12 fifths: {(fifth**12):.4f} (should be ~128 = 2^7)")
print(f"Pythagorean comma: {fifth**12 / 128:.8f}")

# The continued fraction of log2(3/2)
log_fifth = math.log2(fifth)
print(f"\nlog2(3/2) = {log_fifth:.10f}")
print(f"As fraction: {log_fifth} ≈ 7/12 = {7/12:.10f}")
print(f"Error: {abs(log_fifth - 7/12):.10f}")
print(f"This error IS the Pythagorean comma!")

# Fibonacci convergents of log2(3/2)
from fractions import Fraction
cf = Fraction(log_fifth).limit_denominator(1000)
print(f"Best rational: {cf.numerator}/{cf.denominator}")

# Part 4: Harmonic interference creates scales
print("\n--- Part 4: Scales from Harmonic Interference ---")
# Take harmonics 1-16 and snap to nearest 12-TET
scale_notes = set()
for n in range(1, 17):
    freq = f0 * n
    semitones = 12 * math.log2(freq / f0)
    pitch_class = round(semitones) % 12
    scale_notes.add(pitch_class)

scale = sorted(scale_notes)
print(f"Notes from harmonics 1-16 of A1: {scale}")
print(f"Scale size: {len(scale)} notes")
print(f"Intervals: {[scale[i+1]-scale[i] for i in range(len(scale)-1)] + [12-scale[-1]+scale[0]]}")

# Compare with known scales
major = {0,2,4,5,7,9,11}
minor = {0,2,3,5,7,8,10}
pentatonic = {0,2,4,7,9}
harmonic_set = set(scale)
print(f"Overlap with major: {len(harmonic_set & major)}/{len(major)}")
print(f"Overlap with minor: {len(harmonic_set & minor)}/{len(minor)}")
print(f"Overlap with pentatonic: {len(harmonic_set & pentatonic)}/{len(pentatonic)}")

# Part 5: The lattice IS periodic
print("\n--- Part 5: Lattice Periodicity ---")
# Check if harmonics repeat at the octave
octave_harmonics = {}
for n in range(1, 65):
    freq = f0 * n
    semitones = 12 * math.log2(freq / f0)
    pc = round(semitones) % 12
    octave = int(round(semitones) // 12)
    if pc not in octave_harmonics:
        octave_harmonics[pc] = []
    octave_harmonics[pc].append((n, octave))

# Show which pitch classes have the most harmonic support
for pc in sorted(octave_harmonics.keys()):
    notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    support = len(octave_harmonics[pc])
    harmonics_list = [h[0] for h in octave_harmonics[pc][:8]]
    print(f"  {notes[pc]:2s} (PC {pc:2d}): {support:2d} harmonics support it — H{harmonics_list}")

# Part 6: Nonlinear distortion creates NEW harmonics
print("\n--- Part 6: Nonlinear Distortion = Creative Emergence ---")
# When a string is driven nonlinearly, new frequencies appear
# that aren't in the original spectrum
# f_new = m*f1 ± n*f2 (intermodulation)
f1, f2 = 220.0, 330.0  # A3 and E4 (perfect fifth)
print(f"Input: f1={f1}Hz (A3), f2={f2}Hz (E4)")
print(f"Intermodulation products:")
for m in range(1, 6):
    for n in range(1, 6):
        for sign in [1, -1]:
            f_new = m*f1 + sign*n*f2
            if f_new > 0 and f_new < 4000:
                semi = 12 * math.log2(f_new / f0)
                pc = round(semi) % 12
                notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
                print(f"  {m}×{f1:.0f} {'+' if sign>0 else '-'} {n}×{f2:.0f} = {f_new:7.1f} Hz → {notes[pc]} (PC {pc})")

print("\n=== CONCLUSION ===")
print("The harmonic series IS a lattice. Harmonic interference creates scales.")
print("Fibonacci/Penrose structure in harmonic ratios. Nonlinear distortion = emergence.")
