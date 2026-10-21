/-
Bridge lemmas between OpenAI's formal challenge statement (ComparatorChallenges.NavierStokes,
identical in text to DeepMind's Formal Conjectures statement) and the literal rendering of
Clay's text in ClayLiteral.lean. Row IDs refer to evidence/formal/clay-lean-bridges.md.

Direction, as required by the risk review:
- data rows (D*): formal data condition ⇒ Clay data condition;
- solution rows (S*): Clay solution condition ⇒ formal solution condition.
-/
import Mathlib
import ComparatorChallenges.NavierStokes
import ClayLiteral

namespace Bridges

open ClayLiteral
open NavierStokes.Comparator

/-- Row D6: formal periodic data imply Clay's condition (8). -/
theorem d6 (u0 : R3 → R3) (f : R3 → ℝ → R3)
    (hu : InitialVelocityConditionPeriodic u0) (hf : ForceConditionPeriodic f) :
    Cond8 u0 f :=
  ⟨fun x j => hu.isOnePeriodic x j, fun x t j ht => hf.isOnePeriodic t ht x j⟩

/-- Row S3: Clay's initial condition (3) gives the formal `initial_condition` field. -/
theorem s3 (u0 : R3 → R3) (u : R3 → ℝ → R3) (h : Eq3 u0 u) : ∀ x, u x 0 = u0 x := h

/-- Row S6: Clay's (10) gives the formal periodic-velocity field. -/
theorem s6 (u : R3 → ℝ → R3) (h : Cond10 u) : ∀ t ≥ 0, IsOnePeriodic (u · t) :=
  fun t ht x j => (h x t j ht).symm

/-- Row S7 (formal side only): the formal periodic-pressure field is exactly Clay's erratum
    condition. Whether Clay's solutions must satisfy it remains the open reading. -/
theorem s7_formal_side (p : R3 → ℝ → ℝ) (h : Erratum p) : ∀ t ≥ 0, IsOnePeriodic (p · t) :=
  fun t ht x j => h x t j ht

/-- Row P1: the formal theorems hold for every ν > 0, so in particular for Clay's given ν. -/
theorem p1 {P : ℝ → Prop} (h : ∀ nu : ℝ, nu > 0 → P nu) (ν : ℝ) (hν : 0 < ν) : P ν := h ν hν

end Bridges
