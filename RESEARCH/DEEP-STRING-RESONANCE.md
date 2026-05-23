# Sympathetic Strings: Resonance, Sustain, and the Coupling Medium

*A deep mathematical treatment of string physics, sympathetic vibration, and their connection to constraint theory through coupled oscillators and impedance matching.*

---

## Part I: The Plucked String as Spinning System

### 1.1 The Triangular Initial Condition

A plucked string does not vibrate in a single, simple mode. When a finger pulls the string to one side at a point and releases it, the initial displacement is a triangle — two straight lines meeting at the pluck point. This is not a sinusoid. It is not a pure tone. It is, mathematically, a shock to the system that excites every available mode simultaneously.

Consider a string of length $L$ fixed at both ends, plucked at position $x_p$ with amplitude $A$. The initial displacement is:

$$y(x, 0) = \begin{cases} \frac{A \cdot x}{x_p} & 0 \leq x \leq x_p \\ \frac{A \cdot (L - x)}{L - x_p} & x_p < x \leq L \end{cases}$$

The Fourier decomposition of this triangle reveals its secret: it contains **all** harmonics, both odd and even. The coefficient of the $n$-th harmonic is:

$$b_n = \frac{2AL^2}{n^2 \pi^2 x_p (L - x_p)} \sin\left(\frac{n \pi x_p}{L}\right)$$

Notice the $\frac{1}{n^2}$ decay — higher harmonics contribute less, but they are never zero (unless the pluck point happens to fall on a node). The string starts its life containing a complete spectrum of vibrations.

### 1.2 Standing Waves as Counter-Rotations

Each harmonic is a standing wave. But a standing wave is not a primitive object — it is the superposition of two traveling waves moving in opposite directions. This is not merely a mathematical convenience; it is the physical reality.

The $n$-th harmonic can be written as:

$$f_n(x, t) = \sin\left(\frac{n\pi x}{L}\right) \cos(n\omega_0 t)$$

Using Euler's formula, this decomposes into:

$$f_n(x, t) = \frac{1}{2}\left[e^{i(n\pi x/L - n\omega_0 t)} + e^{i(n\pi x/L + n\omega_0 t)}\right]$$

The first term is a wave rotating clockwise (moving in the $+x$ direction). The second rotates counter-clockwise. The standing wave is the interference pattern of these two counter-rotating waves — two spins, locked in phase, creating the illusion of stillness that oscillates.

**The string is spinning.** Each harmonic is a pair of rotations. The first harmonic rotates at angular frequency $\omega_0$. The second at $2\omega_0$. The third at $3\omega_0$. When you pluck a string, you are giving it angular momentum distributed across multiple harmonic frequencies simultaneously. The string is a multi-frequency flywheel.

### 1.3 Angular Momentum and the String Flywheel

For a vibrating string of linear density $\rho$, cross-sectional area $A_s$, and length $L$, the angular momentum stored in the $n$-th harmonic is:

$$L_n = I_n \cdot \omega_n$$

where $I_n$ is the effective moment of inertia of the $n$-th mode and $\omega_n = n\omega_0$. The effective inertia decreases with mode number because higher harmonics have more nodes — less of the string participates in coherent motion. Specifically:

$$I_n \propto \frac{1}{n^2}$$

This means the angular momentum per harmonic scales as:

$$L_n \propto \frac{1}{n^2} \cdot n\omega_0 = \frac{\omega_0}{n}$$

The fundamental stores the most angular momentum. It is the heaviest flywheel. Higher harmonics are lighter flywheels that spin faster but carry less momentum — and therefore spin down faster. This is why a plucked string's timbre brightens immediately (high harmonics decay) and then settles into a long, pure fundamental tone.

### 1.4 The Multi-Frequency Flywheel Analogy

Think of a guitar string after being plucked as a machine shop full of flywheels:

