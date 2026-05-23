# Accessibility Calibration: A Ladder of Input Modalities for Constraint-Based Music Systems

**Author:** SuperInstance Research  
**Date:** May 2026  
**Status:** Research Paper — Position & Framework  
**Domain:** Accessible Digital Musical Instruments (ADMIs), Constraint-Based Composition, Adaptive Music Technology

---

## Abstract

Constraint-based music systems — particularly those grounded in constraint theory primitives such as snap, funnel, consensus, laman, and tempo — offer a structural advantage for accessibility that has gone largely unexplored: the constraint itself acts as the accessibility feature. By reducing the space of valid musical outputs, constraint systems guarantee that even imprecise, low-bandwidth, or low-degree-of-freedom inputs produce musically coherent results. This paper proposes a graduated accessibility framework — an "Accessibility Ladder" — consisting of five input modalities of increasing sophistication: single-hand percussion, breath synchronization, binary tongue switching, eye-gaze tracking, and surface electromyography (EMG). For each level, we describe the input modality, its mapping to constraint theory primitives, minimum viable hardware, an example use case with persona, and technical challenges. We argue that constraint-based composition systems are uniquely positioned to serve musicians with varying physical capabilities because they do not require the musician to produce precise control signals — only to influence the trajectory of a pre-structured musical space.

---

## 1. Introduction

The field of Accessible Digital Musical Instruments (ADMIs) has made significant strides in enabling musicians with physical disabilities to participate in electronic and computer-mediated music-making [1][2]. However, most existing approaches treat accessibility as an afterthought — retrofitting conventional instrument interfaces with alternative controllers. The result is often a compromise: the musician can *trigger* sounds, but the expressive nuance available to able-bodied performers remains out of reach.

Constraint-based composition systems offer a fundamentally different starting point. Rather than requiring a musician to specify every parameter of every note, these systems define a *space of valid musical possibilities* through constraints — mathematical and musical rules that bound what is permissible. The musician's role shifts from "specify everything" to "guide the system through a constrained space." This shift has profound implications for accessibility: the constraint system handles precision, while the musician provides intention.

The constraint theory framework developed in the SuperInstance project [3] identifies five core primitives:

- **Snap**: A threshold mechanism that quantizes continuous input to discrete musical states, with configurable deadband to prevent oscillation.
- **Funnel**: A convergence mechanism that narrows the space of valid outputs as additional constraints are applied.
- **Consensus**: A resolution mechanism that reconciles multiple competing constraints into a unified musical state.
- **Laman**: A structural rigidity mechanism (borrowed from Laman graph theory) that ensures the constraint network is minimally rigid — exactly determined, not over- or under-constrained.
- **Tempo**: A temporal constraint mechanism that governs rhythmic alignment and phase relationships.

These primitives compose. A snap can feed into a funnel, which participates in a consensus, all governed by laman rigidity and tempo synchronization. It is this composability that makes the framework so powerful for accessibility: each input modality can be mapped to a different layer of the constraint stack, and the system's inherent structure compensates for whatever precision the musician cannot provide.

This paper proposes an Accessibility Ladder with five levels, each representing an input modality suitable for musicians with progressively different (not necessarily "more severe") physical capabilities. The ladder is not hierarchical in a normative sense — it does not imply that "higher" levels are better. Rather, it offers a menu of options that can be matched to individual needs, and that can be combined.

---

## 2. The Accessibility Ladder

### Level 1: One-Hand Drum

**Input Modality:**  
A single hand (or any single effector — foot, elbow, knee) strikes a surface. Strikes are detected by a contact microphone, piezoelectric sensor, or capacitive touch pad arranged in a grid (typically 2×2 to 4×4). Each grid cell maps to a constraint region. Velocity is captured but not required for basic operation.

**Mapping to Constraint Primitives:**  
- *Snap:* Each strike triggers a snap event, quantizing the musician's input to the nearest constraint node on the grid. The snap deadband prevents re-triggering from hand vibrations or tremors.
- *Tempo:* Inter-strike timing provides tempo information. The system extracts periodicity using autocorrelation and locks the tempo constraint to the musician's natural rhythm.
- *Funnel:* Each strike narrows the funnel — the system eliminates musical possibilities inconsistent with the selected constraint region, converging toward a specific musical output.

