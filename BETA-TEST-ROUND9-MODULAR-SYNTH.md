# BETA TEST — Round 9: The Modular Synthesist

**Tester Profile:** Modular synth enthusiast. 6-case Eurorack system. Patch cables, CV, gates, LFOs, envelopes — the whole vocabulary. Has an Expert Sleepers ES-3, a Disting, and a fondness for weird utility modules nobody else stocks.

**Repos evaluated:** `flux-tensor-midi`, `constraint-synth`, `fm-research`

---

## 1. Evaluation

### CV Output: Latent, Not Literal

Neither repo speaks CV natively. That's not a criticism — it's an opportunity. The FluxVector is a 9-channel continuous signal. If you squint, that's already a control voltage source. The salience and tolerance per channel? That's CV scaling and slew. The `FluxVectorMapper` in `flux_bridge.py` maps channels to frequency, filter cutoff, envelope shapes, lattice stretch, and noise floor — all things I'd want on a modular panel as knobs and jacks.

The bridge between `flux-tensor-midi` → `constraint-synth` already does what a modular signal chain does: oscillation → shaping → filtering → output. The `LatticeOscillator` is a VCO. The `FunnelEnvelope` is an envelope generator. The `ConsonanceFilter` is a VCF. They're just living in software.

The gap: no OSC output. No DC-coupled audio interface targeting. No Silent Way or Expert Sleepers protocol. But the *math* is there. The FluxVector channels are already normalized (0–1 float or INT8 -128..127). That's 0–10V if you scale it. Close the gap with an OSC bridge and you've got AI-driven CV.

### Physical Instruments as Modules

The `RoomMusician` concept maps perfectly to modular thinking. Each room is a voice — a VCO + VCF + VCA + envelope. The `Band` class is the patch: who listens to whom, what's the signal flow. The listening matrix in `ensemble/` is literally a patch matrix.

The AI jam system (`ai_jam/agent.py`) with personality-driven constraint profiles is the most interesting thing here for modular. An "AI musician" that responds to context with interval choices, rhythmic density, snap behavior, and dynamics — that's an autonomous generative module. Feed it CV from your system, get musical responses back. It's a Turing Machine on steroids, except it has a theory of mind about what the other musicians are playing.

### Constraints → CV Mapping

This is where constraint-synth shines for modular people. Every parameter has a lattice-theoretic interpretation:

- **Lattice shape** = waveform selector (sine, saw, square, triangle, eisenstein)
- **Lattice stretch** = inharmonicity / FM index
- **Snap threshold** = quantization strength (soft → hard)
- **Deadband funnel** = envelope shape (convergence → pocket → divergence)
- **Consonance threshold** = filter cutoff

These aren't metaphors bolted onto a normal synth. The waveshape *literally is* the lattice geometry. The oscillator snaps continuous phase to discrete lattice directions. Different lattices produce different shapes. That's a module I'd want in my rack — not because it's novel, but because the parameter space is *coherent*. Every knob does something mathematically meaningful, and the interactions between knobs follow from the theory, not from arbitrary design decisions.

### OSC → Expert Sleepers

The ES-3 outputs 8 channels of DC-coupled audio → CV. FluxVector has 9 channels. That's almost too clean. Map channels 0–7 to ES-3 outputs, use channel 8 (weight/urgency) as a gate or trigger. Add an OSC bridge to `flux-tensor-midi` that streams FluxVector values at audio rate (or at control rate — 100Hz is plenty for CV) and you've got real-time AI-driven modular control.

The `TZeroClock` with EWMA drift correction is the secret weapon here. Modular clocks drift. That's part of the charm. But if you want tight sync, you need adaptive clock correction. The T-0 clock already does this — it tracks its own temporal reference point and smooths timing jitter. That's a clock generator module that actually understands groove.

### AI Jam Controlling Modular Voices

The AI jam agent (`AIAgent`) with personality profiles and short-term memory is the killer app. Here's the vision:

1. Your modular plays a phrase → captured as MIDI via a MIDI interface or as audio → transcribed
2. The phrase becomes the "context" fed to the AI jam agent
3. The agent generates a response using its personality profile and constraint semantics
4. The response is streamed as FluxVector → OSC → ES-3 → CV into your modular
5. Your modular responds back → the loop continues

It's a call-and-response jam partner that never gets tired, understands music theory at a lattice level, and can be tuned by adjusting personality parameters (interval preferences, rhythmic density, snap behavior) the way you'd tune a module by turning knobs.

---

## 2. Ideation: Five Eurorack Modules for a Constraint-Theoretic System

### Module 1: Snap Quantizer (6HP)

**What it does:** Quantizes incoming CV to an Eisenstein lattice grid. Not a standard chromatic quantizer — this one uses the hexagonal tiling from EisensteinSnap to snap to musically meaningful intervals based on the covering radius 1/√3 ≈ 0.577.

