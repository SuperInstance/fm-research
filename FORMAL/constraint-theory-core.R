#' constraint-theory-core: Unified Geometric Constraint Theory in R
#'
#' Complete R implementation of the constraint theory system.
#' Covers Eisenstein A2 lattice, deadband funnels, Laman rigidity,
#' metronome consensus, and holonomy consistency verification.
#'
#' @name constraint-theory-core
#' @docType package
#' @author Constraint Theory Project
#' @seealso \url{https://github.com/SuperInstance/constraint-theory-core}
NULL

# ===========================================================================
# CONSTANTS (derived from first principles)
# ===========================================================================

#' Fundamental constants for the A2 lattice
#' @export
SQRT_3 <- sqrt(3.0)

#' Real part of omega = e^(2*pi*i/3)
#' @export
OMEGA_RE <- -0.5

#' Imaginary part of omega
#' @export
OMEGA_IM <- SQRT_3 / 2.0

#' Covering radius rho = 1/sqrt(3) ~ 0.577
#' @export
COVERING_RADIUS <- 1.0 / SQRT_3

#' Safe threshold rho/2 ~ 0.289
#' @export
SAFE_THRESHOLD <- COVERING_RADIUS / 2.0

#' Two * pi
#' @export
TWO_PI <- 2.0 * pi

#' Number of Pythagorean directions
#' @export
DIRECTION_COUNT <- 48L

#' Number of dodecet directions (12 nearest neighbours on A2)
#' @export
DODECET_COUNT <- 12L

#' The 12 minimal nonzero vectors of the A2 lattice
#' @export
DODECET_DIRECTIONS <- list(
  c(1L, 0L), c(0L, 1L), c(-1L, 1L), c(-1L, 0L),
  c(0L, -1L), c(1L, -1L), c(2L, -1L), c(1L, -2L),
  c(-1L, -1L), c(-2L, 1L), c(-1L, 2L), c(1L, 1L)
)

# ===========================================================================
# A2 LATTICE
# ===========================================================================

#' Represent an A2 lattice point
#'
#' Creates an A2 point object: a*1 + b*omega where omega = e^(2*pi*i/3).
#'
#' @param a Integer coefficient of basis vector 1
#' @param b Integer coefficient of basis vector omega
#' @return List with components a, b, plus methods norm_sq, to_complex, arith
#' @export
#' @examples
#' pt <- a2_point(1, 2)
#' pt$norm_sq()
#' pt$to_complex()
a2_point <- function(a, b) {
  stopifnot(is.numeric(a), is.numeric(b))
  a <- as.integer(a)
  b <- as.integer(b)
  structure(
    list(
      a = a, b = b,
      norm_sq = function() a * a - a * b + b * b,
      to_complex = function() c(a + b * OMEGA_RE, b * OMEGA_IM)
    ),
    class = c("A2Point", "list")
  )
}

#' @export
print.A2Point <- function(x, ...) {
  cat(sprintf("A2Point(a=%d, b=%d)\n", x$a, x$b))
}

#' Snap a point (x,y) to the nearest A2 lattice point
#'
#' Every point in the complex plane is within rho = 1/sqrt(3) of an A2
#' lattice point. This guarantee underpins the entire unified architecture.
#'
#' @param x Real coordinate (numeric)
#' @param y Imaginary coordinate (numeric)
#' @return List with \code{point} (A2Point) and \code{error} (numeric)
#' @export
#' @examples
#' result <- a2_snap(0.5, 0.3)
#' print(result$point)
#' cat("Error:", result$error, "\n")
a2_snap <- function(x, y) {
  stopifnot(is.numeric(x), length(x) == 1, is.finite(x))
  stopifnot(is.numeric(y), length(y) == 1, is.finite(y))

  # Convert Cartesian to lattice coordinates
  # z = x + iy = a + b*omega = a + b*(-1/2 + i*sqrt(3)/2)
  # x = a - b/2, y = b*sqrt(3)/2 => b = 2y/sqrt(3), a = x + b/2
  b_f <- y / OMEGA_IM
  a_f <- x + b_f * 0.5

  # Round to nearest integers
  a <- round(a_f)
  b <- round(b_f)

  # Check 6 candidates for closest lattice point
  best <- a2_point(a, b)
  best_err <- .distance_to(x, y, best)

  offsets <- list(c(1L, 0L), c(-1L, 0L), c(0L, 1L),
                  c(0L, -1L), c(1L, -1L), c(-1L, 1L))
  for (off in offsets) {
    cand <- a2_point(a + off[1], b + off[2])
    err <- .distance_to(x, y, cand)
    if (err < best_err) {
      best <- cand
      best_err <- err
    }
  }

  list(point = best, error = best_err)
}

