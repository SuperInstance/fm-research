# The Evolution of MIDI — From Analogue Control Voltage to Digital Tensor

## An Archaeological Study in Control Surfaces, Quantization, and the Mathematics of Musical Expression

---

**Abstract.** This paper traces the 60-year evolution of electronic musical control from analogue voltage to digital tensor, arguing that the perceived conflict between "analogue warmth" and "digital precision" was never a fundamental property of the signal medium, but rather an artifact of the *control surface* — the interface between human intention and machine response. We examine the pre-MIDI era of control voltage (CV/gate), the engineering compromises of MIDI 1.0, the resurgence of analogue synthesis, and the mathematical convergence enabled by MIDI 2.0, MPE, OSC, and modern tensor-based constraint systems. Central to our analysis is the role of splining as the bridge between discrete message-passing and continuous physical response, and the emergence of what we term **Tensor-MIDI** — a representation in which musical control data is treated as a multi-dimensional tensor with continuous interpolation, exact fraction arithmetic, and soft-saturation dynamics. We connect each historical stage to the underlying mathematics of Banach spaces, lattice quantization, and piecewise-linear dynamical systems.

---

## 1. The Pre-MIDI Era: Voltage as Language (1960–1982)

### 1.1 The Moog Modular and the Tyranny of the Patch Cable

In 1964, Robert Moog introduced the first commercial voltage-controlled modular synthesizer. The concept was disarmingly simple: every musical parameter — pitch, timbre, amplitude, filter cutoff — was controlled by an electrical voltage. A one-volt-per-octave standard (1 V/oct) meant that increasing the control voltage by exactly 1.000 V raised the pitch by one musical octave. A gate signal (typically +5 V) triggered the envelope generator. An envelope produced a continuous voltage contour that shaped the sound over time.

This was **control voltage** (CV), and it had a beautiful property: it was **continuous**. A CV signal could take any value within its voltage range. There was no quantization, no discretization, no steps. If you slowly swept a filter cutoff, the cutoff frequency moved smoothly through every real number in its range. The resolution was limited only by the noise floor of the analogue circuitry — thermal noise, shot noise, power supply ripple — which, paradoxically, became part of the sonic character.

But CV/gate had a catastrophic limitation: **one cable per parameter**. A moderately complex patch on a large Moog system could require dozens of patch cables. Each voice in a polyphonic setup needed its own complete signal path. There was no concept of a "message" that could travel down a single wire and be interpreted by multiple destinations. If you wanted to control six voices polyphonically, you needed six sets of CV/gate inputs, six filters, six amplifiers.

### 1.2 The Proliferation of Incompatible Standards

By the late 1970s, the synthesizer market had fragmented into a tower of Babel. Each manufacturer used proprietary voltage standards:

- **Moog**: 1 V/oct for pitch, S-trig (short-to-ground) or V-trig (voltage) for gate, +5 V gate level.
- **Roland**: Some units used 1 V/oct, others used Hz/V (hertz per volt) for pitch, a logarithmic/exponential nightmare for interoperability.
- **Korg**: Hz/V pitch, incompatible with Moog without conversion boxes.
- **ARP**: 1 V/oct but different gate polarities and trigger sensitivities.
- **Oberheim**: Proprietary digital scanning keyboards that generated internal CV but exposed no standard interface.
- **Yamaha**: Early digital implementations (GX-1, CS-80) used internal digital-to-analogue conversion with proprietary protocols.

The Sequential Circuits Prophet-5 (1978) was a landmark because it was **microprocessor-controlled** — it used an Intel 8080 to scan the keyboard, assign voices, and generate internal CV via DACs. But even the Prophet-5 had no standard way to communicate with other manufacturers' equipment. The industry needed a lingua franca.

### 1.3 The Mathematical Nature of the Problem

From a mathematical perspective, the pre-MIDI era was characterized by **continuous scalar control** in a high-dimensional space. Each synthesizer voice existed in a parameter space $\mathcal{P} \subset \mathbb{R}^n$ where $n$ was large (pitch, cutoff, resonance, attack, decay, sustain, release, pulse width, etc.). The control surface was a manifold mapped by continuous functions $f: \mathbb{R} \to \mathcal{P}$.

