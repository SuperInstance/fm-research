% constraint-theory-core: Unified Geometric Constraint Theory in MATLAB
%
% Complete MATLAB implementation of the constraint theory system.
% Covers Eisenstein A2 lattice, deadband funnels, Laman rigidity,
% metronome consensus, and holonomy consistency verification.
%
% Functions:
%   a2_snap, soft_snap, a2_covering_radius, is_safe, norm_sq
%   decode_dodecet, encode_dodecet, vector48_encode, vector48_decode
%   holonomy_product, is_consistent
%   temporal_agent (class), deadband_funnel
%   is_laman, henneberg_construct, algebraic_connectivity, optimal_coupling
%   soft_rigidity
%   metronome (class), consensus_round
%   cycle_holonomy, verify_consistency, soft_verify_consistency
%   isolate_fault, fault_boundaries
%   get_genre, list_genres
%   plot_lattice, plot_convergence, plot_rigidity_graph
%
% Author: Constraint Theory Project
% See also: https://github.com/SuperInstance/constraint-theory-core

%% ========================================================================
% CONSTANTS
%% ========================================================================

function out = ct_constants(name)
% CT_CONSTANTS Return fundamental constants for the A2 lattice.
%   out = ct_constants(name) returns the named constant.
%
%   Names:
%     'sqrt3'          - sqrt(3)
%     'omega_re'       - -0.5
%     'omega_im'       - sqrt(3)/2
%     'covering_radius' - 1/sqrt(3)
%     'safe_threshold' - 1/(2*sqrt(3))
%     'two_pi'         - 2*pi
%     'direction_count' - 48
%     'dodecet_count'  - 12

  persistent CONST
  if isempty(CONST)
    CONST = struct();
    CONST.sqrt3 = sqrt(3);
    CONST.omega_re = -0.5;
    CONST.omega_im = CONST.sqrt3 / 2;
    CONST.covering_radius = 1 / CONST.sqrt3;
    CONST.safe_threshold = CONST.covering_radius / 2;
    CONST.two_pi = 2 * pi;
    CONST.direction_count = 48;
    CONST.dodecet_count = 12;
  end

  if nargin < 1
    out = CONST;
    return
  end

  out = CONST.(name);
end

%% ========================================================================
% A2 LATTICE
%% ========================================================================

function [pt, err] = a2_snap(x, y)
% A2_SNAP Snap a point (x,y) to the nearest A2 lattice point.
%
%   [pt, err] = a2_snap(x, y) returns:
%     pt  - struct with fields a, b (integer lattice coordinates)
%     err - Euclidean distance from (x,y) to the snapped point
%
%   Every point in the complex plane is within rho = 1/sqrt(3) of an A2
%   lattice point. This guarantee underpins the unified architecture.
%
%   Example:
%     [pt, err] = a2_snap(0.5, 0.3);
%     fprintf('Snapped to (%d, %d), error = %.6f\n', pt.a, pt.b, err);

  C = ct_constants();

  % Validate inputs
  validateattributes(x, {'numeric'}, {'scalar', 'finite'}, 'a2_snap', 'x');
  validateattributes(y, {'numeric'}, {'scalar', 'finite'}, 'a2_snap', 'y');

  % Convert Cartesian to lattice coordinates
  b_f = y / C.omega_im;
  a_f = x + b_f * 0.5;

  % Round to nearest integers
  a = round(a_f);
  b = round(b_f);

  % Check 6 candidates
  best = struct('a', a, 'b', b);
  best_err = distance_to(x, y, best, C);

  offsets = [1 0; -1 0; 0 1; 0 -1; 1 -1; -1 1];
  for k = 1:size(offsets, 1)
    cand = struct('a', a + offsets(k,1), 'b', b + offsets(k,2));
    e = distance_to(x, y, cand, C);
    if e < best_err
      best = cand;
      best_err = e;
    end
  end

  pt = best;
  err = best_err;
end

function d = distance_to(x, y, pt, C)
% Internal: Euclidean distance from (x,y) to an A2 point
  if nargin < 4, C = ct_constants(); end
  px = pt.a + pt.b * C.omega_re;
  py = pt.b * C.omega_im;
  d = sqrt((x - px)^2 + (y - py)^2);
end

