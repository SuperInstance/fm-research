# BETA TEST — ROUND 3: The Math Educator

**Tester Persona:** High school math teacher, runs a "Math in Music" elective. Students aged 15–18. Knows basic Python.  
**Date:** 2026-05-23  
**Packages Tested:** `constraint-theory-core` v0.1.0, `fm-research` education materials  
**Environment:** Python 3.10+, pip install -e ., Ubuntu/WSL2

---

## Executive Summary

This is a genuinely impressive educational toolkit that bridges abstract mathematics and music in a way I haven't seen before. The 50-minute class plan is among the best single-session lesson plans I've used in 12 years of teaching. The exercise generator is programmatically solid. But there are real gaps — the math-to-music bridge is stronger on the music side than the math side, several exercises assume music theory knowledge that my math students won't have, and the workbook needs significant adaptation for a math classroom. With targeted revisions, this could become a standard teaching tool.

**Overall Grade: B+** — Usable with modifications. Strong foundation. Needs a math-teacher's polish pass.

---

## Part 1: The 50-Minute Class Plan

### Is It Actually Usable?

**Yes, with caveats.** This is one of the most detailed and thoughtful single-session plans I've seen. The minute-by-minute breakdown is realistic — most lesson plans I've used lie about timing, but this one doesn't. Here's my assessment phase by phase:

**The Hook (0–5 min): ✅ Excellent**
The three-note piano demo is a perfect attention grabber. The question "Why does it still sound like music?" is exactly the right level of provocative for 15-year-olds. The reveal of "constraints" as the answer is clean. This works as written.

**The Constraint Zoo (5–15 min): ✅ Very Good**
The SNAP/FUNNEL/TEMPO framework is intuitive and the physical demonstrations (playing only white keys, singing Ti and stopping, clapping exercises) are the right move. Ten minutes is tight for three constraint types, but the pacing notes acknowledge this.

*Issue:* The "TEMPO" constraint name is confusing. In music, tempo means speed. Here it means "which rhythm values are allowed." I'd rename this to "GRID" or "RHYTHM" to avoid the collision with the standard meaning. My students who've had band or orchestra will be confused.

**Hands-On Composition (15–25 min): ✅ Good, needs minor tweaks**
The 3-pitch composition exercise is well-designed. The pitch assignments by group are smart — using triads means everything sounds consonant no matter what students write, which keeps the first experience positive.

*Issue:* 10 minutes is barely enough for students who've never composed before. I'd budget 12–15 minutes. Also, some of my math students won't know what a "bar" or "4/4 time" is. The worksheet assumes basic musical literacy.

**Performance + Analysis (25–35 min): ✅ Good**
The coaching table for common student struggles is genuinely useful — I'll print that out. The "constraint tightness" spectrum drawn on the board is a strong visual.

**Constraint Tarot Activity (35–45 min): ⚠️ Nice idea, unclear execution**
I couldn't find the `constraint-theory-web/constraint-tarot.html` file in the repository. The class plan references it, the instructor guide explains how to serve it, but it doesn't seem to exist yet (or is in a different repo). This is a significant gap — the "fun payoff" of the class depends on a tool I can't access.

**Wrap-Up (45–50 min): ✅ Solid**
The three takeaways are clear. The homework assignment is appropriate. The teaser for next class ("what happens when we add more voices?") creates good momentum.

### What Needs Changing

1. **Rename TEMPO → GRID** (or RHYTHM). The collision with the standard musical term is a real problem.
2. **Add a "What is a bar? What is 4/4?" micro-lesson** (2–3 slides) for non-music students. This is my math elective, not band. Many students won't know this.
3. **Budget more time for composition** — 15 minutes instead of 10.
4. **Provide the Constraint Tarot tool**, or a paper-based fallback with enough detail to be usable without it.

### What's Missing

- **Math connections are implicit, not explicit.** The plan teaches music composition under constraints. But nowhere does it say "hey, you just did combinatorics" or "this is a graph theory problem." For a *math* class, I need those connections made visible.
- **No assessment of mathematical understanding.** The rubric measures musical compliance. I need to know: did the student understand *why* fewer notes = more focused outcomes? Can they compute the number of possible melodies? Can they explain the difference between a constraint and a preference?
- **No connection to the Python library.** The class plan is entirely analog (piano, paper, clapping). The exercise generator is mentioned in the instructor guide but not woven into the lesson. For a math class, I'd want a "let's see what the computer says" moment.

