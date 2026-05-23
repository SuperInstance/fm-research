# Physical Instruments for Constraint Primitives

> Conceptual prototypes and build plans for tangible interfaces that embody each constraint type in the FM constraint framework.

---

## Introduction

Constraint theory is abstract. You can read about SNAP operations, funnel functions, consensus networks, and rigidity theorems — but reading about rigidity is nothing like *feeling* a structure resist deformation under your hands. These instruments close that gap.

Each instrument is designed around a single constraint primitive. The constraint isn't simulated on a screen — it *is* the physics of the device. When you play the Lattice Piano, the lattice positions are mechanical detents your fingers must push through. When you roll a ball in the Gravity Well, the shape of the bowl *is* the funnel function.

These are teaching instruments first, musical instruments second. But the best teaching happens when you're having fun, so each one is designed to be genuinely playable.

**Build difficulty:** All instruments are achievable in a weekend with basic maker tools (3D printer, soldering iron, Arduino). None require specialized fabrication beyond what a hackerspace provides.

**Cost targets:** $50–$800 depending on instrument. Budget builds are noted where applicable.

---

## 1. SNAP — "The Lattice Piano"

### Concept

A keyboard where each key snaps to discrete lattice positions. Unlike a normal piano with 12 keys per octave, the Lattice Piano has continuous keys — but they *resist* movement between valid lattice points. The player feels the A₂ lattice geometry in their fingers.

### Mechanism

Each key is a slider that rides on a cam shaft. The cam has notches (detents) cut at positions corresponding to A₂ lattice points in pitch space. A spring presses a follower against the cam, creating tactile snap points.

**Key components:**
- **Cam shaft:** One per key, 3D printed with detent profile matching the lattice. Different cams for different lattice resolutions (12-TET, 19-TET, 31-TET, continuous A₂).
- **Spring-loaded follower:** Provides snap force. Spring tension is adjustable — light for subtle feel, heavy for unmistakable snap.
- **Hall effect sensor:** Reads key position continuously (no quantization noise from switches).
- **Microcontroller:** Maps continuous position to nearest lattice point, outputs MIDI.

**The snap feel:** Between lattice points, the follower rides on the cam's slope — the key resists but allows movement. At a lattice point, it drops into a detent with a satisfying click. The player *must* push deliberately to play between lattice points, making the constraint physically tangible.

### Musical Use

- **Feel the lattice in your fingers.** Play a scale and feel how lattice points are distributed in pitch space.
- **Feel microtonal tension.** Switch to a higher-resolution lattice (31-TET) and feel the denser snap pattern.
- **Compose by constraint.** The snap points literally constrain what's easy to play. Melodies that follow the lattice flow naturally; ones that don't require physical effort.

### How This Teaches Constraint Theory

SNAP is the operation of quantizing continuous values to a discrete lattice. On paper it's `snap(x, L)` — function mapping to nearest lattice point. On the Lattice Piano, your finger *is* `x`, and the cam mechanism *is* `L`. You feel the basin of attraction around each lattice point (the region where the snap pulls your finger to that point). You feel the Voronoi boundary where two lattice points compete. You feel that the constraint is *real* — it takes energy to violate.

### Weekend Build Plan

**Saturday:**
1. 3D print cam shafts (2–3 hours). STL generator script takes lattice specification and outputs cam profile.
2. Assemble key mechanisms: cam + follower + spring + slider rail (2 hours).
3. Wire Hall effect sensors to Arduino (1 hour).

**Sunday:**
4. Write Arduino firmware: read sensors, snap to lattice, output MIDI (2 hours).
5. Calibrate and tune spring tension (1 hour).
6. Build enclosure — laser-cut or 3D printed box (1 hour).

**Estimated cost:** $200–400 (Hall effect sensors × $3 each, Arduino Mega $35, springs/hardware $30, 3D printing filament $20, enclosure $30–50).

---

## 2. FUNNEL — "The Gravity Well"