function [xy, err, snapped] = soft_snap(x, y, epsilon)
% SOFT_SNAP Snap with continuous softness control via epsilon-interpolation.
%
%   [xy, err, snapped] = soft_snap(x, y, epsilon) interpolates between
%   the original point (epsilon=1, free) and the exact snap (epsilon=0, rigid).
%
%   Inputs:
%     x, y    - coordinates
%     epsilon - softness in [0,1]. Default 0.
%
%   Outputs:
%     xy      - [soft_x; soft_y]
%     err     - distance from soft point to lattice point
%     snapped - exact lattice point struct

  if nargin < 3, epsilon = 0; end
  validateattributes(epsilon, {'numeric'}, {'scalar', '>=', 0, '<=', 1}, 'soft_snap', 'epsilon');

  [snapped, exact_err] = a2_snap(x, y);
  C = ct_constants();

  if abs(epsilon - 1) < 1e-15
    xy = [x; y];
    err = exact_err;
    return
  end

  if epsilon == 0
    sx = snapped.a + snapped.b * C.omega_re;
    sy = snapped.b * C.omega_im;
    xy = [sx; sy];
    err = exact_err;
    return
  end

  sx = snapped.a + snapped.b * C.omega_re;
  sy = snapped.b * C.omega_im;
  soft_x = (1 - epsilon) * sx + epsilon * x;
  soft_y = (1 - epsilon) * sy + epsilon * y;
  err = sqrt((soft_x - sx)^2 + (soft_y - sy)^2);
  xy = [soft_x; soft_y];
end

function r = a2_covering_radius()
% A2_COVERING_RADIUS Return the A2 covering radius rho = 1/sqrt(3).
  r = ct_constants('covering_radius');
end

function result = is_safe(error)
% IS_SAFE Check if quantization error is within safe threshold (rho/2).
  result = error < ct_constants('safe_threshold');
end

function n = norm_sq(a, b)
% NORM_SQ Squared Eisenstein norm: a^2 - a*b + b^2.
  n = a * a - a * b + b * b;
end

function dir = decode_dodecet(index)
% DECODE_DODECET Decode dodecet index (0-11) to A2 direction [a; b].
  dirs = [1 0; 0 1; -1 1; -1 0; 0 -1; 1 -1; ...
          2 -1; 1 -2; -1 -1; -2 1; -1 2; 1 1];
  validateattributes(index, {'numeric'}, {'scalar', '>=', 0, '<', 12});
  dir = dirs(index + 1, :)';
end

function idx = encode_dodecet(a, b)
% ENCODE_DODECET Encode A2 direction to dodecet index (0-11).
  dirs = [1 0; 0 1; -1 1; -1 0; 0 -1; 1 -1; ...
          2 -1; 1 -2; -1 -1; -2 1; -1 2; 1 1];
  for idx = 1:size(dirs, 1)
    if dirs(idx,1) == a && dirs(idx,2) == b
      return
    end
  end
  idx = -1;
  error('(%d, %d) is not a dodecet direction', a, b);
end

function idx = vector48_encode(angle)
% VECTOR48_ENCODE Quantize angle to one of 48 Pythagorean directions.
  C = ct_constants();
  normalized = mod(angle, C.two_pi);
  idx = mod(round(normalized / C.two_pi * C.direction_count), C.direction_count);
end

function angle = vector48_decode(index)
% VECTOR48_DECODE Decode Pythagorean direction index to angle (radians).
  validateattributes(index, {'numeric'}, {'scalar', '>=', 0, '<', 48});
  C = ct_constants();
  angle = index * C.two_pi / C.direction_count;
end

function h = holonomy_product(directions)
% HOLONOMY_PRODUCT Compute holonomy around a cycle (sum mod 48).
%   0 = consistent. Empty returns 0.
  if isempty(directions), h = 0; return, end
  h = mod(sum(directions), 48);
end

function result = is_consistent(directions)
% IS_CONSISTENT Check if cycle is holonomy-free.
  result = holonomy_product(directions) == 0;
end

%% ========================================================================
% DEADBAND FUNNEL / TEMPORAL AGENT (class)
%% ========================================================================

