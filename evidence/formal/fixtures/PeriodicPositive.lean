import ComparatorChallenges.NavierStokes

open ContDiff Set InnerProductSpace MeasureTheory
open scoped Laplacian
noncomputable section

namespace NavierStokes.Comparator

local notation "ℝ³" => EuclideanSpace ℝ (Fin 3)

def periodicControlData : ℝ³ := EuclideanSpace.single (0 : Fin 3) 1

def periodicControlInitial : ℝ³ → ℝ³ := fun _ => periodicControlData

def periodicControlForce : ℝ³ → ℝ → ℝ³ := fun _ _ => 0

def periodicControlVelocity : ℝ³ → ℝ → ℝ³ := fun _ _ => periodicControlData

def periodicControlPressure : ℝ³ → ℝ → ℝ := fun _ _ => 0

theorem periodicControlData_nonzero : periodicControlData ≠ 0 := by
  intro h
  have h0 := congrArg (fun x : ℝ³ => x (0 : Fin 3)) h
  simp [periodicControlData] at h0

theorem periodicControlInitial_condition :
    InitialVelocityConditionPeriodic periodicControlInitial := by
  constructor
  · constructor
    · intro x
      change divergence (fun _ : ℝ³ => periodicControlData) x = 0
      exact divergence_const periodicControlData x
    · change ContDiff ℝ ∞ (fun _ : ℝ³ => periodicControlData)
      exact contDiff_const
  · intro x i
    simp [IsOnePeriodic, periodicControlInitial]

theorem periodicControlForce_condition :
    ForceConditionPeriodic periodicControlForce := by
  constructor
  · constructor
    · change ContDiffOn ℝ ∞ (fun _ : ℝ³ × ℝ => (0 : ℝ³))
        (Set.univ ×ˢ Set.Ici (0 : ℝ))
      exact contDiffOn_const
  · intro t ht x i
    simp [IsOnePeriodic, periodicControlForce]
  · intro m K
    refine ⟨0, ?_⟩
    intro x t ht
    change ‖iteratedFDerivWithin ℝ m (fun _ : ℝ³ × ℝ => (0 : ℝ³))
      (Set.univ ×ˢ Set.Ici (0 : ℝ)) (x, t)‖ ≤ 0 / (1 + t) ^ K
    simp

theorem periodicControl_solution :
    NavierStokesExistenceAndSmoothnessPeriodic 1 periodicControlInitial
      periodicControlForce periodicControlVelocity periodicControlPressure := by
  constructor
  · constructor
    · intro x t ht
      simp [periodicControlVelocity, periodicControlForce, periodicControlPressure]
    · intro x t ht
      change divergence (fun _ : ℝ³ => periodicControlData) x = 0
      exact divergence_const periodicControlData x
    · intro x
      rfl
    · change ContDiffOn ℝ ∞ (fun _ : ℝ³ × ℝ => periodicControlData)
        (Set.univ ×ˢ Set.Ici (0 : ℝ))
      exact contDiffOn_const
    · change ContDiffOn ℝ ∞ (fun _ : ℝ³ × ℝ => (0 : ℝ))
        (Set.univ ×ˢ Set.Ici (0 : ℝ))
      exact contDiffOn_const
  · intro t ht x i
    simp [IsOnePeriodic, periodicControlVelocity]
  · intro t ht x i
    simp [IsOnePeriodic, periodicControlPressure]

theorem periodic_nonzero_control :
    periodicControlData ≠ 0 ∧
      InitialVelocityConditionPeriodic periodicControlInitial ∧
      ForceConditionPeriodic periodicControlForce ∧
      NavierStokesExistenceAndSmoothnessPeriodic 1 periodicControlInitial
        periodicControlForce periodicControlVelocity periodicControlPressure := by
  exact ⟨periodicControlData_nonzero, periodicControlInitial_condition,
    periodicControlForce_condition, periodicControl_solution⟩

#print axioms periodic_nonzero_control

end NavierStokes.Comparator