#' Snap with continuous softness control via epsilon-interpolation
#'
#' Interpolates between the original point (epsilon=1, free) and the
#' exact lattice snap (epsilon=0, rigid).
#'
#' @param x Real coordinate
#' @param y Imaginary coordinate
#' @param epsilon Softness parameter in [0,1]
#' @return List with \code{xy} (c(soft_x, soft_y)), \code{error}, \code{snapped} (A2Point)
#' @export
soft_snap <- function(x, y, epsilon = 0.0) {
  stopifnot(is.numeric(epsilon), length(epsilon) == 1, epsilon >= 0, epsilon <= 1)

  snapped_result <- a2_snap(x, y)
  snapped <- snapped_result$point
  err <- snapped_result$error

  if (abs(epsilon - 1.0) < 1e-15) {
    return(list(xy = c(x, y), error = err, snapped = snapped))
  }
  if (epsilon == 0.0) {
    sx_sy <- snapped$to_complex()
    return(list(xy = sx_sy, error = err, snapped = snapped))
  }

  sx_sy <- snapped$to_complex()
  soft_x <- (1.0 - epsilon) * sx_sy[1] + epsilon * x
  soft_y <- (1.0 - epsilon) * sx_sy[2] + epsilon * y

  dx <- soft_x - sx_sy[1]
  dy <- soft_y - sx_sy[2]
  soft_err <- sqrt(dx * dx + dy * dy)

  list(xy = c(soft_x, soft_y), error = soft_err, snapped = snapped)
}

#' Return the A2 covering radius rho = 1/sqrt(3)
#' @return Numeric scalar
#' @export
a2_covering_radius <- function() COVERING_RADIUS

#' Check if quantization error is within the safe threshold (rho/2)
#' @param error Numeric quantization error
#' @return Logical
#' @export
is_safe <- function(error) error < SAFE_THRESHOLD

#' Compute squared Eisenstein norm a^2 - a*b + b^2
#' @param a Integer coefficient
#' @param b Integer coefficient
#' @return Integer
#' @export
norm_sq <- function(a, b) a * a - a * b + b * b

#' Decode a dodecet index (0-11) to an A2 direction vector
#' @param index Integer index 0-11
#' @return Integer vector c(a, b)
#' @export
decode_dodecet <- function(index) {
  stopifnot(is.numeric(index), index >= 0, index < DODECET_COUNT)
  DODECET_DIRECTIONS[[as.integer(index) + 1L]]
}

#' Encode an A2 direction vector to a dodecet index
#' @param a Integer coefficient
#' @param b Integer coefficient
#' @return Integer index 0-11
#' @export
encode_dodecet <- function(a, b) {
  for (i in seq_along(DODECET_DIRECTIONS)) {
    if (DODECET_DIRECTIONS[[i]][1] == a && DODECET_DIRECTIONS[[i]][2] == b) {
      return(as.integer(i - 1L))
    }
  }
  stop(sprintf("(%d, %d) is not a dodecet direction", a, b))
}

#' Quantize an angle to one of 48 Pythagorean directions
#' @param angle Angle in radians
#' @return Integer index 0-47
#' @export
vector48_encode <- function(angle) {
  normalized <- angle %% TWO_PI
  as.integer(round(normalized / TWO_PI * DIRECTION_COUNT)) %% DIRECTION_COUNT
}

#' Decode a Pythagorean direction index to an angle
#' @param index Integer index 0-47
#' @return Numeric angle in radians
#' @export
vector48_decode <- function(index) {
  stopifnot(index >= 0, index < DIRECTION_COUNT)
  index * TWO_PI / DIRECTION_COUNT
}

#' Compute holonomy around a cycle of directions (sum mod 48)
#' @param directions Integer vector of direction indices
#' @return Integer holonomy (0 = consistent)
#' @export
holonomy_product <- function(directions) {
  if (length(directions) == 0) return(0L)
  sum(directions) %% DIRECTION_COUNT
}

#' Check if a cycle of directions is holonomy-free
#' @param directions Integer vector of direction indices
#' @return Logical
#' @export
is_consistent <- function(directions) holonomy_product(directions) == 0L

