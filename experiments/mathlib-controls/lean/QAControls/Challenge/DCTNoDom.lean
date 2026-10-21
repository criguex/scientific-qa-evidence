import Mathlib

open MeasureTheory Filter Topology

namespace QAControls

theorem dominated_convergence {α : Type*} [MeasurableSpace α] {μ : Measure α}
    (F : ℕ → α → ℝ) (f : α → ℝ)
    (hF : ∀ n, AEStronglyMeasurable (F n) μ)
    (hlim : ∀ᵐ a ∂μ, Tendsto (fun n => F n a) atTop (𝓝 (f a))) :
    Tendsto (fun n => ∫ a, F n a ∂μ) atTop (𝓝 (∫ a, f a ∂μ)) := by
  sorry

end QAControls
