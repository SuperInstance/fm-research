%% constraint-theory-core MATLAB Test Suite
% Verifies numerical correctness of all modules.
%
% Run each section individually (Ctrl+Enter) or run all.

tests_passed = 0;
tests_failed = 0;

    function test(name, condition)
      if condition
        fprintf('  PASS: %s\n', name);
        tests_passed = tests_passed + 1;
      else
        fprintf('  FAIL: %s\n', name);
        tests_failed = tests_failed + 1;
      end
    end

%% --- A2 Lattice ---
fprintf('--- A2 Lattice ---\n');

% Origin
[pt, err] = a2_snap(0, 0);
test('Origin snap: (0,0)', pt.a == 0 && pt.b == 0);
test('Origin snap: error=0', abs(err) < 1e-12);

% Covering radius guarantee
rng(123);
all_within = true;
for i = 1:100
  x = rand()*20 - 10;
  y = rand()*20 - 10;
  [~, e] = a2_snap(x, y);
  if e > 1/sqrt(3) + 1e-10
    all_within = false;
    break
  end
end
test('Covering radius guarantee (100 random)', all_within);

% Known points
[pt, ~] = a2_snap(1, 0);
test('snap(1,0) -> (1,0)', pt.a == 1 && pt.b == 0);

% Soft snap eps=0
[~, err_hard] = a2_snap(0.5, 0.3);
[~, err_soft] = soft_snap(0.5, 0.3, 0);
test('soft_snap(eps=0) == snap', abs(err_soft - err_hard) < 1e-12);

% Soft snap eps=1
[xy, ~, ~] = soft_snap(0.5, 0.3, 1.0);
test('soft_snap(eps=1) returns original', abs(xy(1)-0.5)<1e-12 && abs(xy(2)-0.3)<1e-12);

% is_safe
test('is_safe(0.1) = true', is_safe(0.1));
test('is_safe(0.5) = false', ~is_safe(0.5));

% norm_sq
test('norm_sq(1,0) = 1', norm_sq(1,0) == 1);
test('norm_sq(1,1) = 1', norm_sq(1,1) == 1);
test('norm_sq(2,1) = 3', norm_sq(2,1) == 3);

% Dodecet roundtrip
dodecet_ok = true;
for i = 0:11
  d = decode_dodecet(i);
  idx = encode_dodecet(d(1), d(2));
  if idx ~= i, dodecet_ok = false; break; end
end
test('Dodecet roundtrip 0-11', dodecet_ok);

% Holonomy
test('holonomy(empty) = 0', holonomy_product([]) == 0);
test('holonomy(12,12,12) = 0', holonomy_product([12 12 12]) == 0);

%% --- Temporal Agent ---
fprintf('\n--- Temporal Agent ---\n');

agent = temporal_agent(0.1);
agent = agent.observe(0.1, 0.3, 1.0);
r = agent.observed_result;
test('Initial phase is narrowing or approach', ...
  strcmp(r.phase, 'narrowing') || strcmp(r.phase, 'approach'));

agent2 = temporal_agent(0.1, 1/sqrt(3), 0.01);
agent2 = agent2.observe(5, 5, 1.0);
test('Anomaly detected for far point', strcmp(agent2.observed_result.phase, 'anomaly'));

agent3 = temporal_agent(1.0, 1.0);
eps_before = agent3.epsilon();
agent3 = agent3.decay(1.0);
eps_after = agent3.epsilon();
test('Decay reduces epsilon', eps_after < eps_before);

agent3 = agent3.reset();
test('Reset restores epsilon', abs(agent3.epsilon() - 1.0) < 1e-10);

%% --- Laman Rigidity ---
fprintf('\n--- Laman Rigidity ---\n');

for n = [2 3 5 10 15]
  edges = henneberg_construct(n);
  test(sprintf('Henneberg(%d) has %d edges', n, 2*n-3), size(edges,1) == 2*n-3);
  test(sprintf('Henneberg(%d) is Laman', n), is_laman(n, edges));
end

bad_edges = [0 1; 1 2];
test('3 vertices, 2 edges not Laman', ~is_laman(3, bad_edges));
test('0 vertices, empty edges is Laman', is_laman(0, []));

edges5 = henneberg_construct(5);
ac = algebraic_connectivity(edges5, 5);
test('Algebraic connectivity > 0', ac > 0);

oc = optimal_coupling(edges5, 5);
test('Optimal coupling in (0,1)', oc > 0 && oc < 1);

%% --- Metronome ---
fprintf('\n--- Metronome ---\n');

m = metronome(1.0, 0, 0.1, 0.5);
test('Initial phase = 0', abs(m.phase()) < 1e-10);
test('Initial tick_count = 0', m.tick_count() == 0);

m = m.tick();
test('After tick: tick_count = 1', m.tick_count() == 1);

m2 = metronome(1.0, pi/4, 0.1, 0.5);
test('Phase = pi/4', abs(m2.phase() - pi/4) < 1e-10);

m2 = m2.reset();
test('Reset: tick_count = 0', m2.tick_count() == 0);

%% --- Holonomy ---
fprintf('\n--- Holonomy ---\n');

tiles_ok = { struct('edges', [0 1; 1 2; 2 0], 'directions', [12 12 12]), ...
             struct('edges', [0 1; 1 3; 3 0], 'directions', [24 24 0]) };
test('verify_consistency: all ok', verify_consistency(tiles_ok));

tiles_bad = { struct('edges', [0 1; 1 2; 2 0], 'directions', [12 12 12]), ...
              struct('edges', [0 1; 1 2; 2 0], 'directions', [1 2 3]) };
test('verify_consistency: has bad', ~verify_consistency(tiles_bad));

bad = fault_boundaries(tiles_bad);
test('fault_boundaries = [2]', isequal(bad, 2));

%% --- Genre Brain ---
fprintf('\n--- Genre Brain ---\n');

jazz = get_genre('jazz');
test('Jazz lattice = 0.30', abs(jazz.lattice - 0.30) < 1e-10);

serialism = get_genre('serialism');
test('Serialism: all zeros', ...
  serialism.lattice==0 && serialism.temporal==0 && serialism.rigidity==0);

chaos = get_genre('chaos');
test('Chaos: all ones', ...
  chaos.lattice==1 && chaos.temporal==1 && chaos.rigidity==1);

%% --- Summary ---
fprintf('\n=== Results: %d passed, %d failed ===\n', tests_passed, tests_failed);
if tests_failed > 0
  fprintf('SOME TESTS FAILED!\n');
else
  fprintf('All tests passed!\n');
end
