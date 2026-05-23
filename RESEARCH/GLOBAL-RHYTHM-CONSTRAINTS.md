# Global Rhythm Traditions Mapped to Constraint Theory: Jazz, Afro-Cuban, Brazilian & Latin Jazz

**Forgemaster ⚒️ | 2026-05-23 | v1**

---

## Abstract

Rhythm is the oldest constraint satisfaction system in human music. Across jazz, Afro-Cuban, Brazilian, and Latin jazz fusion traditions, musicians navigate temporal lattices of extraordinary complexity — swing ratios that bend a grid, clave patterns that lock an entire ensemble into a single timeline, and polymetric layers that maintain independence while converging on shared downbeats. This paper maps five foundational constraint theory primitives — SNAP, FUNNEL, CONSENSUS, LAMAN, and TEMPO — onto the structural mechanics of global rhythm traditions, tracing the lineage from West African bell patterns through Cuban clave to Brazilian samba layers and jazz swing feel. We propose six novel rhythmic parameters derived from this mapping and present fifteen rhythmic presets encoding specific traditions as constraint satisfaction profiles. The central argument: every rhythmic tradition is a constraint engine with its own SNAP grid, FUNNEL gravity, CONSENSUS rules, LAMAN rigidity, and TEMPO pocket — and understanding them as such enables both deeper performance practice and systematic computational modeling.

---

## 1. Jazz Rhythm as Temporal Constraint System

### 1.1 The Swing Ratio Continuum

Jazz rhythm is defined by one parameter above all others: the **swing ratio** — the proportional relationship between the long and short portions of a subdivided beat. In a binary (straight) subdivision, the ratio is 1:1. In a ternary (triplet) subdivision, the ratio is 2:1. But jazz does not occupy a single point on this continuum; it **inhabits the entire spectrum**.

The swing ratio can be expressed as a continuous parameter from 0.50 to 0.80:

- **0.50** — Straight eighths (1:1). Grid-locked, mechanical. Post-bop fusion, some ECM jazz.
- **0.57** — Slight lilt. Barely perceptible swing. Cool jazz (Miles Davis *Birth of the Cool*).
- **0.67** — Triplet feel (2:1). The canonical jazz swing. Count Basie, Oscar Peterson.
- **0.70–0.73** — Hard bop swing. Deeper in the pocket. Art Blakey, Lee Morgan.
- **0.75** — Dotted feel (3:1). Heavy, laid-back. Some Dexter Gordon, Paul Gonsalves.
- **0.80** — Double-dotted. Almost 4:1. Deep blues feel, some early New Orleans.

In constraint theory terms, **SNAP** governs the subdivision grid. A swing ratio of 0.67 snaps to a triplet grid; 0.50 snaps to a straight grid. But jazz musicians routinely violate their own grid, playing between snap points — a deliberate constraint violation that creates the "human feel." Studies by Friberg and Sundström (2002) showed that professional jazz musicians vary swing ratio ±0.05 within a single performance, and that the ratio tends to **compress toward 0.55 at faster tempos** and **expand toward 0.75 at slower tempos**.

This is not imprecision. It is a **dynamic SNAP parameter** that adjusts with tempo, creating a living grid rather than a fixed one. The constraint is not "swing at exactly 2:1" but "swing at the ratio that creates maximum pocket feel at this tempo."

### 1.2 Behind/Ahead of the Beat as Funnel Offset

The beat in jazz is not a point but a **region** — a gravitational well described by FUNNEL. The downbeat exerts pull on all surrounding events, but musicians deliberately position themselves at different offsets from the center:

- **Behind the beat** (positive offset): Creates laid-back, heavy feel. Lester Young, Dexter Gordon, Miles Davis (second quintet). The note arrives 20-50ms after the theoretical grid point. The FUNNEL gravity is felt but resisted.

- **On the beat** (zero offset): Locked, driving. Freddie Hubbard, Woody Shaw. The note arrives at the grid point. Maximum FUNNEL alignment.

- **Ahead of the beat** (negative offset): Creates urgency, forward motion. Thelonious Monk, Charles Mingus bass lines. The note arrives 15-30ms before the grid point. The FUNNEL is anticipated rather than followed.

The critical insight: **the beat offset is an ensemble-wide parameter, not an individual one**. A rhythm section achieves "the pocket" when all members agree on a shared offset. The bassist and drummer must match offsets; the pianist/guitarist comping must align with the bass-drum pocket; the horn soloist plays against this collective position. This is **FUNNEL with consensus** — the gravity center is not the metronomic downbeat but the ensemble's agreed-upon pocket.

When the pocket is achieved, the FUNNEL parameter effectively **widens** — the acceptable region around the center grows because the collective agreement creates a felt beat that doesn't require metronomic precision. This is why a great jazz rhythm section can sound incredibly tight while individual timing measurements show considerable variance.

### 1.3 Syncopation as Deliberate Constraint Violation

Syncopation in jazz is the **controlled violation of the SNAP grid** — placing events on off-beat grid points or between grid points entirely. The constraint system allows violations, but they must be:

1. **Predictable** — The listener can infer the underlying grid despite the violation
2. **Recoverable** — The music returns to grid alignment within a bounded number of beats
3. **Hierarchical** — Syncopations at the subdivision level are more freely permitted than at the beat level; beat-level syncopations are more freely permitted than bar-level syncopations

This creates a **syncopation budget** — a measure of how many and how severe constraint violations are permitted per unit of musical time. Thelonious Monk operates at a high syncopation budget; Count Basie operates at a low one. The budget is not random but stylistically determined: bebop has a higher budget than swing, free jazz has a higher budget than bebop, and fusion varies widely.

The constraint mapping: syncopation budget = the number of beats per measure where events are permitted to fall off the SNAP grid. A budget of 0 means strict grid adherence (march, ragtime early period). A budget of 2-3 is typical mainstream jazz. A budget of 4-6 is advanced bebop. A budget exceeding 6 approaches free playing, where the grid itself becomes ambiguous.

### 1.4 Ride Cymbal Patterns as Temporal Lattice

The jazz ride cymbal pattern is a **temporal lattice** — a repeating rhythmic framework that defines the SNAP grid for the entire ensemble. The standard pattern in 4/4 is:

```
1  2&  3  4&
X  X   X  X . X
```

Where the first four strokes fall on beats 1, 2&, 3, and the last two form a pickup into beat 1 of the next bar. The ride pattern creates a lattice of **five primary snap points** per bar, with the crucial characteristic that the second and fifth points fall on upbeats — creating inherent syncopation within the lattice itself.

Different ride patterns select different SNAP grids:

- **Standard swing:** Triplet grid, emphasis on beat 1 and the "and" of beat 2
- **Bebop ride:** Adds the "let" of beat 2 (the third triplet), creating a denser six-point lattice
- **Half-time feel:** Beat 1, beat 3, with the characteristic backbeat on beat 3. Lattice points: 4 per bar at half density
- **Elvin Jones ride:** Irregular accents superimposed on the standard pattern, creating the illusion of metric displacement while maintaining the underlying lattice

The ride cymbal is the **LAMAN element** of jazz — the pattern that changes least over the course of a performance. While the bass walks, the piano comps, and the soloist explores, the ride cymbal maintains its lattice with minimal variation. This provides the rigid backbone against which all other constraint violations are measured.

### 1.5 Triplet Feel vs. Straight Feel as Snap Grid Selection

The choice between triplet feel and straight feel is fundamentally a **SNAP grid selection**:

- **Triplet grid (SNAP = 0.67):** Each beat divides into three equal parts. The grid points are at 0.0, 0.33, 0.67 of each beat. Jazz walking bass operates primarily on the first and third points (beat and second triplet). Melodic lines use all three.

- **Straight grid (SNAP = 0.50):** Each beat divides into two equal parts. Grid points at 0.0, 0.50. Latin jazz, fusion, and post-bop often employ straight feel, creating a different constraint space.

- **Sixteenth-note grid (SNAP = 0.25):** Each beat divides into four parts. Used in funk, fusion, and some modern jazz. Creates a denser constraint space with more possible syncopation points.

The grid selection determines the **available syncopation space**. A triplet grid in 4/4 offers 12 snap points per bar; a straight grid offers 8; a sixteenth-note grid offers 16. The density of available snap points directly affects the syncopation budget — more points means more opportunities for constraint violation, and correspondingly different aesthetic results.

Modern jazz musicians frequently **switch grids mid-phrase** — playing a passage in triplet feel and then shifting to straight feel, or interpolating quintuplet subdivisions. This is a grid-switching operation in constraint terms, analogous to changing the SNAP resolution on the fly.

### 1.6 Elvin Jones: Metric Displacement as Constraint Redirection

Elvin Jones's drumming with the John Coltrane Classic Quartet (1961-1966) represents perhaps the most sophisticated application of **metric displacement** in jazz history. The technique involves playing patterns that imply a different meter than the actual one — most characteristically, playing in **3 over 4/4**.

In constraint terms, Jones creates a **secondary SNAP grid** in 3/4 superimposed over the primary 4/4 grid. The secondary grid has a different periodicity (3 beats vs. 4 beats), so the two grids go in and out of phase every 12 beats (LCM of 3 and 4). This creates a cycle of:

1. **Alignment** (grids coincide) → strong downbeat feel
2. **Divergence** (grids separate) → polyrhythmic tension
3. **Re-alignment** (grids converge) → resolution

Jones does not merely superimpose 3 over 4 — he **fluidly redirects** the listener's attention between the two grids, making the primary grid recede and the secondary grid emerge, then reversing the process. This is constraint **redirection**: the FUNNEL gravity temporarily shifts from the primary grid's downbeat to the secondary grid's downbeat, creating the sensation that the entire rhythmic field has shifted.

The constraint load on the other musicians is immense. The bassist (Jimmy Garrison or later players) must maintain the 4/4 walking pattern while the drums create a 3/4 illusion. The pianist must decide whether to follow the drums or the bass. The soloist (Coltrane) navigates both grids simultaneously, using the tension between them as fuel for motivic development.

### 1.7 Max Roach: Melodic Drumming as Pitch-Rhythm Unification

Max Roach's approach to drumming represents a different but equally revolutionary constraint architecture: **pitch-rhythm unification**. In his seminal *We Insist! Freedom Now Suite* (1960) and throughout his career, Roach treated the drum kit as a melodic instrument, creating phrases where pitch contour and rhythmic contour are coupled constraints.

The drum kit presents a discrete pitch space:
- Bass drum → low fundamental
- Floor tom → mid-low
- Rack toms → mid to mid-high
- Snare (head) → mid-high with resonant component
- Snare (rim) → high, sharp
- Hi-hat (closed) → high, metallic
- Ride cymbal bell → highest, most sustained

Roach's melodic phrases assign **pitch targets** to rhythmic events, creating a dual constraint: each phrase must satisfy both rhythmic placement AND pitch contour requirements. This is directly analogous to the Yoruba talking drum tradition (see West African Polyrhythm Constraints), where pitch and rhythm form coupled channels.

In constraint terms, Roach's approach adds a **secondary SNAP grid** — a pitch grid superimposed on the temporal grid. The pitch grid is less rigid than the temporal grid (it's more of a contour constraint than a point constraint), but it adds significant complexity to the constraint satisfaction problem. A phrase must satisfy: correct timing (temporal SNAP), correct accent pattern (dynamic constraint), AND correct pitch motion (pitch SNAP).

---

## 2. Afro-Cuban Rhythm: Clave as Universal Constraint

### 2.1 Clave: THE Timeline Constraint

If jazz rhythm centers on the swing ratio, Afro-Cuban music centers on the **clave** — a five-note timeline pattern that serves as the **LAMAN element** for the entire rhythmic system. The clave is not merely a rhythm; it is a **structural law** from which all other rhythmic decisions derive.

**Son Clave 2-3:**
```
| X . . X . . X . | . X . X . . . . |
  1 & 2 & 3 & 4 &   1 & 2 & 3 & 4 &
```
Strokes on: 2, 3, 4&, 6, 7 (in two-bar unit). The "2-side" (bar 2) has two strokes; the "3-side" (bar 1) has three. Played in 2-3 direction.

**Son Clave 3-2:** The reverse direction — the 3-side comes first. Same pattern, different orientation. The direction determines the entire feel of a piece and cannot be reversed mid-performance without a formal transition.

**Rumba Clave 3-2:**
```
| X . . X . . . X | . X . X . . . . |
  1 & 2 & 3 & 4 &   1 & 2 & 3 & 4 &
```
The third stroke of the 3-side is delayed by one eighth note (from beat 4 to beat 4&), creating greater syncopation. This single stroke displacement creates a fundamentally different groove feel — rumba is more "floating," son is more "grounded."

In constraint theory terms, the clave is the **absolute LAMAN** — the timeline that NEVER changes during a piece. All other parts must satisfy alignment with the clave. A part that contradicts the clave is not merely wrong — it is *caballo* (horselike), a term Cuban musicians use for rhythmic disorientation. The constraint is binary: you are either in clave or out of clave.

### 2.2 Cascara: The Secondary Timeline

**Cascara** (also called **marcha** or **ride pattern**) is the pattern played on the sides of the timbales or on a bell. It serves as the **secondary LAMAN** — less rigid than clave but more rigid than individual drum parts:

```
| X . X . . X X . | . X . X . X X . |
  1 & 2 & 3 & 4 &   1 & 2 & 3 & 4 &
```

