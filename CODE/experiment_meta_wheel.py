import numpy as np
import json
import time

print("=== Experiment 26: The Meta-Wheel (Autonomous R&D) ===\n")
print("The wheel designs its own experiments based on previous results.\n")

np.random.seed(42)
N = 500
dt = 0.01

def lorenz_step(state, sigma, rho, beta, dt):
    x, y, z = state[:, 0], state[:, 1], state[:, 2]
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return state + np.column_stack([dx, dy, dz]) * dt

def kuramoto_step(phases, freqs, K):
    z = np.mean(np.exp(1j * phases))
    phases += (freqs + K * np.imag(z * np.exp(-1j * phases))) * 0.01
    return phases

def soft_snap(x, epsilon):
    snapped = np.round(x)
    return (1 - epsilon) * snapped + epsilon * x

# The meta-wheel state
insights = []
params = {'sigma': 10.0, 'rho': 28.0, 'beta': 8/3, 'eps': 0.5, 'K': 1.0, 'N': 500}
surprises = []  # track unexpected results

EXPERIMENT_TYPES = [
    'lorenz_sweep',      # sweep one parameter
    'kuramoto_sync',     # sync dynamics
    'soft_snap_sweep',   # constraint sweep
    'coupled_systems',   # two systems interacting
    'noise_injection',   # add noise at different levels
    'evolutionary',      # genetic optimization
]

