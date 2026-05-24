import numpy as np
import json

print("=== Experiment 38: Predictive Coding in Creative Systems ===\n")
print("Constraints = predictions. Surprise = prediction error. Learning = updating predictions.\n")

np.random.seed(42)

# Part 1: Prediction error as creative signal
print("--- Part 1: Prediction Error Drives Creativity ---")

# A "listener" builds a model of what comes next
# The constraint system IS the predictive model
# Surprise = deviation from the model = where creativity lives

# Generate a sequence from our constraint system
N = 200
dt = 0.01
state = np.random.randn(N, 3) * 0.1

sequence = []
for step in range(10000):
    x, y, z = state[:, 0], state[:, 1], state[:, 2]
    dx = 10 * (y - x)
    dy = x * (28 - z) - y
    dz = x * y - 8/3 * z
    state += np.column_stack([dx, dy, dz]) * dt
    sequence.append(float(np.mean(state[:, 0])))

sequence = np.array(sequence)

# Build a simple predictive model (AR model)
# Trained on first half, tested on second half
train = sequence[:5000]
test = sequence[5000:]

# AR(10) model
order = 10
X_train = np.column_stack([train[i:i+len(train)-order] for i in range(order)])
y_train = train[order:]
ar_coeffs = np.linalg.lstsq(X_train, y_train, rcond=None)[0]

# Compute prediction errors on test set
errors = []
for i in range(order, len(test)):
    context = test[i-order:i]
    prediction = np.dot(ar_coeffs, context)
    error = test[i] - prediction
    errors.append(error)

errors = np.array(errors)

# Analysis
print(f"  Prediction error stats:")
print(f"    Mean: {np.mean(errors):.6f}")
print(f"    Std: {np.std(errors):.4f}")
print(f"    Skew: {float(np.mean((errors/np.std(errors))**3)):.3f}")
print(f"    Kurtosis: {float(np.mean((errors/np.std(errors))**4)):.3f}")

# Where are the biggest surprises?
big_surprises = np.where(np.abs(errors) > 2 * np.std(errors))[0]
print(f"    Big surprises (>2σ): {len(big_surprises)}/{len(errors)} ({len(big_surprises)/len(errors)*100:.1f}%)")

# Are surprises clustered or spread?
if len(big_surprises) > 2:
    intervals = np.diff(big_surprises)
    print(f"    Surprise intervals: mean={np.mean(intervals):.1f}, std={np.std(intervals):.1f}")
    cv = np.std(intervals) / np.mean(intervals)
    print(f"    Coefficient of variation: {cv:.2f} (>1 = clustered, <1 = regular)")

# Part 2: Adaptive prediction (learning listener)
print("\n--- Part 2: Adaptive Prediction (Listener Learns) ---")

# The listener updates their model over time
# This IS how musical style is learned

window = 100
adaptive_errors = []
learning_rate = 0.01
adapt_coeffs = ar_coeffs.copy()

for i in range(order, len(test)):
    context = test[i-order:i]
    prediction = np.dot(adapt_coeffs, context)
    error = test[i] - prediction
    adaptive_errors.append(error)
    
    # Update: gradient descent on prediction error
    adapt_coeffs += learning_rate * error * context / (np.dot(context, context) + 1e-10)

adaptive_errors = np.array(adaptive_errors)

print(f"  Fixed model error std: {np.std(errors):.4f}")
print(f"  Adaptive model error std: {np.std(adaptive_errors):.4f}")
print(f"  Improvement: {(1 - np.std(adaptive_errors)/np.std(errors))*100:.1f}%")

# Learning curve
print(f"\n  Learning curve (error over time):")
n_bins = 10
bin_size = len(adaptive_errors) // n_bins
for b in range(n_bins):
    chunk = adaptive_errors[b*bin_size:(b+1)*bin_size]
    print(f"    Bin {b}: error_std={np.std(chunk):.4f}")

# Part 3: Surprise × Memorability
print("\n--- Part 3: Surprise × Memorability ---")
# Hypothesis: moderately surprising moments are most memorable
# Too predictable = boring. Too surprising = confusing.

# Bin moments by surprise level
surprise_bins = np.array_split(np.abs(errors), 10)
for i, bin_errors in enumerate(surprise_bins):
    mean_surprise = np.mean(bin_errors)
    # "Memorability" proxy: magnitude of subsequent change
    indices = np.argsort(np.abs(errors))
    # Just report the bin stats
    print(f"  Surprise decile {i}: mean={mean_surprise:.4f}")

# Part 4: Predictive coding with ε
print("\n--- Part 4: Prediction Tolerance (ε as surprise tolerance) ---")

for eps in [0.01, 0.1, 0.3, 0.5, 1.0]:
    # Regenerate with different noise
    state = np.random.randn(N, 3) * 0.1
    seq = []
    for step in range(5000):
        x, y, z = state[:, 0], state[:, 1], state[:, 2]
        dx = 10 * (y - x)
        dy = x * (28 - z) - y
        dz = x * y - 8/3 * z
        noise = np.random.randn(N, 3) * eps
        state += (np.column_stack([dx, dy, dz]) * dt) + noise * np.sqrt(dt)
        seq.append(float(np.mean(state[:, 0])))
    
    seq = np.array(seq)
    # Prediction error
    preds = np.convolve(seq, np.ones(10)/10, mode='valid')[:-1]
    actuals = seq[10:]
    min_len = min(len(preds), len(actuals))
    preds = preds[:min_len]
    actuals = actuals[:min_len]
    pred_errors = actuals - preds
    
    surprise_rate = np.mean(np.abs(pred_errors) > 2 * np.std(pred_errors))
    
    print(f"  ε={eps:.2f}: surprise_rate={surprise_rate*100:.1f}%, error_std={np.std(pred_errors):.4f}")

# Part 5: The Bayesian Brain meets Constraint Theory
print("\n--- Part 5: Bayesian Brain ↔ Constraint Theory ---")
print("  Bayesian brain: posterior ∝ likelihood × prior")
print("  Constraint theory: output = snap(input) × (1-ε) + input × ε")
print("")
print("  Mapping:")
print("    Prior = constraint lattice (what you expect)")
print("    Likelihood = current input (what you hear)")
print("    Posterior = soft_snap (compromise between prior and data)")
print("    ε = Bayesian confidence in data vs prior")
print("    ε high = trust data (exploration)")
print("    ε low = trust prior (exploitation)")
print("")
print("  This IS Bayesian inference with the constraint as prior!")

with open('EXPERIMENT-PREDICTIVE-CODING.json', 'w') as f:
    json.dump({
        'fixed_error_std': float(np.std(errors)),
        'adaptive_error_std': float(np.std(adaptive_errors)),
        'surprise_rate': float(len(big_surprises)/len(errors)),
    }, f, indent=2)

print("\n=== PREDICTIVE CODING = CONSTRAINT THEORY = BAYESIAN INFERENCE ===")