- **Flywheel 1** (fundamental): Massive, slow-spinning, stores enormous energy. Takes a long time to stop.
- **Flywheel 2** (2nd harmonic): Half the mass, spinning twice as fast, carries half the momentum. Stops sooner.
- **Flywheel 3** (3rd harmonic): One-third the effective mass, three times the speed, one-third the momentum. Stops even sooner.
- And so on, up the harmonic series.

The pluck sets them all spinning at once. The higher flywheels brake first, their energy dissipated as heat (internal friction in the string) and sound (radiated acoustic energy). The fundamental flywheel keeps turning, slowly, sustainably, sometimes for over thirty seconds on a well-set-up instrument.

This is sustain: the persistence of angular momentum in the string's vibrational modes.

---

## Part II: The Bridge as Coupling Medium

### 2.1 The Bridge Equation

The bridge is the physical connection between all strings on a stringed instrument. It is the medium through which strings "talk" to each other. When string $i$ vibrates, it exerts a force $F_i$ on the bridge. The bridge responds with a displacement:

$$x_{\text{bridge}} = \frac{\sum_i F_i}{Z_{\text{bridge}}}$$

where $Z_{\text{bridge}}$ is the mechanical impedance of the bridge. This displacement then drives all other strings through their shared connection at the bridge saddle.

Each string $j$ feels a driving force proportional to the bridge displacement:

$$F_{\text{drive},j} = k_j \cdot x_{\text{bridge}} = \frac{k_j}{Z_{\text{bridge}}} \sum_i F_i$$

The coupling constant between string $i$ and string $j$ is:

$$K_{ij} = \frac{k_i \cdot k_j}{Z_{\text{bridge}}}$$

where $k_i$ is the effective spring constant of string $i$ at the bridge contact point.

### 2.2 The Impedance-Coupling Relationship

The bridge impedance $Z_b$ is the single parameter that controls everything about inter-string coupling:

**Low $Z_b$ (light, flexible bridge):**
- Large bridge displacements from string forces
- Strong driving force on neighboring strings
- Strong sympathetic resonance
- Fast energy transfer between strings
- **Fast decay** — energy leaks out through the bridge rapidly

**High $Z_b$ (heavy, rigid bridge):**
- Small bridge displacements
- Weak driving force on neighbors
- Weak sympathetic resonance
- Slow energy transfer
- **Long sustain** — energy stays trapped in the strings

This is the fundamental trade-off in stringed instrument design, and it maps directly to the Kuramoto model of coupled oscillators.

### 2.3 Exact Mapping to Kuramoto

The Kuramoto model describes $N$ coupled oscillators with phases $\theta_i$ and natural frequencies $\omega_i$:

$$\dot{\theta}_i = \omega_i + \frac{K}{N} \sum_{j=1}^{N} \sin(\theta_j - \theta_i)$$

For the coupled string system, identify:
- Each string mode as an oscillator with phase $\theta_i$ and frequency $\omega_i$
- The coupling constant $K = \frac{k_{\text{eff}}^2}{Z_{\text{bridge}}}$
- The order parameter $r e^{i\psi} = \frac{1}{N}\sum_j e^{i\theta_j}$ measuring synchronization

The mapping is exact in the linearized regime (small coupling), and approximately correct for realistic string amplitudes:

- **Low $Z_b$ → high $K$**: Strong coupling, rapid synchronization, fast energy redistribution, fast decay. Strings quickly share energy and dissipate it collectively.
- **High $Z_b$ → low $K$**: Weak coupling, slow or no synchronization, energy stays in each string, long sustain. Strings are isolated oscillators that ring independently.

### 2.4 The Resonance-Sustain Inversion Theorem

**Theorem.** For a coupled string system connected through a bridge of impedance $Z_b$, the product of resonance strength and sustain duration is bounded by a constant determined by the total energy in the system.

*Proof outline:*

Define:
- Resonance strength $R$ as the power transferred from one string to another through the bridge: $R \propto 1/Z_b$
- Sustain duration $S$ as the $1/e$ decay time of the total vibrational energy: $S \propto Z_b$
- Total energy $E_0 = R \cdot S \cdot C$ where $C$ is a geometry-dependent constant