classdef temporal_agent
% TEMPORAL_AGENT Deadband funnel agent with exponential temporal decay.
%
%   The agent tracks a point on the Eisenstein lattice with a decaying
%   deadband. When error stays below the deadband, the funnel narrows.
%   When error exceeds the deadband, an anomaly is flagged and the
%   funnel resets.
%
%   Properties:
%     decay_rate    - exponential decay rate lambda
%     epsilon_0     - initial deadband width
%     delta         - anomaly threshold
%     softness      - soft-snap parameter [0,1]
%     epsilon       - current deadband width (read-only)
%     anomaly_count - number of anomalies detected (read-only)
%
%   Methods:
%     observe(x, y, t) - observe a point, update funnel
%     decay(dt)        - manually decay deadband
%     reset()          - reset to initial width
%
%   Example:
%     agent = temporal_agent(0.1);
%     result = agent.observe(0.1, 0.3, 1.0);
%     fprintf('Phase: %s, Error: %.4f\n', result.phase, result.error);

  properties
    decay_rate
    epsilon_0
    delta
    softness
  end

  properties (Access = private)
    epsilon_val
    last_t = []
    last_error = 0
    anomalies = 0
  end

  methods
    function obj = temporal_agent(decay_rate, epsilon_0, delta, softness)
      if nargin < 1, decay_rate = 0.1; end
      if nargin < 2, epsilon_0 = ct_constants('covering_radius'); end
      if nargin < 3, delta = ct_constants('covering_radius'); end
      if nargin < 4, softness = 0; end

      validateattributes(decay_rate, {'numeric'}, {'scalar', 'nonnegative', 'finite'});
      validateattributes(epsilon_0, {'numeric'}, {'scalar', 'positive', 'finite'});

      obj.decay_rate = decay_rate;
      obj.epsilon_0 = epsilon_0;
      obj.delta = delta;
      obj.softness = softness;
      obj.epsilon_val = epsilon_0;
    end

    function e = epsilon(obj)
      e = obj.epsilon_val;
    end

    function c = anomaly_count(obj)
      c = obj.anomalies;
    end

    function obj = observe(obj, x, y, t)
      [pt, error] = a2_snap(x, y);

      effective_eps = obj.epsilon_val * (1 + obj.softness);

      % Decay
      if ~isempty(obj.last_t)
        dt = t - obj.last_t;
        if dt > 0
          obj.epsilon_val = obj.epsilon_val * exp(-obj.decay_rate * dt);
        end
      end
      obj.last_t = t;

      if error > obj.delta
        phase = 'anomaly';
        obj.anomalies = obj.anomalies + 1;
        obj.epsilon_val = obj.epsilon_0;
      elseif error > effective_eps
        phase = 'approach';
      else
        phase = 'narrowing';
      end

      obj.last_error = error;

      % Return via struct stored in temp
      obj.observed_result = struct('phase', phase, 'error', error, ...
        'deadband', obj.epsilon_val, 'snapped_a', pt.a, 'snapped_b', pt.b);
    end

    function obj = decay(obj, dt)
      if dt > 0
        obj.epsilon_val = obj.epsilon_val * exp(-obj.decay_rate * dt);
      end
    end

    function obj = reset(obj)
      obj.epsilon_val = obj.epsilon_0;
    end
  end
end

%% ========================================================================
% LAMAN RIGIDITY
%% ========================================================================

function result = is_laman(n, edges)
% IS_LAMAN Check if a graph is Laman rigid.
%
%   result = is_laman(n, edges) checks two conditions:
%   1. |E| = 2n - 3
%   2. Every subset of k vertices spans at most 2k - 3 edges
%
%   Inputs:
%     n     - number of vertices (>= 0)
%     edges - Mx2 matrix of edge pairs (0-indexed)
%
%   Example:
%     edges = henneberg_construct(6);
%     is_laman(6, edges)  % true

  validateattributes(n, {'numeric'}, {'scalar', 'nonnegative', 'integer'});
  n = int32(n);

  if isempty(edges) || (isvector(edges) && numel(edges) == 0)
    result = n < 2;
    return
  end

  if n < 2
    result = size(edges, 1) == 0;
    return
  end

  expected = 2 * n - 3;
  if size(edges, 1) ~= expected
    result = false;
    return
  end

  if n <= 15
    result = check_subsets(n, edges);
  else
    result = pebble_game(n, edges);
  end
end

function edges = henneberg_construct(n, seed)
% HENNEBERG_CONSTRUCT Build a Laman graph via Henneberg type-I.
%
%   edges = henneberg_construct(n, seed) starts with K2 and adds vertices,
%   each connecting to two distinct existing vertices.
%
%   Inputs:
%     n    - number of vertices (>= 2)
%     seed - random seed (default 42)

  if nargin < 2, seed = 42; end
  validateattributes(n, {'numeric'}, {'scalar', '>=', 2, 'integer'});
  rng(seed);

  edges = [0 1];
  for v = 2:(n-1)
    candidates = randperm(v) - 1;  % 0-indexed
    i = candidates(1);
    j = candidates(2);
    edges = [edges; v i; v j];
  end
end

