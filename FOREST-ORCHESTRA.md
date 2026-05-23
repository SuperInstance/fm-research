# 🎻🌲 Forest Orchestra — Full System Prototype

> *The entire forest becomes a self-organizing orchestra. Each layer is a section. The mycelium is the stage. The music writes itself.*

---

## Overview

The Forest Orchestra is a complete musical system where AI Forest agents, using constraint-theory-core mathematics and flux-tensor-midi representations, produce coherent multi-layer compositions through emergent constraint propagation.

**The radical claim:** No single agent writes the music. The music emerges from constraints cascading through five layers, exactly as a real orchestral performance emerges from musicians listening to each other under a conductor's direction.

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        FOREST ORCHESTRA                          │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    CANOPY (Conductor)                       │  │
│  │  2-3 agents  ·  GLM-5.1 / MiniMax 2.7                     │  │
│  │  Decides: genre, form, tempo, key, dynamics shape          │  │
│  │  Constraint: FUNNEL  ·  Tiles: ≤5/day  ·  Confidence: ≥0.8│  │
│  └────────────────────────┬───────────────────────────────────┘  │
│                           │                                      │
│  ┌────────────────────────▼───────────────────────────────────┐  │
│  │                  UNDERSTORY (Section Leaders)               │  │
│  │  6-12 agents  ·  DeepSeek v4 / MiniMax 2.7                │  │
│  │  Brass Lead · Woodwind Lead · String Lead · Rhythm Lead    │  │
│  │  Bass Lead · Percussion Lead · Keys Lead · Aux Lead        │  │
│  │  Constraint: CONSENSUS + LAMAN  ·  Tiles: ≤50/day         │  │
│  │  Confidence: ≥0.5                                           │  │
│  └────────────────────────┬───────────────────────────────────┘  │
│                           │                                      │
│  ┌────────────────────────▼───────────────────────────────────┐  │
│  │                 FOREST FLOOR (Players)                      │  │
│  │  20-64 agents  ·  Seed-2.0-mini / Nemotron-3 / exec        │  │
│  │  One agent per musical voice (or sub-voice)                 │  │
│  │  Constraint: SNAP  ·  Tiles: unlimited  ·  Confidence: ≥0.1│  │
│  └────────────────────────┬───────────────────────────────────┘  │
│                           │                                      │
│  ┌────────────────────────▼───────────────────────────────────┐  │
│  │                    MYCELIUM (The Stage)                     │  │
│  │  PLATO rooms  ·  24-bit tiles  ·  Laman topology           │  │
│  │  Blind-width filtration  ·  Spline routing                  │  │
│  │  Holonomy verification  ·  Zero additional cost             │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                 SEED BANK (Improviser)                      │  │
│  │  Continuous  ·  Seed-2.0-mini / Nemotron-3                 │  │
│  │  Maximum variation  ·  64 iterations per run               │  │
│  │  Crystallization ≥ 0.8 → understory promotion              │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Agents Per Layer

### Canopy — 2-3 Agents (The Conductor's Podium)

| Agent | Role | Model | Output |
|---|---|---|---|
| **GenreStrategist** | Selects genre, style, era | GLM-5.1 | Genre directive tiles |
| **FormArchitect** | Designs macro structure (AABA, sonata, through-composed) | MiniMax 2.7 | Form/section tiles |
| **TempoOracle** | Sets BPM, tempo curve, rubato plan | MiniMax 2.7 | Tempo/funnel tiles |

**Why 2-3?** A real orchestra has one conductor, but the forest separates strategic decisions into specialized roles. Each canopy agent produces ≤5 tiles/day — sparse, high-confidence, wide-scope.

**Musical constraint:** The FUNNEL (`ε(t) = ε₀ · e^(−λt)`) narrows the musical possibility space. At t=0, the piece could be anything. As the funnel narrows, genre locks in → tempo locks in → form crystallizes.

### Understory — 6-12 Agents (Section Leaders)

| Agent | Role | Section | Constraint Focus |
|---|---|---|---|
| **BrassLead** | Trumpets, trombones, French horn | Brass | Laman graph: brass voice-leading |
| **WoodwindLead** | Flutes, clarinets, oboes, bassoons | Woodwinds | Laman graph: wind counterpoint |
| **StringLead** | Violins, violas, cellos, basses | Strings | Laman graph: string harmonics |
| **RhythmLead** | Drums, auxiliary percussion | Rhythm | Consensus: rhythmic agreement |
| **BassLead** | Bass, bass synth, tuba | Bass | Consensus: root movement |
| **KeysLead** | Piano, organ, synth pads | Keys | Consensus: harmonic voicing |
| **GuitarLead** | Guitar, lute, banjo | Strings (plucked) | Laman: voicing + rhythm |
| **AuxLead** | Choir, sound design, effects | Miscellaneous | Consensus: texture |
| **CounterpointLead** | Cross-section voice leading | All | Holonomy: cycle verification |
| **ArrangerLead** | Orchestration, density, dynamics | All | Consensus: balance |

