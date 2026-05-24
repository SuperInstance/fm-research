"""
================================================================================
THE HARMONIC CONVECTION EXPERIMENT
================================================================================
A vectorized NumPy exploration of 4096 coupled Lorenz systems where the
control parameter ρ adapts in real-time based on emergent harmonic fields.

NOVELTY:
- ρ is not static; it evolves via gradient ascent on local consonance
- Wing-dependent modality: left wing (x>0) → A# major, right wing (x<0) → F minor
- Structure Function and Complexity-Entropy guide global ρ biasing
- Call-and-response dialogue index measured between wings in real-time
- Tonality strength tracks emergence of A# major across the ensemble

MUSICAL MAPPING:
- Trajectory angle in x-y plane → pitch class on circle of fifths
- z-height → octave register and dynamic weight
- Wing identity → modality (major/minor)
- ρ value → "temperature" of the musical agent (CE peak at 15, SF peak at 24)

METRICS COMPUTED:
- Total Consonance, Call Consonance, Response Consonance, Dialogue Index
- Structure Function (lag-5 mean squared displacement)
- Complexity-Entropy (Bandt-Pompe ordinal patterns on pitch classes)
- Tonality Strength (ensemble clustering around A# major)
- Wing Balance (left/right population ratio)
- ρ Distribution moments and flow
================================================================================
"""

import numpy as np
from pathlib import Path
import json
from datetime import datetime
import time

# ==============================================================================
# CONFIGURATION
# ==============================================================================
N_SYSTEMS = 4096
N_STEPS = 100_000
DT = 0.01
SAVE_EVERY = 100

SIGMA = 10.0
BETA = 8.0 / 3.0
RHO_MIN, RHO_MAX = 10.0, 35.0

# Musical constants
AS_SHARP_PC = 10          # A# = 10 in chromatic [0-11]
F_MINOR_PC = 5            # F minor relative to A# major
N_BINS_RHO = 32           # For local harmonic field computation
WINDOW_MEM = 50           # Memory buffer for running metrics

# Interval consonance weights (just intonation / psychoacoustic)
# Index = interval class [0..11]: unison, m2, M2, m3, M3, P4, TT, P5, m6, M6, m7, M7
INTERVAL_WEIGHTS = np.array([
    1.00,  # P1 (unison)
    0.08,  # m2 (highly dissonant)
    0.25,  # M2 (dissonant)
    0.82,  # m3 (consonant)
    0.88,  # M3 (major consonance)
    0.60,  # P4 (imperfect)
    0.05,  # TT (tritone, most tense)
    0.95,  # P5 (perfect consonance)
    0.72,  # m6 (medium consonance)
    0.78,  # M6 (medium-major consonance)
    0.20,  # m7 (dissonant)
    0.15,  # M7 (leading tone tension)
], dtype=np.float64)

# Pre-compute consonance matrix: C[i,j] = weight[interval_class(i,j)]
CHROMATIC = np.arange(12)
INTERVAL_CLASS = np.minimum(
    np.abs(CHROMATIC[:, None] - CHROMATIC[None, :]),
    12 - np.abs(CHROMATIC[:, None] - CHROMATIC[None, :])
)
CONSONANCE_MATRIX = INTERVAL_WEIGHTS[INTERVAL_CLASS]

# ==============================================================================
# LORENZ DYNAMICS (Vectorized RK4)
# ==============================================================================
def lorenz_deriv(X, Y, Z, rhos):
    """Return derivatives for all systems."""
    dX = SIGMA * (Y - X)
    dY = X * (rhos - Z) - Y
    dZ = X * Y - BETA * Z
    return dX, dY, dZ


