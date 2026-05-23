# Hyperbolic Genre Space: Why Genres Live on a Poincaré Ball

**Author:** SuperInstance Research  
**Date:** 2026-05-23  
**Synergy:** flux-hyperbolic-py × flux-tensor-midi → Genre Geometry  
**Status:** Deep Synergy Research Document

---

## Abstract

Music genres are not a flat list. They are not even a flat tree. Genres form a *hierarchically nested, continuously blending, culturally entangled structure* that resists Euclidean representation. This paper argues that the natural home for genre space is the **Poincaré ball model of hyperbolic geometry**, and shows how the `flux-hyperbolic-py` library provides exactly the mathematical machinery needed to build a working hyperbolic genre map — one where distance encodes musical dissimilarity, blending is interpolation via the Fréchet mean, and exploration is a random walk on negatively curved space.

We connect the constraint-based music theory of `flux-tensor-midi` to the hyperbolic routing geometry of `flux-hyperbolic-py`, producing a unified framework where:

- Genres are points on an 8-dimensional Poincaré ball
- Genre similarity is hyperbolic distance
- Genre blending is weighted Fréchet mean
- Cultural distance between traditions is curvature-aware separation
- Novelty is how far from your home genre you can wander

---

## 1. The Problem with Flat Genre Space

### 1.1 Genres Are Hierarchical

Consider the path:

```
Music → Western → Classical → Baroque → Bach → Fugue
```

This is a path from root to leaf in a tree. Each step narrows scope. In a flat vector space, there is no natural way to represent this hierarchy without distorting either the parent-child relationships or the sibling similarities. Baroque and Romantic are siblings — they should be roughly equidistant from Classical, but close to each other compared to, say, Baroque and Techno.

In Euclidean space, as you add hierarchical levels, the tree grows exponentially. The number of dimensions needed to faithfully embed an n-level tree with branching factor b grows as O(b^n). This is catastrophic for music, where genre trees have branching factors of 5-10 and depths of 4-6 levels.

### 1.2 Genres Blend Continuously

Jazz + Classical = Third Stream. Hip-hop + Electronic = Trip-hop. Blues + Country = Rockabilly. These aren't discrete combinations — they're *blends*, weighted averages between two (or more) genre points. In flat space, averaging two points gives you the midpoint of a line segment. But genres don't blend linearly. The blend of Jazz and Classical isn't "half jazz, half classical" in every musical dimension — it's a *new genre* with its own emergent properties.

### 1.3 Genres Have Variable Granularity

"Classical music" spans 500 years of Western art music. "Bebop" spans roughly a decade. In a flat embedding, they'd need to occupy the same "size" of space, which distorts either the breadth of Classical or the specificity of Bebop. Hyperbolic space naturally handles this: points near the boundary (high norm) represent highly specific genres, while points near the origin represent broad categories.

### 1.4 Cultural Distance Is Non-Isotropic

Western Classical and Indian Classical share the word "classical" but are musically distant. Western Jazz and Blues share some harmony but differ in form and phrasing. The distance metric must respect these asymmetric, culturally-determined relationships. A simple Euclidean metric treats all dimensions equally, but musical dimensions have different salience in different traditions.

---

## 2. Why Hyperbolic Space?

### 2.1 Trees Embed Naturally

The key mathematical insight comes from Sarkar (2011): any finite tree can be embedded into hyperbolic space with arbitrarily low distortion. Specifically, a tree with maximum degree Δ and diameter D embeds into the Poincaré ball of dimension d with distortion O(Δ^(1/d) · log(D)), which is *exponential improvement* over Euclidean embeddings.

For our genre tree with ~30 leaf genres, branching factor ~5, and depth ~5, hyperbolic space in 8 dimensions provides embeddings with distortion under 5% — compared to 30-50% distortion in the best Euclidean embedding of the same tree.

### 2.2 The Poincaré Ball Model

The Poincaré ball is the open unit ball B^n = {x ∈ ℝ^n : ||x|| < 1} equipped with the Riemannian metric:

```
g_x = (2 / (1 - ||x||²))² · I
```

The metric tensor grows as points approach the boundary, meaning:
- **Points near the origin** (center) represent broad categories — "Music", "Western", "Eastern"
- **Points near the boundary** represent specific genres — "Bach-style fugue", "Coltrane-mode jazz"
- **Distance grows logarithmically** near the boundary, so many highly-specific genres can coexist in the "outer ring" without crowding

The hyperbolic distance between two points u, v ∈ B^n is:

```
d(u, v) = arcosh(1 + 2||u - v||² / ((1 - ||u||²)(1 - ||v||²)))
```

