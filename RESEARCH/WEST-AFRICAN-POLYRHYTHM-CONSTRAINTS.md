# West African Polyrhythm and Cross-Rhythm Traditions Mapped to Constraint Theory

**Forgemaster ⚒️ | 2026-05-23 | v1**

---

## Abstract

West African polyrhythmic traditions represent some of the most sophisticated temporal constraint satisfaction systems ever developed by human culture. In ensembles spanning Ghana, Nigeria, Mali, Guinea, Cuba, Brazil, and the broader African diaspora, multiple simultaneous rhythmic streams converge under rigid structural rules — bell patterns that never vary, drum layers that interlock with mathematical precision, and tempos that emerge from embodied collective cognition rather than metronomic prescription. This paper maps five foundational constraint theory primitives — SNAP, FUNNEL, CONSENSUS, LAMAN, and TEMPO — onto the structural mechanics of West African polyrhythm, demonstrating that these traditions are not merely musical practices but instantiated constraint engines operating in real-time on human performers. We propose five novel rhythmic parameters derived from this mapping and present ten rhythmic presets encoding specific West African and diasporic traditions as constraint satisfaction profiles.

---

## 1. Polyrhythmic Systems as Constraint Architectures

### 1.1 Ewe Drumming (Ghana): Bell Pattern + Polymetric Layering

The Ewe people of southeastern Ghana and southern Togo developed one of the most analytically rich drumming traditions on the planet. The central organizing principle is the **bell timeline** (gankogui), an iron double bell that plays an unchanging asymmetrical pattern across twelve eighth-note pulses. In the Agbadza style, the bell pattern distributes seven strokes across twelve pulses with the additive structure 2+2+1+2+2+2+1, producing the phrasing LLSLLLS (long-long-short-long-long-long-short).

This single pattern generates the entire polymetric field:

- The **sogo** (lead drum) improvises within constraints proportional to one bell cycle
- The **kidi** (support drum) plays a fixed interlocking pattern
- The **kagan** (small drum) maintains a steady subdividing pulse
- The **atsimevu** (master drum) issues calls and variations

The critical insight: the bell pattern creates a **3:2 hemiola** against any straight duple subdivision. Every other instrument must satisfy the constraint of aligning with this asymmetrical timeline while maintaining their own internal logic. The result is not chaos but a stable polymetric field where multiple time signatures coexist without ever resolving into a single meter.

### 1.2 Yoruba Talking Drums (Nigeria): Pitch + Rhythm as Dual Constraint Channels

The Yoruba dùndún (talking drum) system presents a fundamentally different constraint architecture: **two simultaneous constraint channels** operating on a single instrument. The hourglass-shaped drum is struck with a curved stick while the player's arm squeezes and releases leather tension cords, modulating pitch in real time.

Because Yoruba is a tonal language with three primary tone levels (low, middle, high), the drum simultaneously satisfies:

1. **Rhythmic constraints** — temporal placement of strikes
2. **Tonal constraints** — pitch contour mimicking speech intonation

The simultaneity is not optional. In "talking" mode, a dùndún player produces meaningful Yoruba phrases where the rhythmic and tonal channels are co-dependent: changing the rhythm changes the syllable structure, changing the pitch changes the word meaning. This is a **coupled constraint system** — two constraint channels that cannot be independently satisfied.

The bata drum ensemble extends this to three drums (iyá, itótele, okónkolo) in religious contexts (Santería), where the drums literally "speak" to the orishas. The constraint load is immense: liturgical correctness requires specific rhythmic-tonal phrases at specific ceremonial moments, creating a time-critical coupled constraint problem.

### 1.3 Djembe Ensembles (Mali/Guinea): Hierarchical Polyrhythmic Architecture

The djembe ensemble tradition of the Mande peoples (spanning Mali, Guinea, Burkina Faso, Ivory Coast) implements a **hierarchical constraint system** with clearly defined layers:

**Dunun family (bass drums):**
- **Kenkeni** (highest) — steady pulse, often the simplest pattern, acts as temporal anchor
- **Sangban** (middle) — more syncopated, creates primary polyrhythmic tension
- **Dundunba** (lowest) — deep bass notes, emphasizes structural downbeats, allows variation

**Djembe voices:**
- 2-3 accompaniment djembes playing fixed interlocking parts
- 1 lead djembe responsible for cues, breaks, solos, and dancer accompaniment

**Bell:** Each dunun typically has an attached iron bell, maintaining an independent timeline layer.

The total system: 3 dunun + 3 bells + 3 djembe = **9 simultaneous constraint layers**, all interlocking. The lead djembe operates with greater freedom but must still satisfy alignment constraints with every other layer. The dunun patterns are typically more rigid (higher LAMAN value), while the lead djembe has more latitude but is funneled by the collective pattern.

