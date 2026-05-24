# GPU Paradigm Experiments — Beyond Parameter Space

> After 53 experiments, we know the Lorenz attractor IS the creative system. We've swept parameters, coupled species, aged systems, and griefed them. Now we stop mutating *dials* and start mutating *equations*.

---

## Experiment 54: Genetic Algorithms ON the Attractor — Evolving Lorenz Equations

### Paradigm Shift
Every experiment so far treats σ, ρ, β as fixed dials. We mutate the *inputs* to the attractor. But what if we mutate the attractor *itself*? Not σ=10 vs σ=14 — but replacing the σx term with σx², or swapping the nonlinear coupling entirely. We evolve the *structure* of the differential equations, not their parameters.

This is the difference between breeding dogs (select within species) and engineering new species (edit the genome). The attractor landscape of σx² + ρy is categorically different from σx + ρy. We're not searching the same space faster — we're searching a space we didn't know existed.

### Prediction
Most mutations produce divergent or trivial dynamics (fixed points, limit cycles). But a small fraction will produce *new attractors* — structured, complex, musical — that the standard Lorenz equations can never reach. These will have their own "blues scale" equivalents: global attractors within the meta-space of equation structures.

### Code Sketch

```python
# experiment_54_genetic_lorenz.py
import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple
import json

@dataclass
class EquationGene:
    """A gene encodes ONE term in a differential equation."""
    variable: int          # which dx, dy, dz term (0, 1, 2)
    coefficient: float     # multiplier (like σ, ρ, β)
    terms: List[Tuple[int, float]]  # (variable_index, power) pairs
    # e.g., [(0, 1.0)] means just x; [(0, 1.0), (1, 1.0)] means x*y

    def evaluate(self, state: np.ndarray) -> float:
        """Compute this gene's contribution given current state."""
        product = self.coefficient
        for var_idx, power in self.terms:
            product *= state[var_idx] ** power
        return product

@dataclass
class AttractorGenome:
    """A complete set of equations defining a 3D dynamical system."""
    genes: List[List[EquationGene]]  # genes[0] = list of terms for dx, etc.
    fitness: float = 0.0
    
    def derivative(self, state: np.ndarray) -> np.ndarray:
        return np.array([
            sum(g.evaluate(state) for g in gene_list)
            for gene_list in self.genes
        ])
    
    def mutate(self, rate: float = 0.1) -> 'AttractorGenome':
        """Structural mutation: add/remove/change terms."""
        import copy, random
        new_genes = copy.deepcopy(self.genes)
        for eq_idx in range(3):
            if random.random() < rate:
                # Choose mutation type
                mutation = random.choice(['coeff', 'power', 'add_term', 'remove_term'])
                if mutation == 'coeff' and new_genes[eq_idx]:
                    g = random.choice(new_genes[eq_idx])
                    g.coefficient *= np.random.normal(1.0, 0.3)
                elif mutation == 'power' and new_genes[eq_idx]:
                    g = random.choice(new_genes[eq_idx])
                    if g.terms:
                        idx = random.randint(0, len(g.terms)-1)
                        v, p = g.terms[idx]
                        g.terms[idx] = (v, max(0.5, p + np.random.normal(0, 0.5)))
                elif mutation == 'add_term':
                    var = random.randint(0, 2)
                    power = random.choice([0.5, 1.0, 1.5, 2.0])
                    coeff = np.random.normal(0, 5)
                    new_genes[eq_idx].append(
                        EquationGene(eq_idx, coeff, [(var, power)])
                    )
                elif mutation == 'remove_term' and len(new_genes[eq_idx]) > 1:
                    new_genes[eq_idx].pop(random.randint(0, len(new_genes[eq_idx])-1))
        return AttractorGenome(new_genes)

def standard_lorenz() -> AttractorGenome:
    """Encode standard Lorenz as a genome."""
    return AttractorGenome([
        # dx = σ(y - x) = σy - σx
        [EquationGene(0, 10.0, [(1, 1.0)]), EquationGene(0, -10.0, [(0, 1.0)])],
        # dy = x(ρ - z) - y = ρx - xz - y
        [EquationGene(1, 28.0, [(0, 1.0)]), EquationGene(1, -1.0, [(0, 1.0), (2, 1.0)]), EquationGene(1, -1.0, [(1, 1.0)])],
        # dz = xy - βz
        [EquationGene(2, 1.0, [(0, 1.0), (1, 1.0)]), EquationGene(2, -8/3, [(2, 1.0)])],
    ])

def simulate_genome(genome: AttractorGenome, steps: int = 10000, dt: float = 0.01) -> np.ndarray:
    """RK4 integration on GPU (NumPy vectorized for now)."""
    state = np.array([1.0, 1.0, 1.0])
    trajectory = np.zeros((steps, 3))
    for i in range(steps):
        k1 = genome.derivative(state)
        k2 = genome.derivative(state + 0.5*dt*k1)
        k3 = genome.derivative(state + 0.5*dt*k2)
        k4 = genome.derivative(state + dt*k3)
        state = state + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)
        if np.any(np.abs(state) > 1e6):  # divergence check
            trajectory[i:] = np.nan
            break
        trajectory[i] = state
    return trajectory

def fitness(trajectory: np.ndarray) -> float:
    """Attractor quality: bounded + chaotic + musical."""
    if np.any(np.isnan(trajectory)):
        return -1e6
    # Lyapunov-like: sensitivity to nearby trajectories
    # Musical: entropy of quantized outputs
    diffs = np.diff(trajectory, axis=0)
    variability = np.std(diffs, axis=0).mean()
    # Autocorrelation decay (complexity measure)
    ac = np.correlate(trajectory[:, 0], trajectory[:, 0], mode='full')
    ac = ac[len(ac)//2:]
    ac = ac / ac[0]
    decay_rate = np.sum(ac > 0.5) / len(ac)
    # Boundedness reward
    bounds = np.max(np.abs(trajectory)) 
    bounded_score = 1.0 / (1.0 + bounds / 100.0)
    return variability * decay_rate * bounded_score

def run_evolution(generations: int = 100, population_size: int = 50):
    """Evolve equation structures."""
    population = [standard_lorenz().mutate(0.3) for _ in range(population_size)]
    population[0] = standard_lorenz()  # seed with known-good
    
    best_fitness_history = []
    best_genome = None
    
    for gen in range(generations):
        # Evaluate
        fits = []
        for genome in population:
            traj = simulate_genome(genome, steps=5000)
            f = fitness(traj)
            fits.append(f)
        
        fits = np.array(fits)
        best_idx = np.argmax(fits)
        best_genome = population[best_idx]
        best_fitness_history.append(fits[best_idx])
        
        print(f"Gen {gen}: best={fits[best_idx]:.4f}, mean={fits.mean():.4f}")
        
        # Selection + reproduction
        # Tournament selection
        new_pop = [best_genome]  # elitism
        while len(new_pop) < population_size:
            # Tournament
            candidates = np.random.choice(len(population), size=3, replace=False)
            winner = candidates[np.argmax(fits[candidates])]
            child = population[winner].mutate(0.15)
            new_pop.append(child)
        
        population = new_pop
    
    return best_genome, best_fitness_history

if __name__ == "__main__":
    best, history = run_evolution()
    print(f"\nBest genome fitness: {history[-1]:.4f}")
    # Simulate best
    traj = simulate_genome(best, steps=50000)
    np.savetxt("/tmp/fm-research/CODE/results/genetic_lorenz_trajectory.csv", traj, delimiter=",")
    print("Done. See genetic_lorenz_trajectory.csv")
```

