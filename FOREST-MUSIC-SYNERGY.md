# 🌲🎵 Forest-Music Synergy — Architecture Document

> *A forest IS an orchestra. Every layer produces a musical voice. The mycelial network is the consensus protocol that keeps them in time.*

---

## The Core Insight

The AI Forest layered agent ecology maps directly onto musical constraint systems. A forest is an ecosystem of constraint systems — each layer constrains different aspects of a musical performance, and the mycelial PLATO network provides the consensus protocol that keeps all layers coherent.

| Forest Layer | Musical Role | Constraint Type | Timescale |
|---|---|---|---|
| **Canopy** | Conductor / Composer | FUNNEL (deadband narrowing) | Hours–days |
| **Understory** | Section leaders / Arrangers | CONSENSUS (Laman metronome) | Minutes–hours |
| **Forest Floor** | Players / Performers | SNAP (Eisenstein quantization) | Seconds–minutes |
| **Mycelium** | The stage / the shared pulse | PLATO tile routing | Instantaneous |
| **Seed Bank** | Improviser / Explorer | TEMPO (tension loop) | Continuous |

---

## Architecture: Forest Layers → Constraint Layers → Musical Output

```
                        ┌─────────────────────────────┐
                        │        CANOPY STRATEGIST     │
                        │   Genre · Macro-form · BPM  │
                        │   FUNNEL constraint: ε(t)    │
                        │   "What are we playing?"     │
                        └──────────┬──────────────────┘
                                   │ High-confidence tiles
                                   │ (genre, tempo, key, form)
                                   ▼
                 ┌─────────────────────────────────────┐
                 │      UNDERSTORY SPECIALISTS          │
                 │  Voice leading · Harmony · Counterpt │
                 │  CONSENSUS + LAMAN constraints       │
                 │  "How do the voices fit together?"   │
                 └──────────┬──────────────────────────┘
                            │ Domain tiles (chord voicings,
                            │ voice-leading rules, progressions)
                            ▼
              ┌──────────────────────────────────────────┐
              │         FOREST FLOOR WORKERS              │
              │   Micro-timing · Groove · Velocity       │
              │   SNAP constraint: Eisenstein lattice     │
              │   "When exactly does each note land?"     │
              └──────────┬───────────────────────────────┘
                         │ High-frequency tiles
                         │ (timing, velocity, articulation)
                         ▼
           ┌──────────────────────────────────────────────┐
           │          MYCELIAL PLATO NETWORK              │
           │   24-bit tiles · Real-time consensus         │
           │   Laman rigidity · Holonomy verification     │
           │   "Every tile from every layer, everywhere"  │
           └──────────────────────────────────────────────┘
```

---

## Layer 1: Canopy Strategists — Macro-Musical Direction

### Constraint: FUNNEL (Temporal Deadband)

The canopy uses the **deadband funnel** from constraint-theory-core:

```
ε(t) = ε₀ · e^(−λt)
```

The canopy narrows the musical decision space over time. Early in composition, everything is possible (wide funnel). As the piece takes shape, the deadband narrows — genre locks in, tempo solidifies, key centers emerge.

### What the Canopy Decides

| Decision | Constraint Mechanism | Tile Output |
|---|---|---|
| **Genre** | Initial wide funnel → converges | `{genre: "jazz", confidence: 0.85}` |
| **Tempo/BPM** | FUNNEL narrowing around target | `{bpm: 138, epsilon: 2.0}` |
| **Macro-form** | ABA, through-composed, sonata | `{form: "AABA", sections: 4}` |
| **Key center** | Lattice snap to pitch classes | `{key: "Bb", mode: "mixolydian"}` |
| **Duration** | Strategic horizon (bars, minutes) | `{duration_bars: 64}` |

### Canopy → Mycelium

Canopy tiles are sparse (≤5/day) but high-confidence (≥0.8). They propagate through PLATO rooms like `canopy-genre`, `canopy-form`, `canopy-tempo`. These become **hard constraints** for lower layers — the understory cannot violate a canopy directive once crystallized.

---

## Layer 2: Understory Specialists — Voice Leading and Harmony