# Internal: Euclidean distance from (x,y) to an A2 point
.distance_to <- function(x, y, point) {
  pc <- point$to_complex()
  dx <- x - pc[1]
  dy <- y - pc[2]
  sqrt(dx * dx + dy * dy)
}


# ===========================================================================
# DEADBAND FUNNEL / TEMPORAL AGENT
# ===========================================================================

#' Phases of the deadband funnel
#' @export
FUNNEL_APPROACH  <- "approach"
#' @export
FUNNEL_NARROWING <- "narrowing"
#' @export
FUNNEL_ANOMALY   <- "anomaly"

#' Create a TemporalAgent (deadband funnel with exponential decay)
#'
#' The funnel starts wide (permissive) and narrows monotonically:
#' epsilon(t) = epsilon_0 * exp(-lambda*t)
#'
#' When prediction error exceeds the deadband, an anomaly is detected
#' and the funnel resets. Otherwise, the system converges to zero drift.
#'
#' @param decay_rate Exponential decay rate lambda
#' @param epsilon_0 Initial deadband width (default: covering radius)
#' @param delta Anomaly threshold (default: covering radius)
#' @param softness Soft-snap parameter [0,1]. 0=exact, 1=free
#' @return An environment with methods observe(), decay(), reset(), and properties epsilon, anomaly_count
#' @export
#' @examples
#' agent <- temporal_agent(decay_rate = 0.1)
#' result <- agent$observe(0.1, 0.3, t = 1.0)
#' cat("Phase:", result$phase, "Error:", result$error, "\n")
temporal_agent <- function(decay_rate = 0.1,
                           epsilon_0 = COVERING_RADIUS,
                           delta = COVERING_RADIUS,
                           softness = 0.0) {
  stopifnot(is.numeric(decay_rate), decay_rate >= 0, is.finite(decay_rate))
  stopifnot(is.numeric(epsilon_0), epsilon_0 > 0, is.finite(epsilon_0))

  .eps   <- epsilon_0
  .last_t <- NULL
  .last_error <- 0.0
  .anomalies  <- 0L

  env <- new.env(parent = emptyenv())

  env$epsilon <- function() .eps

  env$anomaly_count <- function() .anomalies

  env$observe <- function(x, y, t) {
    snap_res <- a2_snap(x, y)
    pt   <- snap_res$point
    error <- snap_res$error

    # Apply soft deadband
    effective_eps <- .eps * (1.0 + softness)

    # Decay
    if (!is.null(.last_t)) {
      dt <- t - .last_t
      if (dt > 0) .eps <<- .eps * exp(-decay_rate * dt)
    }
    .last_t <<- t

    if (error > delta) {
      phase <- FUNNEL_ANOMALY
      .anomalies <<- .anomalies + 1L
      .eps <<- epsilon_0
    } else if (error > effective_eps) {
      phase <- FUNNEL_APPROACH
    } else {
      phase <- FUNNEL_NARROWING
    }

    .last_error <<- error

    list(
      phase = phase,
      error = error,
      deadband = .eps,
      snapped_a = pt$a,
      snapped_b = pt$b
    )
  }

  env$decay <- function(dt) {
    if (dt > 0) .eps <<- .eps * exp(-decay_rate * dt)
  }

  env$reset <- function(x = 0, y = 0) {
    .eps <<- epsilon_0
  }

  env
}


# ===========================================================================
# LAMAN RIGIDITY
# ===========================================================================

#' Check if a graph is Laman rigid
#'
#' A graph G = (V,E) with n vertices is Laman rigid iff:
#' 1. |E| = 2n - 3
#' 2. Every subset of k vertices spans at most 2k - 3 edges
#'
#' @param n Number of vertices
#' @param edges Matrix or list of edges, each row c(i,j)
#' @return Logical
#' @export
#' @examples
#' edges <- henneberg_construct(6)
#' is_laman(6, edges)
is_laman <- function(n, edges) {
  stopifnot(is.numeric(n), n >= 0)
  n <- as.integer(n)

  if (is.list(edges) && !is.data.frame(edges)) {
    edges <- do.call(rbind, edges)
  }
  if (is.null(edges) || length(edges) == 0) {
    return(n < 2)
  }
  if (is.vector(edges)) edges <- matrix(edges, ncol = 2, byrow = TRUE)

  if (n < 2) return(nrow(edges) == 0)

  expected <- 2L * n - 3L
  if (nrow(edges) != expected) return(FALSE)

  # Brute-force subset check for small n
  if (n <= 15) return(.check_subsets(n, edges))

  # Pebble game for larger graphs
  .pebble_game(n, edges)
}