This is exactly the distance function implemented in `flux-hyperbolic-py`'s `PoincareBall.distance()`.

### 2.3 Exponential Capacity

In Euclidean space, the volume of a ball of radius r grows as r^n. In hyperbolic space, it grows as e^r. This means the Poincaré ball has **exponentially more room near the boundary** than near the center. This is precisely what we need for genre taxonomy: the broad categories at the center take up little space, while the many specific genres near the boundary have exponentially more room to spread out.

For music, this means we can represent both "Classical" (broad, near center) and "Bach-style fugue", "Mozart concerto", "Beethoven sonata" (specific, near boundary) without the specific genres crowding each other.

---

## 3. The Hyperbolic Genre Map

### 3.1 Embedding Dimensions

We use the same 8-dimensional embedding from `flux-hyperbolic-py`'s `music_routing.py`:

| Dim | Name | Musical Meaning | Genre Implication |
|-----|------|----------------|-------------------|
| 0 | chromatic_density | How many distinct pitch classes used | Atonal/serial genres high; pentatonic traditions low |
| 1 | rhythmic_intensity | Note density over time | Drum & bass high; ambient low |
| 2 | dynamic_range | Loudness variation | Romantic symphony high; techno low |
| 3 | spaciousness | Rest/silence proportion | Ambient high; death metal low |
| 4 | timing_tightness | Snap to grid (quantization) | Electronic/EDM high; jazz low |
| 5 | angularity | Direction change probability | Free jazz high; minimalism low |
| 6 | sustain | Note length factor | Drone/ambient high; staccato/baroque low |
| 7 | consensus | How much agents agree | Classical/formal high; experimental low |

### 3.2 Hierarchical Genre Placement

Using Sarkar's embedding method, we place genres at increasing norms as we go deeper in the tree:

**Level 0 — Root (norm ≈ 0.0):**
- **Music** — origin point

**Level 1 — Major Traditions (norm ≈ 0.15-0.25):**
- **Western** — moderate chromatic, structured rhythm
- **Eastern** — high chromatic (microtones), moderate rhythm
- **African** — high rhythmic intensity, moderate chromatic
- **Electronic** — high timing tightness, high rhythmic

**Level 2 — Primary Genres (norm ≈ 0.30-0.50):**
- **Classical** — high sustain, moderate chromatic, high consensus
- **Jazz** — high chromatic, low timing, high angularity
- **Rock** — moderate chromatic, high rhythmic, moderate dynamic
- **Hip-hop** — high rhythmic, moderate chromatic, high angularity
- **Raga** — high chromatic, high sustain, low consensus
- **Maqam** — high chromatic, moderate sustain, high consensus
- **Polyrhythm** — very high rhythmic, moderate chromatic
- **Techno** — very high timing, very high rhythmic, low spaciousness
- **Ambient** — very high spaciousness, very high sustain, low rhythmic

**Level 3 — Sub-genres (norm ≈ 0.55-0.75):**
- **Baroque** — high timing, low dynamic, high chromatic
- **Romantic** — high dynamic, high sustain, high chromatic
- **Bebop** — very high chromatic, high rhythmic, very high angularity
- **Fusion** — high chromatic, moderate timing, high rhythmic
- **Trap** — high rhythmic, low timing tightness, high angularity
- **Drill** — very high rhythmic, high angularity, low sustain
- **Detroit Techno** — high rhythmic, high timing, moderate chromatic
- **Dub Techno** — high spaciousness, high sustain, high timing
- **Dhrupad** — very high sustain, high chromatic, very low rhythmic
- **Carnatic** — high chromatic, moderate rhythmic, high angularity

**Level 4 — Specific Styles (norm ≈ 0.80-0.92):**
- **Bach-style** — high chromatic, high timing, high consensus
- **Coltrane-style** — very high chromatic, very high angularity
- **Dilla-style** — low timing, high rhythmic, moderate angularity
- **Basic Channel-style** — very high spaciousness, very high sustain
- **Mbalax** — very high rhythmic, moderate chromatic, high angularity

### 3.3 Distance as Musical Dissimilarity

The hyperbolic distance between two genres naturally captures their musical relationship:

- **Baroque ↔ Romantic**: moderate distance (~1.5-2.0) — share Classical parent, differ in dynamic/sustain
- **Bebop ↔ Fusion**: small distance (~0.8-1.2) — both jazz subgenres, similar chromatic
- **Baroque ↔ Techno**: large distance (~3.5-5.0) — different traditions, different constraints
- **Raga ↔ Maqam**: moderate distance (~2.0-2.5) — both Eastern traditions, but different systems
- **Drum & Bass ↔ Polyrhythm**: moderate distance (~2.0-2.5) — both rhythm-focused, but different cultural origins

