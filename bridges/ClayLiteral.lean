/-
Clay's Navier–Stokes problem, written literally in Lean (row K0 of
evidence/formal/clay-lean-bridges.md).

Source: C. L. Fefferman, "Existence and smoothness of the Navier–Stokes equation",
Clay Mathematics Institute, navierstokes.pdf (SHA-256 c1b5f27b…a06d0c), equations
(1)–(11), alternatives (C) and (D), and the erratum on page 6.

This file is deliberately written in a different style from the DeepMind/OpenAI
formalization: coordinates, repeated partial derivatives along basis vectors,
one-sided time derivatives at t = 0, and the Lebesgue integral of a nonnegative
function. It contains definitions only, no proofs, so that it can be reviewed
against the PDF before any bridge lemma is written. Interpretive choices are
marked "READING" and listed in bridges/README.md.
-/
import Mathlib

open MeasureTheory

namespace ClayLiteral

/-- Position space ℝ³ with the Euclidean norm. -/
abbrev R3 := EuclideanSpace ℝ (Fin 3)

/-- The j-th unit vector e_j. -/
noncomputable def e (j : Fin 3) : R3 := EuclideanSpace.single j 1

/-- Smoothness on all of ℝ³: C^∞ in the Fréchet sense (not analytic). -/
def SmoothR3 {X : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X] (g : R3 → X) : Prop :=
  ContDiff ℝ ((⊤ : ℕ∞) : WithTop ℕ∞) g

/-- ∂^α for a vector field on ℝ³, with the multi-index written as the list of directions
    in which to differentiate, e.g. α = (2, 0, 1) as [0, 0, 2]. -/
noncomputable def dx : List (Fin 3) → (R3 → R3) → (R3 → R3)
  | [], g => g
  | j :: js, g => fun x => fderiv ℝ (dx js g) x (e j)

/-- Repeated one-sided time derivative ∂_t^m on t ≥ 0, for g(x, t). -/
noncomputable def dt {X : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X] :
    ℕ → (R3 → ℝ → X) → (R3 → ℝ → X)
  | 0, g => g
  | m + 1, g => fun x t => derivWithin (fun s => dt m g x s) (Set.Ici 0) t

/-- Mixed derivative ∂_x^α of g(·, t), applied after any time derivatives. -/
noncomputable def dxt : List (Fin 3) → (R3 → ℝ → R3) → (R3 → ℝ → R3)
  | [], g => g
  | j :: js, g => fun x t => fderiv ℝ (fun y => dxt js g y t) x (e j)

/-- C^∞(ℝ³ × [0, ∞)). READING (row S4): taken as the restriction of a C^∞ function
    on ℝ³ × ℝ. The alternative reading, continuous one-sided derivatives of every
    order up to t = 0, is `SmoothOneSided` below; (C) and (D) are stated under both. -/
def SmoothUpToBoundary {X : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X]
    (g : R3 → ℝ → X) : Prop :=
  ∃ G : R3 × ℝ → X, ContDiff ℝ ((⊤ : ℕ∞) : WithTop ℕ∞) G ∧ ∀ x t, 0 ≤ t → G (x, t) = g x t

/-- C^∞(ℝ³ × [0, ∞)), second READING (row S4): derivatives of every order exist one-sidedly
    at t = 0 and are continuous up to t = 0, i.e. `ContDiffOn` within the closed half-space. -/
def SmoothOneSided {X : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X]
    (g : R3 → ℝ → X) : Prop :=
  ContDiffOn ℝ ((⊤ : ℕ∞) : WithTop ℕ∞) (Function.uncurry g) (Set.univ ×ˢ Set.Ici 0)

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

/-- Equation (3). -/
def Eq3 (u0 : R3 → R3) (u : R3 → ℝ → R3) : Prop := ∀ x, u x 0 = u0 x

/-- Condition (4): for any α and K, |∂^α u°(x)| ≤ C_{αK} (1 + |x|)^{-K} on ℝ³.
    READING: K ranges over the reals. -/
def Cond4 (u0 : R3 → R3) : Prop :=
  ∀ α : List (Fin 3), ∀ K : ℝ, ∃ C : ℝ, ∀ x, ‖dx α u0 x‖ ≤ C * (1 + ‖x‖) ^ (-K)

/-- Condition (5): for any α, m, K, |∂_x^α ∂_t^m f(x,t)| ≤ C (1 + |x| + t)^{-K} on ℝ³ × [0, ∞). -/
def Cond5 (f : R3 → ℝ → R3) : Prop :=
  ∀ α : List (Fin 3), ∀ m : ℕ, ∀ K : ℝ, ∃ C : ℝ, ∀ x t, 0 ≤ t →
    ‖dxt α (dt m f) x t‖ ≤ C * (1 + ‖x‖ + t) ^ (-K)

/-- Condition (6) (and (11)): p, u ∈ C^∞(ℝ³ × [0, ∞)). -/
def Cond6 (u : R3 → ℝ → R3) (p : R3 → ℝ → ℝ) : Prop :=
  SmoothUpToBoundary u ∧ SmoothUpToBoundary p

/-- Condition (6) under the second reading of C^∞ on a closed set. -/
def Cond6OneSided (u : R3 → ℝ → R3) (p : R3 → ℝ → ℝ) : Prop :=
  SmoothOneSided u ∧ SmoothOneSided p

/-- Condition (7): ∫_{ℝ³} |u(x,t)|² dx < C for all t ≥ 0, as a Lebesgue integral of a
    nonnegative function. -/
def Cond7 (u : R3 → ℝ → R3) : Prop :=
  ∃ C : ℝ, ∀ t, 0 ≤ t → (∫⁻ x, ENNReal.ofReal (‖u x t‖ ^ 2)) < ENNReal.ofReal C