def run_mini_experiment(exp_type, params):
    """Run a quick experiment and return metrics."""
    
    if exp_type == 'lorenz_sweep':
        # Sweep rho around current value
        rho_range = np.linspace(max(1, params['rho'] - 10), params['rho'] + 10, 20)
        best_rho = params['rho']
        best_div = 0
        for rho in rho_range:
            state = np.random.randn(50, 3) * 0.1
            for _ in range(1000):
                state = lorenz_step(state, params['sigma'], rho, params['beta'], dt)
            div = float(np.std(state[:, 0]))
            if div > best_div:
                best_div = div
                best_rho = rho
        return {'best_rho': best_rho, 'best_div': best_div, 'type': 'lorenz_sweep'}
    
    elif exp_type == 'kuramoto_sync':
        phases = np.random.uniform(0, 2*np.pi, params['N'])
        freqs = np.random.normal(1.0, 0.5, params['N'])
        for _ in range(2000):
            phases = kuramoto_step(phases, freqs, params['K'])
        order = float(np.abs(np.mean(np.exp(1j * phases))))
        return {'order': order, 'K': params['K'], 'type': 'kuramoto_sync'}
    
    elif exp_type == 'soft_snap_sweep':
        eps_range = np.linspace(0.01, 2.0, 20)
        best_eps = 0.5
        best_output = 0
        for eps in eps_range:
            x = np.random.randn(1000) * 5
            output = soft_snap(x, eps)
            creativity = float(np.var(output) * np.mean(np.abs(np.gradient(output))))
            if creativity > best_output:
                best_output = creativity
                best_eps = eps
        return {'best_eps': best_eps, 'best_output': best_output, 'type': 'soft_snap_sweep'}
    
    elif exp_type == 'coupled_systems':
        state1 = np.random.randn(100, 3) * 0.1
        state2 = np.random.randn(100, 3) * 0.1
        K = params['eps'] * 0.1
        for _ in range(2000):
            state1 = lorenz_step(state1, params['sigma'], params['rho'], params['beta'], dt)
            state2 = lorenz_step(state2, params['sigma'] * 0.5, params['rho'] * 1.2, params['beta'], dt)
            coupling = K * (state2[:, 0] - state1[:, 0])
            state1[:, 0] += coupling * dt
            state2[:, 0] -= coupling * dt
        total_div = float(np.std(state1[:, 0]) + np.std(state2[:, 0]))
        corr = float(np.corrcoef(state1[:, 0], state2[:, 0])[0, 1])
        return {'total_div': total_div, 'correlation': corr, 'K': K, 'type': 'coupled_systems'}
    
    elif exp_type == 'noise_injection':
        state = np.random.randn(100, 3) * 0.1
        noise_levels = [0.001, 0.01, 0.1, 0.5, 1.0]
        best_noise = 0.01
        best_div = 0
        for noise in noise_levels:
            s = np.random.randn(100, 3) * 0.1
            for _ in range(2000):
                s = lorenz_step(s, params['sigma'], params['rho'], params['beta'], dt)
                s += np.random.randn(100, 3) * noise * np.sqrt(dt)
            div = float(np.std(s[:, 0]))
            if div > best_div:
                best_div = div
                best_noise = noise
        return {'best_noise': best_noise, 'best_div': best_div, 'type': 'noise_injection'}
    
    elif exp_type == 'evolutionary':
        # Quick evolution: 10 generations
        pop = 50
        rho_pop = np.random.uniform(10, 50, pop)
        sigma_pop = np.random.uniform(5, 15, pop)
        
        for gen in range(10):
            fitnesses = []
            for i in range(pop):
                state = np.random.randn(20, 3) * 0.1
                for _ in range(500):
                    state = lorenz_step(state, sigma_pop[i], rho_pop[i], 8/3, dt)
                fitnesses.append(float(np.std(state[:, 0])))
            
            # Select top half
            top = np.argsort(fitnesses)[-pop//2:]
            rho_pop = np.concatenate([rho_pop[top], rho_pop[top] + np.random.randn(pop//2) * 2])
            sigma_pop = np.concatenate([sigma_pop[top], sigma_pop[top] + np.random.randn(pop//2) * 0.5])
        
        return {'best_rho': float(np.mean(rho_pop)), 'best_sigma': float(np.mean(sigma_pop)),
                'best_fitness': float(max(fitnesses)), 'type': 'evolutionary'}

def extract_insight(result, params):
    """Extract insight from experiment result."""
    exp_type = result['type']
    
    if exp_type == 'lorenz_sweep':
        if abs(result['best_rho'] - params['rho']) > 5:
            return f"ρ sweet spot shifted: {params['rho']:.1f} → {result['best_rho']:.1f}"
        return f"ρ stable around {result['best_rho']:.1f}, diversity={result['best_div']:.4f}"
    
    elif exp_type == 'kuramoto_sync':
        if result['order'] > 0.9:
            return f"Full sync at K={result['K']:.2f} (order={result['order']:.4f})"
        elif result['order'] > 0.5:
            return f"Partial sync at K={result['K']:.2f} (order={result['order']:.4f})"
        return f"No sync at K={result['K']:.2f} (order={result['order']:.4f})"
    
    elif exp_type == 'soft_snap_sweep':
        return f"ε*={result['best_eps']:.3f} maximizes creative output={result['best_output']:.4f}"
    
    elif exp_type == 'coupled_systems':
        return f"Coupling K={result['K']:.3f}: total_div={result['total_div']:.4f}, corr={result['correlation']:.4f}"
    
    elif exp_type == 'noise_injection':
        return f"Optimal noise={result['best_noise']:.3f}, diversity={result['best_div']:.4f}"
    
    elif exp_type == 'evolutionary':
        return f"Evolved: ρ={result['best_rho']:.1f}, σ={result['best_sigma']:.1f}, fitness={result['best_fitness']:.4f}"
    
    return "Generic insight"

def update_params(params, result, insight):
    """Update params based on result — the learning step."""
    
    if result['type'] == 'lorenz_sweep':
        params['rho'] = 0.7 * params['rho'] + 0.3 * result['best_rho']
    elif result['type'] == 'kuramoto_sync':
        if result['order'] < 0.3:
            params['K'] *= 1.2  # increase coupling
        elif result['order'] > 0.95:
            params['K'] *= 0.8  # decrease coupling
    elif result['type'] == 'soft_snap_sweep':
        params['eps'] = 0.5 * params['eps'] + 0.5 * result['best_eps']
    elif result['type'] == 'coupled_systems':
        params['eps'] = 0.9 * params['eps'] + 0.1 * result['K'] * 10
    elif result['type'] == 'noise_injection':
        pass  # noise doesn't change base params (experiment 21 showed this)
    elif result['type'] == 'evolutionary':
        params['rho'] = 0.5 * params['rho'] + 0.5 * result['best_rho']
        params['sigma'] = 0.5 * params['sigma'] + 0.5 * result['best_sigma']
    
    return params

# MAIN LOOP
print("Starting autonomous R&D loop (20 iterations)...\n")

iteration_log = []

for i in range(20):
    # Choose experiment type (rotate through, with bias toward surprising results)
    exp_type = EXPERIMENT_TYPES[i % len(EXPERIMENT_TYPES)]
    
    # Run
    result = run_mini_experiment(exp_type, params)
    
    # Extract insight
    insight = extract_insight(result, params)
    
    # Check for surprise (divergence from expectation)
    if result['type'] == 'lorenz_sweep' and abs(result['best_rho'] - params['rho']) > 5:
        surprise = True
        surprises.append({'iteration': i, 'insight': insight})
    elif result['type'] == 'kuramoto_sync' and result['order'] < 0.3 and params['K'] > 2:
        surprise = True
        surprises.append({'iteration': i, 'insight': insight})
    else:
        surprise = False
    
    # Update params
    params = update_params(params, result, insight)
    
    iteration_log.append({
        'iteration': i,
        'experiment': exp_type,
        'result': {k: v for k, v in result.items()},
        'insight': insight,
        'surprise': surprise,
        'params_after': {k: v for k, v in params.items()}
    })
    
    print(f"  [{i:2d}/20] {exp_type:<20s} | {insight}")
    if surprise:
        print(f"         ⚡ SURPRISE!")

# Final analysis
print(f"\n{'='*60}")
print(f"META-WHEEL COMPLETE")
print(f"  Iterations: 20")
print(f"  Surprises: {len(surprises)}")
print(f"  Final params: σ={params['sigma']:.2f}, ρ={params['rho']:.2f}, "
      f"β={params['beta']:.2f}, ε={params['eps']:.3f}, K={params['K']:.2f}")

# Param evolution
print(f"\n  Parameter evolution:")
for i, log in enumerate(iteration_log):
    if i % 5 == 0:
        p = log['params_after']
        print(f"    iter {i:2d}: σ={p['sigma']:.2f}, ρ={p['rho']:.2f}, ε={p['eps']:.3f}, K={p['K']:.2f}")

# Convergence check
sigmas = [log['params_after']['sigma'] for log in iteration_log]
rhos = [log['params_after']['rho'] for log in iteration_log]
print(f"\n  σ range: {min(sigmas):.2f} → {max(sigmas):.2f}")
print(f"  ρ range: {min(rhos):.2f} → {max(rhos):.2f}")
print(f"  {'Parameters CONVERGING' if (max(sigmas)-min(sigmas)) < 5 else 'Parameters EXPLORING'}")

with open('CODE/EXPERIMENT-META-WHEEL.json', 'w') as f:
    json.dump({
        'iterations': iteration_log,
        'surprises': surprises,
        'final_params': params,
    }, f, indent=2, default=str)

print("\n=== AUTONOMOUS R&D LOOP DEMONSTRATED ===")