The problem was not the mathematics of the control — continuous functions are well-behaved. The problem was the **physical instantiation**: each dimension required a dedicated wire. The topology of the studio was a dense graph $G = (V, E)$ where every module was a vertex and every patch cable an edge. The complexity scaled as $O(n^2)$ for fully connected patches.

What was needed was a **serialization** of the parameter vector — a way to send the coordinates of $\mathcal{P}$ through a single communication channel. But serialization implies time-division, and time-division implies **sampling**, and sampling implies **quantization**. The digital revolution would solve the connectivity problem at the cost of continuity.

---

## 2. The MIDI Revolution: Serializing Music (1983)

### 2.1 The Universal Language

In 1981, Dave Smith of Sequential Circuits and Ikutaro Kakehashi of Roland began discussing a universal interface. By November 1982, the specification was finalized. In January 1983, at the NAMM show, a Roland Jupiter-6 and a Sequential Circuits Prophet-600 were connected with a 5-pin DIN cable. When Smith played a note on the Prophet, the Jupiter sounded. MIDI — Musical Instrument Digital Interface — was born.

The MIDI 1.0 specification (1983) made several engineering decisions that would shape electronic music for four decades:

- **Physical layer**: 5-pin DIN connector (pins 4 and 5 used, pin 2 shield), current-loop opto-isolated receiver.
- **Electrical layer**: Asynchronous serial at **31.25 kbaud** (an odd rate chosen because it divided evenly into common UART clock frequencies: 1 MHz / 32 ≈ 31.25 kHz).
- **Data layer**: 8-bit bytes, but with the most significant bit (MSB) reserved as a status flag. This meant **7 bits of payload per byte**.
- **Channel layer**: 4 bits embedded in status bytes, giving **16 channels**.
- **Message types**: Note On, Note Off, Polyphonic Aftertouch, Channel Aftertouch, Control Change (CC), Program Change, Pitch Bend, System Exclusive (SysEx).

### 2.2 The 7-Bit Compromise

The most consequential decision was the use of 7-bit values for musical data. A Note On message has the form:

```
0x9n key velocity
```

where `key` (0–127) represents the MIDI note number, and `velocity` (0–127) represents how fast the key was struck. This gives **128 velocity levels**.

Why 7 bits? The UART sends 8-bit bytes, but MIDI needed a way to distinguish status bytes from data bytes. The solution: status bytes have the MSB set (1), data bytes have it cleared (0). This left 7 bits for data.

Musically, 128 velocity levels is just barely sufficient. The human ear can distinguish intensity differences of roughly 1 dB under ideal conditions. 128 steps over the dynamic range of a synthesizer (typically 60–80 dB) yields steps of about 0.5–0.6 dB — perceptible but acceptable for most purposes. However, for subtle expressive control, 128 steps create a **stepped response**.

Consider the mapping from velocity $v \in \{0, 1, \dots, 127\}$ to amplitude $A$:

$$A(v) = A_{\max} \left(\frac{v}{127}\right)^\gamma$$

where $\gamma \approx 2$ is a typical exponential mapping. The step size in amplitude between adjacent velocity values is:

$$\Delta A \approx \frac{dA}{dv} = A_{\max} \cdot \gamma \cdot \frac{v^{\gamma-1}}{127^\gamma}$$

At low velocities ($v \approx 1$), $\Delta A$ is tiny. At high velocities ($v \approx 127$), the step is largest. The quantization is **non-uniform in perception** — coarse where human sensitivity is highest.

### 2.3 Pitch Bend and the 14-Bit Workaround

MIDI designers recognized that pitch bend needed finer resolution. Their solution: two 7-bit data bytes, combined into a 14-bit value. The Pitch Bend message carries:

$$b = \text{lsb} + 128 \times \text{msb}$$

giving $2^{14} = 16{,}384$ possible values. With a default range of ±2 semitones, the pitch resolution is:

$$\frac{4 \text{ semitones}}{16384} \approx 0.000244 \text{ semitones} \approx 0.24 \text{ cents}$$

This is below the threshold of pitch discrimination (roughly 5–10 cents for pure tones, 1–2 cents for complex tones in musical context). The 14-bit workaround worked for pitch.