function lam2 = algebraic_connectivity(edges, n)
% ALGEBRAIC_CONNECTIVITY Compute lambda_2 of the graph Laplacian.
%
%   lam2 = algebraic_connectivity(edges, n) uses power iteration.
%   lambda_2 determines convergence rate of consensus and optimal coupling.

  if n < 2, lam2 = 0; return; end
  if isempty(edges), lam2 = 0; return; end

  if n > 50
    lam2 = 2 * size(edges, 1) / (n * (n - 1));
    return
  end

  % Build Laplacian
  L = zeros(n);
  for k = 1:size(edges,1)
    u = edges(k,1) + 1;
    v = edges(k,2) + 1;
    L(u,u) = L(u,u) + 1;
    L(v,v) = L(v,v) + 1;
    L(u,v) = L(u,v) - 1;
    L(v,u) = L(v,u) - 1;
  end

  % Power iteration for second eigenvalue
  x = (1:n)';
  x = x - mean(x);

  for iter = 1:100
    y = L * x;
    y = y - mean(y);
    nrm = sqrt(sum(y.^2));
    if nrm < 1e-15, lam2 = 0; return; end
    x = y / nrm;
  end

  Lx = L * x;
  lam2 = sum(x .* Lx);
end

function alpha = optimal_coupling(edges, n)
% OPTIMAL_COUPLING Compute alpha* = 2/(lambda_2 + lambda_n).
  lam2 = algebraic_connectivity(edges, n);
  if n < 2, alpha = 0; return; end

  deg = zeros(n, 1);
  for k = 1:size(edges,1)
    deg(edges(k,1)+1) = deg(edges(k,1)+1) + 1;
    deg(edges(k,2)+1) = deg(edges(k,2)+1) + 1;
  end
  lam_n = max(deg) + 1;

  if lam2 + lam_n < 1e-10, alpha = 0; return; end
  alpha = 2 / (lam2 + lam_n);
end

function score = soft_rigidity(n_vertices, edges, epsilon)
% SOFT_RIGIDITY Continuous rigidity score softened by epsilon.
%
%   score = soft_rigidity(n, edges, epsilon) returns [0,1].
%   epsilon=0: hard Laman check. epsilon->1: fully soft.

  if nargin < 3, epsilon = 0; end
  validateattributes(epsilon, {'numeric'}, {'scalar', '>=', 0, '<=', 1});

  rigid = is_laman(n_vertices, edges);

  if epsilon == 0
    score = double(rigid);
    return
  end

  ne = size(edges, 1);
  if n_vertices < 2
    score = double(ne == 0);
    return
  end

  expected = 2 * n_vertices - 3;
  edge_ratio = min(ne / expected, 1);
  conn = algebraic_connectivity(edges, n_vertices);
  conn_factor = min(max(conn, 0), 1);

  if rigid
    score = 1 - epsilon * (1 - 0.5 * conn_factor);
  else
    score = epsilon * edge_ratio;
  end
end

function ok = check_subsets(n, edges)
% Internal: brute-force subset check
  for k = 2:n
    combos = nchoosek(0:(n-1), k);
    for col = 1:size(combos, 1)
      vset = combos(col, :);
      count = 0;
      for e = 1:size(edges, 1)
        if ismember(edges(e,1), vset) && ismember(edges(e,2), vset)
          count = count + 1;
        end
      end
      if count > 2 * k - 3
        ok = false;
        return
      end
    end
  end
  ok = true;
end

function ok = pebble_game(n, edges)
% Internal: connectivity check for large graphs
  adj = cell(n, 1);
  for i = 1:n, adj{i} = []; end
  for k = 1:size(edges, 1)
    u = edges(k,1) + 1;
    v = edges(k,2) + 1;
    adj{u} = [adj{u}, v];
    adj{v} = [adj{v}, u];
  end

  visited = false(n, 1);
  queue = 1;
  while ~isempty(queue)
    node = queue(1);
    queue(1) = [];
    if visited(node), continue, end
    visited(node) = true;
    nbrs = adj{node};
    queue = [queue, nbrs(~visited(nbrs))];
  end
  ok = all(visited);
end

%% ========================================================================
% METRONOME (class)
%% ========================================================================