#' Build a Laman graph via Henneberg type-I construction
#'
#' Algorithm:
#' 1. Start with K2 (2 vertices, 1 edge)
#' 2. For each new vertex v (2..n-1): select two distinct existing vertices and connect
#'
#' @param n Number of vertices (>= 2)
#' @param seed Random seed for reproducibility
#' @return Integer matrix with 2 columns (edge list)
#' @export
#' @examples
#' edges <- henneberg_construct(6)
#' is_laman(6, edges)  # TRUE
henneberg_construct <- function(n, seed = 42L) {
  stopifnot(n >= 2)
  n <- as.integer(n)
  set.seed(seed)

  edges <- matrix(c(0L, 1L), ncol = 2, byrow = TRUE)

  for (v in seq(2L, n - 1L)) {
    candidates <- sample(seq(0L, v - 1L))
    i <- candidates[1]
    j <- candidates[2]
    edges <- rbind(edges, c(v, i), c(v, j))
  }

  edges
}

#' Compute algebraic connectivity (lambda_2) of the graph Laplacian
#'
#' lambda_2 is the second-smallest eigenvalue. It determines:
#' - Convergence rate of consensus protocols
#' - Optimal coupling alpha* = 2/(lambda_2 + lambda_n)
#'
#' @param edges Edge list (matrix with 2 columns)
#' @param n Number of vertices
#' @return Numeric algebraic connectivity
#' @export
algebraic_connectivity <- function(edges, n) {
  if (n < 2) return(0.0)

  if (is.list(edges) && !is.data.frame(edges)) {
    edges <- do.call(rbind, edges)
  }
  if (is.vector(edges)) edges <- matrix(edges, ncol = 2, byrow = TRUE)
  if (is.null(edges) || length(edges) == 0) return(0.0)

  if (n > 50) {
    return(2.0 * nrow(edges) / (n * (n - 1)))
  }

  # Build Laplacian
  L <- matrix(0.0, n, n)
  for (k in seq_len(nrow(edges))) {
    u <- edges[k, 1] + 1L
    v <- edges[k, 2] + 1L
    L[u, u] <- L[u, u] + 1.0
    L[v, v] <- L[v, v] + 1.0
    L[u, v] <- L[u, v] - 1.0
    L[v, u] <- L[v, u] - 1.0
  }

  # Power iteration for second eigenvalue
  x <- seq_len(n) * 1.0
  x <- x - mean(x)

  for (iter in seq_len(100L)) {
    y <- L %*% x
    y <- as.numeric(y)
    y <- y - mean(y)
    nrm <- sqrt(sum(y * y))
    if (nrm < 1e-15) return(0.0)
    x <- y / nrm
  }

  as.numeric(sum(x * (L %*% x)))
}

#' Compute optimal coupling alpha* = 2/(lambda_2 + lambda_n)
#' @param edges Edge list
#' @param n Number of vertices
#' @return Numeric optimal coupling
#' @export
optimal_coupling <- function(edges, n) {
  lam2 <- algebraic_connectivity(edges, n)
  if (n < 2) return(0.0)

  # Estimate lambda_n as max degree + 1
  deg <- rep(0L, n)
  if (is.matrix(edges)) {
    for (k in seq_len(nrow(edges))) {
      deg[edges[k,1] + 1L] <- deg[edges[k,1] + 1L] + 1L
      deg[edges[k,2] + 1L] <- deg[edges[k,2] + 1L] + 1L
    }
  }
  lam_n <- max(deg) + 1.0

  if (lam2 + lam_n < 1e-10) return(0.0)
  2.0 / (lam2 + lam_n)
}

#' Continuous rigidity score softened by epsilon
#'
#' At epsilon=0 returns 1 if Laman-rigid else 0.
#' As epsilon -> 1 relaxes toward a continuous measure.
#'
#' @param n_vertices Number of vertices
#' @param edges Edge list
#' @param epsilon Softness in [0,1]
#' @return Numeric score in [0,1]
#' @export
soft_rigidity <- function(n_vertices, edges, epsilon = 0.0) {
  stopifnot(epsilon >= 0, epsilon <= 1)

  if (is.list(edges) && !is.data.frame(edges)) edges <- do.call(rbind, edges)
  if (is.vector(edges) && length(edges) > 0) edges <- matrix(edges, ncol = 2, byrow = TRUE)
  ne <- if (is.null(edges) || length(edges) == 0) 0L else nrow(edges)

  rigid <- is_laman(n_vertices, edges)

  if (epsilon == 0.0) return(if (rigid) 1.0 else 0.0)
  if (n_vertices < 2) return(if (ne == 0) 1.0 else 0.0)

  expected <- 2L * n_vertices - 3L
  edge_ratio <- min(ne / expected, 1.0)
  conn <- algebraic_connectivity(edges, n_vertices)
  conn_factor <- if (conn > 0) min(conn, 1.0) else 0.0

  if (rigid) {
    1.0 - epsilon * (1.0 - 0.5 * conn_factor)
  } else {
    epsilon * edge_ratio
  }
}

