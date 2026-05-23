import numpy as np
import json

print("=== Catastrophe Theory: The Aha Moment ===\n")

# Catastrophe theory: small changes in parameters cause SUDDEN jumps in state
# The cusp catastrophe: V(x) = x⁴/4 - ax²/2 - bx
# x = state (creative output quality)
# a = "splitting factor" (constraint rigidity)
# b = "normal factor" (stress/pressure)

# When a > 0, the potential has two minima (bistable)
# The system can JUMP between minima — this IS the "aha moment"

# Part 1: The creative potential landscape
print("--- Part 1: Creative Potential Landscape ---")
def creative_potential(x, a, b):
    """Cusp catastrophe potential for creative systems."""
    return x**4/4 - a*x**2/2 - b*x

def find_minima(a, b, x_range=(-3, 3)):
    """Find stable states (local minima)."""
    x = np.linspace(x_range[0], x_range[1], 1000)
    V = creative_potential(x, a, b)
    
    minima = []
    for i in range(1, len(x)-1):
        if V[i] < V[i-1] and V[i] < V[i+1]:
            minima.append((x[i], V[i]))
    return minima

# Sweep the splitting parameter (constraint rigidity)
for a in [-2, -1, 0, 0.5, 1, 2, 3]:
    minima = find_minima(a, 0.0)
    n_minima = len(minima)
    states = [f"V={v:.2f} at x={x:.2f}" for x, v in minima]
    print(f"  a={a:5.1f} (rigidity): {n_minima} stable state(s): {states}")

# Part 2: The bifurcation — when one minimum becomes two
print("\n--- Part 2: Creative Bifurcation ---")
# At a=0, the system transitions from 1 minimum to 2
# This IS the transition from "one obvious answer" to "creative tension"

print("  a < 0: ONE creative state (obvious, conventional)")
print("  a = 0: BIFURCATION POINT (the moment of creative potential)")
print("  a > 0: TWO creative states (conventional AND novel coexist)")
print("  The 'aha moment' is the JUMP from conventional to novel minimum")

# Part 3: The stress-induced jump
print("\n--- Part 3: Stress Causes the Jump ---")
a = 2.0  # bifurcated (two states available)

for b in np.arange(-3, 3.1, 0.5):
    minima = find_minima(a, b)
    x_vals = [x for x, v in minima]
    
    if len(x_vals) == 2:
        state = f"TWO states: x={x_vals[0]:.2f} (conventional) and x={x_vals[1]:.2f} (novel)"
    elif len(x_vals) == 1:
        if x_vals[0] > 0:
            state = f"ONE state: x={x_vals[0]:.2f} (NOVEL, jumped!)"
        else:
            state = f"ONE state: x={x_vals[0]:.2f} (conventional)"
    else:
        state = f"{len(x_vals)} states"
    
    print(f"  b={b:5.1f} (stress): {state}")

# Part 4: Hysteresis — why creative breakthroughs feel irreversible
print("\n--- Part 4: Hysteresis (Irreversibility) ---")
# The jump from conventional→novel happens at a DIFFERENT stress level
# than the jump from novel→conventional

a = 2.0
# Forward sweep (increasing stress)
print("  Increasing stress (conventional → novel):")
forward_jump = None
for b in np.arange(-3, 3.01, 0.1):
    minima = find_minima(a, b)
    if len(minima) == 1 and minima[0][0] > 0:
        forward_jump = b
        print(f"    Jump at b={b:.1f}")
        break

# Backward sweep (decreasing stress)
print("  Decreasing stress (novel → conventional):")
backward_jump = None
for b in np.arange(3, -3.01, -0.1):
    minima = find_minima(a, b)
    if len(minima) == 1 and minima[0][0] < 0:
        backward_jump = b
        print(f"    Jump at b={b:.1f}")
        break

if forward_jump and backward_jump:
    hysteresis = abs(forward_jump - backward_jump)
    print(f"  Hysteresis gap: {hysteresis:.1f}")
    print(f"  This is why creative breakthroughs feel IRREVERSIBLE")
    print(f"  Once you see the novel solution, you can't unsee it")

# Part 5: Genre catastrophe
print("\n--- Part 5: Genre as Catastrophe ---")
# Each genre has different (a, b) parameters
# Genre transitions (innovation) are catastrophe jumps

genres = {
    'pop':      {'a': -1.0, 'b': 0.0},    # one state, obvious
    'jazz':     {'a': 2.0, 'b': 0.5},      # bifurcated, slightly stressed
    'classical':{'a': 3.0, 'b': -1.0},     # very bifurcated, conventional
    'avant_garde':{'a': 3.0, 'b': 2.0},    # bifurcated, heavily stressed toward novel
    'blues':    {'a': 1.0, 'b': 1.0},       # moderate bifurcation, moderate stress
}

for genre, params in genres.items():
    minima = find_minima(params['a'], params['b'])
    x_vals = [x for x, v in minima]
    if len(x_vals) == 2:
        tension = abs(x_vals[1] - x_vals[0])
        print(f"  {genre:12s}: TWO states, tension={tension:.2f} (creative potential)")
    elif len(x_vals) == 1:
        state = "novel" if x_vals[0] > 0 else "conventional"
        print(f"  {genre:12s}: ONE state ({state}), no creative tension")

# Part 6: Predicting the aha moment
print("\n--- Part 6: Predicting Creative Breakthroughs ---")
# The aha moment happens when:
# 1. System is bifurcated (a > 0) — constraints create tension
# 2. Stress passes the critical threshold — jump occurs
# 3. The jump is IRREVERSIBLE (hysteresis)

# Simulate: a creator working under increasing stress
a = 2.5  # high constraint rigidity (working within strict rules)
state = -2.0  # start in conventional state

print(f"  Starting state: x={state:.2f} (conventional)")
print(f"  Constraint rigidity: a={a}")
for b in np.arange(-3, 4, 0.2):
    minima = find_minima(a, b)
    # Find the minimum closest to current state
    if minima:
        closest = min(minima, key=lambda m: abs(m[0] - state))
        new_state = closest[0]
        
        if abs(new_state - state) > 0.5:
            print(f"  ⚡ b={b:.1f}: JUMP from x={state:.2f} to x={new_state:.2f} — AHA MOMENT!")
            state = new_state
            break
        state = new_state

print(f"  Final state: x={state:.2f} (NOVEL — irreversible creative breakthrough)")

with open('CODE/EXPERIMENT-CATASTROPHE.json', 'w') as f:
    json.dump({'forward_jump': forward_jump, 'backward_jump': backward_jump}, f)

print("\n=== CATASTROPHE PRINCIPLE ===")
print("The 'aha moment' is a cusp catastrophe jump.")
print("It requires: bifurcation (a>0, creative tension) + stress (b passes threshold)")
print("It's IRREVERSIBLE due to hysteresis (you can't unsee the insight)")
print("Genre innovation IS a catastrophe — sudden, irreversible, stress-triggered")
