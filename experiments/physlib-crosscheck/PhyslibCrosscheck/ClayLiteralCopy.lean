/-
Verbatim copy of the definitions of `R3`, `e`, `div`, `Eq1` and `Eq2` from
bridges/ClayLiteral.lean (SHA-256 1998dac2bee2477b8cc1d100f5345574624bf62290d1f85abf27203b9f8acb2d,
lines 22–23, 25–26, 62–64 and 66–76), so that they can be compared with Physlib, which
needs Lean 4.35.0 while the main study is pinned to Lean 4.34.0-rc2. The text of each
definition and its docstring is unchanged.
-/
import Mathlib

namespace ClayLiteral

/-- Position space ℝ³ with the Euclidean norm. -/
abbrev R3 := EuclideanSpace ℝ (Fin 3)

/-- The j-th unit vector e_j. -/
noncomputable def e (j : Fin 3) : R3 := EuclideanSpace.single j 1

/-- div u = Σᵢ ∂uᵢ/∂xᵢ (equation (2), and the condition on u°). -/
noncomputable def div (u : R3 → R3) (x : R3) : ℝ :=
  ∑ i : Fin 3, fderiv ℝ (fun y => u y i) x (e i)

/-- Equation (1), component i, at (x, t) with t ≥ 0:
    ∂uᵢ/∂t + Σⱼ uⱼ ∂uᵢ/∂xⱼ = ν Δuᵢ − ∂p/∂xᵢ + fᵢ, with Δ = Σₖ ∂²/∂xₖ². -/
def Eq1 (ν : ℝ) (f u : R3 → ℝ → R3) (p : R3 → ℝ → ℝ) : Prop :=
  ∀ x t, 0 ≤ t → ∀ i : Fin 3,
    derivWithin (fun s => u x s i) (Set.Ici 0) t
      + ∑ j : Fin 3, u x t j * fderiv ℝ (fun y => u y t i) x (e j)
    = ν * ∑ k : Fin 3, fderiv ℝ (fun y => fderiv ℝ (fun z => u z t i) y (e k)) x (e k)
      - fderiv ℝ (fun y => p y t) x (e i) + f x t i

/-- Equation (2) on ℝ³ × [0, ∞). -/
def Eq2 (u : R3 → ℝ → R3) : Prop := ∀ x t, 0 ≤ t → div (fun y => u y t) x = 0

end ClayLiteral