### Concept

A circular surface shaped like a funnel or gravity well. A physical ball (bearing or marble) rolls on the surface. The ball's distance from center maps to pitch deviation from a target note. The shape of the well *is* the funnel function — gravity provides the attraction toward the tonal center.

### Mechanism

A CNC-milled or 3D-printed bowl with a specific radial profile:

- **Linear funnel:** Shallow cone — constant gravitational pull toward center.
- **Exponential funnel:** Steepens near center — weak pull far away, very strong pull near target.
- **Gaussian funnel:** Smooth bell-curve cross-section — moderate pull everywhere, maximum near center.
- **Deadband funnel:** Flat near center (deadband region), then steep walls — notes within tolerance are "free," outside tolerance get pulled hard.

The bowls are interchangeable. Swap the bowl to change the funnel profile.

**Key components:**
- **Aluminum bowl:** CNC-milled for precision. Alternative: 3D printed and sanded smooth. 30cm diameter.
- **Steel ball bearing:** 15mm, rolls smoothly. Weight gives satisfying inertia.
- **IR tracking:** IR LED ring around the rim + camera below, tracking ball position at 60fps.
- **LED ring:** Addressable LEDs around the rim, showing funnel shape and current pitch visually.
- **Microcontroller:** Maps (r, θ) to pitch, applies funnel function digitally for visualization, outputs MIDI.

**The feel:** Place the ball near the edge and release. Watch (and hear) it spiral inward toward the center — the target note — accelerating as the well steepens. The ball's kinetic energy maps to musical ornamentation (vibrato, bends). A ball at rest in the center is the pitch at perfect unison with the target.

### Musical Use

- **Feel gravitational pull toward tonal center.** Place the ball anywhere and hear it converge.
- **Compare funnel profiles.** Swap bowls and feel the difference — linear feels "fair," exponential feels "inevitable," gaussian feels "musical."
- **Ornamentation as physics.** Flick the ball so it orbits the center — the resulting pitch oscillation is a natural vibrato shaped by the funnel.
- **Multi-voice: multiple balls** (different sizes/weights) for polyphonic funnel music.

### How This Teaches Constraint Theory

FUNNEL is the operation of attracting values toward a target with configurable strength. The mathematical funnel function `f(x, t, σ)` maps to a physical bowl shape. The ball's trajectory under gravity *is* the constraint dynamics. You see convergence rates, basin shapes, and the difference between funnel profiles — not as graphs on a screen but as a ball rolling in a bowl. The concept of "attraction strength" becomes gravitational steepness. The concept of "deadband" becomes a flat spot in the center.

### Weekend Build Plan

**Saturday:**
1. Design bowl profiles in CAD (1 hour). Parametric: specify funnel type and parameters → get bowl profile.
2. CNC mill or 3D print 2–3 bowls (3–4 hours for printing, 1–2 hours for CNC).
3. Sand and polish bowl surfaces (1 hour — smoothness matters).

**Sunday:**
4. Build frame and IR tracking system (2 hours).
5. Wire LED ring and microcontroller (1 hour).
6. Write tracking firmware and MIDI output (2 hours).
7. Calibrate position-to-pitch mapping (1 hour).

**Estimated cost:** $500–800 with CNC aluminum bowls. Budget alternative: all 3D printed for $150–250 (PLA bowls + tracking hardware + LEDs + Arduino).

---

## 3. CONSENSUS — "The Agreement Network"

### Concept

A set of physical nodes (sliders) connected by elastic cords. Each slider represents one voice in a multi-agent system. The cords represent consensus constraints between voices. Moving one slider physically pulls the others through cord tension.

### Mechanism

4–8 motorized faders arranged in a circle or line. Elastic cords (or spring-loaded cables) connect pairs of faders. The cord routing is configurable — different topologies create different consensus behaviors:

- **Full mesh:** Every voice connected to every other (strong consensus).
- **Ring:** Each voice connected to neighbors (local consensus, global emergence).
- **Star:** One central voice connected to all others (leader/follower).
- **Custom:**任意 connections via a patch panel.

**Key components:**
- **Motorized faders:** 60mm travel, motorized (Bourns or ALPS). Each can be pushed by hand AND driven by the motor.
- **Tension sensors:** Strain gauges on cord attachment points, measuring how hard each consensus link is pulling.
- **Elastic cords:** Adjustable-length bungee or surgical tubing. Different elasticity = different consensus strength.
- **Microcontroller:** Reads all fader positions, drives motors to simulate consensus dynamics, outputs MIDI for each voice.

**The feel:** Grab one fader and move it. You feel resistance from the cords. The connected faders start moving too, dragged by the tension. Let go and the system settles into consensus — all faders drift toward a shared position. Snap a cord (quick-release clip) and that voice is suddenly free. The physical network *is* the consensus algorithm.

### Musical Use

- **Feel multi-agent agreement physically.** Each hand controls one voice; the cords make your hands cooperate.
- **Breaking consensus.** Release a cord and hear one voice diverge. Reconnect and hear it rejoin.
- **Topology exploration.** Different cord routings create different musical textures — full mesh is homophonic, ring is contrapuntal.
- **Constraint strength as elasticity.** Stiffer cords = stronger consensus (voices agree more). Loose cords = weak consensus (voices drift apart).

### How This Teaches Constraint Theory

CONSENSUS is the operation of making multiple agents agree. Mathematically, it's a constraint satisfaction problem: minimize deviation between connected agents. Physically, it's elastic cords pulling sliders together. The tension in each cord *is* the constraint violation — high tension means that pair disagrees strongly. The settling time *is* the convergence rate. Releasing a cord *is* removing a constraint from the system. You feel the difference between over-constrained (too many cords — system is rigid, can't move) and under-constrained (too few — system is floppy, voices wander).

### Weekend Build Plan

**Saturday:**
1. Build base plate with fader mounts (2 hours). Laser-cut acrylic or 3D printed.
2. Install motorized faders and wire to motor drivers (2 hours).
3. Create cord routing system — eye hooks + quick-release clips (1 hour).

**Sunday:**
4. Wire tension sensors (strain gauges or flex sensors) (1 hour).
5. Write consensus dynamics firmware: read positions, compute forces, drive motors (3 hours).
6. Calibrate elasticity and consensus parameters (1 hour).
7. Test with different topologies (1 hour).

**Estimated cost:** $300–600 (motorized faders × $20–40 each, motor drivers, strain gauges, Arduino Mega, elastic cords, enclosure).

---

## 4. LAMAN — "The Rigidity Board"

### Concept

A pegboard where you connect pegs with rigid bars. When you've placed exactly 2n−3 bars for n joints (Laman's theorem), the structure becomes rigid — it won't flex. Remove one bar and it becomes a mechanism. You *feel* the transition from floppy to rigid.

### Mechanism

A large pegboard (60cm × 60cm) with a grid of holes. Pegs slot into holes. Aluminum bars connect pegs with rotating joints (ball joints or pin joints). Spring clips hold bars to pegs.

**Key components:**
- **Pegboard:** 5mm grid of holes, MDF or acrylic. Pre-drilled.
- **Pegs:** 3D printed, with ball-joint receivers on top.
- **Bars:** Aluminum tubing, various lengths (5cm to 25cm). Ball-joint ends that snap onto pegs.
- **Spring clips:** Quick-release, so bars can be added and removed rapidly.
- **Rotation sensors (optional):** IMU on each bar for digital readout of rigidity (angle change over time).

