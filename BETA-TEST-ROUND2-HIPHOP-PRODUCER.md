# BETA TEST REPORT — ROUND 2: THE BEATMAKER
## Persona: Hip-Hop Producer (Ableton, MPC, MIDI controllers, samplers, 808s)

**Date:** 2026-05-23  
**Libraries Tested:** `flux-tensor-midi` v0.1.2, `groove-analyzer` v0.2.0, `constraint-theory-core`  
**Tester:** Simulated hip-hop producer who thinks in drum patterns, 808s, and hi-hat rolls

---

## INSTALL & SETUP

Cloned both repos, `pip install -e .` on each. Zero drama — clean installs, mido/numpy/matplotlib pulled in automatically. `constraint-theory-core` was already present in the workspace.

**Steps:** 3 commands. **First-try success:** ✅

---

## TASK 2a: Trap Beat at 140 BPM

### What I Did
```python
seq = StepSequencer(steps=16)
seq.load_preset("trap_hats")
seq.add_roll("hihat_closed", 12, 15, pattern="straight", velocity=90)
events = seq.render(bpm=140.0, output="/tmp/trap_beat.mid")
```

### Verdict
- **First-try success:** ✅
- **Steps:** 4 lines of code
- The `trap_hats` preset is legit — kick on 0/5/10, snare on 4/12, rapid hats everywhere, open hat accents on 7/15. That's a functional trap pattern.
- Adding a hi-hat roll was one function call. Felt natural.
- **What felt natural:** `load_preset("trap_hats")` → instant pattern. `add_roll()` → instant roll. This is MPC-pad-level simplicity.
- **Confusing parts:** Step numbers are 0-indexed. Not a dealbreaker but producers think in beat numbers (1-4) or grid positions (1-16). Mental math: "snare on 2 and 4" = "steps 4 and 12 in a 16-step grid at 140 BPM." Would love a `add_hit("snare", beat=2)` or similar.

---

## TASK 2b: Boom-Bap Beat at 90 BPM with Swing

### What I Did
```python
seq = StepSequencer(steps=16)
seq.load_preset("boom_bap")
seq_humanized = seq.humanize(swing=0.6, velocity_range=12, timing_range=8, seed=42)
events = seq_humanized.render(bpm=90.0, output="/tmp/boombap_beat.mid")
```

### Verdict
- **First-try success:** ❌ **BUG: MIDI export crashes with negative tick values**
- The `_write_midi()` method in `sequencer.py` converts `start_ms` to ticks using floating-point math. When swing + timing offset pushes an event's start time slightly negative (or the rounding creates a negative delta between sorted events), mido rejects it: `ValueError: message time must be non-negative in MIDI file`.
- **Workaround:** Set `timing_range=0` and reduce swing, or render without file output and write MIDI manually.
- This is a real problem. A producer adding swing to a beat and hitting export shouldn't get a traceback.
- **Fix needed:** Clamp all tick deltas to ≥ 0 in `_write_midi()`, or shift the entire timeline so the earliest event starts at 0.
- The `boom_bap` preset is solid though — kick-snare-kick-snare with hats, ghost kick on step 6. That's the recipe.

---

## TASK 2c: Groove Analysis of Both Beats

### What I Did
```python
timing = extract_microtiming("/tmp/trap_beat.mid", grid_division=16)
fit = fit_deadband(timing)
proof = prove_groove_is_deadband(timing)
```

### Verdict
- **First-try success:** ✅
- **Steps:** 3 lines per beat
- This is genuinely cool. The analysis correctly identified:
  - **Trap beat:** ε=0.9ms, genre match = EDM (because quantized hats are machine-tight), 100% coverage
  - **Boom-bap beat:** ε=18.1ms, genre match = **Hip-hop** ✅, 100% coverage