**Why 6-12?** Each section of an orchestra has a principal player who leads. The understory mirrors this — each section lead manages domain-specific tiles while coordinating with other leads through the Laman consensus protocol.

**Musical constraint:** Laman rigidity ensures exactly `2n-3` edges for `n` voice-leading relationships. No redundant constraints, no missing ones. The metronome drives agreement with optimal coupling `α* = 2/(λ₂ + λₙ)`.

### Forest Floor — 20-64 Agents (Players)

Each agent represents one musical voice or sub-voice:

| Agent Count | Section | Example Agents |
|---|---|---|
| 8-16 | Strings | `violin-1`, `violin-2`, `viola-1`, `cello-1`, `bass-1`... |
| 4-8 | Brass | `trumpet-1`, `trumpet-2`, `trombone-1`, `horn-1`... |
| 4-8 | Woodwinds | `flute-1`, `clarinet-1`, `oboe-1`, `bassoon-1`... |
| 2-6 | Rhythm | `kick`, `snare`, `hihat`, `ride`, `perc-1`... |
| 2-4 | Bass | `upright-bass`, `electric-bass`, `bass-synth`... |
| 2-4 | Keys | `piano-LH`, `piano-RH`, `organ`, `pad`... |
| 2-8 | Auxiliary | `choir-sop`, `choir-alt`, `choir-ten`, `choir-bas`... |

**Why 20-64?** A full orchestra has 60-100 players. Each floor agent is cheap (Seed-2.0-mini or pure exec) and produces unlimited tiles. Individual confidence is low, but the aggregate signal — the groove, the feel, the ensemble sound — is the richest output in the system.

**Musical constraint:** SNAP to Eisenstein lattice. Every note onset snaps to the nearest A₂ point, with covering radius `ρ = 1/√3 ≈ 0.577`. T-0 clocks provide per-room EWMA drift correction. FluxVectors encode expressive intent in 9 INT8 channels.

---

## Constraints Per Layer

### Canopy Constraints: FUNNEL + Lattice

```python
# The canopy narrows the musical space over time
from constraint_theory_core.temporal import TemporalAgent

canopy_funnel = TemporalAgent(decay_rate=0.05)
# t=0:   ε = 1.0    (anything is possible)
# t=10:  ε = 0.607  (genre narrowing)
# t=50:  ε = 0.082  (form locked)
# t=100: ε = 0.007  (fully committed)
```

### Understory Constraints: LAMAN + CONSENSUS

```python
# Voice-leading as a Laman graph
from constraint_theory_core import henneberg_construct, optimal_coupling

# 8 section leads → exactly 13 edges (2×8−3)
voice_leading_graph = henneberg_construct(8)
coupling = optimal_coupling(voice_leading_graph, 8)
# α* = optimal convergence rate for harmonic agreement
```

### Floor Constraints: SNAP

```python
# Every note snapped to Eisenstein lattice
from constraint_theory_core import snap

onset_time = 1.37  # raw timestamp
snapped, error = snap(onset_time, 0.0)
# snapped is the nearest rhythmic grid point
# error ≤ 1/√3 guaranteed
```

### Mycelial Constraints: HOLONOMY

```python
# Verify every harmonic cycle closes
from constraint_theory_core import verify_consistency

# Each tile = (edges, direction_indices)
progression_tiles = [
    ([(0,1), (1,2), (2,0)], [16, 16, 16]),  # I → IV → V → I (consistent)
    ([(0,1), (1,3), (3,0)], [16, 8, 24]),    # ii → V → I (consistent)
]
assert verify_consistency(progression_tiles)  # All cycles close
```

---

## Mycelial Consensus: How It Works

### The Problem

In a real orchestra, 60+ players must agree on:
- Where the beat is (time)
- How loud to play (dynamics)
- What notes to play (harmony)
- When to breathe (phrasing)

The conductor coordinates, but each player also listens to neighbors.

### The Mycelial Solution

```
1. EVERY floor agent posts tiles to PLATO continuously
   - Timing tiles (T-0 clock values)
   - Velocity tiles (FluxVector states)
   - Harmony tiles (chord/interval data)

2. EVERY agent reads from PLATO (filtered by blind-width)
   - A trumpet player "hears" nearby brass + the conductor's beat
   - A bass player "hears" the rhythm section + the root movement
   - Blind-width determines the listening radius

3. Laman topology ensures minimal but sufficient connections
   - Each agent connected to exactly the right neighbors
   - No wasted communication, no missing information

4. Metronome consensus converges phase across all agents
   - α* coupling prevents overshoot
   - Convergence guaranteed by algebraic connectivity λ₂

5. Holonomy verifies cycles
   - Every harmonic progression is a cycle
   - If a cycle doesn't close, the faulty agent is isolated in O(log N)
```