def rk4_step(X, Y, Z, rhos, dt):
    """Vectorized RK4 integration step."""
    k1x, k1y, k1z = lorenz_deriv(X, Y, Z, rhos)
    k2x, k2y, k2z = lorenz_deriv(
        X + 0.5 * dt * k1x, Y + 0.5 * dt * k1y, Z + 0.5 * dt * k1z, rhos
    )
    k3x, k3y, k3z = lorenz_deriv(
        X + 0.5 * dt * k2x, Y + 0.5 * dt * k2y, Z + 0.5 * dt * k2z, rhos
    )
    k4x, k4y, k4z = lorenz_deriv(
        X + dt * k3x, Y + dt * k3y, Z + dt * k3z, rhos
    )
    X_new = X + (dt / 6.0) * (k1x + 2 * k2x + 2 * k3x + k4x)
    Y_new = Y + (dt / 6.0) * (k1y + 2 * k2y + 2 * k3y + k4y)
    Z_new = Z + (dt / 6.0) * (k1z + 2 * k2z + 2 * k3z + k4z)
    return X_new, Y_new, Z_new


# ==============================================================================
# MUSICAL PROJECTION
# ==============================================================================
def trajectory_to_pitch_class(X, Y, Z):
    """
    Map Lorenz trajectory to chromatic pitch class [0, 12).
    Uses the azimuthal angle in x-y plane, modulated by z-height.
    This creates orbiting pitch-class trajectories that naturally
    explore the circle of fifths as the attractor switches lobes.
    """
    theta = np.arctan2(Y, X)
    z_norm = (Z - 25.0) / 15.0
    angle = theta + 0.25 * z_norm
    pc = ((angle + np.pi) / (2.0 * np.pi) * 12.0) % 12.0
    return pc


def compute_harmonic_consonance(pcs, weights=None):
    """
    Compute expected consonance of a pitch-class collection.
    Uses the histogram method: E[C] = sum_{i,j} p(i) p(j) C[i,j]
    This is O(12^2) regardless of ensemble size.
    """
    if weights is None:
        weights = np.ones_like(pcs)
    # Weighted histogram
    hist = np.bincount(np.floor(pcs).astype(int) % 12, weights=weights, minlength=12)
    total = hist.sum()
    if total < 1e-12:
        return 0.0
    p = hist / total
    return float(p @ CONSONANCE_MATRIX @ p)


# ==============================================================================
# METRICS
# ==============================================================================
def structure_function(X_hist, lag=5):
    """Mean squared displacement at lag across the ensemble."""
    if X_hist.shape[0] <= lag:
        return 0.0
    return float(np.mean((X_hist[lag:] - X_hist[:-lag]) ** 2))


def complexity_entropy_ordinal(pcs, order=3):
    """
    Bandt-Pompe complexity-entropy on pitch class sequence.
    Uses ordinal patterns in sliding windows of size `order`.
    """
    n = len(pcs)
    if n < order + 1:
        return 0.0, 1.0
    # Sliding windows
    windows = np.lib.stride_tricks.sliding_window_view(pcs, order)
    # Ordinal pattern for each window (argsort of argsort)
    ranks = np.argsort(np.argsort(windows, axis=1), axis=1)
    # Pattern ID in base `order`
    bases = order ** np.arange(order, dtype=np.int64)
    pattern_ids = np.dot(ranks, bases)
    # Histogram
    n_patterns = order ** order
    hist = np.bincount(pattern_ids, minlength=n_patterns)
    p = hist / hist.sum()
    p = p[p > 0]
    max_ent = np.log2(n_patterns)
    entropy = -np.sum(p * np.log2(p)) / max_ent  # normalized [0,1]
    # Complexity = disequilibrium * entropy
    uniform = 1.0 / n_patterns
    disequilibrium = np.sum((p - uniform) ** 2)
    complexity = disequilibrium * entropy
    return float(complexity), float(entropy)