But it was a workaround, not a principled solution. Other parameters — modulation wheel, breath controller, expression pedal — remained stuck at 7 bits. Control Change (CC) messages use only 7 bits. The result: when you automate a filter cutoff with MIDI CC, you hear the steps.

### 2.4 The Cost of Serialization

MIDI solved the $O(n^2)$ cable problem by serializing musical events into a 1-dimensional byte stream. But this serialization introduced **three fundamental losses**:

1. **Temporal quantization**: Events are ordered but not timestamped within a byte stream. Timing jitter arises from serial transmission delays.
2. **Value quantization**: 7-bit or 14-bit discrete values replace continuous voltages.
3. **Dimensionality reduction**: A musical gesture (say, a chord with per-note pressure, pitch drift, and timbral variation) is flattened into a sequence of messages on 16 channels.

Mathematically, MIDI transforms a continuous trajectory in parameter space $\mathcal{P}$ into a **piecewise-constant function** in time. A continuous envelope $e(t) \in \mathbb{R}$ becomes a sequence of CC values $c_k$ held constant between updates:

$$e_{\text{MIDI}}(t) = c_k \quad \text{for} \quad t_k \leq t < t_{k+1}$$

This is a **zero-order hold** reconstruction. Its frequency response has sinc-shaped lobes, and the step transitions introduce high-frequency artifacts. The ear, sensitive to discontinuities, perceives this as "digital harshness" or "steppiness."

---

## 3. Why Analogue Stayed Popular: The Physics of Imperfection (1983–2025)

### 3.1 The Warmth Myth and the Reality of Saturation

Despite MIDI's convenience, musicians never abandoned analogue synthesizers. The reasons are deeper than nostalgia.

The "analogue warmth" that audio engineers describe has a specific physical basis: **soft saturation**. When an analogue circuit (a transistor, tube, or magnetic tape) is driven beyond its linear range, it does not clip instantly. Instead, the transfer function gradually compresses:

$$V_{\text{out}} = f(V_{\text{in}})$$

where $f$ is a smooth, monotonic function with diminishing slope as $|V_{\text{in}}| \to \infty$. A common model is the **tanh saturator**:

$$f(x) = \tanh(x) \approx x - \frac{x^3}{3} + \frac{2x^5}{15} - \cdots$$

The key property is that saturation adds **odd harmonics** in a smooth, level-dependent way. Soft clipping generates a spectrum that changes continuously with input amplitude. Small signals remain nearly unaffected; large signals are compressed. This is **dynamic range compression** that is signal-dependent and non-linear.

Digital systems, by contrast, with fixed-point INT8 or INT16 representation, implement **hard clipping**:

$$f_{\text{hard}}(x) = \begin{cases} -1 & x < -1 \\ x & -1 \leq x \leq 1 \\ 1 & x > 1 \end{cases}$$

Hard clipping generates a broad spectrum of odd and even harmonics instantly. The transition from linear to clipped is discontinuous. The ear perceives this as harshness.

But note: this is not a fundamental property of digital audio. Floating-point digital systems can implement tanh saturation perfectly. The issue was that early digital synthesizers and samplers used **hard-clipping DACs** and **no anti-aliasing** in their output stages. The "digital coldness" was an implementation choice, not a mathematical necessity.

### 3.2 Vinyl and the Physical Medium

The preference for vinyl records over digital CDs illustrates the same principle. A vinyl record is a physical object. The groove is a continuous mechanical deformation of a plastic substrate. When a stylus tracks the groove, the reproduction is continuous in time and amplitude (ignoring molecular grain structure, which is at the nanometer scale).

More importantly, the vinyl mastering and playback chain introduces:

- **Mechanical compression**: The stylus and groove have finite compliance. High-amplitude, high-frequency content physically cannot be cut at full amplitude without the cutter head bouncing out of the groove. The medium enforces soft limiting.
- **Thermal noise and surface noise**: Random variations that mask quantization and create a "noise floor" below which detail is obscured — but also above which everything sounds "alive."
- **Tracking distortion**: The stylus does not track the groove perfectly; there is microscopic misalignment that generates intermodulation distortion unique to each playback.