**The feel:** Start with 3 pegs and 3 bars (a triangle — the minimal rigid structure for Laman's theorem). It's solid. Add a 4th peg and connect it with 2 bars (2×4−3 = 5 bars total). Still rigid. Now remove one bar — suddenly the 4th peg flops around. The structure went from rigid to mechanism with one bar. You *felt* the phase transition.

### Musical Use

- **Understand rigidity through hands.** Build a rigid structure, then break it. The feeling of "locked in" vs. "floppy" maps directly to musical constraint satisfaction.
- **Compose structures.** Each bar is a constraint; each peg is a musical parameter. A rigid structure = all parameters determined. A mechanism = some parameters free.
- **Perform rigidity.** Build the structure live, adding constraints (bars) one at a time. The audience sees (and hears) the moment the system locks into rigidity.

### How This Teaches Constraint Theory

Laman's theorem states that a 2D structure with n joints is minimally rigid iff it has exactly 2n−3 bars AND every subset of k joints spans at most 2k−3 bars. The Rigidity Board makes this theorem tangible. You *feel* the exact threshold: 2n−3 bars and it's locked. 2n−4 and it's a mechanism. The theorem isn't abstract — it's the difference between a solid shape and a wobbly one in your hands. The "every subset" condition is also testable: build a structure that satisfies 2n−3 globally but has a flexible sub-part (a subset violating the condition). You'll feel that sub-part flop even though the total bar count is correct.

### Weekend Build Plan

**Saturday:**
1. Cut and drill pegboard (1 hour).
2. 3D print 20–30 pegs with ball-joint receivers (3 hours, or batch print overnight).
3. Cut aluminum bars to various lengths and attach ball-joint ends (2 hours).

**Sunday:**
4. Create spring clips (1 hour — bend spring steel or repurpose binder clips).
5. Optional: attach IMU sensors to bars for digital rigidity detection (2 hours).
6. Build tutorial cards: "Build this structure — is it rigid?" challenges (1 hour).

**Estimated cost:** $50–150 (pegboard material $10, aluminum tubing $20, 3D printing filament $10, spring clips $10, optional IMU sensors $5 each).

---

## 5. TEMPO — "The Metronome Funnel"

### Concept

A physical metronome that visualizes temporal constraint as a funnel shape. Near the beat, the funnel is narrow — timing must be precise. Between beats, the funnel is wide — notes can be placed freely. An LED strip shows the funnel shape in real time, and the player's timing is visually mapped onto it.

### Mechanism

A pendulum metronome (or electronic simulation) drives a timing reference. An LED strip (1 meter, addressable) displays the funnel shape:

- **Center of the strip** = the beat (t = 0).
- **Distance from center** = time offset from beat.
- **LED brightness/color** = funnel value at that offset: bright/green at center (narrow, constrained), dimming to red at edges (wide, free).
- **Player input:** A drum pad or MIDI keyboard. When the player hits a note, an LED lights up at the corresponding temporal position on the strip.

The funnel shape updates in real time. Different funnel profiles:
- **Narrow gaussian:** Jazz timing — notes must be near the beat.
- **Wide gaussian:** Rubato-friendly — notes can be far from the beat.
- **Asymmetric:** Swing — the funnel is shifted, encouraging late hits.

**Key components:**
- **Metronome:** Mechanical pendulum (Wittner-style) or electronic (Arduino timer).
- **Hall effect sensor on pendulum:** Detects beat crossing for timing reference.
- **LED strip:** WS2812B, 60 LEDs/meter, mounted in a clear tube or behind frosted acrylic.
- **Drum pad:** Piezo sensor or commercial pad for player input.
- **Microcontroller:** Tracks timing, drives LED animation, reads hits, outputs visualization.

**The feel:** Watch the LED strip pulse — a bright green spot sweeps along it at the tempo. That's the beat. Hit the drum pad and a white dot appears on the strip at your timing position. Inside the green zone? You're in the funnel — constrained timing. Outside? You're free, but maybe too free. The visual makes temporal constraint *spatial*.

### Musical Use

- **See temporal constraint.** The funnel shape on the LED strip shows exactly how much timing freedom you have at each moment.
- **Practice groove.** The visual feedback trains tight timing — try to keep your white dots inside the green zone.
- **Explore swing and rubato.** Change the funnel profile and see how the constraint shape shifts.
- **Ensemble play.** Multiple players each get a drum pad; their hits appear as different colored dots. See the ensemble's consensus in real time.

### How This Teaches Constraint Theory

TEMPO is the temporal version of the funnel constraint. Instead of attracting a pitch toward a target, it constrains timing toward a beat. The funnel function `f(t, t₀, σ)` where t₀ is the beat time and σ is the width parameter maps directly to the LED strip visualization. Narrow σ = tight groove. Wide σ = free rhythm. The key insight: constraint isn't just about pitch — it applies to time too. And the *shape* of the temporal constraint (gaussian? linear? deadband?) determines the musical feel. Jazz has a narrow temporal funnel. Free jazz has almost none. The instrument makes this audible *and* visible.

### Weekend Build Plan

**Saturday:**
1. Build metronome or set up electronic timing (1 hour).
2. Mount Hall effect sensor on pendulum (if mechanical) or wire timing circuit (1 hour).
3. Build LED strip display — mount in acrylic housing (2 hours).

**Sunday:**
4. Wire drum pad and microcontroller (1 hour).
5. Write firmware: timing, LED animation, hit detection, funnel visualization (3 hours).
6. Implement multiple funnel profiles and switching mechanism (1 hour).
7. Playtest and tune visual parameters (1 hour).

**Estimated cost:** $100–200 (LED strip $15, Arduino $10–25, drum pad or piezo $10–20, pendulum or timing hardware $20–30, acrylic housing $15, misc hardware $10).

---

## Bill of Materials Summary

| Instrument | Key Components | Estimated Cost | Build Time |
|---|---|---|---|
| Lattice Piano (SNAP) | Cams, springs, Hall sensors, Arduino | $200–400 | 1 weekend |
| Gravity Well (FUNNEL) | CNC bowls, ball bearing, IR tracking, LEDs | $150–800 | 1 weekend |
| Agreement Network (CONSENSUS) | Motorized faders, elastic cords, strain gauges | $300–600 | 1 weekend |
| Rigidity Board (LAMAN) | Pegboard, aluminum bars, 3D printed joints | $50–150 | 1 weekend |
| Metronome Funnel (TEMPO) | Pendulum, LED strip, drum pad, Arduino | $100–200 | 1 weekend |

---

## Pedagogical Notes

These instruments are designed for a specific learning sequence:

1. **Start with LAMAN** (Rigidity Board). It's the cheapest, simplest, and teaches the foundational concept: constraints create structure. Rigidity is the most visceral constraint — you can literally grab it and shake it.

2. **Then SNAP** (Lattice Piano). Quantization is the next conceptual step — continuous to discrete. The detent mechanism is a mechanical version of the Laman rigidity: the lattice point "holds" your finger.

3. **Then FUNNEL** (Gravity Well). Attraction toward a target. This softens the hard snap into a graded pull. The ball's trajectory teaches convergence.

4. **Then TEMPO** (Metronome Funnel). Same concept as funnel, but in time instead of pitch. This generalization is crucial — constraints aren't just about notes, they're about *events*.

5. **End with CONSENSUS** (Agreement Network). Multiple agents, multiple constraints, emergent agreement. This is where it all comes together — the most complex instrument, but by now the player understands every component.

---

## Open Questions

- **Can these be combined?** A Lattice Piano + Gravity Well hybrid where the well's center snaps to lattice positions. A Consensus Network where the agreement target is a funnel.
- **Digital twins?** Each instrument should have a software simulation for people who can't build the physical version. The sim is less visceral but still educational.
- **Performance repertoire?** These are teaching tools, but could they be concert instruments? What does a piece written for Rigidity Board sound like?
- **Scale?** The Consensus Network naturally extends to 10+ voices. The Gravity Well could be a room-sized installation. How far can these scale?

---

*"The hand is the cutting edge of the mind." — Jacob Bronowski*
