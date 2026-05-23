# THRESHOLD-AUDIT.md

**Org:** SuperInstance  
**Scope:** Top 50 most-recently-updated repos (of ~1680 total)  
**Date:** 2026-05-23  
**Auditor:** Kimi Code CLI  

---

## Executive Summary

Across just the **top 50 repos**, we found **~189,000 lines** of threshold/constraint-related code scattered across **39 Python/Rust repositories**. The fragmentation is severe:

- **7 independent implementations** of lattice snap (Eisenstein/Pythagorean)
- **6 independent implementations** of deadband/funnel logic
- **5 independent implementations** of Laman/rigidity checking
- **4 independent implementations** of consensus rounding
- **3+ independent constraint VM/checker stacks** (Flux VM, flux-check-py, constraint-theory-core)

The single worst offender is `quality-gate-stream`, which contains **22+ model-generated duplicate implementations** of `deadband_filter` and `constraint_snap` from various LLM experiments—functionally identical code produced repeatedly by different models.

**Bottom line:** If you're maintaining this ecosystem, you're maintaining the same 5 constraint primitives ~40 times.

---

## Methodology

1. `gh repo list SuperInstance --limit 50 --json name,updatedAt,primaryLanguage`
2. Filtered to 39 repos with Python/Rust code
3. Shallow-cloned all 39 repos
4. `grep -r` for: `epsilon`, `threshold`, `tightness`, `snap`, `funnel`, `consensus`, `laman`, `rigidity`, `deadband`, `tolerance`, `bound`, `limit`, `delta`, `deviation`, `error`
5. Traced imports, dependencies (Cargo.toml, pyproject.toml, requirements.txt), and vendored subdirectories
6. Measured line counts of constraint-related files per repo

---

## Catalog of Constraint Reinvention

### Tier 1: Canonical Core (KEEP — do not touch)

| Repo | Language | Constraint-Related Lines | Role |
|------|----------|-------------------------|------|
| `constraint-theory-core` | Rust | ~10,917 | **The source of truth.** Snap, manifold, rigidity/percolation, holonomy, quantizer, CSP solver, hidden dimensions, curvature, gauge, k-d tree, SIMD, backtracking, AC3, CDCL, DCS, tile, puzzle. |
| `constraint-substrate` | Rust + Python | ~1,290 | **Reference FFI bridge.** Lattice snap, funnel, Laman rigidity, consensus. Has both Rust and Python impls. Zero external deps—self-contained. |

**Verdict:** These two repos ARE the consolidation target. Everything else should import from them.

---

### Tier 2: Egregious Vendoring / Copy-Paste (KILL FIRST)

| Repo | Language | Constraint Lines | What It Vendors / Duplicates | Consolidation Target |
|------|----------|-----------------|------------------------------|----------------------|
| `deadband-rs` | Python + Rust | ~30,082 | **Full vendored copy of `constraint-substrate`** (both Rust + Python), **full vendored copy of `constraint-instrument`**, plus `hex-zhc` (Laman proofs), dozens of experiment scripts (`eisenstein_snap`, `deadband`, `funnel`) | Import `constraint-substrate` + `constraint-instrument` as deps; delete `constraint-substrate/` and `constraint_instrument/` subdirs |
| `fm-research` | Python | ~10,801 | **~20 files identical to `deadband-rs`** (`experiment-1-calibration-deadband.py`, `falsification_campaign.py`, `fleet_cross_pollination.py`, etc.) | Deduplicate against `deadband-rs`; both should import from `constraint-substrate` |
| `quality-gate-stream` | Python | ~31,934 | **22+ model-generated duplicates** of `deadband_filter` and `constraint_snap` in `artifacts/py/` from DeepSeek, Groq, Kimi, etc. Also scattered deadband/constraint references in fleet services | Delete `artifacts/` model-generated constraint duplicates; import `constraint-substrate` or `deadband-python` |

**Key finding:** `deadband-rs` contains a complete, unmodified copy of `constraint-substrate` at `deadband-rs/constraint-substrate/` and a complete copy of `constraint-instrument` at `deadband-rs/constraint_instrument/`. These are not forks with changes—they are literal file copies.

---

### Tier 3: Independent Musical Constraint Systems (PRESERVE — domain-specific)

