# BETA TEST — ROUND 8: THE CLASSICAL COMPOSER

**Repo:** `SuperInstance/counterpoint-engine`
**Tester:** Classical composer/conductor. Sibelius/Dorico daily driver. Species counterpoint under Fux/Jeppesen. I believe in voice-leading, the Western tonal tradition, and that Bach wrote the rules everyone else merely follows.
**Date:** 2026-05-23

---

## Executive Verdict

**C+ for ambition. D+ for execution.**

This library wants to be a constraint-satisfaction engine for species counterpoint — a noble goal. The framing as Laman graphs is mathematically interesting but musically questionable. The actual counterpoint it generates would get you a **gentle but firm C–** in any undergraduate theory class, and your teacher would ask you to redo the assignment paying attention to *why* the rules exist, not just *that* they exist.

What works: the SAT/UNSAT constraint architecture is clean. No parallel fifths or octaves — the engine catches those. The backtracking search finds solutions reliably.

What fails: almost everything else that makes counterpoint *music* rather than *constraint satisfaction*.

---

## Test 1: First Species Counterpoint (C major, 8 notes)

**Cantus firmus:** C D E F G A B C (MIDI 60–72)
**Generated counterpoint:** C F E D C C D C (MIDI 48, 53, 52, 50, 48, 48, 50, 48)

### What my theory teacher would say:

> "You've avoided parallel fifths and octaves. Congratulations, you've met the minimum standard. Now look at your counterpoint line — C-F-E-D-C-C-D-C. You have *three unisons* (beats 0, 2, 7). Fux permits unisons only at the beginning and end of an exercise. Unisons in the middle destroy voice independence — you've collapsed two voices into one. And your counterpoint ends on a unison when it should end on a perfect consonance (octave or fifth) or at minimum a third, with the upper voice landing on the tonic."

**Specific problems:**

1. **Excessive unisons.** Beats 0, 2, and 7 are all unisons. This is the #1 beginner mistake in species counterpoint. The engine's `consonant_interval` rule allows unisons everywhere — it shouldn't. First species requires *imperfect* consonances (thirds, sixths) preferred on interior beats, with perfect consonances (unison, fifth, octave) only at structural points.

2. **No preference for contrary motion.** The engine picks pitches sorted by proximity to the previous note. This creates too much parallel and oblique motion. Species counterpoint demands *contrary motion as the ideal*, with similar motion used sparingly and only with imperfect consonances.

3. **Melodic contour is aimless.** The counterpoint C-F-E-D-C-C-D-C has no arch, no climax, no sense of direction. A good counterpoint line should have a single high point or low point and move gracefully toward it. This sounds like someone pressing random diatonic keys within range.

4. **Voice is always below the cantus firmus.** Every single beat has the counterpoint below the CF. This isn't voice crossing per se, but it means the engine treats "above" and "below" as afterthoughts. In proper two-voice counterpoint, the counterpoint can be above *or* below, and the relationship matters for the interval quality.

**Fux compliance: 3/10.** The barest mechanical rules are met. The musical spirit is absent.

---

## Test 2: Fourth Species (Suspensions)

**Cantus firmus:** C D E F G F E D C (9 notes)
**Generated result:** Contains 2 suspensions at beats 1 and 5.

### The suspensions work — barely.

Beat 1: Preparation on consonant (m3), suspension on P4 (dissonant), resolution step down to consonant. **This is correct.** A 4-3 suspension. I'd accept this.

Beat 5: Preparation on m6, suspension on tritone (interval 6), resolution step down to P5. **This is a legitimate suspension.** The tritone resolving to the fifth is standard.

### What's wrong:

1. **Only 2 suspensions in 9 beats.** Fourth species is *defined* by tied syncopations creating chains of suspensions. Fux's examples are nearly continuous suspension chains. Two suspensions in nine beats is barely fourth species — it's mostly first species with occasional syncopation.