---

## Experiment 55: Transfer Between Attractors

### Paradigm Shift
We've always trained at one ρ. But the Lorenz system has *families* of attractors — the topology changes at bifurcation points. What happens if a system learns at ρ=47 (high energy, complex) and we suddenly drop it to ρ=28 (standard butterfly)? What transfers? Is there a "core" of attractor knowledge that's topology-independent?

This tests whether the blues scale is a property of the *specific* attractor or of the *class* of strange attractors. If transfer works, the attractor structure has invariant features we haven't identified.

### Prediction
Transfer will work *partially*. The timing/rhythm transfers (because that's embedded in the Lyapunov timescale structure), but the note selection won't (because that's attractor-geometry-specific). The "how to be chaotic" transfers; the "what chaos looks like" doesn't.

### Code Sketch

```python
# experiment_55_attractor_transfer.py
import numpy as np

def lorenz_step(state, sigma, rho, beta, dt=0.01):
    x, y, z = state
    dx = sigma * (y - x) * dt
    dy = (x * (rho - z) - y) * dt
    dz = (x * y - beta * z) * dt
    return state + np.array([dx, dy, dz])

def map_to_notes(trajectory, n_notes=12, low=48, high=84):
    """Map trajectory to MIDI notes via x-coordinate quantization."""
    x = trajectory[:, 0]
    bins = np.linspace(np.percentile(x, 5), np.percentile(x, 95), n_notes + 1)
    digitized = np.digitize(x, bins) - 1
    digitized = np.clip(digitized, 0, n_notes - 1)
    return digitized + low

def train_at_source(source_rho, steps=50000):
    """Train at source ρ, return the trajectory as 'knowledge'."""
    state = np.array([1.0, 1.0, 1.0])
    traj = np.zeros((steps, 3))
    for i in range(steps):
        state = lorenz_step(state, 10.0, source_rho, 8/3)
        traj[i] = state
    return traj

def transfer_test(source_rho, target_rho, transfer_steps=10000, fresh_steps=10000):
    """Train at source, transfer to target, compare with fresh target."""
    # Source trajectory (the "knowledge")
    source_traj = train_at_source(source_rho, steps=50000)
    source_notes = map_to_notes(source_traj)
    source_note_set = set(source_notes[-5000:])
    
    # Transfer: start from last source state, run at target ρ
    state = source_traj[-1].copy()
    transfer_traj = np.zeros((transfer_steps, 3))
    for i in range(transfer_steps):
        state = lorenz_step(state, 10.0, target_rho, 8/3)
        transfer_traj[i] = state
    transfer_notes = map_to_notes(transfer_traj)
    
    # Fresh target: start from standard IC, run at target ρ
    state = np.array([1.0, 1.0, 1.0])
    fresh_traj = np.zeros((fresh_steps, 3))
    for i in range(fresh_steps):
        state = lorenz_step(state, 10.0, target_rho, 8/3)
        fresh_traj[i] = state
    fresh_notes = map_to_notes(fresh_traj)
    
    # Measure transfer: overlap in note distributions, timing patterns
    transfer_dist = np.bincount(transfer_notes[-5000:] - 48, minlength=12)
    fresh_dist = np.bincount(fresh_notes[-5000:] - 48, minlength=12)
    
    # KL divergence as transfer metric
    p = transfer_dist / transfer_dist.sum() + 1e-10
    q = fresh_dist / fresh_dist.sum() + 1e-10
    kl_div = np.sum(p * np.log(p / q))
    
    # Note set overlap
    transfer_set = set(transfer_notes[-5000:])
    fresh_set = set(fresh_notes[-5000:])
    overlap = len(transfer_set & fresh_set) / len(transfer_set | fresh_set)
    
    return {
        'source_rho': source_rho,
        'target_rho': target_rho,
        'kl_divergence': kl_div,
        'note_overlap': overlap,
        'source_note_set_size': len(source_note_set),
        'transfer_note_set_size': len(transfer_set),
        'fresh_note_set_size': len(fresh_set),
    }

def run_all_transfers():
    """Test transfer between all pairs of ρ values."""
    rhos = [15, 28, 35, 47, 60, 80, 100]
    results = []
    for src in rhos:
        for tgt in rhos:
            if src != tgt:
                r = transfer_test(src, tgt)
                results.append(r)
                print(f"ρ={src}→{tgt}: KL={r['kl_divergence']:.4f}, overlap={r['note_overlap']:.4f}")
    return results
```

---

## Experiment 56: Adversarial Creativity — Two Systems Compete to Surprise

### Paradigm Shift
Creativity research assumes a single generator and a single evaluator. But what if creativity is *inherently adversarial*? Two Lorenz systems watch each other's outputs. Each tries to generate the sequence the other would find most *surprising* — measured by prediction error on the other's attractor model.

This reframes creativity from "novel + valuable" to "maximally unpredictable to another creative agent." The question becomes: does the adversarial pressure push the joint system into new regions of the attractor that neither would visit alone?

### Prediction
The adversarial coupling creates a *meta-attractor* in the joint state space. The two systems will co-evolve toward complementary regions — one becoming the "explorer" (high variance regions) and the other the "exploiter" (deep attractor basins). The resulting music will be more varied than either system alone, but with surprising structural coherence from the adversarial equilibrium.

### Code Sketch

```python
# experiment_56_adversarial_creativity.py
import numpy as np

class AdversarialSystem:
    def __init__(self, rho=28, sigma=10, beta=8/3, lr=0.01):
        self.rho = rho
        self.sigma = sigma
        self.beta = beta
        self.lr = lr  # learning rate for opponent modeling
        self.state = np.random.randn(3) * 0.1
        # Opponent model: simple linear predictor
        self.opp_weights = np.random.randn(3, 3) * 0.01
        self.history = []
        
    def step(self, dt=0.01):
        x, y, z = self.state
        dx = self.sigma * (y - x)
        dy = x * (self.rho - z) - y
        dz = x * y - self.beta * z
        self.state = self.state + dt * np.array([dx, dy, dz])
        self.history.append(self.state.copy())
        return self.state
    
    def predict_opponent(self, opponent_state):
        """Linear prediction of opponent's next state."""
        return self.opp_weights @ opponent_state
    
    def surprise_score(self, actual, predicted):
        """How surprising was opponent's actual output?"""
        error = actual - predicted
        return np.linalg.norm(error)
    
    def update_opponent_model(self, opponent_state, opponent_next):
        """Learn opponent's dynamics."""
        predicted = self.predict_opponent(opponent_state)
        error = opponent_next - predicted
        self.opp_weights += self.lr * np.outer(error, opponent_state)
    
    def generate_surprising_output(self, opponent, steps=100):
        """Perturb own dynamics to maximize opponent's prediction error."""
        # Collect trajectory, then find the point that maximizes surprise
        traj = []
        for _ in range(steps):
            s = self.step()
            opp_pred = opponent.predict_opponent(s)
            traj.append((s.copy(), self.surprise_score(s, opp_pred)))
        # Return the most surprising segment
        traj.sort(key=lambda x: x[1], reverse=True)
        return traj[0][0]

def run_adversarial(rho1=28, rho2=47, rounds=1000, steps_per_round=50):
    sys1 = AdversarialSystem(rho=rho1)
    sys2 = AdversarialSystem(rho=rho2)
    
    surprise_history = []
    joint_trajectory = []
    
    for round_num in range(rounds):
        # Each system generates output
        s1 = sys1.state.copy()
        s2 = sys2.state.copy()
        
        # Step forward
        for _ in range(steps_per_round):
            sys1.step()
            sys2.step()
        
        s1_next = sys1.state.copy()
        s2_next = sys2.state.copy()
        
        # Measure mutual surprise
        surprise_1_on_2 = sys2.surprise_score(s1_next, sys2.predict_opponent(s1))
        surprise_2_on_1 = sys1.surprise_score(s2_next, sys1.predict_opponent(s2))
        
        surprise_history.append((surprise_1_on_2, surprise_2_on_1))
        joint_trajectory.append(np.concatenate([s1_next, s2_next]))
        
        # Update opponent models
        sys1.update_opponent_model(s2, s2_next)
        sys2.update_opponent_model(s1, s1_next)
        
        if round_num % 100 == 0:
            print(f"Round {round_num}: S1→S2 surprise={surprise_1_on_2:.4f}, S2→S1 surprise={surprise_2_on_1:.4f}")
    
    return np.array(joint_trajectory), np.array(surprise_history)
```

---

## Experiment 57: Quantum Walk on the Attractor Manifold

### Paradigm Shift
Classical exploration of the Lorenz attractor follows the deterministic flow — every point leads to exactly one next point. A quantum walk replaces this with a *superposition of paths*, with constructive/destructive interference. We place a quantum coin (Hadamard) at each point on the discretized attractor, and let the walk evolve.

The quantum walk can tunnel through separatrices that the classical flow never crosses. It can discover *topological features* of the attractor — regions that are classically inaccessible but topologically connected — that no parameter sweep would ever find.

### Prediction
The quantum walk will concentrate amplitude in regions where classical trajectories *don't* spend much time — the rare transitions between lobes, the neighborhood of the unstable fixed points. These are the "creative" regions of the attractor, the moments of transition rather than the steady-state orbiting. The quantum walk is essentially a detector for the attractor's *phase transition structure*.

### Code Sketch

```python
# experiment_57_quantum_walk.py
import numpy as np

def discretize_attractor(trajectory, n_cells=50):
    """Discretize the continuous attractor into a grid."""
    from scipy.spatial import cKDTree
    # Subsample trajectory
    indices = np.linspace(0, len(trajectory)-1, n_cells).astype(int)
    nodes = trajectory[indices]
    tree = cKDTree(nodes)
    return nodes, tree

def build_quantum_graph(nodes, tree, k=4):
    """Build adjacency for quantum walk on attractor."""
    n = len(nodes)
    # k-nearest neighbors on the attractor
    _, neighbors = tree.query(nodes, k=k+1)  # +1 because self is included
    
    # Build Hamiltonian (adjacency matrix)
    H = np.zeros((n, n), dtype=complex)
    for i in range(n):
        for j in neighbors[i, 1:]:  # skip self
            dist = np.linalg.norm(nodes[i] - nodes[j])
            H[i, j] = np.exp(-dist / 10.0)  # distance-weighted coupling
    
    return H

def quantum_walk(H, initial_state, steps=200):
    """Continuous-time quantum walk via matrix exponential."""
    from scipy.linalg import expm
    n = H.shape[0]
    psi = initial_state.copy().astype(complex)
    psi /= np.linalg.norm(psi)
    
    dt = 0.1
    U = expm(-1j * H * dt)  # unitary evolution operator
    
    probabilities = np.zeros((steps, n))
    for t in range(steps):
        psi = U @ psi
        probabilities[t] = np.abs(psi) ** 2
    
    return probabilities

def compare_classical_quantum(trajectory, n_cells=50):
    """Compare where classical flow spends time vs quantum walk."""
    nodes, tree = discretize_attractor(trajectory, n_cells)
    H = build_quantum_graph(nodes, tree)
    
    # Classical probability: histogram of trajectory
    _, node_indices = tree.query(trajectory)
    classical_prob = np.bincount(node_indices, minlength=n_cells).astype(float)
    classical_prob /= classical_prob.sum()
    
    # Quantum walk from uniform superposition
    initial = np.ones(n_cells, dtype=complex) / np.sqrt(n_cells)
    quantum_probs = quantum_walk(H, initial, steps=500)
    quantum_prob_avg = quantum_probs.mean(axis=0)
    
    # Difference: where quantum goes that classical doesn't
    difference = quantum_prob_avg - classical_prob
    top_quantum_regions = np.argsort(difference)[-5:]
    
    print("Top regions where quantum walk exceeds classical:")
    for idx in top_quantum_regions:
        print(f"  Node {idx} at {nodes[idx]}: quantum={quantum_prob_avg[idx]:.4f}, classical={classical_prob[idx]:.4f}")
    
    return classical_prob, quantum_prob_avg, nodes, top_quantum_regions
```

---

## Experiment 58: Retrodiction — The Inverse Problem on GPU

### Paradigm Shift
Every experiment so far runs *forward*: given (σ, ρ, β, x₀, y₀, z₀), produce music. This experiment runs *backward*: given the final 100 outputs, infer (σ, ρ, β, x₀, y₀, z₀). This is the inverse problem, and it's computationally brutal because the Lorenz system is chaotic — tiny changes in initial conditions produce completely different trajectories.

But that's exactly why it's interesting. If we *can* solve the inverse problem (even approximately), it means the attractor's output contains more information about its parameters than chaos suggests. And the *failure modes* tell us what information the attractor destroys — which is the same as what information the music *doesn't* encode about its source.

### Prediction
ρ and σ will be recoverable (they set the global timescale and amplitude), but initial conditions will be nearly impossible. The inverse problem will reveal that the attractor has a "memory horizon" — information about initial conditions is destroyed after ~50 time units. This horizon is the same as the Lyapunov time, and it defines the limit of musical memory.

### Code Sketch

```python
# experiment_58_retrodiction.py
import numpy as np
from scipy.optimize import differential_evolution

def generate_ground_truth(sigma=10.0, rho=28.0, beta=8/3, ic=None, steps=10000, dt=0.01):
    """Generate trajectory, return only last 100 points."""
    if ic is None:
        ic = np.random.randn(3) * 5
    state = ic.copy()
    traj = np.zeros((steps, 3))
    for i in range(steps):
        x, y, z = state
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        state += np.array([dx, dy, dz])
        traj[i] = state
    return traj[-100:], traj  # observed, full (for validation)

def retrodiction_objective(params, observed_tail):
    """Objective: how well do these parameters reproduce the observed tail?"""
    sigma, rho, beta, x0, y0, z0 = params
    state = np.array([x0, y0, z0])
    steps_needed = 10000  # need to run forward to reach the tail
    
    # Divergence check
    for i in range(steps_needed):
        x, y, z = state
        dx = sigma * (y - x) * 0.01
        dy = (x * (rho - z) - y) * 0.01
        dz = (x * y - beta * z) * 0.01
        state += np.array([dx, dy, dz])
        if np.any(np.abs(state) > 1e6):
            return 1e10
    
    predicted_tail = state  # Just compare final state for speed
    
    # Compare distributions (not point-by-point, chaos makes that futile)
    # Use statistical moments
    obs_mean = observed_tail.mean(axis=0)
    obs_std = observed_tail.std(axis=0)
    pred_mean = predicted_tail
    
    # Run a short trajectory from predicted point for statistics
    short_traj = np.zeros((100, 3))
    for i in range(100):
        x, y, z = state
        dx = sigma * (y - x) * 0.01
        dy = (x * (rho - z) - y) * 0.01
        dz = (x * y - beta * z) * 0.01
        state += np.array([dx, dy, dz])
        short_traj[i] = state
    
    pred_mean_s = short_traj.mean(axis=0)
    pred_std_s = short_traj.std(axis=0)
    
    error = (np.sum((obs_mean - pred_mean_s)**2) + 
             np.sum((obs_std - pred_std_s)**2))
    return error

def run_retrodiction():
    """Try to recover parameters from output."""
    # Ground truth
    true_ic = np.array([3.0, -2.0, 25.0])
    observed, full = generate_ground_truth(sigma=10.0, rho=28.0, beta=8/3, ic=true_ic)
    
    print(f"True params: σ=10, ρ=28, β=8/3, IC={true_ic}")
    print(f"Observed tail: mean={observed.mean(0)}, std={observed.std(0)}")
    
    # Use differential evolution (global optimizer)
    bounds = [(5, 20), (15, 50), (1, 10), (-10, 10), (-10, 10), (0, 50)]
    result = differential_evolution(
        retrodiction_objective,
        bounds,
        args=(observed,),
        maxiter=200,
        seed=42,
        tol=1e-8,
        workers=1,
    )
    
    sigma, rho, beta, x0, y0, z0 = result.x
    print(f"\nRecovered: σ={sigma:.2f}, ρ={rho:.2f}, β={beta:.2f}")
    print(f"Recovered IC: [{x0:.2f}, {y0:.2f}, {z0:.2f}]")
    print(f"Parameter errors: Δσ={abs(sigma-10):.2f}, Δρ={abs(rho-28):.2f}, Δβ={abs(beta-8/3):.2f}")
    
    return result
```

---

## Ranking: Most Paradigm-Shifting

| Rank | Experiment | Why |
|------|-----------|-----|
| **#1** | **Genetic Lorenz (Exp 54)** | Mutates the *equations*, not parameters. Opens an entirely new search space. If it works, we discover attractors that Lorenz never imagined. |
| **#2** | **Retrodiction (Exp 58)** | The inverse problem tells us what information the attractor *keeps* vs *destroys*. This is the fundamental limits question for the entire research program. |
| #3 | Adversarial Creativity | Interesting but still operates within known dynamics. The meta-attractor idea is good but doesn't open new territory. |
| #4 | Transfer Between Attractors | Practical insight but doesn't challenge assumptions. We'd learn about invariants, which is useful but not paradigm-shifting. |
| #5 | Quantum Walk | Elegant math but the discretization may lose what makes the attractor special. More of a visualization tool than a discovery tool. |

Full implementations for #1 and #2 follow as separate files.