/-- Condition (8): u°(x + e_j) = u°(x) and f(x + e_j, t) = f(x, t). -/
def Cond8 (u0 : R3 → R3) (f : R3 → ℝ → R3) : Prop :=
  (∀ x j, u0 (x + e j) = u0 x) ∧ (∀ x t j, 0 ≤ t → f (x + e j) t = f x t)

/-- Condition (9): for any α, m, K, |∂_x^α ∂_t^m f(x,t)| ≤ C (1 + |t|)^{-K} on ℝ³ × [0, ∞). -/
def Cond9 (f : R3 → ℝ → R3) : Prop :=
  ∀ α : List (Fin 3), ∀ m : ℕ, ∀ K : ℝ, ∃ C : ℝ, ∀ x t, 0 ≤ t →
    ‖dxt α (dt m f) x t‖ ≤ C * (1 + |t|) ^ (-K)

/-- Condition (10): u(x, t) = u(x + e_j, t) on ℝ³ × [0, ∞). -/
def Cond10 (u : R3 → ℝ → R3) : Prop := ∀ x t j, 0 ≤ t → u x t = u (x + e j) t

/-- The erratum: p(x + e_j, t) = p(x, t). READING (row S7): whether this is a condition
    on solutions is open, so alternative (D) is stated both with and without it. -/
def Erratum (p : R3 → ℝ → ℝ) : Prop := ∀ x t j, 0 ≤ t → p (x + e j) t = p x t

/-- Alternative (C), for a given ν > 0: there exist a smooth, divergence-free u° on ℝ³ and a
    smooth f on ℝ³ × [0, ∞) satisfying (4), (5), for which there exist no solutions (p, u)
    of (1), (2), (3), (6), (7) on ℝ³ × [0, ∞). -/
def AltC (ν : ℝ) : Prop :=
  ∃ (u0 : R3 → R3) (f : R3 → ℝ → R3),
    SmoothR3 u0 ∧ (∀ x, div u0 x = 0) ∧ SmoothUpToBoundary f ∧ Cond4 u0 ∧ Cond5 f ∧
    ¬ ∃ (p : R3 → ℝ → ℝ) (u : R3 → ℝ → R3),
      Eq1 ν f u p ∧ Eq2 u ∧ Eq3 u0 u ∧ Cond6 u p ∧ Cond7 u

/-- Alternative (D), with the erratum read as a condition on solutions. -/
def AltD_withErratum (ν : ℝ) : Prop :=
  ∃ (u0 : R3 → R3) (f : R3 → ℝ → R3),
    SmoothR3 u0 ∧ (∀ x, div u0 x = 0) ∧ SmoothUpToBoundary f ∧ Cond8 u0 f ∧ Cond9 f ∧
    ¬ ∃ (p : R3 → ℝ → ℝ) (u : R3 → ℝ → R3),
      Eq1 ν f u p ∧ Eq2 u ∧ Eq3 u0 u ∧ Cond10 u ∧ Cond6 u p ∧ Erratum p

/-- Alternative (D), without the erratum. A stronger claim, since more solutions are excluded. -/
def AltD_withoutErratum (ν : ℝ) : Prop :=
  ∃ (u0 : R3 → R3) (f : R3 → ℝ → R3),
    SmoothR3 u0 ∧ (∀ x, div u0 x = 0) ∧ SmoothUpToBoundary f ∧ Cond8 u0 f ∧ Cond9 f ∧
    ¬ ∃ (p : R3 → ℝ → ℝ) (u : R3 → ℝ → R3),
      Eq1 ν f u p ∧ Eq2 u ∧ Eq3 u0 u ∧ Cond10 u ∧ Cond6 u p

/-- Alternative (C) under the second reading of C^∞(ℝ³ × [0, ∞)). -/
def AltC_oneSided (ν : ℝ) : Prop :=
  ∃ (u0 : R3 → R3) (f : R3 → ℝ → R3),
    SmoothR3 u0 ∧ (∀ x, div u0 x = 0) ∧ SmoothOneSided f ∧ Cond4 u0 ∧ Cond5 f ∧
    ¬ ∃ (p : R3 → ℝ → ℝ) (u : R3 → ℝ → R3),
      Eq1 ν f u p ∧ Eq2 u ∧ Eq3 u0 u ∧ Cond6OneSided u p ∧ Cond7 u

/-- Alternative (D), with the erratum on solutions, under the second reading. -/
def AltD_withErratum_oneSided (ν : ℝ) : Prop :=
  ∃ (u0 : R3 → R3) (f : R3 → ℝ → R3),
    SmoothR3 u0 ∧ (∀ x, div u0 x = 0) ∧ SmoothOneSided f ∧ Cond8 u0 f ∧ Cond9 f ∧
    ¬ ∃ (p : R3 → ℝ → ℝ) (u : R3 → ℝ → R3),
      Eq1 ν f u p ∧ Eq2 u ∧ Eq3 u0 u ∧ Cond10 u ∧ Cond6OneSided u p ∧ Erratum p

/-- Sanity check: dropping a requirement on solutions can only make (D) stronger. -/
theorem altD_withoutErratum_imp_withErratum (ν : ℝ) :
    AltD_withoutErratum ν → AltD_withErratum ν := by
  rintro ⟨u0, f, h1, h2, h3, h4, h5, hno⟩
  refine ⟨u0, f, h1, h2, h3, h4, h5, ?_⟩
  rintro ⟨p, u, hu1, hu2, hu3, hu10, hu6, -⟩
  exact hno ⟨p, u, hu1, hu2, hu3, hu10, hu6⟩

end ClayLiteral