2. **No suspension chains.** The two suspensions are isolated, not chained. In proper fourth species, a resolution becomes the preparation for the next suspension: prepare-suspend-resolve-prepare-suspend-resolve. This creates the characteristic "sighing" quality. The engine generates them independently.

3. **The non-suspension beats are just consonant framework.** Where there's no suspension, the voice sits on a consonance. This is technically allowed but musically dull — the whole point of fourth species is the tension-release pattern of suspensions.

4. **No 9-8, 7-6, or 2-3 suspension types.** The engine only produces step-down resolutions but doesn't categorize or ensure variety in suspension type. A good fourth-species exercise uses multiple suspension types.

**Suspension preparation/resolution: technically correct. Musical quality: mediocre.**

---

## Test 3: 4-Voice "Fugue Excerpt"

**Subject:** D Eb D C F E C D Bb (9 notes, D minor)
**Result:** 4 voices, 282/282 constraints satisfied.

### Let's be clear: this is NOT a fugue excerpt.

A fugue has:
- **Staggered entries** — the subject enters in one voice, then another, then another
- **Tonal answer** — the second entry typically transposes to the dominant
- **Countersubject** — a consistent melodic idea that accompanies the subject
- **Episode** — sequential material between entries
- **Stretto** — overlapping subject entries

This engine generates 4 simultaneous voices against a fixed cantus firmus. That's **chorale writing**, not fugal writing. There is no subject/answer structure, no countersubject, no stretto, no episodic material.

The "fugue excerpt" example is simply dishonest labeling. It's 4-voice first-species counterpoint, which is a valid thing, but calling it a "fugue" is like calling a C major scale a "symphony."

### Voice-specific problems:

1. **Voice crossing.** Voice 1 (allegedly alto) is *entirely below* Voice 0 (soprano). At every single beat, the "alto" sings lower than the "soprano." This isn't just crossing — it's voice *inversion*. The bass sings as low as MIDI 38 (D2) while the soprano starts at D4. The spacing is bizarre.

2. **Voice 3 crosses below Voice 2 at beat 1.** Direct voice crossing between inner voices.

3. **No voice-range enforcement by part.** SATB writing has specific ranges: soprano C4-G5, alto G3-D5, tenor C3-G4, bass E2-D4. The engine accepts arbitrary `VoiceRange` objects but doesn't enforce proper SATB spacing or prevent overlap.

4. **No spacing rules.** Adjacent upper voices should be within an octave of each other. The gap between soprano and alto at beat 0 is a fifth, then an octave-plus at beat 1. This is acceptable in free writing but poor in strict 4-part writing.

**Fugal conventions: 0/10. This is not a fugue.**
**4-part writing quality: 4/10. Avoids parallel errors but ignores spacing and crossing.**

---

## Test 4: Parallel Fifths, Octaves, Voice Crossing

### The engine correctly detects parallel fifths and octaves. ✓

The `no_parallel_fifths` and `no_parallel_octaves` rules check consecutive beats for parallel motion into perfect intervals. This works as advertised.

### But it does NOT check:
- **Hidden/direct fifths and octaves** — where two voices move to a perfect interval in similar motion (but not from a perfect interval). These are forbidden in strict counterpoint when the upper voice leaps.
- **Voice crossing** — there is no `no_voice_crossing` constraint. The engine happily generates voices that cross, as seen in the 4-voice test.
- **Voice overlap** — where one voice moves into the previous position of another voice.
- **Spacing violations** — adjacent upper voices more than an octave apart.

The engine catches the most famous rule violations but misses the subtler ones that separate competent from excellent.

---

## Test 5: Minor Mode — Leading Tone Handling

### This is a serious failure.

The engine uses **natural minor** (Aeolian mode): `(0, 2, 3, 5, 7, 8, 10)`.

In tonal counterpoint — which is what species counterpoint IS — the minor mode requires a **raised leading tone**. The seventh degree must be sharpened to create a semitone pull toward the tonic. This is not optional; it is fundamental to tonal music.