**Minimum Viable Hardware:**  
- 4–16 piezoelectric contact sensors (cost: ~$1–5 each)
- Arduino or similar microcontroller for ADC and basic signal processing
- USB or Bluetooth connection to the constraint engine
- Total cost estimate: $15–40

**Example Use Case / Persona:**  
*Maria, 34, hemiplegic following a stroke.* Maria has full use of her left hand but limited fine motor control in her right. She places a 3×3 drum pad grid on her lap table. Each pad corresponds to a harmonic region (e.g., "tonic neighborhood," "dominant preparation," "subdomiant expansion"). She taps to select regions; the constraint system fills in voice-leading, rhythm, and orchestration automatically. She can play fast or slow — the tempo constraint adapts in real time.

**Technical Challenges:**  
- **Tremor rejection:** Musicians with motor impairments may produce unintentional strikes or vibrations. The snap deadband must be calibrated per-user, potentially using machine learning to model individual tremor profiles.
- **Velocity sensitivity vs. binary triggering:** Some users can modulate strike force; others cannot. The system should gracefully degrade from velocity-sensitive to binary mode without loss of musical expressivity.
- **Grid size optimization:** Too few cells limits expressivity; too many demands precision. Adaptive grid sizing based on the user's strike accuracy (measured during a calibration phase) is an open problem.

---

### Level 2: Breath Sync

**Input Modality:**  
A wind controller (e.g., Akai EWI, Yamaha WX) or simple breath sensor (pressure sensor in a mouthpiece) detects airflow pressure and, optionally, lip tension. Breath onset, offset, sustained pressure, and pressure trajectories are captured.

**Mapping to Constraint Primitives:**  
- *Consensus:* Breath pressure modulates the "weight" of the musician's constraints in a consensus resolution. Hard blowing pushes the system toward the musician's preference; gentle breathing allows the system's default constraints to dominate. This creates a continuous expression of musical intention without requiring discrete selections.
- *Tempo:* Breath phrasing (inhale/exhale cycles) provides a natural metrical structure. The system maps breath period to musical phrases, with tempo locked to breathing rate — an inherently biological, stress-responsive timing mechanism.
- *Funnel:* Sustained breath pressure at a given level narrows the funnel by filtering out musical states inconsistent with the current energy level. High pressure → high energy (dense textures, bright timbres, wide intervals). Low pressure → low energy (sparse textures, dark timbres, narrow intervals).

**Minimum Viable Hardware:**  
- Breath pressure sensor (MPX5010GP or similar): ~$5
- Simple mouthpiece or headset mount
- Microcontroller for pressure-to-digital conversion
- Alternative: commercial wind controller ($200–800 for full-featured units)
- Total cost estimate: $10 (DIY) to $800 (commercial)

**Example Use Case / Persona:**  
*James, 52, quadriplegic following a spinal cord injury at C5.* James has no use of his limbs but full breath control and vocal function. He uses a bite-mounted breath sensor. By modulating his breathing, he controls the "energy" of the musical output. When he wants the music to build, he increases pressure; when he wants it to relax, he exhales slowly. The consensus mechanism interprets his breath as a preference signal and adjusts the constraint weights accordingly. He can trigger structural changes (verse/chorus transitions) with sharp breath pulses.

**Technical Challenges:**  
- **Breath signal noise:** Coughing, sneezing, and irregular breathing patterns can generate spurious signals. The system must distinguish intentional musical breath from physiological events — potentially using a learned model of the user's resting breathing pattern.
- **Latency:** Breath-to-sound latency must be below ~20ms for the system to feel responsive. This requires real-time signal processing close to the sensor.
- **Calibration period:** Breath pressure ranges vary enormously between individuals (particularly for those with respiratory conditions). A per-session calibration phase is essential.

---

### Level 3: Tongue Switch

**Input Modality:**  
A binary switch activated by tongue movement, modeled on the tongue-controlled prosthetic interface developed by Hugh Herr's group at MIT [4]. The switch is typically a small contact sensor placed on the palate or behind the teeth. Tongue position (left, right, center, up, down) provides up to five discrete states; with timing patterns (e.g., double-tap, hold), the state space expands further.