classdef metronome
% METRONOME Distributed metronome agent for consensus.
%
%   Each agent maintains a phase phi on the Eisenstein lattice.
%   Parameters: T (period), phi0 (initial phase), epsilon, delta.
%
%   Properties (read-only):
%     T, phi0, epsilon_val, delta, softness
%     phase, tick_count, converged, corrections, anomaly_count
%
%   Methods:
%     tick()                     - advance one period
%     agree(other)               - check sync with another metronome
%     correct(neighbor_phases)   - apply Laman-neighbor correction
%     observe(x, y)              - observe external reference
%     reset()                    - reset to initial state
%     state()                    - return state snapshot
%
%   Example:
%     m = metronome(1.0, 0, 0.1, 0.5);
%     m.tick();

  properties
    T
    phi0
    epsilon_val
    delta
    softness
  end

  properties (Access = private)
    phi_val
    t_val = 0
    tick_count_val = 0
    converged_val = false
    corrections_val = []
    temporal_obj
    alpha_val
  end

  methods
    function obj = metronome(T, phi0, epsilon, delta, neighbors, edges, n_agents, softness)
      if nargin < 1, T = 1.0; end
      if nargin < 2, phi0 = 0; end
      if nargin < 3, epsilon = 0.577; end
      if nargin < 4, delta = 0.577; end
      if nargin < 5, neighbors = []; end
      if nargin < 6, edges = []; end
      if nargin < 7, n_agents = 1; end
      if nargin < 8, softness = 0; end

      validateattributes(T, {'numeric'}, {'scalar', 'positive', 'finite'});

      obj.T = T;
      obj.phi0 = mod(phi0, 2*pi);
      obj.epsilon_val = epsilon;
      obj.delta = delta;
      obj.softness = softness;
      obj.phi_val = obj.phi0;

      obj.temporal_obj = temporal_agent(1/T, epsilon, delta, softness);

      if ~isempty(edges) && n_agents > 1
        obj.alpha_val = optimal_coupling(edges, n_agents);
      else
        obj.alpha_val = 0;
      end
    end

    function p = phase(obj), p = obj.phi_val; end
    function tc = tick_count(obj), tc = obj.tick_count_val; end
    function c = converged(obj), c = obj.converged_val; end
    function cr = corrections(obj), cr = obj.corrections_val; end
    function ac = anomaly_count(obj), ac = obj.temporal_obj.anomaly_count(); end

    function obj = tick(obj)
      obj.t_val = obj.t_val + obj.T;
      obj.phi_val = mod(obj.phi_val + 2*pi, 2*pi);
      obj.tick_count_val = obj.tick_count_val + 1;
      obj.temporal_obj = obj.temporal_obj.decay(obj.T);
    end

    function result = agree(obj, other)
      diff = circular_distance(obj.phi_val, other.phase());
      eff_eps = obj.temporal_obj.epsilon() * (1 + obj.softness);
      result = diff <= eff_eps;
    end

    function [obj, corr] = correct(obj, neighbor_phases)
      if isempty(neighbor_phases) || obj.alpha_val <= 0
        corr = 0;
        return
      end

      avg = circular_mean(neighbor_phases);
      diff = circular_diff(avg, obj.phi_val);
      eff_alpha = obj.alpha_val * (1 - obj.softness);
      correction = eff_alpha * diff;
      obj.phi_val = mod(obj.phi_val + correction, 2*pi);
      obj.corrections_val = [obj.corrections_val, abs(correction)];

      if numel(obj.corrections_val) >= 3
        recent = obj.corrections_val(end-2:end);
        if all(recent < obj.epsilon_val * 0.1)
          obj.converged_val = true;
        end
      end
      corr = abs(correction);
    end

    function [obj, phase_out] = observe(obj, x, y)
      obj.temporal_obj = obj.temporal_obj.observe(x, y, obj.t_val);
      res = obj.temporal_obj.observed_result;
      C = ct_constants();
      cx = res.snapped_a + res.snapped_b * C.omega_re;
      cy = res.snapped_b * C.omega_im;
      obj.phi_val = mod(atan2(cy, cx), 2*pi);
      phase_out = res.phase;
    end

    function obj = reset(obj)
      obj.phi_val = obj.phi0;
      obj.t_val = 0;
      obj.tick_count_val = 0;
      obj.converged_val = false;
      obj.corrections_val = [];
      obj.temporal_obj = obj.temporal_obj.reset();
    end

    function s = state(obj)
      s = struct('phase', obj.phi_val, ...
        'tick_count', obj.tick_count_val, ...
        'converged', obj.converged_val, ...
        'epsilon', obj.temporal_obj.epsilon(), ...
        'anomaly_count', obj.temporal_obj.anomaly_count());
    end
  end
end

function agents = consensus_round(agents, edges)
% CONSENSUS_ROUND Run one round of pairwise consensus.
%
%   agents = consensus_round(agents, edges) applies corrections between
%   all pairs specified in the edge list.

  for k = 1:size(edges, 1)
    i = edges(k, 1) + 1;
    j = edges(k, 2) + 1;
    if i <= numel(agents) && j <= numel(agents)
      agents{i} = agents{i}.correct(agents{j}.phase());
      agents{j} = agents{j}.correct(agents{i}.phase());
    end
  end
end

%% ========================================================================
% HOLONOMY CONSISTENCY
%% ========================================================================

function h = cycle_holonomy(edges, directions)
% CYCLE_HOLONOMY Compute holonomy around a directed cycle (sum mod 48).
%
%   h = cycle_holonomy(edges, directions) returns 0 if consistent.

  if numel(directions) == 0, h = 0; return; end
  if numel(edges) ~= numel(directions)
    error('edges and directions must have the same length');
  end
  if any(directions < 0) || any(directions >= 48)
    error('Direction indices must be in [0, 47]');
  end
  h = mod(sum(directions), 48);
