import Mathlib
import QAControls.Guard

open scoped RealInnerProductSpace

namespace QAControls.SecondRoute

theorem cs_strict_false :
    ¬ ∀ (F : Type) [NormedAddCommGroup F] [InnerProductSpace ℝ F] (x y : F),
      |⟪x, y⟫| < ‖x‖ * ‖y‖ := by
  intro h
  have h1 := h ℝ 1 1
  rw [real_inner_self_eq_norm_mul_norm,
    abs_of_nonneg (mul_nonneg (norm_nonneg _) (norm_nonneg _))] at h1
  exact lt_irrefl _ h1

end QAControls.SecondRoute