The cascara's relationship to clave is critical: the cascara **reinforces** the clave rather than merely coexisting with it. Certain strokes of the cascara coincide with clave strokes, creating alignment points. Between these alignment points, the cascara fills with its own internal logic, but it must always return to agreement with the clave at the designated points.

This is **CONSENSUS with partial overlap** — the cascara and clave share specific agreement points but maintain independent trajectories between them. The cascara is freer than the clave but not free; its freedom is bounded by the requirement to converge with the clave at predetermined moments.

### 2.3 6/8 Afro Feel vs. 4/4 Son Feel: Polymetric Tension

Afro-Cuban music operates in two primary metric modes:

**4/4 Son feel:** Binary subdivision. The clave operates in 4/4 with eighth-note subdivision. The cascara, tumbao (bass pattern), and all drum parts operate in 4/4. This is the metric framework for son, mambo, cha-cha-chá, and most salsa.

**6/8 Afro feel:** Ternary subdivision. The bell patterns derive from 6/8 (or 12/8) compound meter. The fundamental pattern is the **6/8 bell** (also called **cona**):

```
| X . X . X . | X . X . . . |
  1 2 3 4 5 6   1 2 3 4 5 6
```

This pattern creates a **3:2 hemiola** when heard against a duple subdivision — the same 3:2 relationship found in Ewe bell patterns, demonstrating the direct African lineage.

The polymetric tension between 6/8 and 4/4 is a **persistent constraint duality** in Afro-Cuban music. Many pieces transition between the two feels, and some maintain both simultaneously. The **Columbia** style of rumba superimposes 6/8 feel over a 4/4 framework, creating the characteristic "floating" quality. In constraint terms, this is operating two SNAP grids simultaneously — a binary grid and a ternary grid — and requiring all parts to satisfy at least one grid at all times.

### 2.4 Rumba Columbia: Free Rhythm Within Clave

**Rumba Columbia** is a solo vocal and drumming form that presents a paradox: extreme rhythmic freedom within the strictest possible constraint framework. The singer declaims in free rhythm (no fixed meter), the solo drummer (quinto) improvises with maximum expression, but the **clave never stops** and the **rhythm section** (tumbadora and salidor) maintains strict patterns.

In constraint terms, Columbia implements a **tiered freedom system**:

1. **Tier 0 (LAMAN):** Clave — absolute rigidity, never varies
2. **Tier 1 (high LAMAN):** Salidor and tumbadora — fixed patterns with minimal variation
3. **Tier 2 (moderate LAMAN):** Quinto — improvises but must align with clave at key points
4. **Tier 3 (minimal LAMAN):** Vocal — free rhythm, no grid requirement, but must resolve into the rhythmic framework periodically

This tiered system allows maximum expression at the top while maintaining structural integrity at the bottom. The constraint is that **freedom at one tier is bounded by rigidity at lower tiers**. The quinto can play anything — as long as the salidor and tumbadora provide a stable reference frame.

### 2.5 Abakuá: Secret Society Rhythms and Extreme Complexity

The **Abakuá** traditions of Cuba derive from the Efik and Ejagham peoples of southeastern Nigeria and Cameroon. These secret society rhythms represent the most complex constraint systems in Afro-Cuban music:

- **Four independent drum parts** (enkómo) interlock with mathematical precision
- **Bell pattern** maintains an independent timeline
- **Separate percussion** (maruga, chéquere) adds additional layers
- **Vocal chants** follow specific metric patterns tied to liturgical requirements

The Abakuá bell pattern is a twelve-pulse timeline (like Ewe traditions) that creates maximum rhythmic ambiguity: it can be heard in 4/4, 6/8, or 3/4 depending on the listener's orientation. This is a **multistable SNAP grid** — a pattern that satisfies multiple metric interpretations simultaneously, and the "correct" interpretation depends on which drum part the listener attends to.

The constraint complexity is extreme: each drum part must satisfy alignment with the bell, alignment with each other drum at specific intersection points, internal pattern consistency, AND liturgical correctness (the wrong pattern is not merely unmusical but spiritually incorrect). This represents the highest LAMAN values in the Afro-Cuban tradition — constraints that are sacred as well as musical.

### 2.6 Batá Drumming: Orisha-Specific Patterns

The **batá** drum ensemble (derived from Yoruba traditions) is used in Santería/Lucumí religious ceremonies to invoke specific **orishas** (deities). Each orisha has specific rhythmic patterns that are **functionally mandatory** — playing the wrong pattern invokes the wrong deity, which has serious religious consequences.

**Eleguá** (messenger, crossroads): Patterns are simple, staccato, direct — reflecting Eleguá's role as opener of paths. The SNAP grid is relatively wide, allowing flexibility.

**Changó** (thunder, drums, fire): Patterns are aggressive, complex, driving. Changó is associated with the batá itself, so his patterns push the technical limits of the drums. The SNAP grid is tight and the syncopation budget is high — maximum complexity within maximum precision.

**Yemayá** (ocean, motherhood): Patterns are flowing, wave-like, in 6/8 feel. The FUNNEL gravity is gentle — notes flow toward the downbeat like water. The SNAP grid is ternary (6/8), and the syncopation budget is moderate.

**Ogún** (iron, war, labor): Patterns are relentless, machine-like, reflecting Ogún's association with iron and metalwork. Maximum LAMAN — patterns repeat with near-zero variation.

**Oyá** (winds, storms, change): Patterns are unpredictable, shifting, with sudden changes in dynamics and density. Low LAMAN on individual patterns but high LAMAN on the requirement to change at specific ceremonial moments.

The constraint architecture for batá is **liturgically coupled**: the pattern choice is determined by the ceremonial context, the tempo is determined by the priest's directives, and the variations signal transitions between ceremonial phases. The drummer must satisfy musical constraints AND religious constraints simultaneously — a coupled constraint system where the "correctness" of a rhythmic decision depends on both musical and spiritual criteria.

### 2.7 Cuban Popular Styles: Mozambique, Pilón, Songo

**Mozambique** (Pedro Izquierdo "Pello el Afrokán," 1963): A carnival rhythm built on a **high-density SNAP grid** — the pattern distributes strokes across every possible subdivision point, creating maximum density. The conga pattern alone has 8-10 strokes per bar. The constraint is that despite this density, the clave must remain audible. This creates a compression problem: fitting maximum rhythmic information into the grid while preserving clave transparency.

**Pilón** (Enrique Bonne, 1960s): Named after the Cuban coffee grinder, pilón uses a characteristic two-note bass pattern that mimics the grinding motion. The SNAP grid is binary (4/4), and the innovation is that the **bass becomes the timeline** — the bass pattern is as rigid as the clave in other styles, creating a dual LAMAN system (bass + clave).

