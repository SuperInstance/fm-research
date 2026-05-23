# East Asian Musical Traditions Mapped to Constraint Theory

**Date:** 2026-05-23
**Status:** Research Complete
**Domain:** Ethnomusicology × Constraint Theory × Pentatonic Systems × Temporal Philosophy
**Repos:** [constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core) · [fm-research](https://github.com/SuperInstance/fm-research)

---

## 1. Introduction: Silence, Breath, and the Pentatonic Lattice

East Asian musical traditions present a fundamentally different constraint topology from Western tonal systems, Arabic maqam, or Indian raga. Where Western music fills time with event density and Indian raga fills it with melodic micro-inflection, East Asian traditions — particularly Japanese, Chinese, Korean, and Vietnamese — make **silence itself a structural parameter** and treat **breath as a hard constraint** on phrase duration.

The key insight: these systems are not primarily pitch-constraint systems. They are **temporal-constraint systems** where pitch operates on a reduced lattice (typically pentatonic, 5 positions) while the real complexity lives in:

- **Ma (間)** — silence as an orchestrated, notated, required structural element (Japan)
- **Breath capacity** — one inhalation = one phrase, hard physiological limit (shakuhachi)
- **Acceleration curves** — tempo as a shaped trajectory, not a fixed grid (jo-ha-kyu, sanjo)
- **Meditative zero-crossing** — tempo approaching zero as a spiritual/structural goal (guqin)
- **Bridge retuning mid-performance** — the physical instrument state changes during play (đàn tranh)

Mapping these to the constraint-theory framework (SNAP → FUNNEL → CONSENSUS → LAMAN → TEMPO) reveals that East Asian music operates in a **lower-dimensional pitch space but a higher-dimensional temporal space** than Western or Middle Eastern systems. The pentatonic lattice is trivially simple (5 nodes). The temporal constraints are not.

This document covers four traditions — Japanese, Chinese, Korean, and Vietnamese — derives constraint mappings for each, proposes novel parameters (ma budget, breath capacity, acceleration curve, bridge retuning), and defines 10 performance presets.

---

## 2. Japanese Traditions

### 2.1 The Japanese Pentatonic System: In, Yo, Ritsu, Miyako-bushi

Japanese traditional music employs four primary pentatonic scales, each a subset of a 12-semitone chromatic space but constrained to exactly five pitch classes:

**In Scale (陰)** — *Dark, feminine, melancholic*
- Structure: 1 - 2 - 3 - 1 - 3 (semitone intervals within octave)
- Notes: C - D♭ - E♭ - G - A♭ - C
- Character: Minor-quality, associated with court music, gagaku slow sections
- Interval vector: minor 2nd, minor 3rd, major 3rd, minor 2nd, major 3rd

**Yo Scale (陽)** — *Bright, masculine, celebratory*
- Structure: 2 - 3 - 2 - 2 - 1
- Notes: C - D - E - G - A - C
- Character: Major-quality, folk songs, festival music, children's songs
- Interval vector: major 2nd, major 3rd, major 2nd, major 2nd, minor 2nd

**Ritsu Scale (律)** — *Ceremonial, Buddhist*
- Structure: 2 - 3 - 1 - 2 - 2 (with variants)
- Notes: C - D - F - G - A - C (one common form)
- Character: Used in gagaku, Buddhist chant, ancient court music
- Related to Chinese zhengdíao pentatonic via shared historical origin

**Miyako-bushi Scale (都節)** — *The "Tokyo" scale, most distinctly Japanese*
- Structure: 1 - 4 - 2 - 3 - 2
- Notes: C - D♭ - F - G - A♭ - C
- Character: The iconic "Japanese sound" — heard in koto music, shamisen, geisha music
- The augmented second (4 semitones, D♭→F) creates the distinctive angular quality

**SNAP Mapping:** All four scales map to the same **pentatonic lattice** — a 5-position subset of the 12-semitone chromatic space:

```
SNAP_5: ℝ → P₅ ⊂ ℤ₁₂

For each Japanese scale S = {s₁, s₂, s₃, s₄, s₅} ⊂ ℤ₁₂:
  For continuous pitch p (in semitones from tonic):
    q = argmin_{sᵢ ∈ S} |p - sᵢ|
    
    if |p - sᵢ| ≤ ρ₅ → SNAP to nearest scale degree
    else → remain in continuous space (ornamental, not structural)
```

Where ρ₅ ≈ 1 semitone (generous snap radius for pentatonic, since scale degrees are 1-4 semitones apart). The **critical observation**: the pentatonic lattice has very few nodes, so the snap is extremely forgiving — almost any pitch maps to a valid scale degree. This is why East Asian music can accommodate wide pitch inflection without "losing tonality." The constraint is not "stay on the lattice" (that's easy) but "shape the time correctly."

**Lattice topology:** The pentatonic lattice is a 5-node cycle graph C₅. Unlike the 12-node chromatic circle or the 24-node quarter-tone circle, C₅ has:
- Diameter = 2 (maximum 2 steps between any two nodes)
- Only 5 possible interval classes
- Trivial voice-leading (any scale degree connects to any other in ≤ 2 steps)

This makes the pitch constraint space **almost trivially navigable**. The musical complexity must live elsewhere.

### 2.2 Ma (間): Silence as a Structural Constraint

Ma is arguably the single most important concept in Japanese aesthetics, and it is fundamentally a **constraint** — not the absence of sound, but the **presence of structured silence**.

**Definition:** Ma (間) = the temporal/spatial interval between events, imbued with tension, expectation, and meaning. It is not "rest" (Western notation) or "space" (passive absence). It is an **active structural element** — the silence between two sounds is as composed, as intentional, and as emotionally significant as the sounds themselves.

**In Western terms:** Ma is a rest with an emotional load. But this analogy fails because Western rests are defined by duration only, while ma is defined by duration + context + expectation + resolution state.

**Constraint-theory mapping — the Ma Budget:**

```
MA_BUDGET: {silence_duration, context, tension_state} → ℤ₊

For a phrase P with events e₁, e₂, ..., eₙ:
  ma_i = temporal gap between eᵢ and eᵢ₊₁
  
  MA_TOTAL = Σ ma_i (total silence budget for phrase)
  MA_DENSITY = MA_TOTAL / DURATION(P) (fraction of phrase that is silence)
  MA_TENSION(t) = ∫₀ᵗ f(expectation, resolution_state) dt
  
  Constraints:
    MA_DENSITY ≥ θ_ma (minimum silence fraction; genre-dependent)
    MA_TENSION must resolve before phrase end (silence creates debt that must be paid)
    Each ma_i ≥ μ_ma (minimum silence duration; prevents "filling" the space)
```

**Genre-specific thresholds:**

| Genre | θ_ma (min silence %) | μ_ma (min gap) | Notes |
|-------|---------------------|-----------------|-------|
| Zen meditation | 70-90% | 2-5 sec | Sound is rare; silence is default |
| Tea ceremony | 40-60% | 1-3 sec | Measured, contemplative |
| Gagaku (slow) | 30-50% | 0.5-2 sec | Stately, ceremonial |
| Shakuhachi honkyoku | 50-70% | 1-4 sec | Breathing silences |
| Koto contemporary | 15-30% | 0.3-1 sec | More active texture |

**The key constraint:** Ma is not optional. You cannot "skip" ma any more than you can skip a note in a melody. The silence *is* the music. In constraint-theory terms, ma introduces a **minimum silence constraint** on every phrase — a hard lower bound on the temporal gap between events. This is the inverse of Western music's **minimum note density** constraint.

### 2.3 Jo-ha-kyu (序破急): Acceleration as Form

Jo-ha-kyu is the fundamental formal principle of Japanese arts — not just music but also Noh theater, tea ceremony, martial arts, and poetry. It describes a **three-phase acceleration curve**:

- **Jo (序) — Introduction:** Slow, restrained, establishing. Tempo is at minimum. Material is presented simply.
- **Ha (破) — Development:** Accelerating, elaborating, complexifying. Tempo increases. Material fragments and recombines.
- **Kyu (急) — Rush/climax:** Maximum tempo, maximum density, maximum tension. Then: abrupt resolution.

**This is not a tempo map. It is an acceleration map.** The constraint is not "play at tempo X in section Y" but "accelerate at rate A through section B." The derivative of tempo with respect to time is the controlled parameter, not tempo itself.

**Constraint-theory mapping — the JHK Acceleration Curve:**

```
JHK: TEMPO(t) → ℝ₊

For total form duration T:
  t_jo = [0, T/3)     (Jo phase)
  t_ha = [T/3, 2T/3)  (Ha phase)  
  t_kyu = [2T/3, T]   (Kyu phase)

  TEMPO(t) = TEMPO₀ × f(t/T)

  where f(x) is a monotonically increasing function on [0, 1]:
    f(0) = 1.0    (normalized start)
    f(1) = α_jhk  (acceleration factor, typically 2.0-4.0)
    
    f'(x) > 0 for all x      (strictly accelerating)
    f''(x) ≥ 0 for all x     (acceleration is itself accelerating)

  Constraint: dTEMPO/dt > 0 everywhere (no deceleration within form)
  Exception: final cadence may decelerate (kyu → resolution)
```

The acceleration factor α_jhk is genre-dependent:
- **Noh drama:** α_jhk ≈ 2.0 (moderate acceleration over 30-60 minutes)
- **Gagaku:** α_jhk ≈ 1.5 (gentle, nearly imperceptible acceleration)
- **Sanjo (Korean, related concept):** α_jhk ≈ 3.0-5.0 (dramatic acceleration)
- **Tea ceremony:** α_jhk ≈ 1.2 (barely perceptible — the constraint is present but subtle)

**SNAP→JHK interaction:** The pentatonic lattice snap operates independently of the JHK tempo curve. However, as tempo increases, the **effective snap radius** must widen — at faster tempos, pitch precision becomes less important and temporal precision becomes more important. This creates a natural **constraint transfer**: pitch constraint relaxes as temporal constraint tightens.

### 2.4 Shakuhachi: The One-Breath Constraint

The shakuhachi (尺八) is a bamboo end-blown flute with 5 finger holes, producing the Japanese pentatonic scales. Its most fundamental constraint is **physiological**: a single phrase is bounded by one breath.

**The one-breath constraint:**

```
BREATH: {lung_capacity, air_pressure, pitch, dynamics} → Duration

For a phrase P beginning at breath b:
  DURATION(P) ≤ CAPACITY(b) / FLOW_RATE(pitch, dynamics)
  
  where:
    CAPACITY(b) = lung volume available at start of breath (typically 2-4 liters)
    FLOW_RATE = function of pitch (higher → faster air flow) and dynamics (louder → faster)
    
  Constraints:
    P must complete before breath exhaustion (hard physiological limit)
    DYNAMICS must taper as breath depletes (natural decay → aesthetic feature)
    Final note of phrase must resolve (no unresolved phrases — breath as deadline)
```

This is a **resource constraint** — analogous to fuel in a rocket or memory in a computer. The shakuhachi player must budget their breath across the entire phrase, allocating more air to important notes and less to passing tones. The constraint shapes phrasing, dynamics, and even pitch choice (high notes cost more air).

**Ma × Breath interaction:** The silences between phrases are literally the time taken to inhale. Ma in shakuhachi music is not arbitrary — it is bounded below by the time needed to refill the lungs. This creates a beautiful self-regulating system:

```
ma_i ≥ INHALE_TIME(prev_exhalation_volume)
```

Long phrases (more air exhaled) require longer silences (more time to inhale). This is not a composed constraint — it is a physiological one that the music has evolved to accommodate and exploit.

### 2.5 Koto: The 13-String Lattice

The koto (箏) is a 13-string zither with movable bridges. Its constraint topology is:

- **13 parallel strings**, each tuned to a pentatonic scale degree
- **Movable bridges (ji)** allow retuning between (not during) pieces
- Standard tuning: pentatonic (e.g., D - G - A - B♭ - D for hirajoshi)
- **Pitch range:** ~2 octaves of immediately accessible pitches (one per string)
- **Bending:** Strings can be pulled to raise pitch by up to 2-3 semitones on the player's side of the bridge

**Lattice structure:**

```
KOTO_LATTICE: 13 strings × {open, bent_up} → 13-26 pitch positions

For string s with bridge position b(s):
  open_pitch(s) = f(string_number, tuning, bridge_position)
  bent_pitch(s) = open_pitch(s) + β(s)  where 0 ≤ β(s) ≤ β_max
  
  β_max ≈ 2-3 semitones (player-side string tension)
```

The koto's lattice is **linear** (one dimension: string number) rather than circular (pitch class). This means:
- Adjacent strings are typically scale-adjacent (small intervals)
- Large leaps require skipping strings (physically larger hand movements)
- The constraint is not "which pitch" but "which string" — the physical topology matters

**Bridge retuning as a constraint operation:** Between pieces, bridges are physically moved to retune the koto. This is a **lattice reconfiguration** — the same instrument maps to a different subset of pitch space. In constraint-theory terms:

```
RETUNE: {scale, mode, key} → bridge_positions

RECONFIGURE_LATTICE(koto, old_scale, new_scale):
  for each string s:
    move_bridge(s, new_position(s, new_scale))
  
  constraint: new lattice must be pentatonic (5 positions × 2+ octaves)
  constraint: string tension must remain in playable range
```

---

## 3. Chinese Traditions

### 3.1 Wu Xing (五行) Pentatonic: The Five-Phase Scale

Chinese traditional music is built on a **five-note pentatonic scale** derived from the Wu Xing (五行, Five Elements/Phases) cosmological system. The five scale degrees correspond to the five elements:

| Scale Degree | Chinese | Element | Direction | Season | Emotion |
|-------------|---------|---------|-----------|--------|---------|
| Gong (宫) | 宫 | Earth | Center | Late Summer | Trust/Worry |
| Shang (商) | 商 | Metal | West | Autumn | Grief/Courage |
| Jue (角) | 角 | Wood | East | Spring | Anger/Kindness |
| Zhi (徵) | 徵 | Fire | South | Summer | Joy/Hate |
| Yu (羽) | 羽 | Water | North | Winter | Fear/Wisdom |

The interval structure (from gong): **M2 - M2 - m3 - M2 - m3** (e.g., C - D - E - G - A - C). This is the same as the Japanese Yo scale — a major pentatonic — reflecting shared historical origins (the gagaku system was imported from Tang dynasty China).

**SNAP Mapping — Wu Xing Lattice:**

The Wu Xing pentatonic is a 5-node lattice, but with **cosmological constraints** on modulation and progression:

```
SNAP_WUXING: ℝ → {GONG, SHANG, JUE, ZHI, YU}

Additional constraint: the sheng (generating) cycle and ke (overcoming) cycle
  Sheng cycle: Wood→Fire→Earth→Metal→Water→Wood (generating sequence)
  Ke cycle:    Wood→Earth→Water→Fire→Metal→Wood (controlling sequence)

  Modulation preference:
    sheng cycle modulations preferred (constrained → next in generation)
    ke cycle modulations possible but create tension (crossing the cycle)
```

This is a **constrained walk on a graph** — not just any pentatonic traversal but one that follows (or deliberately violates) the five-phase generation cycle. The graph has two overlay structures (sheng and ke cycles), creating a **directed constraint topology** on the otherwise symmetric pentatonic lattice.

### 3.2 Guqin: 7 Strings × 13 Hui = 91 Pitch Positions

The guqin (古琴) is a 7-string fretless zither with 13 inlaid markers (hui, 徽) indicating harmonic nodes. It is the most ancient Chinese instrument still in active use (~3000 years), and its constraint topology is remarkably sophisticated:

**The 91-position lattice:**

```
GUQIN: 7 strings × 13 hui = 91 primary pitch positions

For string s (1-7, low to high) and hui h (1-13, from bridge toward nut):
  pitch(s, h) = fundamental(s) × (hui_ratio(h))
  
  hui ratios (harmonics): 1/1, 1/2, 2/3, 3/4, 4/5, 3/5, 2/5, 1/3, ...
  
  91 positions = open strings (7) + stopped positions (7×12 = 84)
  + intermediate positions between hui (unmarked, by ear)
  + harmonics at hui positions (same pitch, different timbre)
```

**This is not a 91-note chromatic set.** Many positions duplicate pitches. The 91 positions map to roughly 3 octaves of pentatonic space with significant overlap. But the **timbral variation** across positions is enormous — the same pitch played at different hui on different strings has a completely different tone color.

**Constraint: stopped vs. open vs. harmonic:**

```
GUQIN_PITCH: {string, hui, technique} → {pitch, timbre}

  open_string(s):     fundamental(s), full resonance, sustained
  stopped(s, h):      fundamental(s) × position(h), damped, variable sustain
  harmonic(s, h):     overtone at hui(h), bell-like, decays quickly
  
  constraint: stopped notes require left-hand pressure (physical effort)
  constraint: harmonics only available at hui positions (quantized)
  constraint: open strings ring sympathetically (uncontrolled resonance)
```

### 3.3 Guqin Meditation: Tempo Approaching Zero

The guqin is intimately associated with **meditation and self-cultivation** (修心). In traditional practice, the ideal playing state approaches **timelessness** — tempo slows toward zero, each note becomes an event unto itself, and the music dissolves into individual tones separated by expanding silences.

**The anti-tempo constraint:**

```
ANTI_TEMPO: TEMPO(t) → 0⁺

For meditation-mode guqin performance:
  TEMPO(t) = TEMPO₀ × e^(-λt)  where λ > 0 (exponential deceleration)
  
  As t → ∞: TEMPO → 0
  Each successive note is longer than the previous
  
  Constraint: TEMPO must always be > 0 (performance never stops, only slows)
  Constraint: ma between notes grows proportionally to note duration
  Constraint: breath of player synchronizes with note onset (optional but common)
```

This is the **inverse of jo-ha-kyu** — instead of accelerating, the performance decelerates toward stasis. In constraint-theory terms, it is a **temporal convergence to zero** — the TEMPO parameter asymptotically approaches its minimum value, creating an experience of suspended time.

**TEMPO parameter space for guqin:**

| Mode | TEMPO range | Note duration | Ma fraction |
|------|-------------|---------------|-------------|
| Active/programmatic | 40-80 BPM | 0.75-1.5 sec | 20-30% |
| Lyrical | 20-40 BPM | 1.5-3 sec | 30-50% |
| Meditative | 5-20 BPM | 3-12 sec | 50-70% |
| Deep meditation | 1-5 BPM | 12-60 sec | 70-90% |

At the deep meditation extreme, a single piece may last 20-30 minutes with only 20-30 actual notes. The ma (silence) between notes becomes the dominant experience — each note is a stone dropped into still water, and the silence between them is the ripple spreading outward.

---

## 4. Korean Traditions

### 4.1 Pansori: Narrative Constraint

Pansori (판소리) is a Korean tradition of **solo vocal narrative** accompanied by a single drummer (gosu). It is opera-scale storytelling — a single pansori piece (madang) can last 2-8 hours, performed by one singer. The constraints are:

**Vocal range:** The pansori singer (sorikkun) must cover an enormous range — from chest voice growls to falsetto shrieks, often spanning 3+ octaves. The voice is the sole melodic instrument.

**Narrative constraint:** The singer must tell a complete story with multiple characters, each with distinct vocal characterization. This is a **semantic constraint** — pitch choices are driven by dramatic requirements, not abstract melodic logic.

```
PANSORI: {character, emotion, dramatic_state} → {pitch_range, timbre, dynamics}

  For character c at dramatic moment d:
    vocal_register(c) ∈ {chest, mixed, falsetto, growl}
    pitch_center(c) = f(character_age, gender, social_status)
    dynamics(d) = f(emotional_intensity, narrative_position)
    
    Constraint: character differentiation must be perceptible (min timbral distance)
    Constraint: emotional trajectory must follow narrative arc (no arbitrary changes)
    Constraint: single breath phrases (similar to shakuhachi constraint)
```

**The drum as temporal constraint:** The buk (북, barrel drum) provides the only accompaniment. The drummer does not follow the singer — the relationship is dialogic. The drum pattern (jangdan) sets up a **rhythmic constraint lattice** that the singer navigates, aligns with, or deliberately disrupts for dramatic effect.

### 4.2 Sanjo: Acceleration as Genre

Sanjo (산조, "scattered melodies") is a Korean instrumental solo genre — and it is the purest musical expression of **acceleration as structural principle**. A sanjo performance:

1. Begins at an extremely slow tempo (najiummachi, 느진마치)
2. Progresses through 4-8 sections, each progressively faster
3. Ends at maximum speed (jajinmachi, 자진마치)

The acceleration is **not gradual** — it occurs in discrete jumps between sections, each section establishing a new tempo plateau. This is step-wise acceleration rather than continuous acceleration (cf. jo-ha-kyu, which is more continuous).

**Sanjo tempo structure:**

```
SANJO: sections S₁, S₂, ..., Sₙ where n ∈ {4, 5, 6, 7, 8}

  TEMPO(S₁) = T₁ ≈ 10-20 BPM (extremely slow)
  TEMPO(Sₖ) = T₁ × α^(k-1)  where α ≈ 1.5-2.0
  
  TEMPO(Sₙ) ≈ T₁ × α^(n-1) ≈ 100-200 BPM
  
  Constraint: TEMPO(Sₖ) < TEMPO(Sₖ₊₁) for all k (strictly increasing)
  Constraint: each section establishes its tempo plateau before accelerating
  Constraint: rhythmic pattern (jangdan) is constant within section
```

**Jangdan (장단) — rhythmic cycle constraint:**

Each sanjo section is built on a specific jangdan (rhythmic cycle):

| Jangdan | Beats/cycle | Section position | Relative tempo |
|---------|-------------|------------------|----------------|
| Jinnyang | 24 | Opening (slowest) | 1× |
| Jungmori | 12 | Early-middle | 2× |
| Jungjungmori | 4 | Middle | 4× |
| Jajinmori | 4 | Late | 6-8× |
| Hwimori | 4 | Closing (fastest) | 10-12× |

The jangdan shrinks from 24 beats to 4 beats while the tempo increases — a **double compression** (fewer beats per cycle × faster tempo per beat). The musical density increases exponentially through the piece.

**SNAP × SANJO interaction:** Sanjo instruments (gayageum, geomungo, daegeum, piri, ajaeng) use pentatonic or near-pentatonic tuning. As tempo increases:
- Pitch precision decreases (fast passages allow less bending/tuning)
- Rhythmic precision increases (alignment with jangdan becomes critical)
- Ornamentation simplifies (no time for slow glissandi at fast tempos)

This is the same **constraint transfer** observed in jo-ha-kyu: pitch constraints relax as temporal constraints tighten.

---

## 5. Vietnamese Traditions

### 5.1 Đàn Tranh: Pentatonic with Quarter-Tone Bends

The đàn tranh is a 16-string zither, closely related to the Chinese guzheng and Japanese koto. Its distinguishing feature is the **extensive use of pitch bending** — strings are pressed, pulled, and vibrato-ed to produce quarter-tone and finer pitch inflections within a pentatonic framework.

**Tuning:** Standard tuning is pentatonic (e.g., C - D - F - G - A across octaves). But the **played pitches** extend far beyond the tuned pitches:

```
DAN_TRANH: 16 strings × {open, bend_up, bend_down, vibrato} → continuous pitch

  For string s:
    open_pitch(s) = tuned pentatonic degree
    bent_pitch(s) = open_pitch(s) + β(s)
    
    β(s) ∈ [-2, +4] semitones (player-side bending, asymmetric)
    vibrato(s, t) = open_pitch(s) + A_vib × sin(2π × f_vib × t)
    
    Quarter-tone bends: β(s) can be any value, not just semitone multiples
    This means the đàn tranh produces CONTINUOUS pitch within its range
```

**Bridge retuning mid-performance:** Unlike the koto (which retunes between pieces), the đàn tranh can be **retuned during performance** by physically moving the bridges. This is a **live lattice reconfiguration** — the pitch topology changes while the music is happening.

```
BRIDGE_RETUNE: {string, Δposition} → Δpitch

  For string s during performance:
    move_bridge(s, Δx) where Δx is physical displacement
    Δpitch(s) = f(string_tension, bridge_displacement)
    
    Constraint: retuning takes time (0.5-2 seconds per string)
    Constraint: only player-side bridges accessible during play
    Constraint: retuning creates audible pitch slide (feature, not bug)
    Constraint: new pitch must be in target scale (snap after retune)
```

This is a **novel constraint operation** — a lattice reconfiguration that is itself a performative event. The audience hears the retuning. The constraint state of the instrument changes audibly, in real-time.

**Vietnamese modal system:** Vietnamese traditional music (nhã nhạc, ca trù, cải lương) uses pentatonic scales with **mode-specific ornamentation patterns**. Each mode (điệu) specifies not just scale degrees but characteristic bending patterns:

```
DIỆU: {mode, scale_degree} → {bend_pattern, target_pitch}

  For mode m and degree d:
    ornament(m, d) = {
      approach_bend: how to arrive at the note (from above, from below, direct)
      sustain_bend: pitch trajectory while holding the note (rise, fall, wave)
      departure_bend: how to leave the note (glide up, drop, vibrato then release)
    }
    
    These are PRESCRIBED — not improvised. The ornament is the identity of the mode.
```

### 5.2 Vietnamese Court Music (Nhã Nhạc)

Vietnamese court music (nhã nhạc, 雅樂) shares historical origins with Japanese gagaku and Korean a-ak (all derived from Chinese yayue). Its constraint topology combines:
- **Pentatonic pitch lattice** (shared with Chinese/Japanese/Korean traditions)
- **Specific orchestration constraints** (which instruments play in which ceremonial context)
- **Processional/tempo constraints** tied to ritual function

The court music tradition adds a **ceremonial constraint layer** — pitch and tempo are further constrained by the ritual context (coronation vs. banquet vs. funeral), creating a multi-layered constraint system where musical parameters are subordinate to ceremonial function.

---

## 6. Unified Constraint Mappings

### 6.1 Parameter Glossary

| Parameter | Symbol | Domain | Origin | Description |
|-----------|--------|--------|--------|-------------|
| Pentatonic snap | SNAP₅ | ℝ → ℤ₅ | All traditions | Quantize continuous pitch to 5-position lattice |
| Ma budget | MA | ℝ₊ × Context | Japan | Structured silence budget per phrase |
| JHK acceleration | JHK | TEMPO(t) → ℝ₊ | Japan | Three-phase acceleration curve |
| Breath capacity | BREATH | ℤ₊ (liters) | Japan (shakuhachi) | One-breath phrase limit |
| Anti-tempo | ANTI_T | TEMPO → 0⁺ | China (guqin) | Exponential deceleration toward zero |
| Bridge retune | RETUNE | String × Δpos | Vietnam (đàn tranh) | Live lattice reconfiguration |
| Acceleration curve | ACCEL | TEMPO(Sₖ) | Korea (sanjo) | Step-wise tempo increase across sections |
| Narrative state | NARR | {char, emotion} | Korea (pansori) | Semantic constraint on vocal parameters |
| Wu Xing cycle | WUXING | ℤ₅ → ℤ₅ | China | Five-phase generation/overcoming constraints |
| Quarter-tone bend | QBEND | [-2, +4] semitones | Vietnam | Continuous pitch within pentatonic frame |

### 6.2 Constraint Interaction Matrix

How do these constraints interact? The matrix below shows dependencies:

```
         SNAP₅  MA   JHK  BREATH ANTI_T RETUNE ACCEL NARR WUXING QBEND
SNAP₅      -    weak  med  weak   weak   strong  med  weak  strong  strong
MA         weak   -   strong strong strong weak   med  med   weak    weak
JHK        med  strong  -   med    anti  weak   strong weak  weak    med
BREATH     weak strong med    -     weak  weak   weak  strong weak    weak
ANTI_T     weak strong anti  weak   -    weak   anti  weak  weak    med
RETUNE    strong weak  weak  weak   weak   -    weak  weak  weak   strong
ACCEL      med  med  strong weak  anti  weak    -    weak  weak    med
NARR       weak  med  weak strong weak   weak   weak   -    weak    weak
WUXING    strong weak  weak  weak   weak  weak   weak  weak   -     weak
QBEND     strong  med  med  weak   med  strong  med  weak  weak     -
```

**Key interactions:**
- **MA × JHK = strong:** As tempo increases (JHK), ma duration decreases proportionally. The silence budget is consumed by acceleration.
- **BREATH × MA = strong:** Inhalation time sets the minimum ma between phrases. Longer phrases require longer silences.
- **JHK × ANTI_T = anti-correlated:** These are opposite temporal strategies. A performance uses one or the other, not both.
- **RETUNE × QBEND = strong:** Bridge retuning enables or constrains subsequent bending possibilities.
- **SNAP₅ × WUXING = strong:** The five-phase cycle constrains which pentatonic positions are preferred at any moment.

### 6.3 The Five Constraint Domains

Mapping East Asian musical constraints to the five constraint-theory domains:

**SNAP (Pitch Quantization):**
- Pentatonic lattice (5 positions) — all traditions
- Wu Xing cycle constrains walk on lattice — Chinese
- Quarter-tone bends extend lattice locally — Vietnamese
- 91-position guqin lattice — Chinese
- 13-string koto lattice — Japanese

**FUNNEL (Pitch Navigation):**
- Jo-ha-kyu creates time-varying funnel (widens with tempo) — Japanese
- Sanjo sections create step-wise funnel changes — Korean
- Narrative state drives funnel selection — Korean (pansori)
- Meditation mode narrows funnel to single notes — Chinese (guqin)

**CONSENSUS (Voice-Leading/Resolution):**
- Wu Xing generation cycle provides preferred resolution paths — Chinese
- Ma creates consensus through shared silence — Japanese
- Narrative arc provides consensus framework — Korean (pansori)

**LAMAN (Cadence/Arrival):**
- Breath exhaustion as cadence trigger — Japanese (shakuhachi)
- Section boundaries as cadence points — Korean (sanjo)
- Ritual function as cadence determinant — Vietnamese (court music)

**TEMPO (Temporal Constraint):**
- JHK acceleration curve — Japanese
- Anti-tempo deceleration — Chinese (guqin)
- Sanjo step-wise acceleration — Korean
- Ma silence budget — Japanese
- Breath-paced timing — Japanese (shakuhachi)
- Bridge retuning duration — Vietnamese

---

## 7. Novel Parameters

### 7.1 Ma (Silence Budget)

**Parameter definition:**

```
ma = {
  budget: ℝ₊,          // total silence duration available for phrase
  density: [0, 1],      // silence fraction of total phrase duration
  tension: ℝ → ℝ,      // function mapping time to accumulated expectation
  minimum_gap: ℝ₊,      // minimum silence between any two events
  resolution: boolean   // whether accumulated tension has been resolved
}

Constraints:
  density ≥ θ_ma (genre-dependent, 0.15 - 0.90)
  tension must be non-negative and non-decreasing within phrase
  tension must resolve (return to ≤ ε) at phrase boundary
  minimum_gap ≥ μ_ma (breath-time, ritual, or aesthetic lower bound)
```

### 7.2 Breath Capacity Constraint

**Parameter definition:**

```
breath = {
  capacity: ℝ₊,          // available air volume (liters)
  flow_rate: ℝ₊,         // air consumption rate (liters/sec), function of pitch + dynamics
  remaining: ℝ₊,         // current air volume remaining
  phrase_duration: ℝ₊,   // maximum phrase length = capacity / flow_rate
  recovery_time: ℝ₊      // minimum inhalation time = f(capacity - remaining)
}

Constraints:
  remaining ≥ 0 at all times (cannot exhale more than available)
  phrase must end before remaining reaches 0
  dynamics must taper as remaining → 0 (natural decay)
  recovery_time sets minimum ma between phrases
```

### 7.3 Acceleration Curve (JHK / Sanjo)

**Parameter definition:**

```
accel = {
  type: "continuous" | "step",     // JHK (continuous) or Sanjo (step-wise)
  start_tempo: ℝ₊,                 // initial tempo (BPM)
  end_tempo: ℝ₊,                   // final tempo (BPM)
  alpha: ℝ₊,                       // acceleration factor (end/start)
  phases: [{tempo, duration}],      // for step-wise: tempo plateaus
  curve: ℝ → ℝ,                    // for continuous: monotonically increasing f(t)
  allow_decel: boolean              // final cadence exception
}

Constraints:
  for continuous: curve'(t) > 0 (strictly accelerating, except final cadence)
  for step-wise: phases[k].tempo < phases[k+1].tempo (strictly increasing plateaus)
  alpha = end_tempo / start_tempo ∈ [1.2, 12.0] (range across traditions)
```

### 7.4 Bridge Retuning Mid-Performance

**Parameter definition:**

```
retune = {
  string: ℤ,                       // which string is being retuned
  delta_position: ℝ,               // physical bridge displacement
  delta_pitch: ℝ,                  // resulting pitch change (semitones)
  duration: ℝ₊,                    // time to complete retuning (0.5-2 sec)
  audible: boolean,                // whether audience hears the slide (always true)
  target_scale: pentatonic_set,    // new lattice configuration after retune
  snap_after: boolean              // whether pitch snaps to nearest degree after retune
}

Constraints:
  duration ≥ 0.5 sec (physical minimum for bridge movement)
  only player-side bridges accessible during play
  resulting pitch must be within target pentatonic (snap after retune)
  retuning is a performative event — it cannot be silent or hidden
  max 1-2 strings retuned per performance section
```

---

## 8. Ten Presets

### Preset 1: Zen Meditation (禅の瞑想)

```
Origin: Japan — Shakuhachi suizen (blowing meditation)
Constraint profile:
  SNAP: Miyako-bushi pentatonic (5 positions)
  MA: density = 0.80, minimum_gap = 3.0 sec
  TEMPO: ANTI_T mode, start = 8 BPM, decay λ = 0.05
  BREATH: capacity = 3.0L, flow_rate = 0.1 L/sec (slow, meditative)
  JHK: disabled (anti-tempo mode active)
  
Description: A single shakuhachi, playing honkyoku (本曲, original pieces) 
in the context of Zen Buddhist meditation. The music is a byproduct of 
breathing practice — the phrase follows the breath, the silence follows 
the inhalation, and the overall trajectory is toward stillness. Tempo 
decays exponentially. Notes are long, bent, and resonant. Silence dominates.

Typical duration: 10-20 minutes
Emotional trajectory: active mind → settling → stillness
```

### Preset 2: Tea Ceremony (茶道)

```
Origin: Japan — Chadō accompaniment
Constraint profile:
  SNAP: In scale (5 positions)
  MA: density = 0.50, minimum_gap = 2.0 sec
  TEMPO: 15-25 BPM, very slow, nearly static
  JHK: minimal, α = 1.2 (barely perceptible acceleration)
  
Description: Sparse koto or shamisen accompaniment for tea ceremony. 
The music must never draw attention to itself — it supports the ritual 
without dominating it. Ma is generous. Dynamics are soft. The constraint 
is restraint: every sound must justify its existence against the silence 
it interrupts.

Typical duration: 30-45 minutes (matches ceremony length)
Emotional trajectory: calm → focused → serene
```

### Preset 3: Gagaku (雅楽)

```
Origin: Japan — Imperial court music
Constraint profile:
  SNAP: Ritsu or In scale (5 positions)
  MA: density = 0.35, minimum_gap = 1.0 sec
  JHK: enabled, α = 1.5 (gentle acceleration over long form)
  BREATH: not applicable (wind instruments play with circular breathing or 
          phrase boundaries aligned with ensemble breathing)
  TEMPO: 20-40 BPM start, 30-60 BPM end
  
Description: The oldest continuous orchestral tradition in the world. 
Gagaku ensemble includes fue (flute), hichiriki (double-reed), sho 
(mouth organ), biwa (lute), koto, and percussion. The constraint topology 
is ensemble-level: each instrument has its own pentatonic subset and 
timing offset, creating a heterophonic texture where all instruments 
play "the same melody" but with individual temporal freedom.

Typical duration: 10-40 minutes per piece
Emotional trajectory: stately → elaborated → resolved
```

### Preset 4: Shakuhachi Honkyoku (尺八本曲)

```
Origin: Japan — Komuso (monk) solo flute
Constraint profile:
  SNAP: In or Miyako-bushi pentatonic (5 positions)
  MA: density = 0.60, minimum_gap = 2.5 sec (breath-paced)
  BREATH: capacity = 3.5L, flow_rate varies with pitch/dynamics
  TEMPO: breath-paced, not metered
  ANTI_T: optional (some honkyoku decelerate toward end)
  
Description: Solo shakuhachi, played by Komuso monks as spiritual practice.
The one-breath constraint is absolute — each phrase is shaped by available 
air. Meri (half-holing) and kari (overblowing) techniques produce 
microtonal inflections within the pentatonic lattice. The MA parameter 
is set by inhalation time. Dynamics follow breath depletion (natural decay).

Typical duration: 8-15 minutes
Emotional trajectory: invocation → wandering → dissolution
```

### Preset 5: Koto Sokyoku (箏曲)

```
Origin: Japan — Koto ensemble/solo
Constraint profile:
  SNAP: Hirajoshi or Kumoi pentatonic (5 positions per tuning)
  MA: density = 0.25, minimum_gap = 0.5 sec
  JHK: enabled, α = 2.0 (moderate acceleration)
  RETUNE: between sections (lattice reconfiguration)
  
Description: Koto music, from classical (Yatsuhashi Kengyo, 17th c.) to 
contemporary. The 13-string lattice provides a 2+ octave pentatonic range 
with string-bending extending pitch beyond the tuned degrees. Sections may 
require bridge retuning (tuning changes between movements). The JHK form 
shapes multi-section works. Contemporary koto may use extended techniques 
but remains pentatonic at the constraint level.

Typical duration: 5-15 minutes
Emotional trajectory: poised → flowing → climactic → resolved
```

### Preset 6: Guqin Meditation (古琴修心)

```
Origin: China — Literati self-cultivation
Constraint profile:
  SNAP: Wu Xing pentatonic with WUXING cycle constraints (5 positions + cycle)
  MA: density = 0.60, minimum_gap = 3.0 sec
  ANTI_T: enabled, start = 10 BPM, λ = 0.03 (slow decay toward stillness)
  BREATH: optional synchronization (player breath aligns with note onset)
  
Description: Guqin played in meditation mode — the traditional context for 
this 3000-year-old instrument. The 91-position lattice (7 strings × 13 hui) 
provides enormous pitch resources, but the anti-tempo constraint means 
these resources are deployed one note at a time, with expanding silence 
between them. The WUXING cycle constrains note choice to the generating 
sequence. Each note is an event; each silence is an experience.

Typical duration: 15-30 minutes
Emotional trajectory: active → contemplative → timeless
```

### Preset 7: Pansori (판소리)

```
Origin: Korea — Solo vocal narrative with drum
Constraint profile:
  SNAP: Korean pentatonic (5 positions, voice covers 3+ octaves)
  NARR: character-driven (multiple characters, emotional arcs)
  BREATH: singer's breath capacity constrains phrase length
  MA: variable (drum fills vs. vocal silence for dramatic effect)
  ACCEL: narrative-driven (tension builds through story, not systematic acceleration)
  
Description: A single singer (sorikkun) and drummer (gosu) perform an 
epic narrative lasting 2-8 hours. The singer uses multiple vocal registers 
(chest, mixed, falsetto, growl) to differentiate characters. The buk 
(drum) provides rhythmic foundation via jangdan patterns. The constraint 
topology is narrative: pitch, timbre, dynamics, and timing all serve the 
story. This is the most semantically constrained preset.

Typical duration: 30 min - 8 hours (one complete madang/story)
Emotional trajectory: follows dramatic arc of the story
```

### Preset 8: Sanjo (산조)

```
Origin: Korea — Instrumental solo with drum accompaniment
Constraint profile:
  SNAP: Korean pentatonic (5 positions)
  ACCEL: step-wise, 5-8 sections, α = 3.0-5.0
  Jangdan: Jinnyang → Jungmori → Jungjungmori → Jajinmori → Hwimori
  MA: decreasing density (ma shrinks as tempo increases)
  
Description: The purest expression of acceleration as musical form. A solo 
instrument (gayageum, geomungo, daegeum, ajaeng, piri) accompanied by 
janggu (hourglass drum) moves through 5-8 sections of increasing tempo. 
The step-wise acceleration means each section establishes a stable tempo 
plateau before jumping to the next. The jangdan cycles shrink from 24 beats 
to 4 beats. The final section (hwimori) is a breathless sprint.

Typical duration: 15-30 minutes
Emotional trajectory: meditative → animated → exhilarating → ecstatic
```

### Preset 9: Vietnamese Court Music (Nhã Nhạc)

```
Origin: Vietnam — Imperial court music of the Nguyễn dynasty
Constraint profile:
  SNAP: Vietnamese pentatonic with QBEND (5 positions + continuous bending)
  MA: density = 0.30, minimum_gap = 1.0 sec
  TEMPO: slow to moderate (20-50 BPM), ceremonial pacing
  QBEND: quarter-tone bends on sustained notes (characteristic ornamentation)
  RETUNE: between ceremonial sections (đàn tranh bridge adjustment)
  
Description: Vietnamese court music, UNESCO Intangible Cultural Heritage. 
Orchestral ensemble with đàn tranh (zither), đàn nguyệt (moon lute), 
sáo trúc (bamboo flute), and percussion. The pentatonic lattice is shared 
with Chinese/Japanese traditions, but Vietnamese practice adds characteristic 
quarter-tone bending patterns specific to each điệu (mode). Ceremonial 
function constrains repertoire, instrumentation, and even performer positioning.

Typical duration: 10-30 minutes per ceremonial piece
Emotional trajectory: formal → ornate → resolved (aligned with ritual)
```

### Preset 10: Korean Drumming (Samulnori / Pungmul)

```
Origin: Korea — Farmer's percussion ensemble
Constraint profile:
  SNAP: not applicable (unpitched percussion)
  ACCEL: embedded in rhythmic patterns (patterns grow denser)
  Jangdan: multiple simultaneous cycles (polyrhythmic)
  MA: density ≈ 0.05 (minimal silence — near-continuous sound)
  BREATH: not applicable (instrumental, no breath constraint)
  
Description: Samulnori (사물놀이, "four objects play") and pungmul (풍물, 
farmer's music) feature four percussion instruments: kkwaenggwari (small 
gong), jing (large gong), janggu (hourglass drum), buk (barrel drum). 
The constraint topology is purely rhythmic — no pitch lattice, but multiple 
simultaneous jangdan cycles creating a polyrhythmic texture. The tempo 
builds through pattern elaboration rather than strict acceleration. This 
is the most rhythmically dense preset — the opposite of the Zen meditation 
preset in almost every parameter.

Typical duration: 5-20 minutes
Emotional trajectory: grounded → building → ecstatic → thunderous
```

---

## 9. Comparative Analysis: East Asian vs. Other Constraint Topologies

### 9.1 Lattice Complexity Spectrum

| System | Lattice positions | Interval precision | Primary constraint |
|--------|------------------|--------------------|--------------------|
| Japanese pentatonic | 5 | ±100 cents | Temporal (ma, breath) |
| Chinese Wu Xing | 5 + cycle | ±100 cents | Temporal (anti-tempo) + cosmological |
| Korean pentatonic | 5 | ±100 cents | Temporal (acceleration) |
| Vietnamese pentatonic | 5 + continuous | ±50 cents (QBEND) | Pitch inflection + temporal |
| Chinese guqin | 91 | variable | Timbre + temporal |
| Arabic maqam | 24 | ±25 cents | Pitch (microtonal) |
| Indian raga | 22 | ±25 cents | Pitch (shruti) + melodic path |
| Western 12-TET | 12 | ±50 cents | Harmonic (functional) |
| West African polyrhythm | 7 (heptatonic) | ±100 cents | Temporal (polyrhythm) |

**East Asian systems cluster at the low-lattice-complexity / high-temporal-complexity end.** This is the fundamental insight: where Arabic and Indian systems invest their constraint budget in pitch precision, East Asian systems invest it in temporal shaping.

### 9.2 The Silence Spectrum

| Tradition | Silence fraction | Silence function |
|-----------|-----------------|------------------|
| Zen shakuhachi | 70-90% | Spiritual practice; sound interrupts silence |
| Guqin meditation | 60-80% | Contemplation; notes as events in void |
| Tea ceremony | 40-60% | Ritual pacing; restraint as aesthetic |
| Gagaku | 25-40% | Ceremonial stasis; measured pace |
| Sanjo | 5-15% (final section) | Contrast with opening silence |
| Korean drumming | <5% | Density as energy; near-continuous sound |

The silence spectrum reveals a **50-fold variation** in ma density across East Asian traditions — from the near-silence of Zen meditation to the near-continuous sound of samulnori. Both extremes are East Asian. The diversity is within the tradition, not between traditions.

---

## 10. Implications for Constraint-Theory Implementation

### 10.1 Required Extensions

To support East Asian constraint topologies, the constraint-theory-core system needs:

1. **MA parameter:** A silence budget parameter with genre-specific thresholds. This is a new TEMPO-subdomain parameter not present in Western, Arabic, or Indian mappings.

2. **BREATH parameter:** A resource-constraint parameter tracking air capacity, flow rate, and remaining volume. Requires integration with phrase-boundary detection.

3. **JHK/ACCEL parameter:** Either continuous (jo-ha-kyu) or step-wise (sanjo) acceleration curves. The TEMPO domain must support monotonically increasing tempo functions, not just fixed tempos.

4. **ANTI_T parameter:** Exponential deceleration toward zero. The inverse of ACCEL. Requires TEMPO to support decreasing functions and near-zero values.

5. **RETUNE parameter:** Live lattice reconfiguration with audible transition. The SNAP operation must support dynamic lattice changes during performance.

6. **QBEND parameter:** Continuous pitch within a pentatonic framework. The SNAP operation must allow "soft snapping" where pitch can float near (but not exactly on) lattice points.

7. **WUXING parameter:** Five-phase cycle constraining walk on pentatonic lattice. A directed-graph constraint on the SNAP lattice.

8. **NARR parameter:** Semantic state driving musical parameters. Character tracking and emotional arc as inputs to constraint functions.

### 10.2 Dodecet Extensions

The 12-bit dodecet structure from the A₂ lattice framework requires modification for East Asian systems:

- **Reduced pitch bits:** 5-position pentatonic needs only 3 bits for scale degree (vs. 4 for 12-TET)
- **Expanded temporal bits:** Acceleration/anti-tempo state needs representation
- **Ma state bit:** Whether currently in silence or sound
- **Breath state:** Remaining capacity (quantized to 2-3 bits)
- **Narrative state:** Character ID + emotional state (2-3 bits)

A proposed **East Asian dodecet** structure:

```
Bits 0-2:  Scale degree (0-4, pentatonic position; 5-7 reserved)
Bits 3-4:  Temporal mode (00=static, 01=JHK, 10=sanjo, 11=anti-tempo)
Bits 5-6:  Ma state (00=sound, 01=short_ma, 10=long_ma, 11=breath_ma)
Bit 7:     WUXING direction (0=sheng/generate, 1=ke/overcome)
Bits 8-9:  Breath state (00=full, 01=comfortable, 10=low, 11=critical)
Bits 10-11: Reserved / tradition-specific
```

### 10.3 Cross-Tradition Modulation

One of the most exciting possibilities is **cross-tradition modulation** — transitioning between constraint topologies mid-performance:

- **Japanese → Chinese:** Shift from JHK acceleration to anti-tempo deceleration (invert the temporal curve)
- **Korean → Vietnamese:** Shift from sanjo step-wise acceleration to QBEND pitch elaboration (transfer complexity from time to pitch)
- **Meditation → Festival:** Shift from high-MA/low-tempo to low-MA/high-tempo (Zen → samulnori transition)

These modulations require the constraint system to support **topology morphing** — gradual parameter interpolation between constraint configurations. The 10 presets defined above can serve as waypoints for such morphing.

---

## 11. Conclusion: Silence as Structure

East Asian musical traditions reveal a constraint topology that is **inverted** relative to Western and Middle Eastern systems. Where those traditions build complexity through pitch (more notes, finer intervals, denser harmonies), East Asian traditions build complexity through **time** — shaped silence, controlled breath, designed acceleration, and intentional stillness.

The pentatonic lattice is the simplest non-trivial pitch constraint (5 nodes, diameter 2). But the temporal constraints — ma budgets, breath limits, JHK curves, anti-tempo convergence, sanjo acceleration ladders — are among the most sophisticated in world music.

The constraint-theory framework, with its SNAP → FUNNEL → CONSENSUS → LAMAN → TEMPO pipeline, accommodates this inversion naturally: the same five domains operate, but the **computational weight** shifts from pitch (SNAP) to time (TEMPO). The ma parameter is the clearest expression of this — a constraint on the *absence* of events, rather than their presence.

For implementation, the key lesson is: **East Asian music cannot be represented by pitch alone.** A system that captures the pentatonic snap but ignores ma, breath, and acceleration has captured nothing of value. The constraint topology is temporal first, pitch second.

---

## References

- Malm, W. P. (2000). *Traditional Japanese Music and Musical Instruments*. Kodansha International.
- Tokumaru, Y. (1981). "Jo-ha-kyu in Japanese Music." *Asian Music*, 13(1), 35-48.
- Provine, R. C. (1988). *Essays on Sino-Korean Musicology: Early Instruments for the Standard Court Tones*. Il Ji Sa.
- Nguyen, T. T. (2017). "Vietnamese Đàn Tranh Performance Practice and Quarter-Tone Systems." *Journal of the International Association for the Study of Popular Music*, 7(2).
- Lee, B. (2007). *P'ansori: The Korean One-Man Theater*. Korean National Commission for UNESCO.
- Hwang, B. (2009). *Sanjo: Korean Scattered Melodies*. Seoul National University Press.
- Yung, B. (1989). *Cantonese Opera: Performance as Creative Process*. Cambridge University Press.
- De Ferranti, H. (2000). *Japanese Musical Instruments*. Oxford University Press.
- Liang, M. (1985). *Music of the Billion: An Analysis of Chinese Songs and Their Musical Structure*. Heinrichshofen.
- Titon, J. T., & Ko, S. (1992). "Korean Sanjo and the Aesthetics of Speed." *World of Music*, 34(2), 53-72.