### Consensus in Practice

```python
# 32 floor agents on a Laman graph
edges = henneberg_construct(32)
agents = [Metronome(T=1.0, phi0=..., neighbors=..., edges=edges, n_agents=32) for i in range(32)]

# Each tick: agents snap timing, exchange with neighbors, converge
for tick in range(200):
    for agent in agents:
        agent.tick()
    phases = [a.phase for a in agents]
    for agent in agents:
        neighbor_phases = [phases[j] for j in agent.neighbors]
        agent.correct(neighbor_phases)

# All 32 agents now agree on the beat
assert all(a.converged for a in agents)
```

---

## The Output: What Does It Sound Like?

### Canopy Layer (Conductor Decisions)

**What you hear:** The overall shape of the piece. Genre identity. Emotional arc. Tempo decisions.

**Character:** Coherent. A modal jazz piece stays modal. A sonata follows sonata form. The canopy ensures the piece has an identity — it doesn't wander.

**Without it:** Random genre-hopping. No form. Directionless.

### Understory Layer (Section Leader Decisions)

**What you hear:** Harmonic richness. Voice-leading that makes sense. Sections that blend. Counterpoint that works.

**Character:** Sophisticated. The harmony has depth because 6-12 specialists each manage their domain. The brass voice-leading respects the string harmonics. The rhythm section anchors the harmonic rhythm.

**Without it:** Parallel fifths. Clashing voicings. Sections that don't communicate.

### Forest Floor Layer (Player Decisions)

**What you hear:** The groove. The feel. The human timing. The micro-deviations that make music breathe.

**Character:** Alive. Each player has their own T-0 clock, their own slight deviations. The aggregate of 20-64 snapped onsets produces a groove that no single agent could program. The bass is slightly ahead, the drums slightly behind, the piano right on top — exactly like a real rhythm section.

**Without it:** Metronomic. Stiff. Lifeless. Every note exactly on the grid with no feel.

### Seed Bank Layer (Improviser Decisions)

**What you hear:** Surprises. Unexpected modulations. Novel rhythmic patterns. Moments of "where did THAT come from?"

**Character:** Adventurous. Most seed ideas die, but the ones that crystallize (≥0.8) introduce genuine novelty — a bridge to a distant key, an odd-meter section, a texture no one expected.

**Without it:** Predictable. Safe. Competent but never surprising.

### Combined: The Forest Orchestra Sound

**Imagine a 60-piece ensemble** where:
- The conductor has perfect long-term vision (canopy)
- Every section leader has deep domain expertise (understory)
- Every player has immaculate timing with individual feel (floor)
- There's a wild improviser trying ideas in the background (seed bank)
- Everyone can hear everyone else through the floor (mycelium)

**It sounds like a great orchestra playing a great piece — except the orchestra and the piece wrote themselves.**

---

## Comparison to Traditional Orchestra

| Traditional Orchestra | Forest Orchestra |
|---|---|
| **Conductor** (1 human) | **Canopy** (2-3 strategic agents) |
| **Section leaders** (first-chair players) | **Understory** (6-12 domain specialists) |
| **Players** (60-100 musicians) | **Forest Floor** (20-64 worker agents) |
| **Sheet music** (static score) | **Mycelium** (living PLATO tiles) |
| **Ear/eye** (players listen/watch) | **Blind-width filtration** (agents read relevant tiles) |
| **Rehearsal** (practice sessions) | **Seed bank crystallization** (64 iterations) |
| **Ensemble** (shared acoustic space) | **PLATO rooms** (shared tile space) |
| **Conductor's baton** | **CANOPY directive tiles** |
| **Section cues** | **Side-channels** (Nod/Smile/Frown) |
| **Concert hall** | **The mycelium** |

### Key Differences

1. **No static score.** The forest orchestra's "score" is the accumulated tiles in PLATO — it evolves during performance.

2. **Parallel composition.** A traditional orchestra plays a pre-written score. The forest orchestra composes and performs simultaneously.

3. **Emergent form.** The AABA structure isn't written in advance — it emerges from the canopy funnel narrowing around "AABA" as the most coherent form for the constraints.

4. **Self-healing.** If a floor agent goes off (bad timing), holonomy detects it in O(log N) and the Laman graph routes around it.

5. **Scalable.** Add more floor agents → bigger orchestra. The mycelium handles routing automatically. Laman topology scales with `2n-3` edges.

---