### Constraint: CONSENSUS (Laman Metronome)

The understory uses **Laman rigidity** and the **metronome consensus protocol**:

- The harmonic graph is a Laman graph: exactly `2n-3` edges for `n` voices
- Each voice is a node; edges represent voice-leading constraints
- The metronome drives distributed consensus: `α* = 2/(λ₂ + λₙ)`
- Holonomy verifies that every harmonic cycle closes

### What the Understory Does

| Function | Constraint | Tile Output |
|---|---|---|
| **Voice leading** | Laman graph edges = allowed motions | `{voices: 4, edges: 5, motion: "contrary"}` |
| **Harmony** | Consensus on chord quality | `{chord: "m7", root: "F#", inversion: 2}` |
| **Counterpoint** | Species rules as Laman constraints | `{species: 3, dissonance: "passing"}` |
| **Progression** | Holonomy-verified cycle | `{cycle: "ii-V-I", holonomy: 0}` |
| **Arrangement** | Domain-specific tile clusters | `{instrument: "brass", role: "sustained"}` |

### Understory ↔ Canopy

The understory receives canopy directives as constraints. It produces dense domain tiles (≤50/day, confidence ≥0.5) that flow back up as **evidence** — "the voice leading in bar 24 wants a key change" can bubble up to the canopy for strategic evaluation.

### Understory ↔ Forest Floor

Implementation tiles flow down: specific MIDI instructions, FluxVector states, timing parameters. The understory says *what to play*; the floor decides *exactly when and how hard*.

---

## Layer 3: Forest Floor Workers — Micro-Timing and Groove

### Constraint: SNAP (Eisenstein Lattice)

The floor uses **Eisenstein lattice quantization** from constraint-theory-core:

- Every note onset snaps to the nearest A₂ lattice point
- Covering radius `ρ = 1/√3 ≈ 0.577` guarantees optimal rhythmic packing
- Snap ratios encode rhythmic roles: unison (1:1), halftime (2:1), triplet (3:2)
- INT8 saturation in FluxVectors gives zero-allocation velocity encoding

### What the Floor Produces

| Output | Mechanism | Tile Type |
|---|---|---|
| **Micro-timing** | Eisenstein snap of timestamps | `{snap_point: (3, -1), error: 0.082}` |
| **Groove** | Aggregate of snapped deviations | `{groove_pattern: "swing", depth: 0.6}` |
| **Velocity** | FluxVector INT8 channels | `{arousal: 80, valence: 64, dominance: 48}` |
| **Articulation** | Side-channel Nod/Smile/Frown | `{articulation: "legato", confidence: 0.7}` |
| **Ensemble sync** | T-0 clock EWMA correction | `{clock_drift: 0.003, ewma: 120.01}` |

### Floor → Mycelium

Unlimited tiles per day. Individual confidence can be as low as 0.1. But **aggregate** floor tiles produce the richest musical signal — the groove, the feel, the human timing that makes music breathe.

---

## Layer 4: Mycelial Network — The Consensus Substrate

### PLATO as Musical Consensus

The mycelium is the **shared pulse** of the forest orchestra:

```
Every tile from every layer → PLATO room
Every agent reads from PLATO (filtered by blind-width)
Blind-width at each layer determines what it "hears"
```

### Musical Properties

| Mycelium Feature | Musical Meaning |
|---|---|
| **Object permanence** | Musical decisions never vanish — a groove from bar 4 persists |
| **Spline routing** | Tiles flow between instruments via learned dependencies |
| **24-bit tiles** | Compact musical messages (timing, velocity, harmony) |
| **Blind-width filtration** | Each player hears only what's relevant to their part |
| **Bit allocation** | Dynamic precision per connection (more bits for rhythm, fewer for color) |

### The Mycelium IS the Conductor's Score

In a traditional orchestra, the conductor reads a score. In the forest orchestra, the mycelium IS the score — a living, evolving document of every musical decision, accessible to every agent at every layer.

---

## Layer 5: Seed Bank — Musical Exploration and Novelty

### Constraint: TEMPO (Tension Loop)

The seed bank is the **improviser** of the forest:

- Maximum variation, minimum cost (Seed-2.0-mini, Nemotron-3)
- 64 iterations per seed run (dodecet convention)
- Crystallization score ≥ 0.8 to graduate to understory
- The tension loop proposes and analyzes — like a musician trying ideas

### What the Seed Bank Explores

- Novel rhythmic patterns
- Unusual harmonic progressions
- Genre-crossing combinations
- Micro-timing innovations
- Timbral experiments

Most seeds die. Some germinate into understory domain tiles. A rare few reach the canopy and change the entire direction of the piece.

---

## Emergent Behavior: The Cascade

The magic of the forest-music synergy is **cascading constraint resolution**:

```
1. CANOPY decides: "We're playing modal jazz, 138 BPM, AABA form"
   → Funnels to understory via PLATO

2. UNDERSTORY specializes:
   → "Voice leading: parallel 4ths in the horn section"
   → "Harmony: Dorian mode on the A sections, Lydian on B"
   → "Counterpoint: call-and-response between brass and reeds"
   → Laman consensus ensures voices don't conflict

3. FLOOR executes:
   → "Trumpet: slight behind-beat on beat 3 (Eisenstein snap offset)"
   → "Bass: ahead of beat by 12ms (groove pattern)"
   → "Drums: swing ratio 3:2 with varying depth per bar"
   → Each timestamp snapped to Eisenstein lattice

4. MYCELIUM connects:
   → Every timing tile visible to every player
   → Side-channels (Nod/Smile/Frown) flow freely
   → T-0 clocks synchronize across rooms

5. SEED BANK explores:
   → "What if the bridge went to Db instead of G?"
   → Crystallization score 0.9 → escalated to understory
   → Understory integrates → cascade continues
```

The result: **coherent multi-layer composition** that emerges from constraint propagation, not top-down programming.

---

## Mapping to flux-tensor-midi

The synergy is not theoretical — it maps directly to existing code:

| Forest Concept | flux-tensor-midi Implementation |
|---|---|
| Canopy strategist | `Band` conductor, sets BPM, assigns roles |
| Understory specialist | `RoomMusician` with harmony/Jaccard awareness |
| Forest floor worker | `EisensteinSnap` + `TZeroClock` per room |
| Mycelial network | PLATO rooms as `RoomMusician` connections |
| Seed bank | Novel `FluxVector` states from tension loops |
| Side-channels | `Nod`, `Smile`, `Frown` between rooms |
| 24-bit tiles | `FluxVector` INT8 saturation (9 channels × 8 bits = 72 bits packed) |

---

## Five Constraint Types → Five Musical Functions

| Constraint Type | Module | Forest Layer | Musical Function |
|---|---|---|---|
| **SNAP** | `lattice` | Forest Floor | Rhythmic quantization, micro-timing |
| **FUNNEL** | `temporal` | Canopy | Genre/tempo convergence over time |
| **LAMAN** | `rigidity` | Understory | Voice-leading graph, minimal edges |
| **CONSENSUS** | `metronome` | Understory | Harmonic agreement between voices |
| **HOLONOMY** | `holonomy` | Mycelium | Cycle verification, progression coherence |

The forest IS the constraint system. The music IS the output.

---

## Why This Works

1. **Layered constraints are how music works.** A tempo decision (canopy) constrains harmony (understory) which constrains timing (floor). This is not a metaphor — it's the physics of ensemble performance.

2. **The mycelium solves the conductor problem.** In a real orchestra, the conductor coordinates. In the forest, the mycelium does it for free — every agent sees every tile, filtered by relevance.

3. **Emergence from constraint propagation.** No single layer writes the music. The music emerges from constraints cascading through layers, just as a real performance emerges from musicians listening to each other.

4. **The seed bank is the improviser.** Jazz musicians try things. Most don't work. The ones that do change the direction of the performance. The seed bank does exactly this, mathematically.

5. **24-bit tiles are compact enough for real-time music.** At MIDI resolution, a 24-bit tile can encode timing, velocity, and channel information in a single atomic message. The mycelium routes these faster than any conductor could gesture.

---

*The canopy doesn't play the notes. The roots don't decide the genre. But together, the forest makes music.*
