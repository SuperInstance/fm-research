# BETA TEST — Round 5: The Accessibility Advocate

**Tester:** Accessibility Research Division  
**Perspective:** Researcher working with disabled musicians; daily use of single-switch devices, eye-gaze tracking, and breath controllers  
**Date:** May 23, 2026  
**Repositories Evaluated:** fm-research, flux-tensor-midi, constraint-theory-web

---

## Executive Summary

This project makes a bold claim: **"the constraint IS the accessibility feature."** After reading every relevant document — the Accessibility Calibration paper, the Physical Instruments paper, the constraint web tools, and the flux-tensor-midi engine — I believe this claim holds water, with caveats. The theoretical framework is genuinely innovative and maps well to how disabled musicians actually think about making music. But the current implementation is almost entirely theoretical and visual, with significant gaps in WCAG compliance, keyboard navigation, screen reader support, and practical input modality integration. The ideas are strong enough to build on; the software is not yet usable by the people it claims to serve.

**Verdict: Promising research program, currently inaccessible software. Fix the web tools first — disabled musicians can't use them today.**

---

## 1. Accessibility Calibration Paper — Is the Ladder Realistic?

### Overview

The paper proposes five levels: One-Hand Drum → Breath Sync → Tongue Switch → Eye-Gaze → Surface EMG. Each maps to constraint primitives (snap, funnel, consensus, laman, tempo).

### Strengths

1. **The ladder is NOT hierarchical.** The paper explicitly states this isn't "better" or "worse" — it's a menu. This is correct and respectful. In my work, the most damaging assumption people make is that quadriplegic musicians need "simpler" instruments. They don't. They need different interfaces to the same musical complexity.

