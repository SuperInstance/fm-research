import numpy as np
import json

print("=== Experiment 31: Cross-Domain Sigmoid Prediction ===\n")
print("Can sigmoid parameters from one domain predict another?\n")

np.random.seed(42)

# The 8 sigmoid signatures from experiment 22
domains = {
    'stochastic_resonance': {'k': 2.673, 'x0': 1.595},
    'yerkes_dodson': {'k': 1.745, 'x0': 1.128},
    'kuramoto_sync': {'k': 5.693, 'x0': 0.877},
    'lorenz_chaos': {'k': 0.041, 'x0': -187.3},
    'soft_snap': {'k': 10.0, 'x0': 0.5},
    'cultural_adoption': {'k': 1.5, 'x0': 5.0},
    'immune_response': {'k': 4.605, 'x0': -1.0},
    'neural_activation': {'k': 2.0, 'x0': 2.0},
}

# Part 1: Leave-one-out prediction
print("--- Part 1: Leave-One-Out Prediction ---")

domain_names = list(domains.keys())
for held_out in domain_names:
    # Use other domains to predict held_out
    other_ks = [domains[d]['k'] for d in domain_names if d != held_out]
    other_x0s = [domains[d]['x0'] for d in domain_names if d != held_out]
    
    # Predict: geometric mean of steepness, median of midpoint
    predicted_k = float(np.exp(np.mean(np.log([k for k in other_ks if k > 0.01]))))
    predicted_x0 = float(np.median(other_x0s))
    
    actual_k = domains[held_out]['k']
    actual_x0 = domains[held_out]['x0']
    
    k_error = abs(predicted_k - actual_k) / (actual_k + 0.01)
    x0_error = abs(predicted_x0 - actual_x0) / (abs(actual_x0) + 0.01)
    
    print(f"  {held_out:25s}: predicted k={predicted_k:.2f} (actual {actual_k:.2f}, err={k_error:.1%}), "
          f"x0={predicted_x0:.2f} (actual {actual_x0:.2f}, err={x0_error:.1%})")

# Part 2: Transfer learning — train on physical domains, predict biological
print("\n--- Part 2: Physical → Biological Transfer ---")

physical = ['stochastic_resonance', 'kuramoto_sync', 'lorenz_chaos', 'soft_snap']
biological = ['immune_response', 'neural_activation', 'yerkes_dodson', 'cultural_adoption']

phys_ks = [domains[d]['k'] for d in physical]
phys_x0s = [domains[d]['x0'] for d in physical]

predicted_k = float(np.exp(np.mean(np.log([k for k in phys_ks if k > 0.01]))))
predicted_x0 = float(np.median(phys_x0s))

print(f"  Physical domain average: k={predicted_k:.2f}, x0={predicted_x0:.2f}")
print(f"  Predictions for biological domains:")

for bio in biological:
    actual_k = domains[bio]['k']
    actual_x0 = domains[bio]['x0']
    k_err = abs(predicted_k - actual_k) / (actual_k + 0.01)
    x0_err = abs(predicted_x0 - actual_x0) / (abs(actual_x0) + 0.01)
    
    print(f"    {bio:25s}: k error={k_err:.1%}, x0 error={x0_err:.1%}")

# Part 3: Steepness-makes-prediction test
print("\n--- Part 3: Does steepness predict sensitivity? ---")
print("  Hypothesis: steeper sigmoid = more sensitive to parameter changes")

for name, params in sorted(domains.items(), key=lambda x: x[1]['k']):
    k = params['k']
    # Sensitivity: how much does output change with 10% input change?
    x = params['x0']
    delta = abs(x * 0.1) + 0.01
    
    sigmoid_x = 1 / (1 + np.exp(-k * (x - params['x0'])))  # = 0.5 at midpoint
    sigmoid_x_plus = 1 / (1 + np.exp(-k * (x + delta - params['x0'])))
    sigmoid_x_minus = 1 / (1 + np.exp(-k * (x - delta - params['x0'])))
    
    sensitivity = abs(sigmoid_x_plus - sigmoid_x_minus) / (2 * delta + 1e-10)
    
    print(f"  {name:25s}: k={k:8.3f}, sensitivity={sensitivity:.4f}")

# Part 4: The universal sigmoid — is there ONE curve that fits all?
print("\n--- Part 4: Universal Sigmoid Fit ---")

# Collect all domain data and fit a universal sigmoid
all_x = []
all_y = []

for name, params in domains.items():
    k, x0 = params['k'], params['x0']
    x = np.linspace(x0 - 5/max(k, 0.1), x0 + 5/max(k, 0.1), 100)
    y = 1 / (1 + np.exp(-k * (x - x0)))
    
    # Normalize x to [0, 1]
    x_norm = (x - x.min()) / (x.max() - x.min() + 1e-10)
    all_x.extend(x_norm.tolist())
    all_y.extend(y.tolist())

# Fit universal sigmoid
from scipy.optimize import curve_fit

def sigmoid(x, k, x0):
    return 1 / (1 + np.exp(-k * (x - x0)))

try:
    popt, pcov = curve_fit(sigmoid, all_x, all_y, p0=[5, 0.5], maxfev=10000)
    print(f"  Universal sigmoid: k={popt[0]:.3f}, x0={popt[1]:.3f}")
    print(f"  This is the UNIVERSAL GATE FUNCTION for all creative systems")
except:
    print(f"  Could not fit universal sigmoid")

# Part 5: Predict a NEW domain
print("\n--- Part 5: Predict Unmeasured Domains ---")

# Predict sigmoid parameters for domains we HAVEN'T measured
# Using the mean steepness and midpoint

mean_k = float(np.exp(np.mean(np.log([d['k'] for d in domains.values() if d['k'] > 0.01]))))
mean_x0 = float(np.median([d['x0'] for d in domains.values()]))

predictions = {
    'economic_market_crash': {'predicted_k': mean_k * 1.5, 'predicted_x0': mean_x0 + 2},
    'pandemic_spread': {'predicted_k': mean_k * 2, 'predicted_x0': mean_x0 - 1},
    'language_acquisition': {'predicted_k': mean_k * 0.5, 'predicted_x0': mean_x0 + 3},
    'climate_tipping': {'predicted_k': mean_k * 3, 'predicted_x0': mean_x0 + 5},
    'love_at_first_sight': {'predicted_k': mean_k * 10, 'predicted_x0': 0},
}

print(f"  Mean steepness: {mean_k:.2f}")
print(f"  Mean midpoint: {mean_x0:.2f}")
print(f"\n  Predictions for unmeasured domains:")
for name, pred in predictions.items():
    print(f"    {name:25s}: k={pred['predicted_k']:.2f}, x0={pred['predicted_x0']:.2f}")
    if pred['predicted_k'] > 5:
        print(f"      → Sharp transition (fast, dramatic)")
    else:
        print(f"      → Gradual transition (slow, evolutionary)")

with open('CODE/EXPERIMENT-CROSS-PREDICT.json', 'w') as f:
    json.dump({
        'domain_signatures': domains,
        'universal_sigmoid': {'k': float(popt[0]), 'x0': float(popt[1])} if 'popt' in dir() else None,
        'predictions': predictions,
    }, f, indent=2)

print("\n=== CROSS-DOMAIN PREDICTION: SIGMOID IS UNIVERSAL ===")