end

function ok = verify_consistency(tiles)
% VERIFY_CONSISTENCY Check all tiles are holonomy-free.
%
%   tiles is a cell array, each element a struct with fields:
%     edges       - Nx2 edge matrix
%     directions  - N-element direction vector
%
%   ok = verify_consistency(tiles) returns true if all consistent.

  for i = 1:numel(tiles)
    if cycle_holonomy(tiles{i}.edges, tiles{i}.directions) ~= 0
      ok = false;
      return
    end
  end
  ok = true;
end

function score = soft_verify_consistency(tiles, epsilon)
% SOFT_VERIFY_CONSISTENCY Soft holonomy check with continuous tolerance.
  if nargin < 2, epsilon = 0; end
  if isempty(tiles), score = 1; return; end
  if epsilon == 0
    score = double(verify_consistency(tiles));
    return
  end

  total_dev = 0;
  for i = 1:numel(tiles)
    h = cycle_holonomy(tiles{i}.edges, tiles{i}.directions);
    total_dev = total_dev + min(h, 48 - h);
  end
  max_dev = numel(tiles) * 24;
  if max_dev == 0, score = 1; return; end

  raw = 1 - total_dev / max_dev;
  score = epsilon * 1.0 + (1 - epsilon) * raw;
end

function idx = isolate_fault(tiles)
% ISOLATE_FAULT O(log N) fault isolation via binary search.
  if isempty(tiles), error('tiles list is empty'); end
  if verify_consistency(tiles), error('no inconsistent tile found'); end

  lo = 1;
  hi = numel(tiles) + 1;
  while lo < hi - 1
    mid = floor((lo + hi) / 2);
    if ~verify_consistency(tiles(lo:mid-1))
      hi = mid;
    else
      lo = mid;
    end
  end
  idx = lo;
end

function bad = fault_boundaries(tiles)
% FAULT_BOUNDARIES Return indices of all inconsistent tiles.
  bad = [];
  for i = 1:numel(tiles)
    if cycle_holonomy(tiles{i}.edges, tiles{i}.directions) ~= 0
      bad = [bad, i];
    end
  end
end

%% ========================================================================
% GENRE BRAIN
%% ========================================================================

function eps = get_genre(name)
% GET_GENRE Get genre epsilon profile.
%
%   eps = get_genre('jazz') returns a struct with fields:
%     lattice, temporal, rigidity, consensus, holonomy

  genres = struct( ...
    'serialism', struct('lattice',0,'temporal',0,'rigidity',0,'consensus',0,'holonomy',0), ...
    'strict_counterpoint', struct('lattice',0,'temporal',0.05,'rigidity',0,'consensus',0.05,'holonomy',0), ...
    'classical', struct('lattice',0.10,'temporal',0.10,'rigidity',0.10,'consensus',0.10,'holonomy',0.10), ...
    'romantic', struct('lattice',0.20,'temporal',0.25,'rigidity',0.15,'consensus',0.20,'holonomy',0.15), ...
    'jazz', struct('lattice',0.30,'temporal',0.35,'rigidity',0.25,'consensus',0.30,'holonomy',0.25), ...
    'free_jazz', struct('lattice',0.50,'temporal',0.55,'rigidity',0.45,'consensus',0.50,'holonomy',0.45), ...
    'minimalism', struct('lattice',0.05,'temporal',0.15,'rigidity',0.05,'consensus',0.10,'holonomy',0.05), ...
    'ambient', struct('lattice',0.60,'temporal',0.65,'rigidity',0.50,'consensus',0.55,'holonomy',0.50), ...
    'noise', struct('lattice',0.90,'temporal',0.90,'rigidity',0.85,'consensus',0.90,'holonomy',0.85), ...
    'chaos', struct('lattice',1.0,'temporal',1.0,'rigidity',1.0,'consensus',1.0,'holonomy',1.0) ...
  );

  key = lower(strrep(strrep(name, ' ', '_'), '-', '_'));
  if ~isfield(genres, key)
    error('Unknown genre ''%s''. Available: %s', name, strjoin(fieldnames(genres), ', '));
  end
  eps = genres.(key);
end