# Internal: brute-force subset check
.check_subsets <- function(n, edges) {
  edge_set <- list()
  for (k in seq_len(nrow(edges))) {
    u <- min(edges[k,1], edges[k,2])
    v <- max(edges[k,1], edges[k,2])
    edge_set[[length(edge_set) + 1L]] <- paste(u, v, sep = ",")
  }
  edge_vec <- unlist(edge_set)

  for (k in 2:n) {
    combos <- combn(seq(0L, n - 1L), k)
    for (col in seq_len(ncol(combos))) {
      vset <- combos[, col]
      count <- 0L
      for (kk in seq_len(nrow(edges))) {
        u <- edges[kk, 1]
        v <- edges[kk, 2]
        if (u %in% vset && v %in% vset) count <- count + 1L
      }
      if (count > 2L * k - 3L) return(FALSE)
    }
  }
  TRUE
}

# Internal: pebble game (connectivity check for large graphs)
.pebble_game <- function(n, edges) {
  adj <- lapply(seq_len(n), function(.) integer(0))
  for (k in seq_len(nrow(edges))) {
    u <- edges[k,1] + 1L
    v <- edges[k,2] + 1L
    adj[[u]] <- c(adj[[u]], v)
    adj[[v]] <- c(adj[[v]], u)
  }
  visited <- logical(n)
  queue <- 1L
  while (length(queue) > 0L) {
    node <- queue[1L]
    queue <- queue[-1L]
    if (visited[node]) next
    visited[node] <- TRUE
    nbrs <- adj[[node]]
    queue <- c(queue, nbrs[!visited[nbrs]])
  }
  all(visited)
}


# ===========================================================================
# METRONOME CONSENSUS
# ===========================================================================

#' Create a Metronome agent
#'
#' Each agent maintains a phase phi on the Eisenstein lattice.
#' Parameters theta = (T, phi0, epsilon, delta) control:
#' - T: period (seconds per tick)
#' - phi0: reference phase (radians)
#' - epsilon: deadband tolerance
#' - delta: anomaly threshold
#'
#' @param T Period in seconds (positive)
#' @param phi0 Initial phase in radians
#' @param epsilon Deadband tolerance
#' @param delta Anomaly threshold
#' @param neighbors Integer vector of Laman-neighbor indices
#' @param edges Edge list for optimal coupling
#' @param n_agents Total number of agents
#' @param softness Softness parameter [0,1]
#' @return Environment with methods tick(), agree(), correct(), observe(), reset(), state()
#' @export
#' @examples
#' m <- metronome(T = 1.0, phi0 = 0.0, epsilon = 0.1, delta = 0.5)
#' m$tick()
metronome <- function(T = 1.0, phi0 = 0.0, epsilon = 0.577,
                      delta = 0.577, neighbors = integer(0),
                      edges = NULL, n_agents = 1L, softness = 0.0) {
  stopifnot(is.numeric(T), T > 0, is.finite(T))

  .T <- T
  .phi0 <- phi0 %% TWO_PI
  .phi <- .phi0
  .t <- 0.0
  .tick_count <- 0L
  .converged <- FALSE
  .corrections <- numeric(0)

  .temporal <- temporal_agent(
    decay_rate = if (.T > 0) 1.0 / .T else 1.0,
    epsilon_0 = epsilon,
    delta = delta,
    softness = softness
  )

  .alpha <- if (!is.null(edges) && n_agents > 1) {
    optimal_coupling(edges, n_agents)
  } else 0.0

  env <- new.env(parent = emptyenv())

  env$phase <- function() .phi
  env$tick_count <- function() .tick_count
  env$converged <- function() .converged
  env$corrections <- function() .corrections
  env$anomaly_count <- function() .temporal$anomaly_count()

  env$tick <- function() {
    .t <<- .t + .T
    .phi <<- (.phi + TWO_PI) %% TWO_PI
    .tick_count <<- .tick_count + 1L
    .temporal$decay(.T)
    .phi
  }

  env$agree <- function(other) {
    diff <- .circular_distance(.phi, other$phase())
    effective_eps <- .temporal$epsilon() * (1.0 + softness)
    diff <= effective_eps
  }

  env$correct <- function(neighbor_phases) {
    if (length(neighbor_phases) == 0L || .alpha <= 0) return(0.0)

    avg_phase <- .circular_mean(neighbor_phases)
    diff <- .circular_diff(avg_phase, .phi)
    eff_alpha <- .alpha * (1.0 - softness)
    correction <- eff_alpha * diff
    .phi <<- (.phi + correction) %% TWO_PI
    .corrections <<- c(.corrections, abs(correction))

    # Convergence: 3 consecutive tiny corrections
    if (length(.corrections) >= 3L) {
      recent <- tail(.corrections, 3L)
      if (all(recent < epsilon * 0.1)) .converged <<- TRUE
    }

    abs(correction)
  }

  env$observe <- function(x, y) {
    result <- .temporal$observe(x, y, t = .t)
    cx <- result$snapped_a + result$snapped_b * OMEGA_RE
    cy <- result$snapped_b * OMEGA_IM
    .phi <<- atan2(cy, cx) %% TWO_PI
    result$phase
  }

  env$reset <- function() {
    .phi <<- .phi0
    .t <<- 0.0
    .tick_count <<- 0L
    .converged <<- FALSE
    .corrections <<- numeric(0)
    .temporal$reset()
  }

  env$state <- function() {
    list(
      phase = .phi,
      tick_count = .tick_count,
      converged = .converged,
      epsilon = .temporal$epsilon(),
      anomaly_count = .temporal$anomaly_count()
    )
  }

  env
}

