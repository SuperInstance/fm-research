%% constraint-theory-core MATLAB Examples
% Demonstrates each module of the constraint theory system.
%
% Run each section (Ctrl+Enter in MATLAB, or section by section).

%% ========================================================================
% 1. A2 Lattice
%% ========================================================================

% Snap test points
test_points = [0.5 0.3; 1.2 0.8; -0.7 1.1; 0 0; 0.3 sqrt(3)/2];
fprintf('--- A2 Lattice Snap ---\n');
for i = 1:size(test_points, 1)
  [pt, err] = a2_snap(test_points(i,1), test_points(i,2));
  fprintf('  snap(%.2f, %.2f) -> (%d, %d), error=%.6f, safe=%d\n', ...
    test_points(i,1), test_points(i,2), pt.a, pt.b, err, is_safe(err));
end

fprintf('  Covering radius: %.6f\n', a2_covering_radius());

% Soft snap
[xy, err, snp] = soft_snap(0.5, 0.3, 0.3);
fprintf('  soft_snap(0.5, 0.3, eps=0.3) -> (%.4f, %.4f)\n', xy(1), xy(2));

% Dodecet
dir = decode_dodecet(0);
fprintf('  Dodecet 0: (%d, %d)\n', dir(1), dir(2));

% Vector48
idx = vector48_encode(pi/4);
fprintf('  pi/4 -> direction %d -> angle %.4f\n', idx, vector48_decode(idx));

%% ========================================================================
% 2. Deadband Funnel
%% ========================================================================

fprintf('\n--- Deadband Funnel ---\n');
agent = temporal_agent(0.1);

obs = [0.1 0.3 1.0; 0.12 0.28 2.0; 0.11 0.31 3.0; 0.5 0.5 4.0; 0.1 0.3 5.0];
for i = 1:size(obs, 1)
  agent = agent.observe(obs(i,1), obs(i,2), obs(i,3));
  r = agent.observed_result;
  fprintf('  t=%.1f: phase=%s, error=%.4f, deadband=%.4f\n', ...
    obs(i,3), r.phase, r.error, r.deadband);
end
fprintf('  Anomaly count: %d\n', agent.anomaly_count());

%% ========================================================================
% 3. Laman Rigidity
%% ========================================================================

fprintf('\n--- Laman Rigidity ---\n');
for n = [3 5 8 10]
  edges = henneberg_construct(n);
  fprintf('  n=%d: %d edges, is_laman=%d\n', n, size(edges,1), is_laman(n, edges));
end

edges6 = henneberg_construct(6);
ac = algebraic_connectivity(edges6, 6);
oc = optimal_coupling(edges6, 6);
fprintf('  n=6: lambda_2=%.6f, alpha*=%.6f\n', ac, oc);

sr = soft_rigidity(6, edges6, 0.3);
fprintf('  n=6: soft_rigidity(eps=0.3)=%.4f\n', sr);

%% ========================================================================
% 4. Metronome Consensus
%% ========================================================================

fprintf('\n--- Metronome Consensus ---\n');
n_agents = 5;
edges5 = henneberg_construct(n_agents);

agents = cell(1, n_agents);
for i = 1:n_agents
  agents{i} = metronome(1.0, rand()*2*pi, 0.577, 0.577, [], edges5, n_agents);
end
fprintf('  %d agents, %d edges\n', n_agents, size(edges5,1));

% Run 20 consensus rounds
for round = 1:20
  for i = 1:n_agents
    agents{i} = agents{i}.tick();
  end
  agents = consensus_round(agents, edges5);
end

converged_count = 0;
phases = zeros(1, n_agents);
for i = 1:n_agents
  if agents{i}.converged(), converged_count = converged_count + 1; end
  phases(i) = agents{i}.phase();
end
fprintf('  After 20 rounds: %d/%d converged\n', converged_count, n_agents);
fprintf('  Phase spread: %.6f rad\n', max(phases) - min(phases));

%% ========================================================================
% 5. Holonomy
%% ========================================================================

fprintf('\n--- Holonomy ---\n');

tiles_ok = { struct('edges', [0 1; 1 2; 2 0], 'directions', [12 12 12]), ...
             struct('edges', [0 1; 1 3; 3 0], 'directions', [24 24 0]) };
fprintf('  Consistent tiles: %d\n', verify_consistency(tiles_ok));

tiles_bad = { struct('edges', [0 1; 1 2; 2 0], 'directions', [12 12 12]), ...
              struct('edges', [0 1; 1 2; 2 0], 'directions', [1 2 3]) };
fprintf('  Mixed tiles: %d\n', verify_consistency(tiles_bad));

bad = fault_boundaries(tiles_bad);
fprintf('  Bad indices: %s\n', mat2str(bad));

sv = soft_verify_consistency(tiles_bad, 0.5);
fprintf('  Soft verify (eps=0.5): %.4f\n', sv);

%% ========================================================================
% 6. Genre Brain
%% ========================================================================

fprintf('\n--- Genre Brain ---\n');
for g = {'classical', 'jazz', 'ambient', 'noise'}
  eps = get_genre(g{1});
  fprintf('  %-20s: lattice=%.2f temporal=%.2f rigidity=%.2f\n', ...
    g{1}, eps.lattice, eps.temporal, eps.rigidity);
end

fprintf('\n=== All examples completed! ===\n');