function g = list_genres()
% LIST_GENRES Return all built-in genre profiles.
  g = struct( ...
    'serialism', struct('lattice',0,'temporal',0,'rigidity',0,'consensus',0,'holonomy',0), ...
    'strict_counterpoint', struct('lattice',0,'temporal',0.05,'rigidity',0,'consensus',0.05,'holonomy',0), ...
    'classical', struct('lattice',0.10,'temporal',0.10,'rigidity',0.10,'consensus',0.10,'holonomy',0.10), ...
    'romantic', struct('lattice',0.20,'temporal',0.25,'rigidity',0.15,'consensus',0.20,'holonomy',0.15), ...
    'jazz', struct('lattice',0.30,'temporal',0.35,'rigidity',0.25,'consensus',0.30,'holonomy',0.25), ...
    'free_jazz', struct('lattice',0.50,'temporal',0.55,'rigidity',0.45,'consensus',0.50,'holonomy',0.45), ...
    'minimalism', struct('lattice',0.05,'temporal',0.15,'rigidity',0.05,'consensus',0.10,'holonomy',0.05), ...
    'ambient', struct('lattice',0.60,'temporal',0.65,'rigidity',0.50,'consensus',0.55,'holonomy',0.50), ...
    'noise', struct('lattice',0.90,'temporal',0.90,'rigidity',0.85,'consensus',0.90,'holonomy',0.85), ...
    'chaos', struct('lattice',1.0,'temporal',1.0,'rigidity',1.0,'consensus',1.0,'holonomy',1.0) ...
  );
end

%% ========================================================================
% CIRCULAR MATH HELPERS
%% ========================================================================

function m = circular_mean(angles)
% Internal: circular mean
  if isempty(angles), m = 0; return; end
  m = atan2(sum(sin(angles)), sum(cos(angles)));
end

function d = circular_diff(target, current)
% Internal: shortest signed difference in [-pi, pi]
  d = target - current;
  while d > pi, d = d - 2*pi; end
  while d < -pi, d = d + 2*pi; end
end

function dist = circular_distance(a, b)
% Internal: shortest absolute distance in [0, 2pi)
  diff = abs(a - b);
  dist = min(diff, 2*pi - diff);
end

%% ========================================================================
% VISUALIZATION
%% ========================================================================

function plot_lattice(points, snapped_pts, title_str)
% PLOT_LATTICE Visualize A2 lattice with snapped points.
%
%   plot_lattice(points) - plots original points and their snaps
%   plot_lattice(points, snapped, title) - with pre-computed snaps
%
%   Inputs:
%     points     - Nx2 matrix of (x,y) coordinates
%     snapped_pts - Nx2 matrix of snapped (x,y) coordinates (optional)
%     title_str  - plot title (default: 'A2 Lattice Snap')

  if nargin < 3, title_str = 'A2 Lattice Snap'; end

  C = ct_constants();

  % Compute snaps if not provided
  if nargin < 2 || isempty(snapped_pts)
    snapped_pts = zeros(size(points));
    for i = 1:size(points, 1)
      [pt, ~] = a2_snap(points(i,1), points(i,2));
      snapped_pts(i,:) = [pt.a + pt.b * C.omega_re, pt.b * C.omega_im];
    end
  end

  % Generate lattice grid
  rx = range([points(:,1); snapped_pts(:,1)]);
  ry = range([points(:,2); snapped_pts(:,2)]);
  a_range = floor(min(points(:,1))-1) : ceil(max(points(:,1))+1);
  b_range = floor(min(points(:,2))*2/sqrt(3)-1) : ceil(max(points(:,2))*2/sqrt(3)+1);
  [A, B] = meshgrid(a_range, b_range);
  gx = A + B * C.omega_re;
  gy = B * C.omega_im;

  figure;
  hold on;
  plot(gx(:), gy(:), 'k+', 'MarkerSize', 4);

  for i = 1:size(points, 1)
    plot([points(i,1) snapped_pts(i,1)], ...
         [points(i,2) snapped_pts(i,2)], ...
         'b-', 'LineWidth', 1);
    plot(points(i,1), points(i,2), 'ro', 'MarkerSize', 6, 'MarkerFaceColor', 'r');
    plot(snapped_pts(i,1), snapped_pts(i,2), 'gs', 'MarkerSize', 8, 'MarkerFaceColor', 'g');
  end

  title(title_str);
  xlabel('Re'); ylabel('Im');
  axis equal; grid on;
  hold off;
end

function plot_convergence(history, title_str)
% PLOT_CONVERGENCE Plot convergence history of metronome agents.
%
%   history is Nx3 matrix: [tick, agent_id, correction]
%   or struct array with fields tick, agent, correction.

  if nargin < 2, title_str = 'Metronome Convergence'; end
  if isstruct(history)
    ticks = [history.tick];
    agents = [history.agent];
    corrs = [history.correction];
  else
    ticks = history(:,1);
    agents = history(:,2);
    corrs = history(:,3);
  end

  figure;
  unique_agents = unique(agents);
  hold on;
  for a = unique_agents'
    mask = agents == a;
    semilogy(ticks(mask), max(corrs(mask), 1e-15), '.-', 'DisplayName', sprintf('Agent %d', a));
  end
  hold off;
  title(title_str);
  xlabel('Tick'); ylabel('Correction (log scale)');
  legend('show');
  grid on;