- The boom-bap's 18ms deadband is right in the hip-hop sweet spot (the genre profiles say Hip-hop ε≈20ms).
- `prove_groove_is_deadband()` returns a dict with coverage, variance_collapse, genre_coherence — scientifically satisfying.
- **What felt natural:** The API flow. Extract timing → fit deadband → prove. Clean pipeline.
- **Confusing parts:** Only 1 track detected (since everything's on channel 10). The `pocket_pct` came back as 10000% which seems like a percentage display bug (should be 100%?).
- **Producer take:** I'd use this to A/B my beats against genre benchmarks. "Is my swing actually pocketed?" This answers it with numbers.

---

## TASK 2d: 32-Bar Arrangement (Intro/Verse/Chorus/Verse/Outro)

### What I Did
Two approaches:
1. `Arrangement` class with `Track` objects — generates 5632 events across 32 bars automatically
2. Manual section-building with `StepSequencer` — chain 16-step patterns with time offsets for each section

### Verdict
- **First-try success:** ✅ (manual approach), ⚠️ (Arrangement class)
- **Steps:** ~40 lines for manual section-based arrangement
- The `Arrangement` class works but generates very abstract events — FluxVector channels → MIDI notes. The results are musically ambiguous (random-seeming note choices from channel-to-note mapping). Not a "producer" tool yet.
- Manual approach (sequencing sections with `StepSequencer` per section, offsetting by bar duration) is more like what a producer actually does — build a loop, copy it, vary it.
- **What felt natural:** The concept of chaining sequencer patterns with time offsets. Every DAW works this way.
- **Confusing parts:** The `Arrangement` class doesn't have section markers, mute/unmute, or pattern switching. You'd need to build all that yourself. No `arrangement.add_section("verse", bars=8, pattern=verse_pattern)` API.
- **Missing for producers:** Song mode / arrangement view. Pattern chains. Per-section instrument muting (like "drop the kick in the intro, bring it in at verse 1").

---

## TASK 2e: Bass Line Using the Constraint Solver

### What I Did
Used `constraint-theory-core`'s `Metronome` + `henneberg_construct` + `optimal_coupling` to run distributed consensus across 5 agents, then mapped the converged phases to C minor pentatonic notes.

### Verdict
- **First-try success:** ⚠️ (technically works, but...)
- **Steps:** ~50 lines of code, most of which is manual mapping from math → music
- **This is the biggest gap.** The constraint solver provides mathematical primitives (Laman rigidity, consensus, deadbands) but has ZERO musical mapping. There's no `generate_bass_line(key="C", scale="minor_pentatonic", pattern="quarter_notes")` function.
- The mapping from oscillator phases → scale degrees → MIDI notes is entirely manual. A producer would never figure this out.
- **What the constraint solver actually gives you:** Mathematical guarantee that N agents reach consensus. Cool for distributed systems. Not cool for writing a bass line.
- **What producers need:** "Constrain this bass line to C minor, resolve to the root on beat 1, avoid parallel fifths." That's a very different kind of constraint solver.
- **Bottom line:** The constraint solver is impressive math. It's not a music tool. Yet.

---

## TASK 2f: Euclidean Rhythms on Hi-Hats

### What I Did
```python
seq.euclidean("hihat_closed", steps=16, pulses=7, rotation=2, velocity=80)
seq.euclidean("hihat_open", steps=16, pulses=3, rotation=0, velocity=70)
seq.euclidean("rimshot", steps=16, pulses=5, rotation=1, velocity=60)
```

### Verdict
- **First-try success:** ✅
- **Steps:** 3 function calls
- **This is the most fun I had.** Euclidean rhythms are a producer secret weapon — E(3,8) on hats, E(5,16) on percussion, E(7,16) on rims. Instant polyrhythmic texture.
- The API is clean: `instrument, pulses, rotation, velocity`. Rotation is the secret sauce — shift the pattern by a few steps and the whole groove transforms.
- Björklund's algorithm is correctly implemented. The patterns sound right.
- **What felt natural:** This is exactly how you'd want it. Name the drum, pick the density, rotate. Done.
- **Producer take:** I'd use this constantly. Layering Euclidean hats over a straight kick-snare is a go-to technique. Having it as one function call instead of manually placing hits? Yes please.

---

## TASK 2g: Export Everything to MIDI

### What I Did
`seq.render(bpm=140.0, output="file.mid")` for each beat. Also manual MIDI writing via mido for the arrangement.

### Verdict
- **First-try success:** ✅ (when no humanize/swing), ❌ (with humanize — the negative tick bug)
- **Steps:** 1 line per export (when it works)
- When it works, it's seamless. One parameter and you get a valid .mid file.
- The negative tick bug makes humanized export unreliable. This needs fixing before release.
- All channels go to channel 10 (drums) by default, which is correct for GM percussion.
- **Missing:** Multi-track export. Everything dumps to one track. A producer wants kick on track 1, snare on track 2, hats on track 3, bass on track 4. This is critical for mixing in a DAW.

---

## IDEATION SESSION: Can This Replace My MPC?

### Can flux-tensor-midi replace an MPC?

**Short answer: No. Not today. But the bones are interesting.**

An MPC is a physical instrument. It's pads under your fingers, 16 levels of velocity sensitivity, the feel of a snare when you tap it hard vs. ghost-tap it soft. It's also 30 years of workflow refinement — the 16-pad grid, the timeline, the step editor, the pad mixer, sample chopping with start/end points and truncation. You don't think about any of that; your fingers just know where to go.

flux-tensor-midi is a *theory engine* wearing a drum rack costume. The StepSequencer is genuinely usable — I built trap beats, boom-bap patterns, Euclidean polyrhythms in a few lines of code. The drum rack's GM map is complete and correct. The presets are musically literate. But it's all code. You write `seq.add_hit("kick", 0, 115)` instead of tapping a pad. For a programmer-producer, that might be fine. For most beatmakers, it's a non-starter.

The theoretical foundation — FluxVectors, Eisenstein snaps, T-0 clocks, deadband funnels — is fascinating from an academic perspective. But as a producer, I don't think in 9-channel arousal/valence/dominance tensors. I think "kick on 1, snare on 2-and-4, hats going 16ths with a little swing, maybe a roll on the 4." The mapping between producer-think and tensor-think is missing. The `GenreBrain` class gets closest — load "hiphop" and it configures salience profiles and tolerance vectors — but the output is still abstract FluxVector states, not drum patterns you can hear.

### What would make me switch?

1. **A browser-based or app-based UI.** Pads I can tap. A piano roll. A timeline with drag-and-drop. Code is for programmers; beats are for feel. If there was a web UI where the pads hit the StepSequencer underneath, I'd be interested.

2. **Real-time playback.** I need to hear the beat as I build it. Currently, I export to MIDI, load it in Ableton, assign sounds, and THEN I hear it. That's a 5-step round-trip for every edit. An MPC plays back instantly.

3. **Audio, not just MIDI.** Every beat starts with sound selection. I browse through 808 samples until I find the right one — the one that shakes the room, sits in the pocket, tunes to the key. flux-tensor-midi only generates MIDI note data. No audio. No samples. No synthesis. An 808 kick is just note 36 on channel 10. That's like writing a recipe that says "add protein" without specifying chicken or tofu.

4. **Undo/redo, drag-and-drop, pattern chaining.** These aren't luxuries; they're the workflow. I need to try a hi-hat pattern, decide it's wrong, undo it, try another one. I need to drag a 4-bar verse loop onto the timeline 8 times for the verse. I need to mute the kick during the intro and bring it back for the drop. None of this exists in the code API.

5. **Integration with my DAW.** I live in Ableton. If flux-tensor-midi was an Ableton plugin (Max for Live device, VST, or even a MIDI output I can route), I'd use it. The `daw_bridge.py` adapter exists but seems to be a stub referencing dawdreamer.

### The Drum Rack — Toy or Tool?

**Tool. A real one. But a specialized tool.**

The `DrumRack` + `StepSequencer` combo is the strongest part of this library. The GM percussion map is complete (36 instruments from kick to triangle). The step sequencer has:
- 8/16/32 step grids ✅
- Hit placement with velocity ✅
- Rolls (straight/triplet/dotted) ✅
- Flams ✅
- Euclidean rhythms ✅
- Humanize with swing ✅
- 6 genre presets ✅
- MIDI export ✅

That's a functional drum programmer. The Euclidean rhythm generator alone is worth the price of admission. But it needs:
- **Accent patterns** (velocity curves over the pattern, not just per-hit)
- **Per-step probability** (chance a hit fires — critical for trap hat patterns)
- **Micro-timing presets** ("laid back snare", "pushed hats") 
- **Variable step resolution** (some instruments at 16th, others at 32nd or 64th)

### What About Sampling? Audio Manipulation?

**This is the elephant-sized 808 in the room.** Hip-hop production IS sampling. I chop breaks, pitch-shift vocals, time-stretch loops, layer an 808 under a live kick, sidechain the bass to the kick. flux-tensor-midi does none of this because it's MIDI-only.

The `audio/dawdreamer_bridge.py` file exists but appears to be a bridge to dawdreamer for rendering. There's no sampler, no waveform display, no sample chopping, no audio effects. For this to be a production tool, it needs:
- Sample loading and mapping (drag a WAV onto a pad)
- Sample editing (start/end points, loop points, reverse, normalize)
- Basic audio processing (pitch shift, time stretch, EQ, compression)
- Sidechain routing (duck the bass when the kick hits)

Without audio, this is a drum programmer and theoretical framework. Not a production environment.

### Dream Feature: What Would Blow My Mind?

**AI-assisted groove matching with real-time visual feedback.**

Imagine this: I play a reference track — say, a Metro Boomin beat. The system analyzes it with `groove-analyzer`, extracts the deadband profile, the microtiming DNA, the swing factor, the velocity curves. Then it generates a *new* beat in the same pocket — same feel, different pattern. Not a copy; a companion piece.

Now show me the deadband funnel in real-time as I play. I tap my pads and the funnel narrows when I'm in the pocket and flashes red when I'm drifting. It's like a groove tuner. I can SEE my timing, quantize it against the reference, and lock in.

Take it further: I have a bass line from `constraint-theory-core` that's mathematically constrained to be consonant. The system detects my chord progression, constrains the bass to chord tones, and suggests passing tones. It's like having a music theory co-pilot that speaks math.

And the kicker: all of this runs as a VST inside my DAW. I don't have to leave Ableton. The tensor engine runs in the background, analyzing my MIDI in real-time, suggesting fills, variations, and arrangement moves based on genre conventions. The `GenreBrain` loads "trap" and knows that verse 2 should strip down the hats, the 808 should glide on the turnaround, and the snare should have a flam on beat 4 of the last bar of the chorus.

That's the dream. The math is here. The theory is here. The API is here. Wrap it in a real-time interface with audio support and visual feedback, and you've got something that could genuinely change how people make beats.

---

## BUGS FOUND

1. **Negative tick MIDI export** (CRITICAL): `StepSequencer._write_midi()` crashes when humanize swing/timing pushes event deltas negative. Reproducible with `humanize(swing=0.5, timing_range=5)` at 90 BPM.

2. **`pocket_pct` display** (MINOR): `groove-analyzer`'s `TrackTiming.pocket_pct` returns values like 10000% (should be 100% or the field is misnamed/miscalculated).

3. **All events on one track** (DESIGN): MIDI export puts everything on one track. Multi-track export needed for DAW mixing workflows.

## SUMMARY SCORECARD

| Task | First-Try? | Steps | Natural? | Notes |
|------|-----------|-------|----------|-------|
| 2a. Trap beat | ✅ | 4 lines | ✅ | Preset + roll = instant trap |
| 2b. Boom-bap + swing | ❌ | 6 lines | ⚠️ | Export bug with humanize |
| 2c. Groove analysis | ✅ | 3 lines | ✅ | Correctly identifies genres |
| 2d. 32-bar arrangement | ⚠️ | 40 lines | ⚠️ | No section/song-mode API |
| 2e. Bass (constraints) | ⚠️ | 50 lines | ❌ | No musical constraint API |
| 2f. Euclidean rhythms | ✅ | 3 lines | ✅ | Best feature, instant polyrhythms |
| 2g. MIDI export | ⚠️ | 1 line | ⚠️ | Works sans humanize; single-track |

**Overall:** The drum programming layer (DrumRack + StepSequencer) is genuinely useful and could be a real tool with a UI. The theoretical foundation (FluxVectors, deadband funnels, Eisenstein snaps) is impressive science but needs a bridge to producer workflow. The constraint solver is cool math that doesn't yet speak music. The groove analyzer is the sleeper hit — genre-accurate microtiming analysis in 3 lines of code.

**Would I use it?** The Euclidean rhythm generator and groove analyzer, yes — tomorrow. The rest needs a UI, audio support, and real-time playback before I'd touch it for actual production.