In C minor, the leading tone is B-natural (pitch class 11), not B-flat (pitch class 10). But pitch class 11 is not in the natural minor scale. So:

- The engine's `proper_resolution` rule checks if the leading tone (pc=11) resolves to the tonic (pc=0)
- But the engine's `Scale(minor)` never produces pitch class 11
- Therefore no counterpoint note ever IS the leading tone
- Therefore the `proper_resolution` rule **never actually fires in minor mode**

This is a catastrophic design flaw. It means the engine's minor mode is **functionally modal** (Aeolian), not tonal. Species counterpoint is inherently tonal. The engine cannot generate tonally correct minor-mode counterpoint.

**What's needed:** Harmonic minor scale (raised 7th) as default for minor mode, or at minimum a `melodic_minor` option that raises 6 and 7 ascending and lowers them descending.

**My theory teacher would write in red pen:** "You have written Aeolian-mode counterpoint. Please redo in a tonal minor key with proper leading-tone resolution."

---

## Test 6: MusicXML Export

**There is no MusicXML export.** Only MIDI.

This is a significant limitation for any Sibelius or Dorico user. MIDI import into notation software:
- Loses voice assignments (which notes belong to which voice)
- Loses rhythmic notation intent (no way to distinguish quarter notes from tied eighths)
- Loses key signature, time signature, and enharmonic spelling
- Requires manual cleanup that takes longer than entering the notes by hand

A counterpoint engine targeting notation-software users **must** export MusicXML. The MIDI export is a nice demo but practically useless for the stated audience.

**Verdict: Not usable in a Sibelius/Dorico workflow without MusicXML.**

---

## The Laman Graph Framing

The library frames contrapuntal constraints as edges in a Laman graph, claiming that "a counterpoint texture is rigid iff its constraint graph is Laman." This is mathematically interesting but musically questionable.

**The problem:** A Laman graph with N vertices has exactly 2N−3 edges. For 4 voices, that's 5 edges (constraints). But real counterpoint has far more than 5 constraint types operating between 4 voices — parallel intervals, consonance, resolution, voice crossing, spacing, range, contour, etc. The Laman framework forces you to pick only 5 of potentially dozens of constraint-pair relationships.

The engine's workaround is to apply the same 5 constraint *types* to all voice pairs (not just the Laman edges), which makes the Laman framing somewhat decorative — the actual constraint checking doesn't respect the graph structure.

**My verdict:** The Laman framing is a clever mathematical analogy but doesn't add musical value. It's more useful as a publication hook than as an engineering principle.

---

## IDEATION: Teaching Tool or Composition Tool? (600 words)

### Neither — Yet

Let me be direct about what this engine is and isn't.

**As a teaching tool,** it falls short because it generates counterpoint that is *mechanically adequate but musically impoverished*. A student using this would learn to avoid parallel fifths but wouldn't learn why contrary motion matters, why melodic contour matters, why the quality of each interval matters beyond "is it consonant?" Species counterpoint pedagogy isn't about avoiding errors — it's about developing a sensibility for beautiful, singable lines. This engine produces lines that are technically error-free but uninspired. A student would be better served by studying Fux's examples directly, which is what composition teachers have been saying for 300 years.

The engine would be *much* more valuable as a teaching tool if it could:
- Explain *why* each note was chosen (not just that it satisfies constraints)
- Show the alternatives that were rejected and explain why
- Score the quality of a student's counterpoint against a rubric
- Generate "almost correct" examples for students to find errors in
- Provide progressive difficulty levels matching standard pedagogy

**As a composition tool,** it's even further from useful. Real composers don't write first-species counterpoint as finished music. They use contrapuntal technique as *infrastructure* beneath melodic, harmonic, and rhythmic surfaces. A composition tool needs to handle:
- Free rhythm and meter
- Chromatic harmony and modulation
- Motivic development and transformation
- Textural variation (homophonic vs. contrapuntal sections)
- Orchestration and timbral considerations
- Formal architecture (sonata, rondo, etc.)

This engine addresses none of these. It's a proof-of-concept, not a compositional aid.

