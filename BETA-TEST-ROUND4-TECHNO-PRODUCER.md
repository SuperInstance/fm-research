# BETA TEST REPORT — Round 4: The Techno Purist

**Tester:** Berlin-based techno producer, Ableton Live user, modular enthusiast  
**Date:** 2026-05-23  
**Packages tested:** `flux-tensor-midi` v0.1.2, `constraint-synth` v0.1.0  
**Environment:** Python 3.10, WSL2, DawDreamer 0.8.3 available (no SoundFonts)  
**Test results:** 390/390 tests passing (340 flux-tensor-midi + 50 constraint-synth)

---

## 1. Setup & Installation

```bash
gh repo clone SuperInstance/flux-tensor-midi
gh repo clone SuperInstance/constraint-synth
pip install -e .   # both packages
```

`flux-tensor-midi` installed cleanly — zero dependencies, as advertised. `constraint-synth` hit a setuptools flat-layout error (`Multiple top-level packages discovered in a flat-layout: ['demos', 'constraint_synth']`). Fixed by adding `[tool.setuptools.packages.find]` with `include = ["constraint_synth*"]` to `pyproject.toml`. This is a packaging bug that should be fixed upstream.

**Installation rating: 7/10** — minor packaging issue, otherwise smooth.

---

## 2. Test Results

### 2a) Techno Loop at 132 BPM, 16 bars

```python
from flux_tensor_midi.tracks import techno_loop
arr = techno_loop(bpm=132, bars=16, seed=42)
arr.generate_all()
events = arr.to_midi_events()
# → 2560 events across 3 tracks (kick, synth, arp)
```

**Output quality:** The MIDI generation works mechanically — 2560 events across kick (ROOT role), synth (OFFSET role), and arp (DOUBLETIME role). The event density is correct: arp generates 3x more events than kick or synth, matching the doubletime rhythmic role. Events carry proper timestamps, velocities, and durations.

**What's wrong:**
- The note mapping is crude. `Track.generate()` maps FluxVector channels 0–8 to notes via `(channel * note_range // 9)`, producing a fixed note-per-channel grid. There's no actual pitch content — no scales, no key, no chord tones. For techno, you'd want the kick on MIDI 36, the synth playing actual notes from a scale (A minor, probably), and the arp following a chord progression. Currently it's random pitch clusters.
- No velocity patterning beyond the initial FluxVector salience values. A real techno track has very specific dynamics: the kick is always 120+, the hi-hats have a clear accent pattern, the synth swells and recedes.
- The `techno_loop()` preset has no hi-hat track. Three instruments: kick, synth, arp. Where's the hi-hat? The most important element in techno after the kick.

**Production-ready?** No. Good as a proof-of-concept for the tensor → MIDI pipeline, but musically unusable. Needs scale/key awareness, velocity patterns, and proper drum voice assignment.

### 2b) Kick Drum via Constraint Synth

```python
synth = ConstraintSynth.from_preset('808_kick')
signal = synth.play_note(pitch=36, velocity=120, duration=0.5)
# → 22050 samples, 0.5s, peak=0.9445
```

**Output quality:** The 808_kick preset produces a clean sine wave with fast attack and a 400Hz lowpass. It's a technically correct sub-bass tone. The 0.5s duration with attack=0.001 and release=0.35 gives a smooth exponential-ish decay.

**What's wrong:**
- It's just a sine wave. A real 808 kick has a pitch envelope — the oscillator starts at ~150Hz and sweeps down to ~40Hz over 50-100ms. This creates the characteristic "boom." Without that pitch sweep, it's a bass tone, not a kick.
- No transient. A kick drum needs a sharp click at the attack (noise burst, high-pass filtered, 5-10ms). The current preset is all body, no attack.
- The lowpass at 400Hz is good for the fundamental, but a real 808 benefits from some harmonics in the initial transient (maybe a brief square wave burst mixed in).
- No distortion/saturation. Every techno producer drives their 808s through saturation. The mathematical purity is the enemy here.

**Production-ready?** No. It's a sine wave, not a kick. Closest to a clean sub-bass. Needs pitch envelope, transient layer, and saturation to compete with a hardware 808 or even a sample.

### 2c) Hi-Hat Pattern with Micro-Timing

