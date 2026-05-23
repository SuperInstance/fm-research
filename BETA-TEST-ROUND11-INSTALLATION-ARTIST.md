# BETA TEST ROUND 11: The Installation Artist
## Museum Exhibition Designer & Interactive Artist — "The Constraint Room"

**Beta Tester:** Museum exhibition designer, interactive artist, room-scale installation specialist  
**Date:** 2026-05-23  
**Repos Evaluated:** constraint-theory-web, fm-research, flux-tensor-midi, constraint-synth

---

## 1. Repository Evaluations

### a) Physical Instruments Paper (APPLIED-DODECET-SNAPWORKS, FINAL-BMA-DEADBAND-SNAP, PRECISION-EMERGENCE) — Gallery Viability

The research papers describe a complete theoretical framework that translates directly into physical installations:

- **The Dodecet as 12-bit register** → A physical control surface with 12 illuminated toggle switches, each representing a nibble. Visitors flip switches and watch a projection of the constraint state vector reorganize in real-time. The three nibbles (constraint state, direction, chirality) map to three distinct physical modalities: a pressure-sensitive pad, a rotary encoder, and a binary toggle bank. This is **immediate gallery material** — tactile, visual, and sonically rewarding.

- **BMA Deadband Snap ($2L$ threshold)** → The "snap" moment — where pattern recognition crystallizes — is inherently dramatic. A counting installation where visitors accumulate observations and then *hear/see* the snap at exactly $2L$ samples is pure theatre. The Fibonacci optimality ($L=2$, requiring only 4 observations) makes it fast enough for a gallery dwell time.

- **Precision Emergence Ladder** → The seven-phase transition (Aid → Surpass → Replace → Fuse → React → Understand → Transcend) is essentially a curated exhibition narrative arc. Each rung can be a station. Visitors experience the phase change themselves.

**Verdict:** These papers are the conceptual backbone of the entire exhibition. The mathematics is deep but the *experiences* it describes are visceral and physical. This is the rare theoretical framework that was practically begging to be built.

### b) Web Playground (constraint-playground.html) — Touch-Screen Kiosk Potential

The Constraint Playground is already structured as five stations (Snap, Funnel, Consensus, Rigidity, Tempo) with:
- Canvas-based interaction (touch-compatible)
- Real-time audio synthesis via Web Audio API
- Global BPM/key controls
- Visual feedback with color-coded zones
- Responsive design that scales to tablet

**As a kiosk:** It works almost out of the box. The canvas interactions (`touch-action: none` already set) are touch-ready. A 27" touch monitor mounted in a kiosk enclosure with quality headphones would be an immediate install. The "Export JSON" and "Combine All" buttons give visitors a tangible takeaway.

**What needs work for museum deployment:**
- Harder audio limiting (prevent max-volume headphone damage — mandatory for public installations)
- Session timer (auto-reset after 3 minutes idle)
- Accessibility: screen reader descriptions for each station, high-contrast mode
- Physical enclosure design to prevent damage from enthusiastic visitors (kids are *brutal* on touch screens)

**Verdict:** 85% ready for kiosk deployment. The hardest work (interaction design, audio engine, visual feedback) is done. The remaining 15% is museum-grade hardening.

### c) Audio Demos (constraint-synth/demos/) — Museum-Quality Sound?

The seven demos cover the full constraint theory pipeline: snap, funnel, consensus, rigidity, genre presets, AI jam, and evolution. Critical assessment:

- **demo_snap_effect.wav** — The moment where free pitch snaps to A₂ lattice is the single most compelling sound in the collection. In a gallery, this needs to be played through a subwoofer so visitors *feel* the quantization in their chest. The 31-second duration is perfect for attention spans.

- **demo_consensus_voices.wav** — Four voices converging from chaos to locked harmony is viscerally powerful. In a dome with four speakers (one per voice), visitors stand at the center and hear consensus form around them. This is the centerpiece audio experience.

- **demo_laman_rigidity.wav** — The three-phase structure (free → rigid → release) is perfect for a physical rigidity demonstration. Pair with a physical tensegrity structure that locks and unlocks in sync.