# ==============================================================================
# ADAPTIVE HARMONIC FIELD
# ==============================================================================
def compute_rho_binned_consonance(rhos, pcs, n_bins=N_BINS_RHO):
    """
    Compute local consonance in ρ-bins.
    Returns: bin_consonance array [n_bins], bin_centers [n_bins], bin_counts [n_bins]
    """
    bin_edges = np.linspace(RHO_MIN, RHO_MAX, n_bins + 1)
    bin_idx = np.clip(np.digitize(rhos, bin_edges) - 1, 0, n_bins - 1)

    bin_consonance = np.zeros(n_bins)
    bin_counts = np.zeros(n_bins, dtype=np.int64)

    for b in range(n_bins):
        mask = bin_idx == b
        count = mask.sum()
        bin_counts[b] = count
        if count > 0:
            bin_consonance[b] = compute_harmonic_consonance(pcs[mask])
        else:
            # Empty bins get interpolated later
            bin_consonance[b] = np.nan

    # Fill empty bins via forward/backward fill
    mask_valid = ~np.isnan(bin_consonance)
    if mask_valid.any():
        bin_consonance = np.interp(
            np.arange(n_bins),
            np.arange(n_bins)[mask_valid],
            bin_consonance[mask_valid],
        )
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
    return bin_consonance, bin_centers, bin_counts


def adapt_rhos(rhos, pcs, tonality_strength, step_num):
    """
    Adapt ρ values based on local harmonic field and global state.

    Two forces act on each ρ:
    1. LOCAL: Gradient ascent on binned consonance (systems move toward
       ρ-regions that produce more consonant pitch collections)
    2. GLOBAL: State-dependent pull toward known metric peaks
       - High tonality → pull toward SF peak (ρ=24, structure/order)
       - Low tonality → pull toward CE peak (ρ=15, complexity/entropy)

    Plus small thermal noise to prevent collapse.
    """
    # --- Local consonance gradient ---
    bin_consonance, bin_centers, bin_counts = compute_rho_binned_consonance(rhos, pcs)
    # Smooth the consonance profile
    kernel = np.array([0.25, 0.5, 0.25])
    bin_consonance = np.convolve(bin_consonance, kernel, mode="same")
    # Gradient in bin space
    dc_dbin = np.gradient(bin_consonance)
    # Map each system's ρ to a bin and read the gradient
    bin_edges = np.linspace(RHO_MIN, RHO_MAX, N_BINS_RHO + 1)
    bin_idx = np.clip(np.digitize(rhos, bin_edges) - 1, 0, N_BINS_RHO - 1)
    local_gradient = dc_dbin[bin_idx]
    # Scale gradient by bin width to get physical ρ-shift direction
    bin_width = (RHO_MAX - RHO_MIN) / N_BINS_RHO
    local_shift = 0.008 * local_gradient * bin_width

    # --- Global state-dependent pull ---
    if tonality_strength > 0.30:
        # Ensemble is tonal: seek structure (SF peak)
        global_target = 24.0
    elif tonality_strength > 0.15:
        # Transitional: seek the complexity-entropy peak
        global_target = 15.0
    else:
        # Atonal: explore the middle ground
        global_target = 19.5

    global_pull = 0.0003 * (global_target - rhos)

    # --- Thermal noise (decreases over time = simulated annealing) ---
    noise_amp = 0.005 / (1.0 + step_num / 5000.0)
    thermal = noise_amp * np.random.randn(N_SYSTEMS)

    # Apply adaptation
    rhos_new = rhos + local_shift + global_pull + thermal
    return np.clip(rhos_new, RHO_MIN, RHO_MAX)