2. **Personas are well-chosen.** Maria (hemiplegic, one hand), James (C5 quadriplegic, breath only), Aisha (ALS, tongue only), Robert (Parkinson's, tremor), Chen Wei (C3 injury, shoulder shrug). These represent real populations I work with. The Aisha/ALS persona is particularly important — ALS progression means input modalities must be *interchangeable*, not just available.

3. **Hardware costs are realistic.** The paper estimates $15–40 for Level 1 (drum pads), $10–800 for Level 2 (breath), $100–200 for Level 3 (tongue switch). These are within reach for individual musicians and definitely within reach for music therapy programs. The DIY emphasis matters — most commercial ADMIs are prohibitively expensive.

4. **The snap deadband concept is well-understood.** For musicians with tremors (Parkinson's, essential tremor, cerebral palsy), a configurable deadband is not optional — it's essential. The paper correctly identifies this as a per-user calibration problem.

5. **Composability of modalities is correctly identified.** Breath + tongue switch, eye-gaze + EMG — these combinations match real-world needs. Many disabled musicians I work with use two or more alternative input methods simultaneously.

### Weaknesses

1. **No empirical validation.** This is a position paper, which is fine as far as it goes. But the personas are hypothetical. Maria hasn't tested the drum pad. James hasn't tried the breath controller with this specific constraint engine. Until disabled musicians actually use the system, the ladder remains speculative.

2. **Level 5 (EMG) is aspirational.** Surface EMG is notoriously unreliable for real-time control. The paper acknowledges signal-to-noise and fatigue issues but doesn't offer solutions beyond "advanced signal processing." In practice, EMG-based music control has been attempted many times (the Tanaka & Knapp reference is good) and the results are consistently disappointing for live performance. For recording/composing at one's own pace, it could work. For live performance, I'm skeptical.

3. **Missing input modalities.** The ladder omits several modalities that my community uses daily:
   - **Sip-and-puff controllers** (binary/ternary pneumatic switches — incredibly common, cheap, reliable)
   - **Head pointers and head mice** (used by many quadriplegic musicians)
   - **Brain-computer interfaces (BCI)** — still emerging but relevant for locked-in syndrome
   - **Voice/speech recognition** — not for singing, but for commanding the system
   - **Switch scanning** (single or dual switch with automated sequential scanning through options)

4. **The "ladder" metaphor risks implying hierarchy.** Despite the disclaimer, calling it a "ladder" with "levels" 1–5 creates an unconscious implication of progression. I'd rename it to something like "Input Modality Atlas" or "Constraint Interface Catalog."

5. **Calibration is hand-waved.** "Automated calibration routines that adapt the constraint mapping to individual needs — possibly using machine learning — are an open research area." Yes. And this is the hardest part. Every disabled musician is different. Two people with the same C5 spinal cord injury will have different functional abilities. Calibration isn't an afterthought — it's 80% of the work.

### WCAG Compliance of the Paper Itself

N/A — it's a Markdown document. Reasonably well-structured with headers. Could use alt-text descriptions for any future diagrams. The mathematical notation is accessible in text form.

---

## 2. Web Tools — Screen Reader and Keyboard Evaluation

### What I Tested

- `constraint-playground.html` — The main interactive playground with 5 stations (Snap, Funnel, Consensus, Rigidity, Tempo)
- `constraint-tarot.html` — The card-drawing metaphor interface
- Multiple experiment pages under `experiments/`

### Screen Reader Compatibility: FAILING

**Current state:** The web tools are **entirely canvas-based** with zero ARIA markup, zero semantic structure within interactive areas, and zero screen reader announcements.

Specific findings:

- **Zero `aria-*` attributes** anywhere in constraint-playground.html or constraint-tarot.html
- **Zero `role` attributes** on interactive elements
- **Zero `tabindex` attributes** — nothing in the interactive areas is keyboard-focusable
- **No `alt` text** — canvas elements have no fallback content
- **No skip-navigation links** — users must tab through the entire header to reach content
- **No live regions** (`aria-live`) — state changes (note placed, constraint applied) are visually-only

**Impact:** A screen reader user arriving at constraint-playground.html would hear the page title, the hero text, and the navigation links. The 5 interactive stations — the entire point of the page — would be invisible. The canvas elements render as unlabeled graphics with no interactive content announced.

**Severity: CRITICAL.** This is not a minor accessibility gap — it's a complete absence of accessibility for blind and low-vision users.

### Keyboard Navigation: FAILING

**Current state:** All interaction is mouse/touch-only via canvas click events.

Specific findings:

- The playground uses `canvas.addEventListener('click', ...)` and `canvas.addEventListener('mousemove', ...)` exclusively
- No `keydown` / `keyup` handlers for the interactive areas
- The BPM slider and key selector in the global controls ARE keyboard-accessible (they're native HTML form elements)
- The station-level buttons (Clear, Play) are native `<button>` elements and ARE keyboard-accessible
- But the actual interactive canvases — where you place notes, drop balls, drag sliders — are mouse-only

**Impact:** A musician who uses keyboard-only navigation (common for motor impairments, also the primary alternative to mouse for screen reader users) can reach the page, adjust BPM and key, and press "Play" — but cannot actually interact with any of the constraint stations.

### Color and Contrast: MOSTLY PASSING

- The dark theme uses high-contrast text (#e8e8f0 on #0a0a0f) — contrast ratio approximately 16.5:1, well above WCAG AA (4.5:1)
- The muted text (#6b6b80 on #0a0a0f) — approximately 4.0:1 — FAILS WCAG AA for normal text (requires 4.5:1) but PASSES for large text (3:1)
- The colored station headings use saturated colors that have reasonable contrast against the dark background
- **No information is conveyed by color alone** — each station also uses text labels, symbols (◆), and spatial position

### Responsive Design: PASSING

- The CSS includes `@media(max-width:700px)` breakpoints
- Uses `clamp()` for responsive typography
- Flexbox layouts with `flex-wrap` handle narrow viewports
- Touch targets on buttons appear adequate (padding provided)

### Practical Barrier Summary

| Barrier | Severity | Effort to Fix |
|---|---|---|
| Canvas-only interaction (no keyboard) | CRITICAL | High — requires complete interaction redesign |
| Zero ARIA markup | CRITICAL | Medium — add labels, roles, live regions |
| No screen reader fallbacks | CRITICAL | High — canvas needs text alternatives |
| Muted text contrast (4.0:1) | MINOR | Trivial — lighten #6b6b80 to ~#7878a0 |
| No skip-nav link | MODERATE | Trivial — add hidden skip link |
| No focus indicators (custom) | MODERATE | Low — CSS focus-visible styles |
| No reduced-motion support | MODERATE | Low — `prefers-reduced-motion` media query |

---

## 3. Can the Constraint System Work with Single-Switch Input?

### Assessment: Yes, In Theory — With the Right Mapping

A single-switch device produces one binary signal: activated or not activated. The musician controls *timing* and *duration* (hold vs. tap). This is the lowest-bandwidth input modality commonly used.

The constraint framework CAN work with single-switch input if:

1. **Switch scanning is implemented.** The system automatically cycles through constraint options (harmonic regions, rhythmic patterns, timbral choices). The musician activates the switch to select. This is standard practice in augmentative and alternative communication (AAC) and switch-accessible software. The constraint system is well-suited to this because each "choice" presented to the user is already a high-level musical decision, not a low-level parameter.

2. **Temporal patterns encode intent.** Tap patterns (morse-code-like) can encode more than binary:
   - Single tap = advance to next option
   - Double tap = select current option
   - Hold = "perform now" or "commit current constraints"
   - Hold-release timing = energy/urgency level (maps to funnel convergence rate)

3. **The snap deadband prevents accidental double-activations.** Many switch users have difficulty with precise timing. The snap mechanism's configurable deadband is directly applicable here.

4. **Consensus provides the "undo."** If a switch selection produces undesirable musical results, the consensus mechanism should gracefully absorb the error without requiring an explicit undo (which would need another switch action).

### What's Missing

- **No switch-scanning implementation exists** in the current codebase
- **No dwell-time selection** (where holding the switch for a configured duration selects)
- **No configurable scan rate** (some users need 0.5s per option; others can handle 0.1s)
- **No auditory scanning feedback** (critical — the musician needs to HEAR what they're about to select)

### Recommendation

Implement a "scan mode" that works with any binary input:
1. Audio announces each constraint option in sequence
2. Musician activates switch to select
3. System applies selected constraint and advances to next parameter
4. After all parameters are set, "perform" mode renders the constrained music

This is achievable with current web APIs (Web Audio for speech, gamepad API for switch input) and would make the system genuinely usable by single-switch musicians.

---

## 4. Physical Instruments Paper — Buildable?

### Overall Assessment: Yes, With Caveats

The Physical Instruments paper describes five buildable devices. I evaluated each for:

1. **Can a maker actually build this in a weekend?**
2. **Can it be adapted for disabled musicians?**
3. **Is it safe?**

### Per-Instrument Evaluation

**The Lattice Piano (SNAP) — BUILDABLE, GOOD FOR ACCESSIBILITY**

- Cam + follower mechanism is a well-understood mechanical design
- 3D printing the cam shafts is straightforward; the parametric OpenSCAD approach is smart
- **Accessibility angle:** The adjustable spring tension is key — disabled musicians with reduced force can use lighter springs. The snap provides tactile feedback even without visual confirmation.
- **Concern:** The Hall effect sensors require precise positioning. A musician with one functional hand might struggle with assembly but could certainly play it.
- **Missing:** No CAD files yet in PHYSICAL-INSTRUMENTS-CAD/ — just the directory structure.

**The Gravity Well (FUNNEL) — BUILDABLE, EXCELLENT FOR ACCESSIBILITY**

- This is the most immediately accessible instrument. A ball rolling in a bowl requires almost no physical force and provides rich visual, auditory, and tactile feedback.
- **Accessibility angle:** This could work with head-pointer interaction (pushing the ball), breath (blowing the ball), or even chin control. The low force requirement makes it ideal.
- **Concern:** CNC aluminum bowls at $500–800 are expensive. The $150–250 3D printed alternative is more realistic for most disabled musicians, but printed surfaces have higher friction, changing the funnel dynamics.
- **Safety:** A 15mm steel ball bearing is a choking hazard and could cause injury if the device tips. Recommend a clear acrylic cover with ventilation holes.

**The Agreement Network (CONSENSUS) — BUILDABLE, MODERATE ACCESSIBILITY**

- Motorized faders are well-documented. The elastic cord mechanism is clever and intuitive.
- **Accessibility angle:** The motorized faders can be driven BY the system — a musician doesn't need to move them manually. The system could move the faders in scan mode, and a single-switch activation "grabs" the currently-moving fader.
- **Concern:** $300–600 is expensive. Motorized faders are the cost driver.
- **Safety:** Elastic cords under tension can snap. Eye protection recommended during use.

**The Rigidity Board (LAMAN) — BUILDABLE, GOOD FOR TEACHING**

- Simplest build. Pegboard + bars + joints. $50–150.
- **Accessibility angle:** Primarily a teaching tool, not a performance instrument. Good for music therapy contexts where the therapist and musician build structures together.
- **Concern:** Small parts (spring clips, ball joints) are fine-motor tasks. Assembly assistance may be needed.

**The Metronome Funnel (TEMPO) — BUILDABLE, EXCELLENT FOR ACCESSIBILITY**

- The visual LED strip is a strong accessibility feature — it makes time VISIBLE.
- **Accessibility angle:** Deaf and hard-of-hearing musicians could use this as a visual rhythm reference. The LED strip could also use haptic feedback (vibration motors) for dual-sensory temporal cueing.
- **Concern:** The mechanical pendulum approach has latency and reliability issues. An electronic timing reference would be more consistent and accessible.

### Missing Safety Considerations

The paper doesn't discuss safety at all. For any instrument intended for use by disabled musicians:

- **Seizure triggers:** Flashing LEDs (especially the Tempo station) must respect photosensitive epilepsy guidelines (no flashes >3Hz)
- **Strangulation hazards:** Elastic cords (Consensus instrument) must have quick-release mechanisms
- **Choking hazards:** Small parts (ball bearings, pegs, spring clips) must be secured or enlarged
- **Electrical safety:** Any Arduino/USB-powered device must be properly insulated, especially for musicians who may have limited sensation and cannot feel overheating or shock

---

## 5. Does "Constraint IS the Accessibility Feature" Hold Up?

### The Argument

The core claim: By reducing the space of valid musical outputs, constraint systems guarantee that imprecise, low-bandwidth inputs produce coherent results. The musician provides *direction*; the constraint system provides *precision*.

### Verdict: YES, With Important Nuances

**Where it works brilliantly:**

1. **Reduced input precision requirement.** This is real and important. A traditional piano requires hitting a specific key at a specific velocity at a specific time. A constraint system requires "somewhere in this harmonic region, at roughly this energy level, at approximately this time." The constraint engine handles the rest. This is genuinely liberating for musicians with motor impairments.

2. **The mathematical foundation is sound.** The Laman rigidity condition (2n−3 edges for n vertices) provides a formal guarantee that the constraint network is "determined enough" without being "over-determined." This isn't hand-waving — it's graph theory. The system can prove it's in a valid state.

3. **The shift from "specify everything" to "guide the trajectory" matches how composition actually works.** Most composers — disabled or not — think in terms of "more tension here" and "resolve this" rather than "MIDI note 60, velocity 96, tick 480." The constraint system operationalizes this higher-level thinking.

**Where it needs more work:**

1. **Constraints can also be prisons.** If the constraint system is too rigid, the musician has no room for expression. If it's too loose, it provides no value. The "goldilocks zone" of constraint strictness is individual and contextual. The paper acknowledges this (via the funnel width parameter) but underestimates how much tuning this requires.

2. **"Coherent" ≠ "Expressive."** A constraint system can guarantee that the output is musically valid without guaranteeing that it's musically *interesting* or *personal*. The musician's personality must still come through. The paper doesn't address how to measure whether a musician feels ownership of the output.

3. **The accessibility benefit is bidirectional.** Just as constraints help disabled musicians by reducing precision requirements, they also risk constraining disabled musicians *more* than able-bodied ones. An able-bodied musician can always override a constraint by playing "raw" notes. A disabled musician using a single-switch input is *entirely dependent* on the constraint system. If the constraints are wrong, the disabled musician has no escape hatch. This power asymmetry must be acknowledged.

4. **"Constraint as accessibility feature" risks condescension.** The framing must be careful not to imply that disabled musicians NEED constraints because they can't handle freedom. Constraints are a creative tool, not a crutch. The paper mostly gets this right but occasionally tips into "the system handles precision" language that could be read as patronizing.

**Bottom line:** The claim holds. Constraint-based systems are uniquely well-suited to accessible music-making. But the implementation must empower, not restrict. The disabled musician must remain the artist, not become a passenger in the constraint system.

---

## 6. Ideation Session

### Input Modalities That Are Missing

The Accessibility Ladder covers five modalities but omits several that are critical in real-world accessible music technology:

**Sip-and-Puff Controllers** — These are the workhorses of switch access. A tube connected to a pressure sensor; the musician sips (inhale) or puffs (exhale) to produce two distinct binary signals. They cost $20–100, are incredibly reliable, require minimal physical capability (mouth control only), and are already integrated into most AAC devices. The constraint system should absolutely support sip-and-puff as a first-class input. Mapping: sip = advance through constraint options (scan mode), puff = select current option. Sustained puff = "perform now."

**Switch Scanning with Auditory Feedback** — This isn't an input device per se, but a *mode of interaction* that works with any binary switch (including sip-and-puff, tongue switch, or EMG threshold). The system automatically cycles through options and announces each one audibly. The musician activates their switch to select. This is the single most important accessibility pattern for any system that offers multiple choices. The constraint system, with its discrete constraint options (harmonic regions, rhythmic patterns, etc.), is a natural fit. Each constraint option becomes a scan item. The musician hears "tonic" → "dominant" → "subdominant" → *click* → "subdominant selected."

**Head Tracking / Head Mouse** — Many quadriplegic musicians use head-mounted reflectors tracked by a camera (e.g., TrackerPro, SmartNav) or built-in head tracking (Windows Eye Control, macOS Head Pointer). This provides a 2D cursor controlled by head movement. The constraint system's visual interface could be directly controlled by head tracking — look at a constraint region and dwell to select. The snap mechanism's deadband is perfect for absorbing the imprecision of head movement.

**Voice Control for Commands (Not Performance)** — The paper doesn't mention voice/speech at all. While voice is an obvious input for singing, it's also powerful as a *command interface* for the constraint system. "More tension" → increase harmonic constraint intensity. "Resolve" → shift to tonic neighborhood. "Add drums" → activate rhythmic constraint layer. This is particularly valuable for musicians who have speech but limited physical control. Web Speech API makes this implementable in the browser today.

**Brain-Computer Interfaces (BCI)** — Still emerging, but relevant. Non-invasive EEG headbands (OpenBCI, Emotiv) can detect motor imagery (imagining hand movement), steady-state visually evoked potentials (SSVEP — looking at flashing targets), and P300 signals (recognizing a rare stimulus). For locked-in musicians who have no motor output whatsoever, BCI is the last resort. The constraint system's low-bandwidth requirement (the musician only needs to indicate "this one" among a small set of options) is well-matched to BCI's limited throughput. A P300 speller-style interface could present constraint options as a grid of flashing items; the system detects which one the musician's brain responds to.

**Breath Velocity as Continuous Control** — The paper's Level 2 (Breath Sync) treats breath as a relatively simple pressure signal. But breath control is far more nuanced. Professional wind players (including those using breath controllers for accessibility) can produce:
- Continuous pressure (0 to max)
- Rapid pressure changes (articulation)
- Vibrato (periodic pressure oscillation)
- Double/triple tonguing (rapid on/off)
- Circular breathing (continuous sustained tone)

The constraint system should exploit all of these. Breath vibrato could modulate the funnel convergence rate. Breath articulation could trigger snap events. Sustained breath could "hold" a constraint active.

**Body-Worn Inertial Sensors (IMU)** — Accelerometers and gyroscopes worn on any movable body part (wrist, ankle, head, torso) provide 6-axis motion data. For musicians with limited but present movement in any body part, IMU data maps naturally to constraint parameters: tilt selects a constraint region, shake triggers an event, rotation modulates a parameter.

### Can Constraints Help Disabled Musicians Make BETTER Music?

This is the provocative question, and I believe the answer is yes — not in spite of the constraints, but because of them.

**Constraints as Creative Catalysts.** The history of music is a history of constraints. The 12-tone equal temperament system is a constraint. Sonata form is a constraint. A 4/4 time signature is a constraint. Jazz musicians impose constraints on themselves (chord changes, modes, time feels) and then create within those boundaries. Hip-hop producers constrain themselves to sampled breaks and limited hardware. The constraint IS the art.

For disabled musicians, the constraint system externalizes what all musicians do internally: define a creative space and then explore it. The difference is that able-bodied musicians can fall back on technical facility when their creative constraints fail — they can "play their way out" of a dead end. Disabled musicians working with the constraint system need the system to provide that fallback. When the creative direction leads to a dead end, the constraint engine should offer alternatives, not dead ends.

**The Reduction-to-Essence Argument.** When you remove the ability to "play everything," you're forced to make every choice count. I've seen disabled musicians produce work that is more focused, more intentional, and more emotionally direct than their able-bodied peers — precisely because they can't hide behind technique. The constraint system amplifies this effect. If you can only make 5 musical decisions per minute (single-switch scanning rate), those 5 decisions carry enormous weight. The constraint system should honor that weight by making every option musically meaningful.

**Collaborative Constraint.** The consensus mechanism is the most exciting accessibility feature in this entire project. It enables a form of music-making that doesn't exist in the traditional instrument paradigm: the musician and the system collaborate as equals. The musician proposes constraints (through whatever input modality they use); the system proposes complementary constraints (based on musical logic); the consensus mechanism resolves them into a unified musical state. This is not a musician playing an instrument. This is a musician having a conversation with an intelligent musical collaborator. For disabled musicians who have been excluded from ensemble playing (because traditional instruments don't accommodate them), this collaborative model could be transformative.

**Constraint as Identity.** Over time, a disabled musician's preferred constraint configurations become their musical signature — their "sound." Just as a guitarist's tone is shaped by their instrument's physical constraints (string tension, body resonance, pickup position), a constraint-system musician's tone is shaped by their constraint profile. This profile encodes their musical taste, their physical capabilities, and their creative instincts into a reproducible, shareable, evolving musical identity. Two musicians using the same constraint system with different constraint profiles will sound completely different — even if they're both using single-switch input.

### Dream: A Concert Where Disabled Musicians Perform Using Constraints

*The venue is a converted warehouse — concrete floors, exposed beams, excellent acoustics. The stage has no traditional instruments. Instead, each performer has a personalized station.*

**First act: Maria and the Lattice Piano.** Maria, hemiplegic since her stroke at 32, sits at a modified Lattice Piano with enlarged pads and reduced spring tension. She plays with her left hand, tapping constraint regions. But she's not alone — the constraint engine fills in a full orchestral arrangement around her harmonic choices. The audience hears a symphony; Maria controls its harmonic trajectory with one hand. The constraint system handles voice leading, orchestration, dynamics, and timing. Maria's contribution — her harmonic choices, her rhythmic feel, her energy — is unmistakably present in every measure.

**Second act: James and the Breath Ensemble.** James, C5 quadriplegic, sits in his wheelchair with a breath controller mounted on a headset. He breathes. The room fills with sound — not a solo performance, but an ensemble. The constraint engine generates multiple voices, each constrained by James's breath signal. When he inhales, the music breathes too. When he increases pressure, the texture thickens. When he releases, it opens. The consensus mechanism resolves his breath energy into a balanced ensemble texture. He is the conductor and the section leader and the soloist, all through a tube in his mouth.

**Third act: The Constraint Quartet.** Four disabled musicians, four different input modalities, one constraint system. Aisha uses her tongue switch for harmonic constraints. Robert uses eye-gaze for melodic contour. Chen Wei uses EMG for rhythmic density. Maria uses her one hand for timbral energy. The consensus mechanism resolves all four inputs into a coherent musical output in real time. The audience watches four musicians who have never been able to play in an ensemble before — and hears a quartet. Not a curiosity. Not a demonstration of "assistive technology." A performance. Music that moves people.

The quartet navigates through a pre-composed constraint landscape — a piece written for this specific ensemble that maps each musician's input to a distinct musical role. But within that landscape, they have freedom. Aisha can choose more or less harmonic determination. Robert can shape the melody with his gaze. Chen Wei can drive the rhythm harder or softer. Maria can warm or cool the timbre. Their choices interact through the consensus mechanism, creating emergent musical structures that no single musician (and no AI) could have predicted.

**Fourth act: The Improvised Constraint Conversation.** The audience is invited to participate. A row of simple constraint controllers — just buttons, anyone can use them — runs along the front of the stage. Each audience member can propose a constraint: "more tense," "resolve," "add percussion," "slower." These constraints join the consensus alongside the disabled musicians' inputs. The musicians have veto power (their constraint votes carry higher weight), but the audience shapes the performance. The boundary between performer and audience dissolves. Everyone is making music. Some with their hands, some with their breath, some with their eyes, some with a button.

**Encore: Aisha Alone.** Aisha, who has ALS and can only move her tongue, performs a solo piece. Four tongue positions, center hold, and timing. That's all she has. The constraint system turns those five signals into a 12-minute piece that moves the audience to tears. Not because it's impressive that she can do it despite her disability. Because the music is genuinely beautiful — spare, deliberate, full of intent. Every note matters because every note was chosen. The constraint system didn't make it easy. It made it possible. And Aisha made it art.

*This concert doesn't exist yet. But the constraint theory framework described in these repositories makes it technically feasible. What's needed now is not more theory — it's implementation, testing with real disabled musicians, and the political will to center disabled voices in the design process.*

### What Would Make This Real

1. **Hire disabled consultants.** Not as beta testers — as co-designers. Pay them. The personas in the paper are well-intentioned but they're inventions. Real disabled musicians should shape this system from the beginning.

2. **Partner with music therapy programs.** University music therapy departments, rehabilitation hospitals, and organizations like Drake Music, Abilities in Harmony, and the Christopher and Dana Reeve Foundation.

3. **Build the web tools to WCAG 2.1 AA first.** The constraint playground should be the most accessible music tool on the internet. Not because it's a nice thing to do, but because accessibility IS the product's core value proposition. If the web tool isn't accessible, the entire research program is undermined.

4. **Open-source everything.** Disabled musicians are expert tinkerers out of necessity. They'll modify, hack, and improve the system in ways you never imagined. Open hardware, open software, open documentation.

5. **Start with the Rigidity Board.** It's the cheapest, simplest physical instrument, and it teaches the foundational concept. Get it into the hands of music therapists and disabled musicians immediately. Iterate based on their feedback, not theoretical analysis.

---

## Summary Scorecard

| Criterion | Rating | Notes |
|---|---|---|
| Accessibility Calibration ladder realism | ★★★★☆ | Well-designed, missing key modalities |
| Screen reader compatibility (web) | ★☆☆☆☆ | Zero ARIA, zero keyboard nav for interactive content |
| Keyboard navigation (web) | ★★☆☆☆ | Form elements work; canvases are mouse-only |
| Single-switch compatibility (conceptual) | ★★★★☆ | The framework supports it; no implementation exists |
| Single-switch compatibility (implemented) | ★☆☆☆☆ | Not implemented |
| Physical instruments buildability | ★★★★☆ | Well-documented; CAD files not yet provided |
| Physical instruments safety | ★★☆☆☆ | No safety discussion at all |
| "Constraint IS accessibility" thesis | ★★★★★ | Compelling and well-argued |
| Empirical validation | ☆☆☆☆☆ | Position paper only; no user studies |
| Inclusivity of design process | ★★☆☆☆ | Personas are hypothetical; no disabled co-designers credited |

---

*"We don't need simpler instruments. We need instruments that meet us where we are."*  
*— Every disabled musician, everywhere*

---

*Filed by the Accessibility Research Division, SuperInstance Beta Test Program.*  
*Push to fm-research.*