### 1.4 Standard Polyrhythmic Ratios as Constraint Problems

The foundational polyrhythmic ratios of West African music map directly to constraint satisfaction problems:

| Ratio | Name | Constraint Character |
|-------|------|---------------------|
| 3:2 | Hemiola | The fundamental cross-rhythm; 3 pulses in the space of 2 |
| 4:3 | Sesquialtera | Quarter-note triplets against dotted rhythm |
| 5:4 | Quintuplet cross | Creates maximum tension in 4/4 contexts |
| 7:4 | Septuplet cross | Advanced polyrhythm, found in Ewe and Fon traditions |

Each ratio defines a **periodic alignment constraint**: the two rhythmic streams must agree at a common multiple of their respective cycle lengths. For 3:2, alignment occurs every 6 pulses; for 4:3, every 12; for 5:4, every 20; for 7:4, every 28. The alignment point is where CONSENSUS resolves — the moment when all streams agree on a shared downbeat.

The tension between alignment points is not a bug but a feature. West African musical aesthetics value the "stretch" — the controlled dissonance between rhythmic streams that resolves into periodic agreement. This is constraint satisfaction with deliberate, structured violation windows.

### 1.5 Clave: The African Diaspora's Constraint Backbone

The Cuban clave patterns — direct descendants of West African bell timelines — demonstrate how a single five-stroke pattern can serve as the **rigid core** of an entire rhythmic ecosystem:

**3-2 Son Clave:** Strokes on beats 1, 2&, 4, 6, 7 (in two bars of 4/4). The three-side (first bar) carries more strokes; the two-side (second bar) is sparser. The final stroke of the three-side lands on the downbeat of beat four.

**2-3 Rumba Clave:** Strokes on beats 2, 3, 5, 6&, 8. The third stroke on the three-side is delayed to the "and" of beat four (versus the downbeat in son clave), creating greater syncopation and forward motion.

The clave functions identically to the West African bell pattern: it is **sacrosanct**. All other parts — piano montunos, bass tumbaos, conga patterns, brass figures — must align with the clave or risk being rhythmically "wrong" (a situation Cuban musicians call *montuno cruzado* or crossing the clave). The clave is the **LAMAN rigidity constraint** of Afro-Cuban music: it provides the fixed structural backbone against which all other parts are verified.

---

## 2. Constraint Mapping: Five Primitives in Rhythmic Space

### 2.1 SNAP → Rhythmic Grid Quantization

In constraint theory, SNAP maps a continuous input to the nearest point on a discrete lattice. Applied to rhythm, SNAP is **temporal quantization**: the mapping of a performer's imprecise strike time to the nearest grid point on the rhythmic subdivision lattice.

In Eisenstein integer theory, snap operates on pitch-class space using the hexagonal lattice Z[ω]. For rhythm, the lattice is **temporal**: a subdivision grid where each axis represents a different temporal layer. A 16th-note grid at 120 BPM creates a lattice with spacing 125ms. SNAP maps the drummer's actual strike (say, 127ms late) to the nearest grid point (125ms), absorbing the 2ms error.

**The West African SNAP is culturally conditioned.** Ewe drummers do not snap to a metronomic grid — they snap to the bell pattern, which is asymmetrical. The SNAP lattice is not uniform; it is warped by the timeline pattern. Grid points near bell strokes are "stronger attractors" than points between bell strokes. This creates a **non-uniform snap field** where the quantization strength varies across the cycle.

The snap deadband prevents double-triggering from imprecise strikes (tremors, bounce, involuntary movements) — exactly as in the Eisenstein snap for pitch. A drummer who strikes slightly early and slightly late in rapid succession should not generate two events if the intent was one.

### 2.2 FUNNEL → Gravitational Pull Toward the "One"

The FUNNEL primitive narrows the possibility space toward a target state. In rhythmic constraint theory, the FUNNEL is the **gravitational pull toward the downbeat** — the "one."

West African music exhibits a clear FUNNEL dynamic. Multiple rhythmic streams diverge and create polyrhythmic tension, but they are drawn back toward periodic alignment points. The alignment is not optional; it is enforced by the shared timeline. In Ewe music, the low bell stroke serves as the primary gravitational attractor — all parts move toward it for cadential resolution.

The FUNNEL operates at multiple timescales:

- **Micro-funnel:** Each subdivision cycle pulls toward the nearest strong beat
- **Meso-funnel:** Each bell cycle pulls toward its final stroke (resolution)
- **Macro-funnel:** Each phrase pulls toward the lead drum's cadential signal

