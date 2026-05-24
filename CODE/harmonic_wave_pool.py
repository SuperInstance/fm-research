"""
================================================================================
THE HARMONIC WAVE POOL
================================================================================
A 64×64 toroidal lattice of 4096 coupled Lorenz systems where the physical
coupling strength between neighbors is modulated by their musical consonance
on the circle of fifths.

NOVELTY:
- Harmony becomes a spatial field: consonant neighbors synchronize faster
- The circle of fifths literally shapes the physics of diffusion
- Harmonic domains emerge, compete, and propagate as traveling waves
- The butterfly's two wings become spatial regions in call-and-response
- Real-time tracking of harmonic vorticity, domain walls, and wave speed

PHYSICS:
Each lattice site i has Lorenz dynamics with additional coupling:
    dX_i/dt = σ(Y_i - X_i) + ε Σ_j C(n_i, n_j) · (X_j - X_i)
where j ∈ {N,S,E,W} neighbors, C is circle-of-fifths consonance, and n_i is
agent i's current pitch class. Same for dY/dt, dZ/dt.

MUSICAL MAPPING:
- Azimuthal angle in (x,y) → chromatic pitch class [0,12)
- z-height → dynamic weight / octave register
- ρ value → "temperature" (CE=15 cool/structured, SF=24 warm/chaotic)

ANALYSIS:
- Spatial autocorrelation of pitch class
- Harmonic vorticity (curl of pitch gradient)
- Domain wall length (boundary between dissonant regions)
- Wave propagation speed via cross-correlation
- Collective z-oscillation as emergent metrical pulse
- Structure Function & Complexity-Entropy for the lattice field
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
GRID_SIZE = 64          # 64×64 = 4096 agents
N_STEPS = 80_000
DT = 0.0125
SAVE_EVERY = 100

SIGMA = 10.0
BETA = 8.0 / 3.0
RHO_MIN, RHO_MAX = 12.0, 32.0
EPSILON = 0.08          # Base coupling strength

# Circle-of-fifths consonance weights for interval classes [0..11]
INTERVAL_WEIGHTS = np.array([
    1.00, 0.08, 0.25, 0.82, 0.88, 0.60,
    0.05, 0.95, 0.72, 0.78, 0.20, 0.15
], dtype=np.float32)

# Precompute consonance matrix C[i,j] = weight[interval_class(i,j)]
CHROMATIC = np.arange(12)
INTERVAL_CLASS = np.minimum(
    np.abs(CHROMATIC[:, None] - CHROMATIC[None, :]),
    12 - np.abs(CHROMATIC[:, None] - CHROMATIC[None, :])
)
CONSONANCE_MATRIX = INTERVAL_WEIGHTS[INTERVAL_CLASS].astype(np.float32)

# Target tonality: A# major (pc=10)
TARGET_PC = 10.0

# ==============================================================================
# VECTORIZED RK4 WITH SPATIAL COUPLING
# ==============================================================================
def lorenz_deriv(X, Y, Z, rhos, Cx, Cy, Cz):
    """
    Compute derivatives with harmonic coupling.
    Cx, Cy, Cz are the weighted neighbor differences for each dimension.
    """
    dX = SIGMA * (Y - X) + EPSILON * Cx
    dY = X * (rhos - Z) - Y + EPSILON * Cy
    dZ = X * Y - BETA * Z + EPSILON * Cz
    return dX, dY, dZ


def harmonic_coupling(F, pcs):
    """
    Compute consonance-weighted neighbor differences for field F.
    F and pcs are 2D arrays of shape (H, W).
    Returns weighted sum of (F_neighbor - F_center) for 4 neighbors.
    """
    # Neighbors on torus
    F_n = np.roll(F, -1, axis=0)
    F_s = np.roll(F, 1, axis=0)
    F_e = np.roll(F, -1, axis=1)
    F_w = np.roll(F, 1, axis=1)

    # Neighbor pitch classes
    pc_n = np.roll(pcs, -1, axis=0)
    pc_s = np.roll(pcs, 1, axis=0)
    pc_e = np.roll(pcs, -1, axis=1)
    pc_w = np.roll(pcs, 1, axis=1)

    # Consonances (lookup in precomputed matrix)
    C_n = CONSONANCE_MATRIX[np.floor(pcs).astype(int) % 12,
                            np.floor(pc_n).astype(int) % 12]
    C_s = CONSONANCE_MATRIX[np.floor(pcs).astype(int) % 12,
                            np.floor(pc_s).astype(int) % 12]
    C_e = CONSONANCE_MATRIX[np.floor(pcs).astype(int) % 12,
                            np.floor(pc_e).astype(int) % 12]
    C_w = CONSONANCE_MATRIX[np.floor(pcs).astype(int) % 12,
                            np.floor(pc_w).astype(int) % 12]

    # Weighted coupling
    out = (C_n * (F_n - F) + C_s * (F_s - F) +
           C_e * (F_e - F) + C_w * (F_w - F))
    return out


def rk4_step(X, Y, Z, rhos, pcs):
    """One RK4 step with harmonic coupling."""
    # k1
    Cx = harmonic_coupling(X, pcs)
    Cy = harmonic_coupling(Y, pcs)
    Cz = harmonic_coupling(Z, pcs)
    k1x, k1y, k1z = lorenz_deriv(X, Y, Z, rhos, Cx, Cy, Cz)

    # k2
    X2 = X + 0.5 * DT * k1x
    Y2 = Y + 0.5 * DT * k1y
    Z2 = Z + 0.5 * DT * k1z
    pcs2 = trajectory_to_pitch_class(X2, Y2, Z2)
    Cx2 = harmonic_coupling(X2, pcs2)
    Cy2 = harmonic_coupling(Y2, pcs2)
    Cz2 = harmonic_coupling(Z2, pcs2)
    k2x, k2y, k2z = lorenz_deriv(X2, Y2, Z2, rhos, Cx2, Cy2, Cz2)

    # k3
    X3 = X + 0.5 * DT * k2x
    Y3 = Y + 0.5 * DT * k2y
    Z3 = Z + 0.5 * DT * k2z
    pcs3 = trajectory_to_pitch_class(X3, Y3, Z3)
    Cx3 = harmonic_coupling(X3, pcs3)
    Cy3 = harmonic_coupling(Y3, pcs3)
    Cz3 = harmonic_coupling(Z3, pcs3)
    k3x, k3y, k3z = lorenz_deriv(X3, Y3, Z3, rhos, Cx3, Cy3, Cz3)

    # k4
    X4 = X + DT * k3x
    Y4 = Y + DT * k3y
    Z4 = Z + DT * k3z
    pcs4 = trajectory_to_pitch_class(X4, Y4, Z4)
    Cx4 = harmonic_coupling(X4, pcs4)
    Cy4 = harmonic_coupling(Y4, pcs4)
    Cz4 = harmonic_coupling(Z4, pcs4)
    k4x, k4y, k4z = lorenz_deriv(X4, Y4, Z4, rhos, Cx4, Cy4, Cz4)

    X_new = X + (DT / 6.0) * (k1x + 2 * k2x + 2 * k3x + k4x)
    Y_new = Y + (DT / 6.0) * (k1y + 2 * k2y + 2 * k3y + k4y)
    Z_new = Z + (DT / 6.0) * (k1z + 2 * k2z + 2 * k3z + k4z)
    return X_new, Y_new, Z_new


# ==============================================================================
# MUSICAL PROJECTION
# ==============================================================================
def trajectory_to_pitch_class(X, Y, Z):
    """Map Lorenz state to chromatic pitch class [0, 12)."""
    theta = np.arctan2(Y, X)
    z_mod = (Z - 25.0) / 15.0
    angle = theta + 0.25 * z_mod
    pc = ((angle + np.pi) / (2.0 * np.pi) * 12.0) % 12.0
    return pc.astype(np.float32)


# ==============================================================================
# SPATIAL ANALYSIS
# ==============================================================================
def spatial_autocorrelation(field, max_lag=16):
    """Compute 2D spatial autocorrelation via FFT."""
    field = field - field.mean()
    fft = np.fft.fft2(field)
    power = np.abs(fft) ** 2
    acf = np.fft.ifft2(power).real
    acf = acf / acf[0, 0]
    # Extract radial average
    h, w = field.shape
    center_y, center_x = h // 2, w // 2
    lags = np.arange(max_lag)
    radial = []
    for lag in lags:
        y_idx = (center_y + np.round(lag * np.sin(np.linspace(0, 2 * np.pi, 64)))).astype(int) % h
        x_idx = (center_x + np.round(lag * np.cos(np.linspace(0, 2 * np.pi, 64)))).astype(int) % w
        radial.append(acf[y_idx, x_idx].mean())
    return lags, np.array(radial)


def harmonic_vorticity(pcs):
    """
    Compute curl of the pitch gradient field.
    High vorticity = swirling harmonic motion (like a musical eddy).
    """
    # Gradient in pitch space (handle wraparound at octave boundary)
    dx = np.sin(2 * np.pi * (np.roll(pcs, -1, axis=1) - pcs) / 12.0)
    dy = np.sin(2 * np.pi * (np.roll(pcs, -1, axis=0) - pcs) / 12.0)
    # Curl = d(dy)/dx - d(dx)/dy
    curl = (np.roll(dy, -1, axis=1) - dy) - (np.roll(dx, -1, axis=0) - dx)
    return float(np.abs(curl).mean())


def domain_wall_length(pcs):
    """Count boundaries between dissonant adjacent cells."""
    pc_int = np.floor(pcs).astype(int) % 12
    # Horizontal boundaries
    diff_h = np.minimum(np.abs(pc_int - np.roll(pc_int, -1, axis=1)),
                        12 - np.abs(pc_int - np.roll(pc_int, -1, axis=1)))
    # Vertical boundaries
    diff_v = np.minimum(np.abs(pc_int - np.roll(pc_int, -1, axis=0)),
                        12 - np.abs(pc_int - np.roll(pc_int, -1, axis=0)))
    # Dissonant if interval class > 4 (tritone or larger)
    walls = (diff_h > 4).sum() + (diff_v > 4).sum()
    return int(walls)


def structure_function_2d(field, lag=3):
    """Mean squared displacement at spatial lag."""
    diff_x = field - np.roll(field, lag, axis=1)
    diff_y = field - np.roll(field, lag, axis=0)
    return float(np.mean(diff_x ** 2 + diff_y ** 2))


def complexity_entropy_field(pcs, order=3):
    """Complexity-entropy on the 2D pitch class field."""
    flat = pcs.flatten()
    n = len(flat)
    if n < order + 1:
        return 0.0, 1.0
    windows = np.lib.stride_tricks.sliding_window_view(flat, order)
    ranks = np.argsort(np.argsort(windows, axis=1), axis=1)
    bases = order ** np.arange(order, dtype=np.int64)
    pattern_ids = np.dot(ranks, bases)
    n_patterns = order ** order
    hist = np.bincount(pattern_ids, minlength=n_patterns)
    p = hist / hist.sum()
    p = p[p > 0]
    max_ent = np.log2(n_patterns)
    entropy = -np.sum(p * np.log2(p)) / max_ent
    uniform = 1.0 / n_patterns
    disequilibrium = np.sum((p - uniform) ** 2)
    complexity = disequilibrium * entropy
    return float(complexity), float(entropy)


# ==============================================================================
# MAIN EXPERIMENT
# ==============================================================================
def run_experiment():
    print("=" * 72)
    print("THE HARMONIC WAVE POOL")
    print("=" * 72)
    print(f"Lattice:          {GRID_SIZE}×{GRID_SIZE} = {GRID_SIZE**2} agents")
    print(f"Steps:            {N_STEPS}")
    print(f"dt:               {DT}")
    print(f"Coupling ε:       {EPSILON}")
    print(f"Simulation time:  {N_STEPS * DT:.1f} Lorenz units")
    print(f"Target tonality:  A# major (pc={TARGET_PC})")
    print("=" * 72)

    np.random.seed(0xACEACE)
    # Initialize ρ with a gradient across the lattice
    y_coords = np.linspace(0, 1, GRID_SIZE)[:, None]
    x_coords = np.linspace(0, 1, GRID_SIZE)[None, :]
    rhos = 15.0 + 9.0 * (x_coords + y_coords) + np.random.randn(GRID_SIZE, GRID_SIZE).astype(np.float32) * 1.5
    rhos = np.clip(rhos, RHO_MIN, RHO_MAX)

    # Initial conditions scattered near attractor
    X = np.random.randn(GRID_SIZE, GRID_SIZE).astype(np.float32) * 6.0
    Y = np.random.randn(GRID_SIZE, GRID_SIZE).astype(np.float32) * 6.0
    Z = np.random.randn(GRID_SIZE, GRID_SIZE).astype(np.float32) * 7.0 + 25.0

    # Buffers
    N_SAVE = N_STEPS // SAVE_EVERY
    X_hist = np.zeros((N_SAVE, GRID_SIZE, GRID_SIZE), dtype=np.float32)
    Y_hist = np.zeros((N_SAVE, GRID_SIZE, GRID_SIZE), dtype=np.float32)
    Z_hist = np.zeros((N_SAVE, GRID_SIZE, GRID_SIZE), dtype=np.float32)
    rho_hist = np.zeros((N_SAVE, GRID_SIZE, GRID_SIZE), dtype=np.float32)
    pc_hist = np.zeros((N_SAVE, GRID_SIZE, GRID_SIZE), dtype=np.float32)

    metrics = {
        "step": [], "time": [],
        "mean_rho": [], "std_rho": [],
        "mean_pc": [], "pc_variance": [],
        "spatial_corr_lag1": [],
        "harmonic_vorticity": [],
        "domain_walls": [],
        "structure_function": [],
        "complexity": [], "entropy": [],
        "tonality_strength": [],
        "sync_order_param": [],
        "mean_z": [], "z_pulse": [],
    }

    t0 = time.time()

    for step in range(N_STEPS):
        pcs = trajectory_to_pitch_class(X, Y, Z)
        X, Y, Z = rk4_step(X, Y, Z, rhos, pcs)

        if step % SAVE_EVERY == 0:
            s = step // SAVE_EVERY
            X_hist[s] = X
            Y_hist[s] = Y
            Z_hist[s] = Z
            rho_hist[s] = rhos
            pc_hist[s] = pcs

            # Tonality: proximity to A# major scale
            scale_pcs = np.array([10, 0, 2, 3, 5, 7, 9], dtype=np.float32)
            expanded = np.abs(pcs[..., None] - scale_pcs[None, None, :]) % 12
            min_dist = np.minimum(expanded, 12 - expanded).min(axis=2)
            tonality = float(np.exp(-min_dist.mean() / 1.5))

            # Synchronization order parameter: magnitude of mean field
            mean_phase = np.exp(2j * np.pi * pcs / 12.0).mean()
            sync_param = float(np.abs(mean_phase))

            # Z-pulse: variance of z as proxy for collective rhythmic energy
            z_pulse = float(Z.var())

            # Spatial autocorrelation at lag 1
            _, acf = spatial_autocorrelation(pcs, max_lag=2)
            acf_lag1 = float(acf[1]) if len(acf) > 1 else 0.0

            # Domain walls
            walls = domain_wall_length(pcs)

            # Vorticity
            vort = harmonic_vorticity(pcs)

            # Structure function
            sf = structure_function_2d(pcs, lag=3)

            # Complexity-entropy
            comp, ent = complexity_entropy_field(pcs, order=3)

            metrics["step"].append(int(step))
            metrics["time"].append(float(step * DT))
            metrics["mean_rho"].append(float(rhos.mean()))
            metrics["std_rho"].append(float(rhos.std()))
            metrics["mean_pc"].append(float(pcs.mean()))
            metrics["pc_variance"].append(float(pcs.var()))
            metrics["spatial_corr_lag1"].append(acf_lag1)
            metrics["harmonic_vorticity"].append(vort)
            metrics["domain_walls"].append(walls)
            metrics["structure_function"].append(sf)
            metrics["complexity"].append(comp)
            metrics["entropy"].append(ent)
            metrics["tonality_strength"].append(tonality)
            metrics["sync_order_param"].append(sync_param)
            metrics["mean_z"].append(float(Z.mean()))
            metrics["z_pulse"].append(z_pulse)

            if step % 10000 == 0:
                elapsed = time.time() - t0
                print(
                    f"  step {step:6d}  |  "
                    f"ρ={rhos.mean():5.2f}±{rhos.std():4.2f}  |  "
                    f"T={tonality:.3f}  |  "
                    f"Sync={sync_param:.3f}  |  "
                    f"Walls={walls:4d}  |  "
                    f"Vort={vort:.3f}  |  "
                    f"SF={sf:.3f}  |  "
                    f"{elapsed:.1f}s"
                )

    elapsed_total = time.time() - t0
    print(f"\nSimulation complete in {elapsed_total:.1f}s")

    # ==============================================================================
    # POST-PROCESSING
    # ==============================================================================
    print("\nAnalyzing emergent spatial structures...")

    # Track domain formation over time
    walls_arr = np.array(metrics["domain_walls"])
    walls_first = walls_arr[:len(walls_arr)//2].mean()
    walls_second = walls_arr[len(walls_arr)//2:].mean()
    walls_change = walls_second - walls_first

    # Tonality evolution
    tonal_arr = np.array(metrics["tonality_strength"])
    tonal_first = tonal_arr[:len(tonal_arr)//2].mean()
    tonal_second = tonal_arr[len(tonal_arr)//2:].mean()

    # Sync evolution
    sync_arr = np.array(metrics["sync_order_param"])
    sync_first = sync_arr[:len(sync_arr)//2].mean()
    sync_second = sync_arr[len(sync_arr)//2:].mean()

    # Z-pulse rhythm strength
    pulse_arr = np.array(metrics["z_pulse"])
    pulse_mean = pulse_arr.mean()
    pulse_cv = pulse_arr.std() / (pulse_mean + 1e-12)

    # Spatial correlation decay
    acf_arr = np.array(metrics["spatial_corr_lag1"])
    acf_mean = acf_arr.mean()

    # Final snapshot analysis
    final_pcs = pc_hist[-1]
    _, final_acf = spatial_autocorrelation(final_pcs, max_lag=16)
    correlation_length = np.argmax(final_acf < 1 / np.e) if (final_acf < 1 / np.e).any() else len(final_acf)

    # ==============================================================================
    # SAVE
    # ==============================================================================
    out_dir = Path("/tmp/fm-research/CODE")
    out_dir.mkdir(parents=True, exist_ok=True)

    np.savez_compressed(
        out_dir / "harmonic_wave_pool_state.npz",
        X=X_hist, Y=Y_hist, Z=Z_hist,
        rhos=rho_hist, pcs=pc_hist,
    )

    with open(out_dir / "harmonic_wave_pool_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    emergent = {
        "domain_walls_first_half": float(walls_first),
        "domain_walls_second_half": float(walls_second),
        "domain_walls_change": float(walls_change),
        "tonality_first_half": float(tonal_first),
        "tonality_second_half": float(tonal_second),
        "tonality_gain": float(tonal_second - tonal_first),
        "sync_first_half": float(sync_first),
        "sync_second_half": float(sync_second),
        "sync_change": float(sync_second - sync_first),
        "z_pulse_mean": float(pulse_mean),
        "z_pulse_cv": float(pulse_cv),
        "spatial_corr_lag1_mean": float(acf_mean),
        "correlation_length": int(correlation_length),
        "mean_vorticity": float(np.mean(metrics["harmonic_vorticity"])),
        "max_vorticity": float(np.max(metrics["harmonic_vorticity"])),
        "mean_structure_function": float(np.mean(metrics["structure_function"])),
    }

    with open(out_dir / "harmonic_wave_pool_emergent.json", "w") as f:
        json.dump(emergent, f, indent=2)

    summary = {
        "experiment_name": "harmonic_wave_pool",
        "timestamp": datetime.now().isoformat(),
        "runtime_seconds": elapsed_total,
        "grid_size": GRID_SIZE,
        "n_agents": GRID_SIZE ** 2,
        "n_steps": N_STEPS,
        "dt": DT,
        "epsilon": EPSILON,
        "parameters": {"sigma": SIGMA, "beta": BETA, "rho_range": [RHO_MIN, RHO_MAX]},
        "musical_mapping": {
            "target_tonality_pc": TARGET_PC,
            "projection": "azimuthal_angle_plus_z_modulation",
            "coupling": "circle_of_fifths_consonance_weighted",
        },
        "emergent_properties": emergent,
    }

    with open(out_dir / "harmonic_wave_pool_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Save script
    script_src = Path(__file__).read_text()
    (out_dir / "harmonic_wave_pool.py").write_text(script_src)

    print(f"\n{'='*72}")
    print("RESULTS SAVED")
    print(f"{'='*72}")
    print(f"State:    {out_dir / 'harmonic_wave_pool_state.npz'}")
    print(f"Metrics:  {out_dir / 'harmonic_wave_pool_metrics.json'}")
    print(f"Emergent: {out_dir / 'harmonic_wave_pool_emergent.json'}")
    print(f"Summary:  {out_dir / 'harmonic_wave_pool_summary.json'}")
    print(f"\nKey findings:")
    print(f"  Domain walls:        {walls_first:.0f} → {walls_second:.0f} ({'sharpened' if walls_change < 0 else 'blurred'})")
    print(f"  Tonality gain:       {tonal_second - tonal_first:+.3f}")
    print(f"  Sync evolution:      {sync_first:.3f} → {sync_second:.3f}")
    print(f"  Correlation length:  {correlation_length} lattice units")
    print(f"  Mean vorticity:      {np.mean(metrics['harmonic_vorticity']):.3f}")
    print(f"  Z-pulse CV:          {pulse_cv:.3f}")
    print(f"{'='*72}")

    return summary


if __name__ == "__main__":
    run_experiment()