```python
# Eisenstein lattice oscillator + noise for metallic content
hh_osc = LatticeOscillator(frequency=8000.0, lattice_shape='eisenstein', 
                           noise_floor=0.3, lattice_stretch=1.02)
hh_env = FunnelEnvelope(attack=0.0001, decay=0.03, sustain=0.1, release=0.02)
# 16th note pattern with ±5-15ms micro-timing offsets
# → 3.8s pattern, 4 bars
```

**Output quality:** The eisenstein snap at 8kHz with 30% noise floor produces an interesting metallic texture. The staircase quantization from the hexagonal lattice creates harmonically rich content that's vaguely cymbal-like. The micro-timing via random offsets (±5-15ms) does create a more human feel.

**What's wrong:**
- The "eisenstein snap" at audio rate creates staircase quantization noise, which is harsh and digital. Real hi-hats have noise that's band-pass filtered (6-12kHz) with very specific resonant peaks. The lattice snap doesn't approximate this well.
- No band-pass filtering specific to cymbals. The 12kHz lowpass helps but isn't enough — you need a narrow bandpass around 8-10kHz with resonance.
- Micro-timing via random offsets is the wrong approach. In techno, the swing/groove is deterministic and repeatable (the same pattern every bar, like a Jomox XBase or TR-909 swing setting). Random offsets sound sloppy, not groovy.
- The FunnelEnvelope's decay=0.03s is too long for a closed hi-hat (should be ~5-10ms) and the sustain=0.1 means there's a sustained tone, which sounds like a sustained drone, not a percussive hit.

**Production-ready?** No. Interesting texturally but not a hi-hat. The eisenstein lattice concept is intriguing for experimental sound design, but it needs bandpass filtering and proper percussive envelopes.

### 2d) 128-Bar Evolving Arrangement

```python
arr = techno_loop(bpm=132, bars=128, seed=7)
arr.generate_all()
# → 20480 events
```

**Output quality:** Scales linearly — 128 bars generates 8x the events of 16 bars. Generation is fast (<1s for all events). The system handles long arrangements without issues.

**What's wrong:**
- There's no actual evolution. `Track.generate()` uses the same FluxVector state for every tick. A 128-bar techno arrangement should have build-ups, breakdowns, drops, filter sweeps, element introductions. Currently it's 128 identical bars.
- No arrangement intelligence. No concept of "introduce the kick at bar 1, add hi-hats at bar 9, drop to kick-only at bar 33, full elements at bar 41."
- The `Arrangement.loop()` method just repeats with time offsets — no variation, no evolution. It's copy-paste, not arrangement.

**Production-ready?** No. A 128-bar arrangement needs structure, dynamics, and evolution. This is a flat repeating pattern.

### 2e) DawDreamer Bridge

```python
from flux_tensor_midi.audio.dawdreamer_bridge import create_renderer, find_soundfonts
renderer = create_renderer()  # → DawDreamerRenderer (dawdreamer installed)
sf2 = find_soundfonts()       # → [] (no SoundFonts found)
```

**Output quality:** The DawDreamerRenderer class is well-structured with proper VST and SoundFont loading, MIDI file generation from events, and WAV output. The `create_renderer()` factory correctly detects DawDreamer and returns the real renderer.

**What's wrong:**
- No SoundFonts available in the default environment. The `_detect_sf2_paths()` searches standard locations but finds nothing on WSL2. There's no bundled SF2 or download helper.
- The MockRenderer generates silent WAVs, which is fine for testing but useless for actual audio production.
- No VST discovery. On a real production machine, you'd want to auto-detect VST paths (Ableton's plugin folders, etc.).
- The MIDI file generation from `MidiEvent` → `MidiExportConfig` → `build_midi_file()` works, but the tick conversion (`start_tick = int(start_ms / 1000.0 * (bpm / 60.0) * ppqn)`) could have rounding issues for complex rhythms.

**Production-ready?** Infrastructure is solid. Needs better SoundFont/VST discovery and ideally a bundled GM SoundFont for immediate audio output.

### 2f) Flux Bridge for Direct Audio Render

```python
bridge = FluxBridge(preset='techno_bass')
audio = bridge.render_events(events)  # 384 events → 30s audio
bridge.to_wav(audio, 'output.wav')
# Render time: ~200ms for 32 events, ~2s for 384 events
```

**Output quality:** The FluxBridge is the star of the show. It takes MidiEvent objects directly and renders them through ConstraintSynth with proper timing, overlapping, and normalization. The `render_flux_sequence()` method allows direct FluxVector → audio without MIDI intermediation. The `render_flux_vector()` with 9-channel parameter mapping (pitch, dynamics, timbre, brightness, space, tension, noise, snap, weight) is genuinely innovative.

