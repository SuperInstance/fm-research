import numpy as np
import json

print("=== Solitons in Creative Systems ===\n")

# A soliton: a self-reinforcing wave packet that:
# 1. Maintains its shape over distance/time
# 2. Passes through other solitons unchanged
# 3. Emerges from nonlinear + dispersive balance

# Hypothesis: Great creative ideas are solitons.
# They maintain their identity across cultures and centuries.
# They pass through other ideas and emerge intact.
# Shakespeare → Kurosawa → Lion King = same soliton, different medium.

# Part 1: KdV soliton (classic)
print("--- Part 1: Classic Soliton (KdV Equation) ---")
# u_t + 6u·u_x + u_xxx = 0
# Soliton solution: u(x,t) = (c/2) · sech²(√c/2 · (x - ct))

def soliton(x, t, c, x0=0):
    """KdV soliton with speed c."""
    arg = np.sqrt(c)/2 * (x - c*t - x0)
    return c/2 / np.cosh(arg)**2

x = np.linspace(-20, 20, 1000)

# Two solitons with different speeds
c1, c2 = 4.0, 1.0  # speeds (also = amplitude × 2)

for t in [-5, 0, 5, 10]:
    u1 = soliton(x, t, c1, x0=-10)
    u2 = soliton(x, t, c2, x0=-5)
    
    # At t=0 they overlap, but at t>>0 they separate with soliton 1 ahead
    # The FAST soliton passes THROUGH the slow one and both emerge unchanged
    
    total = np.max(u1 + u2)
    print(f"  t={t:3d}: peak1={np.max(u1):.3f}, peak2={np.max(u2):.3f}, combined={total:.3f}")

print("  After collision: both solitons emerge UNCHANGED. Identity preserved.")

# Part 2: Creative solitons — ideas that survive transmission
print("\n--- Part 2: Creative Solitons ---")
# An idea is a soliton if it:
# 1. Maintains form across translations (languages, media, cultures)
# 2. Passes through other ideas and emerges intact
# 3. Has a "speed" (rate of cultural propagation)
# 4. Has an "amplitude" (cultural impact)

creative_solitons = {
    'Hero Journey':      {'amplitude': 3.0, 'speed': 1.0, 'origin': -3000},
    'Love Conquers All': {'amplitude': 2.5, 'speed': 0.8, 'origin': -5000},
    'Revenge':           {'amplitude': 2.0, 'speed': 1.2, 'origin': -10000},
    'Rags to Riches':    {'amplitude': 2.0, 'speed': 0.5, 'origin': -1000},
    'Forbidden Love':    {'amplitude': 2.5, 'speed': 0.7, 'origin': -2000},
    'Quest':             {'amplitude': 3.0, 'speed': 0.9, 'origin': -4000},
    'Sacrifice':         {'amplitude': 3.5, 'speed': 1.1, 'origin': -8000},
    'Trickster':         {'amplitude': 1.5, 'speed': 0.6, 'origin': -15000},
}

print("  Creative solitons (narrative archetypes):")
for name, props in sorted(creative_solitons.items(), key=lambda x: -x[1]['amplitude']):
    # How far has this idea propagated?
    propagation = props['speed'] * (2025 - props['origin'])  # distance = speed × time
    print(f"    {name:20s}: impact={props['amplitude']:.1f}, speed={props['speed']:.1f}, "
          f"origin={props['origin']}yr, propagation={propagation:.0f} cultural-units")

# Part 3: Soliton collision = remix/crossover
print("\n--- Part 3: Soliton Collision = Creative Remix ---")
# When two narrative solitons collide:
# During collision: they interact nonlinearly (new story!)
# After collision: both emerge intact (original stories preserved)
# But phase shifts occur (each is slightly changed by the encounter)

# Simulate: Hero Journey collides with Forbidden Love
# Result during collision: "Romeo and Juliet" (new form)
# After collision: Hero Journey continues (Star Wars)
#                  Forbidden Love continues (Brokeback Mountain)
# Both changed by the encounter but fundamentally intact