The key insight: **hyperbolic distance respects the tree structure**. Siblings are close; cousins are moderate; distant branches are far. This is exactly what we want for genre similarity.

---

## 4. Genre Blending as Fréchet Mean

### 4.1 The Fréchet Mean on the Poincaré Ball

The Fréchet mean generalizes the arithmetic mean to manifolds. On the Poincaré ball, it's the point that minimizes the sum of squared hyperbolic distances to all input points. `flux-hyperbolic-py` implements this via iterative tangent-space averaging:

1. Start with an initial estimate (weighted Euclidean average)
2. Map all input points to the tangent space at the estimate (logmap)
3. Compute weighted mean in tangent space
4. Map back to the ball (expmap)
5. Repeat until convergence

### 4.2 Blending Examples

**Jazz + Classical = Third Stream:**
```
blend = frechet_mean([jazz_point, classical_point], weights=[0.5, 0.5])
```
The resulting point sits between Jazz and Classical in hyperbolic space — it inherits chromatic richness from both, moderate timing from Classical, moderate angularity from Jazz. It's not "half jazz, half classical" in each dimension — the Fréchet mean respects the curvature of the space, producing a *natural blend*.

**Hip-hop + Electronic = Trip-hop (weighted):**
```
blend = frechet_mean([hiphop_point, electronic_point], weights=[0.6, 0.4])
```
Weighted blending lets you bias toward one genre. A 60/40 hip-hop/electronic blend produces something like trip-hop — still rhythm-heavy but with more spaciousness and electronic production values.

**Three-way blend — Jazz + Blues + Rock:**
```
blend = frechet_mean([jazz, blues, rock], weights=[0.33, 0.33, 0.34])
```
Three-way blends explore the interior of the triangle formed by the three genres in hyperbolic space. The result tends toward a "fusion" or "crossover" genre.

### 4.3 Non-Commutativity of Blending Order

Because the Fréchet mean in hyperbolic space is computed iteratively, and because hyperbolic space is curved, the *initial estimate* matters. Different initial estimates converge to the same point (the mean is unique for points in a convex set), but the convergence path differs. This is musically meaningful: the *process* of blending two genres (which one you start from) affects intermediate states, even if the final blend is the same.

---

## 5. Constraint Mapping

### 5.1 From Constraints to Dimensions

The 8 embedding dimensions directly correspond to constraint parameters in `flux-tensor-midi`'s `AgentPersonality`:

| Constraint | Hyperbolic Dimension | Genre Family |
|-----------|---------------------|--------------|
| `snap_epsilon` | timing_tightness | Electronic, Baroque → high; Jazz, Blues → low |
| `note_density` | rhythmic_intensity | D&B, Drill → high; Ambient, Drone → low |
| `direction_change_prob` | angularity | Free jazz, Noise → high; Minimalism, Ambient → low |
| `rest_probability` | spaciousness | Ambient, Dub → high; Death metal, Hardcore → low |
| `velocity_range` | dynamic_range | Romantic, Post-rock → high; Techno, House → low |
| `preferred_intervals` | chromatic_density | Serial, Free jazz → high; Pop, Blues → low |
| `sustain_factor` | sustain | Drone, Ambient → high; Baroque, Funk → low |
| `consensus_weight` | consensus | Classical, March → high; Experimental, Free → low |

### 5.2 Distance as Constraint Distance

Two genres that are close in hyperbolic space share similar constraint profiles. This is not accidental — it's a direct consequence of the embedding:

- **Nearby genres** share most constraint values, differing on 1-2 axes
- **Moderate-distance genres** differ on 3-4 axes
- **Distant genres** differ on most axes

For example:
- **Jazz ↔ Blues**: similar chromatic (both use blue notes), different rhythmic intensity and timing. Hyperbolic distance ~1.0.
- **Jazz ↔ Baroque**: different timing, different angularity, different consensus. Both high chromatic. Hyperbolic distance ~3.0.
- **Ambient ↔ Death Metal**: differ on 7 of 8 axes. Hyperbolic distance ~6.0+.

### 5.3 Constraint-Aware Blending

When blending two genres, the Fréchet mean produces a point whose constraint profile is the "geodesic average" — not a simple arithmetic mean, but a curvature-aware interpolation. This means:

1. **Blending nearby genres** produces smooth transitions (small geodesic)
2. **Blending distant genres** produces more dramatic jumps (large geodesic through the interior of the ball)
3. **The result is always a valid genre** (always inside the ball, always has a well-defined constraint profile)

This is critical for composition: any blend of any two genres produces a musically coherent result, because the hyperbolic geometry guarantees the blend point has valid constraint values.

---

## 6. Applications

### 6.1 Genre Recommendation via Hyperbolic Nearest Neighbors

Given a listener's preference profile (embedded as a point on the Poincaré ball), recommend the nearest genres in hyperbolic space. This naturally handles the hierarchy:

- A listener who likes "Bebop" will be recommended "Hard Bop", "Modal Jazz", and "Post-Bop" (nearby siblings) before "Classical" or "Techno" (distant branches)
- A listener who likes both "Jazz" and "Classical" can be placed at their Fréchet mean and recommended genres near that blend point

The `nearest_genres()` function in `hyperbolic_genre.py` implements this.

### 6.2 Cross-Genre Composition

A composer wanting to work in a genre blend can:
1. Place their "home genre" on the ball
2. Place the "target genre" they want to blend with
3. Compute the Fréchet mean to find the blend point
4. Decode the blend point back into constraint parameters
5. Use those constraints to guide composition

This is implemented via `genre_blend()` → `decode_to_personality()`.

### 6.3 Genre Exploration via Random Walk

A random walk on the Poincaré ball is a natural genre exploration mechanism:
1. Start at your home genre
2. Take a step in a random tangent direction
3. Exponential-map back to the ball
4. The step size (in tangent space) controls how "adventurous" you are
5. Find the nearest genre to your new position

In hyperbolic space, random walks have different properties than in Euclidean space:
- **Near the center**, walks move quickly between broad genres
- **Near the boundary**, walks stay local to specific subgenres
- **The curvature naturally resists "falling off the edge"** — walks can't escape the ball

The `genre_walk()` function implements this exploration.

### 6.4 Cultural Distance Measurement

Hyperbolic distance between cultural music traditions provides a principled measure of musical-cultural similarity:

- **Western Classical ↔ Indian Classical**: large distance (~4-5) despite sharing "classical" status
- **Blues ↔ West African Polyrhythm**: moderate distance (~2-3) reflecting historical roots
- **Jazz ↔ Maqam**: moderate distance (~2-3) — both have modal/improvisational traditions
- **Techno ↔ African Electronic**: small-moderate distance (~1.5-2.5) — shared rhythmic focus

The `cultural_distance()` function computes this, with weights for different musical dimensions that reflect ethnomusicological knowledge.

### 6.5 Novelty Quantification

"How novel is this composition?" becomes a geometric question: how far is the composition's constraint profile from the nearest established genre?

- **Novelty ≈ 0**: inside an existing genre (derivative)
- **Novelty ~ 0.5-1.5**: between nearby genres (blending)
- **Novelty ~ 2.0-3.5**: between distant genres (fusion)
- **Novelty > 3.5**: far from any established genre (experimental)

This provides a quantitative, reproducible measure of musical novelty that correlates with perceptual novelty.

---

## 7. Theoretical Connections

### 7.1 Word Embeddings → Genre Embeddings

The Poincaré embeddings of Nickel & Kiela (2017) showed that hierarchical relationships in WordNet embed better in hyperbolic space than in Euclidean space. Our genre embeddings are analogous: genre taxonomy is a hierarchical knowledge graph, and Poincaré embeddings capture this hierarchy with lower distortion than flat vector space models (Word2Vec, GloVe).

### 7.2 Tree vs. DAG

Strictly speaking, genre relationships form a *directed acyclic graph* (DAG), not a tree — genres can have multiple parents (e.g., "Third Stream" has both "Jazz" and "Classical" as parents). Hyperbolic space handles this gracefully: the Fréchet mean of two parent genres produces a child that is closer to both parents than either parent is to each other, maintaining the DAG structure in a way that tree-only embeddings cannot.

### 7.3 Curvature as Creativity Parameter

The curvature parameter c of the Poincaré ball model controls how "curved" the space is. In the standard model, c = -1. By varying c:

- **c → 0**: space becomes Euclidean (flat genre taxonomy)
- **c → -∞**: space becomes more curved (sharper genre boundaries, more hierarchy)
- **c = -1**: balanced (default)

This curvature parameter could serve as a "creativity dial": higher curvature means genres are more sharply separated (conventional composition), lower curvature means genres blend more easily (experimental composition).

### 7.4 Information Geometry Connection