# ==============================================================================
# MAIN EXPERIMENT
# ==============================================================================
def run_experiment():
    print("=" * 72)
    print("THE HARMONIC CONVECTION EXPERIMENT")
    print("=" * 72)
    print(f"Ensemble size:    {N_SYSTEMS}")
    print(f"Integration steps: {N_STEPS}")
    print(f"Time step:        {DT}")
    print(f"Total simulation time: {N_STEPS * DT:.1f} Lorenz time units")
    print(f"ρ range:          [{RHO_MIN}, {RHO_MAX}]")
    print(f"Metric peaks:     CE→ρ=15,  SF→ρ=24")
    print(f"Target tonality:  A# major (pc={AS_SHARP_PC})")
    print("=" * 72)

    # --- Initialize state ---
    np.random.seed(0x5F3759DF)
    # Bimodal ρ distribution around the two metric peaks
    rhos = np.concatenate([
        np.random.normal(15.0, 2.5, N_SYSTEMS // 2),
        np.random.normal(24.0, 2.5, N_SYSTEMS - N_SYSTEMS // 2),
    ])
    rhos = np.clip(rhos, RHO_MIN, RHO_MAX)

    # Scatter initial conditions near the attractor
    X = np.random.randn(N_SYSTEMS) * 8.0
    Y = np.random.randn(N_SYSTEMS) * 8.0
    Z = np.random.randn(N_SYSTEMS) * 9.0 + 27.0

    # --- Buffers ---
    N_SAVE = N_STEPS // SAVE_EVERY
    state_hist = np.zeros((N_SAVE, N_SYSTEMS, 3), dtype=np.float32)
    rho_hist = np.zeros((N_SAVE, N_SYSTEMS), dtype=np.float32)
    pc_hist = np.zeros((N_SAVE, N_SYSTEMS), dtype=np.float32)

    metrics = {
        "step": [],
        "time": [],
        "mean_rho": [],
        "std_rho": [],
        "skew_rho": [],
        "total_consonance": [],
        "call_consonance": [],
        "response_consonance": [],
        "dialogue_index": [],
        "structure_function": [],
        "complexity": [],
        "entropy": [],
        "tonality_strength": [],
        "wing_balance": [],
        "mean_z": [],
        "z_variance": [],
    }

    # Circular buffers for running metrics
    recent_X = np.zeros((WINDOW_MEM, N_SYSTEMS), dtype=np.float64)
    recent_pcs = np.zeros((WINDOW_MEM, N_SYSTEMS), dtype=np.float64)
    buf_idx = 0

    t0 = time.time()

    for step in range(N_STEPS):
        # --- Integrate ---
        X, Y, Z = rk4_step(X, Y, Z, rhos, DT)

        # --- Musical projection ---
        pcs = trajectory_to_pitch_class(X, Y, Z)
        wing_mask = X > 0  # True = left wing (call)

        # --- Update circular buffers ---
        recent_X[buf_idx % WINDOW_MEM] = X
        recent_pcs[buf_idx % WINDOW_MEM] = pcs
        buf_idx += 1

        # --- Analysis & adaptation ---
        if step % SAVE_EVERY == 0:
            s = step // SAVE_EVERY
            state_hist[s, :, 0] = X.astype(np.float32)
            state_hist[s, :, 1] = Y.astype(np.float32)
            state_hist[s, :, 2] = Z.astype(np.float32)
            rho_hist[s, :] = rhos.astype(np.float32)
            pc_hist[s, :] = pcs.astype(np.float32)

            # Split by wing for call-and-response analysis
            left_pcs = pcs[wing_mask]
            right_pcs = pcs[~wing_mask]

            call_c = (
                compute_harmonic_consonance(left_pcs)
                if len(left_pcs) > 0 else 0.0
            )
            response_c = (
                compute_harmonic_consonance(right_pcs)
                if len(right_pcs) > 0 else 0.0
            )

            # Dialogue = cross-wing consonance (sample pairs)
            if len(left_pcs) > 0 and len(right_pcs) > 0:
                # Subsample for speed if populations are large
                max_sample = 256
                if len(left_pcs) > max_sample:
                    left_samp = np.random.choice(left_pcs, max_sample, replace=False)
                else:
                    left_samp = left_pcs
                if len(right_pcs) > max_sample:
                    right_samp = np.random.choice(right_pcs, max_sample, replace=False)
                else:
                    right_samp = right_pcs
                # Expected cross-consonance via histogram product
                h_left = np.bincount(np.floor(left_samp).astype(int) % 12, minlength=12)
                h_right = np.bincount(np.floor(right_samp).astype(int) % 12, minlength=12)
                h_left = h_left / h_left.sum()
                h_right = h_right / h_right.sum()
                dialogue_c = float(h_left @ CONSONANCE_MATRIX @ h_right)
            else:
                dialogue_c = 0.0

            total_c = 0.3 * call_c + 0.3 * response_c + 0.4 * dialogue_c
            dialogue_idx = dialogue_c - 0.5 * (call_c + response_c)

            # Structure function on recent history
            valid_mem = min(buf_idx, WINDOW_MEM)
            sf = structure_function(recent_X[:valid_mem], lag=5)

            # Complexity-entropy on recent pitch classes
            flat_pcs = recent_pcs[:valid_mem].flatten()
            comp, ent = complexity_entropy_ordinal(flat_pcs, order=3)

            # Tonality strength: how close is ensemble to A# major scale?
            # A# major scale (approximate chromatic): A#(10), C(0), D(2), D#(3), F(5), G(7), A(9)
            scale_pcs = np.array([10, 0, 2, 3, 5, 7, 9], dtype=np.float64)
            # For each pitch class, distance to nearest scale degree
            expanded = np.abs(pcs[:, None] - scale_pcs[None, :]) % 12
            min_dist = np.minimum(expanded, 12 - expanded).min(axis=1)
            tonality = float(np.exp(-min_dist.mean() / 1.5))

            # Wing balance
            wing_balance = float(wing_mask.sum()) / N_SYSTEMS

            # Record metrics
            metrics["step"].append(int(step))
            metrics["time"].append(float(step * DT))
            metrics["mean_rho"].append(float(rhos.mean()))
            metrics["std_rho"].append(float(rhos.std()))
            metrics["skew_rho"].append(float((((rhos - rhos.mean()) / (rhos.std() + 1e-12)) ** 3).mean()))
            metrics["total_consonance"].append(total_c)
            metrics["call_consonance"].append(call_c)
            metrics["response_consonance"].append(response_c)
            metrics["dialogue_index"].append(dialogue_idx)
            metrics["structure_function"].append(sf)
            metrics["complexity"].append(comp)
            metrics["entropy"].append(ent)
            metrics["tonality_strength"].append(tonality)
            metrics["wing_balance"].append(wing_balance)
            metrics["mean_z"].append(float(Z.mean()))
            metrics["z_variance"].append(float(Z.var()))

            # --- ADAPT ρ ---
            rhos = adapt_rhos(rhos, pcs, tonality, step)

            # Progress
            if step % 10000 == 0:
                elapsed = time.time() - t0
                print(
                    f"  step {step:6d}  |  "
                    f"ρ={rhos.mean():5.2f}±{rhos.std():4.2f}  |  "
                    f"C={total_c:.3f}  |  "
                    f"Dlg={dialogue_idx:+.3f}  |  "
                    f"T={tonality:.3f}  |  "
                    f"SF={sf:.2e}  |  "
                    f"CE={comp:.3f}/{ent:.3f}  |  "
                    f"{elapsed:.1f}s"
                )

    elapsed_total = time.time() - t0
    print(f"\nSimulation complete in {elapsed_total:.1f}s")

    # ==============================================================================
    # POST-PROCESSING & EMERGENT PROPERTY ANALYSIS
    # ==============================================================================
    print("\nAnalyzing emergent properties...")

    # 1. ρ flow analysis: where did systems end up vs start?
    rho_start = rho_hist[0, :]
    rho_end = rho_hist[-1, :]
    rho_flow = rho_end - rho_start

    # 2. Tonality emergence: when did A# major stabilize?
    tonality_arr = np.array(metrics["tonality_strength"])
    half_steps = len(tonality_arr) // 2
    tonality_first_half = tonality_arr[:half_steps].mean()
    tonality_second_half = tonality_arr[half_steps:].mean()
    tonality_gain = tonality_second_half - tonality_first_half

    # 3. Synchronization: did wings become more or less correlated?
    dialogue_arr = np.array(metrics["dialogue_index"])
    dialogue_first = dialogue_arr[:half_steps].mean()
    dialogue_second = dialogue_arr[half_steps:].mean()

    # 4. Metric peak alignment: did ρ drift toward SF=24 or CE=15?
    final_rho_peak1_frac = np.mean((rho_end >= 13) & (rho_end <= 17))
    final_rho_peak2_frac = np.mean((rho_end >= 22) & (rho_end <= 26))

    # 5. Harmonic phase transitions: find points of rapid change
    consonance_arr = np.array(metrics["total_consonance"])
    consonance_diff = np.abs(np.diff(consonance_arr))
    transition_steps = np.where(consonance_diff > np.percentile(consonance_diff, 95))[0]

    # ==============================================================================
    # SAVE RESULTS
    # ==============================================================================
    out_dir = Path("/tmp/fm-research/CODE")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Large arrays compressed
    np.savez_compressed(
        out_dir / "harmonic_convection_state.npz",
        states=state_hist,
        rhos=rho_hist,
        pcs=pc_hist,
        rho_flow=rho_flow,
    )

    # Time-series metrics
    with open(out_dir / "harmonic_convection_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    # Emergent analysis
    emergent = {
        "tonality_first_half": float(tonality_first_half),
        "tonality_second_half": float(tonality_second_half),
        "tonality_gain": float(tonality_gain),
        "dialogue_first_half": float(dialogue_first),
        "dialogue_second_half": float(dialogue_second),
        "dialogue_change": float(dialogue_second - dialogue_first),
        "final_rho_near_ce15_fraction": float(final_rho_peak1_frac),
        "final_rho_near_sf24_fraction": float(final_rho_peak2_frac),
        "rho_flow_mean": float(rho_flow.mean()),
        "rho_flow_std": float(rho_flow.std()),
        "n_phase_transitions": int(len(transition_steps)),
        "max_consonance": float(consonance_arr.max()),
        "mean_consonance": float(consonance_arr.mean()),
        "max_tonality": float(tonality_arr.max()),
    }

    with open(out_dir / "harmonic_convection_emergent.json", "w") as f:
        json.dump(emergent, f, indent=2)

    # Summary
    summary = {
        "experiment_name": "harmonic_convection",
        "timestamp": datetime.now().isoformat(),
        "runtime_seconds": elapsed_total,
        "N_SYSTEMS": N_SYSTEMS,
        "N_STEPS": N_STEPS,
        "DT": DT,
        "SAVE_EVERY": SAVE_EVERY,
        "parameters": {
            "sigma": SIGMA,
            "beta": BETA,
            "rho_min": RHO_MIN,
            "rho_max": RHO_MAX,
        },
        "musical_mapping": {
            "target_tonality_pc": AS_SHARP_PC,
            "relative_minor_pc": F_MINOR_PC,
            "wing_modality": "left_major_right_minor",
            "projection": "azimuthal_angle_plus_z_modulation",
        },
        "final_state": {
            "mean_rho": float(rhos.mean()),
            "std_rho": float(rhos.std()),
            "mean_z": float(Z.mean()),
        },
        "emergent_properties": emergent,
    }

    with open(out_dir / "harmonic_convection_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Also save the script itself for reproducibility
    script_src = Path(__file__).read_text()
    (out_dir / "harmonic_convection.py").write_text(script_src)

    print(f"\n{'='*72}")
    print("RESULTS SAVED")
    print(f"{'='*72}")
    print(f"State history:    {out_dir / 'harmonic_convection_state.npz'}")
    print(f"Time-series:      {out_dir / 'harmonic_convection_metrics.json'}")
    print(f"Emergent props:   {out_dir / 'harmonic_convection_emergent.json'}")
    print(f"Summary:          {out_dir / 'harmonic_convection_summary.json'}")
    print(f"\nKey findings:")
    print(f"  Tonality gain:        {tonality_gain:+.3f} ({'emerged' if tonality_gain > 0 else 'dissolved'})")
    print(f"  Dialogue evolution:   {dialogue_second - dialogue_first:+.3f}")
    print(f"  ρ flow (mean±std):    {rho_flow.mean():+.3f} ± {rho_flow.std():.3f}")
    print(f"  Systems near CE=15:   {final_rho_peak1_frac:.1%}")
    print(f"  Systems near SF=24:   {final_rho_peak2_frac:.1%}")
    print(f"  Phase transitions:    {len(transition_steps)}")
    print(f"{'='*72}")

    return summary


if __name__ == "__main__":
    run_experiment()