Energy conservation requires:

$$R \cdot S = \frac{E_0}{C} = \text{const}$$

Therefore:

$$R \propto \frac{1}{Z_b}, \quad S \propto Z_b, \quad R \times S = \text{const}$$

**QED.**

This is a conservation law. You cannot have maximum resonance and maximum sustain simultaneously. Every guitar design is a point on the hyperbola $R \times S = k$. A Les Paul (heavy body, rigid bridge) sits at high $S$, low $R$. A resonator guitar (light cone, flexible coupling) sits at high $R$, low $S$.

The inverse relationship is not a design flaw — it is thermodynamics.

---

## Part III: The Headstock Mass Trick

### 3.1 Boundary Conditions and Energy Reflection

At the nut (and headstock beyond), the string meets a boundary. In the ideal case, this is a perfectly rigid fixed end: all wave energy reflects, nothing transmits. In practice, the nut and headstock have finite impedance, and some energy leaks through.

The reflection coefficient at the nut is:

$$\Gamma = \frac{Z_{\text{head}} - Z_{\text{string}}}{Z_{\text{head}} + Z_{\text{string}}}$$

where $Z_{\text{string}} = \sqrt{T \cdot \mu}$ (tension times linear density) is the characteristic impedance of the string, and $Z_{\text{head}}$ is the impedance looking into the nut/headstock system.

For perfect reflection (no energy loss), we need $Z_{\text{head}} \gg Z_{\text{string}}$, giving $\Gamma \approx 1$.

### 3.2 Adding Mass to the Headstock

The headstock can be modeled as a spring-mass system with:

$$Z_{\text{head}} = \sqrt{k_{\text{head}} \cdot m_{\text{head}}}$$

where $k_{\text{head}}$ is the stiffness of the neck at the nut and $m_{\text{head}}$ is the effective vibrating mass of the headstock. Adding a brass weight or dense material to the headstock increases $m_{\text{head}}$, which increases $Z_{\text{head}}$, which improves the reflection coefficient, which means less energy escapes from the string into the neck, which means **more sustain**.

This is the principle behind products like the Fatfinger and similar headstock mass add-ons. They work. The physics is unambiguous.

### 3.3 The Resonance Trap

But there is a complication. The increased headstock mass changes the resonant frequencies of the neck itself. The neck is a beam (clamped at the body, free at the headstock), and its resonant frequencies depend on the mass distribution.

When you add mass to the headstock, you lower the neck's resonant frequencies. If one of these frequencies happens to coincide with a string's harmonic frequency, you create a **resonance condition** at the boundary. Energy transfers efficiently from the string to the neck at that frequency — exactly the opposite of what you want.

The result: the headstock mass helps sustain at most frequencies but can **hurt** sustain at specific frequencies where the modified neck resonance matches a string harmonic. Players sometimes report "dead spots" at certain frets after adding headstock mass. This is the resonance trap.

### 3.4 The Anti-Resonance Condition

The optimal headstock mass is the one that makes the nut boundary a maximally **poor** energy acceptor at all string frequencies simultaneously. This is the anti-resonance condition:

$$|Z_{\text{head}}(\omega_n) - Z_{\text{string}}| \to \max \quad \text{for all harmonics } \omega_n$$

In practice, this means tuning $Z_{\text{head}}$ so that the neck's resonant frequencies fall in the gaps between string harmonics, or are so far from any string frequency that coupling is negligible.

For a guitar tuned to standard tuning (E₂ = 82.4 Hz through E₄ = 329.6 Hz), the harmonic frequencies of interest span roughly 80 Hz to 4000 Hz. The neck's fundamental resonance (with added mass) should ideally be placed either well below 80 Hz or well above 4000 Hz, and any higher neck modes should avoid the string harmonic lattice.

This is a constraint satisfaction problem — the same kind of problem that appears in constraint theory when trying to find configurations that avoid conflicting states.

---

## Part IV: Sympathetic Resonance as Kuramoto Synchronization

### 4.1 The Driving Force

