# GENOME-MUSIC SYNERGY

**Evolving Musical Constraint Profiles via Genetic Expression**

> A genome encodes a constraint profile. Evolution optimizes music by evolving constraint parameters. Same genome, different contexts, different music.

## 1. The Core Idea

flux-genome-py gives us a **fixed genome with adaptive expression** — 25 genes across 5 domains, where the environment determines which genes activate. constraint-theory-core gives us the **mathematical constraint machinery** — Eisenstein snapping, deadband funnels, Laman rigidity, distributed consensus, holonomy verification. flux-tensor-midi gives us the **musical instantiation** — genre brains, room musicians, FluxVectors, Eisenstein rhythm snapping.

The synergy: **repurpose the genome's gene structure to encode musical constraint parameters**, then let evolutionary pressure (fitness evaluation of compositions) drive the genome toward musical styles.

### The Pipeline

```
Genome (25 genes, 5 music domains)
  ↓ Ribosome reads it with musical environment
Transcript Profile (which musical constraint genes activate)
  ↓ Ribosome translates
Constraint Configuration Dict (epsilon, gravity, BPM, grid, thresholds)
  ↓ Pass to flux-tensor-midi / constraint-theory-core
Composition (MIDI output)
  ↓ Evaluate against fitness function
Fitness Score (novelty + constraint satisfaction + genre match)
  ↓ Selection + Mutation
Next Generation
```

## 2. Architecture: Genome → Constraint Profile → Composition

### 2.1 Five Musical Domains

The original genome has 5 engineering domains (maritime, medical, automotive, aerospace, industrial). For music, we remap to 5 constraint types:

| Domain | Constraint Type | Parameters | Musical Meaning |
|--------|----------------|------------|-----------------|
| **Snap** | Eisenstein quantization | grid_resolution, snap_tolerance | How rigidly notes lock to grid |
| **Funnel** | Deadband narrowing | ε₀, λ (decay rate), anomaly threshold | How timing precision tightens over time |
| **Consensus** | Ensemble agreement | coupling α*, consensus threshold | How tightly players synchronize |
| **Laman** | Structural rigidity | edge density, min_edges | Minimum connections between musical voices |
| **Tempo** | Temporal flow | BPM, swing_ratio, rubato_tolerance | The time feel |

### 2.2 Gene → Parameter Mapping

Each of the 25 genes encodes a real-valued parameter via its `structure` array (Eisenstein lattice point). The ribosome maps these to constraint config values:

```python
# Gene structure → constraint parameter
structure = np.array([phi, 1.0, 0.0])  # Eisenstein lattice point

# Extraction: parameter = structure[0] * scale + offset
# The structure IS the DNA; different environments cause different
# expression levels, which modulate the parameter
```

**Expression as modulation:** A gene's expression level (0.0–1.0) modulates its parameter's influence. Strongly expressed genes dominate the constraint profile; weakly expressed ones contribute subtly. This is how the same genome produces jazz in one context and electronic in another.

### 2.3 Musical Environment

The "environment" dict that drives expression now includes musical context:

```python
musical_environment = {
    "domain": "music",
    "genre": "jazz",          # activates jazz-relevant genes
    "ensemble_size": 3,       # affects Laman rigidity
    "rubato": True,           # affects funnel decay rate
    "improvisation": True,    # affects snap tolerance
    "regulatory": False,      # no standards compliance needed
}
```

## 3. Five Domains Mapped to Five Constraint Types

### 3.1 Snap Domain (5 genes)

| Gene | Structure Element | Parameter | Jazz | Electronic | Hip-hop | Classical | Math |
|------|-------------------|-----------|------|------------|---------|-----------|------|
| `snap_resolution` | structure[0] | Grid subdivision (2=8th, 3=triplet, 4=16th, 5=quintuple) | 3 | 4 | 4 | 2 | 5 |
| `snap_tolerance` | structure[1] | How close a note must be to snap (0.0=machine, 1.0=free) | 0.5 | 0.02 | 0.1 | 0.15 | 0.0 |
| `snap_strength` | structure[2] | Pull toward grid (0.0=none, 1.0=full quantize) | 0.4 | 0.98 | 0.9 | 0.7 | 1.0 |
| `snap_phase_offset` | expression_level | Grid phase shift for swing/feel | 0.33 | 0.0 | 0.25 | 0.0 | 0.0 |
| `snap_swing` | protein output | Swing ratio (0.5=straight, 0.67=triplet swing) | 0.67 | 0.5 | 0.6 | 0.5 | 0.5 |

### 3.2 Funnel Domain (5 genes)

| Gene | Parameter | Meaning |
|------|-----------|---------|
| `epsilon_0` | Initial deadband width (ms) | Starting timing tolerance |
| `decay_rate` | λ in ε(t) = ε₀·e^(-λt) | How fast precision tightens |
| `anomaly_threshold` | δ for anomaly detection | When to flag a timing anomaly |
| `reset_rate` | Funnel reset speed | Recovery after anomaly |
| `drift_adaptation` | EWMA α for clock drift | How quickly players adapt |