**What's wrong:**
- The `ConstraintSynth` is stateful (BiquadLowpass, SchroederReverb have internal state). When rendering overlapping notes via `render_events()`, the filter/reverb state from one note bleeds into the next. This can be desirable (reverb tail) or problematic (filter resonance buildup).
- Audio quality is limited by the underlying synth — sine waves and basic saw/triangle don't compete with commercial soft synths.
- The `render_events()` method creates a fresh `ConstraintSynth` internally (from the preset), so all notes use the same timbre. No per-track or per-channel instrument assignment.
- Normalization after rendering is destructive — if one note peaks at 1.0, the whole mix gets turned down. Per-track gain staging would be better.

**Production-ready?** Close. The architecture is right, but the audio quality needs significant improvement to be usable in a real production. As a prototyping/sketching tool, it works.

---

## 3. IDEATION SESSION — Can This Create a Berghain-Worthy Techno Track?

### Can This System Create a Berghain-Worthy Techno Track?

Let's be honest: not today. Not this year. But the *architecture* has something that existing tools don't, and that's worth exploring.

A Berghain-quality techno track — think Marcel Dettmann, Ben Klock, Rødhåd — has several characteristics that make it extraordinarily difficult to generate algorithmically:

**1. Sound Design Precision**

Techno lives and dies by sound design. A Ben Klock kick isn't just a sine wave with a pitch envelope — it's layered: a sub sine with a precise pitch sweep (starting at ~120Hz, landing at ~45Hz over 80ms), a midrange transient layer (noise burst through a resonant filter at ~200Hz, 10ms), and sometimes a third layer for punch (compressed square wave, 5ms). The constraint-synth's lattice oscillator can produce the base sine, but it lacks pitch envelopes entirely. The oscillator frequency is set once per note and stays fixed. For a kick drum, you need `frequency` to be a function of time within a single note — this is a fundamental architectural gap.

The eisenstein lattice snap is genuinely interesting for metallic/percussive sounds. The staircase quantization creates harmonics that are related to the fundamental but not in a standard harmonic series. This is actually similar to what happens when you ring-modulate or frequency-shift a sound — you get non-integer harmonics that can sound metallic and alien. In the right context (a filtered noise burst through an eisenstein oscillator at 6-8kHz, band-passed, with a 3ms decay), this could produce usable hi-hat and cymbal sounds. But the current implementation doesn't have the filtering or envelope precision to get there.

**2. Groove and Micro-Timing**

Techno groove isn't random — it's precise. A TR-909 has a specific swing feel because of its clock architecture. Ableton's groove pools extract timing from real performances. The Eisenstein snap concept (snapping to hexagonal lattice points) is actually a really clever mathematical framework for groove: the covering radius of 1/√3 ≈ 0.577 provides a natural "snap window" that's tighter than a simple grid but looser than exact timing. This is the right idea.

But the current implementation doesn't use it for actual timing. The `EisensteinSnap` class exists in the tensor domain, but when it comes to actual MIDI event timing, the `Track.generate()` method uses `RoomMusician.emit()` which returns timestamps from the T-0 clock's EWMA — and that EWMA is just smoothing jitter, not creating groove. A real techno groove would use the Eisenstein lattice to snap note onsets to specific rhythmic positions (slightly ahead of the grid for push, slightly behind for laid-back feel) with the snap ratio determining the groove amount.

**3. Arrangement and Tension**

A 128-bar techno arrangement has very specific structural requirements: 16 bars of kick-only intro, gradual introduction of elements (hi-hats at bar 17, synth pad at bar 33, bass line at bar 49), a breakdown (everything drops out except a filtered pad at bar 65), tension build (noise sweep, rising filter, element reintroduction), and a drop (full power at bar 81). The `Arrangement` class has no concept of any of this. The `loop()` method is literally just time-offset repetition.

What's needed is an arrangement DSL — something like:
```python
arr.section("intro", bars=16, tracks=["kick"])
arr.section("build", bars=16, tracks=["kick", "hat"], filter_sweep=(200, 8000))
arr.section("breakdown", bars=16, tracks=["pad"], filter_sweep=(8000, 200))
arr.section("drop", bars=16, tracks=["kick", "hat", "bass", "synth"])
```
This could integrate with the FluxVector system — each section gets different salience profiles, and the transition between sections is a morphing of the FluxVector states.

**4. Modular Integration: CV Output and OSC**