- **demo_ai_jam_parker_miles.wav** — The 65-second Parker/Miles dialogue is beautiful but too long for a passive kiosk. Better as ambient sound in a lounge area, or as a seated listening station with headphones and a "record sleeve" describing the agents.

**Production quality:** The synthesis is clean but the demos feel like developer artifacts. For museum deployment, they need:
- Reverb tailoring for the specific space
- Subwoofer content below 80Hz for physical impact
- Gentle fade-ins to prevent startling visitors
- LUFS normalization to -16 (broadcast standard for public spaces)

**Verdict:** Conceptually stunning. Sonically needs a mastering pass and spatial audio rendering for the installation. The raw material is excellent.

### d) Constraint Piano as REAL Piano with Hardware Mods

This is the bold one. The constraint-synth's LatticeOscillator maps lattice geometry to waveform: sine = continuous, square = Z₂ binary snap, eisenstein = A₂ hexagonal tiling. The constraint-filter applies consonance thresholds. The funnel-envelope shapes ADSR as deadband convergence.

**Hardware mod concept:** Take a real acoustic piano and add:
- **Magnetic rail above the keys** with electromagnets that physically resist motion when snap is engaged — the player *feels* the lattice pulling their fingers
- **LED strip under each key** showing snap target positions (the A₂ lattice points light up)
- **Consonance filter as physical damping** — felt dampers engage proportionally to dissonance, physically preventing dissonant intervals from sustaining
- **Funnel mode** — a servo-controlled sustain pedal that gradually locks rhythm to metronomic grid

The key insight from the synth code: every parameter has a lattice-theoretic interpretation. This isn't arbitrary hardware hacking — the physical modifications *are the theory*. The LatticeOscillator's `snap_threshold` parameter (0=soft snap, 1=hard snap) maps directly to electromagnet strength.

**Build difficulty:** High. Requires custom electro-mechanical design. But the payoff is enormous — a real piano that *physically enforces constraint theory* through touch resistance and visual guidance.

**Verdict:** This would be the viral centerpiece of the exhibition. A real piano that pushes back. Instagram gold. Budget accordingly.

### e) Consensus Module — Visitors Physically Agreeing on Notes

The consensus station (drag 4 voices into agreement) is already interactive. The physical version:

**The Consensus Table** — A round table with four stations, each with a physical slider (pitch) and a rotary knob (timbre). Four visitors each control one voice. The table surface is a projection showing the harmonic space. When all four sliders converge on the same region, the table lights up, the dissonant audio resolves to harmony, and a camera takes a photo of the team. The "Negotiate" button becomes a physical "Agree?" button that all four must press simultaneously (a literal consensus mechanism).

**What makes this work as a group experience:**
- The consensus strictness slider maps to a physical difficulty level
- Groups naturally develop communication strategies (pointing, counting down)
- The audio reward (harmony from dissonance) is immediately satisfying
- The simultaneous button press is a memorable social moment

**Flux-tensor-midi's side-channels (Nod/Smile/Frown)** add a brilliant non-verbal layer: each station has three physical buttons (nod = acknowledge, smile = approve, frown = disagree). The audio reacts to these side-channel signals before consensus is reached. This is *ensemble body language as music*.

**Verdict:** The most gallery-ready interactive of the entire collection. The software already implements the math. The physical build is straightforward (sliders + knobs + projection + buttons). This is the installation that tour groups will remember.

### f) Constraint Tarot — Physical Card-Drawing Station

The tarot HTML implements a full card-based divination system over constraint types (Lattice, Funnel, Consensus, Laman, Tempo) with:
- Animated card flip transitions
- Spread layouts (past/present/future)
- Rich visual design with gold accents and constellation backgrounds
- Per-card descriptions linking constraint types to musical/archetypal meanings

**As a physical station:** This is perfect. The translation is obvious:
- **Physical cards** (6"×10", heavy card stock, gold foil) with the constraint symbols and descriptions from the HTML
- **A velvet-draped table** with a single spotlight
- **Speaker overhead** that plays the constraint's audio demo when the card is placed on an NFC reader embedded in the table
- **A "reading cloth"** with the spread positions printed on it
- **Receipt printer** that prints the visitor's reading (constraint combination + interpretation) as a takeaway