Digital audio, properly dithered and oversampled, is *mathematically* more accurate. But accuracy is not always desirable. The human auditory system evolved to interpret sounds with continuous variation. A completely deterministic, noise-free signal can sound sterile because it contains no micro-variations for the ear to latch onto as "natural."

### 3.3 The Four Pillars of Analogue Desirability

Why did musicians continue to pay premium prices for 1970s synthesizer designs? Four properties, all related to continuity:

**1. Continuous parameter control.** A knob on a Moog filter changes cutoff frequency as a continuous function of angle. There are no steps. If you record an automation sweep, the underlying physical voltage is continuous. In a digital synthesizer controlled by MIDI CC, the same sweep is a staircase with 128 steps.

**2. Natural saturation character.** As discussed, analogue circuits saturate softly. The harmonic content grows organically with amplitude.

**3. Thermal drift and organic variation.** Analogue components (resistors, capacitors, transistors) have temperature coefficients. A VCO drifts by cents per minute. Two voices in a polyphonic synth never sound exactly identical. This creates a **chorusing effect** and a sense of life. Mathematically, the parameter space $\mathcal{P}$ is not fixed; it undergoes a slow random walk:

$$\frac{d\theta}{dt} = \sigma W(t)$$

where $\theta$ is a parameter (e.g., pitch offset), $\sigma$ is the drift magnitude, and $W(t)$ is Wiener process noise.

**4. Circuit imperfections as fingerprint.** Manufacturing tolerances mean every analogue unit is unique. The filter in unit #1247 has a slightly different resonance peak than #1248. This uniqueness is prized.

### 3.4 The Digital Perfection Problem

Digital synthesis, especially in the DAW era, aimed for perfection. A software synthesizer produces exactly the same output every time. The parameter space is deterministic. There is no drift, no noise floor, no variation.

This "perfection" strips away the statistical texture that the human auditory system uses to verify that a sound source is physical. We are deeply attuned to detect whether a sound comes from a resonant physical object or a mathematical formula. A purely digital sound, without dither, without micro-variation, triggers a subtle "uncanny valley" response in trained listeners.

The industry responded with plugins: tape saturation, tube emulation, vinyl noise, analog circuit modeling. These are attempts to **re-inject continuity and stochasticity** into a discrete, deterministic framework. But they are retrofits. The fundamental architecture remains message-passing between discrete events.

---

## 4. MIDI 2.0 and the Convergence (2020–2026)

### 4.1 Higher Resolution, Bidirectional Communication

MIDI 2.0, finalized in 2020, addresses many of MIDI 1.0's limitations:

- **16-bit resolution** for velocity and most controllers ($2^{16} = 65{,}536$ levels).
- **Per-note controllers**: Each note in a chord can have independent pitch bend, timbre, and pressure.
- **Bidirectional communication**: Devices can query each other for capabilities.
- **Higher data rates**: Still over the same cables, but with more efficient encoding.
- **Property exchange**: Devices can share parameter metadata.

The jump from 7-bit to 16-bit is significant. The velocity step size drops from:

$$\Delta v_{7} = \frac{1}{128} \approx 0.78\%$$

to:

$$\Delta v_{16} = \frac{1}{65536} \approx 0.0015\%$$

At 16 bits, quantization noise in velocity is below the thermal noise floor of any analogue circuit. For practical purposes, it is continuous.

### 4.2 MPE: CV/Gate Reborn

MIDI Polyphonic Expression (MPE) is perhaps the most important development. Standard MIDI sends one Pitch Bend value per channel. MPE allocates one channel per note, allowing continuous per-note pitch bend, pressure, and timbre.

With MPE, playing a chord and bending individual notes creates a continuous multi-dimensional control surface. Each finger on a controller (like the ROLI Seaboard or Sensel Morph) generates a stream of per-note messages. The result is **functionally equivalent to polyphonic CV/gate**, but in a digital protocol.

The historical irony is profound: MIDI was created to escape the cable tyranny of CV, but 40 years later, musicians demanded CV-like expression and got it through a more sophisticated digital protocol. The circle closed.

### 4.3 OSC and the Network Paradigm

Open Sound Control (OSC), developed at CNMAT in the late 1990s, took a different approach. OSC messages are:

- **Arbitrary resolution**: Values are 32-bit or 64-bit floats.
- **Addressable via URLs**: `/synthesizer/voice3/filter/cutoff`.
- **Network-based**: Runs over UDP/IP, not serial cables.
- **Timestamped**: Messages carry explicit time tags.

OSC abandons the channel paradigm entirely. It is a flexible, high-resolution control protocol that treats musical control as a **continuous parameter vector in a namespace**. However, OSC never achieved universal hardware adoption because it requires more processing power and network infrastructure than simple UART serial.

### 4.4 The Convergence Thesis

By 2025, the technological distinctions had blurred:

- Digital synthesizers model analogue circuits with increasing fidelity (circuit simulation, component-level modeling).
- Analogue synthesizers include digital control (MIDI-to-CV converters, digital sequencers).
- Controllers provide continuous expression (MPE, polyphonic aftertouch, capacitive surfaces).
- DAWs run at 64-bit float with oversampling, eliminating the hard-clipping artifacts of early digital.

The convergence is not accidental. It reflects a mathematical truth: the Shannon-Nyquist theorem guarantees that a bandlimited continuous signal can be perfectly reconstructed from discrete samples. The problem was never digital vs. analogue. It was **insufficient sampling rate and insufficient bit depth in the control domain**.

---

## 5. Splining — The Bridge Between Discrete and Continuous

### 5.1 What Splining Does

A spline is a piecewise-defined function that interpolates smoothly between a set of discrete control points. Given a set of points $\{(t_i, y_i)\}_{i=0}^{n}$, a spline $S(t)$ satisfies:

1. $S(t_i) = y_i$ for all $i$ (interpolation).
2. $S(t)$ is continuous and smooth (typically $C^1$ or $C^2$) at the knots $t_i$.

The simplest spline is the **linear spline**:

$$S_i(t) = y_i + \frac{y_{i+1} - y_i}{t_{i+1} - t_i}(t - t_i) \quad \text{for} \quad t \in [t_i, t_{i+1}]$$

This is $C^0$ continuous — no jumps, but discontinuities in the first derivative (corners). For audio and control applications, we typically want **cubic splines**, which are $C^2$ continuous. A cubic spline on interval $[t_i, t_{i+1}]$ has the form:

$$S_i(t) = a_i + b_i(t-t_i) + c_i(t-t_i)^2 + d_i(t-t_i)^3$$

The coefficients are determined by requiring continuity of $S$, $S'$, and $S''$ at each knot, plus boundary conditions (natural, clamped, or periodic).

### 5.2 Splining as a Tensor Operation

This is where splining connects deeply to our mathematical framework. A spline is not merely a curve-fitting technique; it is a **linear operator in a function space**.

Consider the B-spline basis. Given a knot vector $\mathbf{t} = (t_0, t_1, \dots, t_{n+k})$, the B-spline basis functions $N_{i,k}(t)$ of degree $k-1$ are defined recursively (Cox-de Boor):

$$N_{i,1}(t) = \begin{cases} 1 & t_i \leq t < t_{i+1} \\ 0 & \text{otherwise} \end{cases}$$

$$N_{i,k}(t) = \frac{t - t_i}{t_{i+k-1} - t_i} N_{i,k-1}(t) + \frac{t_{i+k} - t}{t_{i+k} - t_{i+1}} N_{i+1,k-1}(t)$$

A spline curve is then:

$$S(t) = \sum_{i=0}^{n} N_{i,k}(t) \cdot P_i$$

where $P_i$ are the control points. This is a **linear combination of basis functions weighted by coefficients**. In other words, it is a **tensor contraction**:

$$S = \mathbf{N} \cdot \mathbf{P}$$

where $\mathbf{N}$ is the vector of basis functions evaluated at $t$, and $\mathbf{P}$ is the vector of control points. The spline exists in the **span** of the B-spline basis functions, which form a finite-dimensional subspace of the Banach space $C^2([a,b])$.

For surfaces, we use **tensor product splines**:

$$S(u,v) = \sum_{i=0}^{n} \sum_{j=0}^{m} N_{i,k}(u) \cdot M_{j,l}(v) \cdot P_{i,j}$$