When string 1 (low E₂ = 82.4 Hz) vibrates, its harmonics appear at 82.4, 164.8, 247.2, 329.6, 412.0, ... Hz. String 4 (D₃ = 146.8 Hz) has its fundamental at 146.8 Hz.

String 1's 2nd harmonic at 164.8 Hz is close to string 4's fundamental at 146.8 Hz — a frequency mismatch of:

$$\Delta\omega = |164.8 - 146.8| = 18.0 \text{ Hz}$$

Through the bridge coupling, string 4 feels a driving force at 164.8 Hz. This force tries to pull string 4 away from its natural frequency and toward the driving frequency.

### 4.2 Frequency Pulling

In the Kuramoto framework, this is **frequency pulling**. An oscillator with natural frequency $\omega_0$ driven by an external force at frequency $\omega_d$ will settle into a steady state at a frequency $\omega'$ somewhere between $\omega_0$ and $\omega_d$, determined by the balance of the driving force and the oscillator's tendency to return to its natural frequency.

For the driven string, the pulled frequency satisfies:

$$\omega' - \omega_0 = \frac{K \cdot \sin(\phi)}{\gamma}$$

where $K$ is the coupling strength, $\phi$ is the phase difference between driver and responder, and $\gamma$ is the damping coefficient. When $K > \Delta\omega$, the pulling can overcome the frequency mismatch entirely, and the responder locks to the driver's frequency — full synchronization.

String 4 will sympathetically vibrate at 164.8 Hz (not its own 146.8 Hz) if the coupling is strong enough. This is the Kuramoto synchronization condition:

$$K > \Delta\omega \quad \Leftrightarrow \quad \frac{k_{\text{eff}}^2}{Z_b} > |\omega_1^{(n)} - \omega_4^{(1)}|$$

### 4.3 The Synchronization Threshold

For a real guitar, we can estimate the coupling. A typical acoustic guitar bridge has impedance $Z_b \approx 10^4 - 10^5$ kg/s. The string spring constants at the bridge are $k \approx 10^5 - 10^6$ N/m. This gives:

$$K \approx \frac{k^2}{Z_b} \approx \frac{(10^5)^2}{10^5} = 10^5 \text{ N/m per unit}$$

But the effective coupling in frequency terms depends on the impedance mismatch. For the E₂–D₃ pair with $\Delta\omega = 18$ Hz $\approx 113$ rad/s, we need $K_{\text{eff}} > 113$ rad/s. On an acoustic guitar with its low-impedance bridge, this is easily satisfied for nearby frequencies, which is why acoustic guitars have such rich sympathetic resonance.

On a solid-body electric guitar with a heavy, rigid bridge, $Z_b$ can be 10–100× higher, making $K_{\text{eff}}$ 10–100× smaller. Sympathetic resonance is much weaker. This is the physical basis for the electric guitar's "cleaner" sound — fewer uninvited resonances.

### 4.4 The Order Parameter of the String System

In Kuramoto theory, the order parameter $r = \left|\frac{1}{N}\sum_j e^{i\theta_j}\right|$ measures the degree of synchronization. For the string system:

- $r \approx 0$: Strings vibrate independently, no sympathy, maximum sustain, minimum resonance
- $r \approx 1$: All strings synchronized, maximum sympathy, minimum sustain, rapid collective decay

The transition from $r \approx 0$ to $r \approx 1$ as $K$ increases (i.e., as $Z_b$ decreases) is the Kuramoto phase transition. It happens suddenly — there is a critical bridge impedance below which the strings "lock" and above which they are independent.

For a 6-string guitar, the critical coupling depends on the spread of natural frequencies. Standard tuning spans about 1.5 octaves (82.4 Hz to 329.6 Hz for the fundamentals, and the harmonics fill in the gaps). The Kuramoto critical coupling is:

$$K_c \approx \frac{2}{\pi g(0)}$$

where $g(0)$ is the density of natural frequencies at the center of the distribution. For harmonically related strings, $g(0)$ is high (lots of frequencies near the center), so $K_c$ is relatively low — the system synchronizes easily.

