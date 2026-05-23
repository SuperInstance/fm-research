#!/usr/bin/env python3
"""
Run All Experiments — orchestrator for the full experimental suite.

Runs all experiments sequentially and generates:
- EXPERIMENT-RESULTS.md — summary of all findings
- figures/ — all plots
- data/ — raw CSVs

Each experiment is also independently runnable.
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Ensure experiments directory is in path
EXPERIMENTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EXPERIMENTS_DIR))


def run_all(output_base: str = None):
    """Run all experiments in sequence."""
    output_base = output_base or str(EXPERIMENTS_DIR / "output")
    os.makedirs(output_base, exist_ok=True)

    results = {}
    start_time = time.time()

    print("=" * 72)
    print("  FM-RESEARCH EXPERIMENTAL SUITE")
    print(f"  Started: {datetime.now().isoformat()}")
    print("=" * 72)
    print()

    experiments = [
        ("epsilon_sweep", "Epsilon Sweep"),
        ("consensus_scaling", "Consensus Scaling"),
        ("genre_boundaries", "Genre Boundaries"),
        ("evolutionary_pressure", "Evolutionary Pressure"),
        ("constraint_interaction", "Constraint Interaction"),
    ]

    for module_name, display_name in experiments:
        print(f"\n{'─' * 72}")
        print(f"  RUNNING: {display_name}")
        print(f"{'─' * 72}\n")

        t0 = time.time()
        try:
            mod = __import__(module_name)
            csv_path, fig_dir = mod.run_experiment(output_dir=os.path.join(output_base, module_name))
            elapsed = time.time() - t0
            results[module_name] = {
                "status": "success",
                "csv_path": csv_path,
                "fig_dir": fig_dir,
                "elapsed": elapsed,
                "error": None,
            }
            print(f"\n  ✓ {display_name} completed in {elapsed:.1f}s")
        except Exception as e:
            elapsed = time.time() - t0
            results[module_name] = {
                "status": "error",
                "csv_path": None,
                "fig_dir": None,
                "elapsed": elapsed,
                "error": str(e),
            }
            print(f"\n  ✗ {display_name} FAILED: {e}")

    total_elapsed = time.time() - start_time

    # Generate summary
    _generate_summary(results, output_base, total_elapsed)

    print(f"\n{'=' * 72}")
    print(f"  ALL EXPERIMENTS COMPLETE")
    print(f"  Total time: {total_elapsed:.1f}s")
    print(f"  Results: {output_base}")
    print(f"{'=' * 72}")

    return results


def _generate_summary(results: dict, output_base: str, total_elapsed: float):
    """Generate EXPERIMENT-RESULTS.md with findings summary."""
    import numpy as np

    md_lines = [
        "# FM-Research Experiment Results",
        "",
        f"_Generated: {datetime.now().isoformat()}_",
        f"_Total runtime: {total_elapsed:.1f}s_",
        "",
        "---",
        "",
    ]

    for module_name, info in results.items():
        display = module_name.replace("_", " ").title()
        md_lines.append(f"## {display}")
        md_lines.append("")
        md_lines.append(f"**Status:** {'✅ Success' if info['status'] == 'success' else '❌ Error'}")
        md_lines.append(f"**Runtime:** {info['elapsed']:.1f}s")

        if info['status'] == 'error':
            md_lines.append(f"**Error:** {info['error']}")
            md_lines.append("")
            continue

        md_lines.append(f"**CSV:** `{info['csv_path']}`")
        md_lines.append(f"**Figures:** `{info['fig_dir']}`")
        md_lines.append("")

        # Read and summarize CSV data
        csv_path = info['csv_path']
        if csv_path and os.path.exists(csv_path):
            try:
                import csv as csv_mod
                with open(csv_path) as f:
                    reader = csv_mod.DictReader(f)
                    rows = list(reader)

                md_lines.append(f"**Data points:** {len(rows)}")
                md_lines.append("")

                # Module-specific summaries
                if module_name == "epsilon_sweep":
                    _summarize_epsilon_sweep(rows, md_lines)
                elif module_name == "consensus_scaling":
                    _summarize_consensus_scaling(rows, md_lines)
                elif module_name == "genre_boundaries":
                    _summarize_genre_boundaries(rows, md_lines)
                elif module_name == "evolutionary_pressure":
                    _summarize_evolutionary(rows, md_lines)
                elif module_name == "constraint_interaction":
                    _summarize_constraint_interaction(rows, md_lines)

            except Exception as e:
                md_lines.append(f"*Error reading results: {e}*")
                md_lines.append("")

        md_lines.append("---")
        md_lines.append("")

    # Write the markdown file
    md_path = os.path.join(output_base, "EXPERIMENT-RESULTS.md")
    with open(md_path, "w") as f:
        f.write("\n".join(md_lines))
    print(f"\nSummary written: {md_path}")


def _summarize_epsilon_sweep(rows, md):
    """Summarize epsilon sweep findings."""
    import numpy as np

    # Find optimal epsilon per genre
    genres = set(r["genre"] for r in rows)
    md.append("### Key Findings")
    md.append("")
    md.append("**Optimal epsilon (peak interest) per genre:**")
    md.append("")

    for genre in sorted(genres):
        genre_rows = [r for r in rows if r["genre"] == genre]
        # Group by epsilon
        from collections import defaultdict
        by_eps = defaultdict(list)
        for r in genre_rows:
            by_eps[r["epsilon"]].append(r)

        best_eps = None
        best_score = -1
        for eps, group in by_eps.items():
            avg_ent = np.mean([float(g["entropy"]) for g in group])
            avg_unique = np.mean([float(g["unique_pitches"]) for g in group])
            score = 0.5 * avg_ent + 0.5 * avg_unique
            if score > best_score:
                best_score = score
                best_eps = eps

        md.append(f"- **{genre}**: optimal ε ≈ {best_eps} (composite score: {best_score:.2f})")

    md.append("")
    md.append("**Inverted-U hypothesis:** The composite interest score should peak at moderate epsilon (~0.2–0.4), confirming the hypothesis that too-tight constraints produce boring music and too-loose constraints produce noise.")
    md.append("")


def _summarize_consensus_scaling(rows, md):
    """Summarize consensus scaling findings."""
    import numpy as np

    voice_counts = sorted(set(int(r["n_voices"]) for r in rows))

    md.append("### Key Findings")
    md.append("")
    md.append("**Scaling behavior:**")
    md.append("")
    md.append("| Voices | Convergence Tick | Final Coherence | Harmonic Coherence |")
    md.append("|--------|-----------------|-----------------|-------------------|")

    for nv in voice_counts:
        subset = [r for r in rows if int(r["n_voices"]) == nv]
        conv = np.mean([float(r["convergence_tick"]) for r in subset])
        coh = np.mean([float(r["final_coherence"]) for r in subset])
        harm = np.mean([float(r["harmonic_coherence"]) for r in subset])
        md.append(f"| {nv} | {conv:.1f} | {coh:.4f} | {harm:.4f} |")

    md.append("")
    md.append("**Laman rigidity hypothesis:** If coherence remains high (>0.9) even at 16 voices, Laman coupling maintains musical coherence at scale.")
    md.append("")


def _summarize_genre_boundaries(rows, md):
    """Summarize genre boundary findings."""
    import numpy as np

    transitions = set((r["genre_a"], r["genre_b"]) for r in rows)

    md.append("### Key Findings")
    md.append("")
    md.append("**Crossover points:**")
    md.append("")

    for ga, gb in sorted(transitions):
        subset = [r for r in rows if r["genre_a"] == ga and r["genre_b"] == gb]
        # Find where scale_conf_a and scale_conf_b cross
        by_t = {}
        for r in subset:
            t = float(r["t"])
            if t not in by_t:
                by_t[t] = {"a": [], "b": []}
            by_t[t]["a"].append(float(r["scale_conf_a"]))
            by_t[t]["b"].append(float(r["scale_conf_b"]))

        ts = sorted(by_t.keys())
        crossover_t = None
        for i in range(len(ts) - 1):
            mean_a1 = np.mean(by_t[ts[i]]["a"])
            mean_b1 = np.mean(by_t[ts[i]]["b"])
            mean_a2 = np.mean(by_t[ts[i+1]]["a"])
            mean_b2 = np.mean(by_t[ts[i+1]]["b"])
            if (mean_a1 - mean_b1) * (mean_a2 - mean_b2) < 0:
                crossover_t = (ts[i] + ts[i+1]) / 2
                break

        if crossover_t is not None:
            md.append(f"- **{ga} → {gb}**: boundary at t ≈ {crossover_t:.2f}")
        else:
            md.append(f"- **{ga} → {gb}**: no clear crossover (one genre dominates)")

    md.append("")
    md.append("**No-genre zones:** Areas where neither genre's scale conformance exceeds 0.6 indicate ambiguous musical territory.")
    md.append("")


def _summarize_evolutionary(rows, md):
    """Summarize evolutionary pressure findings."""
    import numpy as np

    genres = sorted(set(r["genre"] for r in rows))

    md.append("### Key Findings")
    md.append("")
    md.append("**Evolution improvement:**")
    md.append("")

    for genre in genres:
        subset = [r for r in rows if r["genre"] == genre]
        gen0 = [r for r in subset if int(r["generation"]) == 0]
        gen99 = [r for r in subset if int(r["generation"]) == max(int(r2["generation"]) for r2 in subset)]

        if gen0 and gen99:
            fit_start = np.mean([float(r["best_fitness"]) for r in gen0])
            fit_end = np.mean([float(r["best_fitness"]) for r in gen99])
            improvement = (fit_end - fit_start) / max(fit_start, 0.001) * 100
            md.append(f"- **{genre}**: fitness {fit_start:.4f} → {fit_end:.4f} ({improvement:+.1f}% improvement)")

    md.append("")
    md.append("**Real vs overfitting:** Check whether independent quality metrics (entropy, consonance) improve alongside fitness. If fitness rises but independent quality stagnates, the system is overfitting its own fitness function.")
    md.append("")


def _summarize_constraint_interaction(rows, md):
    """Summarize constraint interaction findings."""
    import numpy as np

    md.append("### Key Findings")
    md.append("")
    md.append("**Most surprising combinations (by surprise score):**")
    md.append("")

    # Find top surprise combinations
    combos = {}
    for r in rows:
        key = (r["constraint_a"], r["constraint_b"], float(r["tightness"]))
        if key not in combos:
            combos[key] = []
        combos[key].append(float(r["surprise"]))

    avg_surprise = {k: np.mean(v) for k, v in combos.items()}
    sorted_combos = sorted(avg_surprise.items(), key=lambda x: x[1], reverse=True)

    for (ca, cb, tight), surprise in sorted_combos[:10]:
        md.append(f"- **{ca} × {cb}** (t={tight}): surprise = {surprise:.4f}")

    md.append("")
    md.append("**Emergent properties:** Look for constraint pairs where the combined effect significantly exceeds the average of their individual effects — these are the emergent musical properties.")
    md.append("")


if __name__ == "__main__":
    run_all()
