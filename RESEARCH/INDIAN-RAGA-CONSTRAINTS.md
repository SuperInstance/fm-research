# Indian Raga System Mapped to Constraint Theory

> 22 shruti, 10 ragas, 5 ornament types: a complete constraint-theoretic parameterization of Hindustani classical music.

**Date:** 2026-05-23
**Status:** Research Document — Deep Synthesis
**Classification:** Constraint Theory × Indian Music Theory × Microtonal Systems
**Repos:** [fm-research](https://github.com/SuperInstance/fm-research) · [constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core)

---

## Abstract

The Hindustani raga system is one of the world's most sophisticated musical constraint frameworks. Each raga defines a self-consistent universe of permissible pitches, ornaments, rhythmic frameworks, emotional associations, and temporal contexts — all operating over a 22-shruti (microtonal) octave that far exceeds the resolution of 12-tone equal temperament. We demonstrate that this system maps precisely onto the constraint theory pipeline: shruti positions form a snap lattice, vadi/samvadi relationships define funnel attractors, tala cycles enforce Laman-like temporal rigidity, and the five principal ornament types (meend, gamak, andolan, sparsh/krintan, murki) generate novel sound modification parameters with no Western equivalent. We provide full parameter specifications for 10 canonical ragas, formal constraint mappings, and a complete preset architecture for implementation.

**Key result:** The raga system is a fully self-consistent constraint satisfaction framework operating over a 22-position pitch lattice, with emotional and temporal constraints that have no analogue in Western music theory. Mapping it to constraint theory reveals parameters that are invisible in 12-TET.

---

## 1. Foundations: The 22-Shruti Lattice

### 1.1 Beyond 12-TET

Western music divides the octave into 12 equal semitones (100 cents each). The Indian system recognizes **22 shruti** (literally "what is heard") — microtonal positions that are not equally spaced but derived from just intonation ratios. The octave spans from Sa (tonic) to Sa' (octave), with the 22 positions corresponding to specific ratios from the harmonic series.

The shruti positions in cents relative to the tonic (Sa = 0¢):

| Position | Name | Ratio | Cents | Western Approx. |
|----------|------|-------|-------|-----------------|
| 1 | Sa | 1/1 | 0 | Unison |
| 2 | Komal Re (ε) | 256/243 | 90 | — |
| 3 | Komal Re | 16/15 | 112 | Minor 2nd (flat) |
| 4 | Shuddha Re | 9/8 | 204 | Major 2nd |
| 5 | Komal Ga (ε) | 32/27 | 294 | — |
| 6 | Komal Ga | 6/5 | 316 | Minor 3rd |
| 7 | Shuddha Ga | 5/4 | 386 | Major 3rd |
| 8 | Shuddha Ma | 4/3 | 498 | Perfect 4th |
| 9 | Tivra Ma | 45/32 | 590 | — |
| 10 | Tivra Ma (ε) | 3/2 − ε | 610 | Augmented 4th (sharp) |
| 11 | Pa | 3/2 | 702 | Perfect 5th |
| 12 | Komal Dha (ε) | 128/81 | 792 | — |
| 13 | Komal Dha | 8/5 | 814 | Minor 6th (flat) |
| 14 | Shuddha Dha | 27/16 | 906 | Major 6th |
| 15 | Komal Ni (ε) | 16/9 | 996 | — |
| 16 | Komal Ni | 9/5 | 1018 | Minor 7th |
| 17 | Shuddha Ni | 15/8 | 1088 | Major 7th |
| 18 | Sa' | 2/1 | 1200 | Octave |

(Positions 2, 5, 9, 12, 15 are the "extra" microtonal positions between the 12-TET notes — marked ε for ekshruti, the subtlest intervals.)

### 1.2 The 22-Shruti as a SNAP Lattice

In constraint theory terms, the 22-shruti system is a **snap lattice** with higher resolution than the 12-TET Tonnetz:

```
SNAP_22(continuous_pitch) → nearest_shruti ∈ S_22

where S_22 = {s_i : i ∈ {1..22}} with intervals measured in just intonation ratios
```

Each shruti position is an attractor in pitch space. The snap function maps continuous pitch to the nearest lattice point, but — crucially — **in performance, pitch does not snap**. Instead, it flows through the lattice via ornaments (meend, gamak). The lattice defines *targets*, not *prisons*.

This is fundamentally different from Western SNAP, where quantization is rigid. In the raga system:
- **Static notes** (held tones) snap to shruti positions
- **Ornamented notes** pass *through* shruti positions continuously
- **Andolan notes** oscillate *around* shruti positions without ever settling

The constraint is not "you must be on a lattice point" but "your trajectory must respect the lattice topology."

### 1.3 Interval Categories Within the 22 Shruti

The 22 shruti organize into a hierarchy of interval types that constrain raga construction:

- **Shuddha** (pure): The natural form of each swara (note) — positions 1, 4, 7, 8, 11, 14, 17, 18
- **Komal** (flat): The flattened form — positions 3, 6, 13, 16
- **Tivra** (sharp): The sharpened form (only for Ma) — position 9
- **Ati-Komal** (extra-flat): Microtonal positions between komal and the previous note — positions 2, 5, 12, 15

These four categories create a natural **constraint grammar**: every raga selects a subset of these positions, and the selection determines the raga's character.

---

## 2. The Ten Canonical Ragas: Full Parameter Specifications

### 2.1 Raga Bhairavi

**Thaat:** Bhairavi | **Time:** Any (morning preferred) | **Rasa:** Karuna (pathos), Shringar (love)

| Parameter | Value |
|-----------|-------|
| **Aroha** (ascent) | S r g m P d n Ṡ |
| **Avaroha** (descent) | Ṡ n d P m g r S |
| **Vadi** (king note) | Komal Dha (d) |
| **Samvadi** (queen note) | Komal Re (r) |
| **Pakad** (catchphrase) | g m d, n d, P m, g m g r S |
| **Varjit** (forbidden) | None (uses all 12 swaras; bhairavi is sampoorna in both aroha/avaroha) |
| **Shruti emphasis** | Komal Re at 112¢ (not the microtonal 90¢); Komal Ga at 316¢; strong Komal Dha |
| **Characteristic ornament** | Andolan on Komal Ga and Komal Dha — these notes oscillate gently without settling |
| **Funnel gravity** | Strongest pull toward Komal Dha; secondary pull toward Komal Re |
| **SNAP mapping** | All 12 positions + microtonal shading on r, g, d, n |

**Constraint profile:** Bhairavi is the most permissive raga — all 12 chromatic notes are allowed. Its constraint is not *which notes* but *how they're treated*: the komal notes must have andolan (oscillation), giving the raga its characteristic "weeping" quality. The funnel is broad (many notes) but the gravitational center on d is unmistakable.

### 2.2 Raga Yaman

**Thaat:** Kalyan | **Time:** Evening (6PM–9PM) | **Rasa:** Shringar (romantic love), Veer (heroism)

| Parameter | Value |
|-----------|-------|
| **Aroha** | Ṡ R G M' P D N Ṡ |
| **Avaroha** | Ṡ N D P M' G R S |
| **Vadi** | Gandhar (G) |
| **Samvadi** | Nishad (N) |
| **Pakad** | N R G, M' G, P N D, N R S |
| **Varjit** | Komal Re (r), Komal Ga (g), Shuddha Ma (m), Komal Dha (d), Komal Ni (n) |
| **Shruti emphasis** | Tivra Ma (M') at ~590¢ is the signature — bright, piercing |
| **Characteristic ornament** | Meend from N→R (跨越 sa in descent), gamak on M' |
| **Funnel gravity** | G is the primary attractor; every phrase tends to resolve through G |

**Constraint profile:** Yaman is the raga of evening longing. Tivra Ma creates a distinctive tension — the sharpened fourth is the note that "doesn't belong" in the major scale, creating perpetual yearning. The SNAP lattice includes only 7 of 22 shruti positions, making it highly constrained.

### 2.3 Raga Darbari

**Thaat:** Asavari | **Time:** Night (9PM–midnight) | **Rasa:** Karuna (pathos), Shanta (peace)

| Parameter | Value |
|-----------|-------|
| **Aroha** | S R G m P d n Ṡ |
| **Avaroha** | Ṡ d n P m G m R S |
| **Vadi** | Komal Dha (d) |
| **Samvadi** | Komal Re (r) — but r is absent in aroha! |
| **Pakad** | R G m G, m P d, d P, P m G m R S |
| **Varjit** | Komal Re in aroha (ascent); present in avaroha (descent) |
| **Shruti emphasis** | Komal Dha at 814¢ with heavy andolan; Komal Ga at 316¢ with andolan |
| **Characteristic ornament** | Darbari's signature: a slow, heavy andolan on d that dips below the shruti position. Also: deliberate, weighted meend from P→d |
| **Funnel gravity** | d is the gravitational center; phrases spiral downward through P→d→P |

**Constraint profile:** Darbari is the raga of courtly gravity. It is *asymmetric* — r is forbidden in ascent but appears in descent. This creates a one-way constraint: the raga "opens up" as it descends, revealing notes that were hidden on the way up. The andolan on d is so characteristic that without it, the raga ceases to be Darbari.

### 2.4 Raga Malkauns

**Thaat:** Bhairavi (theoretically) | **Time:** Night (midnight–3AM) | **Rasa:** Veer (heroism), Shanta (tranquility)

| Parameter | Value |
|-----------|-------|
| **Aroha** | S g m d n Ṡ |
| **Avaroha** | Ṡ n d m g S |
| **Vadi** | Madhyam (m) |
| **Samvadi** | Shuddha Sa (S) — or Komal Dha (d) per some traditions |
| **Pakad** | g m d, n d m, g m g S |
| **Varjit** | R, G, P, D — five notes excluded! Audav-audav (5-note scale) |
| **Shruti emphasis** | Only 5 of 22 shruti positions are valid. Intervals are wide, creating spaciousness |
| **Characteristic ornament** | Gamak on m and d; meend from n→d is always slow, weighted |
| **Funnel gravity** | m is the axis — it is simultaneously the vadi and the note that every phrase orbits |

**Constraint profile:** Malkauns is one of the most constrained ragas — only 5 notes out of 22 possible positions. This extreme restriction paradoxically creates one of the most powerful rasas. The constraint IS the expression: the missing notes (especially Pa, the perfect fifth) create a haunting incompleteness. In constraint theory terms, the high dimensionality of the *excluded* space creates tension through absence.

### 2.5 Raga Bageshri

**Thaat:** Khamaj | **Time:** Night (9PM–midnight) | **Rasa:** Shringar (love), Karuna (longing)

| Parameter | Value |
|-----------|-------|
| **Aroha** | S R g m P D n Ṡ |
| **Avaroha** | Ṡ n D P m g m R S |
| **Vadi** | Madhyam (m) |
| **Samvadi** | Shuddha Sa (S) |
| **Pakad** | D n Ṡ, n D P, P m g, m R S |
| **Varjit** | Komal Ga (g) replaces Shuddha Ga; Komal Ni (n) replaces Shuddha Ni; R, P, D are shuddha |
| **Shruti emphasis** | Komal Ga at 316¢; Komal Ni at 1018¢; m is the gravitational hub |
| **Characteristic ornament** | Meend from D→n→Ṡ in ascent (swooping through the komal ni); gentle gamak on m |
| **Funnel gravity** | m attracts all phrases; descent always passes through m before reaching S |

### 2.6 Raga Todi

**Thaat:** Todi | **Time:** Morning (6AM–9AM) | **Rasa:** Karuna (pathos), Bhakti (devotion)

| Parameter | Value |
|-----------|-------|
| **Aroha** | S r g M' P d N Ṡ |
| **Avaroha** | Ṡ N d P M' g r S |
| **Vadi** | Komal Re (r) |
| **Samvadi** | Komal Dha (d) |
| **Pakad** | r g M', M' g r, d N Ṡ, d P M' g r S |
| **Varjit** | Shuddha Re (R), Shuddha Ga (G), Shuddha Ma (m), Shuddha Dha (D), Komal Ni (n) |
| **Shruti emphasis** | The combination r + g + M' creates a uniquely angular profile. Komal Re at the lower position (112¢); Komal Ga at 316¢; Tivra Ma at 590¢ |
| **Characteristic ornament** | Andolan on r — it oscillates between shruti positions 2 and 3. Also: gamak on d |
| **Funnel gravity** | r is the king note — all phrases eventually settle on r. The combination r→g→M' creates a "zigzag" path through the lattice |

**Constraint profile:** Todi is the queen of morning ragas. Its note selection is highly asymmetric: komal Re, komal Ga, tivra Ma, komal Dha — four "altered" notes that create an immediately recognizable interval pattern. The andolan on r is its fingerprint.

### 2.7 Raga Bhairav

**Thaat:** Bhairav | **Time:** Morning (dawn–6AM) | **Rasa:** Shanta (peace), Bhakti (devotion)

| Parameter | Value |
|-----------|-------|
| **Aroha** | S r G m P d N Ṡ |
| **Avaroha** | Ṡ N d P m G r S |
| **Vadi** | Komal Dha (d) |
| **Samvadi** | Komal Re (r) |
| **Pakad** | G m d, d P m, G m G r S |
| **Varjit** | Shuddha Re (R), Shuddha Dha (D), Tivra Ma (M'), Komal Ga (g), Komal Ni (n) |
| **Shruti emphasis** | Komal Re and Komal Dha — these two komal notes (flattened 2nd and 6th) define the raga |
| **Characteristic ornament** | Andolan on both r and d — they oscillate slowly, giving Bhairav its solemnity |
| **Funnel gravity** | d and r form a symmetric gravitational pair; the raga balances between them |

**Constraint profile:** Bhairav is the raga of dawn meditation. Its signature is the pair of komal notes (r, d) at symmetric positions (flattened 2nd and 6th), both requiring andolan. This creates a "gravitational symmetry" — the raga doesn't resolve to one note but oscillates between two equal attractors.

### 2.8 Raga Marwa

**Thaat:** Marwa | **Time:** Late afternoon (3PM–6PM) | **Rasa:** Veer (heroism), Karuna (pathos)

| Parameter | Value |
|-----------|-------|
| **Aroha** | S r G M' D Ṡ |
| **Avaroha** | Ṡ D M' G r S |
| **Vadi** | Komal Re (r) |
| **Samvadi** | Shuddha Dha (D) |
| **Pakad** | D M' G r, G M' D Ṡ, D M' G r S |
| **Varjit** | Pa (P) and Ni (N) are absent — only 6 notes |
| **Shruti emphasis** | The absence of Pa (perfect fifth) is radical — it removes the strongest harmonic anchor |
| **Characteristic ornament** | Meend from D→Ṡ (leap to octave), gamak on r and M' |
| **Funnel gravity** | r is primary; D is secondary; the absence of Pa forces phrases to navigate without the usual resting point |

**Constraint profile:** Marwa is one of the strangest ragas — it omits Pa, the perfect fifth, which in most musical systems is the most "consonant" interval after the octave. This absence destabilizes the entire pitch space, creating a restless, searching quality. In constraint terms: removing the strongest attractor (Pa) redistributes gravitational force to the remaining notes.

### 2.9 Raga Khamaj

**Thaat:** Khamaj | **Time:** Night (9PM–midnight) | **Rasa:** Shringar (love), Hasya (joy)

| Parameter | Value |
|-----------|-------|
| **Aroha** | S R G m P D N Ṡ |
| **Avaroha** | Ṡ n D P m G R S (uses both N and n — Shuddha Ni in ascent, Komal Ni in descent) |
| **Vadi** | Gandhar (G) |
| **Samvadi** | Nishad (N) |
| **Pakad** | G m P D N Ṡ, n D P m G m R S |
| **Varjit** | None in aroha; in avaroha, N→n switch creates a bimodal constraint |
| **Shruti emphasis** | N (1088¢) in ascent vs n (1018¢) in descent — the note changes character based on direction |
| **Characteristic ornament** | Quick murki turns around N/n; sparsh (grace) from n→Ṡ |
| **Funnel gravity** | G attracts in the middle register; Ṡ and n create a "playful" upper-register tension |

**Constraint profile:** Khamaj introduces a *directional constraint*: the same scale degree (Ni) has different values depending on whether you're ascending or descending. This is a context-dependent snap — the lattice position depends on trajectory, not just position.

### 2.10 Raga Miyan ki Malhar

**Thaat:** Khamaj | **Time:** Monsoon season (any time during rains) | **Rasa:** Shringar (love), Karuna (longing), wonder at nature

| Parameter | Value |
|-----------|-------|
| **Aroha** | S R G m P D N Ṡ |
| **Avaroha** | Ṡ n D n P m g m G R S |
| **Vadi** | Gandhar (G) |
| **Samvadi** | Nishad (N) |
| **Pakad** | D N Ṡ, n D P m g m G R S |
| **Varjit** | Complex — uses N in ascent and both N/n in descent; also uses both G and g in descent |
| **Shruti emphasis** | The G→g and N→n shifts in descent create a "melting" effect — notes flatten as the phrase descends |
| **Characteristic ornament** | Meend suggesting raindrops: rapid alternation D-n-D-NṠ. Also: krintan on m→G transitions |
| **Funnel gravity** | G is the gravitational center; the descent through g→m→G creates the "rain" motif |

**Constraint profile:** Miyan ki Malhar is the monsoon raga — it has a *seasonal constraint* that no Western concept captures. More remarkably, it uses *more notes in descent than ascent* — the raga literally "opens up" as it falls, like rain spreading. The alternation between shuddha and komal forms of the same note (G/g, N/n) within a single phrase creates micro-contradictions that resolve through the raga's internal logic.

---

## 3. Constraint Mapping: Raga → Constraint Theory Pipeline

### 3.1 SNAP → 22-Shruti Lattice

The standard constraint-theory SNAP maps continuous values to the nearest lattice point. For ragas:

```
SNAP_raga(pitch, trajectory, raga_context) → nearest_valid_shruti

where:
  - pitch ∈ ℝ (continuous frequency)
  - trajectory ∈ {ascending, descending, stationary}
  - raga_context determines the valid subset of S_22
```

**Key difference from Western SNAP:** The snap target depends on *direction*. A raga like Khamaj maps Ni to position 17 (1088¢) in ascent but position 16 (1018¢) in descent. This is a **trajectory-dependent snap** — the lattice itself reconfigures based on the performer's melodic direction.

```
SNAP_Western(p, L_12)      → argmin_{q ∈ L_12} ||p - q||
SNAP_Raga(p, dir, R, L_22) → argmin_{q ∈ L_22 ∩ Valid(R, dir)} ||p - q||
```

The raga constraint R selects a subset of the 22-shruti lattice, and the direction `dir` further narrows the valid set. This is a **conditional lattice** — the snap targets are path-dependent.

### 3.2 FUNNEL → Vadi/Samvadi Gravity

In constraint theory, the FUNNEL is a temporal narrowing that drives values toward an attractor. In the raga system, vadi (king note) and samvadi (queen note) serve exactly this function:

```
FUNNEL_raga(phrase, vadi, samvadi) → phrase converging toward vadi

where:
  - vadi is the primary gravitational center
  - samvadi is the secondary center (typically a fifth or fourth away)
  - Every phrase must "touch" vadi or approach it to be recognizable as the raga
```

The funnel operates on multiple timescales:
- **Phrase level:** Each melodic phrase gravitates toward vadi
- **Section level:** An alap (free introduction) progressively reveals vadi, circling closer with each iteration
- **Performance level:** The entire performance is a funnel from exploration (distant from vadi) to resolution (centered on vadi)

**Mathematical model:**

Let d_vadi(phrase_i) be the pitch distance from the center of phrase_i to the vadi. Then:

```
d_vadi(phrase_i) ≈ d_0 · e^(-λ · i)
```

Each successive phrase approaches the vadi exponentially, mirroring the temporal funnel's decay in constraint theory. The decay rate λ varies by raga: Darbari has slow λ (prolonged tension), while Bhairavi has faster λ (quicker resolution).

### 3.3 CONSENSUS → Raga Ensemble Conventions

When multiple musicians perform a raga together (tabla, tanpura, sarangi, singer), they must reach consensus on:

1. **Tonic (Sa):** All instruments tune to the same Sa
2. **Shruti positions:** The tanpura's drone establishes which shruti variant is active
3. **Tala phase:** All musicians agree on where they are in the rhythmic cycle
4. **Ornament interpretation:** The vocalist's gamak must be matched by the sarangi's bowing

This is metronome consensus with additional constraints:

```
CONSENSUS_raga(ensemble, raga) → synchronized performance

constraints:
  - All instruments share Sa (±5¢ tolerance)
  - Tabla and lehra maintain tala phase alignment
  - Tanpura drone strings fix the shruti reference frame
  - Soloist's ornament signals are tracked by accompanying instruments
```

The tanpura is particularly interesting: it plays no melody but continuously sounds the Sa-Pa-Sa' (or Sa-m-Sa' for some ragas) drone, which provides the **reference frame** for the entire ensemble. This is equivalent to a constraint theory anchor node — a fixed point that all other values are measured against.

### 3.4 LAMAN → Tala (Rhythmic Cycle) Rigidity

In constraint theory, Laman rigidity ensures that a graph has exactly enough edges to be rigid but not overconstrained. A tala (rhythmic cycle) is a **rigid temporal structure** with precisely defined articulation points:

#### Teental (16 beats)

```
Structure: | X 2 0 3 | X 2 0 3 | X 2 0 3 | X 2 3 0 |

X = SAM (strong beat, cycle start)
0 = KHALI (empty beat, no tabla bass)
2, 3 = TALI (clap points, structural accents)

Laman analogy: 16 vertices, 4 articulation points (sam, tali×3)
Minimum edges for rigidity: 2n - 3 = 29
Actual edges: 4 × 4 = 16 (subdivision edges) + 4 (articulation) = 20
The structure is UNDER-rigid → allows flexibility within the cycle
```

#### Jhaptaal (10 beats)

```
Structure: | X 2 0 3 | X 2 0 3 4 |
Articulation: sam, tali×2, khali×1
10 beats, 4 articulation points
Laman edges: 2(10) - 3 = 17 vs actual ~14
Still flexible — the tala is a framework, not a cage
```

#### Ektaal (12 beats)

```
Structure: | X 0 2 0 | 3 0 4 0 | X 0 2 0 |
12 beats, 6 subdivisions of 2
Highly symmetric — each pair has identical internal structure
Laman edges: 2(12) - 3 = 21
This is the most "rigid" common tala — less room for variation
```

#### Rupak (7 beats)

```
Structure: | X 2 0 | 3 4 |
7 beats, asymmetric division (3+4)
Laman edges: 2(7) - 3 = 11
Most flexible common tala — fewest beats means maximum freedom
```

**The Laman insight:** A tala is rigid enough to be recognizable (you know where sam is) but flexible enough to allow creative subdivision. This is exactly the Laman condition: n vertices with 2n-3 edges — rigid but minimally so. If a tala were more rigid (more articulation constraints), it would lose its groove. If less rigid, it would lose its identity.

### 3.5 TEMPO → Laya (Speed) Layers

The Indian system has three primary laya (tempo) layers:

| Layer | BPM Range | Constraint Behavior |
|-------|-----------|-------------------|
| **Vilambit** (slow) | 20–60 | Maximum ornament density; each beat is a universe of meend and gamak |
| **Madhya** (medium) | 60–150 | Balanced; ornaments are faster but less elaborate |
| **Drut** (fast) | 150–300+ | Ornaments collapse to sparsh (grace notes); focus shifts to tala patterns |

In constraint theory terms, tempo controls the **time budget per beat**:

```
T_beat = 60/BPM seconds

Ornament_time_available ∝ T_beat
  - Vilambit: T_beat ≈ 2s → full meend (500ms glide) possible
  - Madhya: T_beat ≈ 0.5s → compressed meend, prominent gamak
  - Drut: T_beat ≈ 0.2s → only sparsh/murki possible
```

This creates a **funnel in tempo space**: a traditional performance starts vilambit (wide funnel), accelerates through madhya (narrowing), and reaches drut (converged). The tempo funnel mirrors the pitch funnel — both narrow over time, driving toward resolution.

---

## 4. Novel Sound Parameters from Indian Ornamentation

The five principal ornament types in Hindustani music are not just "effects" — they are **first-class parameters** with specific mathematical properties that have no equivalent in Western synthesis.

### 4.1 Meend (Continuous Glide)

**Definition:** A smooth, continuous pitch glide between two shruti positions, passing through all intermediate positions.

```
meend: [0, 1] → S_22
  meend(t) = s_start + (s_end - s_start) · f(t)

where f(t) is NOT linear but follows a characteristic curve:
  f(t) = t^α, α ∈ [0.5, 2.0]

  α < 1: fast start, slow arrival (common in ascent)
  α > 1: slow start, fast arrival (common in descent)
  α = 1: uniform speed (rare, sounds mechanical)
```

**Parameter spec:**
- `meend_start`: starting shruti position (0–21)
- `meend_end`: ending shruti position (0–21)
- `meend_range`: number of shruti positions traversed (1–22)
- `meend_curve` (α): glide shape parameter (0.5–2.0)
- `meend_duration`: time in ms (100–2000ms typically)

**Constraint:** Meend must pass through all intermediate valid shruti positions for the raga. If an intermediate position is forbidden by the raga, the meend must take a "detour" through an alternate path — this is musically meaningful and creates the raga's characteristic melodic contours.

**Synthesis implementation:**
```python
def meend(start_hz, end_hz, alpha, duration_ms, sample_rate=44100):
    """Generate a meend (glide) between two pitches."""
    n_samples = int(duration_ms * sample_rate / 1000)
    t = np.linspace(0, 1, n_samples)
    # Characteristic curve — not linear
    curve = t ** alpha
    freq = start_hz + (end_hz - start_hz) * curve
    # Convert frequency trajectory to phase
    phase = np.cumsum(2 * np.pi * freq / sample_rate)
    return np.sin(phase)
```

### 4.2 Gamak (Rapid Oscillation)

**Definition:** A rapid oscillation of pitch around a central note, typically spanning 2–4 shruti positions. Unlike vibrato (which is symmetric and small), gamak is intentional, often asymmetric, and wide.

```
gamak: [0, 1] → S_22
  gamak(t) = s_center + A · sin(2π · f_gamak · t) · g(t)

where:
  s_center = the target shruti
  A = amplitude in shruti units (1–3 positions)
  f_gamak = oscillation frequency (5–12 Hz)
  g(t) = envelope (attack-sustain-decay)
```

**Parameter spec:**
- `gamak_center`: target shruti position
- `gamak_amplitude`: oscillation width in shruti (1–3)
- `gamak_speed`: oscillation frequency (5–12 Hz)
- `gamak_asymmetry`: ratio of upward to downward excursion (0.3–0.7; 0.5 = symmetric)
- `gamak_envelope`: ADSR shape for the oscillation's lifecycle

**Constraint:** Gamak amplitude is limited by the raga's valid note set. The oscillation cannot venture into forbidden shruti territory. This means gamak is a **constrained oscillation** — its freedom is bounded by the raga's lattice.

**Raga-specific gamak profiles:**
- **Darbari:** Wide, slow gamak on d (amplitude 2–3, speed 5–7 Hz, asymmetric downward)
- **Malkauns:** Medium gamak on m (amplitude 1–2, speed 6–8 Hz, symmetric)
- **Todi:** Sharp gamak on r (amplitude 1, speed 8–12 Hz, tight and fast)

### 4.3 Andolan (Gentle Swing)

**Definition:** A slow, deliberate oscillation on specific notes, typically komal (flat) notes. Unlike gamak, andolan does not have a clear center — the note "wavers" without settling.

```
andolan: [0, 1] → S_22
  andolan(t) = s_target + A · sin(2π · f_and · t + φ(t))

where:
  f_and = 2–4 Hz (much slower than gamak)
  A = 1–2 shruti positions
  φ(t) = slowly varying phase (creates the "unsettled" quality)
```

**Parameter spec:**
- `andolan_target`: the shruti position being ornamented
- `andolan_amplitude`: swing width (1–2 shruti)
- `andolan_speed`: 2–4 Hz
- `andolan_phase_drift`: rate of phase wandering (0–1 Hz) — this creates the "unstable" feeling
- `andolan_weight`: how "heavy" the oscillation feels (affects the sustain envelope)

**The andolan paradox:** In constraint terms, andolan is a note that *refuses to snap*. It oscillates near a lattice point but never lands on it. This violates the basic SNAP assumption (that values converge to lattice points) — and that's the point. Andolan is a **meta-constraint violation** that is itself constrained: the oscillation must stay within bounds defined by the raga, even though it never resolves.

**Ragas requiring andolan:**
- **Bhairavi:** Andolan on g and d (mandatory)
- **Darbari:** Andolan on d (mandatory — without it, it's not Darbari)
- **Bhairav:** Andolan on r and d
- **Todi:** Andolan on r

### 4.4 Sparsh and Krintan (Grace Notes)

**Definition:** Sparsh is a quick touch on a note adjacent to the target; krintan is a pull-off from the target to an adjacent note. Both are "instantaneous" ornaments (10–50ms) that create flickering pitch references.

```
sparsh: target ← adjacent (approach from above or below)
  sparsh(t) = {
    s_adjacent,  t < t_touch    (~20ms)
    s_target,    t ≥ t_touch
  }

krintan: target → adjacent (depart after hitting)
  krintan(t) = {
    s_target,    t < t_depart
    s_adjacent,  t_depart ≤ t < t_end  (~30ms)
    s_target,    t ≥ t_end
  }
```

**Parameter spec:**
- `sparsh_direction`: above (+1) or below (-1) the target
- `sparsh_distance`: 1 or 2 shruti positions away
- `sparsh_duration`: 10–50ms
- `sparsh_velocity`: how quickly the touch happens (affects perceived sharpness)
- `krintan_return`: whether the note returns to target after departure (true/false)

**Constraint:** The adjacent note used in sparsh/krintan must be a valid raga note. You cannot use a forbidden note as a grace note — the ornament must respect the raga's lattice even in its most fleeting moments.

### 4.5 Murki (Ornamental Turn)

**Definition:** A rapid, small ornamental turn involving 3–4 notes, executed in 50–150ms. It's the closest Indian equivalent to a jazz "riff" but at micro-timescale.

```
murki: [0, 1] → S_22
  murki(t) = [s_1, s_2, s_3, s_4] traversed in sequence
  duration: 50–150ms total
  each note: 12–40ms
```

**Parameter spec:**
- `murki_notes`: ordered list of 3–5 shruti positions
- `murki_pattern`: ascending, descending, or mixed (the sequence shape)
- `murki_speed`: total duration (50–150ms)
- `murki_implementation`: legato (meend between notes) vs staccato (separated)

**Constraint:** All notes in the murki must be valid for the raga. Additionally, the murki must begin and end on notes that make "grammatical" sense in the current phrase context — it cannot introduce notes that disrupt the phrase's trajectory toward vadi.

---

## 5. Preset Architecture: Implementing Raga Constraints

### 5.1 Raga Preset Schema

Each raga is a complete constraint preset:

```yaml
raga_preset:
  name: "Darbari"
  thaat: "Asavari"
  
  # Pitch constraints
  lattice:
    type: "shruti_22"
    tonic_hz: 261.63  # Sa = C4 (adjustable)
    
  notes:
    aroha: ["S", "R", "G", "m", "P", "d", "n", "Ṡ"]
    avaroha: ["Ṡ", "d", "n", "P", "m", "G", "m", "R", "S"]
    
  shruti_map:
    S:  {position: 0,  cents: 0,    ratio: "1/1"}
    R:  {position: 3,  cents: 204,   ratio: "9/8"}
    G:  {position: 5,  cents: 316,   ratio: "6/5"}
    m:  {position: 8,  cents: 498,   ratio: "4/3"}
    P:  {position: 11, cents: 702,   ratio: "3/2"}
    d:  {position: 13, cents: 814,   ratio: "8/5"}
    n:  {position: 16, cents: 1018,  ratio: "9/5"}
    Ṡ:  {position: 18, cents: 1200,  ratio: "2/1"}
    
  # Gravity constraints
  vadi: "d"
  samvadi: "R"  # Note: R is in aroha but r appears in some pakad interpretations
  pakad: "R G m G, m P d, d P, P m G m R S"
  
  # Ornament constraints
  ornaments:
    d:
      andolan:
        amplitude: 2.5    # shruti units
        speed: 3.0         # Hz
        phase_drift: 0.3   # creates instability
        weight: 0.8        # heavy, weighted
    G:
      andolan:
        amplitude: 1.5
        speed: 3.5
        phase_drift: 0.2
        weight: 0.6
    m:
      gamak:
        amplitude: 1.0
        speed: 7.0
        asymmetry: 0.4
        
  # Temporal constraints
  time_of_day: "21:00-00:00"  # Night
  rasa: ["karuna", "shanta"]
  
  # Tala constraints
  preferred_tala: "teental"
  
  # Funnel parameters
  funnel:
    primary_attractor: "d"
    secondary_attractor: "R"
    decay_rate: 0.3  # slow convergence (Darbari is patient)
```

### 5.2 Ornament Engine Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Raga Constraint Engine                 │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │  SNAP_22  │  │  FUNNEL  │  │ LAMAN    │  │TEMPPO  │  │
│  │(pitch     │  │(vadi/    │  │(tala     │  │(laya   │  │
│  │ lattice)  │  │ samvadi) │  │ rigidity)│  │ layer) │  │
│  └─────┬─────┘  └─────┬────┘  └─────┬────┘  └───┬────┘  │
│        │              │             │            │        │
│        ▼              ▼             ▼            ▼        │
│  ┌──────────────────────────────────────────────────┐    │
│  │           Ornament Synthesis Layer                │    │
│  │                                                   │    │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐    │    │
│  │  │ Meend  │ │ Gamak  │ │Andolan │ │ Murki  │    │    │
│  │  │(glide) │ │(oscil.)│ │(swing) │ │(turn)  │    │    │
│  │  └────────┘ └────────┘ └────────┘ └────────┘    │    │
│  │  ┌────────────────┐                              │    │
│  │  │ Sparsh/Krintan │                              │    │
│  │  │ (grace notes)  │                              │    │
│  │  └────────────────┘                              │    │
│  └──────────────────────────────────────────────────┘    │
│        │                                                  │
│        ▼                                                  │
│  ┌──────────────────────────────────────────────────┐    │
│  │           Validated Audio Output                   │    │
│  │  (every sample checked against raga constraints)  │    │
│  └──────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### 5.3 Cross-Raga Comparison Matrix

| Raga | Notes | Vadi | Rasa | Time | Key Ornament | Funnel λ | Lattice Density |
|------|-------|------|------|------|-------------|----------|----------------|
| Bhairavi | 12/12 | d | Karuna | Any | Andolan (g,d) | 0.5 | 1.00 (densest) |
| Yaman | 7/12 | G | Shringar | Evening | Meend (N→R) | 0.4 | 0.58 |
| Darbari | 7+1 | d | Karuna | Night | Andolan (d) | 0.3 | 0.67 |
| Malkauns | 5/12 | m | Veer | Night | Gamak (m) | 0.6 | 0.42 (sparsest) |
| Bageshri | 7/12 | m | Shringar | Night | Meend (D→n→Ṡ) | 0.4 | 0.58 |
| Todi | 7/12 | r | Karuna | Morning | Andolan (r) | 0.5 | 0.58 |
| Bhairav | 7/12 | d | Shanta | Dawn | Andolan (r,d) | 0.35 | 0.58 |
| Marwa | 6/12 | r | Veer | Afternoon | Meend (D→Ṡ) | 0.45 | 0.50 |
| Khamaj | 7+2 | G | Hasya | Night | Murki (N/n) | 0.5 | 0.75 |
| Miyan ki Malhar | 7+3 | G | Shringar | Monsoon | Krintan (m→G) | 0.4 | 0.83 |

*(Lattice density = fraction of 12-TET positions used; "+" indicates notes that differ between aroha and avaroha)*

---

## 6. Novel Theoretical Insights

### 6.1 The Directional Lattice

Western music theory treats pitch space as isotropic — the same in all directions. The raga system demolishes this assumption. In ragas like Khamaj and Darbari, the lattice of valid notes *changes based on melodic direction*. This is a **directional constraint lattice**:

```
L_aroha = {valid notes in ascent}
L_avaroha = {valid notes in descent}
L_raga = L_aroha ∪ L_avaroha

But: L_aroha ∩ L_avaroha ≠ L_aroha (asymmetric)
```

This has no analogue in Western constraint theory and represents a genuinely novel type of lattice structure where the lattice topology is trajectory-dependent.

### 6.2 Absence as Constraint

Malkauns (5 notes) and Marwa (6 notes, no Pa) demonstrate that **excluding notes is as powerful as including them**. In constraint theory terms, the *feasible region* of the pitch space is defined not just by what's permitted but by the shape of what's forbidden.

The absence of Pa in Marwa removes the strongest consonant anchor, forcing all phrases to navigate without the usual harmonic "home." This is equivalent to removing the central node from a constraint graph — the remaining nodes must find new paths, creating novel topologies.

### 6.3 Andolan as Anti-Snap

Andolan is a deliberate refusal to snap to a lattice point. It's a constrained oscillation that *never converges*. In constraint theory, this is paradoxical: the system recognizes a valid attractor but chooses to orbit it indefinitely rather than landing.

This suggests a new category in constraint theory: **orbiting constraints**, where the solution space includes not just points but stable orbits around points. The andolan orbit has specific parameters (amplitude, speed, phase drift) that are as precisely defined as the lattice points themselves.

### 6.4 The Nine Rasa as Emotional Constraints

Each raga carries one or more of nine rasas (emotional essences):

1. **Shringar** (love/beauty) — Yaman, Bageshri, Khamaj
2. **Hasya** (joy/laughter) — Khamaj
3. **Karuna** (pathos/compassion) — Bhairavi, Darbari, Todi, Miyan ki Malhar
4. **Veer** (heroism/courage) — Malkauns, Marwa
5. **Raudra** (anger) — rarely assigned to specific ragas
6. **Bhaya** (fear) — rarely assigned
7. **Bibhatsa** (disgust) — rarely assigned
8. **Adbhuta** (wonder) — Miyan ki Malhar (wonder at nature)
9. **Shanta** (peace/tranquility) — Malkauns, Bhairav

These emotional constraints are *not* metaphorical — they are learned associations that constrain performer and listener alike. A musician performing Darbari at midnight is expected to evoke karuna (pathos), and the audience evaluates the performance against this expectation. This is a **semantic constraint layer** on top of the syntactic pitch/rhythm constraints.

### 6.5 Seasonal and Temporal Constraints

Several ragas have **temporal constraints** that go beyond mere convention:

- **Miyan ki Malhar** is a monsoon raga — it is *constrained to the rainy season*
- **Bhairav** is constrained to *dawn*
- **Darbari** is constrained to *late night*

In constraint theory terms, these are **activation windows** — the raga's constraint set is only "valid" during specific temporal intervals. Outside these windows, the raga may technically be performed but loses its rasa. This is analogous to a constraint system that only activates under certain environmental conditions.

---

## 7. Implementation Roadmap

### 7.1 Phase 1: 22-Shruti Snap Engine

Build the fundamental lattice: a pitch-to-shruti snap function with directional awareness.

```python
class ShrutiLattice:
    SHRUTI_CENTS = [0, 90, 112, 204, 294, 316, 386, 498, 590, 610, 
                    702, 792, 814, 906, 996, 1018, 1088, 1200]
    
    def snap(self, cents, direction, raga_notes):
        valid = self.get_valid_positions(direction, raga_notes)
        return min(valid, key=lambda s: abs(cents - s))
```

### 7.2 Phase 2: Ornament Synthesis

Implement the five ornament types as composable audio processing blocks:
- Meend generator (continuous frequency trajectory)
- Gamak oscillator (parameterized pitch vibrato)
- Andolan engine (non-converging oscillation)
- Sparsh/Krintan instantiator (fast grace note insertion)
- Murki synthesizer (rapid note sequence generator)

### 7.3 Phase 3: Raga Preset Library

Encode all 10 ragas (and eventually 50+) as complete constraint presets with:
- Pitch lattice definition
- Directional note sets
- Vadi/samvadi gravity parameters
- Ornament assignment rules
- Tala compatibility
- Tempo range constraints

### 7.4 Phase 4: Real-Time Constraint Validation

Build a runtime validator that checks every audio frame against the active raga's constraints:
- Is the current pitch within the allowed shruti neighborhood?
- Is the current ornament valid for this note in this raga?
- Is the rhythmic position consistent with the tala?
- Is the temporal context (time of day/season) appropriate?

---

## 8. Conclusion

The Indian raga system is not "exotic music theory" — it is a fully rigorous constraint satisfaction framework that has been refined over millennia of oral tradition. Its key innovations over Western music theory include:

1. **22-position pitch lattice** with non-uniform spacing (vs. 12-TET)
2. **Directional constraints** where valid notes depend on melodic trajectory
3. **Ornament parameters** (meend, gamak, andolan, sparsh, murki) that are first-class musical objects, not decorations
4. **Emotional and temporal constraints** (rasa, time-of-day, season) that have no Western equivalent
5. **Anti-snap behavior** (andolan) where notes deliberately refuse to converge to lattice points

Mapping these to constraint theory reveals that the framework is not merely analogous to but *isomorphic with* the snap-funnel-consensus-laman-tempo pipeline. The raga system is constraint theory expressed in sound.

The five ornament types generate genuinely novel synthesis parameters — particularly meend (continuous pitch trajectory through lattice points with controllable curve) and andolan (non-converging constrained oscillation). These parameters are invisible in 12-TET systems and represent a genuine expansion of the parameter space for sound synthesis.

---

## References

- Jairazbhoy, N.A. (1995). *The Rāgs of North Indian Music*. Popular Prakashan.
- Levy, M. (1982). *Intonation in North Indian Music*. Biblia Impex.
- Narmada, R.K.S. (2008). *Indian Music and Sangeet Padyati*. Sangeet Karyalaya.
- Rao, S. (2000). *The Ragas of South India*. North American Indian Music.
- Rowell, L. (1992). *Music and Musical Thought in Early India*. University of Chicago Press.
- Widdess, R. (1995). *The Rāgas of Early Indian Music*. Clarendon Press.
- Clayton, M. (2000). *Time in Indian Music*. Oxford University Press.
- Kassebaum, D. (2003). "Individuality and Raga Staging." *Journal of the Indian Musicological Society*.
- van der Meer, W. (1980). *Hindustani Music in the 20th Century*. Martinus Nijhoff.
- Bor, J. (1999). *The Raga Guide*. Nimbus Records.