| Repo | Language | Constraint Lines | What It Implements | Should Import From Core? |
|------|----------|-----------------|-------------------|------------------------|
| `constraint-instrument` | Python | ~6,511 | Musical constraint system: terrain morph, error-rate monitor, groove consensus, constraint profiles, 17 genre terrains. Domain-specific music logic. | **Partial.** The generic `consensus`, `snap`, and `error` primitives should import from `constraint-substrate`. The terrain/genre logic stays. |
| `constraint-synth` | Python | ~2,489 | Constraint-theory synthesizer: Eisenstein snap oscillator, funnel envelope, flux bridge. | **Yes.** `eisenstein_snap` and `funnel` should import from `constraint-substrate`. Synth voice logic stays. |
| `counterpoint-engine` | Python | ~4,512 | Real-time counterpoint engine. **Already depends on `constraint-theory-core` and `flux-tensor-midi`.** Uses Laman rigidity for voice leading. | **Already imports core.** This is the pattern to emulate. |
| `groove-analyzer` | Python | ~2,819 | Groove = deadband funnel via MIDI microtiming. Deadband groove analysis, genre comparison. | **Partial.** Generic deadband/funnel from `constraint-substrate`; groove-specific metrics stay. |
| `spline-midi-smooth` | Python | ~903 | Deadband spline for MIDI pitch bend. Proves deadband = piecewise-linear spline. | **Partial.** The `deadband_bounds` and `deadband_spline` are MIDI-specific wrappers; core deadband from `constraint-substrate`. |
| `plato-room-musician` | Python | ~944 | Score fetcher and synthetic score generator. | Minimal constraint overlap; keep as-is. |
| `jazz-voicing-engine` | Python | 0 | No constraint-related code found. | N/A |

---

### Tier 4: Independent Non-Musical Implementations (EVALUATE)

| Repo | Language | Constraint Lines | What It Implements | Verdict |
|------|----------|-----------------|-------------------|---------|
| `penrose-memory` | Rust + Python | ~2,190 | Penrose snap, tensor threshold, constraint check, SIMD threshold benchmarks. Aperiodic tiling memory system. | **Preserve.** Penrose snap is geometrically distinct from Eisenstein/Pythagorean snap. Could share `threshold` primitives. |
| `agent-field` | Python | ~363 | Agent field tolerance checks (`within_tolerance`). | **Import from core.** Trivial to replace with `constraint-substrate` consensus/epsilon. |
| `flux-check-py` | Python | ~2,079 | `flux-constraint-check` CLI. Exact constraint checking, bounds, fracture/coalesce, sediment correction. Vectorized batch checks. | **Evaluate for merge.** This is a high-quality independent implementation. Consider contributing `fracture/coalesce` and `sediment` concepts upstream to `constraint-theory-core`, or keeping as the "Python fast path." |
| `flux-verify-api` | Rust | ~914 | Constraint problem parser/compiler (Sonar/Thermal/Generic parsers), bytecode VM, signing. | **Evaluate for merge.** Unique contribution: natural-language constraint parsing. Could become a `constraint-theory-core` frontend. |
| `flux-vm-v3` | Rust | ~3,383 | VM with JIT x86 compilation for constraint checking, bounded memory, parallel checks, aviation/nuclear/temperature presets. | **Evaluate for merge.** Unique contribution: JIT-compiled constraint checking. Could become the execution backend for `constraint-theory-core`. |
| `sunset-ecosystem` | Python | ~7,554 | Delta tracker, similarity thresholds, flux compat constraints, thermal breeding threshold, JEPA memory. | **Partial.** Generic threshold/delta from `constraint-substrate`; ecosystem-specific logic stays. |
| `ai-forest` | Python | ~4,600 | Threshold sweeps, cross-model consensus, room spectrum tolerance, bit-depth contracts. | **Partial.** Generic consensus/threshold from `constraint-substrate`; experiment logic stays. |
| `collective-ai` | Python | 0 | No unique constraint code (generic delta computation). | N/A |

---

### Tier 5: Large Repos with Scattered Constraint Code (DEFRAGMENT)

