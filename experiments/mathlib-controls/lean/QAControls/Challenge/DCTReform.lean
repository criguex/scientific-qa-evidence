import Mathlib

open MeasureTheory Filter Topology

namespace QAControls

theorem dominated_convergence {α : Type*} [MeasurableSpace α] {μ : Measure α}
    (F : ℕ → α → ℝ) (f : α → ℝ)
    (bound : α → ℝ) (hF : ∀ n, AEStronglyMeasurable (F n) μ) (hb : AEStronglyMeasurable bound μ ∧ ∫⁻ a, ENNReal.ofReal (bound a) ∂μ < ⊤)
    (hle : ∀ n, ∀ᵐ a ∂μ, ‖F n a‖ ≤ bound a)
    (hlim : ∀ᵐ a ∂μ, Tendsto (fun n => F n a) atTop (𝓝 (f a))) :
    Tendsto (fun n => ∫ a, F n a ∂μ) atTop (𝓝 (∫ a, f a ∂μ)) := by
  sorry

end QAControls