**Panel:** CV In, CV Out, Lattice Select (Z₂/chromatic, Z/pentatonic, A₂/Eisenstein), Snap Strength (0–100%, from pass-through to hard quantize), Lattice Stretch knob (inharmonicity). Two LEDs showing input vs. snapped value. A "Root" input for transposition.

**Why it matters:** Standard quantizers snap to 12-TET semitones or selected scales. The Eisenstein lattice gives you a two-dimensional snap space where both pitch *and* rhythm can be quantized simultaneously. The stretch parameter lets you detune the lattice — microtonal quantization that still sounds intentional because it follows a coherent geometry. This is the quantizer for people who find standard quantizers too safe.

**Constraint theory connection:** The `EisensteinSnap` class from `flux-tensor-midi/core/snap.py` implements exactly this. The `RhythmicRole` enum (ROOT, HALFTIME, TRIPLET, WALTZ, COMPOUND, DOUBLETIME, OFFSET, QUINTUPLE, SEPTUPLE) maps to Eisenstein ratios that determine quantization behavior. The snap threshold from `LatticeOscillator` controls quantization strength.

### Module 2: Funnel (8HP)

**What it does:** A slew limiter / envelope generator where the slew shape follows the deadband funnel lifecycle: convergence (slew in), pocket (hold), divergence (slew out). This isn't linear slew — it's mathematically shaped by the funnel geometry.

**Panel:** CV In, CV Out, Trigger In, Convergence (attack slew), Pocket Width (hold time/divergence threshold), Divergence (release slew), Mode switch (Slew / Envelope / LFO). The slew shape is the funnel cross-section at the current point in its lifecycle.

**Why it matters:** Every modular system needs slew. But linear slew is boring, and exponential slew is just a design choice. Funnel slew is *structural* — the shape comes from the constraint theory, not from a designer's preference. When you feed it a stepped sequence, the convergence phase pulls toward the target with a shape determined by the Voronoi cell geometry of the funnel. It feels different from any slew I've used — more deliberate, like the voltage *wants* to arrive at its destination through a specific path.

**Constraint theory connection:** The `FunnelEnvelope` from `constraint-synth/envelope.py` implements this as ADSR, but the underlying funnel model is richer. The deadband funnel has three phases: convergence toward a pocket, stability within the pocket (bounded by the deadband), and divergence out of the pocket. Mapping these to slew behavior gives you a slew limiter where the "hold" phase isn't just a delay — it's a region of stability bounded by the deadband threshold.

### Module 3: Consensus (10HP)

**What it does:** A mixer where the output isn't just a weighted sum — it's the consensus of multiple inputs under constraint theory. The module uses Jaccard similarity to measure how "aligned" the inputs are and adjusts the mix accordingly. High consensus (similar inputs) → clean, coherent output. Low consensus (dissimilar inputs) → the module highlights the tension rather than muddying it.

**Panel:** 4 CV/audio inputs with individual attenuvertors, Consensus Output, Tension Output (separate jack for the disagreement signal), Jaccard Window (how many samples to compare), Blend knob (from pure sum to consensus-weighted). LED bar showing real-time consensus level across all inputs.

**Why it matters:** Standard mixers sum. That's fine for most things. But when you're mixing modulation sources — say, two LFOs, a random source, and an envelope — a straight sum often produces mush. Consensus mixing preserves the character of aligned sources while extracting the interesting disagreement as a separate signal. Use the consensus output for your primary modulation, the tension output for secondary modulation or to FM the consensus. It's a mixer that understands *meaning*, not just amplitude.

**Constraint theory connection:** The Jaccard similarity and weighted Jaccard from `flux-tensor-midi/harmony/` compute this. The `Band.harmony()` method already does multi-musician coherence analysis. The chord quality and consonance metrics (`consonance()`, `quality()`) are exactly what the Consensus module would output — a measure of how well multiple signals agree, and a characterization of the nature of that agreement.

### Module 4: Laman Rigidity (8HP)

**What it does:** A structural module that enforces "rigidity" on a patch. Inspired by Laman graph rigidity from constraint theory — a system is rigid when it has exactly enough constraints to be stable but not overdetermined. The module takes N inputs and produces outputs that are "rigid" — no redundant dependencies, no sagging, no overdetermined lock-ups.

**Panel:** 4 inputs, 4 outputs, Rigidity knob (from floppy to rigid), Constraint Count (shows how many independent constraints are active), Lock output (gate high when system reaches rigidity). Mode: Static (hold the rigid state) / Dynamic (continuously rebalance as inputs change).

**Why it matters:** Modular patches can get chaotic. Too many modulation sources feeding too many destinations and everything either locks up (overdetermined) or goes random (underdetermined). The Laman Rigidity module watches the constraint graph of your patch and tells you when you've hit the sweet spot — exactly enough constraints for stability without redundancy. In static mode, it holds that state. In dynamic mode, it continuously adjusts outputs to maintain rigidity as inputs shift. It's a patch diagnostic and stabilizer in one module.