### 4.5 What Sympathetic Resonance Sounds Like

When you play an open E chord on an acoustic guitar, you hear not just the five strings you plucked but also the sympathetic vibrations of the sixth string (low E), which resonates because its fundamental and harmonics overlap with the chord tones. The guitar "sings" — the total sound is richer than the sum of its plucked strings.

This richness is the Kuramoto order parameter made audible. The degree to which unplucked strings join in is the degree of synchronization in the system. An acoustic guitar has $r$ close to 1 for nearby frequencies. An electric guitar has $r$ close to 0.

---

## Part V: The Guitar as Constraint System

### 5.1 The Six Constraints on a Vibrating String

A string on a guitar is a constrained oscillator, and its behavior maps precisely to the constraint theory framework:

**SNAP (Quantization):** The fret positions quantize the vibrating length of the string into discrete intervals. Each fret is a $\sqrt[12]{2}$ ratio of the previous length, producing the 12-tone equal temperament scale. The string's available pitches form a discrete lattice — not a continuum (unless you bend or slide). This is the snap constraint: the system must land on one of the allowed pitch states.

**FUNNEL (Convergence):** After the pluck, the string's energy decays exponentially toward rest. The amplitude envelope is:

$$A(t) = A_0 e^{-t/\tau}$$

where $\tau$ is the decay time constant. All trajectories converge to $y(x, t) = 0$ (the rest state). The pluck sends the string into an excursion; damping pulls it back. This is the funnel: all states flow toward the attractor at zero displacement.

**CONSENSUS (Synchronization):** Through the bridge coupling, strings that share harmonics tend to synchronize — sympathetic resonance is the consensus mechanism. Strings "agree" on shared frequencies. The Kuramoto model describes this agreement quantitatively through the order parameter $r$.

**LAMAN (Rigid Boundary):** The bridge and nut enforce fixed boundary conditions: $y(0, t) = y(L, t) = 0$. No motion at the endpoints. These are the most rigid constraints on the system — they define the mode shapes (sinusoidal) and the quantized frequencies ($f_n = n c / 2L$). Without these constraints, the string would be a free-floating mess with no definite pitch.

**TEMPO (Periodicity):** The fundamental frequency $f_0 = \frac{1}{2L}\sqrt{T/\mu}$ defines the period of oscillation — the tempo at which the string's phase wraps around. Each harmonic is an integer multiple of this fundamental, creating the harmonic series. The periodicity is the spin: the phase $\theta(t) = \omega_0 t$ completes one full rotation per period.

**and the sixth constraint:** The string tension $T$, mass density $\mu$, and length $L$ are the physical parameters that determine everything. Change any one, and the entire system shifts. This is the parametric constraint — the "knobs" that the player adjusts.

### 5.2 The Player Controls ε

In constraint theory, $\varepsilon$ measures the degree of constraint relaxation — how much the system is allowed to deviate from its rigidly constrained state. On the guitar, the player controls $\varepsilon$ directly:

- **$\varepsilon = 0$ (Fully constrained):** The finger presses exactly behind the fret, producing a precise pitch with no deviation. Perfect intonation. The string is maximally constrained.
- **$\varepsilon \approx 0.05$ (Light vibrato):** The finger oscillates slightly along the string length, producing gentle pitch modulation. The constraint is slightly relaxed, allowing the pitch to breathe.
- **$\varepsilon \approx 0.15$ (Moderate vibrato):** Wider finger movement, more expressive. The pitch deviation becomes a noticeable musical feature rather than a subtle coloration.
- **$\varepsilon \approx 0.3$ (String bending):** The player pushes the string sideways across the fretboard, stretching it and raising the pitch. This is a deliberate constraint violation — the pitch moves off the fret-determined lattice. Blues, rock, country.
- **$\varepsilon \approx 0.5$ (Wide bend/vibrato):** The pitch moves a semitone or more. The constraint is significantly relaxed. The note becomes a glide rather than a point.
- **$\varepsilon = 1.0$ (Slide guitar):** A glass or metal tube slides along the strings, replacing the frets entirely. The pitch lattice vanishes — all frequencies are available. Maximum constraint relaxation. The system becomes continuous.