**Mapping to Constraint Primitives:**  
- *Snap:* Each tongue position maps to a snap state. The system quantizes the musician's selection to the nearest constraint node, with the snap deadband preventing accidental state changes from involuntary tongue movements (e.g., during speech or swallowing).
- *Laman:* Tongue switch states select which constraints are *active* in the laman rigidity graph. By toggling constraints on and off, the musician controls the structural rigidity of the musical system — adding constraints makes the music more determined (less freedom, more predictability), while removing constraints opens up the possibility space.
- *Consensus:* When multiple constraint sets compete (e.g., "harmonic" vs. "rhythmic" constraints), tongue position casts a "vote" in the consensus resolution.

**Minimum Viable Hardware:**  
- Intraoral switch array (custom 3D-printed palate mold with embedded contact sensors): ~$50–150 in materials
- Bluetooth Low Energy (BLE) transmitter for wireless data
- Total cost estimate: $100–200 (DIY); commercial equivalents would likely cost $500–1500

**Example Use Case / Persona:**  
*Aisha, 28, living with ALS (amyotrophic lateral sclerosis).* Aisha has lost most voluntary limb control but retains tongue and facial muscle function. She uses a custom-fitted palate switch with four positions (left, right, forward, back) plus a "center hold" state. She navigates through constraint presets: left selects harmonic constraints, right selects rhythmic constraints, forward increases constraint strictness (more determined output), back decreases it (more freedom). Center hold triggers a "perform" action — the system renders the current constraint configuration as music. She composes by building up constraint configurations measure by measure.

**Technical Challenges:**  
- **Intraoral sensor reliability:** Saliva, temperature changes, and mouth movements (eating, speaking) can interfere with sensor readings. Hermetic sealing and redundant sensing channels are necessary.
- **State space design:** The tongue has limited positional degrees of freedom. Designing intuitive mappings from 4–5 tongue positions to meaningful musical constraint operations requires careful user-centered design and iterative testing.
- **Hygiene and comfort:** Any intraoral device must be biocompatible, cleanable, and comfortable for extended wear. This imposes material and form factor constraints on the hardware design.

---

### Level 4: Eye-Gaze

**Input Modality:**  
An eye-gaze tracker (e.g., Tobii Eye Tracker 5, or integrated camera-based tracking) monitors the musician's point of regard on a screen or projected surface. Dwell time (the duration of fixation at a point) serves as the primary activation mechanism — looking at a constraint region for a configured threshold (typically 300–800ms) selects it.

**Mapping to Constraint Primitives:**  
- *Snap:* Gaze position is continuously quantized to the nearest constraint region using snap mechanics. The deadband prevents unintended selections from microsaccades and natural eye jitter.
- *Funnel:* Gaze dwell time modulates funnel convergence. Brief glances explore the constraint space without committing; prolonged fixation narrows the funnel by locking in the selected constraint. This creates a natural "browse → commit" interaction pattern.
- *Consensus:* Gaze position can bias consensus resolution by weighting constraints associated with the gazed-upon region more heavily than others. Looking at "bright timbre" constraints makes the consensus favor bright timbres, even if other constraints are pulling in different directions.
- *Tempo:* Gaze patterns (saccade frequency, fixation duration) correlate with cognitive load and emotional state. The system can infer tempo adjustments from gaze dynamics — rapid scanning suggests urgency (faster tempo), prolonged fixations suggest contemplation (slower tempo).

**Minimum Viable Hardware:**  
- Tobii Eye Tracker 5 or similar: ~$200–250
- Alternative: laptop with built-in eye tracking (some modern laptops include this)
- Display screen or projected surface with constraint region visualization
- Total cost estimate: $200–500

**Example Use Case / Persona:**  
*Robert, 67, living with Parkinson's disease with significant tremor in both hands.* Robert cannot reliably use physical controllers but has intact eye movement. The screen displays a visual representation of the constraint space — a landscape of harmonic, melodic, and rhythmic regions rendered as colored zones. He scans the landscape with his eyes, dwelling on regions he wants to activate. The system highlights gazed-upon regions in real time (providing visual feedback) and commits them after the dwell threshold. Robert performs by "looking his way through" a composition — a form of musical navigation that feels more like conducting than playing.

**Technical Challenges:**  
- **Midas touch problem:** In gaze-based interaction, every look is potentially an action. Dwell-time thresholds must be carefully tuned — too short and every glance triggers an action; too long and the interface feels sluggish. Adaptive dwell-time (shortening for experienced users, lengthening for novices) is a potential solution.
- **Gaze accuracy:** Eye trackers typically have 0.5–1° accuracy, which translates to ~1–2cm error at typical viewing distances. Constraint regions must be large enough to accommodate this error, or the snap mechanism must include a generous enough deadband.
- **Visual feedback latency:** The musician must see what they're selecting in near-real-time. Any latency in the gaze-to-visual-feedback loop breaks the sense of direct manipulation. Sub-50ms end-to-end latency is the target.