This is where I get excited. The FluxVector's 9 channels are essentially a high-dimensional control signal. In modular synthesis, you'd map these to CV:

| FluxVector Channel | CV Destination |
|---|---|
| Arousal (0) | Filter cutoff |
| Valence (1) | VCA level |
| Dominance (2) | Wavefolder depth |
| Uncertainty (3) | S&H sample rate |
| Novelty (4) | LFO rate |
| Relevance (5) | Envelope sustain |
| Competence (6) | FM index |
| Affiliation (7) | Pan position |
| Urgency (8) | Reverb send |

The `OscBridge` class in `daw_bridge.py` already has OSC support (`_send_osc`, `_osc_pad`, `_osc_string`). Extending this to output CV-compatible signals (0-5V via Expert Sleepers ES-8 or similar DC-coupled audio interface) would be straightforward — the FluxVector values are already normalized 0-1, you just need to scale to the appropriate voltage range and output at audio rate through a DC-coupled output.

For OSC, the `OscBridge` class is already structured to send `/flux/channel/{n}` messages. Adding bi-directional OSC (receiving sensor data back from the modular) would close the loop: modular → sensors → FluxVector → constraints → CV back to modular. This is a genuinely new paradigm for human+AI modular performance.

**5. Sound Quality vs. Hardware**