print("  Collision: Hero Journey × Forbidden Love")
print("    During collision: 'Romeo and Juliet' (nonlinear interaction)")
print("    After collision: Hero Journey → 'Star Wars' (phase shifted)")
print("    After collision: Forbidden Love → 'Brokeback Mountain' (phase shifted)")
print("    Both archetypes SURVIVE the collision. That's what makes them solitons.")

# Part 4: Non-soliton ideas (dissipate over time)
print("\n--- Part 4: Non-Soliton Ideas (Dissipate) ---")
# Ideas that are NOT solitons: they spread but lose amplitude
# Fashion trends, slang, memes without depth
dissipative_ideas = {
    'Pet Rock':          {'amplitude': 2.0, 'decay': 0.5},
    'Disco':             {'amplitude': 3.0, 'decay': 0.3},
    'Mullets':           {'amplitude': 1.5, 'decay': 0.4},
    'Fidget Spinner':    {'amplitude': 2.5, 'decay': 0.8},
    'Y2K Panic':         {'amplitude': 2.0, 'decay': 0.9},
}

for name, props in dissipative_ideas.items():
    # Amplitude at t=10 years
    amp_10 = props['amplitude'] * np.exp(-props['decay'] * 10)
    print(f"    {name:20s}: initial={props['amplitude']:.1f}, at 10yr={amp_10:.3f} ({'GONE' if amp_10 < 0.1 else 'fading'})")

# Part 5: What makes an idea a soliton?
print("\n--- Part 5: Soliton Condition for Ideas ---")
print("An idea is a soliton if:")
print("  1. Nonlinearity: the idea gets STRONGER when challenged (stress=creativity)")
print("  2. Dispersion: the idea naturally wants to spread (cultural transmission)")
print("  3. Balance: strengthening rate = spreading rate")
print("")
print("  Nonlinearity >> Dispersion: idea becomes rigid dogma (no spread)")
print("  Dispersion >> Nonlinearity: idea becomes shallow trend (no depth)")
print("  Balance: idea maintains depth WHILE spreading = SOLITON")
print("")
print("  The Hero's Journey is a soliton because:")
print("    - It gets stronger when reinterpreted (nonlinear)")
print("    - It naturally spreads across cultures (dispersive)")
print("    - These rates are balanced (it's survived 5000+ years)")

# Part 6: Soliton creation formula
print("\n--- Part 6: How to Create a Soliton Idea ---")
# For KdV: soliton exists when nonlinearity 6u·u_x = dispersion u_xxx
# For ideas: challenge_response_rate = spread_rate

# Test: create a synthetic soliton idea
target_amplitude = 2.0
for spread_rate in [0.1, 0.3, 0.5, 0.7, 1.0]:
    # Nonlinearity needed to balance dispersion
    needed_nonlinearity = spread_rate  # balance condition
    
    # Can the idea strengthen at this rate when challenged?
    max_nonlinearity = target_amplitude * 0.5  # realistic limit
    
    balanced = abs(needed_nonlinearity - max_nonlinearity) < 0.2
    print(f"  spread={spread_rate:.1f}: need nonlinearity={needed_nonlinearity:.1f}, "
          f"max possible={max_nonlinearity:.1f}, {'✅ SOLITON' if balanced else '❌ unbalanced'}")

with open('EXPERIMENT-SOLITON.json', 'w') as f:
    json.dump({
        'soliton_archetypes': list(creative_solitons.keys()),
        'dissipative_trends': list(dissipative_ideas.keys()),
    }, f, indent=2)

print("\n=== SOLITON PRINCIPLE ===")
print("Great ideas are solitons: they maintain identity through transmission.")
print("Fashion trends dissipate: they spread but lose amplitude.")
print("Dogma is over-nonlinear: rigid, doesn't spread.")
print("The sweet spot: depth × spread = cultural soliton.")