The genius of the tarot metaphor is that it makes abstract mathematical concepts feel mystical and personal. Visitors aren't "learning about A₂ lattice snapping" — they're "drawing The Lattice card in their reading." Same knowledge, completely different emotional entry point.

**Verdict:** An absolute must-include. Low build cost, high emotional impact. The HTML is essentially the design document for the physical cards.

---

## 2. IDEATION: The Constraint Room

### A Traveling Exhibition for Science Museums

**"The Constraint Room: How Mathematics Makes Music"**

A 2,000 sq ft immersive installation touring North American science museums. Five stations, one per constraint type, each occupying a themed zone within a darkened gallery space. Visitors spend 45–90 minutes exploring how constraint — the mathematical forcing of structure from freedom — creates the music we hear.

---

### The Space

The room is dark. Not black — deep indigo, with faint constellation patterns on the ceiling that slowly shift (they're actually A₂ lattice projections). A low ambient hum — the sound of pure unconstrained noise — plays from hidden speakers throughout. As visitors interact with stations and impose constraints, the ambient sound evolves: noise becomes tone, chaos becomes rhythm, disorder becomes music. The entire room is a living demonstration of the Precision Emergence Ladder.

The floor is divided into five zones by subtle LED channels in the floor, each a different color matching the constraint type: electric blue (Snap), emerald green (Funnel), warm gold (Consensus), hot pink (Rigidity), deep purple (Tempo). Visitors follow the light path between stations.

---

### Station 1: The Snap Wall (◆ Electric Blue)

**Concept:** A 12-foot wide touch-sensitive LED wall displaying a continuous field of notes — a shimmering, undulating landscape of pitch. Visitors touch the wall to place notes. In free mode, notes go exactly where touched. Then they press the "Snap" button.

The entire field reorganizes. Notes jump to A₂ lattice positions with a satisfying physical *click* sound (the snap). The wall lights up with a hexagonal grid overlay showing the lattice. Each snapped note triggers a tone. The cumulative effect: a visitor's random scribbles become a melody, constrained into beauty.

**Physical build:**
- 12' × 8' LED matrix wall (P2.5 indoor panels, ~$15K)
- Capacitive touch overlay (~$5K)
- Subwoofer behind the wall for the physical snap impact
- Custom software adapting constraint-playground's Snap Lab to large-scale canvas

**Dwell time:** 3–5 minutes per visitor. Groups of 2–3 can collaborate on the same wall.

**Budget:** $28,000 (hardware + custom software + physical enclosure)

---

### Station 2: The Funnel Floor (◆ Emerald Green)

**Concept:** A 10' × 10' floor projection. Visitors walk onto it and their position becomes a "wandering note" — projected as a glowing dot beneath their feet with a pitch that matches their X position. A golden target dot pulses at the center (the tonic). The funnel's gravity is adjustable via a physical dial on the railing.

At low gravity, visitors can roam freely and hear their pitch wander. At high gravity, the projection visually pulls their dot toward the target, and the audio pitch slides toward the tonic. At maximum gravity, the floor essentially forces you toward the center — the projection creates a visual gravity well so compelling that visitors physically walk toward the target without realizing it.

**Physical build:**
- Floor projection system (10' × 10', rear-projection from below or ceiling-mounted short-throw) (~$12K)
- Position tracking (overhead camera + blob detection, or LiDAR) (~$5K)
- Physical railing with gravity dial and headphone jack (~$3K)
- Custom software: funnel simulator scaled to floor coordinates

**Dwell time:** 2–4 minutes. Best experienced solo or in pairs.

**Budget:** $24,000

---

### Station 3: The Consensus Table (◆ Warm Gold)

**Concept:** As described above. A round table, four stations, four visitors. Each person controls one voice (pitch slider + timbre knob). The table surface is a projection showing harmonic space. Four side-channel buttons (Nod, Smile, Frown) enable non-verbal negotiation. A camera above captures the moment of consensus.

The audio is spatial: four speakers, one per quadrant. Each visitor hears their voice closest, with others arriving from their respective directions. When consensus forms, all four speakers lock into harmony and the sound becomes unified — spatially centered, like the voices merged into one.

**Physical build:**
- Custom circular table (48" diameter, projection surface top) (~$4K)
- Four aluminum control arms with slider, knob, and three buttons (~$6K)
- Short-throw projector below table (rear-projection through surface) (~$3K)
- 4-channel audio system with speakers at each quadrant (~$3K)
- Camera + photo printer for consensus moments (~$2K)
- NFC reader + receipt printer for takeaways (~$1K)
- Software: consensus negotiation engine with spatial audio

**Dwell time:** 5–8 minutes per group. This is the social hub — visitors will queue for this one.

**Budget:** $32,000

---

### Station 4: The Rigidity Bridge (◆ Hot Pink)

**Concept:** A physical tensegrity structure — aluminum struts and steel cables forming a 6-foot tall bridge-like sculpture. Visitors press a button to engage "Laman rigidity" and the cables tension simultaneously, the structure locks solid, and a resonant tone sounds (the structure is literally singing because it's rigid — vibration modes lock into harmonic frequencies).

Release rigidity, and the structure sags. The tone warbles and detunes. Visitors can add or remove cables (physical connectors on quick-release clips) and feel the difference between a minimally rigid framework (2N-3 edges, the Laman condition) and an under-constrained one.

The genius: the same Laman graph theory that governs the audio (from demo_laman_rigidity.wav) governs the physical structure. Remove one cable below the Laman threshold and both the sculpture *and* the music go floppy.

**Physical build:**
- Custom tensegrity sculpture (aluminum struts, steel cables, quick-release connectors) (~$8K)
- Servo-actuated cable tensioning system (~$5K)
- Contact microphones on struts feeding into resonance processor (~$2K)
- LED strips on cables that illuminate when tensioned (~$1K)
- Interactive touchscreen showing the graph and Laman condition (~$3K)
- Software: graph rigidity detector + audio resonance mapping

**Dwell time:** 4–6 minutes. Visitors will add and remove cables repeatedly.

**Budget:** $28,000

---

### Station 5: The Tempo Tunnel (◆ Deep Purple)

**Concept:** A 20-foot long corridor with LED strips running the length of both walls. Visitors walk through. Beat markers flash along the LEDs at the current BPM. The visitor's footsteps are tracked via pressure sensors in the floor. When footsteps align with beat markers, the tunnel glows purple (in the pocket). When footsteps are off, it flickers red.

A funnel dial at the entrance controls strictness. At narrow funnel width, only metronomic precision counts — the tunnel is unforgiving. At wide funnel, almost anything goes. The audio: a persistent rhythmic pattern that gains clarity and body as the visitor's timing improves. Perfect timing triggers a bass drop that visitors feel in their chest.

**Physical build:**
- 20' corridor structure (modular truss, black fabric walls) (~$6K)
- LED strip arrays, both walls, full length (~$4K)
- Floor pressure sensor array (~$5K)
- Subwoofer system at tunnel exit (~$3K)
- BPM/funnel control panel at entrance (~$2K)
- Software: tempo funnel engine with real-time step detection

**Dwell time:** 2–3 minutes per pass. Visitors will re-run to improve their score.

**Budget:** $27,000

---

### The Tarot Alcove

Tucked between stations 3 and 4: a small alcove with a velvet-draped table, a single overhead lamp, and the Constraint Tarot. Six large-format cards with gold-foil constraint symbols. An embedded NFC reader plays each card's audio demo when placed on the reading cloth. A receipt printer issues the visitor's reading.

**Budget:** $8,000 (cards, table, reader, printer, fabrication)

---

### The Constraint Piano (Rotating Feature)

Not part of the core exhibition — a special engagement piece that rotates between venues. The hardware-modified acoustic piano described in evaluation (d). Booked as a performance feature: local pianists invited to play "constrained recitals" where the piano gradually increases snap, funnel, and rigidity over the course of a piece until the performer is physically fighting the instrument.

**Budget:** $75,000 (piano + custom electromechanical mods + touring case)

---

### Budget Summary

| Item | Cost |
|------|------|
| Snap Wall | $28,000 |
| Funnel Floor | $24,000 |
| Consensus Table | $32,000 |
| Rigidity Bridge | $28,000 |
| Tempo Tunnel | $27,000 |
| Tarot Alcove | $8,000 |
| Spatial audio system (whole room) | $15,000 |
| Room construction (walls, lighting, flooring) | $25,000 |
| Central server + networking | $8,000 |
| Content development + software integration | $40,000 |
| Fabrication + installation labor | $20,000 |
| Shipping cases (touring) | $12,000 |
| **Total** | **$267,000** |
| Constraint Piano (optional) | +$75,000 |
| **Grand Total with Piano** | **$342,000** |

---

### Timeline

| Phase | Duration | Milestone |
|-------|----------|-----------|
| Design Development | 8 weeks | Final designs, engineering drawings, software architecture |
| Prototyping | 12 weeks | Working prototypes of all five stations in workshop |
| Content Production | 6 weeks (parallel) | Audio mastering, visual assets, tarot cards, piano mods |
| Fabrication | 10 weeks | Physical construction, LED systems, sensors, enclosures |
| Software Integration | 8 weeks (parallel) | Custom software for each station, central control system |
| Assembly & Testing | 4 weeks | Full build in workshop, visitor testing with focus groups |
| Touring Prep | 3 weeks | Road cases, installation guides, training docs for venues |
| **Total** | **~9 months** | Ready to ship to first venue |

---

### Touring Vision

"The Constraint Room" targets the ASTC (Association of Science and Technology Centers) circuit — mid-to-large science museums with 2,000+ sq ft temporary exhibition space. Target venues: Exploratorium (SF), Museum of Science (Boston), Pacific Science Center (Seattle), Ontario Science Centre, National Museum of Mathematics (NYC), COSI (Columbus), and the touring network of Smithsonian affiliates.

Booking model: 12-week residencies, 4 venues per year, 2-year tour. The modular design (five independent stations + central audio) allows venues to configure for available space. The Constraint Piano books separately as a special event.

Educational programming: each venue receives a curriculum packet tying the five stations to middle/high school math standards (graph theory, algebra, geometry, probability). Field trip groups cycle through stations with structured worksheets. The Consensus Table doubles as a team-building exercise for corporate events.

The dream: a generation of museum visitors who understand that *constraints aren't limitations — they're the source of structure, beauty, and music*. The A₂ lattice isn't abstract math. It's the hexagonal pattern on the wall you touched that turned noise into melody. Laman rigidity isn't a graph theory theorem. It's the bridge you made sing by adding one more cable. The BMA deadband isn't a convergence bound. It's the moment you heard the pattern snap into place.

That's the exhibition. That's The Constraint Room.

---

## 3. Summary Assessment

| Component | Gallery Ready? | Notes |
|-----------|---------------|-------|
| Research papers | ✅ Conceptual backbone | Each paper is a station's theoretical foundation |
| Web playground | ✅ 85% kiosk-ready | Needs museum hardening, accessibility, session timeout |
| Audio demos | ⚠️ Needs mastering | Spatial rendering + LUFS normalization + reverb |
| Constraint piano | 🔧 Major build | Electromechanical design needed, but the payoff is enormous |
| Consensus module | ✅ Most gallery-ready | Physical build is straightforward, software exists |
| Constraint tarot | ✅ Must-include | Low cost, high emotional impact, perfect card designs ready |

**Overall:** This ecosystem has something I've never seen in a math-and-music project: a unified theoretical framework where *every interactive element is a direct physical instantiation of the same mathematics*. The A₂ lattice appears in the Snap Wall, the oscillator shapes, the floor projection, and the tarot cards. Laman rigidity governs both the audio demos and the physical bridge. The deadband funnel shapes both envelopes and the Tempo Tunnel. This coherence is what separates a great exhibition from a collection of demos. Build it.