Current constraint-synth sound quality: 3/10 compared to hardware.
- Sine oscillator: Clean but sterile. No analog drift, no temperature-dependent tuning. A hardware VCO has subtle pitch wobble and harmonic content that this lacks.
- Square/saw oscillators: The PolyBLEP anti-aliasing is a nice touch (reduces aliasing at discontinuities), but the waveforms are still mathematically perfect. They sound digital in the bad way.
- Filter: The BiquadLowpass is technically correct but sounds clinical. A Moog-style ladder filter has nonlinear resonance that self-oscillates musically. The biquad is transparent, which is the opposite of what you want in techno.
- Reverb: The Schroeder reverb is a 1960s algorithm. It works but sounds metallic and cold. For techno, you want convolution reverb (sample an actual warehouse, Berghain's room sound) or at minimum a Valhalla-style algorithmic reverb with diffusion.

The gap is significant but not insurmountable. Adding wavetable oscillators (scan through single-cycle waveforms sampled from hardware), nonlinear filter models (circuit simulation or at least OTA-style saturation), and convolution reverb would bring the quality from 3/10 to maybe 7/10.

**6. Dream: A Constraint Module for Eurorack**

Here's my dream product: a 10HP Eurorack module called **CONSTRAINT**.

Front panel:
- 9 CV inputs (one per FluxVector channel, 0-5V)
- 9 CV outputs (the constrained/quantized values)
- Lattice shape knob (sine → square → saw → triangle → eisenstein, continuously variable)
- Stretch knob (lattice stretch, 0.9–1.1)
- Snap knob (soft → hard snap threshold)
- Tolerance knob (how much deviation from the lattice is allowed)
- Side-channel buttons: NOD (trigger output, "I acknowledge"), SMILE (gate high, "this works"), FROWN (gate low, "something's off")
- Clock input/output (Eisenstein-snapped timing)
- USB-C for firmware updates and FluxVector preset loading

What it does: takes 9 CV inputs, snaps them to the constraint lattice, outputs the quantized result. The lattice shape determines the snap behavior — sine is transparent (pass-through), square forces binary (on/off), eisenstein creates hexagonal quantization patterns. The stretch knob introduces inharmonicity. The tolerance knob controls how aggressively the snap happens.

Why this matters: it's a quantizer, but not for pitch. It quantizes *intent*. You plug 9 LFOs or random sources into the inputs, dial in the lattice shape and snap amount, and get musically structured control signals out. The side-channel outputs create feedback loops between modules — if the constraint system "approves" of the current state (NOD output fires), another module can advance to the next step. If it "frowns" (FROWN output fires), a modulation source gets attenuated.

The T-0 clock feature is also powerful in hardware: each module runs its own clock with EWMA drift correction. You can have multiple CONSTRAINT modules in a system, each with slightly different clock speeds, and they naturally synchronize through the side-channel communication. This is literally how a band of humans plays together — each person has their own internal tempo, and they adjust to each other through non-verbal cues.

Price target: €250–350. STM32H7-based, 12-bit ADC/DAC, open-source firmware. The constraint-theory math runs in real-time on the MCU.

### Overall Assessment

| Dimension | Rating (1-10) | Notes |
|---|---|---|
| Architecture | 9 | Elegant, mathematically grounded, extensible |
| Sound Quality | 3 | Basic oscillators, needs major work |
| Musical Intelligence | 2 | No scale/key/arrangement awareness |
| Groove/Timing | 5 | Eisenstein snap concept is great, poorly applied |
| Code Quality | 8 | Clean, well-tested (390 tests), good docs |
| Modular Potential | 9 | CV/OSC integration could be transformative |
| Production Readiness | 2 | Can't make a releasable track yet |
| Innovation | 10 | Genuinely new paradigm — constraint theory → music |

### Recommended Priority Improvements (for techno use case)

1. **Pitch envelopes on the oscillator** — frequency as a function of time within a note. This is essential for any percussive sound (kick, snare, tom). Without it, you can't make drums.

2. **Scale/key awareness** — the `Track.generate()` method should accept a scale and root note, and generate notes from that scale. This is table stakes for any music generation system.

3. **Arrangement sections** — add a DSL for intro/build/breakdown/drop with per-section track visibility and FluxVector morphing.

4. **Hi-hat track in techno_loop** — it's missing. Add it with DOUBLETIME role.

5. **Deterministic micro-timing** — replace random offsets with Eisenstein-snapped groove patterns. Let the user specify a "swing" amount (0 = straight, 1 = maximum swing) and snap to the lattice accordingly.

6. **Nonlinear filter models** — replace the biquad with at minimum a Moog-style ladder filter simulation. Saturation on the filter drive is crucial for techno.

7. **Convolution reverb** — or at least better algorithmic reverb with diffusion. The Schroeder is too metallic.

8. **Per-track instruments in FluxBridge** — allow different ConstraintSynth presets per MIDI channel so the kick sounds different from the synth.

9. **Bundled SoundFont** — include a basic GM SoundFont with the DawDreamer bridge so you get audio output out of the box.

10. **CV calibration mode** — for the Eurorack module dream, add a mode that outputs steady DC voltages at known levels for calibrating the DAC/ADC in the modular system.

---

## 4. Audio Output Files

Generated during testing:

| File | Duration | Description |
|---|---|---|
| `output/kick_808.wav` | 0.5s | 808 kick preset, sine + lowpass |
| `output/techno_bass.wav` | 0.3s | Techno bass preset, saw + filter |
| `output/hihat_pattern.wav` | 3.8s | Eisenstein hi-hats with micro-timing, 4 bars |
| `output/techno_bridge.wav` | 30.0s | Full FluxBridge render of 384 events |
| `output/bridge_direct.wav` | 15.3s | Comparison render, 32 events |
| `output/flux_sequence.wav` | 5.3s | Direct FluxVector sequence render |
| `output/techno_dawdreamer.wav` | 230.2s | DawDreamer bridge render (silent, no SF2) |
| `output/techno_full_16bars.wav` | 30.1s | Full 16-bar techno track (kick + hat + bass) |

---

## 5. Bugs Found

1. **constraint-synth packaging error** — `pyproject.toml` missing `[tool.setuptools.packages.find]`, causing `pip install -e .` to fail with "Multiple top-level packages."

2. **Negative sample index in micro-timing** — When micro-timing offsets push `start_ms` below 0, `int(start_ms / 1000.0 * sr)` produces negative sample indices, causing `ValueError: operands could not be broadcast together with shapes (0,)` in array slicing. The `FluxBridge.render_events()` has the same potential issue.

3. **ConstraintSynth stateful filter/reverb** — The `BiquadLowpass` and `SchroederReverb` maintain internal state. When reused across multiple `play_note()` calls with the same `ConstraintSynth` instance, filter resonance and reverb tail from previous notes bleed into subsequent notes. For some use cases (reverb tail) this is desired; for others (filter on a new note) it's problematic. There should be a `reset()` method or a stateless mode.

4. **FunnelEnvelope with sustain=0** — When `sustain=0`, the envelope produces a release that immediately goes to zero. Combined with certain durations, the `_crossfade` method in `ConstraintSynth.render_melody()` can produce empty arrays that cause shape mismatches.

5. **No hi-hat in techno_loop preset** — The `techno_loop()` function creates kick/synth/arp tracks but no hi-hat. For techno, this is like a guitar with no strings.

---

*"The constraint theory is sound. The lattice geometry is beautiful. The music isn't there yet. But the path from here to Berghain is clearer than I expected."*