### 3.3 Consensus Domain (5 genes)

| Gene | Parameter | Meaning |
|------|-----------|---------|
| `coupling_alpha` | Consensus coupling strength | α* = 2/(λ₂ + λₙ) derived from Laman |
| `consensus_threshold` | Agreement tolerance | When players are "in sync" |
| `listen_depth` | How many neighbors to hear | Connectivity in the Laman graph |
| `correct_rate` | Phase correction speed | How fast to pull toward consensus |
| `leader_weight` | Conductor influence | How much the leader drives agreement |

### 3.4 Laman Domain (5 genes)

| Gene | Parameter | Meaning |
|------|-----------|---------|
| `edge_density` | Fraction of possible edges used | How interconnected voices are |
| `min_edges` | Minimum edges (2n-3 = rigid) | Structural rigidity threshold |
| `redundancy` | Extra edges beyond minimal | Fault tolerance in the musical graph |
| `voice_independence` | Autonomy per voice | How independent each musician is |
| `coupling_topology` | Graph structure (star, ring, full) | How musicians listen to each other |

### 3.5 Tempo Domain (5 genes)

| Gene | Parameter | Meaning |
|------|-----------|---------|
| `bpm` | Beats per minute | Base tempo |
| `swing_ratio` | Long-short ratio for swung beats | Groove feel |
| `rubato_extent` | Maximum tempo deviation | Expressive timing range |
| `accel_decel` | Rate of tempo change | How smoothly tempo shifts |
| `groove_depth` | Strength of groove pattern | How locked the rhythm is |

## 4. Evolution Operator

### 4.1 Mutation

The genome's structure arrays are Eisenstein lattice points. Mutation operates on these:

```python
def mutate_genome(genome, mutation_rate=0.1, mutation_scale=0.3):
    """Mutate gene structures — small perturbations on the Eisenstein lattice."""
    for gene_id, gene in genome.genes.items():
        if random.random() < mutation_rate:
            # Perturb structure by a small random vector
            perturbation = np.random.randn(3) * mutation_scale
            gene.structure = gene.structure + perturbation
            
        # Promoter/silencer mutations (rewire regulatory network)
        if random.random() < mutation_rate * 0.3:
            if gene.promoters:
                # Swap a promoter target
                gene.promoters[random.randint(0, len(gene.promoters)-1)] = random.choice(
                    list(genome.genes.keys())
                )
```

### 4.2 Crossover

Two parent genomes produce offspring by exchanging genes:

```python
def crossover(parent_a, parent_b):
    """Single-point crossover on gene ordering."""
    gene_ids = list(parent_a.genes.keys())
    point = random.randint(1, len(gene_ids) - 1)
    
    child = Genome()
    for i, gid in enumerate(gene_ids):
        source = parent_a if i < point else parent_b
        child.add_gene(copy.deepcopy(source.genes[gid]))
    return child
```

### 4.3 Fitness Evaluation

Fitness is a weighted combination of multiple objectives:

```python
def fitness(composition, target_genre):
    w_novelty = 0.25
    w_constraint = 0.25
    w_genre = 0.30
    w_listenability = 0.20
    
    score = (
        w_novelty * novelty_score(composition) +
        w_constraint * constraint_satisfaction(composition) +
        w_genre * genre_match(composition, target_genre) +
        w_listenability * listenability(composition)
    )
    return score
```

## 5. Fitness Functions for Music

### 5.1 Novelty Score
Measures how different the composition is from the population average. Encourages diversity.

- Compare constraint profiles using Euclidean distance in parameter space
- Reward unexpected parameter combinations
- Penalize clones of existing compositions

### 5.2 Constraint Satisfaction
How well the composition obeys its own constraint profile.

- Snap satisfaction: fraction of notes within snap tolerance of grid
- Funnel compliance: timing stays within the deadband funnel
- Consensus achievement: voices agree within threshold
- Laman rigidity: the listening graph is minimally rigid
- Tempo stability: BPM stays within specified range

### 5.3 Genre Match
Distance between the composition's actual parameters and the target genre's ideal profile.

Uses GenreBrain's presets as target vectors:
- Jazz: triplet grid, high rubato, moderate coupling
- Electronic: 16th grid, machine precision, high coupling
- Hip-hop: 16th grid, tight kick, loose hat
- Classical: 8th grid, moderate precision, high voice independence
- Math: quintuple/septuple grid, zero tolerance, exact snap

### 5.4 Listenability
Subjective quality heuristics:

- Rhythmic coherence: consistent pulse perception
- Harmonic balance: not too dissonant, not too simple
- Dynamic range: presence of loud and soft
- Repetition vs variation: enough pattern to follow, enough change to stay interesting

## 6. Example Genomes for Known Musical Styles