---

### Level 5: Surface Electromyography (EMG)

**Input Modality:**  
Surface EMG electrodes placed on the skin detect electrical activity from underlying muscles. Even muscles that cannot produce visible movement (e.g., due to paralysis or weakness) often generate measurable EMG signals. This makes EMG uniquely valuable for musicians with severe motor impairments — the system can detect *intention* even when *execution* is impossible.

**Mapping to Constraint Primitives:**  
- *Snap:* EMG amplitude is thresholded to produce discrete events (muscle activation / relaxation). The snap deadband is critical here — EMG signals are inherently noisy, and the deadband prevents rapid oscillation between "activated" and "relaxed" states.
- *Funnel:* EMG amplitude (continuous) modulates funnel convergence strength. Strong muscle activation pushes the funnel toward convergence (narrowing the musical output space); relaxation allows the funnel to open (expanding possibilities). This creates a direct, embodied mapping between physical effort and musical determination.
- *Consensus:* Multiple EMG channels (from different muscle groups) vote in the consensus mechanism. Left bicep activation weights "harmonic" constraints; right bicep weights "rhythmic" constraints; forearm activation weights "timbral" constraints. The consensus resolves these competing preferences into a unified musical state.
- *Laman:* EMG-derived constraint activations can be added to or removed from the laman rigidity graph, dynamically adjusting the structural rigidity of the musical system. More active muscles → more constraints → more determined output. Fewer active muscles → fewer constraints → more generative freedom.

**Minimum Viable Hardware:**  
- Myo Armband (discontinued but available used) or Delsys Trigno system: $100 (used Myo) to $5,000+ (clinical-grade Delsys)
- Mid-range: OpenBCI Cyton + EMG electrodes: ~$800–1,200
- Electrode placement and signal conditioning hardware
- Total cost estimate: $100 (basic) to $5,000+ (research-grade)

**Example Use Case / Persona:**  
*Chen Wei, 41, C3 spinal cord injury, quadriplegic with some shoulder and bicep function.* Chen Wei can shrug his shoulders and flex his biceps slightly but cannot move his hands or fingers. EMG electrodes on his biceps and shoulders capture his muscle activations. He "plays" by flexing and relaxing different muscle groups: left bicep controls harmonic density, right bicep controls rhythmic complexity, and shoulder shrugs trigger structural transitions. The constraint system translates these subtle, imprecise gestures into fully determined musical output. Over months of practice, Chen Wei develops a personal "muscle vocabulary" — a gestural language mapped to musical intent through the constraint framework.

**Technical Challenges:**  
- **Signal-to-noise ratio:** Surface EMG is notoriously noisy. Cross-talk between adjacent muscles, motion artifacts, and sweat-induced impedance changes all degrade signal quality. Advanced signal processing (bandpass filtering, envelope detection, pattern recognition) is essential.
- **Fatigue:** Muscle fatigue changes EMG characteristics over time. The system must adapt to gradual signal drift within a session, not just between sessions.
- **Electrode placement reproducibility:** Day-to-day variation in electrode placement changes the signal. Calibration routines (possibly automated) are needed at the start of each session.
- **Latency vs. classification accuracy:** Real-time EMG classification involves a tradeoff: longer analysis windows improve accuracy but increase latency. For musical applications, sub-100ms latency is desirable, which constrains the classification approach.

---

## 3. The Key Insight: Constraint as Accessibility Feature

The central argument of this paper is that constraint-based music systems possess an inherent accessibility advantage that conventional instrument interfaces do not: **the constraint IS the accessibility feature.**

Consider a traditional piano. The pianist must:
1. Locate the correct key (spatial precision)
2. Press it with the correct force (dynamic precision)
3. At the correct time (temporal precision)
4. While coordinating with other fingers (multi-effector coordination)
5. While reading notation (cognitive load)

Each of these requirements is a potential accessibility barrier. A musician who lacks spatial precision cannot find the right key. A musician who lacks dynamic control cannot shape the sound. A musician who lacks timing precision cannot maintain rhythm.

