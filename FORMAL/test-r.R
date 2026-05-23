#!/usr/bin/env Rscript
# =============================================================================
# constraint-theory-core R Test Suite
# Verifies numerical correctness against the Python implementation.
# =============================================================================

source("FORMAL/constraint-theory-core.R")

cat("=== Constraint Theory Core - R Tests ===\n\n")

passed <- 0L
failed <- 0L

test <- function(name, condition) {
  if (isTRUE(condition)) {
    cat(sprintf("  PASS: %s\n", name))
    passed <<- passed + 1L
  } else {
    cat(sprintf("  FAIL: %s\n", name))
    failed <<- failed + 1L
  }
}

# --- A2 Lattice Tests ---
cat("--- A2 Lattice ---\n")

# Origin snaps to origin with zero error
res <- a2_snap(0, 0)
test("Origin snap: point is (0,0)", res$point$a == 0L && res$point$b == 0L)
test("Origin snap: error is 0", abs(res$error) < 1e-12)

# Covering radius guarantee
set.seed(123)
for (i in 1:100) {
  x <- runif(1, -10, 10)
  y <- runif(1, -10, 10)
  res <- a2_snap(x, y)
  test(sprintf("Covering radius: error %.6f < %.6f", res$error, COVERING_RADIUS),
       res$error <= COVERING_RADIUS + 1e-10)
}

# Known snap points
res <- a2_snap(1, 0)
test("snap(1,0) -> (1,0)", res$point$a == 1L && res$point$b == 0L)

res <- a2_snap(0, SQRT_3/2)
test("snap(0, sqrt3/2) -> (0,1)", res$point$a == 0L && res$point$b == 1L)

# Soft snap at epsilon=0 equals hard snap
res_hard <- a2_snap(0.5, 0.3)
res_soft <- soft_snap(0.5, 0.3, epsilon = 0.0)
test("soft_snap(eps=0) == snap",
     abs(res_soft$error - res_hard$error) < 1e-12)

# Soft snap at epsilon=1 returns original point
res_free <- soft_snap(0.5, 0.3, epsilon = 1.0)
test("soft_snap(eps=1) returns original",
     abs(res_free$xy[1] - 0.5) < 1e-12 && abs(res_free$xy[2] - 0.3) < 1e-12)

# is_safe
test("is_safe(0.1) = TRUE", is_safe(0.1))
test("is_safe(0.5) = FALSE", !is_safe(0.5))

# norm_sq
test("norm_sq(1,0) = 1", norm_sq(1L, 0L) == 1L)
test("norm_sq(1,1) = 1", norm_sq(1L, 1L) == 1L)
test("norm_sq(2,1) = 3", norm_sq(2L, 1L) == 3L)

# Dodecet roundtrip
for (i in 0:11) {
  d <- decode_dodecet(i)
  idx <- encode_dodecet(d[1], d[2])
  test(sprintf("Dodecet roundtrip %d", i), idx == i)
}

# Vector48 roundtrip
for (i in seq(0, 47, by = 7)) {
  angle <- vector48_decode(i)
  idx <- vector48_encode(angle)
  test(sprintf("Vector48 roundtrip %d", i), idx == i)
}

# Holonomy product
test("holonomy(empty) = 0", holonomy_product(integer(0)) == 0L)
test("holonomy(12,12,12) = 0", holonomy_product(c(12L, 12L, 12L)) == 0L)
test("holonomy(5,10,15) = 30", holonomy_product(c(5L, 10L, 15L)) == 30L)

# is_consistent
test("is_consistent(12,12,12) = TRUE", is_consistent(c(12L, 12L, 12L)))
test("is_consistent(5,10,15) = FALSE", !is_consistent(c(5L, 10L, 15L)))

cat("\n")

# --- Temporal Agent Tests ---
cat("--- Temporal Agent ---\n")

agent <- temporal_agent(decay_rate = 0.1)
res <- agent$observe(0.1, 0.3, t = 1.0)
test("Initial observation: phase is narrowing or approach",
     res$phase %in% c(FUNNEL_NARROWING, FUNNEL_APPROACH))
test("Initial error < covering radius", res$error < COVERING_RADIUS + 1e-10)

# Anomaly detection
agent2 <- temporal_agent(decay_rate = 0.1, delta = 0.01)
res2 <- agent2$observe(5.0, 5.0, t = 1.0)
test("Anomaly detected for far point", res2$phase == FUNNEL_ANOMALY)
test("Anomaly count incremented", agent2$anomaly_count() == 1L)

# Decay
agent3 <- temporal_agent(decay_rate = 1.0, epsilon_0 = 1.0)
eps_before <- agent3$epsilon()
agent3$decay(1.0)
eps_after <- agent3$epsilon()
test("Decay reduces epsilon", eps_after < eps_before)

# Reset
agent3$reset()
test("Reset restores epsilon", abs(agent3$epsilon() - 1.0) < 1e-10)

cat("\n")

# --- Laman Rigidity Tests ---
cat("--- Laman Rigidity ---\n")