The funnel rate (how aggressively parts converge) varies by tradition. Djembe music funnels hard — strong unison breaks snap everyone back to the one. Yoruba bata drumming funnels more gradually, with the iyá (lead drum) guiding resolution over longer phrases.

### 2.3 CONSENSUS → Polymetric Alignment: Multiple Meters Converging Periodically

CONSENSUS in constraint theory requires multiple independent agents to agree on a shared state. In polyrhythmic music, CONSENSUS is the **periodic alignment of polymetric streams**.

Consider an ensemble playing simultaneously in 3/4 and 4/4 (a 3:2 polymeter). These meters are independent — they have different downbeat placements and different cycle lengths. But every 12 pulses (LCM of 3 and 4), they align. That alignment is CONSENSUS.

The beauty of West African polymeter is that CONSENSUS is both guaranteed and insufficient. The mathematical structure ensures periodic alignment (the LCM always exists), but the musical texture between alignment points is where the art lives. The CONSENSUS resolution is the骨架 — the skeleton — and the inter-rhythmic space is the flesh.

Multi-drum consensus in djembe ensembles works differently. Here, 6-9 independent parts must all converge on the break signal issued by the lead djembe. The consensus is not mathematical periodicity but **social cueing**: the lead player signals, and all other players must snap to unison within a single beat. This is distributed consensus with a leader — analogous to Byzantine consensus with a designated coordinator.

### 2.4 LAMAN → Bell Pattern Rigidity: The Sacred Timeline

The LAMAN constraint ensures structural rigidity — sufficient constraints to prevent the system from deforming. In West African music, the **bell pattern is the LAMAN constraint**: it provides the rigid structural backbone that makes the entire polyrhythmic system stable.

The bell timeline is sacred. It does not vary. It does not adapt. It is the fixed lattice against which all other parts are measured. This is not a cultural arbitrary — it is a mathematical necessity. If the timeline is allowed to deform, the polyrhythmic field loses its reference frame and collapses into noise. The LAMAN rigidity of the bell pattern is what allows 6-9 other parts to operate with varying degrees of freedom while maintaining coherence.

Different traditions have different LAMAN budgets:

- **Ewe Agbadza:** Bell is absolutely rigid (variation budget = 0). All variation happens in the drum layers.
- **Djembe Kuku:** Bell is rigid, but the dundunba (bass drum) is allowed limited variation.
- **Afrobeat:** The "bell" is typically a shaker or rhythm guitar pattern that is quite rigid, but the horn section and bass have significant freedom.
- **Gwo Ka:** No separate bell — the boula drum IS the timeline, and it is rigid. The maké drum improvises against it.

The LAMAN value of a tradition can be quantified as the ratio of rigid layers to total layers. Ewe drumming has the highest LAMAN ratio (the bell never varies); Afrobeat has a lower ratio (more parts have freedom).

### 2.5 TEMPO → Tempo Giusto: The "Right" Tempo Is Felt, Not Chosen

The TEMPO primitive in constraint theory governs the rate of constraint evaluation. In West African rhythm, tempo is not a parameter to be set but a **collectively perceived property** — what Western classical theory calls *tempo giusto* (the "just" or "right" tempo).

Vijay Iyer's research on embodied cognition in West African rhythm demonstrates that the "feel" of a rhythm is not a passive perceptual event but an active, whole-body construction. The tempo emerges from the communal interplay of dancers, singers, and drummers. It is felt through movement, not measured by a clock.

In constraint terms: TEMPO is not an external parameter but an **emergent property of the constraint system itself**. When the bell pattern, drum layers, and dance patterns reach mutual satisfaction, the system settles into a natural frequency. This frequency is "right" not because it matches a metronome marking but because all constraints are simultaneously satisfied at that rate and no other.

The consequences are profound:

1. **Tempo is not adjustable independently.** Changing the tempo without changing the feel requires restructuring the entire constraint system.
2. **Microtiming IS the system.** The systematic microrhythmic variations that characterize West African performance (playing slightly behind or ahead of the grid) are not deviations from the tempo but constitutive features of it. They are part of the TEMPO constraint.
3. **The body is the clock.** TEMPO is embodied — felt through dance, breath, and collective movement rather than cognitively tracked.

---

## 3. Novel Rhythmic Parameters

Constraint theory suggests new parameters for describing and controlling rhythmic systems. These go beyond traditional BPM and time-signature specifications to capture the structural depth of polyrhythmic traditions.

### 3.1 Swing Factor per Subdivision

Standard Western music treats swing as a binary parameter (straight vs. swung 8th notes). West African rhythm requires **per-subdivision swing control**:

- **16th-note swing:** In djembe music, the second 16th note of each beat is often delayed, creating a lilt
- **Triplet swing:** Ewe bell patterns create implicit triplet swing against duple subdivisions
- **Compound swing:** 12/8 rhythms (Kuku, Agbadza) have their own swing profiles where dotted values are stretched

Each subdivision level can have an independent swing factor (0.0 = perfectly straight, 1.0 = maximum swing). The interaction between swing factors at different levels creates the characteristic "groove" of each tradition.

**Constraint mapping:** Swing factor modifies the SNAP lattice. A swing value of 0.67 at the 8th-note level warps the temporal grid so that the second 8th note in each pair lands at 2/3 of the beat rather than 1/2.

### 3.2 Groove Pocket Width

The "pocket" is the temporal tolerance around each grid point within which a strike is considered "in time." In funk and Afrobeat, the pocket is famously tight — bass and drums must be nearly perfectly aligned. In some djembe traditions, the pocket is wider, allowing more individual expression within the groove.

**Groove pocket width (σ)** defines the standard deviation of acceptable timing around each grid point. A narrow pocket (σ ≈ 5ms) demands mechanical precision. A wide pocket (σ ≈ 30ms) allows more expressive microtiming.

The pocket width interacts with SNAP: the snap deadband should be at least as wide as the pocket, otherwise legitimate expressive timing variations get quantized away.

### 3.3 Cross-Rhythm Density

**Cross-rhythm density (ρ)** measures the number of simultaneous polyrhythmic layers in operation. It is defined as the number of independent periodic streams active at any moment:

- ρ = 1: Monophonic rhythm (single line)
- ρ = 2: Basic polyrhythm (e.g., 3:2 bell + straight pulse)
- ρ = 3-4: Standard West African ensemble (bell + 2-3 drums)
- ρ = 5-7: Dense ensemble (djembe + dunun family + bells)
- ρ = 8+: Maximum density (Afrobeat, large samba bateria)

Higher density increases constraint load exponentially. Each additional layer must satisfy alignment constraints with every other layer at their respective LCM points.

### 3.4 Timeline Variation Budget

The **timeline variation budget (β)** quantifies how much the primary timeline (bell pattern) is allowed to deviate from its canonical form:

- β = 0: Bell is absolutely rigid (Ewe Agbadza, Cuban Son Clave)
- β = 0.1: Minimal variation allowed (ornamental microtiming, no structural change)
- β = 0.3: Moderate variation (dunun bass patterns can shift accents)
- β = 0.5: Significant variation (lead drum can reshape the timeline)
- β = 1.0: No fixed timeline (free improvisation)

This parameter is directly related to LAMAN rigidity: lower β = higher LAMAN constraint on the timeline. Most West African traditions operate at β = 0 for the bell and β = 0.2-0.4 for the drum layers.

### 3.5 Call-Response Timing Gap

West African music is fundamentally **conversational**. The call-response structure between lead and ensemble instruments introduces a temporal parameter: the **gap** between call and response.

**Call-response gap (γ)** measures the delay between a lead signal and the ensemble's response:

- γ = 0: Simultaneous response (unison breaks in djembe)
- γ ≈ 1 beat: Standard response (Afrobeat horn stabs, samba calls)
- γ ≈ 1 cycle: Extended response (Yoruba ceremonial drumming, where the "response" may be an entire phrase)

The gap is not random — it is culturally coded. In djembe tradition, specific break signals have specific response timings. A "e" call (low tone) gets an immediate response; a "rang" call (slap-tone-slap) gets a one-beat-delayed response.

---

## 4. Ten Rhythmic Presets as Constraint Profiles

Each preset encodes a specific tradition as a constraint satisfaction profile with parameters for the five novel rhythmic parameters plus the five constraint primitives.

### 4.1 Ewe Agbadza

```
Origin: Ghana/Togo (Ewe people)
Meter: 12/8 (felt as 4 bell cycles)
Layers: bell (gankogui) + sogo + kidi + kagan + atsimevu = 5
Polyrhythm: 3:2 hemiola (bell against duple subdivision)
LAMAN: β = 0 (bell never varies)
SNAP: Non-uniform grid warped by bell pattern
FUNNEL: Strong pull to low bell stroke (cycle end)
CONSENSUS: Alignment every 12 pulses (all layers)
TEMPO: ~100-120 BPM, felt through dance
Swing: Triplet swing on subdivisions (factor ≈ 0.6)
Pocket width: σ ≈ 15ms (moderate precision)
Cross-rhythm density: ρ = 4
Call-response gap: γ ≈ 0 (tight ensemble response)
```