This is a **2D tensor operation**: the basis is the outer product of two 1D bases, and the control points form a matrix (a 2D tensor). NURBS (Non-Uniform Rational B-Splines) extend this by introducing rational weights, enabling exact representation of conic sections.

### 5.3 Splining the MIDI Quantization Problem

Splining directly addresses every quantization artifact of MIDI:

**Velocity stepping.** A MIDI 1.0 velocity value $v \in \{0, \dots, 127\}$ is a sample of an underlying continuous expression gesture. If we treat a sequence of note-on events as control points $(t_i, v_i)$, we can construct a spline through them. The resulting envelope $S(t)$ is continuous and smooth. When this envelope modulates amplitude, there are no perceptible steps — only a continuous dynamic contour.

**CC automation stepping.** A DAW automation lane with MIDI CC data is a piecewise-constant function. Converting it to a cubic spline interpolant produces a $C^2$ continuous control signal. The derivative $S'(t)$ is continuous, meaning the *rate of change* of the parameter never jumps. Since human perception is sensitive to changes in rate (acceleration), this eliminates the "mechanical" feel of stepped automation.

**Pitch bend microtonality.** Even with 14-bit pitch bend, continuous pitch gestures (like a violin portamento) are sampled. Spline interpolation between pitch bend values reconstructs a smooth pitch trajectory. For microtonal music, where intervals smaller than a semitone are structural, splining is essential.

### 5.4 Splining in Audio Signal Processing

The connection between splining and audio runs deeper than control data.

**Anti-aliasing and sinc interpolation.** The Whittaker-Shannon interpolation formula reconstructs a bandlimited signal from samples:

$$x(t) = \sum_{n=-\infty}^{\infty} x[n] \cdot \operatorname{sinc}\left(\frac{t - nT}{T}\right)$$

where $\operatorname{sinc}(x) = \frac{\sin(\pi x)}{\pi x}$. The sinc function is the **ideal interpolating kernel** — it is the limit of a B-spline as degree $\to \infty$. In practice, we use finite-degree splines (cubic, quintic) as approximations to sinc. Sample rate conversion, implemented via polyphase filters, is essentially spline interpolation with optimized kernels.

**Wavetable synthesis.** In wavetable synthesis, a sound is represented by a sequence of single-cycle waveforms. As the tone evolves, the oscillator crossfades between waveforms. A naive crossfade is linear interpolation — a degree-1 spline. Higher-quality implementations use cubic spline interpolation between wavetable frames, producing smoother spectral evolution.

### 5.5 Splining in Constraint Theory

Our constraint-theoretic framework makes explicit use of splining at multiple levels:

**The deadband funnel as a piecewise-linear spline.** In our phase-space control system, the deadband defines a region around a nominal trajectory within which no control action is taken. The boundary of the deadband is a piecewise-linear spline through phase space. Inside the deadband, the system is uncontrolled (free evolution); outside, a restoring force applies. The transition at the boundary is $C^0$ continuous (position matches) but $C^1$ discontinuous (force appears). This is mathematically a **linear spline with a switching condition**.

**Eisenstein snap as nearest-point on a lattice spline.** When we quantize a continuous state vector to an Eisenstein lattice (hexagonal packing in 2D), we are finding the nearest lattice point. The Voronoi cells of the lattice partition the plane into regions. The boundaries between cells are piecewise-linear. The "snap" operation — projecting a continuous point to its nearest lattice point — is a **piecewise-constant mapping** with discontinuities at the cell boundaries. If we instead project onto a *smoothed* lattice (convolving the lattice with a Gaussian), we obtain a $C^\infty$ approximation. This is lattice splining.

**FLUX vectors as spline control points.** In our FLUX representation, state vectors at discrete constraint checkpoints serve as control points for an interpolating spline that generates continuous trajectories between checkpoints. The FLUX vector $\phi_i$ at checkpoint $i$ determines not just the position but the derivative (via momentum components), enabling Hermite interpolation — a spline where both position and tangent are specified at each knot. This is a $C^1$ spline with explicit derivative control.

---

## 6. Tensor-MIDI: Resolving the Analogue/Digital Split

### 6.1 The 40-Year Tension