# Henneberg construction produces Laman graphs
for (n in c(2, 3, 5, 10, 15)) {
  edges <- henneberg_construct(n)
  test(sprintf("Henneberg(%d) has %d edges = 2*%d-3", n, nrow(edges), n),
       nrow(edges) == 2L * n - 3L)
  test(sprintf("Henneberg(%d) is Laman", n), is_laman(n, edges))
}

# Non-Laman graph
test("2 edges on 3 vertices is not Laman", !is_laman(3, matrix(c(0,1,1,2), ncol=2, byrow=TRUE)))
test("Empty graph on 0 vertices is Laman", is_laman(0, matrix(nrow=0, ncol=2)))
test("Empty graph on 1 vertex is Laman", is_laman(1, matrix(nrow=0, ncol=2)))

# Algebraic connectivity
edges5 <- henneberg_construct(5)
ac <- algebraic_connectivity(edges5, 5)
test("Algebraic connectivity > 0 for connected graph", ac > 0)

# Optimal coupling
oc <- optimal_coupling(edges5, 5)
test("Optimal coupling > 0", oc > 0)
test("Optimal coupling < 1", oc < 1)

# Soft rigidity
test("soft_rigidity(eps=0) for Laman = 1",
     abs(soft_rigidity(5, edges5, 0.0) - 1.0) < 1e-10)
test("soft_rigidity(eps=0) for non-Laman = 0",
     abs(soft_rigidity(3, matrix(c(0,1,1,2), ncol=2, byrow=TRUE), 0.0)) < 1e-10)

cat("\n")

# --- Metronome Tests ---
cat("--- Metronome ---\n")

m <- metronome(T = 1.0, phi0 = 0.0, epsilon = 0.1, delta = 0.5)
test("Initial phase = 0", abs(m$phase()) < 1e-10)
test("Initial tick_count = 0", m$tick_count() == 0L)

phi <- m$tick()
test("After tick: tick_count = 1", m$tick_count() == 1L)

m2 <- metronome(T = 1.0, phi0 = pi/4, epsilon = 0.1, delta = 0.5)
test("Phase initialized correctly", abs(m2$phase() - pi/4) < 1e-10)

# Reset
m2$reset()
test("Reset: phase back to phi0", abs(m2$phase() - pi/4) < 1e-10)
test("Reset: tick_count = 0", m2$tick_count() == 0L)

# State snapshot
s <- m$state()
test("State has phase", !is.null(s$phase))
test("State has tick_count", !is.null(s$tick_count))
test("State has converged", !is.null(s$converged))

cat("\n")

# --- Holonomy Tests ---
cat("--- Holonomy ---\n")

tiles_ok <- list(
  list(directions = c(12L, 12L, 12L)),
  list(directions = c(24L, 24L, 0L))
)
test("verify_consistency: all consistent", verify_consistency(tiles_ok))

tiles_bad <- list(
  list(directions = c(12L, 12L, 12L)),
  list(directions = c(1L, 2L, 3L))
)
test("verify_consistency: has inconsistency", !verify_consistency(tiles_bad))

# Isolate fault
many <- c(
  lapply(1:10, function(.) list(directions = c(12L, 12L, 12L))),
  list(list(directions = c(5L, 10L, 15L)))
)
fault <- isolate_fault(many)
test("isolate_fault finds index 11", fault == 11L)

# Fault boundaries
bad <- fault_boundaries(tiles_bad)
test("fault_boundaries: c(2)", identical(bad, 2L))

# Soft verify
sv0 <- soft_verify_consistency(tiles_bad, 0.0)
test("soft_verify(eps=0) for bad = 0", abs(sv0) < 1e-10)

sv_ok <- soft_verify_consistency(tiles_ok, 0.0)
test("soft_verify(eps=0) for ok = 1", abs(sv_ok - 1.0) < 1e-10)

cat("\n")

# --- Genre Brain Tests ---
cat("--- Genre Brain ---\n")

jazz <- get_genre("jazz")
test("Jazz lattice epsilon = 0.30", abs(jazz$lattice - 0.30) < 1e-10)
test("Jazz temporal epsilon = 0.35", abs(jazz$temporal - 0.35) < 1e-10)

serialism <- get_genre("serialism")
test("Serialism: all zeros",
     serialism$lattice == 0 && serialism$temporal == 0 &&
     serialism$rigidity == 0 && serialism$consensus == 0 && serialism$holonomy == 0)

chaos <- get_genre("chaos")
test("Chaos: all ones",
     chaos$lattice == 1 && chaos$temporal == 1 &&
     chaos$rigidity == 1 && chaos$consensus == 1 && chaos$holonomy == 1)

all_genres <- list_genres()
test("10 genres available", length(all_genres) == 10)

cat("\n")

# --- Summary ---
cat(sprintf("=== Results: %d passed, %d failed ===\n", passed, failed))
if (failed > 0) {
  cat("SOME TESTS FAILED!\n")
  quit(status = 1)
} else {
  cat("All tests passed!\n")
}