The Agbadza is the archetypal Ewe rhythm — an 12/8 war dance pattern that demonstrates the full constraint architecture. The bell's seven strokes across twelve pulses create an asymmetrical timeline that generates polymetric potential against any straight duple or triple subdivision. The sogo (lead drum) has the most freedom but must funnel toward the bell's low stroke. All other drums maintain fixed interlocking patterns with zero variation budget.

### 4.2 Yoruba Bata

```
Origin: Nigeria (Yoruba people, religious context)
Meter: 12/8 or free meter (liturgical)
Layers: iyá + itótele + okónkolo = 3 drums, each dual-headed
Polyrhythm: Variable (3:2, 4:3, free polymeter)
LAMAN: β = 0.1 (liturgical patterns are near-fixed)
SNAP: Coupled pitch-rhythm snap (two channels simultaneously)
FUNNEL: Gradual, controlled by iyá (lead)
CONSENSUS: Alignment driven by liturgical requirements
TEMPO: Tempo giusto — determined by ceremonial context, not choice
Swing: Variable, often heavy triplet feel (factor ≈ 0.7)
Pocket width: σ ≈ 10ms (ritual precision required)
Cross-rhythm density: ρ = 3-5
Call-response gap: γ ≈ 1-2 cycles (ceremonial phrasing)
```

Bata drumming is unique in the constraint catalog because each drum operates on **two simultaneous channels** (two heads, played with both hands, producing different pitches). The iyá (largest drum) has the added constraint of "talking" — producing Yoruba tonal phrases. This is a coupled pitch-rhythm constraint system with liturgical correctness requirements, making it one of the most constraint-dense traditions in the catalog.

### 4.3 Djembe Kuku

```
Origin: Guinea (Forest Region, Beyla area, Malinke people)
Meter: 12/8 or fast 4/4 with triplet feel
Layers: 3 djembe + 3 dunun (kenkeni, sangban, dundunba) + bells = 7-9
Polyrhythm: 3:2, with interlocking djembe parts creating additional density
LAMAN: β = 0 (bell/dunun), β = 0.2 (accompaniment djembes), β = 0.6 (lead djembe)
SNAP: Moderate — joyful celebration allows looser quantization
FUNNEL: Hard funnel on unison breaks; softer during cycles
CONSENSUS: Strong — break signals require instant alignment from all
TEMPO: ~120-140 BPM, upbeat celebration tempo
Swing: Lilting 12/8 swing (factor ≈ 0.55)
Pocket width: σ ≈ 20ms (groove over precision)
Cross-rhythm density: ρ = 6-8
Call-response gap: γ ≈ 0 (breaks demand immediate response)
```

Kuku is a celebration rhythm — historically played by women returning from fishing. The densest preset in terms of active layers (up to 9 simultaneous parts), Kuku demonstrates how high cross-rhythm density can coexist with joyful, accessible music. The constraint satisfaction is rigorous but the result feels effortless.

### 4.4 Djembe Sofa

```
Origin: Guinea (Upper Guinea, Kouroussa/Kankan/Faranah, Malinke people)
Meter: 4/4, moderate to slow
Layers: 3 djembe + 3 dunun + bells (originally bolon + dunun, djembe added later)
Polyrhythm: Subtle 3:2 undertones, primarily linear
LAMAN: β = 0 (dunun), β = 0.3 (accompaniment djembes), β = 0.5 (lead)
SNAP: Precise — warrior music demands discipline
FUNNEL: Strong, gradual pull — tension builds toward resolution
CONSENSUS: Very strong — structured progression from signal through intro to main pattern
TEMPO: ~80-100 BPM, deliberate and measured
Swing: Minimal (factor ≈ 0.2), more straight than swung
Pocket width: σ ≈ 12ms (tight, disciplined)
Cross-rhythm density: ρ = 4-5
Call-response gap: γ ≈ 1 beat (structured call-response)
```

Sofa is the warrior rhythm — originally played for horseback warriors before and after battle. Its constraint profile reflects military discipline: minimal swing, tight pockets, strong funnel dynamics, and a structured progression from signal to main pattern. The bolon (a string instrument similar to a contrabass) provides additional harmonic constraints in traditional contexts.

### 4.5 Cuban Son Clave (3-2)

```
Origin: Cuba (Eastern Cuba, Afro-Cuban son tradition)
Meter: 4/4 (two-bar cycle)
Layers: clave + bass + guitar/tres + percussion (bongos, maracas, güiro)
Polyrhythm: 3:2 (the clave itself is a 3-against-2 structure)
LAMAN: β = 0 (clave is sacred — never reversed within a performance)
SNAP: Moderate, with characteristic Cuban "ayorno" (playing slightly behind)
FUNNEL: Strong pull to the "two-side" of the clave
CONSENSUS: All parts align with clave orientation (3-2 or 2-3, not both)
TEMPO: ~90-110 BPM, son tempo
Swing: Minimal on paper, but ayorno microtiming creates implicit swing (factor ≈ 0.3)
Pocket width: σ ≈ 20ms (Cuban feel tolerates more deviation)
Cross-rhythm density: ρ = 3-4
Call-response gap: γ ≈ 1-2 beats (montuno section call-response)
```

