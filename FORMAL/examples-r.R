#!/usr/bin/env Rscript
# =============================================================================
# constraint-theory-core R Examples
# Demonstrates each module of the constraint theory system.
# =============================================================================

cat("=== Constraint Theory Core - R Examples ===\n\n")

# Source the main file
source("FORMAL/constraint-theory-core.R")

# --- 1. A2 Lattice ---
cat("--- A2 Lattice ---\n")

# Snap some points
test_points <- rbind(
  c(0.5, 0.3),
  c(1.2, 0.8),
  c(-0.7, 1.1),
  c(0.0, 0.0),
  c(0.3, SQRT_3/2)
)

for (i in seq_len(nrow(test_points))) {
  res <- a2_snap(test_points[i,1], test_points[i,2])
  cat(sprintf("  snap(%.2f, %.2f) -> A2Point(%d, %d), error=%.6f, safe=%s\n",
              test_points[i,1], test_points[i,2],
              res$point$a, res$point$b, res$error,
              is_safe(res$error)))
}

cat(sprintf("  Covering radius: %.6f\n", a2_covering_radius()))
cat(sprintf("  Safe threshold: %.6f\n", SAFE_THRESHOLD))

# Soft snap
ss <- soft_snap(0.5, 0.3, epsilon = 0.3)
cat(sprintf("  soft_snap(0.5, 0.3, eps=0.3) -> (%.4f, %.4f), error=%.6f\n",
            ss$xy[1], ss$xy[2], ss$error))

# Dodecet encoding
dir <- decode_dodecet(0)
cat(sprintf("  Dodecet 0: (%d, %d)\n", dir[1], dir[2]))
idx <- encode_dodecet(dir[1], dir[2])
cat(sprintf("  Encoded back: %d\n", idx))

# Vector48
angle_idx <- vector48_encode(pi/4)
cat(sprintf("  pi/4 -> direction %d -> angle %.4f rad\n", angle_idx, vector48_decode(angle_idx)))

cat("\n")

# --- 2. Deadband Funnel ---
cat("--- Deadband Funnel (Temporal Agent) ---\n")

agent <- temporal_agent(decay_rate = 0.1)

observations <- list(
  c(0.1, 0.3, 1.0),
  c(0.12, 0.28, 2.0),
  c(0.11, 0.31, 3.0),
  c(0.5, 0.5, 4.0),  # Should be anomaly
  c(0.1, 0.3, 5.0)   # After reset
)

for (obs in observations) {
  res <- agent$observe(obs[1], obs[2], t = obs[3])
  cat(sprintf("  t=%.1f: phase=%s, error=%.4f, deadband=%.4f, anomalies=%d\n",
              obs[3], res$phase, res$error, res$deadband, agent$anomaly_count()))
}

cat("\n")

# --- 3. Laman Rigidity ---
cat("--- Laman Rigidity ---\n")

# Build Laman graphs of various sizes
for (n in c(3, 5, 8, 10)) {
  edges <- henneberg_construct(n)
  cat(sprintf("  n=%d: %d edges, is_laman=%s\n",
              n, nrow(edges), is_laman(n, edges)))
}

# Algebraic connectivity
edges6 <- henneberg_construct(6)
ac <- algebraic_connectivity(edges6, 6)
oc <- optimal_coupling(edges6, 6)
cat(sprintf("  n=6: lambda_2=%.6f, alpha*=%.6f\n", ac, oc))

# Soft rigidity
sr_hard <- soft_rigidity(6, edges6, epsilon = 0.0)
sr_soft <- soft_rigidity(6, edges6, epsilon = 0.3)
cat(sprintf("  n=6: soft_rigidity(eps=0)=%.2f, soft_rigidity(eps=0.3)=%.4f\n", sr_hard, sr_soft))

# Non-Laman graph
bad_edges <- rbind(c(0,1), c(1,2))
cat(sprintf("  3 vertices, 2 edges: is_laman=%s\n", is_laman(3, bad_edges)))

cat("\n")

# --- 4. Metronome Consensus ---
cat("--- Metronome Consensus ---\n")

# Create 5 agents with different initial phases
n_agents <- 5L
edges5 <- henneberg_construct(n_agents)

agents <- lapply(seq_len(n_agents), function(i) {
  metronome(
    T = 1.0,
    phi0 = runif(1, 0, 2 * pi),
    epsilon = 0.577,
    delta = 0.577,
    edges = edges5,
    n_agents = n_agents
  )
})

cat(sprintf("  %d agents, %d edges\n", n_agents, nrow(edges5)))

# Run consensus rounds
history <- data.frame()
for (round in seq_len(20)) {
  for (a in agents) a$tick()
  agents <- consensus_round(agents, edges5)

  for (i in seq_along(agents)) {
    corrs <- agents[[i]]$corrections()
    if (length(corrs) > 0) {
      history <- rbind(history, data.frame(
        tick = round,
        agent = i,
        correction = tail(corrs, 1)
      ))
    }
  }
}

# Check convergence
converged_count <- sum(sapply(agents, function(a) a$converged()))
cat(sprintf("  After 20 rounds: %d/%d agents converged\n", converged_count, n_agents))

# Show final phases
phases <- sapply(agents, function(a) a$phase())
cat(sprintf("  Final phases: %s\n", paste(sprintf("%.4f", phases), collapse = ", ")))
cat(sprintf("  Phase spread: %.6f rad\n", max(phases) - min(phases)))

cat("\n")

# --- 5. Holonomy ---
cat("--- Holonomy Consistency ---\n")

# Consistent tiles
tiles_ok <- list(
  list(directions = c(12L, 12L, 12L)),
  list(directions = c(24L, 24L, 0L))
)
cat(sprintf("  Consistent tiles: verify_consistency=%s\n", verify_consistency(tiles_ok)))

# Inconsistent tile
tiles_bad <- list(
  list(directions = c(12L, 12L, 12L)),
  list(directions = c(1L, 2L, 3L))  # sum=6 != 0 mod 48
)
cat(sprintf("  Mixed tiles: verify_consistency=%s\n", verify_consistency(tiles_bad)))

# Fault isolation
many_tiles <- c(
  lapply(1:10, function(.) list(directions = c(12L, 12L, 12L))),
  list(list(directions = c(5L, 10L, 15L)))  # bad
)
fault_idx <- isolate_fault(many_tiles)
cat(sprintf("  Fault isolated at index: %d\n", fault_idx))

# All bad tiles
bad_idx <- fault_boundaries(tiles_bad)
cat(sprintf("  Bad tile indices: %s\n", paste(bad_idx, collapse = ", ")))

# Soft verification
sv <- soft_verify_consistency(tiles_bad, epsilon = 0.5)
cat(sprintf("  Soft verify (eps=0.5): %.4f\n", sv))

cat("\n")

# --- 6. Genre Brain ---
cat("--- Genre Brain ---\n")

for (g in c("classical", "jazz", "ambient", "noise")) {
  eps <- get_genre(g)
  cat(sprintf("  %-20s: lattice=%.2f temporal=%.2f rigidity=%.2f consensus=%.2f holonomy=%.2f\n",
              g, eps$lattice, eps$temporal, eps$rigidity, eps$consensus, eps$holonomy))
}

cat("\n=== All examples completed successfully! ===\n")