### Would Bach Approve?

Bach would recognize the attempt and appreciate the mathematical framing — he was, after all, a master of systematic thinking in music. The Art of Fugue is essentially a demonstration that you can build an entire musical universe from a single subject through rigorous contrapuntal procedures.

But Bach would be horrified by the output. His counterpoint isn't just rule-following; it's *expressive*. Every voice is a melody worth singing. Every interval choice has emotional weight. The suspension in measure 15 of the C minor fugue (WTC I) isn't there because the rules require it — it's there because it *aches*. This engine's suspensions don't ache. They merely resolve.

### Where It Deviates from Species Rules

Beyond the issues already detailed:
1. **No distinction between perfect and imperfect consonances.** Fux requires imperfect consonances (3rds, 6ths) on most beats, reserving perfect ones (unisons, 5ths, octaves) for beginnings and endings.
2. **No contrary motion preference.** The engine is motion-agnostic; Fux demands contrary motion as the default.
3. **No melodic arc requirement.** A counterpoint line should have a single climax and move purposefully.
4. **No prohibition on repeating the same interval quality consecutively.** Two major thirds in a row is poor voice leading.
5. **No treatment of the tritone.** The tritone (augmented fourth/diminished fifth) has special handling rules in species counterpoint that the engine ignores.

### The Dream: A Full Symphonic Movement

What would it take to generate a full symphonic movement? This engine is approximately 1% of the way there. The remaining 99% requires:
- Tonal harmony (chord progressions, modulation, cadences)
- Formal structures (sonata form, scherzo, theme and variations)
- Orchestration (instrument-specific writing, doublings, balance)
- Thematic development (motivic transformation, fragmentation, augmentation)
- Rhythmic sophistication (syncopation, hemiola, mixed meter)
- Dynamic and articulation control
- Textural architecture (when to write for full orchestra vs. chamber texture)
- Expressive timing (rubato, agogic accents)

The constraint-satisfaction paradigm could potentially scale to these problems, but it would require orders of magnitude more constraints and a much more sophisticated search strategy than simple backtracking.

### The Honest Assessment

This is a clever undergraduate CS project dressed up with Laman graph theory. The code is clean, the tests pass, the API is reasonable. But it confuses *avoiding errors* with *creating music*. The gap between "no parallel fifths" and "write a beautiful melody" is the entire history of Western art music.

---

## Summary Scorecard

| Criterion | Score | Notes |
|-----------|-------|-------|
| No parallel 5ths/octaves | 9/10 | Correctly enforced |
| Consonance enforcement | 7/10 | Works but allows unisons everywhere |
| Leading tone resolution | 2/10 | Broken in minor; never fires |
| Melodic quality | 2/10 | Aimless contours, no climax |
| Contrary motion preference | 0/10 | Not implemented |
| Species 4 suspensions | 5/10 | Correct but sparse, no chains |
| Multi-voice writing | 4/10 | Voice crossing, poor spacing |
| Fugal structure | 0/10 | Labeling is dishonest |
| MusicXML export | 0/10 | Not available |
| Minor mode handling | 1/10 | Natural minor = not tonal |
| Voice crossing prevention | 0/10 | Not implemented |
| Hidden 5ths/octaves | 0/10 | Not checked |
| Code quality | 8/10 | Clean, well-documented |
| Test coverage | 8/10 | 156 tests, all passing |
| API design | 7/10 | Reasonable, if limited |

**Overall: 3.5/10 as a musical tool. 7/10 as a CS project.**

The engine does what it says on the tin — generates note sequences satisfying a subset of contrapuntal constraints. But the subset is too small, the musical defaults are too permissive, and the output lacks the qualities that make species counterpoint worth studying. Fix the minor mode, add voice-crossing checks, prefer contrary motion, ban unisons on interior beats, and add MusicXML export — then we can talk.

---

*"The rules of counterpoint are not chains but wings." — Nadia Boulanger. This engine has chains but no wings.*
