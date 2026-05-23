import Mathlib.Data.Finset.Basic
import Mathlib.Data.Nat.Basic
import Mathlib.Tactic

namespace ConstraintTheory.LamanRigidity

/-- An edge as an unordered pair of vertex indices. -/
structure Edge (n : ℕ) where
  src : Fin n
  dst : Fin n
  h_ne : src ≠ dst
  deriving DecidableEq

/-- Edge set of a graph on n vertices. -/
def EdgeSet (n : ℕ) := Finset (Edge n)

/-- The Laman condition: |E| = 2n - 3 and every vertex subset
    spans at most 2|V'| - 3 edges. -/
def IsLaman {n : ℕ} (edges : EdgeSet n) : Prop :=
  edges.card = 2 * n - 3 ∧
  ∀ (V' : Finset (Fin n)),
    V'.card ≥ 2 →
      (edges.filter (fun e => e.src ∈ V' ∧ e.dst ∈ V')).card ≤ 2 * V'.card - 3

/-- Laman graphs have exactly 2n-3 edges. -/
theorem laman_edge_count {n : ℕ} (edges : EdgeSet n)
    (h : IsLaman edges) : edges.card = 2 * n - 3 := h.1

/-- Subgraph sparsity: every subgraph of a Laman graph is (2,3)-sparse. -/
theorem laman_subgraph_sparse {n : ℕ} (edges : EdgeSet n)
    (h : IsLaman edges) (V' : Finset (Fin n)) (hV' : V'.card ≥ 2) :
    (edges.filter (fun e => e.src ∈ V' ∧ e.dst ∈ V')).card ≤ 2 * V'.card - 3 :=
  h.2 V' hV'

/-- Adding one edge to a Laman graph overconstrains. -/
theorem laman_overconstrained {n : ℕ} (edges : EdgeSet n) (e : Edge n)
    (h_laman : IsLaman edges) (h_new : ¬e ∈ edges) :
    (insert e edges).card > 2 * n - 3 := by
  rw [Finset.card_insert_of_not_mem h_new, laman_edge_count edges h_laman]; omega

/-- Removing one edge from a Laman graph creates flexibility. -/
theorem laman_flexible {n : ℕ} (edges : EdgeSet n) (e : Edge n)
    (h_laman : IsLaman edges) (h_mem : e ∈ edges) :
    (edges.erase e).card < 2 * n - 3 := by
  rw [Finset.card_erase_of_mem h_mem, laman_edge_count edges h_laman]; omega

end ConstraintTheory.LamanRigidity