The 3-2 son clave is the foundation of Cuban popular music. Its five strokes (three in the first bar, two in the second) create an asymmetrical timeline that functions identically to the West African bell pattern — with the crucial difference that the clave's asymmetry is between bars rather than within a single cycle. All parts (bass tumbao, piano montuno, horn lines) must align with the clave or risk *cruzado* (crossing the clave).

### 4.6 Cuban Rumba Clave (2-3)

```
Origin: Cuba (Havana and Matanzas, Afro-Cuban rumba tradition)
Meter: 4/4 (two-bar cycle)
Layers: claves + cajón/quinto + tumbadora + salidor + vocal call-response
Polyrhythm: 3:2 with greater syncopation (delayed third stroke)
LAMAN: β = 0 (clave rigid), β = 0.4 (quinto improvisation)
SNAP: Loose — rumba celebrates individual microtiming
FUNNEL: Weaker than son — rumba thrives on sustained tension
CONSENSUS: Clave-aligned, but with more tolerance for ambiguity
TEMPO: ~100-130 BPM (varies by rumba type: yambú slow, guaguancó medium, columbia fast)
Swing: Heavier than son (factor ≈ 0.5)
Pocket width: σ ≈ 25ms (wide pocket, expressive)
Cross-rhythm density: ρ = 4-5
Call-response gap: γ ≈ 1-4 beats (vocal call-response central to rumba)
```

The rumba clave differs from the son clave by a single stroke placement: the third stroke on the three-side is delayed by one 8th note (from the downbeat of beat 4 to the "and" of beat 4). This single-grid-point shift creates a dramatically different feel — more syncopated, more forward-moving, less resolved. In constraint terms, the FUNNEL is weaker: the rumba clave creates a timeline where the gravitational pull toward resolution is less immediate, sustaining polyrhythmic tension longer.

### 4.7 Brazilian Samba

```
Origin: Brazil (Rio de Janeiro, Bahia; African roots in Yoruba, Congo, Angola traditions)
Meter: 2/4 (felt in 16th-note subdivisions)
Layers: surdo (3 sizes) + tamborim + agogô + reco-reco + caixa + repinique + chocalho = 10+
Polyrhythm: Multiple simultaneous (3:2 from agogô, duple surdo pulse, syncopated tamborim)
LAMAN: β = 0 (surdo marcação — the bass pulse is sacred), β = 0.3 (tamborim), β = 0.5 (repinique)
SNAP: Grid-aligned but with characteristic samba swing (16th notes slightly uneven)
FUNNEL: Strong pull to beat 2 (the surdo de marcação defines the "one" of samba)
CONSENSUS: Massive distributed consensus — 200+ percussionists in a bateria
TEMPO: ~100-120 BPM for samba enredo; variable for pagode
Swing: Samba swing on 16th notes — first and third slightly long, second and fourth slightly short (factor ≈ 0.4)
Pocket width: σ ≈ 15ms (surdo tight, tamborim looser)
Cross-rhythm density: ρ = 8-12
Call-response gap: γ ≈ 1-2 beats (cuíca and repinique calls)
```

The Brazilian samba bateria is the **highest cross-rhythm density** in the preset catalog. A typical Rio carnival bateria has 200-400 percussionists across 8-10 instrument types, all maintaining independent parts that must collectively produce a unified groove. The surdo de marcação (marking surdo) plays the rigid LAMAN backbone — beats 1 and 2 (with emphasis on beat 2, the "one" of samba). The tamborim, agogô, and other high instruments create the polyrhythmic surface. The consensus mechanism is remarkable: with no conductor, 300+ players maintain alignment through the shared surdo pulse and visual cuing from the mestre (director).

### 4.8 Highlife (Ghana)

```
Origin: Ghana (Akan, Ga, Ewe peoples; merged with Western instruments in 1920s-1950s)
Meter: 4/4 or 12/8
Layers: guitar (palm-pick pattern) + bass + drums (kit) + percussion + horns + vocals
Polyrhythm: 3:2 from guitar pattern against 4/4 drum kit
LAMAN: β = 0 (guitar timeline), β = 0.3 (drums), β = 0.5 (horns)
SNAP: Moderate — combines African timeline rigidity with Western groove feel
FUNNEL: Strong pull to downbeat, but guitar pattern creates continuous polymetric tension
CONSENSUS: All parts lock to the guitar timeline (which functions as the "bell")
TEMPO: ~110-130 BPM, danceable
Swing: Moderate (factor ≈ 0.35), 16th-note feel
Pocket width: σ ≈ 18ms
Cross-rhythm density: ρ = 4-6
Call-response gap: γ ≈ 1-2 beats (vocal call-response, horn stabs)
```