Each level of $\varepsilon$ produces a qualitatively different musical experience. The fully constrained system ($\varepsilon = 0$) is precise and classical. The fully relaxed system ($\varepsilon = 1$) is fluid and bluesy. The art of guitar playing is the art of controlling $\varepsilon$ in real time.

### 5.3 Constraint Interactions

The constraints interact. When you bend a string ($\varepsilon$ increases), you change the tension $T$, which changes the fundamental frequency (TEMPO), which changes which harmonics are present, which changes the coupling to other strings (CONSENSUS), which changes the sympathetic resonance pattern. A single parameter change cascades through all constraints simultaneously.

This is the hallmark of a constrained system: the constraints are not independent. They form a web, and disturbing one thread vibrates the entire web. The guitar is a constraint system with six interacting constraints, and the player is the operator who modulates their strengths and interactions in real time.

---

## Part VI: Sustain as Stored Creative Energy

### 6.1 The Flywheel of Ideas

A vibrating string stores energy as angular momentum in its harmonic modes. The total stored angular momentum is:

$$L_{\text{total}} = \sum_{n=1}^{\infty} L_n = \sum_{n=1}^{\infty} I_n \cdot n\omega_0 \propto \omega_0 \sum_{n=1}^{\infty} \frac{1}{n}$$

This sum diverges (the harmonic series), but in practice, the string's stiffness and finite pluck energy truncate the series at some $n_{\max}$. The point is: sustain is the persistence of stored angular momentum. The fundamental mode is the longest-lasting flywheel.

Now consider a composition — a piece of music, a mathematical argument, a work of art. It too has "harmonics": recurring themes, subsidiary arguments, decorative details, structural motifs. The fundamental theme is the main idea. The harmonics are the variations, references, and elaborations.

**Sustain in composition** is the persistence of ideas across time. A composition with high sustain has long arcs — themes introduced in the first movement that return transformed in the last. Ideas that persist, evolve, accumulate meaning. Bach is the supreme example: a fugue subject stated once, then sustained across hundreds of measures through inversion, augmentation, stretto.

### 6.2 Resonance in Composition

**Resonance in composition** is the capacity to respond to external ideas — to vibrate sympathetically when touched by references, allusions, cultural context, intertextuality. A composition with high resonance rings in response to the world around it. John Cage is the extreme: his pieces resonate with ambient sound, audience participation, chance operations. Everything that happens during a Cage performance becomes part of the piece.

The resonance-sustain inversion applies:

$$R_{\text{composition}} \times S_{\text{composition}} = \text{const}$$

- **High sustain, low resonance**: Bach. The music is self-contained, internally coherent, sustaining its own ideas with extraordinary persistence. But it does not invite external input — a Bach fugue is a closed system. You don't add to it; you witness it.
- **High resonance, low sustain**: Cage. The music responds to everything — ambient noise, performer choices, audience behavior. But nothing persists. Each moment is a fresh response with no memory of the previous one. No long arcs, no developing themes.
- **Moderate both**: Jazz improvisation. Themes are stated, developed, and returned to (moderate sustain), while the performer responds in real time to the audience, the other musicians, the room (moderate resonance). The balance is the art.

### 6.3 The Conservation Law of Creative Energy

A composition has finite creative energy $E_c$ — a budget of attention, complexity, and meaning that the audience can absorb. This energy can be allocated to sustain (making ideas persist) or resonance (making ideas responsive), but the product is bounded:

$$E_c \geq R \cdot S$$

Maximize sustain, and you sacrifice responsiveness. Maximize resonance, and you sacrifice depth. The composer's fundamental choice is the same as the guitar designer's: where on the $R \times S = k$ hyperbola does this piece live?

