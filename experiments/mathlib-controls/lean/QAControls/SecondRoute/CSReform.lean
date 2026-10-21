import Mathlib
import QAControls.Guard

open scoped RealInnerProductSpace

namespace QAControls.SecondRoute

theorem abs_le_mul_iff_sq (a b c : ℝ) (hb : 0 ≤ b) (hc : 0 ≤ c) :
    |a| ≤ b * c ↔ a ^ 2 ≤ b ^ 2 * c ^ 2 := by
  rw [← mul_pow, ← sq_abs a]
  exact (sq_le_sq₀ (abs_nonneg a) (mul_nonneg hb hc)).symm

theorem cs_reform_equiv :
    (∀ (F : Type) [NormedAddCommGroup F] [InnerProductSpace ℝ F] (x y : F),
      |⟪x, y⟫| ≤ ‖x‖ * ‖y‖) ↔
    (∀ (F : Type) [NormedAddCommGroup F] [InnerProductSpace ℝ F] (x y : F),
      ⟪x, y⟫ ^ 2 ≤ ‖x‖ ^ 2 * ‖y‖ ^ 2) :=
  ⟨fun h F _ _ x y => (abs_le_mul_iff_sq _ _ _ (norm_nonneg x) (norm_nonneg y)).1 (h F x y),
   fun h F _ _ x y => (abs_le_mul_iff_sq _ _ _ (norm_nonneg x) (norm_nonneg y)).2 (h F x y)⟩

#guard_independent cs_reform_equiv of abs_real_inner_le_norm real_inner_le_norm norm_inner_le_norm real_inner_mul_inner_self_le

end QAControls.SecondRoute