---

## Part 2: The Exercise Generator

### Beginner Level — All 4 Topics

I ran all four topics at beginner level with seed=42. Results:

| Topic | Template Selected | Usable for Math Students? | Notes |
|-------|------------------|--------------------------|-------|
| `species_counterpoint` | Interval classification on A₂ lattice | ⚠️ Partially | The snap/is_safe computation is great math. But "cantus firmus" and "first-species counterpoint" are foreign terms. Need translation. |
| `voice_leading` | Triad distance matrix | ✅ Yes | This is essentially a distance matrix computation. Perfect for a math class. Students can compute, tabulate, find minimum. |
| `harmonic_constraints` | Chord progression analysis (C→G→Am→F→C) | ⚠️ Partially | Computing "distance" between chords is good math. But "smooth" vs "rough" classification is subjective without clear thresholds. |
| `rhythmic_constraints` | Temporal funnel with quarter/eighth notes | ✅ Yes | The funnel concept (tolerance narrowing over time) is directly mathematical. The binary choice (quarter vs eighth) per beat is combinatorics. |

**The good:** The generator works perfectly. Seed reproducibility passed. Error handling is clean. The JSON output is well-structured. The CLI is usable. The scoring rubrics are consistent (always sum to 100). Each exercise has clear constraints, starting notes, solutions, and rubrics.

**The problem:** Three of the four beginner exercises assume significant music theory knowledge. "Cantus firmus," "species counterpoint," "SATB voicing," "consonant intervals" — these are not terms my math students know. The beginner label is misleading; it means "beginner at constraint theory," not "beginner at music."

### Advanced Level — All 4 Topics

I ran all four at advanced with seed=7. These are *serious* exercises:

| Topic | Template Selected | Appropriate For? | Notes |
|-------|------------------|------------------|-------|
| `species_counterpoint` | Invertible counterpoint at the octave | College music majors | Way beyond high school math students |
| `voice_leading` | Temporal funnel + Laman rigidity | Strong math students with music background | The funnel + rigidity combo is beautiful math but requires understanding both domains deeply |
| `harmonic_constraints` | Bach chorale as CSP | College CS/music crossover | This is a genuine constraint satisfaction problem — would fit a CS class, not a math elective |
| `rhythmic_constraints` | Euclidean rhythm (Björklund's algorithm) | ✅ Strong math students | This is the winner. Björklund's algorithm is real math, maximal evenness is a provable property, A₂ distance gives it a computational component. |

**The gap between beginner and advanced is enormous.** Beginner exercises ask "which intervals are safe?" Advanced exercises ask "compose a five-voice motet with Laman-rigid voice-pair graph." There's no middle ground for a math student who doesn't know counterpoint but can handle the math.

### Seed Parameter — Reproducibility

✅ **Works perfectly.** Same seed always produces the same exercise. Different seeds produce different template selections. This is essential for:
- Giving all students the same exercise (same seed)
- Giving each student a unique exercise (different seeds)
- Reproducing grading disputes (same seed = same exercise)

This is one of the most practically useful features for a teacher.

### What I'd Need for a Math Classroom

A "math mode" flag that:
1. Strips out music-theory jargon and replaces it with mathematical language
2. Adds explicit math objectives ("compute," "classify," "verify," "count")
3. Includes Python code snippets students can run and modify
4. Provides numerical exercises (compute the A₂ distance, count Laman edges) rather than composition exercises ("write a counterpoint")

---

## Part 3: The Student Workbook

### Would My Students Use It?

**The worksheets are well-structured, but designed for music students, not math students.** Here's the honest breakdown:

**Worksheet 1 (SNAP): ⚠️**
The three-note composition exercise is fine. But the "How Many Melodies?" combinatorics question (Exercise 1B) is *exactly* the kind of thing I want — "how many different 4-beat melodies can you make with 3 pitches and 2 rhythm values?" This is a genuine math problem embedded in a music context, and it's brilliant. I'd expand this section significantly.

**Worksheet 2 (FUNNEL): ✅**
The "landing on C" and "round trip" exercises are good, but again, they assume students know what "C major" means. For math students, I'd frame this as: "You have a set of 7 elements. Your sequence must start and end with element 1. How does this constraint affect the space of possible sequences?"

**Worksheet 3 (TEMPO/GRID): ⚠️**
The rhythm exercises work better for math than the pitch exercises, because rhythm is essentially counting and division. "Each bar has 4 beats. You can use notes worth 1 beat or 0.5 beats. Fill the bar exactly." This is a partition problem.

**Worksheet 4 (Combining Constraints): ✅**
This is where the math gets interesting. Combining constraints = intersecting constraint sets. The total number of possible melodies shrinks (or doesn't) depending on how constraints interact. This is where I'd spend the most time in a math class.

**Worksheet 5 (Constraint Tarot): ❌**
Without the Tarot tool, this is unusable. And even with it, the "draw random constraints and compose" framing is more suited to a creative workshop than a math class.

**Self-Assessment Rubric:** The emoji-based rubric (😕😐😊) is too childish for 15–18 year olds. They'll find it patronizing. Replace with a standard 1–4 scale or proficiency-based language (Beginning / Developing / Proficient / Exemplary).

**Glossary:** Good and necessary. But it's music-focused. I'd add mathematical terms: combinatorics, constraint satisfaction, graph theory, lattice, covering radius, rigidity, convergence.

### What Would Make It Work for Math Students

1. **Add computation sections:** After each composition exercise, add a "Do the Math" section:
   - "How many different melodies satisfy your constraints? Show your work."
   - "What's the minimum/maximum number of notes in a 4-bar melody with your constraints?"
   - "Graph your melody as a sequence of pitch numbers. What patterns do you see?"

2. **Replace music-theory terminology with mathematical language** in a parallel track:
   - "SNAP constraint" → "Subset constraint on a discrete set"
   - "FUNNEL constraint" → "Boundary condition on a sequence"
   - "TEMPO constraint" → "Partition constraint on a fixed-sum integer"

3. **Add Python exercises:** "Run this code. What does snap(0.5, 0.3) return? Why?"

---

## Part 4: Assessment Rubrics

### Are They Usable?

**For a music class: ✅ Excellent.** The three-level rubric system (beginner/intermediate/advanced) with 100-point breakdowns is thorough, fair, and practical. The feedback templates are specific and useful — I'd actually use them.

**For a math class: ⚠️ Needs major adaptation.**

The rubrics measure:
- Constraint compliance (following musical rules)
- Musical coherence (does it sound good?)
- Creativity within constraints
- Analytical writing about the process

For a math class, I'd need to measure:
- **Mathematical correctness:** Can they compute the number of valid melodies? Can they correctly identify Laman edges? Can they verify holonomy?
- **Computational fluency:** Can they use the Python library to check their work?
- **Conceptual understanding:** Can they explain *why* a constraint reduces the solution space? Can they generalize from music to other domains?
- **Transfer:** Can they apply the same constraint framework to a non-musical problem?

The portfolio rubric is a good structure (worksheets + compositions + reflection + peer review). I'd keep the structure, change the content.

**The quick grading reference (red/green flags) is excellent.** "Student breaks a constraint intentionally and can explain why → advanced thinking" — this is exactly the kind of insight that makes a rubric actually useful rather than just a scoring tool.

---

## Part 5: IDEATION SESSION — A Semester with Constraint Theory

### My Curriculum: "Math in Music — Constraint Theory Semester"

If I had this material for a full semester (18 weeks, 3 sessions/week, 50 min each), here's what I'd build:

#### Unit 1: Foundations (Weeks 1–4) — "What Are Constraints?"

**Week 1: Introduction to Constraints**
- Day 1: The 50-minute class plan (as written, with modifications above)
- Day 2: Combinatorics of constrained melody — count the possibilities
- Day 3: Python intro: `pip install`, `generate_exercise()`, the `snap()` function

**Week 2: Discrete Sets and Subsets (SNAP)**
- Day 1: Pitch as integer, octave as mod 12, scales as subsets
- Day 2: Combinatorics: how many 4-note melodies from a k-note subset?
- Day 3: Lab day: explore different subset sizes, measure "variety" vs "coherence"

**Week 3: Sequences and Boundary Conditions (FUNNEL)**
- Day 1: Sequences with fixed endpoints — boundary conditions
- Day 2: Markov chains: each note depends on the previous one
- Day 3: Lab day: build a first-order Markov chain from a simple melody

**Week 4: Integer Partitions (TEMPO/GRID)**
- Day 1: Rhythm as integer partitioning (each bar = sum of note values)
- Day 2: Generating functions for rhythm patterns
- Day 3: Quiz + reflection: "What do these three constraint types have in common?"

#### Unit 2: Combinations (Weeks 5–9) — "When Constraints Collide"

**Week 5: Combining Constraints = Intersecting Solution Spaces**
- Day 1: Two constraints at once — the solution space shrinks (or not)
- Day 2: Venn diagrams of constraint spaces
- Day 3: Lab: generate exercises with all three constraints, compute solution counts

**Week 6: Graph Theory Introduction**
- Day 1: Notes as nodes, transitions as edges
- Day 2: Degree, connectivity, paths — applied to melody graphs
- Day 3: Build the C-major melody graph (7 nodes, edges between consecutive scale tones)

**Week 7: Laman Rigidity**
- Day 1: What makes a structure rigid? Straws and connectors demo (physical)
- Day 2: The 2n-3 rule — prove it for small cases
- Day 3: `henneberg_construct()` — build rigid graphs, verify with `is_laman()`

**Week 8: Consensus and Coupling**
- Day 1: The metronome synchronization problem
- Day 2: Algebraic connectivity and optimal coupling — what do eigenvalues have to do with music?
- Day 3: Lab: run 9-agent consensus, observe convergence, vary α

**Week 9: Midterm Project**
- Design a constraint system for a 16-bar composition
- Compute the size of the solution space
- Write a 1-page mathematical analysis
- Perform the composition

#### Unit 3: Advanced Topics (Weeks 10–14) — "The Deep Math"

**Week 10: The Eisenstein A₂ Lattice**
- Day 1: Hexagonal close-packing — why this lattice?
- Day 2: `snap()` and covering radius — the geometry of "closest point"
- Day 3: Lab: snap every interval from 0–12 semitones, plot the errors

**Week 11: Holonomy and Cycle Consistency**
- Day 1: What goes around comes around — loops in constraint systems
- Day 2: `verify_consistency()` and `isolate_fault()` — debugging with math
- Day 3: Lab: build a tile system, inject a fault, find it

**Week 12: Deadband Funnels**
- Day 1: Exponential decay ε(t) = ε₀ · e^(−λt) — why this function?
- Day 2: The three phases (FREE → TIGHTENING → LOCKED → ANOMALY)
- Day 3: Lab: sweep λ and observe convergence speed

**Week 13: Composition as Optimization**
- Day 1: Voice leading as shortest-path problem
- Day 2: Neo-Riemannian transformations as graph traversal
- Day 3: Lab: find the shortest PLR path between two triads

**Week 14: The Full Pipeline**
- Day 1: Lattice → Temporal → Rigidity → Metronome → Holonomy
- Day 2: Compose a piece that uses all five modules
- Day 3: Performance + mathematical analysis

#### Unit 4: Synthesis (Weeks 15–18) — "Beyond Music"

**Week 15: Constraints in Other Domains**
- Day 1: Constraints in visual art (color palettes, composition rules)
- Day 2: Constraints in writing (poetic forms, constrained writing like lipograms)
- Day 3: Constraints in game design (rules as constraints)

**Week 16: Final Project Work**
- Students design their own constraint system (in music or another domain)
- Must include mathematical analysis of the constraint space

**Week 17: Presentations**
- 15-minute presentations: demonstrate the system, explain the math, show results

**Week 18: Reflection and Portfolio**
- Written reflection on the course
- Portfolio assembly
- Course evaluation

### Math Concepts Mapped to Constraint Types

| Math Concept | Constraint Type | Connection |
|-------------|----------------|------------|
| **Set theory & subsets** | SNAP | Restricting to a subset of a universal set |
| **Combinatorics** | SNAP + TEMPO | Counting valid sequences under constraints |
| **Sequences & series** | FUNNEL | Boundary conditions, convergence |
| **Modular arithmetic** | SNAP (pitch classes) | Notes as integers mod 12 |
| **Integer partitions** | TEMPO | Filling a bar = partitioning an integer |
| **Graph theory** | All (Laman, Metronome) | Notes as nodes, transitions as edges |
| **Linear algebra** | Rigidity (eigenvalues) | Laplacian matrix, algebraic connectivity |
| **Exponential functions** | Temporal (deadband) | ε(t) = ε₀ · e^(−λt) |
| **Optimization** | Voice leading | Shortest path, minimal distance |
| **Group theory** | Holonomy | Cycle consistency, identity element |
| **Topology** | Holonomy | Loops, covering spaces |
| **Geometry** | Lattice | Closest-point problem, covering radius |
| **Probability/Markov chains** | FUNNEL | Transition probabilities between states |
| **Information theory** | Tightness | Shannon entropy of the constraint set |
| **Proof techniques** | All | Proving properties of constrained systems |

### Could This Be a Full AP-Level Course?

**Almost, but not quite as-is.** Here's my honest assessment:

**What it has going for AP readiness:**
- Deep mathematical content (graph theory, linear algebra, optimization)
- Computationally rigorous (Python library with real algorithms)
- Cross-disciplinary (music + math + CS)
- Project-based assessment potential
- College-level rigor in the advanced exercises

**What it's missing for AP:**
- **No formal proofs.** AP courses require students to construct mathematical arguments. The exercises ask students to *verify* (run the code) but not to *prove* (show why the code works). "Prove that the Laman condition 2n-3 is necessary for rigidity" — that's an AP-level question, and it's absent.
- **No homework problem sets.** AP courses need nightly practice. The workbook has composition exercises but not mathematical problem sets.
- **No exams.** No midterm, no final, no AP-style free-response questions.
- **Insufficient breadth.** The math is deep in a narrow area (lattice geometry + graph theory). An AP course needs to connect to a broader range of mathematical standards.
- **No standards alignment.** No mapping to Common Core, NCTM, or any state standards. This is essential for getting a course approved.

**To make it AP-ready, I'd need:**
1. A problem set for each unit (25–30 problems, mixing computation, proof, and application)
2. Two exams (midterm + final) with AP-style free-response questions
3. Standards alignment document
4. A formal proofs supplement
5. Prerequisites: Algebra II minimum, Precalculus recommended

**My verdict:** This could be the foundation of an *excellent* honors elective or a dual-enrollment course (high school + college credit through a local university). It's not quite AP-ready without the additions above, but it's closer than anything else I've seen.

### Dream: What Would a "Constraint Theory" Textbook Contain?

**Title:** *Constraint Theory: The Mathematics of Productive Limitation*  
**Subtitle:** *From Musical Composition to Distributed Systems*  
**Audience:** Advanced high school / undergraduate

**Part I: Foundations**

**Chapter 1: The Paradox of Constraint**
- Historical examples: sonnet form, haiku, Bach's Art of Fugue, Dogme 95
- Why does constraint enhance creativity? (Psychological evidence)
- Mathematical framing: the solution space of a constrained problem

**Chapter 2: Discrete Sets and Subsets**
- Pitch as integer, octave as equivalence class
- Scales as subsets of Z₁₂
- Combinatorics of constrained sequences
- Exercises: count valid melodies, generate all melodies with k pitches

**Chapter 3: Integer Partitions and Rhythm**
- Rhythmic notation as integer partition
- Generating functions for rhythm patterns
- Euclidean rhythms (Björklund's algorithm)
- Exercises: compute E(k,n) for various parameters

**Chapter 4: Sequences with Constraints**
- Boundary conditions: start/end constraints
- Markov chains for melody generation
- Convergence and stationarity
- Exercises: build and analyze a Markov melody generator

**Part II: Geometry**

**Chapter 5: The Eisenstein A₂ Lattice**
- Hexagonal close-packing and why it matters
- The snap problem: finding the nearest lattice point
- Covering radius and safe thresholds
- Exercises: snap intervals, compute errors, plot the lattice

**Chapter 6: Distance and Voice Leading**
- Metrics on pitch-class space
- Minimal voice leading as shortest path
- The voice-leading orbifold (Callendar, Quinn, Tymoczko)
- Exercises: compute distance matrices, find minimal paths

**Chapter 7: Funnels and Convergence**
- Exponential decay: ε(t) = ε₀ · e^(−λt)
- Phase transitions: FREE → TIGHTENING → LOCKED → ANOMALY
- Stability analysis of the funnel
- Exercises: simulate funnels with varying λ, plot convergence

**Part III: Networks**

**Chapter 8: Graph Theory for Musicians**
- Notes as nodes, transitions as edges
- Degree, connectivity, paths, cycles
- Musical interpretation of graph properties
- Exercises: build melody graphs, compute properties

**Chapter 9: Rigidity — The Laman Condition**
- Rigid vs. flexible structures (physical intuition)
- The 2n-3 rule and Henneberg construction
- Proof sketch: why 2n-3 is necessary
- Exercises: build Laman graphs, test rigidity

**Chapter 10: Consensus and Synchronization**
- The distributed agreement problem
- Laplacian matrices and eigenvalues
- Algebraic connectivity and convergence rate
- Optimal coupling α* = 2/(λ₂ + λₙ)
- Exercises: simulate consensus, compute optimal coupling

**Chapter 11: Holonomy — What Goes Around**
- Cycle consistency in transformation groups
- Holonomy product and identity verification
- Fault isolation via binary bisection
- Exercises: verify consistency, isolate injected faults

**Part IV: Synthesis**

**Chapter 12: The Full Pipeline**
- Lattice → Temporal → Rigidity → Metronome → Holonomy
- Case study: composing a piece with all five modules
- Performance and analysis

**Chapter 13: Beyond Music**
- Constraints in engineering (structural, thermal, electrical)
- Constraints in computer science (type systems, API contracts)
- Constraints in visual art, writing, game design
- The universality of productive limitation

**Chapter 14: Open Problems**
- What makes a "good" constraint? (Aesthetics vs. mathematics)
- Can we quantify creativity within constraints?
- Constraint discovery: finding optimal constraints automatically
- Connections to AI and generative systems

**Appendices**
- A: Python programming introduction (for students new to code)
- B: Music theory crash course (for students new to music)
- C: Mathematical prerequisites review
- D: Complete API reference for `constraint-theory-core`
- E: Solutions to selected exercises
- F: Glossary of terms (music + math + CS)

---

## Summary of Recommendations

### Critical (Must Fix Before Classroom Use)
1. **Provide or remove the Constraint Tarot tool** — it's central to the lesson plan but doesn't exist in the repos
2. **Add a "math mode" to the exercise generator** — strip music jargon, add mathematical objectives
3. **Include prerequisite music theory** — a 2-page crash course for non-music students

### Important (Would Significantly Improve Usability)
4. **Rename TEMPO → GRID/RHYTHM** to avoid confusion with musical tempo
5. **Add mathematical exercises to the workbook** — computation, proof, counting
6. **Create problem sets** — not just composition exercises, but mathematical problem sets with answers
7. **Add a "how to adapt this for math class" section** to the instructor guide
8. **Age up the self-assessment rubric** — replace emoji scale with proficiency language

### Nice to Have (Would Elevate the Product)
9. **Standards alignment document** (Common Core, NCTM)
10. **Jupyter notebook versions** of exercises that students can run and modify
11. **Visualizations** — lattice plots, convergence graphs, Laman graph diagrams
12. **Video demos** of the 50-minute class being taught
13. **Differentiated problem sets** by student math level (Algebra I / Geometry / Algebra II / Precalculus)

---

## Final Thoughts

The core insight — that constraint theory provides a unified mathematical framework for understanding music — is genuinely novel and pedagogically powerful. The `constraint-theory-core` library is solid, well-tested (83 tests!), and the exercise generator is a real tool that real teachers would use.

The education materials (class plan, workbook, rubrics, instructor guide) are thoughtful and detailed — clearly written by someone who understands teaching, not just the subject matter. The differentiation strategies, the coaching table for common student struggles, the pacing tips — these are the marks of an experienced educator.

The gap is in the *bridge*. The materials are written for a music class that happens to use math, not a math class that happens to use music. For my "Math in Music" elective, I need to flip that framing — start with the math, use music as the engaging context, and make the mathematical content explicit at every step.

With a focused "math teacher adaptation pass" — adding computation exercises, stripping jargon, including problem sets, and connecting to math standards — this would be one of the most innovative math curricula I've seen in my career. It's 80% of the way there.

The semester curriculum I've outlined above is what I'd actually teach. And I'd be genuinely excited to teach it.