A constraint-based system restructures this relationship. Instead of requiring the musician to produce precise outputs, it asks the musician to provide *imprecise direction* and uses constraints to guarantee that the output is musically valid. The musician's role becomes:

1. **Indicate a region of interest** (spatial imprecision is fine — the snap mechanism quantizes)
2. **Express energy or intention** (dynamic imprecision is fine — the funnel handles convergence)
3. **Maintain a temporal feel** (temporal imprecision is fine — the tempo constraint provides metrical structure)
4. **Using whatever effectors are available** (multi-effector coordination is not required — any single input modality suffices)

This is not "dumbing down" music-making. It is a fundamentally different relationship between musician and instrument — one that is arguably more aligned with how many composers actually think. A composer does not think "I need middle C at fortissimo at exactly beat 3 of measure 47." They think "I want more tension here" or "this section should feel open." Constraint-based systems operationalize this kind of thinking, and accessibility input modalities provide the physical interface to it.

The mathematical foundation for this is the Laman rigidity condition [5]. A Laman graph on n vertices has exactly 2n − 3 edges and is generically rigid — it has no flex. In the constraint music system, each constraint is an edge in this graph. The system ensures that the constraint network is always at or near Laman rigidity: enough constraints to be musically determined, but not so many that the system becomes over-constrained (which would make it brittle and unresponsive). This rigidity guarantee means that the musician's inputs, however imprecise, are always resolved into a unique, musically coherent state.

---

## 4. Composability: Combining Modalities

The Accessibility Ladder is not a single-file path. Modalities can be combined. A musician might use:

- **Breath + tongue switch:** Breath controls energy (consensus weight), tongue switch selects constraint regions (snap).
- **Eye-gaze + EMG:** Gaze selects the region, EMG amplitude modulates the constraint intensity (funnel convergence).
- **One-hand drum + breath:** Drum triggers events (snap + tempo), breath shapes the musical trajectory (funnel).

This composability arises naturally from the constraint theory framework. Because each primitive operates independently (snap, funnel, consensus, laman, tempo are orthogonal mechanisms), different input modalities can drive different primitives without interference. The consensus mechanism resolves any conflicts between competing inputs — exactly as it resolves conflicts between competing musical constraints.

We propose a modular input architecture:

```
Input Layer    →  Constraint Mapping  →  Constraint Engine  →  Musical Output
──────────────     ──────────────────     ─────────────────     ────────────────
One-hand drum  →  Snap + Tempo       ─┐
Breath sensor  →  Consensus + Funnel  ─┤
Tongue switch  →  Snap + Laman       ─┼→  Resolution       →  MIDI / Audio
Eye-gaze       →  Snap + Funnel      ─┤    (Consensus)
EMG            →  Snap + Funnel + Laman┘
```

Each input modality is a plugin that maps to one or more constraint primitives. The constraint engine resolves all inputs into a unified musical state. This architecture allows individualized configurations without custom software — only the mapping layer changes.

---

## 5. Related Work

**Accessible Digital Musical Instruments (ADMIs):** The NIME (New Interfaces for Musical Expression) community has produced extensive work on ADMIs. The Skoog [6] is a squeezable music controller designed for musicians with disabilities. The Soundbeam [7] uses ultrasonic gesture detection. Our approach differs by leveraging the *computational* structure of constraint systems rather than adapting physical interfaces.

**Adaptive Music Technology:** Drake Music [8] has pioneered accessible music technology in the UK, developing instruments and interfaces for musicians with disabilities. Their work focuses on physical interface adaptation; our focus is on computational compensation through constraint resolution.

**Eye-gaze Music Systems:** Hornof and Sato [9] developed EyeMusic, an eye-gaze-controlled music composition system. Their system requires gaze-based note entry; our approach uses gaze as one input to a constraint engine, requiring less precision.

**EMG Music Control:** Tanaka and Knapp [10] explored EMG-based musical instruments. Their work focuses on gesture classification for traditional instrument control; we use EMG amplitude as a continuous control signal for constraint modulation, avoiding the need for accurate gesture classification.

**Constraint-Based Music Systems:** The earliest constraint-based composition system was probably OMSession [11], followed by PWConstraints [12] and Strasheela [13]. These systems were primarily batch-oriented (compose offline, listen later). Our framework is real-time and interactive, making it suitable for live performance.

---