For four decades, the music technology community has debated analogue vs. digital. The debate was framed as:

- Analogue = warm, continuous, imperfect, alive.
- Digital = cold, discrete, precise, sterile.

We argue that this framing is a category error. The warmth of analogue comes from specific physical properties (soft saturation, thermal noise, drift) that are **perfectly reproducible in digital systems**. The coldness of early digital came from specific engineering compromises (7-bit quantization, hard clipping, no dither) that are **not intrinsic to digital representation**.

The real distinction was always about the **control surface** — the mapping from human action to machine state.

### 6.2 Tensor-MIDI: A Principled Synthesis

We propose **Tensor-MIDI** not as a competing protocol, but as a conceptual framework that resolves the historical tension. Tensor-MIDI treats musical control data as a multi-dimensional tensor with the following properties:

**INT8 saturation = analogue warmth.** Instead of hard-clipping digital values, we apply a soft-saturation function modeled after analogue circuits:

$$\text{sat}(x) = \tanh(x / \alpha) \cdot \alpha$$

where $\alpha$ is a scaling parameter. This maps the real line to $[-\alpha, \alpha]$ with smooth transition. In fixed-point INT8 arithmetic, we implement this via lookup tables or piecewise polynomial approximations. The result: the digital signal acquires the harmonic characteristics of analogue saturation without leaving the digital domain.

**Deadband = analogue noise gate.** In CV systems, voltages below the noise floor have no effect. We formalize this as a deadband function:

$$\text{db}(x) = \begin{cases} x - \delta & x > \delta \\ 0 & |x| \leq \delta \\ x + \delta & x < -\delta \end{cases}$$

Only changes larger than $\delta$ propagate. This mimics the threshold behavior of analogue circuits and reduces message traffic (only transmit what matters). The deadband boundary is a piecewise-linear spline in the input-output plane.

**Fraction arithmetic = Pythagorean tuning.** Analogue VCOs drift in pitch. Digital oscillators are exact. But exact to what? Standard digital synthesis uses equal-tempered tuning (12-tone equal temperament, 12-TET), which is a compromise. Our framework uses exact fraction arithmetic for frequency ratios:

$$f = f_0 \cdot \frac{p}{q}$$

where $p, q \in \mathbb{Z}$ are small integers. This yields just intonation and Pythagorean tuning exactly, with no rounding error. The digital system is not just precise — it is **more precise than analogue** for musical intervals, because it avoids the thermal drift that causes analogue beat frequencies to wander.

**Splining = continuous expression from discrete events.** MIDI events are discrete. Human expression is continuous. Splining is the bridge. A Tensor-MIDI control stream is a sequence of events that define knots in a multi-dimensional spline. The audio engine renders the spline, not the raw events. The control surface, from the musician's perspective, is continuous because the reconstruction is $C^2$.

**Tensor representation = all dimensions simultaneously.** MIDI flattens musical control into a 1D byte stream. Tensor-MIDI represents the musical state at time $t$ as a tensor $\mathcal{M}(t) \in \mathbb{R}^{N \times D}$ where $N$ is the number of voices and $D$ is the number of parameters per voice (pitch, velocity, pressure, timbre, pan, etc.). This tensor is not serialized; it is processed in parallel by the synthesis engine. The tensor can be interpolated via multi-dimensional splines, filtered via tensor convolutions, and constrained via tensor norms.

### 6.3 The Mathematical Core

The unifying mathematical observation is this:

> The analogue/digital divide was never about continuous vs. discrete signals. It was about whether the control-to-sound mapping was a smooth function or a discontinuous one.

An analogue synthesizer maps continuous control voltages to continuous sound parameters through smooth (though non-linear) transfer functions. Early digital synthesizers mapped discrete messages to sound parameters through zero-order holds — discontinuous mappings.

Tensor-MIDI makes the mapping smooth by construction. The discrete events are **control points** for a smooth interpolant. The synthesis engine operates on the interpolant, not the raw data. Mathematically:

$$\text{Sound}(t) = \text{Synth}\left(\text{Spline}\left(\{\mathcal{M}(t_i)\}_{i=0}^{n}\right)(t)\right)$$

