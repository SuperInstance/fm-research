# Instructor Guide: Teaching Constraint Theory Through Music

> A practical guide for instructors using the `constraint-theory-core` tools and associated education materials in classroom settings.

---

## Table of Contents

1. [Overview](#overview)
2. [Setup Instructions](#setup-instructions)
3. [Prerequisite Knowledge](#prerequisite-knowledge)
4. [Common Student Mistakes](#common-student-mistakes)
5. [Assessment Strategies](#assessment-strategies)
6. [Accessibility Considerations](#accessibility-considerations)
7. [Multi-Session Curriculum (Week 1–4)](#multi-session-curriculum)

---

## Overview

This guide accompanies a set of tools and materials for teaching musical constraint theory:

- **`constraint-theory-core`** — Python library with exercise generator, lattice computations, rigidity verification, and temporal constraints
- **`constraint-theory-web`** — Browser-based Constraint Tarot tool for generating random constraint sets
- **50-MINUTE-CLASS-PLAN.md** — Single-session lesson plan for a first encounter with constraints
- **EXERCISE-CATALOG.md** — Full index of programmable exercises (4 topics × 3 difficulties × 3 templates each)
- **STUDENT-WORKBOOK.md** — Printable student-facing worksheets and composition challenges
- **ASSESSMENT-RUBRICS.md** — Grading rubrics for constraint-based compositions

The curriculum is designed for high school or early college music students. No advanced theory is required.

---

## Setup Instructions

### Software Installation

```bash
# Clone and install constraint-theory-core
git clone https://github.com/SuperInstance/constraint-theory-core.git
cd constraint-theory-core
pip install -e .

# Verify installation
python -m constraint_theory_core exercise --topic species_counterpoint --difficulty beginner --seed 1
```

### Constraint Tarot (Web Tool)

The Constraint Tarot is a browser-based tool that randomly generates constraint sets for composition:

```bash
# Option A: Open directly in browser
# Navigate to constraint-theory-web/constraint-tarot.html

# Option B: Serve locally for classroom use
cd constraint-theory-web
python -m http.server 8000
# Students visit http://<your-ip>:8000/constraint-tarot.html
```

### Classroom Tech Requirements

| Item | Minimum | Recommended |
|------|---------|-------------|
| Instructor station | Laptop with browser + Python 3.10+ | Same, connected to projector |
| Student devices | None (paper works) | 1 laptop/tablet per 2–3 students |
| Internet | Not required | Helpful for Tarot tool hosting |
| Audio | Piano or keyboard | MIDI keyboard + speakers |
| Printing | Handouts for each student | Color printing for reference cards |

### Pre-Class Checklist

- [ ] `constraint-theory-core` installed and exercise generator tested
- [ ] Constraint Tarot accessible (local file or served)
- [ ] Piano/keyboard available for demonstrations
- [ ] Printed handouts: staff paper, Constraint Quick Reference cards, worksheets
- [ ] Timer visible (phone timer works)
- [ ] Whiteboard/markers or projector ready
- [ ] Test exercise generation with a sample seed to preview what students will see

---

## Prerequisite Knowledge

### What Students Should Know

**Required (teach in first 10 minutes if needed):**
- Note names (C, D, E, F, G, A, B)
- What a scale is (can explain as "a subset of notes")
- What rhythm is (can be as simple as "short and long notes")
- Basic piano keyboard layout (black keys vs white keys)

**Helpful but not required:**
- Reading standard notation
- Major/minor triad spelling
- Simple intervals (3rd, 5th, octave)
- What a chord progression is

**Not required:**
- Any knowledge of constraint theory, lattice mathematics, or graph theory
- Advanced music theory (species counterpoint, etc.)
- Programming experience (unless using the API directly)

### What Instructors Should Know

- Basic music theory through diatonic harmony
- Familiarity with the 3 constraint types: SNAP (pitch subset), FUNNEL (tonal gravity), TEMPO (rhythm restriction)
- How to run Python commands and navigate a terminal
- The concepts of "tightness" (how strict a constraint is) and "constraint channeling creativity"

**Deep-dive topics** (for your own understanding; students don't need these):
- Eisenstein A₂ lattice — a mathematical way to measure how "close" pitch intervals are to consonance
- Laman rigidity — a condition from structural engineering applied to musical constraint networks
- Holonomy — consistency of transformations around cycles in the constraint graph
- These are implemented in `constraint-theory-core` and power the exercise verification, but students interact with them through musical metaphors, not math

---

## Common Student Mistakes

### Conceptual Misunderstandings

**1. "Constraints make my music worse."**
- *What's happening:* Students equate "restriction" with "bad."
- *Fix:* Play examples of highly constrained music that sounds great (pop songs using 4 chords, pentatonic melodies). Then play unconstrained chromatic noodling. Ask which sounds better.

**2. "I should try to break the constraints."**
- *What's happening:* Students treat constraints as obstacles to overcome rather than material to work with.
- *Fix:* Reframe: constraints are the *instrument*. You don't fight the guitar's 6 strings — you make music *because* of them.

**3. "Tighter constraints = less music."**
- *What's happening:* Intuitive but wrong. Three notes produce more focused, often more creative melodies than twelve.
- *Fix:* Do the 3-pitch composition exercise. Students are usually surprised by how much they can create.

### Technical Errors

**4. Not counting beats correctly.**
- *What's happening:* In rhythmic constraint exercises, students lose track of measure boundaries.
- *Fix:* Have them count out loud ("1-2-3-4") while composing. Use a metronome during composition.

**5. Ignoring the funnel (starting/ending notes).**
- *What's happening:* Students compose freely without regard to tonal gravity.
- *Fix:* Play their melody ending on a non-tonic note. Then play the same melody ending on tonic. Ask which feels "finished."

**6. Voice crossings in multi-part exercises.**
- *What's happening:* When writing for SATB, students let alto go above soprano, etc.
- *Fix:* Color-code voices (soprano = red, alto = blue, tenor = green, bass = black). Visual crossing becomes obvious.

**7. Parallel fifths/octaves in counterpoint.**
- *What's happening:* Two voices move in the same direction by the same perfect interval.
- *Fix:* This is normal and expected at beginner level. Don't penalize — point it out and explain why it's avoided in classical style. Intermediate students should catch it.

### Workflow Issues

**8. Spending too long on one exercise.**
- *Fix:* Enforce time limits strictly. Use a visible timer. The constraint *is* the time limit too.

**9. Analysis paralysis with too many choices.**
- *Fix:* Start with the tightest constraints (3 notes, 2 rhythm values). Paradoxically, more freedom can be more paralyzing.

**10. Not checking work against constraints.**
- *What's happening:* Students compose, then forget to verify they actually followed the rules.
- *Fix:* Provide a checklist with each exercise. "Did I use only C, E, G? ✓. Did I start and end on C? ✓."

---

## Assessment Strategies

### Formative (During Class)

- **Quick polls:** "Raise your hand if your melody uses only the 3 allowed pitches."
- **Neighbor check:** Have students play their melody for a partner; partner verifies constraints.
- **Live coding:** Project the exercise generator and have the class compose together.
- **Exit ticket:** One-sentence answer: "What's one way a constraint helped your composition?"

### Summative (Graded Work)

Use the rubrics in **ASSESSMENT-RUBRICS.md** which provide detailed criteria for three levels:

| Level | Focus | What to Grade |
|-------|-------|---------------|
| Beginner | Constraint compliance | Did they follow the rules? |
| Intermediate | Musical quality + constraints | Does it sound good *because* of the constraints? |
| Advanced | Structural understanding | Can they explain *why* the constraints produce certain effects? |

### Portfolio Assessment

For multi-session curricula, collect:
1. All worksheet completions
2. Two polished compositions (one tightly constrained, one loosely)
3. A short reflection (1 paragraph) on how constraints affected their creative process
4. One peer review of a classmate's composition

### Peer Review Guidelines

Have students exchange compositions and evaluate:
- Were the stated constraints followed? (Yes/No + evidence)
- What's the strongest moment in the piece?
- Where does the constraint feel most visible?
- One specific suggestion for improvement.

---

## Accessibility Considerations

### Hearing Impairments

- **Visual rhythm notation:** Ensure all rhythmic exercises use clear visual notation. Students can "feel" rhythm through vibration (place hand on a speaker) or visual pulse indicators.
- **Substitute pitch with structure:** D/deaf students can engage fully with structural and mathematical aspects of constraints (graph properties, Laman counts) even if they can't hear pitch.
- **Caption demonstrations:** When playing examples at the piano, write the note names on the board in real time.

### Visual Impairments

- **Audio-first tools:** The exercise generator outputs text that screen readers can read. Solutions and constraints are text-based.
- **Tactile keyboard work:** Physical piano keyboards provide tactile feedback. Guide hand placement for 3-pitch exercises.
- **Verbal description:** Describe all visual demonstrations verbally. "I'm playing three white keys in a row: C, then E, then G."

### Motor/Physical Limitations

- **Software alternatives:** Students who can't play piano can use notation software (MuseScore is free), the Constraint Tarot web tool, or simply write on staff paper.
- **Simplified input:** For students using assistive technology, the exercise generator accepts command-line input. Provide pre-generated exercises as text files.

### Cognitive/Learning Differences

- **Chunk exercises:** Break multi-step exercises into single steps with clear checkpoints.
- **Concrete before abstract:** Always demonstrate a constraint *musically* before explaining it *conceptually*. Sound → metaphor → theory.
- **Multiple representations:** Present each concept in at least 3 ways: auditory (play it), visual (write it), kinesthetic (clap/tap it).
- **Flexible timing:** Advanced exercises may take some students 60 minutes and others 20. Have extension activities ready for fast finishers.

### English Language Learners

- The constraint types (SNAP, FUNNEL, TEMPO) use simple, intuitive names.
- Visual aids (the Quick Reference Card) reduce language dependency.
- Music is universal — the concepts work in any musical tradition. Encourage students to apply constraints to music from their own culture.

---

## Multi-Session Curriculum

### Week 1: What Are Constraints? (50 minutes)

**Follow the 50-MINUTE-CLASS-PLAN.md directly.**

| Phase | Time | Activity |
|-------|------|----------|
| Hook | 0–5 min | Live performance + "why does this work?" |
| Constraint Zoo | 5–15 min | SNAP, FUNNEL, TEMPO demonstrations |
| Guided Composition | 15–25 min | 3-pitch melody with quarter/eighth notes |
| Tarot Activity | 25–40 min | Generate and compose from random constraint sets |
| Share & Reflect | 40–50 min | Performances and "constraints channel creativity" |

**Homework:** Complete Worksheet 1 (SNAP) from the Student Workbook.

---

### Week 2: Tightening the Constraints (50 minutes)

**Focus:** Deepening understanding of each constraint type through focused exercises.

| Phase | Time | Activity |
|-------|------|----------|
| Review | 0–5 min | Quick recap: name the 3 constraint types. Play last week's best composition. |
| SNAP Deep Dive | 5–20 min | Exercise: compose with 5 pitches (pentatonic) → then 3 → then 2. Discuss: what changes? |
| FUNNEL Deep Dive | 20–35 min | Exercise: compose a melody that *must* end on C. Then: must start *and* end on C. Then: must pass through G in the middle. |
| TEMPO Deep Dive | 35–45 min | Exercise: compose rhythms with halves only → halves + quarters → quarters + eighths. |
| Reflect | 45–50 min | Journal: "Which constraint type is hardest for you? Which is most helpful?" |

**Homework:** Complete Worksheets 2 and 3 (FUNNEL, TEMPO) from the Student Workbook.

**Exercise generator usage:**
```bash
# Generate a voice-leading beginner exercise for the SNAP activity
python -m constraint_theory_core exercise --topic voice_leading --difficulty beginner --seed 7 --show-solution
```

---

### Week 3: Combining Constraints (50 minutes)

**Focus:** Layering multiple constraints; introduction to constraint "tightness."

| Phase | Time | Activity |
|-------|------|----------|
| Warm-up | 0–5 min | Free compose for 3 minutes (no constraints). Then: compose for 3 minutes with all 3 constraints. Which was easier? |
| Constraint Layering | 5–20 min | Start with 1 constraint. Add a 2nd. Add a 3rd. At each step: compose 2 bars. Discuss the effect of each addition. |
| Tightness Spectrum | 20–35 min | Define "tight" vs "loose" constraints. Exercise: compose the same 4-bar phrase at 3 different tightness levels (many notes → 7 → 3). |
| Peer Review | 35–45 min | Exchange compositions. Partner identifies: what constraints were used? How tight? |
| Introduction to Composition Challenge | 45–50 min | Preview the final composition project (Week 4). Hand out the challenge sheet. |

**Homework:** Complete Worksheets 4 and 5 from the Student Workbook. Begin working on Composition Challenge 1.

**Exercise generator usage:**
```bash
# Generate a harmonic constraints intermediate exercise for the layering activity
python -m constraint_theory_core exercise --topic harmonic_constraints --difficulty intermediate --seed 12 --show-solution
```

---

### Week 4: Composition Showcase (50 minutes)

**Focus:** Independent creative work; performance; reflection.

| Phase | Time | Activity |
|-------|------|----------|
| Work Session | 0–15 min | Students finalize their composition challenges. Instructor circulates and coaches. |
| Rehearsal | 15–20 min | Quick practice runs. Pair up for final peer check of constraint compliance. |
| Performances | 20–40 min | Each student performs their composition (or plays a recording). Before performing, they state their constraints. After, the class guesses which moments show the constraints most clearly. |
| Reflection & Portfolio | 40–50 min | Final self-assessment using the rubric in the Student Workbook. Collect portfolios. |
| Wrap-up | 50 min | "Constraints don't limit creativity — they channel it. Take this idea into everything you create." |

**Exercise generator usage:**
```bash
# Generate an advanced exercise for students who want an extra challenge
python -m constraint_theory_core exercise --topic species_counterpoint --difficulty advanced --seed 99 --show-solution
```

---

## Adapting the Curriculum

### Shorter Sessions (30 minutes)
- Week 1: Skip the Tarot activity; extend the guided composition.
- Week 2: Do one deep dive instead of three.
- Week 3: Skip peer review.
- Week 4: Limit to 5 performances.

### Longer Sessions (90 minutes)
- Add the Tarot activity to every session.
- Include a "free compose" warm-up each week.
- Add a listening component: play a piece by a constraint-focused composer (Messiaen's modes of limited transposition, Cage's chance operations, Bach's canons) and analyze the constraints.
- Run the exercise generator live and have students solve programmatically generated exercises.

### College-Level (Semester Course)
- Replace Week 1–4 with a 12-week sequence covering all 12 topic×difficulty combinations
- Introduce the mathematical foundations: A₂ lattice, Laman rigidity, holonomy
- Include programming exercises: students write their own constraint generators
- Final project: compose a multi-movement piece where each movement uses a different constraint system, accompanied by a analytical paper

### For Non-Music Classrooms
- The constraint framework applies to any creative domain. Adapt:
  - **Creative writing:** SNAP = limited vocabulary, FUNNEL = narrative arc, TEMPO = sentence length
  - **Visual art:** SNAP = limited color palette, FUNNEL = compositional focal point, TEMPO = brush stroke size
  - **Game design:** SNAP = limited mechanics, FUNNEL = player progression path, TEMPO = action frequency

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Exercise generator won't install | Ensure Python 3.10+ and pip are available. Try `pip install --upgrade pip` first. |
| Tarot tool won't load | Open the HTML file directly in a browser. No server required. |
| Students finish too fast | Increase constraint tightness. Generate advanced exercises. Have them compose a second piece with *different* constraints. |
| Students are stuck | Reduce constraint tightness. Provide a starting note or rhythm. Pair them with a stronger student. |
| No piano available | Use virtual pianos (online), phone apps, or clap/sing the exercises. |
| Class is too large for performances | Do small-group performances (3–4 students per group). Use a sign-up sheet. |

---

## Further Resources

- **50-MINUTE-CLASS-PLAN.md** — Detailed minute-by-minute lesson plan for Week 1
- **EXERCISE-CATALOG.md** — All 36 exercise templates with objectives, timing, and rubrics
- **STUDENT-WORKBOOK.md** — Printable worksheets and challenges
- **ASSESSMENT-RUBRICS.md** — Grading criteria for all levels
- **constraint-theory-core/docs/USER-GUIDE.md** — Technical documentation for the Python library
- **constraint-theory-web/** — Browser-based Constraint Tarot tool