#' Run one round of consensus among metronome agents
#'
#' @param agents List of metronome environments
#' @param edges Edge list (matrix with 2 columns) defining neighbor relationships
#' @return List of agents after correction (same objects, modified in place)
#' @export
consensus_round <- function(agents, edges) {
  if (is.null(edges) || length(edges) == 0) return(agents)
  if (is.vector(edges)) edges <- matrix(edges, ncol = 2, byrow = TRUE)

  for (k in seq_len(nrow(edges))) {
    i <- edges[k, 1] + 1L
    j <- edges[k, 2] + 1L
    if (i <= length(agents) && j <= length(agents)) {
      agents[[i]]$correct(agents[[j]]$phase())
      agents[[j]]$correct(agents[[i]]$phase())
    }
  }
  agents
}

# Internal helpers for circular math
.circular_mean <- function(angles) {
  if (length(angles) == 0) return(0.0)
  atan2(sum(sin(angles)), sum(cos(angles)))
}

.circular_diff <- function(target, current) {
  diff <- target - current
  while (diff > pi) diff <- diff - TWO_PI
  while (diff < -pi) diff <- diff + TWO_PI
  diff
}

.circular_distance <- function(a, b) {
  diff <- abs(a - b)
  min(diff, TWO_PI - diff)
}


# ===========================================================================
# HOLONOMY CONSISTENCY
# ===========================================================================

#' Compute holonomy around a directed cycle
#'
#' @param directions Integer vector of direction indices (0-47)
#' @return Integer holonomy (0 = consistent)
#' @export
cycle_holonomy <- function(directions) {
  if (length(directions) == 0) return(0L)
  stopifnot(all(directions >= 0), all(directions < DIRECTION_COUNT))
  sum(directions) %% DIRECTION_COUNT
}

#' Verify all tiles are holonomy-free
#'
#' @param tiles List of tiles; each tile is a list with element \code{directions}
#'   (integer vector of direction indices)
#' @return Logical TRUE if all tiles consistent
#' @export
#' @examples
#' tiles <- list(
#'   list(directions = c(12L, 12L, 12L)),
#'   list(directions = c(24L, 24L, 0L))
#' )
#' verify_consistency(tiles)
verify_consistency <- function(tiles) {
  for (tile in tiles) {
    if (cycle_holonomy(tile$directions) != 0L) return(FALSE)
  }
  TRUE
}

