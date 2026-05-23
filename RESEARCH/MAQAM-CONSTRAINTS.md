# Maqam Constraints: Arabic/Turkish Microtonal Systems Mapped to Constraint Theory

**Date:** 2026-05-23
**Status:** Research Complete
**Domain:** Ethnomusicology × Constraint Theory × Microtonal Synthesis
**Repos:** [constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core) · [fm-research](https://github.com/SuperInstance/fm-research)

---

## 1. Introduction: Why Maqam Demands Its Own Constraint Topology

The Arabic/Turkish maqam system is a **24-tone quarter-tone system** — distinct from the Indian 22-shruti system, distinct from 12-TET, distinct from any equal temperament that rounds away microtonal inflection. Each maqam (مقام) is not merely a scale but a **melodic framework** with prescribed ascending/descending paths (sayr), modulation destinations (ghammaz), and an emotional trajectory aimed at producing *tarab* (طرب) — a state of joyful rapture, ecstatic absorption, that is the system's explicit aesthetic goal.

This is not a pitch-class set. It is a **constraint manifold** over a 24-tone lattice with:

- **Quarter-tone precision** (50-cent intervals vs. 100-cent semitones)
- **Asymmetric intervallic DNA** unique to each maqam family
- **Processual constraints** (the sayr is a *path*, not a set)
- **Emotional state tracking** (tarab accumulation as a measurable parameter)
- **Rhythmic rigidity constraints** (iqa'at as invariant temporal scaffolds)

Mapping this to the constraint-theory ecosystem (SNAP → FUNNEL → CONSENSUS → LAMAN → TEMPO) reveals that maqam is, in many ways, a **more demanding constraint topology than Western tonality** — because the lattice is denser, the paths are more constrained, and the emotional feedback loop is explicit rather than implicit.

---

## 2. The 24-Tone Quarter-Tone Lattice

### 2.1 Interval Structure

The Arabic/Turkish tone system divides the octave into **24 equal quarter tones** of 50 cents each. The conventional notation uses:

| Symbol | Interval | Cents | Example (from C) |
|--------|----------|-------|-------------------|
| T | Whole tone | 200 | C→D |
| TS | Three-quarter tone | 150 | C→D½♭ |
| S | Semitone | 100 | C→D♭ |
| QS | Quarter tone | 50 | C→D¼♭ |

The quarter-tone is **not a theoretical ornament** — it is a structural pitch. Maqam Sikah begins on a quarter-tone (E half-flat, written Eꜝ or Eƀ). This is not a "bent note" — it is the *tonic*.

### 2.2 SNAP Mapping: Quarter-Tone Lattice Quantization

In constraint-theory terms, the **SNAP** operation quantizes continuous pitch space onto the 24-tone quarter-tone lattice. This is analogous to the A₂ lattice snap for 12-TET, but with twice the resolution:

```
SNAP_24: ℝ → ℤ₂₄

For continuous pitch p (in cents from reference):
  q = round(p / 50) mod 24
  residue = p - (q × 50)
  
  if |residue| ≤ ρ₂₄ → SNAP to quarter-tone q
  else → remain in continuous space (unsnapped, "bending")
```

Where `ρ₂₄` is the **covering radius** for the 24-tone lattice — the maximum allowed deviation before a pitch is no longer "in tune." For quarter-tone maqam, ρ₂₄ ≈ 25 cents (half a quarter tone). This is tighter than 12-TET's ρ₁₂ ≈ 50 cents.

**Critical insight:** The snap boundary is *not* fixed at 25 cents for all maqamat. In practice, maqam-specific intonation creates **variable snap radii** — certain pitches are treated more strictly (tonic, dominant) while others allow wider deviation (passing tones, upper extensions). This is a **context-dependent snap**, where the lattice point's structural role determines the snap tolerance.

### 2.3 The Dodecet and the 24-Tone System

The 12-bit dodecet from the A₂ lattice framework encodes constraint state for 12-TET. For 24-tone maqam, we need to consider whether this extends naturally:

- **Pitch density doubles:** 24 quarter tones vs. 12 semitones → constraint state needs more resolution
- **But the structural alphabet doesn't double:** Maqamat use subsets of 7-9 notes from the 24, not all 24
- **The dodecet's nibble structure still applies:** Constraint state (4 bits), direction (4 bits — now with quarter-tone angular resolution), chirality/safety (4 bits)

A **quarter-tone dodecet** would use the same 12-bit structure but with 24-entry lookup tables. The snap operation becomes denser, but the constraint-state representation remains isomorphic. This is a significant result: the dodecet architecture **scales to 24-tone systems without structural modification** — only the lookup tables change.

---

## 3. The Nine Maqam Families: Intervallic DNA

Each maqam family has a characteristic interval pattern that defines its identity. These are the **genotype constraints** — the irreducible intervallic fingerprint.

### 3.1 The Ten Preset Maqamat

**Maqam Rast** (راست) — *Bright, happy, fundamental*
- Intervals: T - TS - S - T - T - TS - S
- Notes: C - D - Eꜝ - F - G - A - Bꜝ - C
- Tonic: C | Dominant: G | Leading tone: Bꜝ
- Character: The "default" maqam. Bright, resolved, stable. Used as a starting point for teaching and as a modulation home base.
- Sayr: Ascends from tonic to octave, emphasizing the dominant (G). Descends with characteristic Bꜝ→C resolution.
- Constraint signature: The three-quarter tone (Eꜝ) is the identity marker. SNAP must preserve this as a distinct lattice point — it is NOT E♭ and NOT E♮.

**Maqam Bayati** (بياتي) — *Soulful, most commonly used*
- Intervals: TS - T - S - T - T - TS - S
- Notes: D - Eꜝ - F - G - A - B♭ - C - D
- Tonic: D | Dominant: A | Leading tone: C
- Character: The most widely used maqam in Arabic music. Soulful, warm, grounded. Associated with folk and popular traditions.
- Sayr: Emphasizes the D→Eꜝ quarter-tone interval as the emotional core. Ascends through the dominant, with extensive ornamentation around A.
- Constraint signature: The opening TS interval (D→Eꜝ) creates a distinctive "pull" that the FUNNEL constraint must model as asymmetric gravity toward the tonic.

**Maqam Hijaz** (حجاز) — *The "Middle Eastern" sound*
- Intervals: S - TS - T - T - S - T - S (variant readings exist)
- Notes: D - E♭ - F♯ - G - A - B♭ - C - D
- Tonic: D | Dominant: A
- Character: The most internationally recognized "Middle Eastern" sound. The augmented second (E♭→F♯) is its signature. Exotic, dramatic, passionate.
- Sayr: Strong emphasis on the augmented second interval. Melodic phrases oscillate around this interval before ascending.
- Constraint signature: The augmented second (S+TS = 150+200 = 350 cents, or min3-like) creates a **discontinuity in the lattice** — a wider gap that the FUNNEL must bridge. This is the constraint-theory analog of a "potential energy barrier" between E♭ and F♯.

**Maqam Kurd** (كرد) — *Sad, minor-flavored*
- Intervals: S - T - T - S - T - TS - S
- Notes: D - E♭ - F - G - A - B♭ - C - D
- Tonic: D | Dominant: A
- Character: Resembles the Western Phrygian mode or D minor. Sad, introspective, meditative. Popular in Turkish and Kurdish traditions.
- Sayr: Descending emphasis. The minor second (D→E♭) at the start creates immediate melancholic character.
- Constraint signature: Nearly isomorphic to Western minor — the quarter-tone dimension is relatively inactive. This is a "low quarter-tone density" maqam, meaning the SNAP-to-24 constraint is mostly satisfied by standard 12-TET snapping with minor adjustments.

**Maqam Saba** (صبا) — *Sad, complex, unusual*
- Intervals: TS - S - T - S - T - T + S
- Notes: D - Eꜝ - F - G♭ - A - B♭ - C - D
- Tonic: D | Dominant: G♭ (unusual!)
- Character: Complex, ambiguous, deeply sad. The diminished fourth (G♭) as dominant is highly unusual and creates unresolved tension.
- Sayr: Begins with the characteristic D→Eꜝ quarter step, then descends to G♭ before ascending. The G♭ dominant defies expectations.
- Constraint signature: **Anomalous dominant placement.** The FUNNEL constraint normally centers gravity on the fifth degree. Saba's dominant at the diminished fourth (G♭) creates an asymmetric gravity field that pulls melody in unexpected directions. This is a high-entropy maqam — more constraint violations per phrase than most.

**Maqam Nahawand** (نهاوند) — *Western minor-like*
- Intervals: T - S - T - T - S - T - T
- Notes: C - D - E♭ - F - G - A♭ - B - C (ascending)
- Tonic: C | Dominant: G
- Character: Nearly identical to Western harmonic minor. The raised 7th (B♮) creates the characteristic leading tone.
- Sayr: Ascending uses B♮ (harmonic minor feel), descending uses B♭ (natural minor feel). This dual personality is the constraint — **the scale is path-dependent.**
- Constraint signature: Path-dependent pitch selection. The ascending/descending asymmetry means the SNAP operation must be **state-aware** — which direction is the melody moving? This adds a temporal dimension to the lattice quantization.

**Maqam Ajam** (عجم) — *Western major-like*
- Intervals: T - T - S - T - T - T - S
- Notes: B♭ - C - D - E♭ - F - G - A - B♭
- Tonic: B♭ | Dominant: F
- Character: Essentially the Western major scale. "Ajam" means "non-Arabic" — it's the one maqam that sounds familiar to Western ears.
- Sayr: Standard major-scale melodic patterns. The constraint profile is nearly identical to Western tonal music.
- Constraint signature: **Lowest quarter-tone density** of any maqam. The 24-tone lattice is barely utilized. This is the "12-TET island" within the maqam system — a good test case for verifying that constraint theory handles both high-density and low-density microtonal regimes.

**Maqam Sikah** (سيكاه) — *Starting on a quarter tone!*
- Intervals: TS - S - T - T - S - TS - S
- Notes: Eꜝ - F - G - A - B♭ - C - D - Eꜝ
- Tonic: Eꜝ | Dominant: B♭
- Character: The only maqam starting on a quarter tone. Ethereal, floating, unresolved. The quarter-tone tonic means there is no "ground" in 12-TET terms.
- Sayr: The melody orbits around Eꜝ without ever fully resolving to a 12-TET pitch. Extensive ornamentation and bending around the tonic.
- Constraint signature: **The SNAP operation itself is the identity marker.** In 12-TET, this maqam *cannot exist* — its tonic falls exactly between lattice points. The quarter-tone lattice is not an enhancement for Sikah; it is a **necessity**. This maqam is the proof that 24-tone SNAP is qualitatively different from 12-tone SNAP.

**Maqam Nawa Athar** (نوى أثر) — *Exotic, mysterious*
- Intervals: T - S - T - T - S - TS - S
- Notes: C - D - E♭ - F - G - A♭ - Bꜝ - C
- Tonic: C | Dominant: G
- Character: Mysterious, introspective, with a distinctive quarter-tone in the upper tetrachord (Bꜝ). The combination of minor third (E♭) and three-quarter seventh (Bꜝ) creates an exotic, unresolved quality.
- Sayr: Ascends through minor-flavored lower tetrachord, then the Bꜝ creates a characteristic "floating" resolution.
- Constraint signature: **Bimodal quarter-tone deployment** — quarter tones are absent in the lower tetrachord but active in the upper. This creates an asymmetric lattice where the FUNNEL has different snap tolerances in different register regions.

**Maqam Saba Zamzam** (صبا زمزم) — *Very unusual*
- Intervals: S - TS - T - S - T - T + S
- Notes: D - E♭ - Fꜝ - G - A♭ - B♭ - C - D
- Tonic: D | Dominant: A♭
- Character: Extremely unusual, even within the maqam tradition. The combination of minor second opening and three-quarter third creates deep ambiguity.
- Sayr: Extreme emotional range within a single development. Can move from grief to ecstasy within the modal framework.
- Constraint signature: **Maximum lattice anomaly.** Multiple non-standard intervals create a constraint topology that is barely recognizable compared to the other maqamat. The FUNNEL has no single dominant gravity center — it is a multi-well potential.

---

## 4. Constraint Theory Mapping: SNAP → FUNNEL → CONSENSUS → LAMAN → TEMPO

### 4.1 SNAP: Quarter-Tone Lattice Quantization

The primary SNAP operation for maqam uses a 24-tone lattice with 50-cent spacing:

```
SNAP_MAQAM(pitch, maqam_context):
  // pitch in cents from reference tonic
  
  // Step 1: Base 24-tone snap
  q24 = round(pitch / 50) mod 24
  
  // Step 2: Maqam-specific snap adjustment
  // Not all 24 tones are equally valid in a given maqam
  valid_tones = MAQAM_SCALE[maqam_context]
  
  if q24 in valid_tones:
    residue = pitch - (q24 * 50)
    if abs(residue) ≤ maqam_snap_radius(maqam_context, q24):
      return (q24, "SNAPPED")
    else:
      return (q24, "BENDING")  // Intentional pitch bend
  else:
    // Pitch falls between scale degrees
    nearest = find_nearest_valid(q24, valid_tones)
    return (nearest, "PASSING")  // Quick passing tone
```

The **maqam_snap_radius** function is context-dependent:
- **Tonic:** ρ = 15 cents (very tight — the tonic must be precise)
- **Dominant:** ρ = 20 cents (tight — structural pillar)
- **Characteristic tones** (e.g., Eꜝ in Rast): ρ = 18 cents (identity marker)
- **Passing tones:** ρ = 35 cents (looser — transient)
- **Upper extensions:** ρ = 30 cents (moderate — ornamental)

This variable snap radius is a **novel constraint-theory feature** not present in 12-TET mapping, where the snap radius is typically uniform.

### 4.2 FUNNEL: Tonic/Dominant Gravity with Quarter-Tone Precision

The FUNNEL constraint models the gravitational pull of structurally important pitches. In maqam, this is more complex than in Western tonality because:

1. **Quarter-tone gravity:** The dominant and tonic may be at quarter-tone positions, creating gravity wells that don't align with 12-TET
2. **Asymmetric gravity:** The pull toward the tonic is stronger than toward the dominant (unlike Western music where V→I and I→IV are roughly symmetric)
3. **Modulation gravity:** The ghammaz (modulation target) creates a secondary gravity well that activates during development

```
FUNNEL_MAQAM(melody_position, maqam_state):
  
  // Primary gravity: tonic
  tonic_pull = gravity(melody_position, maqam_state.tonic, 
                       strength=1.0, radius=maqam_state.tonic_range)
  
  // Secondary gravity: dominant  
  dominant_pull = gravity(melody_position, maqam_state.dominant,
                          strength=0.7, radius=maqam_state.dominant_range)
  
  // Tertiary gravity: ghammaz (modulation target)
  if maqam_state.in_development:
    ghammaz_pull = gravity(melody_position, maqam_state.ghammaz,
                           strength=0.4, radius=maqam_state.ghammaz_range)
  else:
    ghammaz_pull = 0
  
  // Quarter-tone correction
  quarter_correction = 0
  if on_quarter_tone(melody_position):
    quarter_correction = fine_adjust(melody_position, maqam_state.quarter_tuning)
  
  return tonic_pull + dominant_pull + ghammaz_pull + quarter_correction
```

The FUNNEL's exponential decay model `ε(t) = ε₀ · e^(-λt)` applies directly: as a taqsim (improvisation) progresses, the melody's deviation from structural pitches narrows. The opening phrases explore wide intervallic space; later phrases converge on the tonic in tighter and tighter orbits. This is **maqam development as temporal funnel**.

### 4.3 CONSENSUS: Taqsim Conventions Between Instruments

In a traditional takht (small ensemble), multiple instruments perform taqsim with **implicit consensus constraints**:

| Constraint | Description | Consensus Mechanism |
|-----------|-------------|-------------------|
| Tonic agreement | All instruments agree on the tonic pitch | Lead instrument establishes; others follow |
| Intonation model | Quarter-tone intonation matches between instruments | Ear-based consensus, not visual/measured |
| Modulation timing | Ensemble shifts maqam together | Cues from lead (nod, breath, chord change) |
| Rhythmic freedom | Taqsim is free-meter but ensemble stays together | Breath-based synchronization |
| Ornamentation | Shared vocabulary of turns, trills, glissandi | Cultural convention (not notated) |

The CONSENSUS constraint for maqam is **more permissive** than Western ensemble playing in some ways (free meter, variable intonation) and **more restrictive** in others (shared microtonal vocabulary, mandatory adherence to sayr conventions).

```
CONSENSUS_MAQAM(ensemble_state):
  
  // Each instrument's pitch trajectory
  trajectories = [instrument.pitch_stream for instrument in ensemble]
  
  // Intonation consensus: all within quarter-tone tolerance
  for each pair (traj_a, traj_b):
    if not within_tolerance(traj_a, traj_b, tolerance=15 cents):
      flag("intonation_drift", pair)
  
  // Modulation consensus: all shift maqam together
  current_maqam_votes = [instrument.inferred_maqam for instrument in ensemble]
  if not unanimous(current_maqam_votes):
    flag("modulation_desync", ensemble)
  
  // Sayr consensus: melodic paths follow tradition
  for trajectory in trajectories:
    if not valid_sayr(trajectory, current_maqam):
      flag("sayr_violation", instrument)
```

### 4.4 LAMAN: Iqa' (Rhythmic Pattern) Rigidity

The iqa'at (rhythmic patterns, عزف إيقاع) are the LAMAN constraint — the rigid temporal scaffold that the melodic constraint system is built upon. Unlike Western time signatures, iqa'at are **patterned sequences of strong and weak beats** with specific idiomatic traditions:

| Iqa' | Meter | Pattern (D=strong, T=weak) | Character |
|------|-------|----------------------------|-----------|
| Maqsum | 4/4 | D-T-T-D-T | Most common, balanced |
| Baladi | 4/4 | D-D-T-D-T | Folk, earthy |
| Saiidi | 4/4 | D-T-D-D-T | Upper Egyptian, martial |
| Ayyub | 2/4 | D-T | Religious, processional |
| Malfuf | 2/4 | D-T | Lively, circular |
| Samai Thaqil | 10/8 | D-T-T-D-T-T-D-T-T-T | Classical, stately |
| Dawr Hindi | 7/4 | D-T-T-D-T-T-D | Unusual, complex |

The LAMAN constraint requires |E| = 2n-3 edges for rigidity in a graph of n nodes. Applied to iqa'at:

```
LAMAN_IQA(iqa_pattern):
  
  // Nodes = beat positions in the iqa' cycle
  n = length(iqa_pattern)
  
  // Edges = structural relationships (strong-weak, onset-ghost, etc.)
  E = generate_structural_edges(iqa_pattern)
  
  // Laman check: is this rhythm rigid (stable) or flexible?
  if |E| >= 2*n - 3:
    return "RIGID"  // Strong rhythmic identity
  elif |E| >= 2*n - 4:
    return "MINIMALLY_RIGID"  // Flexible but coherent
  else:
    return "FLOPPY"  // Free-meter territory (taqsim zone)
```

**Key insight:** Taqsim (free-meter improvisation) operates in the **floppy regime** — no iqa' constraint, maximum melodic freedom. Composed/song material operates in the **rigid regime** — fixed iqa'at, melodic constraint from rhythm. The transition between these regimes (taqsim → iqa' → taqsim) is a **Laman phase transition** in constraint space.

### 4.5 TEMPO: Gradual Acceleration Through Maqam Development

Traditional maqam performance follows a **progressive acceleration** pattern:

```
TEMPO_MAQAM(development_stage):
  
  stages = {
    "taqsim":     {"tempo": "free",     "acceleration": 0},       // Free-meter intro
    "muwashshah": {"tempo": "slow",     "acceleration": 0.02},    // Vocal, measured
    "layali":     {"tempo": "moderate", "acceleration": 0.03},    // Vocal improvisation
    "dawr":       {"tempo": "medium",   "acceleration": 0.04},    // Ensemble
    "waslah":     {"tempo": "fast",     "acceleration": 0.05},    // Suite culmination
    "tetra":      {"tempo": "very_fast","acceleration": 0.06}     // Climax
  }
  
  // TEMPO constraint: gradual acceleration as emotional intensity builds
  current_tempo = base_tempo * (1 + sum(acceleration for completed_stages))
```

This maps directly to the TEMPO constraint theory: the metronome accelerates as constraint satisfaction increases (more notes snapped, tighter funnel, stronger consensus). The acceleration is not arbitrary — it follows the emotional arc of the maqam, which is itself a constraint on timing.

---

## 5. Novel Parameters: Quarter-Tone Bends, Tarab, and Modulation Chains

### 5.1 Quarter-Tone Bends: Not Just Up/Down but Micro-Pivots

In Western music, pitch bend is a simple deviation from a lattice point. In maqam, bends are **structured micro-pivots** that serve specific melodic and emotional functions:

- **Gamak (غمزة):** A quick oscillation around a quarter-tone, typically ±15-25 cents, lasting 50-200ms. This is not vibrato — it is a deliberate microtonal ornament that *identifies* the pitch as quarter-tonal.
- **Tahrik (تحريك):** A directional slide toward a target pitch, overshooting by up to a quarter tone and settling. Duration: 100-400ms. This creates a "magnetic" effect — the target pitch pulls the melody.
- **Tashkeel (تشكيل):** A compound ornament combining gamak and tahrik. The pitch oscillates, then slides to a new target. This is the most complex quarter-tone gesture.

**Constraint mapping:**

```
QUARTER_TONE_BEND(current_pitch, target_pitch, bend_type):
  
  match bend_type:
    case "gamak":
      // Oscillate around quarter-tone
      center = SNAP_24(target_pitch)
      amplitude = 20 cents  // Within snap radius
      frequency = 6-8 Hz  // Faster than vibrato
      return oscillate(center, amplitude, frequency)
    
    case "tahrik":
      // Slide to target with overshoot
      overshoot = 40 cents  // Beyond snap radius → dramatic
      slide_rate = exponential_decay(τ=150ms)
      return slide(current_pitch, target_pitch + overshoot, then → target_pitch)
    
    case "tashkeel":
      // Compound: gamak then tahrik
      gamak_phase = QUARTER_TONE_BEND(current_pitch, target_pitch, "gamak")
      tahrik_phase = QUARTER_TONE_BEND(target_pitch, next_target, "tahrik")
      return concatenate(gamak_phase, tahrik_phase)
```

The key constraint-theory insight: **quarter-tone bends operate in the unsnapped region** of the lattice. They are deliberate violations of SNAP that serve expressive purposes. The constraint system must *allow* these violations while tracking them as intentional (not errors). This requires a **bend state vector** that runs parallel to the snap state.

### 5.2 Tarab Accumulation: Tracking Emotional Intensity

Tarab (طرب) is the aesthetic goal of Arabic music — a state of joyful rapture, musical ecstasy, that arises from the interplay of expectation and surprise within the maqam framework. It is not arbitrary emotional arousal; it is **structurally induced** by specific musical events.

**Tarab triggers:**

1. **Modulation to an unexpected maqam** (violates FUNNEL expectation → emotional spike)
2. **Landing on a quarter-tone after a long ascending passage** (SNAP resolution → satisfaction)
3. **Return to the tonic after extended departure** (FUNNEL convergence → resolution)
4. **Repetition with microtonal variation** (same structure, different SNAP → recognition + surprise)
5. **Rhythmic displacement over the iqa'** (LAMAN violation → tension)

**Tarab accumulation model:**

```
TARAB(melody_stream, maqam_state):
  
  tarab_level = 0  // 0.0 to 1.0
  decay_rate = 0.02  // Per event
  
  for event in melody_stream:
    
    // Modulation trigger
    if event.type == "modulation":
      tarab_level += 0.15 * modulation_distance(maqam_state.current, event.new_maqam)
    
    // Quarter-tone resolution trigger
    if event.type == "quarter_tone_arrival":
      tarab_level += 0.1 * (1 - abs(event.snap_residue) / ρ₂₄)
    
    // Tonic return trigger
    if event.pitch == maqam_state.tonic and maqam_state.departure_duration > 4 beats:
      tarab_level += 0.2
    
    // Repetition with variation
    if event.motif_similar_to(previous_motif) and event.snap_residue ≠ previous_snap_residue:
      tarab_level += 0.08
    
    // Decay
    tarab_level *= (1 - decay_rate)
    tarab_level = clamp(tarab_level, 0.0, 1.0)
    
    maqam_state.tarab = tarab_level
  
  return tarab_level
```

Tarab is a **novel parameter for constraint theory** — it is a measurable, structurally-determined emotional state that emerges from the constraint system's own dynamics. It is not an external parameter but an **internal readout** of the constraint satisfaction process.

### 5.3 Modulation Chains: Legal Maqam Transitions

Maqam modulation is not free — it follows **established paths** determined by shared tones, intervallic compatibility, and tradition. These are legal constraint transitions:

| From | To (Primary) | To (Secondary) | Shared Tones |
|------|-------------|----------------|--------------|
| Rast | Hijaz, Nahawand, Bayati | Suznak, Mahour | 4-5 |
| Bayati | Rast, Hijaz, Kurd | Saba, Huseyni | 4-5 |
| Hijaz | Rast, Kurd, Bayati | Hijaz Kar, Zanjaran | 3-4 |
| Kurd | Nahawand, Hijaz, Bayati | Kurdili Hicazkar | 4-5 |
| Saba | Bayati, Hijaz | Saba Zamzam | 3 |
| Nahawand | Rast, Kurd, Hijaz | Farahfaza | 4-5 |
| Ajam | Nahawand, Rast | Ajam Ushayran | 5 |
| Sikah | Rast, Hijaz | Huzam, Iraq | 3-4 |
| Nawa Athar | Rast, Hijaz, Kurd | Nikriz | 3-4 |

**Example chain:** Rast → Hijaz → Kurd → Nahawand → Rast

```
MODULATION_CHAIN(current_maqam, target_maqam):
  
  // Legal modulation check
  if target_maqam in LEGAL_MODULATIONS[current_maqam]:
    
    // Find pivot tones (shared between source and target)
    pivot_tones = intersection(
      MAQAM_SCALE[current_maqam], 
      MAQAM_SCALE[target_maqam]
    )
    
    // Modulation via pivot: melody lands on shared tone,
    // then reorients around target maqam's structure
    return {
      "legal": true,
      "pivot_tones": pivot_tones,
      "tarab_boost": 0.15 * (1 - len(pivot_tones) / 7),
      // Fewer shared tones = more surprise = more tarab
    }
  else:
    return {
      "legal": false,
      "alternative_path": find_indirect_modulation(current_maqam, target_maqam)
    }
```

**Constraint-theory mapping:** Modulation chains are **state transitions in the constraint graph**. Each transition has:
- **Cost:** Inversely proportional to shared tones (fewer shared = more cognitive load)
- **Tarab reward:** Proportional to surprise (inversely proportional to expectation)
- **Reversibility:** Most modulations are reversible, but the return path may differ

This creates a **weighted directed graph** of maqam transitions, where edge weights encode the tarab potential of each modulation. The graph is not fully connected — some transitions are forbidden (e.g., Saba → Ajam is rare and awkward).

### 5.4 Oud-Specific Techniques: Risha Angle → Timbre → Constraint on Attack Character

The oud (عود) is the primary instrument of the maqam tradition. Its playing technique introduces **physical constraints** that directly affect the constraint topology:

| Technique | Risha Angle | Timbral Effect | Constraint Implication |
|-----------|------------|----------------|----------------------|
| Rest stroke | 90° (perpendicular) | Full, warm, sustained | Max snap precision — note is clear |
| Free stroke | 45° | Lighter, shorter | Moderate snap — less sustain for pitch clarity |
| Tremolo | 30°, rapid alternating | Shimmering, sustained | Snap maintained by repetition |
| Harmonics | Light touch, 12th fret | Bell-like, pure | Different snap target (natural harmonic series) |
| Glissando | Continuous angle change | Sliding, fluid | Deliberate unsnapped region |

```
OUD_ATTACK(risha_angle, string, fret_position):
  
  // Risha angle determines attack character
  angle_radians = risha_angle * π / 180
  
  // Snap precision is a function of attack clarity
  snap_precision = sin(angle_radians)  // 90° = max precision
  
  // Sustain determines how long the snap holds
  sustain = exponential_decay(τ=300ms * snap_precision)
  
  // Quarter-tone feasibility: 
  // Quarter tones are only stable with rest stroke or tremolo
  if fret_position.is_quarter_tone:
    if risha_angle < 60°:
      warn("quarter_tone_unstable")  // Will decay to nearest semitone
    else:
      // Rest stroke stabilizes the quarter tone
      snap_precision *= 1.2  // Bonus: rest stroke on quarter tone is idiomatic
  
  return {
    "snap_precision": snap_precision,
    "sustain": sustain,
    "quarter_tone_stable": risha_angle >= 60°
  }
```

**Key insight:** The physical instrument **constrains the constraint system.** A quarter-tone that is perfectly valid in the abstract 24-tone lattice may be physically unstable on the oud unless the risha angle provides sufficient attack energy. This is a **physics-constraint intersection** — the musical constraints and the physical constraints must be satisfied simultaneously.

---

## 6. The Complete Constraint Topology

### 6.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MAQAM CONSTRAINT SYSTEM                       │
│                                                                 │
│  ┌──────────────┐                                               │
│  │ 24-TONE      │ ← SNAP: Quarter-tone lattice quantization     │
│  │ LATTICE      │    Variable snap radius per structural role   │
│  │ (50¢ grid)   │    Dodecet-scaled to 24 entries               │
│  └──────┬───────┘                                               │
│         │                                                       │
│  ┌──────▼───────┐                                               │
│  │ MAQAM SCALE  │ ← FUNNEL: Tonic/dominant/ghammaz gravity     │
│  │ FILTER       │    Quarter-tone precision gravitational wells  │
│  │ (7-9 tones)  │    Development-stage-dependent narrowing      │
│  └──────┬───────┘                                               │
│         │                                                       │
│  ┌──────▼───────┐                                               │
│  │ ENSEMBLE     │ ← CONSENSUS: Takht taqsim conventions         │
│  │ CONSENSUS    │    Intonation matching (15¢ tolerance)         │
│  │              │    Modulation synchronization                  │
│  └──────┬───────┘                                               │
│         │                                                       │
│  ┌──────▼───────┐                                               │
│  │ IQA' RHYTHM  │ ← LAMAN: Rhythmic pattern rigidity            │
│  │ SCAFFOLD     │    Free-meter (floppy) ↔ fixed (rigid)         │
│  │              │    Laman phase transition at taqsim boundary   │
│  └──────┬───────┘                                               │
│         │                                                       │
│  ┌──────▼───────┐                                               │
│  │ TEMPO ARC    │ ← TEMPO: Gradual acceleration                 │
│  │              │    Development-stage-driven                    │
│  │              │    Tarab-correlated with acceleration          │
│  └──────┬───────┘                                               │
│         │                                                       │
│  ┌──────▼───────┐                                               │
│  │ TARAB STATE  │ ← EMERGENT READOUT                            │
│  │ (0.0 - 1.0)  │    Structurally induced emotional intensity   │
│  │              │    Feeds back into tempo and funnel width      │
│  └──────────────┘                                               │
│                                                                 │
│  ┌──────────────┐                                               │
│  │ OUD PHYSICS  │ ← INSTRUMENT CONSTRAINT                       │
│  │ (risha, etc.)│    Attack character → snap precision           │
│  │              │    Quarter-tone stability depends on technique │
│  └──────────────┘                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Feedback Loops

The maqam constraint system has three critical feedback loops that distinguish it from simpler constraint topologies:

1. **Tarab → Tempo:** As tarab accumulates, the tempo naturally accelerates (performer response to emotional intensity). This is captured by the TEMPO constraint receiving input from the TARAB state.

2. **Tarab → Funnel Width:** Higher tarab correlates with wider funnel tolerance — the performer takes more risks, explores more distant modulations, allows more pitch bending. The FUNNEL's ε₀ parameter is tarab-dependent.

3. **Ensemble → Tarab:** When the ensemble achieves high consensus (tight intonation, synchronized modulations), this *itself* generates tarab — the experience of "locking in" with other musicians. CONSENSUS satisfaction feeds TARAB accumulation.

These feedback loops make the maqam constraint system **dynamically coupled** — changes in one constraint propagate to others through the tarab state variable. This is more complex than Western tonal constraint systems, where the constraints are largely independent.

---

## 7. Implementation: Ten Maqam Presets

### 7.1 Preset Structure

Each preset encodes the full constraint topology for one maqam:

```
MAQAM_PRESET = {
  name: string,
  tonic: int,           // Quarter-tone index (0-23)
  dominant: int,        // Quarter-tone index (0-23)
  ghammaz: [int],       // Array of valid modulation targets
  scale: [int],         // Array of quarter-tone indices in ascending order
  sayr_ascend: [int],   // Preferred ascending path (may differ from scale)
  sayr_descend: [int],  // Preferred descending path
  snap_radii: {int: float},  // Per-degree snap tolerance in cents
  iqa_default: string,  // Default rhythmic pattern
  tempo_range: (float, float),  // Min/max BPM
  tarab_triggers: [string],  // Maqam-specific tarab events
  oud_techniques: [string],  // Preferred oud techniques
}
```

### 7.2 The Ten Presets (Summary Table)

| # | Maqam | Tonic | Dominant | Quarter-Tone Count | Tarab Potential | Difficulty |
|---|-------|-------|----------|-------------------|----------------|------------|
| 1 | Rast | C | G | 2 (Eꜝ, Bꜝ) | Medium | Low |
| 2 | Bayati | D | A | 1 (Eꜝ) | Medium-High | Low-Medium |
| 3 | Hijaz | D | A | 0 (aug2 is structural) | High | Medium |
| 4 | Kurd | D | A | 0 | Medium-Low | Low |
| 5 | Saba | D | G♭ | 1 (Eꜝ) | Very High | High |
| 6 | Nahawand | C | G | 0 (path-dependent) | Medium | Low |
| 7 | Ajam | B♭ | F | 0 | Low | Very Low |
| 8 | Sikah | Eꜝ | B♭ | 1 (tonic!) | Very High | Very High |
| 9 | Nawa Athar | C | G | 1 (Bꜝ) | High | Medium-High |
| 10 | Saba Zamzam | D | A♭ | 1 (Fꜝ) | Extreme | Extreme |

---

## 8. Theoretical Implications

### 8.1 Maqam Proves Constraint Theory Scales Beyond 12-TET

The existence of a coherent, centuries-old musical system operating on a 24-tone lattice with path-dependent constraints, emotional feedback loops, and physical instrument coupling demonstrates that constraint theory is not an artifact of 12-tone equal temperament. It is a **universal framework** for understanding how musical systems constrain pitch, time, and ensemble behavior into coherent aesthetic experiences.

### 8.2 Quarter-Tone Constraints Are Qualitatively Different

The SNAP operation on a 24-tone lattice is not simply "12-TET with more points." It introduces:

- **New pitch categories** that have no 12-TET analog (quarter tones as structural, not ornamental)
- **Variable snap radii** that depend on the pitch's structural role
- **Deliberate unsnapped regions** (bends) that are part of the system, not violations
- **Instrument-dependent snap stability** (oud risha angle affects quarter-tone viability)

### 8.3 Tarab as a Constraint-Theoretic Observable

Tarab is the most significant theoretical contribution of the maqam system to constraint theory. It demonstrates that:

- **Emotional states can be structurally determined** — tarab arises from specific constraint configurations, not arbitrary subjective response
- **Feedback loops couple constraints dynamically** — the constraint system is not static but self-modifying through the tarab variable
- **The aesthetic goal is explicit and measurable** — unlike Western music's implicit beauty criterion, tarab provides a concrete target for optimization

---

## 9. Open Questions

1. **Can the tarab model be validated empirically?** Physiological measurements (heart rate, skin conductance, EEG) during maqam performances could calibrate the tarab accumulation parameters.

2. **What is the minimum quarter-tone resolution for maqam perception?** Are all 50-cent intervals truly perceptually equal, or do some maqamat require finer resolution (e.g., the "neutral third" in Rast varies by region)?

3. **How does the constraint topology change across Arabic vs. Turkish vs. Persian traditions?** The same maqam names refer to different interval structures in different traditions — this is a **dialect of the constraint language.**

4. **Can modulation chains be formalized as a category?** The legal transition graph has compositional structure (A→B→C is a valid chain iff A→B and B→C are legal). This suggests a categorical structure with maqamat as objects and modulations as morphisms.

5. **What is the constraint-theoretic explanation for why some maqamat are "heavier" than others?** Saba and Sikah are considered more demanding, more emotionally intense — is this because they have higher constraint entropy, or because their constraint topologies are more complex?

---

## 10. References and Further Reading

- Marcus, Scott L. *Music in Egypt: Experiencing Music, Expressing Culture*. Oxford University Press, 2007.
- Touma, Habib Hassan. *The Music of the Arabs*. Amadeus Press, 1996.
- Zadeh, L.A. "Fuzzy Sets as a Basis for a Theory of Possibility." *Fuzzy Sets and Systems*, 1978. (For the variable snap radius model.)
- Maqam World: [maqamworld.com](http://maqamworld.com) — Reference for scale structures and modulation patterns.
- Farhat, Hormoz. *The Dastgah Concept in Persian Music*. Cambridge University Press, 1990. (Persian parallel system.)
- Signell, Karl L. *Makam: Modal Practice in Turkish Art Music*. Asian Music Publications, 1977.

---

*Research by the SuperInstance constraint theory project. The maqam system is a living tradition — this mapping is an analytical tool, not a replacement for the embodied knowledge of master musicians (ustaz, أستاذ) who carry these constraints in their hands and ears.*