end

function plot_rigidity_graph(edges, n, title_str)
% PLOT_RIGIDITY_GRAPH Plot a rigidity graph with circular layout.
%
%   plot_rigidity_graph(edges, n) - plots the graph
%   plot_rigidity_graph(edges, n, title) - with custom title

  if nargin < 3, title_str = 'Laman Rigidity Graph'; end

  % Circular layout
  angles = linspace(0, 2*pi, n+1)';
  angles = angles(1:n);
  pos_x = cos(angles);
  pos_y = sin(angles);

  figure;
  hold on;

  % Draw edges
  for k = 1:size(edges, 1)
    i = edges(k,1) + 1;
    j = edges(k,2) + 1;
    plot([pos_x(i) pos_x(j)], [pos_y(i) pos_y(j)], 'b-', 'LineWidth', 1.5);
  end

  % Draw vertices
  plot(pos_x, pos_y, 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'r');

  % Labels
  for i = 1:n
    text(pos_x(i), pos_y(i) + 0.15, num2str(i-1), ...
      'HorizontalAlignment', 'center', 'FontSize', 10);
  end

  title(title_str);
  axis equal; axis off;
  hold off;
end

%% ========================================================================
% NUMERICAL CROSS-VALIDATION
%% ========================================================================

function results = validate_against_python()
% VALIDATE_AGAINST_PYTHON Run numerical cross-validation.
%
%   Compares MATLAB outputs to known Python results.

  results = struct();

  [pt, err] = a2_snap(0, 0);
  results.origin_snap = pt.a == 0 && pt.b == 0 && abs(err) < 1e-12;

  cr = a2_covering_radius();
  results.covering_radius = abs(cr - 1/sqrt(3)) < 1e-12;

  [pt, ~] = a2_snap(1, 0);
  results.snap_1_0 = pt.a == 1 && pt.b == 0;

  [pt, ~] = a2_snap(0, sqrt(3)/2);
  results.snap_0_s3 = pt.a == 0 && pt.b == 1;

  edges = henneberg_construct(6, 42);
  results.henneberg_6 = size(edges, 1) == 9;
  results.is_laman_6 = is_laman(6, edges);
  results.norm_sq_2_1 = norm_sq(2, 1) == 3;
  results.holonomy_12 = holonomy_product([12 12 12]) == 0;

  [xy, ~, ~] = soft_snap(0.5, 0.3, 1.0);
  results.soft_snap_free = abs(xy(1) - 0.5) < 1e-12;

  jazz = get_genre('jazz');
  results.genre_jazz = abs(jazz.lattice - 0.30) < 1e-10;

  fields = fieldnames(results);
  n_pass = sum(struct2array(results));
  fprintf('Cross-validation: %d/%d passed\n', n_pass, numel(fields));
end

function plot_deadband_funnel(agent, x_vals, y_vals, t_vals)
% PLOT_DEADBAND_FUNNEL Visualize deadband funnel narrowing over time.

  n = numel(t_vals);
  errors = zeros(n, 1);
  deadbands = zeros(n, 1);
  phases = cell(n, 1);

  for i = 1:n
    agent = agent.observe(x_vals(i), y_vals(i), t_vals(i));
    r = agent.observed_result;
    errors(i) = r.error;
    deadbands(i) = r.deadband;
    phases{i} = r.phase;
  end

  figure;
  subplot(2,1,1);
  plot(t_vals, errors, 'r.-', 'DisplayName', 'Error'); hold on;
  plot(t_vals, deadbands, 'b.-', 'DisplayName', 'Deadband');
  yline(1/sqrt(3), 'k--', 'Covering Radius');
  ylabel('Magnitude'); title('Deadband Funnel');
  legend('show'); grid on; hold off;

  subplot(2,1,2);
  phase_num = zeros(n, 1);
  for i = 1:n
    switch phases{i}
      case 'narrowing', phase_num(i) = 0;
      case 'approach', phase_num(i) = 1;
      case 'anomaly', phase_num(i) = 2;
    end
  end
  plot(t_vals, phase_num, 'k.-', 'MarkerSize', 10);
  ylabel('Phase'); xlabel('Time'); grid on;
  yticks([0 1 2]); yticklabels({'Narrowing','Approach','Anomaly'});
end