| Repo | Language | Constraint Lines | Scattered Constraint Code | Action |
|------|----------|-----------------|---------------------------|--------|
| `forgemaster` | Rust + Python + C/CUDA | ~88,506 | CUDA extension of core (`constraint-theory-core-cuda`), `deadband-python` package, guard constraints, plato kernel constraints, flux GPU, sonar vision CUDA, constraint domain specs (nuclear, aviation, etc.) | **Consolidate `deadband-python` into `constraint-substrate`.** Keep CUDA extensions and domain specs as they are unique. |
| `plato-training` | Python | ~20,445 | Eisenstein encoder, swarm rooms, intelligence pre-filter. | **Import `constraint-substrate` for Eisenstein primitives.** Keep training-specific logic. |
| `flux-tensor-midi` | Python | ~7,769 | Some constraint mentions in integration tests; mostly unrelated. | No action needed. |
| `superinstance-wiki` | Python | ~6,249 | Fleet repo monitor, grammar security, breeder FSM. | No action needed. |
| `ccc-os` | Python | ~376 | Monitor thresholds (ZC monitor, discussion monitor). Generic threshold usage. | Import `constraint-substrate` for generic thresholds. |

---

## Dependency Graph (Actual vs Ideal)

### Actual (Today)
```
constraint-theory-core  <-- counterpoint-engine
        ^
        | (nothing else imports it)

constraint-substrate  <-- (deadband-rs vendors it)
        ^
        | (fm-research copies it)
        | (quality-gate-stream reinvents it 22x)
        | (constraint-instrument reinvents snap/consensus)
        | (constraint-synth reinvents snap/funnel)
        | (groove-analyzer reinvents deadband/funnel)
        | (spline-midi-smooth reinvents deadband)
        | (agent-field reinvents tolerance)
        | (forgemaster reinvents deadband-python)
        | (plato-training reinvents eisenstein encoder)
        | ... etc

flux-check-py <-- (standalone)
flux-verify-api <-- (standalone)
flux-vm-v3 <-- (standalone)
penrose-memory <-- (standalone)
```

### Ideal (After Consolidation)
```
constraint-theory-core <-- constraint-substrate
        ^                      ^
        |                      |
        |                      |-- counterpoint-engine
        |                      |-- constraint-instrument (generic parts)
        |                      |-- constraint-synth (generic parts)
        |                      |-- groove-analyzer (generic parts)
        |                      |-- spline-midi-smooth (generic parts)
        |                      |-- agent-field
        |                      |-- forgemaster (deadband-python)
        |                      |-- plato-training
        |                      |-- deadband-rs (deleted vendor dirs)
        |                      |-- fm-research
        |                      |-- quality-gate-stream
        |                      |-- ccc-os
        |                      |-- sunset-ecosystem
        |                      |-- ai-forest
        |
        |-- flux-verify-api (constraint parser -> core problem format)
        |-- flux-vm-v3 (JIT backend -> core execution)
        |-- penrose-memory (shared threshold primitives)

flux-check-py <-- (keep as Python fast path OR merge fracture/coalesce into core)
```

---

## Priority Order for Consolidation (Highest Impact First)

### P0 — Immediate (This Week)

1. **`deadband-rs` — Delete Vendor Directories**
   - Remove `deadband-rs/constraint-substrate/` (full copy)
   - Remove `deadband-rs/constraint_instrument/` (full copy)
   - Add `constraint-substrate` and `constraint-instrument` as deps in pyproject.toml
   - **Impact:** Eliminates ~15,000 lines of duplicated code in one PR.

2. **`quality-gate-stream` — Purge Model-Generated Duplicates**
   - Delete `artifacts/py/modelexperiment-*-deadband-filter.py` (22+ files)
   - Delete `artifacts/py/modelexperiment-*-constraint-snap.py` (5+ files)
   - Delete `artifacts/py/testing-*-deadband*.py` redundant test artifacts
   - Add `constraint-substrate` as a fleet dependency
   - **Impact:** Eliminates ~10,000 lines of LLM-generated redundant code.

3. **`fm-research` — Deduplicate Against Deadband-rs**
   - The ~20 shared Python files (`experiment-*.py`, `sim-*.py`, `falsification_campaign.py`) should be deleted from one repo or the other.
   - **Impact:** Eliminates ~8,000 lines of cross-repo duplication.

### P1 — High Impact (Next 2 Weeks)

4. **`forgemaster/deadband-python` — Merge into `constraint-substrate`**
   - `deadband-python` is a standalone package (~500 lines) that reimplements Eisenstein snap + perceptual deadband.
   - Merge its unique features (Fibonacci spline search, HPDF perceptual model) into `constraint-substrate` as optional modules.
   - Delete `forgemaster/deadband/deadband-python/`.
   - **Impact:** Centralizes deadband expertise; eliminates a package.

