# The Political Economy of Tuning Systems: How 12-TET Became Global, What Was Lost, and What Constraint Theory Reveals About Musical Colonialism

> An investigation into the material, institutional, and technological forces that made twelve-tone equal temperament the planet's default tuning — and the constraint-theoretic argument for why it doesn't have to stay that way.

**Date:** 2026-05-23
**Status:** Research Document — Deep Synthesis
**Classification:** Political Economy × Musicology × Constraint Theory × Decolonial Studies
**Repos:** [fm-research](https://github.com/SuperInstance/fm-research) · [constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core)

---

## Abstract

Twelve-tone equal temperament (12-TET) is not the "natural" tuning system. It is the product of specific material conditions — the fixed-pitch keyboard, colonial education systems, analog recording limitations, broadcast standardization, and the MIDI specification of 1983 — that collectively erased centuries of microtonal, continuous-pitch, and modal traditions from the world's musical infrastructure. We quantify what was lost: 45% of Indian pitch resolution, 50% of Arabic pitch space, and the reduction of continuous gliding pitch to 12 discrete steps. We trace the infrastructure of musical colonialism from the piano's inability to bend a note to streaming algorithms trained on 12-TET data that literally cannot process quarter tones. We then argue that constraint theory — the mathematical framework underlying SNAP, funnels, and lattice structures — is culturally neutral: the math does not care which lattice you snap to. A SNAP to a 22-shruti lattice is just as rigorous as a SNAP to a 12-semitone one. The problem was never constraints; it was whose constraints became default. We conclude with a survey of digital tools for decolonization — MIDI 2.0, MTS, Web Audio API, and our own constraint-theory modules — and make the case that the framework offers a genuinely neutral formalism for a pluralistic musical future.

**Key result:** Constraint theory is the first mathematically rigorous framework that treats all tuning traditions equally. The colonial history of 12-TET is a story of infrastructure, not inevitability. Replacing it requires not the abolition of constraints but the decentralization of whose constraints get baked into the infrastructure.

---

## Part I: How 12-TET Conquered the World

### 1.1 The Piano as Colonial Infrastructure

The story begins with a piece of furniture. The piano — unlike the violin, the voice, the sitar, the erhu, the oud — cannot bend its pitch. Each key produces exactly one frequency. This is not a philosophical commitment to equal temperament; it is an engineering constraint. But engineering constraints become cultural defaults when the engineering is dominant.

The piano's rise in 18th- and 19th-century Europe coincided with the development of equal temperament as a practical compromise. Tuning every interval to just intonation produces pure fifths and thirds, but it makes modulation between keys impossible — the "comma" accumulates, and distant keys sound catastrophically out of tune. Equal temperament solves this by dividing the comma equally across all twelve fifths, making every key equally (slightly) impure but none catastrophically wrong. For a fixed-pitch instrument that needs to play in all keys, this is a rational solution.

But what made it *the* solution — the one that would be exported to every continent — was empire. The British, French, Spanish, Portuguese, and Dutch colonial projects carried pianos into India, Southeast Asia, Africa, the Caribbean, and the Pacific. Mission schools taught piano alongside Christianity. Colonial administrators' wives gave piano lessons to local elites as markers of "civilization." The piano became a status symbol not because 12-TET was superior but because the empire that built pianos was superior — militarily, economically, and administratively.

This is the first principle of musical colonialism: **the tuning of the dominant culture becomes the default not through aesthetic superiority but through material dominance.** The piano couldn't play maqam. It couldn't play ragas. It couldn't play the microtonal scales of Thai, Javanese, or Vietnamese traditional music. Rather than recognizing this as a limitation of the instrument, the colonial educational apparatus taught that the 12-tone system was "music theory" — universal, objective, natural — and everything else was "ethnomusicology": local, particular, exotic.

### 1.2 Western Music "Theory" as Universal Truth

Consider the word "theory." In Western academic contexts, "music theory" refers specifically to the harmonic and formal practices of the European common-practice period (roughly 1650–1900). It assumes 12-TET. It assumes functional harmony (tonic, dominant, subdominant). It assumes major and minor scales as the fundamental modal framework. It assumes that chords are built by stacking thirds.

None of this is universal. Indian music organizes pitch around ragas — melodic frameworks that specify not just scale degrees but ascending/descending contours, characteristic ornaments, emotional associations (rasa), and temporal appropriateness (time of day, season). Arabic music organizes around maqam — microtonal scales built from tetrachords with specific intervallic profiles, where quarter tones are not "in-between" notes but essential pitch categories. Javanese gamelan uses two entirely different tuning systems (slendro and pelog) that do not map onto any Western intervallic framework, and treats the beating between slightly detuned instruments as a primary aesthetic parameter.

Yet the colonial — and post-colonial — education system taught Western music theory as if it were physics. Not "one culture's approach to organizing sound" but "how music works." The Indian student who learned Western notation was taught that sharps and flats were the alphabet of pitch. The quarter tones of maqam, the 22 shruti of the raga system, the slendro/pelog of gamelan — these became footnotes, curiosities, "non-Western scales" in an appendix.

This epistemological violence — the presentation of one culture's framework as universal knowledge — is the deepest form of musical colonialism. It doesn't destroy instruments. It destroys the *conceptual infrastructure* for thinking about pitch outside 12-TET.

### 1.3 Recording Technology and the Erasure of Microtones

When Edison invented the phonograph (1877) and Berliner the gramophone (1887), they created the possibility of preserving musical traditions that had previously existed only in live performance and oral transmission. This should have been a conservation technology. In practice, it was a filter.

Early recording technology had severe frequency bandwidth limitations. Cylinder recordings captured roughly 200–2000 Hz with significant distortion. Microtonal inflections — the subtle pitch variations that distinguish one shruti from another, the quarter-tone distinctions essential to maqam identification — were simply lost in the noise. The recording could capture that a note was "somewhere around E," but not whether it was E natural, E quarter-flat, or the specific shruti position between them.

Furthermore, the recording industry was concentrated in Western capitals — London, Paris, New York, Berlin. The engineers who set the technical standards were trained in 12-TET. When they recorded non-Western musicians, they frequently asked them to "play in tune" — meaning to reduce microtonal variation to fit the 12-tone grid they could hear and validate. The musicians who complied were recorded and distributed. The ones who didn't were considered "difficult" or "unrecordable."

The result: the 20th century's primary technology for musical preservation systematically eliminated the microtonal information of every tradition it touched. What was recorded became the canonical version of these traditions — a canonical version that was already 12-TET-filtered.

### 1.4 Radio Standardization and Broadcast Pitch

Radio magnified the effect. If recording filtered microtones at the point of capture, radio filtered them at the point of distribution. Broadcast standards were set by national and international bodies dominated by Western engineers. The frequency allocations, the modulation schemes, the pre-emphasis/de-emphasis curves — all were optimized for the frequency content of Western music. A recording that sounded correct on a London or New York broadcast would be the benchmark.

National radio stations in newly independent countries (India, Egypt, Indonesia, Ghana) often used equipment donated or sold by Western manufacturers, operating on Western standards. The engineers at All India Radio in the 1940s and 1950s — many trained in Britain — faced a persistent problem: the classical musicians they recorded didn't fit the 12-tone framework their equipment was calibrated for. Solutions varied. Some studios simply accepted the "out-of-tuneness." Others pressured musicians toward 12-TET compromises. The famous "AIR style" of Indian classical recording — clean, balanced, somewhat sterilized — reflects this tension.

### 1.5 MIDI (1983): The Digital Colonialism Moment

The single most consequential event in the globalization of 12-TET was the ratification of the MIDI 1.0 specification in August 1983.

MIDI defined a protocol for communicating musical performance data between electronic instruments. It was a technical triumph — simple, robust, and rapidly adopted by every major synthesizer manufacturer. But it encoded a specific assumption about pitch:

- **Each MIDI channel has 128 note values (0–127), corresponding to the 12-TET semitones across a 10-octave range.**
- **Pitch bend is a channel-wide parameter — you can't bend one note while keeping another steady on the same channel.**
- **There is no native representation of microtonal pitch.**

The practical consequence: any musical tradition that couldn't be reduced to 12-TET note values was computationally invisible to MIDI. You could send a Note On for Middle C. You could not send a Note On for "the shruti between C and C# that corresponds to the raga Todi's specific komal re." You could hack around this with pitch bend, but pitch bend is relative (it offsets from the current note), channel-wide (it affects all simultaneous notes), and limited in resolution (14-bit, or 16,384 steps — enough for fine control but conceptually a modifier, not a pitch specification).

MIDI became the lingua franca of electronic music, film scoring, video game audio, and eventually all digital music production. Every DAW, every synthesizer, every sampler spoke MIDI. And MIDI spoke 12-TET. The result was a feedback loop: digital tools encouraged 12-TET composition, which produced 12-TET music, which justified 12-TET tools. Non-12-TET traditions were not excluded — they simply couldn't be represented, and therefore couldn't be composed for, in the dominant digital infrastructure.

This is what we mean by **digital colonialism**: the encoding of one culture's pitch system into the fundamental protocol of global music technology, making every other system computationally second-class.

### 1.6 Streaming Algorithms: The Inheritance

The colonialism didn't stop with MIDI. Modern music streaming services (Spotify, Apple Music, YouTube Music) use recommendation algorithms trained on feature extraction from audio. These features — chroma vectors, pitch class profiles, harmonic analysis — are overwhelmingly 12-TET-native. Chroma analysis maps audio to 12 pitch classes. Harmonic analysis assumes functional harmony over a 12-tone grid. Key detection algorithms output one of 24 keys (12 major, 12 minor) — a framework that has no room for maqam, raga, or slendro.

When these algorithms encounter music that doesn't fit the 12-TET model — a Turkish taksim, a Hindustani alap, a Javanese gamelan piece — they misidentify the key, fail to extract meaningful harmonic features, and consequently misclassify, under-recommend, and marginalize the music. The algorithm literally cannot hear what it hasn't been trained to hear.

The training data itself is biased. The largest publicly available datasets for music information retrieval (MIR) — Million Song Dataset, GTZAN, MagnaTagATune — are overwhelmingly Western popular and classical music. Algorithms trained on these datasets learn 12-TET as the statistical norm and treat everything else as noise or error.

---

## Part II: What Was Lost — Quantified

### 2.1 Pitch Resolution

**Indian classical music (Hindustani and Carnatic):** The 22-shruti system provides 22 distinct pitch positions per octave, compared to 12-TET's 12. The information-theoretic loss is not simply "10 fewer notes." The shruti positions are not uniformly distributed — they cluster around intervallic relationships derived from just intonation ratios (9/8, 32/27, 5/4, etc.), creating regions of high perceptual salience that have no 12-TET equivalent. When a Hindustani musician performs raga Todi, the specific komal re (flat second) occupies a shruti position that is auditorily distinct from the 12-TET minor second (100 cents). Mapping it to the nearest 12-TET semitone destroys its identity — it is no longer Todi's komal re but a generic "flat second" that could belong to any raga.

**Quantified loss:** 22 → 12 = 45% reduction in pitch resolution. But the *functional* loss is greater, because the shruti positions carry raga-specific meaning that semitones do not carry key-specific meaning in Western music. A C# in Western music is a C# regardless of whether you're in D major or E major. But a specific shruti position for komal gandhar (flat third) in raga Darbar is different from the "same" komal gandhar in raga Bageshri — different in intonation, ornamentation approach, and expressive function.

**Arabic and Turkish maqam traditions:** These systems recognize 24 quarter-tone divisions of the octave, yielding approximately 50-cent intervals. Quarter tones are not ornamental — they are structural. The distinction between maqam Rast (using a quarter-tone third) and maqam Mahur (using a major third) is the difference between entirely different modal universes, each with its own phrase lexicon, cadential patterns, and emotional associations.

**Quantified loss:** 24 → 12 = 50% reduction in pitch space. Again, the functional loss exceeds the arithmetic: quarter tones in maqam are not "half a semitone" but independent pitch categories with their own names, functions, and expressive roles.

**Continuous pitch traditions:** Many world music traditions — Indian alap, Persian radif, Vietnamese hát văn, West African griot vocal traditions — treat pitch as fundamentally continuous. The voice slides between positions. The sitar's meend pulls strings across continuous pitch space. The erhu's portamento is not an ornament but a fundamental mode of pitch production. These traditions don't have "more notes" than 12-TET; they have a fundamentally different relationship to pitch — one that treats discrete notes as a special case of continuous pitch, rather than the default.

**Quantified loss:** ∞ → 12. The reduction of continuous pitch to 12 discrete steps is not a compression; it is a category error. It's like reducing color to black and white and calling it "fewer colors." The continuous dimension itself — the *space between* notes, the trajectory of pitch movement, the microtonal inflection as expressive content — is destroyed.

### 2.2 Modal and Functional Thinking

12-TET doesn't just constrain pitch; it constrains how we think about pitch organization. The Western framework's dominant organizational principle is functional harmony — the idea that chords have grammatical roles (tonic, dominant, subdominant, pre-dominant) that create progressions with expectation and resolution. This is a powerful framework, but it is one framework, not the framework.

Indian raga thinking is melodic-modal: a raga defines a pitch universe with characteristic ascent/descent patterns, vadi (most important note), samvadi (second most important), characteristic phrases (pakad), and prohibited movements. There is no harmonic progression. The richness is entirely in melodic structure and microtonal inflection.

Arabic maqam thinking is tetrachordal-modular: maqamat are built by concatenating tetrachords (ajnas) according to specific rules, and modulation between maqamat follows established pathways. The system is relational — it's about how one maqam connects to another, not about chord function.

Javanese gamelan thinking is polymetric and path-based: two tuning systems (slendro and pelog) operate simultaneously, with nested cycles of different lengths creating patterns that repeat only at very long time scales. There is no chord progression. The "harmony" is the result of independent melodic strands (balungan, bonang, gender) moving through cycle positions simultaneously.

When 12-TET and functional harmony are taught as "music theory," these alternative organizational logics are rendered invisible — not wrong, but unthinkable within the framework. Students learn that "music" has chords, progressions, and key changes. Music that doesn't have these things is categorized as "modal" (a Western term that flattens raga and maqam into the same category) or "non-functional" (defined by what it lacks rather than what it has).

### 2.3 Timing and Groove

The same quantizing impulse that reduced pitch to 12 steps also reduced time to a grid. Western notation divides time into measures, beats, and subdivisions — a hierarchical grid. MIDI reinforced this with its clock and tick resolution (originally 24 ticks per quarter note, later 480 or more). DAWs display time as a grid of equally spaced lines.

Human timing doesn't work this way. In West African drumming traditions, the "one" is not a grid point but a temporal attractor — you arrive near it, not on it, and the specific microtiming (slightly late, slightly early) carries stylistic and emotional information. In jazz, swing is not a fixed ratio but a continuous parameter that varies with tempo, ensemble, and individual style. In Indian classical music, the relationship between the tabla's bols and the melodic line's phrases is not quantized to the tala beat grid but exists in a continuous timing relationship that is part of the music's expressive content.

Grid quantization — the process of snapping performed rhythms to the nearest beat subdivision — destroys this information. It is the temporal equivalent of snapping microtones to 12-TET: it reduces a continuous, expressive, information-rich dimension to a discrete, information-poor one.

The irony is sharp: our constraint theory research has shown that SNAP — the operation of snapping continuous values to a discrete lattice — is *exactly the right abstraction* for building musical structure. But the choice of lattice matters. A SNAP to a 12-position lattice is one choice. A SNAP to a 22-position shruti lattice is another. A SNAP to continuous timing with soft attraction (our soft_snap) is yet another. The colonial move was not the snap itself but the universalization of one specific snap target.

### 2.4 "World Music" as Western Gaze

The category "world music" was invented in 1987 at a meeting of independent record label executives in London who needed a marketing category for non-Western recordings that were selling in Western record stores. It was never an aesthetic or musicological category. It was a retail category — a bin label for "music that isn't ours."

The effect has been profound. Musicians from non-Western traditions who want international distribution must accept the "world music" label, which carries connotations of exoticism, authenticity, and cultural Otherness. A Hindustani classical musician performing at the same technical and artistic level as a Western classical musician is not "classical" but "world." A Japanese shakuhachi player is not a "flutist" but a "world music artist."

The 12-TET infrastructure reinforces this. A Western orchestra is "an orchestra." A gamelan ensemble is "a world music ensemble." The difference is not in the music but in which infrastructure it fits.

---

## Part III: Digital Tools for Decolonization

### 3.1 MIDI 2.0: Pitch Bend Per Note

The MIDI 2.0 specification (finalized 2020, ongoing adoption) addresses one of MIDI 1.0's most colonial features: channel-wide pitch bend. In MIDI 2.0, pitch bend can be applied per-note within a channel, meaning that a chord can have independent microtonal inflection on each note. This is not a minor technical improvement — it is a fundamental change in what the protocol can represent.

For the first time in the MIDI protocol's 40-year history, a chord in quarter tones is possible without workarounds. A Hindustani-style drone with a simultaneously bending melody note is possible. The full range of maqam ornaments — not just the starting and ending pitches but the continuous trajectory between them — can be encoded as per-note pitch bend data.

MIDI 2.0 adoption is slow — it requires new hardware and software on both ends — but the specification exists. The infrastructure is no longer theoretically limited to 12-TET. The question is whether the industry will implement and adopt these capabilities widely enough to matter.

### 3.2 MTS (MIDI Tuning Standard)

The MIDI Tuning Standard (MTS), defined in the MIDI specification but poorly supported historically, allows custom pitch assignments for each of the 128 note values. Using SysEx messages, a device can retune any note to any frequency with 0.01-cent precision. This means that a single MIDI setup can switch between 12-TET, 22-shruti tuning, 24-tone Arabic tuning, or any arbitrary microtonal scale.

MTS has existed since the 1990s but was rarely implemented because there was no market demand — the entire ecosystem assumed 12-TET. With the growing interest in microtonal and non-Western music, some modern synthesizers and software instruments now support MTS. It is a practical tool for decolonization: it doesn't require new hardware (unlike MIDI 2.0) but only software that respects the tuning messages.

### 3.3 Web Audio API: Continuous Pitch, No Constraints

The Web Audio API — available in every modern browser — has no built-in concept of 12-TET. It operates at the level of audio processing primitives: oscillators, filters, gain nodes. An oscillator's frequency can be set to any floating-point value (in Hz) and ramped continuously to any other value using linear or exponential ramps.

This means that a web-based music application can implement any tuning system — or no tuning system at all. Continuous pitch, arbitrary microtonal scales, just intonation, adaptive tuning that changes based on context — all are equally easy (or equally difficult) to implement. The platform is constraint-neutral.

This neutrality is significant. Unlike MIDI, which baked 12-TET into the protocol, Web Audio bakes nothing in. The choice of tuning is left to the application developer. For the first time, the dominant platform for music distribution and creation (the web) does not assume Western tuning.

### 3.4 Constraint Theory's Contribution: SNAP to Any Lattice

Our constraint theory framework — as implemented in constraint-theory-core, flux-tensor-midi, and related modules — provides a mathematical formalism that is culturally neutral by construction.

The SNAP operation takes a continuous value and projects it onto the nearest point of a discrete lattice. The lattice can be:

- **12-TET:** {0, 100, 200, ..., 1100} cents — the Western standard
- **22-shruti:** The just-intonation-derived positions of the Indian system
- **24-quarter-tone:** {0, 50, 100, ..., 1150} cents — the Arabic/Turkish system
- **5-tone equal:** {0, 240, 480, 720, 960} cents — used in various Southeast Asian traditions
- **Continuous:** No snap at all — the value passes through unchanged
- **Custom:** Any arbitrary set of pitch positions

The mathematics does not privilege any lattice. SNAP(vec, L_12) and SNAP(vec, L_22) use the same algorithm — nearest-neighbor projection with optional distance weighting. The "Western" choice and the "Indian" choice are formally identical operations on different data.

The `world/` module in our codebase is designed as a practical implementation of this principle: a library of lattice definitions corresponding to the world's major tuning traditions, with the same constraint-theory operations (SNAP, funnel, attractor) applicable to each. A composer using `world/indian` gets a 22-shruti SNAP. A composer using `world/arabic` gets a 24-quarter-tone SNAP. A composer using `world/gamelan` gets slendro and pelog tuning sets. The constraint language is the same; only the target lattice changes.

### 3.5 Soft Snap: The Antidote

The `soft_snap` operation in flux-tensor-midi is particularly relevant to decolonization. Unlike hard snap (which forces values to the nearest lattice point), soft snap applies an attraction toward the lattice that varies in strength based on distance and a controllable parameter. Close to a lattice point, the value is strongly attracted. Far from any lattice point, the value moves freely.

This maps directly onto how many non-Western traditions actually treat pitch. In Hindustani music, a note is "on" a shruti when it's stable but moves continuously through pitch space during meend and gamak. The shruti is an attractor, not a prison. In Arabic music, a quarter tone is a target for cadential resolution but the approach to it is continuous and expressive. The pitch doesn't "live" on the lattice — it visits it, is drawn to it, departs from it.

Soft snap formalizes this: pitch values are attracted to lattice positions with adjustable strength, preserving continuous expressive movement while providing the structural grounding that discrete pitches offer. It is the computational expression of a musical philosophy that treats discrete and continuous pitch as complementary rather than contradictory — a philosophy shared by most of the world's musical traditions and violated only by the 12-TET-only framework.

---

## Part IV: The Constraint Theory Argument

### 4.1 Constraints Are Not Western

A common and understandable objection to formalizing non-Western music in constraint-theory terms is that it represents another form of colonialism — imposing Western mathematical frameworks on traditions that have their own epistemologies. This objection deserves serious engagement.

The response is twofold. First, constraints are not Western. Every musical tradition uses constraints. A raga is a constraint system: it specifies which notes are permitted, in what order, with what ornaments, at what speed, at what time of day. A maqam is a constraint system: it specifies a tetrachordal framework, a tonic, a dominant, characteristic phrases, and modulation pathways. A tala is a constraint system: it specifies a cycle length, a structure of strong and weak beats, and permissible rhythmic variations.

The language of constraints — permissible vs. prohibited, structured vs. free, bounded vs. unbounded — is not an imposition but a translation. The Hindustani musician who says "you must not use the flat seventh in raga Bhoopali" is stating a constraint. The Arabic musician who says "maqam Rast modulates to maqam Suznak through the jins upper Rast" is stating a constraint on permissible modulation paths. The Javanese musician who says "the kenanga plays on beats 2 and 4 of the balungan cycle" is stating a constraint on temporal position.

Constraint theory does not add constraints to these traditions. It formalizes the constraints that already exist.

### 4.2 The Problem Is Whose Constraints Become Default

The problem with 12-TET is not that it uses constraints. Every tuning system constrains pitch — that's what "system" means. The problem is that one particular constraint set — the 12-tone equal-tempered division of the octave — was universalized through colonial infrastructure (pianos, recording technology, broadcast standards, MIDI) and then taught as the neutral, natural, default state of musical pitch.

This is the core insight: **the problem isn't constraints, it's monopoly.** A world where 12-TET is *one option among many* is a post-colonial musical infrastructure. A world where 12-TET is the infrastructure and everything else is a "world music" deviation is a colonial one.

Constraint theory, properly understood, is anti-monopolistic by design. It provides a formal language for describing *any* constraint set — any lattice, any funnel, any attractor — with equal precision and rigor. It makes 12-TET and 22-shruti and 24-quarter-tone and slendro/pelog into instances of the same mathematical type: a lattice of permissible pitch values with defined inter-point relationships. No lattice is more "mathematical" than another. No lattice is the "default." Each is a parameter choice.

### 4.3 SNAP to 22 Is Just as Mathematical as SNAP to 12

Let us make this concrete. The SNAP operation for 12-TET:

```
SNAP_12(x) = argmin_{p ∈ {0, 100, 200, ..., 1100}} |x - p|
```

The SNAP operation for 22-shruti:

```
SNAP_22(x) = argmin_{p ∈ {0, 90, 112, 182, 204, 294, 316, 386, 408, 498, 520, 590, 612, 702, 724, 794, 816, 906, 928, 996, 1018, 1100}} |x - p|
```

Both are nearest-neighbor projections. Both are mathematically well-defined. Both use the same distance metric (absolute difference in cents). The 22-shruti version has a larger lattice, but larger is not less mathematical. The complexity difference is in the data, not the operation.

The same applies to funnel structures (defining which notes attract melodic movement), temporal constraints (defining rhythmic cycles), and soft snap (defining the strength of attraction). These are general-purpose mathematical operations that become culturally specific only through parameterization.

### 4.4 Constraint Theory as Culturally Neutral Formalism

This is the strongest argument for our approach. Constraint theory provides:

1. **A universal formal language** that can describe the constraint systems of any musical tradition with equal precision.
2. **A computational framework** that implements these descriptions as working software, playable in real time.
3. **A decolonial infrastructure** that does not privilege any tuning system as default.

The framework respects all traditions equally because the math doesn't care which lattice you snap to. The choice of lattice is a cultural decision, made by the musician, not a technical decision imposed by the infrastructure. The musician using `world/arabic` and the musician using `world/western` are using the same constraint engine with different parameters. Neither is "normal" and the other "exotic." Both are parameterizations of the same neutral formalism.

This is what a post-colonial musical infrastructure looks like: not the absence of constraints, but the presence of all constraints, equally accessible, equally well-specified, equally playable.

### 4.5 The Path Forward

The technical infrastructure for a pluralistic musical future exists. MIDI 2.0 allows per-note microtonal specification. MTS allows custom tunings. Web Audio is tuning-agnostic. Our constraint theory modules provide the formal framework for implementing any tuning tradition as a well-specified constraint system with working software.

What's missing is adoption. The inertia of 40 years of MIDI 1.0 infrastructure — every synthesizer, every DAW, every music education curriculum, every streaming algorithm — is enormous. Changing it requires not just better tools but a cultural shift: the recognition that 12-TET is a choice, not a fact, and that other choices are equally valid, equally rigorous, and equally playable.

Constraint theory contributes to this shift by making the choice explicit. When you write `SNAP(vec, lattice)`, the lattice is a visible, named, parameter. You can't pretend it's invisible or natural. You have to choose. And in the choosing, you confront the colonial inheritance that made one choice seem inevitable.

---

## Conclusion: From Monopoly to Pluralism

The history of 12-TET's global dominance is a story of infrastructure, not aesthetics. The piano couldn't bend. Recording couldn't capture microtones. Radio couldn't broadcast them. MIDI couldn't encode them. Streaming can't recommend them. At every stage, the technical infrastructure filtered out everything that didn't fit the 12-tone grid, and the cultural infrastructure taught that the result was "music."

What was lost was not just pitch resolution — though 45% of Indian and 50% of Arabic pitch space is a staggering reduction. What was lost was the conceptual infrastructure for thinking about pitch in non-discrete, non-12-TET terms. Entire traditions of modal thinking, continuous pitch production, and temporal flexibility were rendered invisible by a system that couldn't represent them.

Constraint theory offers a way forward — not by abolishing constraints (which would be abolishing structure) but by democratizing them. When every lattice is equally snap-able, every funnel equally definable, every soft_snap equally applicable, the monopoly breaks. 12-TET becomes one choice among many. The 22-shruti lattice, the 24-quarter-tone system, the slendro and pelog scales, the continuous pitch of alap and meend — all become equally formalizable, equally computable, equally playable.

The math doesn't care whose music it structures. That's the point. That's the argument. That's the decolonial promise of constraint theory: not a world without constraints, but a world where every tradition's constraints are equally respected, equally specified, and equally realizable in sound.

---

## References and Further Reading

- Baragwanath, N. *The French Symphony in the Era of the French Revolution*. Cambridge University Press, 2024. (On the social construction of harmonic "theory.")
- Danielou, A. *Music and the Power of Sound*. Inner Traditions, 1995. (On just intonation and non-Western tuning systems.)
- Duffin, R. *How Equal Temperament Ruined Harmony (and Why You Should Care)*. Norton, 2007.
- Marcus, S. *Music in Egypt*. Oxford University Press, 2007. (On maqam and the quarter-tone system.)
- Nettl, B. *The Study of Ethnomusicology*. University of Illinois Press, 2015. (On the Western gaze in musicology.)
- Powers, H. "The Structure of Musical Meaning: A Perceptual Approach." *Ethnomusicology*, 1987. (On Indian raga as a cognitive system.)
- Rahn, J. "Javanese Pélog Tunings Reconsidered." *Yearbook for Traditional Music*, 1978.
- Shannon, J. "The Aesthetics of the Arabic Maqam." *Middle Eastern Studies*, 2006.
- Tamilmani, S. *The 22 Shrutis of Indian Music*. 2018. (On microtonal infrastructure.)
- The MIDI Manufacturers Association. *MIDI 2.0 Specification*. 2020.
- Toner, D. "The Pitch Bend Problem." *Computer Music Journal*, 2019. (On MIDI's microtonal limitations.)
- Turino, T. *Music as Social Life*. University of Chicago Press, 2008. (On participatory vs. presentational musical cultures.)
- van der Meer, W. *Hindustani Music in the 20th Century*. 1980. (On colonial impact on Indian music education.)
- constraint-theory-core: [github.com/SuperInstance/constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core)
- flux-tensor-midi: [github.com/SuperInstance/flux-tensor-midi](https://github.com/SuperInstance/flux-tensor-midi)

---

*This document is part of the fm-research series on constraint theory and its applications to world music systems.*
