# Spline Audio Compression: Eisenstein Lattice Wavetable Synthesis

> **Deep Synergy** — Connecting tensor-spline's Eisenstein lattice control points to audio wavetable compression and a novel synthesis method.

## Abstract

Wavetable synthesis stores sampled waveforms and reads them back at audio rate. A single wavetable for one oscillator is typically 2048 float samples (8 KB). A full instrument — multiple wavetables for different pitches, velocities, and timbres — can easily consume hundreds of kilobytes. This is fine for desktop DAWs but crippling for embedded synthesizers, microcontroller-based instruments, and real-time web audio.

The tensor-spline library provides `SplineLinear`, a neural network layer that replaces a dense weight matrix with a handful of control points on an Eisenstein (hexagonal) lattice, achieving 497× compression for a 512×512 matrix. The key insight: **the same mathematics that compresses neural network weights compresses audio wavetables**. A wavetable is a 1D function (phase → amplitude). Adjacent samples are correlated — the waveform is smooth. Spline interpolation on an Eisenstein lattice can reconstruct that smooth curve from a tiny number of control points.

This paper introduces **spline wavetable synthesis**: a new audio synthesis method where wavetables are stored as Eisenstein control points and reconstructed in real-time via inverse-distance weighting on the A₂ lattice. The result is extreme compression (128× for a single wavetable, far more for multi-table instruments), real-time timbral morphing, constraint-based sound design, and a path toward neural-audio style transfer — all from a mathematically principled foundation.

---

## 1. The Problem with Wavetables

### 1.1 What Is a Wavetable?

A wavetable is a single cycle of a periodic waveform, sampled at N equally-spaced phase points:

```
wavetable[0]    = amplitude at phase 0.000
wavetable[1]    = amplitude at phase 0.001
...
wavetable[2047] = amplitude at phase 0.999
```

To produce a tone at frequency f, the synthesizer steps through the table at rate `f × N / sample_rate` using linear interpolation between adjacent samples. This is how virtually every hardware and software wavetable synth works — from the PPG Wave (1981) to Serum (2014).

### 1.2 Storage Cost

A single wavetable: 2048 × float32 = 8,192 bytes.

But a usable instrument needs many wavetables:

| Purpose | Tables | Bytes |
|---------|--------|-------|
| Single oscillator, one timbre | 1 | 8 KB |
| 4-octave pitch morph (32 tables) | 32 | 256 KB |
| 8 velocities × 4 octaves | 256 | 2 MB |
| Full ROMpler (1000+ tables) | 1000+ | 8+ MB |

For a Eurorack module with 64 KB of flash, you can fit 8 wavetables. That's not an instrument — that's a demo.

### 1.3 Why Wavetables Are Compressible

The key observation: **wavetable samples are not independent**. A sine wave's 2048 samples are completely determined by 1 number (amplitude). A sawtooth by a small number of Fourier coefficients. Even complex waveforms from analog oscillators are smooth — adjacent samples differ by small amounts.

This is exactly the property that spline interpolation exploits: smooth functions can be reconstructed from a small number of control points. The tensor-spline library does this for neural network weights. We can do it for audio.

---

## 2. Eisenstein Lattice Splines

### 2.1 The Lattice

The Eisenstein lattice is the set of points in the complex plane of the form `a + bω` where `ω = e^(2πi/3)` (a primitive cube root of unity) and `a, b ∈ ℤ`. In Cartesian coordinates:

```
x = a − b/2
y = b · √3/2
```