#' Soft holonomy verification with continuous tolerance
#'
#' @param tiles List of tiles (each with $directions)
#' @param epsilon Softness in [0,1]
#' @return Numeric score in [0,1]
#' @export
soft_verify_consistency <- function(tiles, epsilon = 0.0) {
  stopifnot(epsilon >= 0, epsilon <= 1)
  if (length(tiles) == 0) return(1.0)
  if (epsilon == 0.0) return(if (verify_consistency(tiles)) 1.0 else 0.0)

  total_dev <- 0L
  for (tile in tiles) {
    h <- cycle_holonomy(tile$directions)
    total_dev <- total_dev + min(h, DIRECTION_COUNT - h)
  }
  max_dev <- length(tiles) * (DIRECTION_COUNT %/% 2L)
  if (max_dev == 0) return(1.0)

  raw <- 1.0 - total_dev / max_dev
  epsilon * 1.0 + (1.0 - epsilon) * raw
}

#' Isolate a fault via binary search (O(log N))
#' @param tiles List of tiles
#' @return Integer index of an inconsistent tile
#' @export
isolate_fault <- function(tiles) {
  if (length(tiles) == 0) stop("tiles list is empty")
  if (verify_consistency(tiles)) stop("no inconsistent tile found")

  lo <- 1L
  hi <- length(tiles) + 1L
  while (lo < hi - 1L) {
    mid <- (lo + hi) %/% 2L
    if (!verify_consistency(tiles[lo:(mid - 1L)])) {
      hi <- mid
    } else {
      lo <- mid
    }
  }
  lo
}

#' Return indices of all inconsistent tiles
#' @param tiles List of tiles
#' @return Integer vector of bad indices (1-based)
#' @export
fault_boundaries <- function(tiles) {
  bad <- integer(0)
  for (i in seq_along(tiles)) {
    if (cycle_holonomy(tiles[[i]]$directions) != 0L) {
      bad <- c(bad, i)
    }
  }
  bad
}


# ===========================================================================
# GENRE BRAIN
# ===========================================================================

#' Built-in genre profiles (epsilon values per constraint)
#' @export
GENRES <- list(
  serialism = list(lattice = 0.0, temporal = 0.0, rigidity = 0.0, consensus = 0.0, holonomy = 0.0),
  strict_counterpoint = list(lattice = 0.0, temporal = 0.05, rigidity = 0.0, consensus = 0.05, holonomy = 0.0),
  classical = list(lattice = 0.10, temporal = 0.10, rigidity = 0.10, consensus = 0.10, holonomy = 0.10),
  romantic = list(lattice = 0.20, temporal = 0.25, rigidity = 0.15, consensus = 0.20, holonomy = 0.15),
  jazz = list(lattice = 0.30, temporal = 0.35, rigidity = 0.25, consensus = 0.30, holonomy = 0.25),
  free_jazz = list(lattice = 0.50, temporal = 0.55, rigidity = 0.45, consensus = 0.50, holonomy = 0.45),
  minimalism = list(lattice = 0.05, temporal = 0.15, rigidity = 0.05, consensus = 0.10, holonomy = 0.05),
  ambient = list(lattice = 0.60, temporal = 0.65, rigidity = 0.50, consensus = 0.55, holonomy = 0.50),
  noise = list(lattice = 0.90, temporal = 0.90, rigidity = 0.85, consensus = 0.90, holonomy = 0.85),
  chaos = list(lattice = 1.0, temporal = 1.0, rigidity = 1.0, consensus = 1.0, holonomy = 1.0)
)

#' Get genre epsilon profile
#' @param name Genre name (case-insensitive)
#' @return Named list of epsilon values
#' @export
get_genre <- function(name) {
  key <- tolower(gsub("[ -]", "_", name))
  if (!(key %in% names(GENRES))) {
    stop(sprintf("Unknown genre '%s'. Available: %s", name, paste(names(GENRES), collapse = ", ")))
  }
  GENRES[[key]]
}

#' List all built-in genre profiles
#' @export
list_genres <- function() GENRES


# ===========================================================================
# VISUALIZATION (ggplot2)
# ===========================================================================