**Constraint theory connection:** Laman graphs are fundamental to constraint theory. A Laman graph on N vertices has exactly 2N-3 edges — minimally rigid. The module monitors the effective constraint count of its inputs and adjusts outputs to maintain exactly this many independent relationships. The `constraint_filter.py` already does this in software — filtering which lattice directions pass based on consonance thresholds. The Laman Rigidity module extends this to the graph of your entire patch.

### Module 5: Tempo Funnel (6HP)

**What it does:** A clock generator where tempo follows the funnel lifecycle. The clock converges to a target BPM (attack), holds in a pocket (stable groove), then diverges (ritardando or accelerando). Each stage's shape is determined by the funnel geometry, not by linear ramps.

**Panel:** Clock Out, Reset In, Target BPM knob (large, center detent at 120), Convergence Rate (how quickly the clock locks to target), Pocket Width (how long it holds steady), Divergence Rate (how quickly it drifts away), Swing amount (Eisenstein-snap to the clock output for groove). Tap tempo button that uses T-0 EWMA for drift-smoothed tap averaging.

**Why it matters:** Every modular system needs a clock. But most clocks are metronomes — perfectly even, perfectly boring. The Tempo Funnel gives you a clock that *breathes*. It locks in, holds, then drifts. The T-0 clock from `flux-tensor-midi` uses EWMA to smooth timing jitter — that's already a better tap tempo than most modules offer. Combined with the Eisenstein snap for swing (snapping clock pulses to rhythmic ratios like 3:2 for triplet swing, 4:3 for compound feel), you get a clock that generates groove mathematically rather than by adding static delay offsets.

**Constraint theory connection:** The `TZeroClock` from `flux-tensor-midi/core/clock.py` is the EWMA drift-corrected clock. The `EisensteinSnap` with `RhythmicRole` ratios provides the swing/groove quantization. The `FunnelEnvelope` lifecycle (convergence → pocket → divergence) maps directly to musical tempo changes: the clock approaches the target BPM, holds it (the "pocket" — where the groove lives), then drifts away (ritardando into a new section, or accelerando into chaos). This is a clock that understands musical form.

---

## 3. The Dream: A Full Constraint Eurorack System

Picture a 6-case system where every module speaks the same mathematical language. The Tempo Funnel drives the clock. The Snap Quantizer tunes your oscillators to lattice geometries. The Funnel shapes every envelope and slew. The Consensus mixer combines modulation sources with semantic awareness. The Laman Rigidity keeps the whole patch stable.

Now add the AI layer. An embedded computer (Raspberry Pi or Bela) runs `flux-tensor-midi`'s AI jam agent. It listens to your system via an ES-3 (CV in), generates musical responses, and streams them back as CV (ES-3 out). The agent's personality — interval preferences, rhythmic density, snap behavior, dynamics — becomes a set of knobs on a panel. Turn up "Coltrane" and the agent gets more adventurous with intervals and rhythm. Turn it down to "Ballad" and it plays sparse, consonant lines.

The FluxVector becomes the lingua franca of the system. Every module accepts and produces FluxVectors over a common bus (think: a Eurorack version of the `Band` class's listening matrix). You don't patch audio — you patch constraint relationships. The patch cables carry meaning, not just voltage.

This isn't science fiction. Every component exists in software today. The gap is hardware: a CV interface, an embedded compute module, and panel designs. The math is done. The software is done. Someone just needs to build the panels.

I'd buy all five modules tomorrow. And I'd pre-order the AI Jam module the day it was announced.

---

## 4. Honest Assessment

**What works:** The mathematical coherence is real. These aren't arbitrary design choices dressed up in theory — the constraint theory genuinely produces meaningful parameter spaces for synthesis. The Eisenstein lattice snap is the most interesting rhythmic quantization I've seen. The FluxVector as a unified control signal is elegant. The AI jam agent with personality profiles is genuinely exciting for live performance.

**What's missing for modular:** CV output. OSC bridge. Silent Way / Expert Sleepers protocol support. Embedded hardware targeting (Bela, Teensy, Pi). Panel layouts. Eagle/KiCad files. A way to get this out of the computer and into a rack.

**What I'd build first:** The Snap Quantizer. It's the most self-contained concept, the easiest to prototype ( Teensy 4.x + DAC + a few knobs), and the most immediately useful in any modular system. The Eisenstein snap algorithm is already implemented and tested. Port it to C++, add a decent DAC, and you've got a module.

**Overall:** This project has the most interesting synthesis theory I've encountered since I first read about West Coast synthesis. The constraint-theoretic approach to every parameter — waveshape, envelope, filter, mix, clock — creates a system where everything connects to everything else through a shared mathematical framework. In modular, where everything already connects to everything else through patch cables, that's not just elegant — it's a perfect fit.

The question isn't whether this theory produces interesting sounds. It does. The demos prove it. The question is whether it can escape the laptop and become hardware. I hope it does.

---

*Beta tester: 6-case Eurorack, Expert Sleepers ES-3, Disting EX, fond of weird utility modules and generative patches. Would rather patch than menu-dive.*
