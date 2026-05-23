import ConstraintTheory.A2Lattice
import ConstraintTheory.LamanRigidity
import ConstraintTheory.Snap
import ConstraintTheory.Deadband
import ConstraintTheory.Consensus
import ConstraintTheory.Holonomy

namespace ConstraintTheory

open A2Lattice LamanRigidity Snap Deadband Consensus Holonomy

/-- A complete constraint system. -/
structure ConstraintSystem (n : ℕ) where
  positions : Fin n → A2Point
  edges : LamanRigidity.EdgeSet n
  h_laman : IsLaman edges
  deadband_epsilon : ℝ
  h_eps : deadband_epsilon > 0
  consensus_alpha : ℝ
  h_alpha : consensus_alpha > 0 ∧ consensus_alpha < 1

/-- System rigidity from Laman condition. -/
theorem system_rigid {n : ℕ} (sys : ConstraintSystem n) :
    sys.edges.card = 2 * n - 3 :=
  laman_edge_count sys.edges sys.h_laman

/-- System stability from deadband convergence. -/
theorem system_stable {n : ℕ} (sys : ConstraintSystem n) (target : ℝ) (i : Fin n) :
    ∃ (T : ℕ),
      deadband_iter target sys.deadband_epsilon T (sys.positions i |>.u) = target := by
  exact deadband_converges target sys.deadband_epsilon sys.h_eps (sys.positions i |>.u)

end ConstraintTheory