The Spline operator is a linear (or piecewise-linear) projection from the space of discrete sequences $\ell^2$ to the space of continuous functions $L^2$. The Synth operator is a non-linear mapping from control space to audio waveforms. The composition is smooth in the control points, meaning small changes in expression produce small changes in sound — the defining property of "playability."

### 6.4 The Control Surface is Everything

Consider two scenarios:

1. A musician plays a MIDI keyboard with 7-bit velocity into a digital sampler with no interpolation. The control surface is discrete. The sound jumps between 128 amplitude levels. It feels digital.

2. The same musician plays the same keyboard, but the MIDI stream is splined into continuous envelopes with 64-bit precision, driving a physical-modeling synthesizer with soft-saturation output stages. The control surface is continuous. It feels analogue.

The hardware is identical. The protocol is identical. The difference is the **mathematical reconstruction** between message and sound.

This is the central thesis of our archaeological investigation: the 40-year war between analogue and digital was a war over **representation and reconstruction**, not over medium. CV/gate was continuous because the wire carried the signal directly. MIDI was discrete because the wire carried messages. Tensor-MIDI is continuous because the messages are treated as samples of an underlying tensor field, reconstructed via splining, saturated softly, and expressed through exact fraction arithmetic.

### 6.5 Towards a Unified Theory of Musical Control

We can now place all historical systems on a unified mathematical spectrum:

| Era | Representation | Reconstruction | Space | Key Property |
|-----|---------------|----------------|-------|--------------|
| Pre-MIDI (CV) | Continuous voltage | Direct (wire) | $\mathbb{R}$ | $C^\infty$, but $O(n)$ cables |
| MIDI 1.0 | 7-bit messages | Zero-order hold | $\mathbb{Z}_{128}$ | Discrete, compact, universal |
| MIDI 2.0 | 16-bit messages | Zero-order hold | $\mathbb{Z}_{65536}$ | Fine-grained, still discrete |
| MPE | Per-note messages | Zero-order hold per channel | $\mathbb{Z}_{65536}^{N}$ | Polyphonic expression |
| OSC | 32-bit float messages | Application-defined | $\mathbb{F}_{32}^{N}$ | Flexible, network-native |
| Tensor-MIDI | Tensor control points | Spline interpolation | $\text{Spline}(\mathbb{R}^{N \times D})$ | Continuous by construction |

The progression is clear: from continuous-but-unwieldy, to discrete-and-portable, to discrete-but-high-resolution, to continuous-again via mathematical reconstruction.

---

## 7. Conclusion: The Archaeology Ends, the Mathematics Begins

The history of MIDI is not merely a history of connectors and baud rates. It is a case study in the fundamental mathematical tension between **discrete messaging** and **continuous physical systems**.

Control voltage was continuous but unscalable. MIDI was scalable but quantized. MIDI 2.0 and MPE increased resolution but retained the message-passing paradigm. OSC liberated the data format but did not specify reconstruction. Only when we place the entire control structure in a tensor framework, with splining as the reconstruction operator, do we recover the continuity of CV while retaining the universality of MIDI.

The implications extend beyond music. Any system that maps human expression to machine action — robotics, haptics, virtual reality, prosthetics — faces the same choices. Discrete commands are efficient to transmit. Continuous response is necessary for natural interaction. The solution is not to choose one or the other, but to **represent discretely and reconstruct continuously**.

The spline is the bridge. The tensor is the vessel. And the music, as always, is in the continuous space between the notes.

---

**References and Further Reading**

- Smith, D. & Kakehashi, I. (1983). *MIDI 1.0 Specification*. MIDI Manufacturers Association.
- MIDI Association (2020). *MIDI 2.0 Specification*.
- de Boor, C. (2001). *A Practical Guide to Splines*. Springer.
- Roads, C. (1996). *The Computer Music Tutorial*. MIT Press.
- Pirkle, W. (2019). *Designing Software Synthesizer Plugins in C++*. Focal Press.
- Moore, F. R. (1990). *Elements of Computer Music*. Prentice Hall.
- Loy, G. (2006). *Musimathics, Volumes 1 & 2*. MIT Press.

---

*Document version: 1.0*  
*Classification: Research / Archaeological*  
*Word count: approximately 3,400*
