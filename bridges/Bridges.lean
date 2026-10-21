/-
Bridge lemmas between OpenAI's formal statement and the literal rendering of Clay's text
in ClayLiteral.lean. Row IDs refer to evidence/formal/clay-lean-bridges.md.

The import is OpenAI's solution module, so `navier_stokes_breakdown_R3` and
`navier_stokes_breakdown_periodic` below are OpenAI's proved theorems, not the challenge
placeholders. Its definitions come from NavierStokes.ComparatorDefinitions, which Comparator
checked against the challenge statement.

Direction, as required by the risk review:
- data rows (D*): formal data condition ⇒ Clay data condition;
- solution rows (S*): Clay solution condition ⇒ formal solution condition.

K1 is stated conditionally: every bridge not yet proved is an explicit, named hypothesis.
-/
import Mathlib
import NavierStokes.ComparatorSolution
import ClayLiteral

namespace Bridges

open ClayLiteral
open NavierStokes.Comparator
open scoped Laplacian

/-- Row D6: formal periodic data imply Clay's condition (8). -/
theorem d6 (u0 : R3 → R3) (f : R3 → ℝ → R3)
    (hu : InitialVelocityConditionPeriodic u0) (hf : ForceConditionPeriodic f) :
    Cond8 u0 f :=
  ⟨fun x j => hu.isOnePeriodic x j, fun x t j ht => hf.isOnePeriodic t ht x j⟩

/-- Row S3: Clay's initial condition (3) gives the formal `initial_condition` field. -/
theorem s3 (u0 : R3 → R3) (u : R3 → ℝ → R3) (h : Eq3 u0 u) : ∀ x, u x 0 = u0 x := h

/-- Row S4, under ClayLiteral's reading of C^∞(ℝ³ × [0, ∞)) as the restriction of a C^∞
    function: Clay smoothness gives the formal `ContDiffOn` within the closed half-space.
    Note: this reading makes S4 immediate and moves the difficulty to D4. -/
theorem s4 {X : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X] (g : R3 → ℝ → X)
    (h : SmoothUpToBoundary g) :
    ContDiffOn ℝ ((⊤ : ℕ∞) : WithTop ℕ∞) (Function.uncurry g) (Set.univ ×ˢ Set.Ici 0) := by
  obtain ⟨G, hG, hEq⟩ := h
  exact hG.contDiffOn.congr fun p hp => (hEq p.1 p.2 hp.2).symm

/-- Row S6: Clay's (10) gives the formal periodic-velocity field. -/
theorem s6 (u : R3 → ℝ → R3) (h : Cond10 u) : ∀ t ≥ 0, IsOnePeriodic (u · t) :=
  fun t ht x j => (h x t j ht).symm

/-- Row S7, formal side: Clay's erratum condition gives the formal periodic-pressure field.
    Whether Clay's solutions must satisfy the erratum remains the open reading. -/
theorem s7_formal_side (p : R3 → ℝ → ℝ) (h : Erratum p) : ∀ t ≥ 0, IsOnePeriodic (p · t) :=
  fun t ht x j => h x t j ht

/-- Row P1: the formal theorems hold for every ν > 0, so in particular for Clay's given ν. -/
theorem p1 {P : ℝ → Prop} (h : ∀ nu : ℝ, nu > 0 → P nu) (ν : ℝ) (hν : 0 < ν) : P ν := h ν hν

/-- Row K1 for (C), conditional. From OpenAI's proved theorem to Clay's (C) as written in
    ClayLiteral, assuming the bridges not yet proved: D1, D2, D3, D4, D5 on the data side and
    S1, S2, S5 on the solution side. S3 and S4 are proved above. -/