**Songo** (José Luis Quintana "Changuito," Los Van Van, 1970s): Songo is a **fusion constraint system** — it merges Afro-Cuban folkloric patterns with funk, jazz, and pop elements. The drum kit plays patterns derived from folkloric drums but adapted for the kit, creating a hybrid SNAP grid that alternates between binary and ternary subdivision. Songo's key innovation is the **variable SNAP grid**: the subdivision feel can shift between straight and triplet within a single pattern, requiring the musician to satisfy two grids in alternation.

---

## 3. Brazilian Rhythm: Layered Constraint Architecture

### 3.1 Samba: Multiple Independent Constraint Layers

Brazilian samba, particularly the **samba de enredo** (carnival samba) of Rio's escolas de samba, presents the most layered constraint architecture in Western hemisphere music. A full bateria (drum corps) maintains **6-8 simultaneous independent constraint layers**:

**Surdo (bass drums) — three voices:**
- **Surdo de marcação (first surdo):** Beats 1 and 3 (or beat 1 only in some styles). The temporal anchor. Highest LAMAN — never varies.
- **Surdo de resposta (second surdo):** Beats 2 and 4. Offbeats from the first surdo's perspective. Creates the duple feel.
- **Surdo de corte (third surdo):** Syncopated pattern between the first and second. Adds swing. Moderate LAMAN with some variation.

**Tamborim:** Small hand drum played with a stick, featuring rapid patterns (carreteiro) that create a high-density secondary grid. The tamborim often plays sixteenth-note or thirty-second-note patterns that subdivide the surdo grid. Its pattern is the most complex fixed pattern in the bateria.

**Agogô:** Double or triple iron bell. Plays a timeline pattern analogous to Cuban clave — a repeating asymmetric pattern that all other parts reference. This is the samba's **LAMAN timeline**.

**Cuíca:** Friction drum with a distinctive "laughing" sound. Plays syncopated patterns that respond to the melody. The most improvisational layer — lowest LAMAN, highest syncopation budget.

**Repinique:** High-pitched drum played with two sticks. Plays calls, breaks, and fill patterns. Functions as the lead voice for the bateria. Moderate LAMAN — fixed patterns with improvisational breaks.

**Caixa (snare):** Steady rolling pattern that fills the rhythmic space between the surdo beats. The "glue" that binds all layers together. High LAMAN — rarely varies.

The constraint architecture is **hierarchical and nested**: the surdo defines the beat grid (SNAP level 1), the tamborim and agogô define the subdivision grid (SNAP level 2), the caixa fills the space between grid points (SNAP level 3), and the cuíca and repinique operate with relative freedom above these three levels. This nesting means that freedom at higher levels is bounded by rigidity at lower levels — exactly the tiered freedom system seen in rumba Columbia and Abakuá traditions.

### 3.2 Bossa Nova: João Gilberto's Guitar Pattern

João Gilberto's guitar pattern is perhaps the most influential single rhythmic innovation in 20th-century popular music. It is a **syncopated two-bar pattern** that creates a unique constraint profile:

```
| . . X . . X . X | . X . . X . . X |
  1 & 2 & 3 & 4 &   1 & 2 & 3 & 4 &
```

(Notation simplified; actual pattern has slight variations depending on the chord voicing and song form.)