Highlife is the fusion preset — West African timeline constraint theory applied to Western instruments. The electric guitar's palm-picking pattern (typically a 3:2 pattern in 4/4 time) functions as the bell timeline, providing the LAMAN backbone. The drum kit, bass, horns, and vocals all lock to this pattern. Highlife demonstrates that the constraint architecture is portable: the same structural principles that organize an Ewe drum ensemble can organize a modern electric band.

### 4.9 Afrobeat (Nigeria)

```
Origin: Nigeria (Fela Kuti, Lagos, 1970s; Yoruba, highlife, jazz, funk fusion)
Meter: 4/4 (extended multi-section forms, 10-30 minute pieces)
Layers: rhythm guitar (2-3) + bass + drums + percussion (shaker, congas) + horns (3-5) + keyboards + vocals
Polyrhythm: Dense — multiple guitars create interlocking 3:2 patterns, horns add counter-rhythms
LAMAN: β = 0.1 (shaker/rhythm guitar timeline), β = 0.3 (bass), β = 0.6 (horns), β = 0.8 (tenor solo)
SNAP: Loose pocket, deep groove — Fela famously valued feel over precision
FUNNEL: Extended — tension builds over many bars before resolving to the one
CONSENSUS: Band consensus through repetitive ostinatos — the groove is the consensus
TEMPO: ~95-115 BPM, deep mid-tempo
Swing: Heavy 16th-note swing (factor ≈ 0.5)
Pocket width: σ ≈ 25ms (wide, feel-oriented)
Cross-rhythm density: ρ = 7-10
Call-response gap: γ ≈ 2-4 beats (vocal call-response central to Afrobeat)
```

Afrobeat is the maximal preset — the highest total constraint load in the catalog. Fela Kuti's bands typically featured 10-15 musicians, each maintaining an independent rhythmic strand that collectively produced a unified groove. The rhythm guitars played interlocking patterns (each guitar gets a different fragment of the timeline, and together they create the full bell pattern — a spatial distribution of the LAMAN constraint across multiple players). The horns added counter-rhythmic hits. The bass held down a repetitive ostinato that functioned as both melodic foundation and rhythmic anchor. Afrobeat demonstrates that extreme cross-rhythm density can feel powerful rather than chaotic when the LAMAN backbone is strong.

### 4.10 Gwo Ka (Guadeloupe)

```
Origin: Guadeloupe (French Caribbean; West African roots from Congo, Sierra Leone, Senegal)
Meter: Variable — seven fundamental rhythms with different meters
Layers: boula (timeline drum) + maké (improvising drum) + chacha (rattle) + tibwa (sticks) + vocals
Polyrhythm: 3:2 and free polymeter depending on rhythm type
LAMAN: β = 0 (boula — the timeline drum is sacred), β = 0.5 (maké improvises freely)
SNAP: Wide — Gwo Ka values raw expression over grid precision
FUNNEL: Varies by rhythm type — Kaladja (slow, weak funnel), Léwoz (warrior, strong funnel)
CONSENSUS: Boula-driven — all parts lock to the boula pattern
TEMPO: Tempo giusto — each of the seven rhythms has its own "right" tempo
Swing: Heavy (factor ≈ 0.5-0.7), very free rhythmic feel
Pocket width: σ ≈ 30ms (widest pocket in the catalog)
Cross-rhythm density: ρ = 3-4 (sparse but intense)
Call-response gap: γ ≈ 1-2 cycles (vocal call-response in Creole)
```

Gwo Ka is the **minimal maximal** preset: minimal layers (typically just two drums plus voice) but maximal expressive intensity within those layers. The boula drum plays the rigid timeline; the maké drum improvises freely against it. This is LAMAN rigidity with only one rigid element and one free element — the simplest possible constraint architecture that still generates polyrhythmic complexity. The seven fundamental rhythms (Kaladja, Menndé, Léwoz, Padjanbèl, Woulé, Graj, Toumblak) each encode a different constraint profile, from the sorrowful Kaladja to the warrior Léwoz to the joyous Toumblak.

---

## 5. Theoretical Implications

### 5.1 Rhythm as Constraint Satisfaction

The central thesis of this mapping is that West African polyrhythmic traditions are not merely musical practices that *can be described* by constraint theory — they *are* constraint satisfaction systems, instantiated in human performers rather than silicon. Each ensemble is a constraint engine running in real time:

- **SNAP** quantizes imprecise human timing to the grid defined by the timeline
- **FUNNEL** pulls all parts toward periodic alignment points
- **CONSENSUS** resolves the polymetric field at shared alignment points
- **LAMAN** enforces timeline rigidity as the structural backbone
- **TEMPO** emerges from the collective constraint satisfaction rather than being imposed

### 5.2 The Eisenstein Temporal Lattice

The Eisenstein integer lattice Z[ω] used for pitch-class snap has a natural temporal analogue. In 12/8 time with 16th-note subdivisions, the temporal grid forms a hexagonal pattern where each subdivision level provides one "axis." The snap function maps imprecise strike times to the nearest node on this temporal lattice, with the bell pattern warping the lattice to create non-uniform attraction fields.

The covering radius of the temporal lattice (the maximum distance from any point to the nearest lattice node) defines the system's timing tolerance — the groove pocket width. Just as the Eisenstein lattice's covering radius of 1/√3 ≈ 0.577 defines the maximum snap error in pitch space, the temporal covering radius defines the maximum acceptable timing deviation.

### 5.3 Cross-Rhythm as Phase Space

Each polyrhythmic ratio (3:2, 4:3, 5:4, 7:4) defines a trajectory through a phase space where the x-axis is the slower pulse and the y-axis is the faster pulse. The trajectory traces a Lissajous figure that closes after LCM(n,m) pulses. The alignment point (CONSENSUS resolution) occurs when the trajectory passes through the origin.

Different traditions favor different regions of this phase space:

- Ewe and Fon music clusters around 3:2 (low-order polyrhythm, fast LCM)
- Yoruba ceremonial music explores 4:3 and 5:4 (higher-order, slower LCM)
- Some advanced djembe traditions incorporate 7:4 (high-order, very slow LCM = maximum tension)

### 5.4 The Variation Budget as Freedom

The timeline variation budget (β) creates a natural hierarchy within any ensemble:

1. **β = 0 (Bell/Timeline):** The fixed lattice. No freedom.
2. **β ≈ 0.1-0.2 (Foundation drums):** Minimal freedom. Microtiming only.
3. **β ≈ 0.3-0.5 (Accompaniment):** Moderate freedom. Pattern variation allowed.
4. **β ≈ 0.6-0.8 (Lead):** Significant freedom. Soloing, calls, signals.
5. **β ≈ 1.0 (Voice/Dance):** Maximum freedom. Unconstrained expression.

This hierarchy maps directly to the constraint engine's priority stack: higher β values mean lower constraint priority, which means the constraint solver resolves their conflicts last.

---

## 6. Conclusion: The Drum Is the Compiler

West African polyrhythmic traditions have been solving constraint satisfaction problems in real time for centuries — using human performers as the compute substrate, bell patterns as the rigid lattice, and collective embodied cognition as the solver. The mapping to constraint theory is not a reduction but a revelation: it shows that the same mathematical structures that organize pitch in Eisenstein space organize time in rhythmic space.

The ten presets in this catalog are not museum pieces. They are constraint profiles — executable specifications for a rhythmic constraint engine. Each one encodes centuries of cultural knowledge as a set of parameter values: how rigid the timeline, how wide the pocket, how dense the cross-rhythms, how hard the funnel pulls, how the swing warps the grid.

The drum is the compiler. The bell is the type system. The ensemble is the runtime. And the music is the proof that the constraints are satisfiable.

---

## References

- Locke, D. "Musical Rhythm of Agbadza Songs." *Cambridge Companion to Rhythm*.
- Iyer, V. "Microstructures of Feel, Macrostructures of Sound: Embodied Cognition in West African and African-American Music." Harvard University.
- Anku, W. "Circles of Time: The Rhythmic Principles of African Music." *Journal of Music Theory*.
- Chernoff, J.M. *African Rhythm and African Sensibility*. University of Chicago Press, 1979.
- Nketia, J.H.K. *The Music of Africa*. W.W. Norton, 1974.
- Arom, S. *African Polyphony and Polyrhythm*. Cambridge University Press, 1991.
- Toussaint, G. "The Geometry of Musical Rhythm." *Proceedings of Bridges*, 2005.
- Konaté, F. and Ott, T. *Rhythmen der Malinke*. Freiburg, 1997.
- Keïta, M. *A Life for the Djembe*. Arun-Verlag, 2004.
- Rose, D. "Gwoka: Music, Song, Dance and Cultural Practice." UNESCO Intangible Heritage, 2014.

---

*Forgemaster ⚒️ — constraint theory sounds good*