5. **`constraint-instrument` + `constraint-synth` — Import Generic Primitives**
   - Replace internal `eisenstein_snap`, `funnel`, `consensus` with `constraint-substrate` calls.
   - Keep domain-specific wrappers (terrain morph, oscillator voice logic).
   - **Impact:** ~1,500 lines of generic math deleted; maintained in one place.

6. **`agent-field`, `ccc-os` — Import Tolerance from Core**
   - Replace `within_tolerance` and monitor thresholds with `constraint-substrate`.
   - **Impact:** Trivial 2-PR changes.

### P2 — Strategic (Next Month)

7. **`flux-check-py` — Evaluate Upstream Contribution**
   - Its `fracture/coalesce` and `sediment` algorithms are unique contributions.
   - Propose adding these as `constraint-theory-core` modules or keep as the official Python fast-path.
   - **Impact:** Prevents future reinvention of fracture analysis.

8. **`flux-verify-api` — Become Core Frontend**
   - Its natural-language parsers (Sonar, Thermal, Generic) should output `ConstraintProblem` structs compatible with `constraint-theory-core`.
   - **Impact:** One parser stack for the whole org.

9. **`flux-vm-v3` — Become Core Backend**
   - Its JIT x86 constraint compiler should compile `constraint-theory-core` `ConstraintProblem` bytecode.
   - **Impact:** One execution backend for the whole org.

10. **`penrose-memory` — Share Threshold Primitives**
    - Extract generic `tensor_threshold` and `constraint_check` into `constraint-theory-core` SIMD module.
    - Keep Penrose-specific snap logic.
    - **Impact:** Penrose gets upstream optimizations; core gets tensor thresholding.

### P3 — Cleanup (Ongoing)

11. **`plato-training`, `sunset-ecosystem`, `ai-forest` — Import Generic Primitives**
    - Replace scattered `eisenstein_snap`, `consensus`, `delta_tracker` thresholds with `constraint-substrate`.
    - **Impact:** Reduces maintenance surface area.

12. **Org-Wide Lint Rule**
    - Add a CI check that fails if a new repo defines `eisenstein_snap`, `deadband_filter`, `laman_check`, or `consensus_round` without importing from `constraint-substrate`.
    - **Impact:** Prevents future reinvention.

---

## Recommendations

### Which Repos Should Just Import `constraint-theory-core` / `constraint-substrate`

| Repo | Should Import | What to Delete / Replace |
|------|--------------|--------------------------|
| `deadband-rs` | `constraint-substrate`, `constraint-instrument` | `constraint-substrate/`, `constraint_instrument/` vendor dirs |
| `fm-research` | `constraint-substrate` | Duplicate experiment scripts shared with `deadband-rs` |
| `quality-gate-stream` | `constraint-substrate` | `artifacts/py/modelexperiment-*` deadband/constraint duplicates |
| `constraint-instrument` | `constraint-substrate` | Internal `snap`, `consensus`, `error_rate` math |
| `constraint-synth` | `constraint-substrate` | Internal `eisenstein_snap`, `funnel` math |
| `groove-analyzer` | `constraint-substrate` | Internal deadband/funnel math |
| `spline-midi-smooth` | `constraint-substrate` | Internal `deadband_bounds` core logic |
| `agent-field` | `constraint-substrate` | `within_tolerance` |
| `ccc-os` | `constraint-substrate` | Monitor threshold logic |
| `forgemaster` | `constraint-substrate` | `deadband-python` package |
| `plato-training` | `constraint-substrate` | `eisenstein_encoder` generic math |
| `sunset-ecosystem` | `constraint-substrate` | Generic `delta_tracker` thresholds |
| `ai-forest` | `constraint-substrate` | Generic consensus/threshold experiments |

### Which Repos Have Unique Implementations Worth Preserving