theorem k1_C (ν : ℝ) (hν : 0 < ν)
    (bD1 : ∀ u0 : R3 → R3, InitialVelocityConditionDecay u0 → SmoothR3 u0)
    (bD2 : ∀ u0 : R3 → R3, InitialVelocityConditionDecay u0 → ∀ x, ClayLiteral.div u0 x = 0)
    (bD3 : ∀ u0 : R3 → R3, InitialVelocityConditionDecay u0 → Cond4 u0)
    (bD4 : ∀ f : R3 → ℝ → R3, ForceConditionDecay f → SmoothUpToBoundary f)
    (bD5 : ∀ f : R3 → ℝ → R3, ForceConditionDecay f → Cond5 f)
    (bS1 : ∀ (f u : R3 → ℝ → R3) (p : R3 → ℝ → ℝ), Eq1 ν f u p → SmoothUpToBoundary u →
      SmoothUpToBoundary p → ∀ x, ∀ t ≥ (0 : ℝ),
        derivWithin (u x ·) (Set.Ici 0) t + fderiv ℝ (u · t) x (u x t) =
          ν • Δ (u · t) x - gradient (p · t) x + f x t)
    (bS2 : ∀ u : R3 → ℝ → R3, Eq2 u → SmoothUpToBoundary u →
      ∀ x, ∀ t ≥ (0 : ℝ), divergence (u · t) x = 0)
    (bS5 : ∀ u : R3 → ℝ → R3, Cond7 u → SmoothUpToBoundary u →
      (∀ t ≥ (0 : ℝ), MeasureTheory.MemLp (‖u · t‖) 2) ∧
        ∃ E, ∀ t ≥ (0 : ℝ), (∫ x, ‖u x t‖ ^ 2) < E) :
    AltC ν := by
  obtain ⟨u0, f, hu, hf, hno⟩ := navier_stokes_breakdown_R3 ν hν
  refine ⟨u0, f, bD1 u0 hu, bD2 u0 hu, bD4 f hf, bD3 u0 hu, bD5 f hf, ?_⟩
  rintro ⟨p, u, h1, h2, h3, ⟨hu6, hp6⟩, h7⟩
  obtain ⟨hint, henergy⟩ := bS5 u h7 hu6
  exact hno ⟨u, p,
    { navier_stokes := bS1 f u p h1 hu6 hp6
      div_free := bS2 u h2 hu6
      initial_condition := s3 u0 u h3
      velocity_smooth := s4 u hu6
      pressure_smooth := s4 p hp6
      integrable := hint
      globally_bounded_energy := henergy }⟩

/-- Row K1 for (D), conditional, with the erratum read as a condition on solutions (S7).
    Assumes D1, D2, D4 for periodic data, D7, S1 and S2; uses the proved D6, S3, S4, S6 and
    the formal side of S7. -/
theorem k1_D (ν : ℝ) (hν : 0 < ν)
    (bD1 : ∀ u0 : R3 → R3, InitialVelocityConditionPeriodic u0 → SmoothR3 u0)
    (bD2 : ∀ u0 : R3 → R3, InitialVelocityConditionPeriodic u0 → ∀ x, ClayLiteral.div u0 x = 0)
    (bD4 : ∀ f : R3 → ℝ → R3, ForceConditionPeriodic f → SmoothUpToBoundary f)
    (bD7 : ∀ f : R3 → ℝ → R3, ForceConditionPeriodic f → Cond9 f)
    (bS1 : ∀ (f u : R3 → ℝ → R3) (p : R3 → ℝ → ℝ), Eq1 ν f u p → SmoothUpToBoundary u →
      SmoothUpToBoundary p → ∀ x, ∀ t ≥ (0 : ℝ),
        derivWithin (u x ·) (Set.Ici 0) t + fderiv ℝ (u · t) x (u x t) =
          ν • Δ (u · t) x - gradient (p · t) x + f x t)
    (bS2 : ∀ u : R3 → ℝ → R3, Eq2 u → SmoothUpToBoundary u →
      ∀ x, ∀ t ≥ (0 : ℝ), divergence (u · t) x = 0) :
    AltD_withErratum ν := by
  obtain ⟨u0, f, hu, hf, hno⟩ := navier_stokes_breakdown_periodic ν hν
  refine ⟨u0, f, bD1 u0 hu, bD2 u0 hu, bD4 f hf, d6 u0 f hu hf, bD7 f hf, ?_⟩
  rintro ⟨p, u, h1, h2, h3, h10, ⟨hu6, hp6⟩, hErr⟩
  exact hno ⟨u, p,
    { navier_stokes := bS1 f u p h1 hu6 hp6
      div_free := bS2 u h2 hu6
      initial_condition := s3 u0 u h3
      velocity_smooth := s4 u hu6
      pressure_smooth := s4 p hp6
      isOnePeriodic_velocity := s6 u h10
      isOnePeriodic_pressure := s7_formal_side p hErr }⟩

end Bridges