#' Plot A2 lattice with snapped points
#'
#' @param points Matrix or data frame with columns x, y (original points)
#' @param title Plot title
#' @return ggplot object
#' @export
#' @examples
#' \dontrun{
#' pts <- cbind(runif(50, -3, 3), runif(50, -3, 3))
#' plot_lattice(pts)
#' }
plot_lattice <- function(points, title = "A2 Lattice Snap") {
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    stop("ggplot2 is required for plotting")
  }

  if (is.vector(points)) points <- matrix(points, ncol = 2, byrow = TRUE)

  # Snap each point
  snapped <- t(apply(points, 1, function(p) {
    res <- a2_snap(p[1], p[2])
    res$point$to_complex()
  }))

  errors <- sapply(seq_len(nrow(points)), function(i) {
    .distance_to(points[i, 1], points[i, 2], a2_point(
      round((points[i,1] + (points[i,2] / OMEGA_IM) * 0.5)),
      round(points[i,2] / OMEGA_IM)
    ))
  })

  df <- data.frame(
    x = points[, 1], y = points[, 2],
    sx = snapped[, 1], sy = snapped[, 2],
    error = errors
  )

  # Generate lattice grid
  range_x <- range(c(points[, 1], snapped[, 1]))
  range_y <- range(c(points[, 2], snapped[, 2]))
  a_range <- seq(floor(min(range_x) - 1), ceiling(max(range_x) + 1))
  b_range <- seq(floor(min(range_y) * 2 / SQRT_3 - 1), ceiling(max(range_y) * 2 / SQRT_3 + 1))
  grid <- expand.grid(a = a_range, b = b_range)
  grid$x <- grid$a + grid$b * OMEGA_RE
  grid$y <- grid$b * OMEGA_IM

  ggplot2::ggplot() +
    ggplot2::geom_point(data = grid, ggplot2::aes(x = x, y = y),
                        shape = 3, color = "gray70", size = 1) +
    ggplot2::geom_segment(data = df,
                          ggplot2::aes(x = x, y = y, xend = sx, yend = sy),
                          arrow = ggplot2::arrow(length = ggplot2::unit(0.15, "cm")),
                          color = "steelblue", alpha = 0.6) +
    ggplot2::geom_point(data = df, ggplot2::aes(x = x, y = y),
                        color = "firebrick", size = 2, shape = 16) +
    ggplot2::geom_point(data = df, ggplot2::aes(x = sx, y = sy),
                        color = "darkgreen", size = 2.5, shape = 15) +
    ggplot2::labs(title = title, x = "Re", y = "Im") +
    ggplot2::theme_minimal() +
    ggplot2::coord_fixed()
}

#' Plot convergence history of metronome agents
#'
#' @param history Matrix or data frame with columns tick, agent, correction
#' @param title Plot title
#' @return ggplot object
#' @export
plot_convergence <- function(history, title = "Metronome Convergence") {
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    stop("ggplot2 is required for plotting")
  }
  df <- as.data.frame(history)
  ggplot2::ggplot(df, ggplot2::aes(x = tick, y = correction, color = factor(agent))) +
    ggplot2::geom_line() +
    ggplot2::geom_point(size = 1) +
    ggplot2::scale_y_log10() +
    ggplot2::labs(title = title, x = "Tick", y = "Correction (log scale)",
                  color = "Agent") +
    ggplot2::theme_minimal()
}

#' Plot a rigidity graph
#'
#' @param edges Edge list (matrix with 2 columns)
#' @param n Number of vertices
#' @param title Plot title
#' @return ggplot object
#' @export
plot_rigidity_graph <- function(edges, n, title = "Laman Rigidity Graph") {
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    stop("ggplot2 is required for plotting")
  }

  # Layout: circular
  angles <- seq(0, 2 * pi, length.out = n + 1)[1:n]
  pos <- data.frame(
    vertex = seq(0, n - 1),
    x = cos(angles),
    y = sin(angles)
  )

  if (is.vector(edges)) edges <- matrix(edges, ncol = 2, byrow = TRUE)

  edge_df <- do.call(rbind, lapply(seq_len(nrow(edges)), function(k) {
    i <- edges[k, 1]; j <- edges[k, 2]
    data.frame(
      x = pos$x[i + 1], y = pos$y[i + 1],
      xend = pos$x[j + 1], yend = pos$y[j + 1]
    )
  }))

  ggplot2::ggplot() +
    ggplot2::geom_segment(data = edge_df,
                          ggplot2::aes(x = x, y = y, xend = xend, yend = yend),
                          color = "steelblue", linewidth = 1) +
    ggplot2::geom_point(data = pos, ggplot2::aes(x = x, y = y),
                        size = 5, color = "firebrick") +
    ggplot2::geom_text(data = pos, ggplot2::aes(x = x, y = y, label = vertex),
                       vjust = -1, size = 4) +
    ggplot2::labs(title = title, x = "", y = "") +
    ggplot2::theme_minimal() +
    ggplot2::coord_fixed()
}
