import Mathlib

open scoped RealInnerProductSpace

namespace QAControls

theorem cauchy_schwarz {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F] (x y : F) :
    ⟪x, y⟫ ^ 2 ≤ ‖x‖ ^ 2 * ‖y‖ ^ 2 := by
  sorry

end QAControls
