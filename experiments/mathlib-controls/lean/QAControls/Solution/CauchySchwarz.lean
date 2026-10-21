import Mathlib

open scoped RealInnerProductSpace

namespace QAControls

theorem cauchy_schwarz {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F] (x y : F) :
    |⟪x, y⟫| ≤ ‖x‖ * ‖y‖ :=
  abs_real_inner_le_norm x y

end QAControls