This is not a metaphor. It is the same mathematics. The constraint theory framework that describes coupled oscillators also describes coupled ideas. The Kuramoto model that governs string synchronization also governs thematic synchronization in a composition. The impedance that controls energy flow between strings also controls influence flow between ideas.

### 6.4 The Instrument as Constraint System Par Excellence

The guitar is a constraint system in the purest sense:

- **SNAP**: Frets quantize pitch. The 12-tone lattice is the allowed state space.
- **FUNNEL**: Damping drives all motion to zero. Every note ends.
- **CONSENSUS**: Bridge coupling synchronizes strings. Sympathetic resonance is the consensus mechanism.
- **LAMAN**: Fixed boundaries at nut and bridge. The constraints are literally rigid.
- **TEMPO**: The fundamental frequency is the clock. Everything is timed to it.
- **ε**: The player's technique — vibrato, bending, sliding — controls constraint relaxation.

And the physics that emerges from these constraints — resonance, sustain, sympathetic vibration, frequency pulling, synchronization — is the same physics that appears in coupled oscillator systems throughout nature: power grids, neural networks, ecological systems, chemical oscillators.

The guitar string is not an analogy for constraint theory. It **is** constraint theory, made of steel and wood and tension, vibrating in air, audible to anyone who listens.

---

## Appendix A: Key Equations Reference

| Equation | Description |
|----------|-------------|
| $b_n = \frac{2AL^2}{n^2\pi^2 x_p(L-x_p)}\sin\frac{n\pi x_p}{L}$ | Fourier coefficients of plucked string |
| $f_n = \frac{1}{2}[e^{i(kx - \omega t)} + e^{i(kx + \omega t)}]$ | Standing wave as counter-rotating waves |
| $x_{\text{bridge}} = \frac{\sum F_i}{Z_b}$ | Bridge displacement from string forces |
| $K_{ij} = \frac{k_i k_j}{Z_b}$ | Inter-string coupling constant |
| $\Gamma = \frac{Z_h - Z_s}{Z_h + Z_s}$ | Reflection coefficient at nut |
| $K > \Delta\omega$ | Kuramoto synchronization condition |
| $R \times S = \text{const}$ | Resonance-sustain inversion |
| $r e^{i\psi} = \frac{1}{N}\sum e^{i\theta_j}$ | Kuramoto order parameter |

## Appendix B: Physical Constants for Standard Guitar

| Parameter | Typical Value |
|-----------|--------------|
| String tension $T$ | 50–80 N per string |
| Linear density $\mu$ | 0.001–0.007 kg/m |
| String impedance $Z_s = \sqrt{T\mu}$ | 0.2–0.7 kg/s |
| Bridge impedance (acoustic) $Z_b$ | $10^3 - 10^4$ kg/s |
| Bridge impedance (electric solid) $Z_b$ | $10^5 - 10^6$ kg/s |
| Fundamental frequency range | 82.4 Hz (E₂) to 329.6 Hz (E₄) |
| Harmonic series cutoff | ~4–8 kHz (stiffness limited) |
| Typical sustain (acoustic) | 5–15 seconds |
| Typical sustain (electric solid) | 30–90 seconds |

## Appendix C: The Kuramoto Model — Quick Reference

The standard Kuramoto model:

$$\dot{\theta}_i = \omega_i + \frac{K}{N}\sum_{j=1}^{N}\sin(\theta_j - \theta_i)$$

- $\theta_i$: phase of oscillator $i$
- $\omega_i$: natural frequency of oscillator $i$
- $K$: global coupling strength
- $N$: number of oscillators
- $r = \left|\frac{1}{N}\sum e^{i\theta_j}\right| \in [0,1]$: order parameter

**Critical coupling:** $K_c = \frac{2}{\pi g(0)}$ where $g(\omega)$ is the frequency distribution.

For the string system: $K \propto 1/Z_b$, so decreasing bridge impedance is increasing Kuramoto coupling.

---

*The sympathetic string does not choose to resonate. The physics compels it. And the physics is constraint theory, wearing a different face.*