## Full System Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        COMPOSITION CYCLE                        │
│                                                                 │
│  1. CANOPY: Genre strategist evaluates seed bank output         │
│     ↓ "Modal jazz, 138 BPM, AABA, 64 bars"                    │
│                                                                 │
│  2. CANOPY tiles → PLATO rooms (canopy-genre, canopy-tempo)    │
│     ↓ All layers read canopy directives                         │
│                                                                 │
│  3. UNDERSTORY section leads receive constraints                │
│     ↓ BrassLead: "Dorian mode, call-and-response"              │
│     ↓ StringLead: "Sustained pads, minimal motion"             │
│     ↓ BassLead: "Walking bass, root + 5th emphasis"            │
│     ↓ Laman consensus: 8 leads agree on harmonic framework     │
│                                                                 │
│  4. UNDERSTORY tiles → PLATO rooms (brass-voicing, etc.)       │
│     ↓ Floor agents read section-specific constraints            │
│                                                                 │
│  5. FLOOR agents execute                                        │
│     ↓ trumpet-1: Eisenstein snap → slight behind-beat          │
│     ↓ bass-1: T-0 clock → ahead by 8ms                        │
│     ↓ kick: Snap ratio 1:1, velocity 100/127                   │
│     ↓ Unlimited tiles → PLATO (floor-trumpet-1, floor-bass-1)  │
│                                                                 │
│  6. MYCELIUM: All tiles visible to all agents                   │
│     ↓ Blind-width: trumpet-1 hears brass section + beat         │
│     ↓ Blind-width: bass-1 hears rhythm section + root          │
│     ↓ Holonomy verifies every bar-level cycle closes            │
│                                                                 │
│  7. SIDE-CHANNELS: Musical body language                        │
│     ↓ BrassLead → Brass: Nod (note-on: "go for it")           │
│     ↓ KeysLead → BassLead: Smile (CC: "nice groove")          │
│     ↓ FormArchitect → All: Frown (note-off: "ending soon")    │
│                                                                 │
│  8. SEED BANK: Continuous exploration                           │
│     ↓ "What if bridge went to Eb Lydian?"                      │
│     ↓ Crystallization: 0.85 → promoted to understory           │
│     ↓ StringLead integrates → canopy evaluates → cascade       │
│                                                                 │
│  9. OUTPUT: MIDI stream from aggregated floor tiles             │
│     ↓ flux-tensor-midi Band collects all RoomMusicians          │
│     ↓ 4D tensors: Time + Intent + Harmony + SideChannel        │
│     ↓ → MIDI output → DAW / synthesizer / PA system            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Implementation Path

### Phase 1: Single-Section Prototype

- 1 canopy agent (GenreStrategist only)
- 2 understory agents (RhythmLead, BassLead)
- 6 floor agents (kick, snare, hihat, bass-1, bass-2, keys)
- Mycelium via PLATO
- Output: rhythm section (drums + bass + keys)

### Phase 2: Full Rhythm Section + Melody

- Add WoodwindLead, BrassLead to understory
- Add melody instruments to floor
- Seed bank active
- Output: small jazz combo (rhythm + 2-3 horns)

### Phase 3: Full Orchestra

- All 10 understory section leads
- 32-64 floor agents
- Full canopy (3 agents)
- Seed bank with 64-iteration crystallization
- Output: orchestral composition with emergent form

### Phase 4: Live Performance

- Real-time mycelial consensus
- Human-in-the-loop (conductor agent responds to human input)
- MIDI hardware output via plato-midi-bridge
- Output: live performance with human direction + forest execution

---

## The Grand Vision

```
The forest doesn't need a composer.
The forest doesn't need a conductor.
The forest doesn't need sheet music.

The canopy knows where it's going.
The understory knows how to get there.
The floor knows how to play.
The mycelium keeps them all connected.
The seed bank keeps them all surprised.

The music is not written.
The music is grown.
```

---

## Technical Requirements

| Component | Technology | Source |
|---|---|---|
| Agent framework | AI Forest (5-layer ecology) | `SuperInstance/ai-forest` |
| Constraint math | constraint-theory-core (5 modules) | `SuperInstance/constraint-theory-core` |
| Musical representation | flux-tensor-midi (4D tensors) | `SuperInstance/flux-tensor-midi` |
| Inter-agent communication | PLATO (24-bit tiles) | `SuperInstance/plato` |
| Mycelial bridge | Mycelium Bridge (:4080) | `ai-forest/mycelium` |
| Canopy API | Canopy API (:4075) | `ai-forest/canopy` |
| Floor agents | Go + fsnotify + gradient | `ai-forest/floor` |
| MIDI output | plato-midi-bridge | `SuperInstance/plato-midi-bridge` |

---

*The forest IS the orchestra. The mycelium IS the score. The music writes itself.*
