# FM-Research Experiment Results

_Generated: 2026-05-23T09:19:16.137598_
_Total runtime: 7.6s_

---

## Epsilon Sweep

**Status:** ✅ Success
**Runtime:** 1.8s
**CSV:** `/home/phoenix/.openclaw/workspace/fm-research/experiments/output/epsilon_sweep/epsilon_sweep_results.csv`
**Figures:** `/home/phoenix/.openclaw/workspace/fm-research/experiments/output/epsilon_sweep/figures`

**Data points:** 1000

### Key Findings

**Optimal epsilon (peak interest) per genre:**

- **classical**: optimal ε ≈ 0.5832 (composite score: 12.55)
- **electronic**: optimal ε ≈ 0.6353 (composite score: 16.39)
- **hiphop**: optimal ε ≈ 0.7395 (composite score: 12.54)
- **jazz**: optimal ε ≈ 0.7395 (composite score: 15.04)
- **math**: optimal ε ≈ 0.6353 (composite score: 9.64)

**Inverted-U hypothesis:** The composite interest score should peak at moderate epsilon (~0.2–0.4), confirming the hypothesis that too-tight constraints produce boring music and too-loose constraints produce noise.

---

## Consensus Scaling

**Status:** ✅ Success
**Runtime:** 2.5s
**CSV:** `/home/phoenix/.openclaw/workspace/fm-research/experiments/output/consensus_scaling/consensus_scaling_results.csv`
**Figures:** `/home/phoenix/.openclaw/workspace/fm-research/experiments/output/consensus_scaling/figures`

**Data points:** 160

### Key Findings

**Scaling behavior:**

| Voices | Convergence Tick | Final Coherence | Harmonic Coherence |
|--------|-----------------|-----------------|-------------------|
| 2 | 83.8 | 0.9378 | 0.9184 |
| 3 | 152.0 | 0.8780 | 0.8927 |
| 4 | 200.0 | 0.7461 | 0.9374 |
| 5 | 190.2 | 0.7623 | 0.8871 |
| 6 | 200.0 | 0.7588 | 0.9051 |
| 8 | 200.0 | 0.5895 | 0.9009 |
| 12 | 200.0 | 0.4977 | 0.9083 |
| 16 | 200.0 | 0.3904 | 0.9129 |

**Laman rigidity hypothesis:** If coherence remains high (>0.9) even at 16 voices, Laman coupling maintains musical coherence at scale.

---

## Genre Boundaries

**Status:** ✅ Success
**Runtime:** 1.3s
**CSV:** `/home/phoenix/.openclaw/workspace/fm-research/experiments/output/genre_boundaries/genre_boundaries_results.csv`
**Figures:** `/home/phoenix/.openclaw/workspace/fm-research/experiments/output/genre_boundaries/figures`

**Data points:** 600

### Key Findings

**Crossover points:**

- **classical → math**: no clear crossover (one genre dominates)
- **electronic → classical**: boundary at t ≈ 0.66
- **electronic → hiphop**: boundary at t ≈ 0.03
- **jazz → classical**: boundary at t ≈ 0.08
- **jazz → hiphop**: no clear crossover (one genre dominates)
- **jazz → math**: no clear crossover (one genre dominates)

**No-genre zones:** Areas where neither genre's scale conformance exceeds 0.6 indicate ambiguous musical territory.

---

## Evolutionary Pressure

**Status:** ✅ Success
**Runtime:** 1.2s
**CSV:** `/home/phoenix/.openclaw/workspace/fm-research/experiments/output/evolutionary_pressure/evolution_results.csv`
**Figures:** `/home/phoenix/.openclaw/workspace/fm-research/experiments/output/evolutionary_pressure/figures`

**Data points:** 300

### Key Findings

**Evolution improvement:**

- **classical**: fitness 0.9412 → 0.9960 (+5.8% improvement)
- **electronic**: fitness 0.8815 → 0.9935 (+12.7% improvement)
- **jazz**: fitness 0.8538 → 0.9974 (+16.8% improvement)

**Real vs overfitting:** Check whether independent quality metrics (entropy, consonance) improve alongside fitness. If fitness rises but independent quality stagnates, the system is overfitting its own fitness function.

---

## Constraint Interaction

**Status:** ✅ Success
**Runtime:** 0.9s
**CSV:** `/home/phoenix/.openclaw/workspace/fm-research/experiments/output/constraint_interaction/constraint_interaction_results.csv`
**Figures:** `/home/phoenix/.openclaw/workspace/fm-research/experiments/output/constraint_interaction/figures`

**Data points:** 225

### Key Findings

**Most surprising combinations (by surprise score):**

- **funnel × funnel** (t=0.8): surprise = 0.9462
- **funnel × funnel** (t=0.5): surprise = 0.9329
- **snap × funnel** (t=0.2): surprise = 0.9307
- **snap × funnel** (t=0.8): surprise = 0.9241
- **funnel × dissonance** (t=0.8): surprise = 0.9191
- **snap × snap** (t=0.2): surprise = 0.9159
- **funnel × dissonance** (t=0.5): surprise = 0.9022
- **snap × funnel** (t=0.5): surprise = 0.8858
- **funnel × consensus** (t=0.8): surprise = 0.8832
- **snap × dissonance** (t=0.2): surprise = 0.8733

**Emergent properties:** Look for constraint pairs where the combined effect significantly exceeds the average of their individual effects — these are the emergent musical properties.

---
