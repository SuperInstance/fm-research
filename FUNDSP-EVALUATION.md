# FunDSP Evaluation: Rust Audio Backend for Constraint Theory Ecosystem

**Date:** 2026-05-23
**Evaluator:** OpenClaw subagent
**Library:** [fundsp](https://github.com/SamiPerttu/fundsp) v0.23.0
**Purpose:** Evaluate suitability as the Rust audio backend for the constraint theory / FM synthesis research ecosystem.

---

## What Is FunDSP?

FunDSP is a Rust-native audio DSP library for real-time audio processing and synthesis. Key characteristics:

- **Functional/composable graph notation** — Audio processing networks are expressed algebraically using Rust operator overloading (e.g., `sine_hz(440) >> lowpass_hz(2000, 1.0)`). No macros required.
- **Zero-cost abstractions** — Graph structure is encoded in Rust types at compile time. Static `AudioNode` graphs compile to stack-allocated, inlined forms. Connectivity errors are caught at compile time.
- **Real-time capable** — Designed for real-time audio with a `no_std` mode, explicit pre-allocation via `allocate()`, and SIMD-accelerated block processing.
- **Rich component library** — Oscillators, filters (lowpass, highpass, bandpass, etc.), noise generators, envelopes, delays, reverb, FFT convolution, and procedural generation tools.
- **Dual component systems** — `AudioNode` (static, stack-allocated, compile-time arity) and `AudioUnit` (dynamic, heap-allocated, runtime arity) for flexibility.

---

## Evaluation Criteria

### 1. API Ergonomics — ★★★★★

**Excellent.** The inline graph notation is arguably FunDSP's strongest feature:

```rust
use fundsp::prelude::*;

// FM synthesis: carrier modulated by modulator
let fm = sine_hz(2.0) * 220.0 * 2.0 + 220.0 >> sine();

// Stereo noise through bandpass filter
let filtered = (noise() | noise()) >> (bandpass_hz(1000, 1.0) | bandpass_hz(1000, 1.0));
```

Operators (`>>` for chaining, `|` for parallel, `*` for modulation) compose naturally. Graph structure is Rust types — compile-time type checking catches wiring errors. The notation is concise enough to serve as a quasi-DSL (the `lapis` project parses it directly).

**For constraint theory:** Mapping constraint outputs to audio parameters is straightforward. A constraint solver produces frequency/amplitude/filter values, and these feed into FunDSP's parameterized components. The type system ensures the graph is valid before runtime.

### 2. Real-Time Safety — ★★★★☆

**Very good, with caveats.**

- **Static graphs (`AudioNode`)** are stack-allocated and avoid runtime allocation. After calling `allocate()`, no further heap allocation occurs — safe for real-time threads.
- **Dynamic graphs (`AudioUnit`)** use heap allocation by nature — not suitable for the hot audio path without careful management.
- `no_std` support is available (disabling `std` feature), enabling use in embedded environments.
- Block processing with SIMD acceleration (via `wide` crate, `f32x8`) is supported.
- The `BlockRateAdapter` handles automatic block processing for generators.

**Caveat:** The library doesn't enforce no-allocation in the audio thread — it's the developer's responsibility to call `allocate()` and avoid dynamic dispatch in the hot path. This is standard for Rust audio but less safe than, say, using `typenum`-enforced static arrays everywhere.

### 3. MIDI Support — ★★★☆☆

**Indirect, via ecosystem.**

FunDSP itself is a pure DSP library — it has no built-in MIDI handling. However:

- **`midi_fundsp`** is a companion crate that bridges MIDI input to FunDSP synthesizers. It handles note-on/note-off, polyphony, and voice allocation.
- FunDSP's `Sequencer` frontend supports event scheduling, which can represent MIDI events.
- For the constraint theory use case, MIDI may not be the primary input — constraint outputs drive parameters directly. But if MIDI I/O is needed, it requires gluing `midir` (or similar) with FunDSP manually, or using `midi_fundsp`.

**Bottom line:** MIDI is possible but not first-class. For a constraint-driven system, this is likely fine — constraints replace MIDI as the control source.

### 4. Integration with Constraint Theory — ★★★★★

**This is FunDSP's sweet spot for our use case.**

The constraint theory ecosystem produces outputs (frequencies, amplitudes, modulation indices, filter coefficients) that need to drive audio parameters. FunDSP excels here:

- **Parameterized components** — Every oscillator, filter, and effect accepts dynamic parameters (Hz, Q, gain, etc.).
- **Tick-level control** — `tick()` processes single samples, allowing per-sample parameter updates from a constraint solver.
- **Block processing** — `process()` handles blocks efficiently, with parameters updateable between blocks.
- **Type-safe graph construction** — The constraint system can programmatically build audio graphs that are verified at compile time.
- **Analytic signal flow** — FunDSP can compute frequency responses of linear networks analytically. This could be fed back into the constraint solver as feedback.

Example integration pattern:
```rust
// Constraint solver produces parameters each audio block
let freq = constraint_solver.solve("carrier_freq");
let mod_index = constraint_solver.solve("modulation_index");

// Feed into FunDSP
let mut synth = sine_hz(mod_freq) * freq * mod_index + freq >> sine();
synth.allocate(sample_rate);
```

### 5. Cross-Platform — ★★★★☆

FunDSP itself is pure Rust with `no_std` support — it runs anywhere Rust does. Platform-specific audio I/O is delegated to `cpal` (which supports ALSA/PipeWire/PulseAudio on Linux, WASAPI/ASIO on Windows, CoreAudio on macOS/iOS, AAudio on Android, WebAudio on WASM).

The `rundsp` crate provides a thin bridge between FunDSP and cpal for quick setup.

**Confirmed platforms:** Linux, macOS, Windows, WebAssembly (via cpal WebAudio backend).

### 6. Binary Size — ★★★★☆

FunDSP is a pure Rust library with minimal dependencies:
- Core dependencies: `wide` (SIMD), `rustfft` (optional, for FFT convolution), `symphonia` (optional, for audio file I/O)
- With `default-features = false` and `no_std`, the dependency tree is very lean
- Typical release builds with FunDSP + cpal should be under 5MB
- Suitable for embedding in applications, games, or even WASM modules

### 7. Maturity — ★★★☆☆

**Mixed signals:**

- **Latest version:** 0.23.0 (released April 2023). The version number suggests active development but pre-1.0 instability.
- **Single maintainer** (SamiPerttu). This is a bus-factor risk.
- **9 open issues, 2 PRs** on GitHub — not heavily trafficked but not abandoned.
- **Active ecosystem:** `bevy_fundsp`, `midi_fundsp`, `lapis`, `quartz` all build on it.
- **Well-documented:** The README is comprehensive with extensive examples. API docs on docs.rs.
- **No formal stability guarantee.** Breaking changes between minor versions are possible.

**Assessment:** Mature enough for research and prototyping. Not yet at "production-stable 1.0" status, but the core abstractions are solid and unlikely to change dramatically.

### 8. Comparison with Alternatives

| Criterion | FunDSP (Rust) | CPAL Direct (Rust) | DAWDreamer (Python) | Faust (DSL) |
|---|---|---|---|---|
| **Level** | Mid-level DSP | Low-level I/O only | High-level DAW | DSL → compiled code |
| **Graph composition** | Type-safe algebraic | Manual callback | Python graph API | Block-diagram DSL |
| **Real-time** | Yes (with care) | Yes (manual) | Offline/rendering | Yes (compiled) |
| **MIDI** | Via midi_fundsp | Manual | Built-in | Via architecture files |
| **Constraint integration** | Direct (Rust) | Manual wiring | Python (easy glue) | External control |
| **Performance** | Near-native (SIMD) | Native | C++ backend, Python overhead | Highly optimized |
| **Binary size** | Small | Minimal | Large (JUCE) | Small (generated C) |
| **Maturity** | Pre-1.0, active | Stable, widely used | Research-grade | Mature, academic |
| **Language lock-in** | Rust | Rust | Python | None (compiles to many) |
| **Learning curve** | Moderate | Low (but tedious) | Low | Steep (new language) |

**Key insight:** FunDSP and CPAL are complementary, not competing. FunDSP handles DSP; CPAL handles audio I/O. The real comparison is FunDSP vs. raw CPAL callback code vs. higher-level alternatives.

---

## Recommendation

### ✅ YES — Adopt FunDSP as the Rust audio backend, with caveats.

**Reasoning:**

1. **Perfect fit for constraint-driven audio.** FunDSP's parameterized, composable graph model maps naturally to a constraint solver's output. This is the primary requirement, and FunDSP nails it.

2. **Rust-native.** If the constraint theory ecosystem is in Rust (or has Rust bindings), FunDSP keeps everything in one language with zero FFI overhead. This matters for real-time performance and type safety.

3. **Ergonomic enough for research.** The inline graph notation lets researchers express FM synthesis, filters, and modulation quickly — essential for rapid prototyping.

4. **Combine with CPAL for I/O.** Use `cpal` for audio device interaction and `fundsp` for all DSP. The `rundsp` crate can bootstrap this integration.

**Caveats to manage:**

- **Pre-1.0 risk:** Pin the version (`fundsp = "0.23.0"`). Expect minor API changes. Abstract FunDSP behind a thin adapter layer so the constraint system isn't tightly coupled to FunDSP's API.
- **Single maintainer:** If FunDSP stagnates, the adapter layer means you can swap backends without rewriting the constraint system.
- **MIDI:** If live MIDI input is needed, budget time to integrate `midi_fundsp` or `midir`. For pure constraint-driven audio, this is a non-issue.
- **Documentation gaps:** The README is excellent but there's no comprehensive API guide. Expect to read source code for advanced use cases.

**Suggested architecture:**
```
Constraint Solver → Parameter Bridge → FunDSP Graph → CPAL Audio Output
                         ↑
                    Adapter Layer
                    (isolate fundsp API)
```

The adapter layer is key — it costs almost nothing to build but provides insurance against FunDSP API churn or a future backend switch (e.g., to Faust-generated code).

---

*Report generated for the SuperInstance/fm-research project.*