### 6.1 Jazz Genome (Bebop)

```python
jazz_environment = {
    "domain": "music",
    "genre": "jazz",
    "rubato": True,
    "improvisation": True,
    "ensemble_size": 3,
}

# Expected expression profile:
# Strongly expressed: snap_tolerance(0.8), rubato_extent(0.9), 
#                     consensus_threshold(0.6), voice_independence(0.8)
# Weakly expressed: snap_strength(0.4), coupling_alpha(0.3)
# Silenced: snap_tolerance for kick (jazz drums are loose)
```

### 6.2 Electronic Genome (Techno)

```python
electronic_environment = {
    "domain": "music",
    "genre": "electronic",
    "rubato": False,
    "improvisation": False,
    "ensemble_size": 3,
}

# Expected expression profile:
# Strongly expressed: snap_strength(0.98), consensus_threshold(0.95),
#                     coupling_alpha(0.9), groove_depth(0.95)
# Weakly expressed: rubato_extent(0.05), voice_independence(0.1)
# Silenced: snap_tolerance (machine precision)
```

### 6.3 Classical Genome

```python
classical_environment = {
    "domain": "music",
    "genre": "classical",
    "rubato": True,
    "improvisation": False,
    "ensemble_size": 3,
}

# Expected expression profile:
# Strongly expressed: consensus_threshold(0.85), voice_independence(0.7),
#                     laman_rigidity(0.9), drift_adaptation(0.95)
# Moderate: snap_tolerance(0.15), rubato_extent(0.3)
```

## 7. Integration Points

### 7.1 From Genome to GenreBrain

The constraint profile produced by the genome feeds directly into `GenreBrain`:

```python
# Traditional: fixed presets
brain = GenreBrain('jazz')

# Evolutionary: genome-derived presets
genome = music_genome()
config = GenomeToConstraints(genome).to_config(genre='jazz')
brain = GenreBrain.from_config(config)  # custom preset from genome
```

### 7.2 From Genome to constraint-theory-core

Constraint parameters map to library modules:

| Genome Parameter | constraint-theory-core Module | Constructor Argument |
|-----------------|------------------------------|---------------------|
| snap_resolution | `lattice.snap()` | (implicit in grid) |
| epsilon_0 | `temporal.TemporalAgent(epsilon_0=...)` | ε₀ |
| decay_rate | `temporal.TemporalAgent(decay_rate=...)` | λ |
| coupling_alpha | `metronome.MetronomeAgent(coupling=...)` | α |
| anomaly_threshold | `temporal.TemporalAgent(anomaly_threshold=...)` | δ |

### 7.3 From Genome to flux-tensor-midi

The composition pipeline:

```python
# 1. Express genome for musical context
incubator = Incubator(music_genome())
result = incubator.express(musical_environment)

# 2. Extract constraint config
config = extract_config(result)

# 3. Create band from evolved constraints
brain = GenreBrain.from_evolved(config)
band, musicians = brain.create_band()

# 4. Render composition
composition = band.render(bars=8)

# 5. Evaluate fitness
score = evaluate_fitness(composition, target='jazz')
```

## 8. Evolutionary Loop

```
Initialize population of N random genomes
    ↓
FOR generation in 1..G:
    ↓
    FOR each genome in population:
        Express → constraint config → composition
        Evaluate fitness against target genre
    ↓
    Select top K genomes (tournament selection)
    ↓
    Crossover parents → offspring
    ↓
    Mutate offspring
    ↓
    Replace population (elitism + offspring)
    ↓
    Log best fitness, diversity metrics
    ↓
RETURN best genome
```

## 9. Why This Works

1. **Genome is fixed, expression is adaptive** — the same 25-gene DNA can produce jazz, electronic, hip-hop, classical, or math rock depending on context. Evolution doesn't change the genome's topology; it tunes the parameters.

2. **Constraint theory is the bridge** — music IS constraints. Snap constrains rhythm, funnels constrain timing, consensus constrains ensemble cohesion, Laman constrains connectivity, tempo constrains flow. The genome encodes constraint parameters.

3. **Fitness drives musical quality** — instead of engineering constraint profiles by hand, we let evolution discover them. The fitness function encodes musical taste.

4. **Promoter/silencer networks add richness** — activating "jazz" promotes rubato genes and silences machine-precision genes. These regulatory interactions create emergent musical behaviors.

5. **Protein degradation = temporal evolution** — proteins have lifetimes and degrade over time. This means a composition's constraint profile evolves during playback, creating dynamic structure.

## 10. Future Directions

- **Multi-genre genomes** that can express convincingly across multiple styles
- **Listener-in-the-loop fitness** — use human preference as fitness signal
- **Cross-species evolution** — mate a jazz genome with an electronic genome
- **Epigenetic marks** — environmental history that affects future expression
- **Protein lifetime = form** — longer-lived proteins create structural sections; short-lived ones create ornamentation