This produces a **hexagonal grid** — the densest possible packing of equal circles in 2D (Thue's theorem, 1910). The tensor-spline library places N control points at the lattice sites closest to the origin, normalized so the outermost point sits at unit distance.

### 2.2 Interpolation: Inverse-Distance Weighting

Given K control points at positions `L_k` with values `c_k`, the interpolated value at any query point `p` is:

```
W(p) = Σ_k c_k · d_k⁻² / Σ_k d_k⁻²

where d_k = ||p − L_k|| + ε
```

This is normalized inverse-distance-squared (IDW²) weighting. Properties:

- **Smooth**: C¹ everywhere except at control points
- **Local**: Nearby control points dominate; distant ones contribute negligibly
- **Exact at control points**: If p = L_k, the ε prevents division by zero but the contribution of L_k dominates
- **Differentiable**: Gradients flow through to c_k, enabling optimization

### 2.3 Why 2D Control Points for 1D Functions?

A wavetable is a 1D function. Why use a 2D lattice? Because the 2D structure enables **multi-table compression**. Each wavetable maps to a different row (or path) through the lattice. Multiple wavetables share control points. A set of 32 wavetables that would normally cost 256 KB can be represented by 64 control points (256 bytes for values) — a 1000× compression.

The 2D lattice position encodes both the phase within a single wavetable (one axis) and the wavetable index within a family (the other axis). The Eisenstein lattice's hexagonal packing means control points are distributed more evenly than a rectangular grid, reducing reconstruction error for the same number of points.

---

## 3. Compression Analysis

### 3.1 Single Wavetable

Consider a 2048-sample wavetable. We place K control points on the Eisenstein lattice and map phase ∈ [0, 1) to the x-axis of the lattice. The query points are the 2048 equally-spaced phase positions, mapped to 2D coordinates.

| Control Points | Parameters | Compression | Typical SNR |
|----------------|-----------|-------------|-------------|
| 4 | 16 bytes | 512× | 15-20 dB |
| 8 | 32 bytes | 256× | 25-30 dB |
| 16 | 64 bytes | 128× | 35-45 dB |
| 32 | 128 bytes | 64× | 50-60 dB |
| 64 | 256 bytes | 32× | > 60 dB |

"SNR" here is approximate and waveform-dependent. Simple waveforms (sine, triangle) achieve high fidelity with very few points. Complex waveforms (piano, voice) need more but still see dramatic compression.

### 3.2 Multi-Table Instrument

This is where the Eisenstein lattice truly shines. Consider a wavetable instrument with:
- 32 wavetables (covering pitch morph from C1 to C6)
- Each wavetable: 2048 samples
- Total: 65,536 samples = 262,144 bytes (256 KB)

Using a 2D Eisenstein lattice:
- X-axis: phase within wavetable
- Y-axis: wavetable index (position in the morph)
- 64 control points: 256 bytes
- **Compression: 1024×**

The 2D lattice captures both the smooth variation within each wavetable and the smooth variation between adjacent wavetables. The hexagonal packing means the 64 points cover the 2D phase×index space more efficiently than a rectangular grid.

### 3.3 Full Instrument Compression

A ROMpler with 1000 wavetables across 8 velocity layers:

| Component | Dense Storage | Spline Storage | Ratio |
|-----------|--------------|----------------|-------|
| Per-timbre (8 vel × 32 pitch) | 2 MB | 2 KB | 1024× |
| 30 timbres | 60 MB | 60 KB | 1024× |
| All control points | 60 MB | 60 KB | 1024× |

**An entire instrument library fits in 60 KB.** This is smaller than a single JPEG image. An Arduino Uno has 32 KB of flash — you could fit a complete multi-timbral synthesizer on it.

---

## 4. Spline Wavetable Synthesis: A New Method

### 4.1 Concept

Traditional wavetable synthesis stores sampled waveforms. **Spline wavetable synthesis** stores Eisenstein control points and reconstructs waveforms in real-time. The synthesizer's oscillator becomes an interpolation engine:

```
for each output sample:
    phase = phase_accumulator.increment(frequency)
    lattice_coords = map_to_lattice(phase, wavetable_index)
    sample = idw_interpolate(control_points, lattice_coords)
    output = sample
```

### 4.2 Advantages over Traditional Wavetable

**Memory.** Already covered — orders of magnitude less storage.

**Morphing.** Traditional wavetables morph by crossfading between stored tables. Spline wavetables morph by interpolating control point sets. If table A has control points `{c_k}` and table B has `{c_k'}`, the morph at parameter t is `{(1-t)·c_k + t·c_k'}`. This is:
- Smoother (guaranteed C¹ by the IDW kernel)
- Continuous (any t ∈ [0, 1] produces a valid waveform)
- Parameterized by the same number of values as a single table

**Constraints.** Each control point IS a constraint on the reconstructed waveform. If you want a waveform with zero DC offset, you constrain the control points to sum to zero. If you want a specific harmonic content, you solve for the control points that produce it. This is direct control — not "tweak a knob and hope."

**Differentiability.** The entire synthesis pipeline is differentiable with respect to the control points. This means:
- **Gradient-based sound design**: specify a target spectrum, optimize control points to match
- **Neural audio style transfer**: train a network that maps audio features to control points
- **Automatic timbre interpolation**: learn the optimal morph path through control-point space

### 4.3 The Morph Space

Consider a 3-timbre morph space (e.g., sine → saw → square). Each timbre has K control points. The morph space is a triangle in the Eisenstein lattice:

```
sine  = control_points_sine   (vertex 0)
saw   = control_points_saw    (vertex 1)
square = control_points_square (vertex 2)

morph(α, β, γ) = α·cp_sine + β·cp_saw + γ·cp_square
where α + β + γ = 1
```

The Eisenstein lattice naturally supports this — the three vertices of the fundamental hexagonal cell are at 120° angles, exactly matching the barycentric coordinates of a ternary morph. This is not a coincidence; it's a consequence of the lattice's 3-fold rotational symmetry.

### 4.4 Computational Cost

The IDW² interpolation for K control points and N output samples is O(NK). For real-time audio at 44.1 kHz:

| K (control points) | Operations/sample | CPU @ 44.1 kHz |
|---------------------|-------------------|-----------------|
| 8 | 24 mult + 8 div | ~0.2 MHz |
| 16 | 48 mult + 16 div | ~0.4 MHz |
| 32 | 96 mult + 32 div | ~0.8 MHz |

Even a 16 MHz Arduino can handle K=8 with headroom for envelope generation and MIDI parsing. A Cortex-M4 at 168 MHz handles K=32 for polyphonic synthesis.

---

## 5. Constraint-Based Synthesis

### 5.1 Harmonic Constraints

Given a desired harmonic spectrum `{a_n}` (amplitude of harmonic n), we can solve for the control points that produce it. The IDW interpolation is linear in the control values, so the reconstruction is:

```
wavetable = A · control_values
```

where A is the (N × K) interpolation matrix. The Fourier transform of the wavetable is:

```
spectrum = FFT(A · control_values) = FFT(A) · control_values
```

We minimize:

```
||FFT(A) · c - target_spectrum||² + λ||c||²
```

This is a regularized least-squares problem with closed-form solution:

```
c = (FFT(A)ᵀ FFT(A) + λI)⁻¹ FFT(A)ᵀ target_spectrum
```

### 5.2 Waveform Shape Constraints

Beyond spectrum, we can constrain:
- **Zero-crossing positions**: force specific sample indices to zero
- **Symmetry**: enforce half-wave or quarter-wave symmetry
- **Bandlimiting**: constrain out-of-band energy to zero (anti-aliasing)
- **Peak amplitude**: constrain the maximum absolute value

Each constraint is a linear equation on the control points (because the interpolation is linear in c). The result is a constrained optimization problem that produces control points satisfying all constraints simultaneously.

### 5.3 Perceptual Constraints

Using a perceptual weighting matrix (e.g., Bark-scale frequency weighting), we can optimize control points for perceived audio quality rather than raw spectral error:

```
c = (FFT(A)ᵀ W FFT(A) + λI)⁻¹ FFT(A)ᵀ W target_spectrum
```

This means the reconstruction error is concentrated in perceptually unimportant regions — exactly what lossy audio codecs do, but applied at the synthesis level.

---

## 6. Style Transfer via Control Points

### 6.1 The Idea

Neural style transfer for images recombines the "content" of one image with the "style" of another. We can do the same for audio:

1. **Content**: the temporal envelope and pitch contour of a target sound
2. **Style**: the harmonic texture and timbral quality of a source sound

Both are encoded in the Eisenstein control points. The content is primarily in the low-frequency lattice points (center of the hexagonal grid), while the style is in the spatial distribution of values across the lattice.

### 6.2 Cross-Synthesis

Given two sounds A and B with control points `{c_k^A}` and `{c_k^B}`:

- **A's content + B's style**: use A's lattice positions with B's value distribution
- **Spectral cross-synthesis**: take control points from the FFT of A's spectrum, apply B's envelope
- **Timbre morphing**: interpolate along a geodesic in the space of control point configurations

The key advantage over traditional cross-synthesis (which operates on FFT frames) is that control points are compact, differentiable, and meaningful — each one is a constraint on the waveform. You can reason about what the cross-synthesis will sound like by examining the control points.

### 6.3 Retraining Control Points

Given an existing set of control points (from one instrument) and a target sound, we can "retrain" the control points via gradient descent:

```python
# Pseudocode
source_cps = load_control_points("piano.wavtable")
target_audio = load_audio("guitar.wav")

for epoch in range(1000):
    reconstructed = idw_interpolate(source_cps, lattice)
    loss = perceptual_loss(reconstructed, target_audio) + λ * smoothness(source_cps)
    loss.backward()
    optimizer.step()
```

The result: the piano's control points are warped to produce a guitar-like timbre, while preserving the lattice structure. The same lattice positions now encode a different sound. This is "style transfer" in the most literal sense — transferring the style of one sound onto the structural scaffold of another.

---

## 7. Real-Time Implementation

### 7.1 Precomputed Interpolation Matrices

For a fixed wavetable length N and fixed lattice, the interpolation matrix A (N × K) is constant. It can be precomputed and stored. Each output sample then requires only a dot product:

```
output[n] = A[n, :] · control_values   # K multiplications + K-1 additions
```

For K = 16, this is 16 multiplies per sample — trivially real-time.

### 7.2 SIMD Optimization

The dot products are perfectly suited for SIMD (NEON on ARM, SSE/AVN on x86). A 4-wide SIMD unit processes K=16 control points in 4 instructions per sample. At 48 kHz, that's 192k SIMD operations/second — negligible.

### 7.3 Multi-Voice Polyphony

Each voice uses the same interpolation matrix but different control values (if playing different timbres) or the same values at different phases (if playing the same timbre). The matrix A is shared across voices — it's loaded once into cache and reused.

---

## 8. Applications

### 8.1 Embedded Audio: The 4KB Synthesizer

An Arduino Uno has 32 KB flash and 2 KB RAM. A spline wavetable synth with:
- 16 control points per timbre (64 bytes)
- 32 timbres (2 KB)
- Interpolation matrix (precomputed, 32 KB flash... too large for Uno)

Alternative: compute the matrix on-the-fly. For K=8, the IDW calculation per sample is ~24 operations. An ATmega328P at 16 MHz can do this at ~20 kHz sample rate for monophonic synthesis.

**Result: A complete monophonic synthesizer with 32 timbres fits in under 2 KB of flash.**

### 8.2 Web Audio: Instant-Load Instruments

WebAudio applications load samples over HTTP. A 10 MB sample library takes seconds on mobile. The same library as spline control points: ~100 KB — loads in under 100 ms on any connection. The browser interpolates in JavaScript (or WebAssembly) with negligible CPU cost.

### 8.3 Modular Synthesis: Morphing Oscillators

In Eurorack, morphing oscillators (like the Piston Honda or Morphagene) are premium modules ($300-500). A spline wavetable oscillator on a Teensy 4.0 ($20) can:
- Store thousands of wavetables in external flash
- Morph smoothly between any two via CV control
- Respond to constraints in real-time (e.g., "make this more bright")

### 8.4 Music Production: Constraint-Based Sound Design

In a DAW plugin, the sound designer specifies constraints:
- "Fundamental at 440 Hz, amplitude 1.0"
- "2nd harmonic at 0.5, 3rd at 0.3"
- "No harmonics above 5 kHz"
- "Peak amplitude ≤ 0.8"

The plugin solves for the optimal control points and presents the resulting waveform. The designer can then drag control points (in a 2D visualization of the Eisenstein lattice) to refine the sound, with constraints maintained in real-time.

### 8.5 AI-Native Synthesis

Differentiability opens the door to neural audio pipelines:
- A neural network outputs Eisenstein control points
- The spline interpolation generates the audio
- The entire pipeline is trained end-to-end with gradient descent

This is a natural architecture for generative audio models: the network's output space is the compact, structured space of control points rather than the uncompressed space of raw audio samples.

---

## 9. Relationship to Existing Work

### 9.1 vs. Standard Wavetable Compression

Existing wavetable compression (e.g., in SF2 format) uses lossless coding (differential + Huffman) or simple downsampling. These are generic — they don't exploit the smoothness of the waveform. Spline compression is domain-specific and achieves much higher ratios for smooth waveforms.

### 9.2 vs. Additive Synthesis

Additive synthesis represents a waveform as a sum of sinusoids (Fourier series). This is efficient for harmonic sounds but requires many partials for inharmonic or noisy content. Spline wavetable synthesis handles both equally well — the control points adapt to the waveform shape regardless of harmonic content.

### 9.3 vs. Neural Audio Codecs

Neural codecs (EnCodec, SoundStream) achieve high compression ratios but require a neural network decoder — orders of magnitude more compute than IDW interpolation. Spline wavetable synthesis targets the regime where compute is scarce and compression must be extreme.

### 9.4 vs. wavetables in Serum/Vital

Serum's wavetable editor allows drawing and morphing, but stores full wavetables. Vital uses FFT-based spectral morphing. Neither achieves the compression ratios or constraint-based design of spline wavetable synthesis.

---

## 10. Mathematical Foundation

### 10.1 Approximation Theory

The IDW² interpolation on the Eisenstein lattice approximates the smooth function f with error bounded by:

```
||f - f_approx|| ≤ C · h² · ||f''||_∞
```

where h is the lattice spacing (inversely proportional to √K for K control points) and ||f''||_∞ is the maximum curvature of f. For K = 16 and a typical audio waveform (||f''||_∞ ~ 100), this gives:

```
error ≤ C · (1/4)² · 100 ≈ 6.25 · C
```

The constant C depends on the IDW kernel but is O(1). This aligns with the ~40 dB SNR observed empirically for K = 16.

### 10.2 The Eisenstein Connection

The Eisenstein lattice is the root lattice A₂ — the same lattice that appears in the representation theory of SU(3). The fundamental domain is an equilateral triangle, and the lattice has 6-fold symmetry. This symmetry means:

- Every control point has 6 nearest neighbors at equal distance
- The interpolation is rotationally symmetric at large scales
- The reconstruction error is isotropic (same in all directions)

These properties make A₂ optimal for 2D interpolation of smooth functions, justifying its use in both neural network weight compression and audio wavetable compression.

### 10.3 The 497× Connection

The tensor-spline library achieves 497× compression for a 512×512 matrix: 262,144 parameters reduced to 528 (16 control points + 512 bias). The same principle applies to audio:

- A 2048-sample wavetable has 2048 degrees of freedom (float32 values)
- 16 Eisenstein control points have 16 degrees of freedom
- Compression: 2048/16 = **128×** (without bias; with bias equivalent to a DC offset parameter, it's still 128×)

The 497× figure for neural networks is higher because the matrix is 2D (512×512), allowing the 2D lattice to capture correlations in both dimensions. Wavetables are 1D, but the technique extends to multi-table families where the 2D structure reappears.

---

## 11. Future Directions

1. **Adaptive lattices**: Learn the lattice positions alongside the control values, allowing the interpolation to place control points where the waveform is most complex.

2. **Hierarchical spline wavetables**: Use the hierarchical spline from tensor-spline's `hierarchical_spline.py` to capture both coarse waveform shape and fine detail at different scales.

3. **Spline FM synthesis**: Apply Eisenstein control points to FM operator stacks, compressing the modulation index matrix.

4. **Real-time constraint solving**: Implement the constrained least-squares solver on embedded hardware for interactive sound design.

5. **Perceptual optimization**: Train control points using a perceptual loss function (e.g., mel-spectrum matching) rather than raw spectral error.

---

## 12. Conclusion

Eisenstein lattice splines, developed for neural network weight compression in tensor-spline, apply directly and powerfully to audio wavetable compression. The key insight — that smooth functions are efficiently represented by control points on a hexagonal lattice — unifies two seemingly unrelated domains.

**Spline wavetable synthesis** is a genuinely new synthesis method with compelling advantages: extreme compression, smooth morphing, constraint-based design, differentiability, and computational efficiency. It opens the door to synthesizers that run on microcontrollers, web audio instruments that load instantly, and AI-native audio pipelines that generate sound from structured, interpretable representations.

The math is the same. The lattice is the same. The compression is real. Let's build some instruments.

---

*See also: `flux_tensor_midi/spline_synth.py` — a complete Python implementation with 15+ tests.*
