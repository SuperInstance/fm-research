import numpy as np
import json
import math

print("=== Flywheel Effect Experiment ===\n")

PHI = (1 + math.sqrt(5)) / 2

# Part 1: Speed vs Mass asymmetry
print("--- Part 1: KE = ½Iω² — Speed Beats Mass ---")
base_ke = 100  # target energy
masses = [1, 2, 5, 10, 20, 50, 100]
print(f"Target KE = {base_ke}")
print(f"To achieve {base_ke} KE:")
for m in masses:
    omega = math.sqrt(2 * base_ke / m)
    print(f"  mass={m:3d}: need ω={omega:.2f} rad/s")
print(f"\nDoubling mass: ×2 effort needed")
print(f"Doubling speed: ×4 energy gained — speed wins")

# Part 2: Fulcrum effect — constraint forcing rotation
print("\n--- Part 2: Fulcrum Converts Linear to Rotational ---")
# Without fulcrum: particle moves linearly, covers distance d
# With fulcrum: same energy creates rotation, covers distance 2πr × n_revolutions

energies = np.linspace(0.1, 10, 20)
for E in [1, 5, 10]:
    # Linear: d = √(2E/m), m=1
    linear_dist = math.sqrt(2 * E)
    
    # Rotational: with fulcrum at r=1, ω = √(2E/I), I=1
    omega = math.sqrt(2 * E)
    # After 10 time units, total angle = ω × 10
    angle = omega * 10
    rotational_dist = angle  # arc length at r=1
    
    ratio = rotational_dist / linear_dist
    print(f"  E={E:.1f}: linear={linear_dist:.2f}, rotational(10s)={rotational_dist:.2f}, ratio={ratio:.1f}×")

# Part 3: Figure skater effect — constraint concentration
print("\n--- Part 3: Figure Skater — Concentrating Constraints ---")
# Start with I=5 (arms out), ω=2
I_start = 5.0
omega_start = 2.0
L = I_start * omega_start  # conserved!
KE_start = 0.5 * I_start * omega_start**2

print(f"Start: I={I_start}, ω={omega_start}, L={L}, KE={KE_start}")
for I_new in [4, 3, 2, 1, 0.5]:
    omega_new = L / I_new
    KE_new = 0.5 * I_new * omega_new**2
    ratio = KE_new / KE_start
    print(f"  Pull in to I={I_new}: ω={omega_new:.1f}, KE={KE_new:.1f} ({ratio:.2f}× original)")

# Part 4: Startup vs Corporate (Inertia trade-off)
print("\n--- Part 4: Startup vs Corporate ---")
# Startup: I=1, can apply small torque often
# Corporate: I=100, can apply large torque rarely

tau_startup = 0.5   # small force
tau_corporate = 10.0  # large force
I_startup = 1.0
I_corporate = 100.0
dt = 1.0
T = 100

omega_s = 0.0
omega_c = 0.0
ke_history_s = []
ke_history_c = []

for t in range(T):
    # Startup applies torque every tick
    omega_s += (tau_startup / I_startup) * dt
    
    # Corporate applies torque every 10 ticks
    if t % 10 == 0:
        omega_c += (tau_corporate / I_corporate) * dt
    
    ke_s = 0.5 * I_startup * omega_s**2
    ke_c = 0.5 * I_corporate * omega_c**2
    ke_history_s.append(ke_s)
    ke_history_c.append(ke_c)

print(f"After {T} ticks:")
print(f"  Startup:  ω={omega_s:.2f}, KE={ke_history_s[-1]:.2f}")
print(f"  Corporate: ω={omega_c:.2f}, KE={ke_history_c[-1]:.2f}")
print(f"  Startup / Corporate = {ke_history_s[-1]/max(ke_history_c[-1], 0.01):.1f}×")

# Part 5: Positive feedback — flywheel runaway
print("\n--- Part 5: Flywheel Runaway (Positive Feedback) ---")
omega = 1.0
I = 5.0
base_torque = 0.1

print("Tick | ω | KE | Feedback Torque | Total Torque")
for t in [0, 10, 20, 50, 100, 200, 500]:
    # Advance simulation to tick t
    omega_sim = 1.0
    for step in range(t):
        # Feedback: torque increases with current ω (positive feedback)
        feedback = 0.01 * omega_sim
        total_torque = base_torque + feedback
        omega_sim += (total_torque / I) * dt
    
    ke = 0.5 * I * omega_sim**2
    feedback_now = 0.01 * omega_sim
    print(f"  t={t:3d}: ω={omega_sim:.2f}, KE={ke:.2f}, feedback={feedback_now:.3f}, total_τ={base_torque+feedback_now:.3f}")

# Part 6: Cross-product torque — only perpendicular force creates rotation
print("\n--- Part 6: Cross Product — Perpendicular Force Only ---")
angles = np.arange(0, 91, 15)
for angle_deg in angles:
    angle_rad = math.radians(angle_deg)
    # Force at angle to lever arm: τ = F·r·sin(θ)
    F = 10.0
    r = 2.0
    torque = F * r * math.sin(angle_rad)
    print(f"  Force at {angle_deg:2d}° to lever: τ = {torque:.2f}")

print(f"\n  At 0° (parallel): NO rotation (all push, no spin)")
print(f"  At 90° (perpendicular): MAXIMUM rotation (pure spin)")
print(f"  In music: tension directly resolved = 0° = boring")
print(f"  In music: tension deflected sideways = 90° = interesting")

# Save results
results = {
    'startup_ke': ke_history_s[-1],
    'corporate_ke': ke_history_c[-1],
    'startup_advantage': ke_history_s[-1] / max(ke_history_c[-1], 0.01)
}
with open('CODE/EXPERIMENT-FLYWHEEL.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n=== SUMMARY ===")
print("Speed beats mass: KE ∝ ω² (quadratic in speed, linear in mass)")
print("Fulcrum converts finite linear force into infinite rotation")
print("Constraint concentration = figure skater pulling arms in = free energy")
print("Startup (small I, frequent τ) beats corporate (large I, rare τ)")
print("Positive feedback creates flywheel runaway (exponential growth)")
print("Only perpendicular force creates rotation (jazz detours > direct resolution)")