The pattern's genius lies in its **asymmetric syncopation**: it creates a repeating cycle where the strong beats (1 and 3) are regularly anticipated, but the anticipations occur at irregular intervals within the two-bar phrase. This means the listener's expectation of the downbeat is both confirmed (it always arrives) and subverted (the pattern's internal accents pull away from it).

In constraint terms, the bossa nova guitar pattern operates a **shifted FUNNEL**: the gravity center is not on the downbeat but slightly ahead of it, creating a gentle forward lean. The SNAP grid is binary (straight eighth notes — no swing), but the accents create a syncopation pattern that implies ternary grouping. The result is a subtle polyrhythmic feel within a strictly duple framework — a "ternary implication" that is never realized.

The bass motion (root on beat 1, fifth on beat 3 of the second bar) reinforces the duple grid while the guitar's syncopation works against it. This **tension between harmonic rhythm (duple) and melodic rhythm (syncopated)** is the defining constraint of bossa nova.

### 3.3 Partido Alto: Syncopation Within Samba

**Partido alto** is a samba sub-style characterized by extreme syncopation in the harmonic instruments (guitar, cavaquinho). The pattern "embryos" (the core rhythmic cells) are two-beat units that can be combined, truncated, or extended to create endless variation within the samba framework.

The constraint system is **generative**: from a small set of rhythmic cells (typically 3-5 two-beat patterns), the musician generates longer phrases by concatenation, repetition, and variation. The constraint is that each cell must satisfy alignment with the samba timeline (agogô pattern) at its boundaries, but internal variation within cells is permitted.

This is **LAMAN at the cell boundary** with **freedom at the cell interior** — a modular constraint system. The partido alto musician's skill is measured by the ability to create phrases that are surprising in their internal content but inevitable in their boundary alignment.

### 3.4 Baião: Northeastern Brazilian Rhythm

The **baião** (popularized by Luiz Gonzaga in the 1940s) is a 2/4 rhythm from Northeastern Brazil with a distinctive accent pattern that sets it apart from samba:

- **Strong accent on beat 1** (reinforced by the zabumba bass drum)
- **Syncopated second beat** (the zabumba plays an offbeat pattern against the strong beat 1)
- **Triangulo (triangle)** plays continuous sixteenth notes, creating a high-density subdivision grid
- **Accordion** provides harmonic and melodic content with characteristic syncopation

The constraint architecture is simpler than samba — fewer layers — but with a distinctive SNAP grid: the accent pattern creates a **strong-weak** feel within 2/4 that is markedly different from samba's more evenly distributed accents. The FUNNEL gravity pulls hard toward beat 1, and the offbeat zabumba creates tension by resisting this pull.

### 3.5 Maracatu: Deep Drums and Metallic Timelines

**Maracatu** (from Pernambuco, Northeastern Brazil) features:

- **Alfaias** (deep rope-tuned drums in three sizes): Play interlocking patterns with strong downbeat emphasis. The largest (alfaia marcação) provides the fundamental pulse; the medium and small sizes add syncopation and variation.
- **Gonguê** (cowbell): Plays a timeline pattern that is the maracatu equivalent of clave — a rigid repeating pattern that all other parts reference.
- **Caixa** (snare): Military-style rolling patterns adapted to the maracatu feel.
- **Tarol** (shallow snare): Rapid patterns filling the rhythmic space.

The constraint architecture combines **Afro-Brazilian layering** with **military-band precision**: the alfaia patterns are rigid (high LAMAN) but the gonguê timeline provides the ultimate reference. The result is a heavy, powerful groove with deep FUNNEL gravity — the downbeat pull in maracatu is stronger than in almost any other Brazilian style.

### 3.6 Afoxé: Candomblé Adapted for Carnival

**Afoxé** rhythms are adapted from **Candomblé** religious ceremonies (Brazilian counterpart to Cuban Santería) for carnival processions. The core pattern is the **ijexá**:

- Simple duple pattern with emphasis on beats 1 and the "and" of beat 2
- Played on agogô (bell), atabaque (conga-type drum), and xequerê (beaded gourd)
- The pattern is nearly identical to the Cuban **cáscara** pattern, demonstrating shared Yoruba origins

The constraint profile is minimalist compared to samba: fewer layers, simpler patterns, but strict adherence to the timeline. The LAMAN value is high for the bell pattern, moderate for the drums, and the syncopation budget is low — afoxé is about purity and clarity of the timeline rather than complexity.

---

## 4. Latin Jazz Fusion: Constraint Systems in Collision

### 4.1 Cubop: Cuban + Bebop Constraint Fusion

**Cubop** (late 1940s) — the meeting of Cuban rhythm and bebop harmony initiated by **Dizzy Gillespie** and **Chano Pozo** — represents the first systematic collision of two complete constraint systems:

**Cuban constraint system:** Clave-based timeline, cascara secondary timeline, tumbao bass, conga patterns, binary SNAP grid with ternary implications.

**Bebop constraint system:** Swing feel (ternary SNAP grid), ride cymbal lattice, walking bass, syncopated melodic lines, chord changes as harmonic timeline.

The fusion creates a **dual-grid constraint problem**: the rhythm section must satisfy the Cuban binary grid (clave, cascara) while the horn players operate in the jazz ternary grid (swing). The bassist bears the heaviest constraint load — walking bass (jazz) must align with the tumbao (Cuban), requiring the bass to satisfy both grids simultaneously.

Dizzy Gillespie's insight was that the **harmonic changes** of bebop could serve as the jazz equivalent of clave — a structural timeline that organizes the music's large-scale form. In this view, chord changes = harmonic clave, and the challenge is to align rhythmic clave with harmonic clave.

### 4.2 Latin Jazz Clave Applied to Jazz Harmony

In modern Latin jazz (Tito Puente, Mongo Santamaria, Chucho Valdés, Gonzalo Rubalcava), the clave is applied to jazz harmony in several ways:

1. **Clave alignment of chord voicings:** Piano montunos (repeated rhythmic-harmonic patterns) are constructed so that their strongest rhythmic accents coincide with clave strokes. This creates **CONSENSUS between harmonic and rhythmic timelines**.

2. **Solo phrasing in clave:** Jazz improvisers learning Latin jazz must internalize the constraint that their phrases should resolve in alignment with the clave. A phrase that resolves against the clave sounds "wrong" even if the notes are harmonically correct.

3. ** clave as form determinant:** In salsa arrangements, the **mambo section** (horn ensemble) and **montuno section** (call-and-response improvisation) are structured around clave cycles. The arrangement must respect clave direction — a 2-3 clave piece cannot transition to a 3-2 orientation without a formal break.

4. **Cáscara as ride cymbal equivalent:** In Latin jazz drum set playing, the cáscara pattern played on the shell of the floor tom or on a bell serves the same function as the ride cymbal pattern in jazz — it provides the temporal lattice (SNAP grid) for the entire ensemble.

### 4.3 Cross-Rhythm as Constraint Satisfaction Problem

The phenomenon of **cross-rhythm** (two or more conflicting rhythmic patterns maintained simultaneously) maps directly to **constraint satisfaction problems** in computer science:

- **Variables:** The time points at which rhythmic events occur
- **Domains:** Possible subdivisions (eighth notes, triplets, sixteenth notes, etc.)
- **Constraints:** (a) Each pattern must maintain internal consistency; (b) Patterns must align at specified intersection points; (c) The composite rhythm must be perceptible as coherent by listeners

The solution space for a cross-rhythmic system is bounded by the LCM of the constituent patterns' cycle lengths. A 3:2 cross-rhythm resolves every 6 pulses; a 4:3 every 12; a 7:4 every 28. Within each resolution cycle, the individual patterns create a pattern of agreement and disagreement — the **interference pattern** that gives cross-rhythm its characteristic tension and release.

In Latin jazz, the most common cross-rhythmic structures are:

- **3:2 over 4/4** — the fundamental Afro-Cuban hemiola, present in virtually all Cuban music
- **6/8 over 4/4** — polymetric tension between Afro feel and son feel
- **2:3 cascara against 3:2 clave** — the cascara pattern has a different accent structure than the clave, creating cross-accentuation within a shared grid

---

## 5. Constraint Mappings: Five Primitives Applied to Rhythm

### 5.1 SNAP → Rhythmic Grid

The **SNAP** parameter defines the subdivision grid:

| Grid Type | SNAP Value | Pulses per Beat | Traditions |
|-----------|-----------|----------------|------------|
| Duple (straight) | 0.50 | 2 | Latin jazz, funk, pilón |
| Triplet (swing) | 0.67 | 3 | Jazz swing, Afro 6/8 |
| Dotted | 0.75 | 4 (dotted subdivision) | Deep swing, blues |
| Sixteenth | 0.25 | 4 | Fusion, samba tamborim |
| Quintuplet | 0.20 | 5 | Advanced jazz, experimental |
| Sextuplet | 0.167 | 6 | Very advanced jazz |

SNAP is not fixed — it can be **dynamic** (varying within a performance) or **simultaneous** (two grids operating concurrently, as in polymetric music). The key insight: SNAP defines the *available* constraint space. A finer grid (more subdivisions) creates more possible snap points and therefore more opportunities for syncopation (constraint violation).

### 5.2 FUNNEL → Beat Gravity

The **FUNNEL** parameter defines the gravitational pull toward metric reference points:

- **Strong FUNNEL** (narrow pocket): All events pulled hard toward the downbeat. Military music, techno, pilón. Pocket depth: 5-15ms.
- **Moderate FUNNEL** (medium pocket): Events gravitate toward but don't always hit the downbeat. Samba, son, pop. Pocket depth: 15-30ms.
- **Weak FUNNEL** (wide pocket): Events float freely around the beat, with only a gentle pull toward downbeats. Free jazz, rumba columbia, avant-garde. Pocket depth: 30-80ms.

The FUNNEL can also be **offset** — the gravity center displaced from the metronomic downbeat. Jazz "behind the beat" playing is a forward-offset FUNNEL (the center is ahead of where you play, pulling you forward). "Ahead of the beat" playing is a backward-offset FUNNEL.

### 5.3 CONSENSUS → Clave Compliance

**CONSENSUS** in rhythm means: all parts must agree on the structural timeline. In Afro-Cuban music, this is **clave compliance** — every part must be "in clave." The consensus check is:

1. Does the part's accent pattern reinforce or contradict the clave?
2. Do the part's strong beats coincide with clave strokes?
3. If the part has a cyclic pattern, does it align with the clave cycle (2-bar)?

A part that fails the consensus check creates **caballo** — rhythmic disorientation that is immediately perceptible to experienced listeners. The consensus requirement is strongest in Afro-Cuban traditions and somewhat relaxed in Brazilian music (where the agogô pattern serves a similar but less rigid function) and jazz (where the consensus requirement is more about pocket alignment than timeline compliance).

### 5.4 LAMAN → Timeline Rigidity

**LAMAN** measures how rigid the timeline constraint is:

| Tradition | Timeline | LAMAN Value | Flexibility |
|-----------|----------|-------------|-------------|
| Afro-Cuban folkloric | Clave | 0.95-1.0 | Virtually none |
| Samba escola | Agogô pattern | 0.85-0.95 | Very slight variation |
| Jazz ride cymbal | Ride pattern | 0.70-0.85 | Some variation in accents |
| Bossa nova guitar | João Gilberto pattern | 0.75-0.85 | Slight syncopation variation |
| Jazz walking bass | Walking pattern | 0.60-0.75 | Note choice varies, rhythm consistent |
| Free jazz | No fixed timeline | 0.0-0.2 | No timeline constraint |

The LAMAN value determines how much the timeline can bend before the constraint is considered violated. High LAMAN = the timeline is sacred. Low LAMAN = the timeline is negotiable.

### 5.5 TEMPO → Groove Pocket Width

**TEMPO** in rhythm is not just BPM — it's the **width of the acceptable timing zone** around each grid point. This is the "groove pocket":

- **Tight pocket** (narrow TEMPO): Events must fall within 5-10ms of the grid point. Samba at carnival tempo, batá drumming in ceremony. Maximum precision required.
- **Medium pocket**: 10-25ms tolerance. Son, salsa, mainstream jazz. The pocket is felt but not rigid.
- **Wide pocket**: 25-50ms tolerance. Jazz ballads, rumba columbia, some Brazilian folk styles. Greater expressive freedom.
- **Very wide pocket**: 50-100ms tolerance. Free jazz, experimental. The grid is a suggestion.

The pocket width interacts with tempo: at fast tempos, the pocket must be tighter (proportionally) because the grid points are closer together. At slow tempos, the pocket can be wider without losing the groove. This creates a **tempo-pocket coupling** — the pocket width must be calibrated to the tempo.

---

## 6. Novel Rhythm Parameters

### 6.1 Clave Adherence Score (0-1)

A continuous measure of how strictly parts follow the clave timeline:

- **0.0:** No relationship to clave (free rhythm, non-Afro-Cuban music)
- **0.3:** Parts reference clave but with frequent deviations (Latin jazz solos)
- **0.5:** Parts mostly in clave with occasional ambiguities (salsa montuno)
- **0.7:** Strong clave alignment (standard son, cha-cha-chá)
- **0.9:** Near-perfect clave adherence (rumba, batá)
- **1.0:** The clave itself — absolute adherence

Application: In a constraint engine, the clave adherence score determines how strictly the system enforces clave alignment on generated parts. A score of 0.9 would allow only the most subtle deviations; 0.5 would permit significant rhythmic freedom as long as key alignment points are respected.

### 6.2 Swing Continuum (0.50-0.80)

The continuous parameter governing the long-short ratio of subdivided beats:

```
0.50 ─── Straight (1:1)
  │
0.57 ─── Slight lilt
  │
0.67 ─── Triplet swing (2:1)
  │
0.75 ─── Dotted feel (3:1)
  │
0.80 ─── Double-dotted (4:1)
```

This parameter directly controls the **SNAP grid** in a constraint engine. Setting swing to 0.67 creates a triplet grid; 0.50 creates a duple grid. Intermediate values create asymmetric grids that don't correspond to standard Western notation but are common in actual performance practice.

### 6.3 Syncopation Budget (0-8 beats per measure)

The number of beats per measure where events are permitted to fall off the primary SNAP grid:

- **0:** No syncopation (march, hymn, ceremonial music)
- **1-2:** Mild syncopation (pop, folk)
- **3-4:** Moderate syncopation (standard jazz, son)
- **5-6:** Heavy syncopation (bebop, samba, rumba)
- **7-8:** Maximum syncopation (free jazz, avant-garde)

This parameter controls how many constraint violations are permitted per measure. A budget of 0 means the system enforces strict grid adherence; a budget of 8 means virtually any placement is acceptable.

### 6.4 Pocket Depth (0-100ms)

The width of the "groove pocket" — the acceptable timing deviation from the theoretical grid:

- **0-10ms:** Machine precision. Electronic music, sequenced tracks.
- **10-25ms:** Tight human pocket. Samba, Afro-Cuban folkloric, funk.
- **25-50ms:** Medium pocket. Jazz, son, salsa, pop.
- **50-100ms:** Wide pocket. Ballads, rumba columbia, free jazz.

Pocket depth determines the **TEMPO parameter** — how much timing variance the system tolerates before a note is considered "out of pocket."

### 6.5 Layer Independence (0-1)

How independent each rhythmic layer can be from others:

- **0.0:** All layers must be synchronized (march, pop drum machine)
- **0.3:** Layers share grid but can vary accent patterns (standard jazz trio)
- **0.5:** Layers can have different accent patterns and slight timing offsets (salsa, son)
- **0.7:** Layers can operate in different subdivisions (Afro-Cuban folkloric, batá)
- **0.9:** Layers are nearly independent (Ewe drumming, Abakuá, samba escola)
- **1.0:** Complete independence (free improvisation)

Layer independence determines how much the constraint engine allows parts to deviate from each other. High independence means the system permits — even encourages — parts that create polyrhythmic tension against each other.

### 6.6 Displacement Factor (0-1)

How often metric displacement occurs — the frequency with which the primary metric frame is temporarily overridden by an alternative:

- **0.0:** Never (steady groove, pop, dance music)
- **0.2:** Occasional (mainstream jazz, standard son)
- **0.4:** Frequent (Elvin Jones-style playing, advanced Latin jazz)
- **0.6:** Constant (free jazz, experimental)
- **0.8-1.0:** Continuous displacement (the metric frame is permanently unstable)

Displacement factor controls the rate of constraint redirection — how often the FUNNEL gravity shifts from the primary grid to a secondary grid.

---

## 7. Fifteen Rhythm Presets as Constraint Profiles

Each preset encodes a specific tradition as a complete constraint satisfaction profile:

### Preset 1: Jazz Swing (Fast)

| Parameter | Value |
|-----------|-------|
| Swing | 0.67 |
| SNAP grid | Triplet |
| FUNNEL | Moderate, slight behind-beat offset (+15ms) |
| CONSENSUS | Medium (pocket alignment) |
| LAMAN | 0.75 (ride cymbal) |
| TEMPO pocket | 20ms |
| Syncopation budget | 4 |
| Layer independence | 0.4 |
| Displacement | 0.2 |
| Clave adherence | 0.0 |
| Pocket depth | 20ms |

**Reference:** Count Basie Orchestra, Oscar Peterson Trio at fast tempos (200+ BPM).

### Preset 2: Jazz Ballad

| Parameter | Value |
|-----------|-------|
| Swing | 0.73 |
| SNAP grid | Dotted/triplet hybrid |
| FUNNEL | Weak, behind-beat offset (+30ms) |
| CONSENSUS | Low (wide interpretive freedom) |
| LAMAN | 0.60 (minimal ride pattern) |
| TEMPO pocket | 40ms |
| Syncopation budget | 5 |
| Layer independence | 0.5 |
| Displacement | 0.1 |
| Clave adherence | 0.0 |
| Pocket depth | 40ms |

**Reference:** Miles Davis *Kind of Blue*, Bill Evans Trio.

### Preset 3: Bossa Nova

| Parameter | Value |
|-----------|-------|
| Swing | 0.50 |
| SNAP grid | Straight eighth |
| FUNNEL | Moderate, no offset |
| CONSENSUS | Medium (guitar-bass alignment) |
| LAMAN | 0.80 (João Gilberto pattern) |
| TEMPO pocket | 25ms |
| Syncopation budget | 4 |
| Layer independence | 0.3 |
| Displacement | 0.05 |
| Clave adherence | 0.4 (agogô reference) |
| Pocket depth | 25ms |

**Reference:** João Gilberto, Stan Getz/Gilberto, Tom Jobim.

### Preset 4: Samba Escola

| Parameter | Value |
|-----------|-------|
| Swing | 0.50 |
| SNAP grid | Sixteenth note |
| FUNNEL | Strong, beat 1 emphasis |
| CONSENSUS | High (agogô timeline) |
| LAMAN | 0.90 (agogô + surdo de marcação) |
| TEMPO pocket | 15ms |
| Syncopation budget | 5 |
| Layer independence | 0.8 |
| Displacement | 0.1 |
| Clave adherence | 0.6 (agogô as reference) |
| Pocket depth | 15ms |

**Reference:** Mangueira, Portela, Salgueiro escolas de samba.

### Preset 5: Baião

| Parameter | Value |
|-----------|-------|
| Swing | 0.50 |
| SNAP grid | Duple (2/4) |
| FUNNEL | Strong, heavy beat 1 pull |
| CONSENSUS | Medium (zabumba + accordion) |
| LAMAN | 0.75 (zabumba pattern) |
| TEMPO pocket | 20ms |
| Syncopation budget | 3 |
| Layer independence | 0.5 |
| Displacement | 0.05 |
| Clave adherence | 0.3 |
| Pocket depth | 20ms |

**Reference:** Luiz Gonzaga, Dominguinhos, Gonzaguinha.

### Preset 6: Son Clave 2-3

| Parameter | Value |
|-----------|-------|
| Swing | 0.50 |
| SNAP grid | Straight eighth |
| FUNNEL | Moderate, clave-aligned |
| CONSENSUS | Very high (clave compliance) |
| LAMAN | 0.95 (son clave) |
| TEMPO pocket | 20ms |
| Syncopation budget | 4 |
| Layer independence | 0.6 |
| Displacement | 0.05 |
| Clave adherence | 0.85 |
| Pocket depth | 20ms |

**Reference:** Septeto Nacional, Buena Vista Social Club, traditional son.

### Preset 7: Son Clave 3-2

| Parameter | Value |
|-----------|-------|
| Swing | 0.50 |
| SNAP grid | Straight eighth |
| FUNNEL | Moderate, clave-aligned |
| CONSENSUS | Very high (clave compliance) |
| LAMAN | 0.95 (son clave) |
| TEMPO pocket | 20ms |
| Syncopation budget | 4 |
| Layer independence | 0.6 |
| Displacement | 0.05 |
| Clave adherence | 0.85 |
| Pocket depth | 20ms |

**Reference:** Same as 2-3 but reversed direction; common in salsa arrangements.

### Preset 8: Rumba Clave

| Parameter | Value |
|-----------|-------|
| Swing | 0.50 |
| SNAP grid | Straight eighth |
| FUNNEL | Moderate-weak (floating feel) |
| CONSENSUS | High (clave compliance) |
| LAMAN | 0.95 (rumba clave) |
| TEMPO pocket | 25ms |
| Syncopation budget | 5 |
| Layer independence | 0.7 |
| Displacement | 0.15 |
| Clave adherence | 0.90 |
| Pocket depth | 25ms |

**Reference:** Yoruba Andabo, Los Muñequitos de Matanzas, rumba guaguancó.

### Preset 9: Mozambique

| Parameter | Value |
|-----------|-------|
| Swing | 0.50 |
| SNAP grid | Sixteenth note |
| FUNNEL | Strong (driving feel) |
| CONSENSUS | High (dense interlocking) |
| LAMAN | 0.85 (conga pattern) |
| TEMPO pocket | 15ms |
| Syncopation budget | 6 |
| Layer independence | 0.6 |
| Displacement | 0.1 |
| Clave adherence | 0.70 |
| Pocket depth | 15ms |

**Reference:** Pello el Afrokán, original Havana carnival style.

### Preset 10: Songo

| Parameter | Value |
|-----------|-------|
| Swing | 0.55 (slight swing) |
| SNAP grid | Variable (straight/triplet hybrid) |
| FUNNEL | Moderate-strong |
| CONSENSUS | High (kick + cascara alignment) |
| LAMAN | 0.80 (kick pattern) |
| TEMPO pocket | 18ms |
| Syncopation budget | 5 |
| Layer independence | 0.5 |
| Displacement | 0.2 |
| Clave adherence | 0.60 |
| Pocket depth | 18ms |

**Reference:** Los Van Van, Changuito, modern Cuban popular music.

### Preset 11: Afro 6/8

| Parameter | Value |
|-----------|-------|
| Swing | 0.67 (ternary subdivision) |
| SNAP grid | Triplet (12/8) |
| FUNNEL | Moderate (flowing) |
| CONSENSUS | High (bell timeline) |
| LAMAN | 0.90 (6/8 bell) |
| TEMPO pocket | 20ms |
| Syncopation budget | 4 |
| Layer independence | 0.7 |
| Displacement | 0.1 |
| Clave adherence | 0.75 (bell as reference) |
| Pocket depth | 20ms |

**Reference:** Afro-Cuban folkloric, columbia in 6/8, abakuá.

### Preset 12: Batá Changó

| Parameter | Value |
|-----------|-------|
| Swing | 0.67 |
| SNAP grid | Triplet (12/8) |
| FUNNEL | Strong (driving, aggressive) |
| CONSENSUS | Very high (liturgical correctness) |
| LAMAN | 0.95 (orisha-specific pattern) |
| TEMPO pocket | 12ms |
| Syncopation budget | 5 |
| Layer independence | 0.6 |
| Displacement | 0.15 |
| Clave adherence | 0.90 |
| Pocket depth | 12ms |

**Reference:** Changó batá toque in Santería ceremony.

### Preset 13: Maracatu

| Parameter | Value |
|-----------|-------|
| Swing | 0.50 |
| SNAP grid | Duple |
| FUNNEL | Very strong (heavy downbeat) |
| CONSENSUS | High (gonguê timeline) |
| LAMAN | 0.85 (gonguê + alfaia marcação) |
| TEMPO pocket | 15ms |
| Syncopation budget | 4 |
| Layer independence | 0.6 |
| Displacement | 0.1 |
| Clave adherence | 0.65 (gonguê as reference) |
| Pocket depth | 15ms |

**Reference:** Maracatu Nação Elefante, Maracatu Nação Camaleão.

### Preset 14: Partido Alto

| Parameter | Value |
|-----------|-------|
| Swing | 0.50 |
| SNAP grid | Sixteenth note |
| FUNNEL | Moderate |
| CONSENSUS | Medium (samba timeline) |
| LAMAN | 0.75 (agogô + surdo) |
| TEMPO pocket | 20ms |
| Syncopation budget | 6 |
| Layer independence | 0.5 |
| Displacement | 0.1 |
| Clave adherence | 0.50 (samba reference) |
| Pocket depth | 20ms |

**Reference:** Candeia, Partido Alto-style samba, roda de samba.

### Preset 15: Cubop

| Parameter | Value |
|-----------|-------|
| Swing | 0.58 (jazz-Cuban hybrid) |
| SNAP grid | Mixed (straight for Latin, triplet for jazz phrases) |
| FUNNEL | Moderate, clave-aligned |
| CONSENSUS | High (clave + changes alignment) |
| LAMAN | 0.85 (clave + montuno) |
| TEMPO pocket | 20ms |
| Syncopation budget | 6 |
| Layer independence | 0.5 |
| Displacement | 0.25 |
| Clave adherence | 0.70 |
| Pocket depth | 20ms |

**Reference:** Dizzy Gillespie/Chano Pozo, Machito and his Afro-Cubans, modern Latin jazz.

---

## 8. Synthesis: Rhythm as Universal Constraint Engine

The mapping of global rhythm traditions onto constraint theory reveals several universal principles:

1. **Every tradition has a LAMAN element** — a rigid timeline that serves as the structural backbone. In Afro-Cuban music, it's the clave. In samba, the agogô pattern. In jazz, the ride cymbal pattern. In batá, the orisha-specific pattern. The LAMAN element is always the most rigid constraint in the system.

2. **Freedom is always tiered** — lower layers are more rigid, upper layers more flexible. The surdo doesn't improvise; the cuíca does. The clave doesn't change; the quinto does. The ride cymbal maintains its lattice; the saxophonist explores. This tiered architecture is not cultural but structural — it's how constraint satisfaction systems manage complexity.

3. **SNAP grids are dynamic** — no tradition uses a truly fixed grid. Jazz swing ratio varies with tempo; samba feel shifts slightly between sections; Afro-Cuban music transitions between 4/4 and 6/8 grids. The grid is a living parameter, not a fixed setting.

4. **FUNNEL defines the pocket** — the width and offset of the gravitational pull toward metric reference points determines the "feel" more than any other parameter. Behind the beat, ahead of the beat, on the beat — these are FUNNEL configurations, not independent phenomena.

5. **CONSENSUS is cultural** — what constitutes "agreement" between parts varies across traditions. In Afro-Cuban music, consensus means literal alignment with the clave timeline. In jazz, consensus means alignment with the ensemble's pocket. In Brazilian music, consensus means alignment with the agogô pattern and surdo pulse. The consensus rule is encoded in the culture, not in acoustics.

6. **Cross-rhythm is constraint satisfaction** — the maintenance of two or more conflicting rhythmic patterns is a real-time constraint satisfaction problem with known mathematical properties (LCM-based resolution cycles, interference patterns, periodic alignment).

These principles suggest that a computational constraint engine capable of modeling global rhythm traditions would need: dynamic SNAP grids, tiered LAMAN values, configurable FUNNEL gravity, culturally-specific CONSENSUS rules, and tempo-coupled TEMPO pockets. The fifteen presets presented here provide starting points for such a system, each encoding a specific tradition's constraint profile as a set of numerical parameters.

The ultimate insight: **rhythm is constraint, groove is satisfaction, and swing is the space between.**

---

## References

- Austerlitz, P. (2005). *Jazz Consciousness: Music, Race, and Humanity.* Wesleyan University Press.
- Berliner, P. (1994). *Thinking in Jazz: The Infinite Art of Improvisation.* University of Chicago Press.
- Buela, H. (2017). *Songo: La Drumming de Changuito.* Latin Percussion.
- Friberg, A., & Sundström, A. (2002). "Swing ratios and ensemble timing in jazz performance." *Music Perception*, 19(3), 333-349.
- Guerrero, J. (2000). *Brazilian Percussion: Manual of Rhythms and Instrumentation.* Xerdeles Editora.
- Mauleón, R. (1993). *Salsa Guidebook for Piano and Ensemble.* Sher Music.
- Moehn, F. (2012). *Contemporary Carioca: Technologies of Mixing in a Brazilian Music Scene.* Duke University Press.
- Murphy, J. (2006). "Music in Brazil." In *Global Music Series.* Oxford University Press.
- Nettl, B. (2015). *The Study of Ethnomusicology: Thirty-Three Discussions.* University of Illinois Press.
- Olatunji, B., & Bettermann, R. (1965). *Musical Instruments of Africa.* John Day Company.
- Ortiz, F. (1950). *La Africanía de la Música Folklórica de Cuba.* Ediciones Cardenas.
- Santos, A. (2013). "Cuban Batá Drumming: Historical and Contemporary Contexts." *Latin American Music Review*, 34(1).
- Toussaint, G. (2013). *The Geometry of Musical Rhythm.* CRC Press.
- Washburne, C. (1998). "Play it con filin!: The swing and expression of salsa." *Latin American Music Review*, 19(2).

---

*Forgemaster ⚒️ — Constraint systems for rhythmic intelligence.*