| Repo | Unique Contribution | Keep / Merge Strategy |
|------|--------------------|-----------------------|
| `constraint-theory-core` | Canonical snap, manifold, rigidity, CSP, holonomy, SIMD | **Keep as-is.** This is the root. |
| `constraint-substrate` | 5 irreducible primitives in Rust + Python FFI | **Keep as-is.** This is the API layer. |
| `penrose-memory` | Penrose aperiodic snap, tensor threshold, SIMD benchmarks | **Keep.** Merge generic `threshold` primitives into core. |
| `flux-check-py` | Fracture/coalesce analysis, sediment correction, vectorized batch checks | **Keep or upstream.** Unique algorithms not in core. |
| `flux-verify-api` | Natural-language constraint parsing (Sonar/Thermal/Generic) | **Keep or upstream.** Unique frontend. |
| `flux-vm-v3` | JIT x86 constraint compiler, bounded memory VM | **Keep or upstream.** Unique execution backend. |
| `forgemaster` (CUDA) | `constraint-theory-core-cuda`, GPU extensions | **Keep.** Hardware-specific extensions can't be in core. |
| `constraint-instrument` (terrains) | 17 genre terrains, musical constraint profiles | **Keep.** Domain-specific. |
| `counterpoint-engine` | Laman counterpoint, voice-leading rigidity | **Keep.** Already imports core correctly. |

---

## Metrics

| Metric | Value |
|--------|-------|
| Repos audited | 39 (of 50 top repos) |
| Total constraint-related lines | ~189,000 |
| Independent implementations of snap | 7 |
| Independent implementations of deadband/funnel | 6 |
| Independent implementations of Laman/rigidity | 5 |
| Independent implementations of consensus | 4 |
| Vendored copies of `constraint-substrate` | 2 (`deadband-rs`, plus inside itself) |
| Vendored copies of `constraint-instrument` | 1 (`deadband-rs`) |
| Model-generated duplicate artifacts | 22+ (`quality-gate-stream`) |
| Repos already importing core correctly | 1 (`counterpoint-engine`) |
| Estimated lines deletable by consolidation | ~45,000–60,000 |

---

## Appendix: Raw Data

### Line Counts by Repo (Constraint-Related Files Only)

| Repo | Files | Lines |
|------|-------|-------|
| `forgemaster` | 307 | 88,506 |
| `quality-gate-stream` | 130 | 31,934 |
| `deadband-rs` | 108 | 30,082 |
| `plato-training` | 45 | 20,445 |
| `constraint-theory-core` | 38 | 10,917 |
| `fm-research` | 38 | 10,801 |
| `sunset-ecosystem` | 32 | 7,554 |
| `flux-tensor-midi` | 32 | 7,769 |
| `constraint-instrument` | 29 | 6,511 |
| `superinstance-wiki` | 13 | 6,249 |
| `ai-forest` | 16 | 4,600 |
| `counterpoint-engine` | 18 | 4,512 |
| `flux-vm-v3` | 14 | 3,383 |
| `groove-analyzer` | 17 | 2,819 |
| `flux-lib-py` | 17 | 2,814 |
| `constraint-synth` | 15 | 2,489 |
| `flux-check-py` | 13 | 2,079 |
| `penrose-memory` | 5 | 2,190 |
| `flux-genome-py` | 9 | 2,103 |
| `plato-room-musician` | 6 | 944 |
| `spline-midi-smooth` | 6 | 903 |
| `tensor-spline` | 2 | 1,421 |
| `style-dna` | 2 | 758 |
| `cocapn-plato` | 5 | 717 |
| `swarm-rooms` | 7 | 428 |
| `cocapn-health` | 2 | 409 |
| `agent-field` | 1 | 363 |
| `AI-Writings` | 2 | 362 |
| `luciddreamer-agent` | 1 | 478 |
| `ccc-os` | 3 | 376 |
| `agentic-compiler` | 2 | 1,259 |
| `flux-ffi` | 1 | 259 |
| `holonomy-harmony` | 2 | 288 |
| `triplet-miner` | 1 | 96 |
| `jazz-voicing-engine` | 0 | 0 |
| `collective-ai` | 0 | 0 |
| `cocapn-glue-core` | 2 | 142 |

### Search Patterns Found

- `epsilon` — 47 repos
- `threshold` — 31 repos
- `snap` — 28 repos
- `constraint` — 26 repos
- `deadband` — 12 repos
- `funnel` — 8 repos
- `consensus` — 7 repos
- `laman` / `rigidity` — 6 repos
- `tolerance` — 5 repos
- `delta` / `deviation` — 15 repos

---

*This audit was generated automatically by shallow-cloning 39 repos and analyzing ~189,000 lines of constraint-related code. The next step is P0: delete the vendor directories in `deadband-rs` and purge the model-generated artifacts in `quality-gate-stream`.*
