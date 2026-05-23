/-- Shared utilities for the Constraint Theory formalization. -/
namespace ConstraintTheory.Basic

/-- The sign function returning -1, 0, or +1. -/
def sign (x : ℝ) : ℝ :=
  if x < 0 then -1 else if x = 0 then 0 else 1

/-- Round to nearest integer. -/
def round (x : ℝ) : ℤ :=
  Int.floor (x + 1 / 2)

end ConstraintTheory.Basic