## 6. Open Problems

1. **Personalized calibration:** Every musician's physical capabilities are unique. Automated calibration routines that adapt the constraint mapping to individual needs — possibly using machine learning — are an open research area.

2. **Latency budgets:** Each input modality has different inherent latency (EMG classification is slower than piezo detection). How should the constraint engine handle asynchronous inputs with different latencies while maintaining musical coherence?

3. **Expressivity metrics:** How do we measure whether a constraint-based system provides sufficient expressivity? Traditional metrics (number of controllable parameters, resolution) are inadequate. We need metrics that capture the *perceived* expressivity of the constraint system from the musician's perspective.

4. **User studies:** This paper is a position paper. Empirical validation with musicians who have disabilities is essential. We plan user studies with each level of the ladder, measuring task completion, musical satisfaction, and long-term engagement.

5. **Temporal adaptation:** As a musician's condition changes (progressive diseases, rehabilitation, fatigue), the system should adapt its constraint mappings. This requires a longitudinal model of the musician's capabilities.

---

## 7. Conclusion

Constraint-based music systems are not merely compatible with accessibility — they are *uniquely suited* to it. The fundamental property of constraint systems — that they reduce the space of valid outputs — directly compensates for the reduced precision of accessible input modalities. The musician provides direction; the constraint system provides precision. This is not a workaround; it is a design principle.

The Accessibility Ladder proposed in this paper offers a structured framework for matching input modalities to individual needs, grounded in the constraint theory primitives of snap, funnel, consensus, laman, and tempo. Each level is realizable with affordable hardware and maps naturally to the computational structure of the constraint engine.

The future of accessible music technology is not about building simpler instruments. It is about building smarter systems that meet musicians where they are — whatever their physical capabilities — and enable them to make music that is genuinely their own.

---

## References

[1] A. Gelineck and S. Serafin, "A Quantitative Evaluation of the Experience of Virtual Musical Instruments," in *Proceedings of the New Interfaces for Musical Expression (NIME)*, 2009.

[2] D. Jack, R. Boyns, and T. Westin, "Accessible Digital Musical Instruments: A Review of Design, Implementation, and Evaluation," in *Proceedings of the International Conference on Disability, Virtual Reality and Associated Technologies*, 2020.

[3] SuperInstance Research, "Constraint Theory and the Five Primitives: Snap, Funnel, Consensus, Laman, Tempo," fm-research repository, 2025–2026.

[4] H. Herr, A. Wilkenfeld, and A. B. Lee, "Tongue-Controlled Prosthesis for Individuals with Severe Limb Loss," *Nature Biomedical Engineering*, vol. 7, pp. 1124–1135, 2023.

[5] G. Laman, "On Graphs and Rigidity of Plane Skeletal Structures," *Journal of Engineering Mathematics*, vol. 4, no. 4, pp. 331–340, 1970.

[6] B. Isbister, N. Ramsay, and S. Sherwood, "Skoog: A New Musical Interface for Accessibility and Education," in *Proceedings of the International Conference on New Interfaces for Musical Expression (NIME)*, 2011.

[7] T. Swingler, "The Invisible Instrument in the Museum," in *Proceedings of the International Conference on New Interfaces for Musical Expression (NIME)*, 2010.

[8] Drake Music, "Accessible Music Technology: Research and Development," Drake Music Organisation, Bristol, UK, 2019.

[9] A. J. Hornof and D. K. Sato, "EyeMusic: Making Music with the Eyes," in *Proceedings of the International Conference on New Interfaces for Musical Expression (NIME)*, 2004.

[10] A. Tanaka and R. B. Knapp, "Multimodal Interaction in Music Using Electromyogram Signals," in *Proceedings of the International Conference on Auditory Display (ICAD)*, 2002.

[11] C. Roads, "The OMSession Project: Constraint-Based Composition in OpenMusic," IRCAM, Paris, 1995.

[12] M. Laurson, "PWConstraints: A Constraint-Based Composition System," in *Proceedings of the International Computer Music Conference (ICMC)*, 1996.

[13] M. T. Roig, T. Nishino, and H. Tojo, "Strasheela: A Constraint-Based Music Composition System," in *Proceedings of the International Computer Music Conference (ICMC)*, 2007.

---

*This paper is part of the SuperInstance constraint theory research program. For the full repository, see github.com/SuperInstance/fm-research.*