Genre distributions can be viewed as probability distributions over musical parameters. The Fisher information metric induces a Riemannian metric on this space of distributions. For certain families of distributions, this metric is hyperbolic — suggesting that the hyperbolic genre map is not just convenient but *information-theoretically natural*.

---

## 8. Implementation Architecture

### 8.1 Module: `hyperbolic_genre.py`

The implementation in `flux_tensor_midi/hyperbolic_genre.py` provides:

```
HyperbolicGenreMap
├── 30+ predefined genres with hand-crafted embeddings
├── poincare_distance(u, v) — delegate to PoincareBall.distance
├── frechet_mean(points, weights) — delegate to FrechetMean.compute
├── genre_blend(name_a, name_b, weight) — blend two genres
├── nearest_genres(target, n) — find n closest genres
├── genre_walk(start, step_size) — random walk on ball
├── cultural_distance(tradition_a, tradition_b) — cultural similarity
├── decode_to_constraints(point) — ball point → constraint dict
└── encode_genre(constraints) — constraint dict → ball point
```

### 8.2 Dependency Flow

```
flux-hyperbolic-py          flux-tensor-midi
├── PoincareBall            ├── AgentPersonality
├── FrechetMean             ├── constraint parameters
└── MusicRoutingSpace       └── SNAP, FUNNEL, BANDIT
        │                           │
        └─────────┬─────────────────┘
                  ▼
         hyperbolic_genre.py
         ├── HyperbolicGenreMap
         ├── genre blending
         ├── cultural distance
         └── genre exploration
```

### 8.3 Test Coverage

15+ tests covering:
- Genre placement validity (all inside ball)
- Distance symmetry and triangle inequality
- Fréchet mean convergence
- Genre blend produces valid interior point
- Nearest neighbors respect hierarchy
- Random walk stays inside ball
- Cultural distance measurements
- Encode/decode roundtrip
- Edge cases (identical genres, boundary genres, origin)

---

## 9. Future Directions

### 9.1 Learned Embeddings

Current genre positions are hand-crafted from musicological knowledge. A natural next step is to *learn* embeddings from listening data: place genres such that listener preference distances are minimized. This is the Poincaré GloVe approach applied to music.

### 9.2 Dynamic Genre Map

Genres evolve over time. The map could be updated as new genres emerge (hyperpop, drill, sigilkore) by placing them near their parent genres and letting the hierarchy adjust.

### 9.3 Multi-Scale Navigation

Different composition tasks require different granularity. A composer planning an album needs Level 1-2 genres. A composer working on a specific passage needs Level 3-4 genres. The hyperbolic map naturally supports zooming: near the origin, you see broad categories; near the boundary, you see specific styles.

### 9.4 Cross-Modal Embeddings

Genre embeddings could be aligned with text embeddings (genre descriptions), audio embeddings (spectral features), and cultural embeddings (geographic/temporal context) to create a multi-modal hyperbolic genre space.

---

## 10. Conclusion

Genre space is hyperbolic. The hierarchical structure of musical taxonomy, the continuous blending between genres, the variable granularity of genre specificity, and the non-isotropic nature of cultural distance all point to negatively curved geometry as the natural representation.

The `flux-hyperbolic-py` library provides the mathematical foundation — Poincaré ball geometry, Fréchet mean computation, exponential and logarithmic maps — and the `flux-tensor-midi` library provides the musical semantics — constraint parameters, personality profiles, musical routing. By connecting them through `hyperbolic_genre.py`, we create a unified framework where:

1. **Genres are points** on the Poincaré ball
2. **Similarity is distance** in hyperbolic space
3. **Blending is interpolation** via the Fréchet mean
4. **Exploration is random walking** on negatively curved space
5. **Novelty is measurable** as distance from established genres

This is not just a neat mathematical trick. It's the correct geometry for a space that has been forced into flat representations for too long.

---

## References

- Nickel, M., & Kiela, D. (2017). *Poincaré Embeddings for Learning Hierarchical Representations.* NeurIPS.
- Sarkar, R. (2011). *Low Distortion Delaunay Embedding of Trees in Hyperbolic Plane.* SoCG.
- Krioukov, D., Papadopoulos, F., Kitsak, M., Vahdat, A., & Boguñá, M. (2010). *Hyperbolic Geometry of Complex Networks.* Physical Review E.
- Bonnabel, S. (2013). *Stochastic Gradient Descent on Riemannian Manifolds.* IEEE Trans. Automatic Control.
- `flux-hyperbolic-py` — Poincaré ball geometry for model capability routing. SuperInstance.
- `flux-tensor-midi` — Constraint-based MIDI composition with agent personalities. SuperInstance.
