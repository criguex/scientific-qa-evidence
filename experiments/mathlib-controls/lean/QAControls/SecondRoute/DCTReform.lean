import Mathlib
import QAControls.Guard

open MeasureTheory Filter Topology

namespace QAControls.SecondRoute

theorem integrable_iff_of_dominates {α : Type} [MeasurableSpace α] {μ : Measure α}
    {F : ℕ → α → ℝ} {bound : α → ℝ} (hle : ∀ n, ∀ᵐ a ∂μ, ‖F n a‖ ≤ bound a) :
    Integrable bound μ ↔
      AEStronglyMeasurable bound μ ∧ ∫⁻ a, ENNReal.ofReal (bound a) ∂μ < ⊤ := by
  have h0 : 0 ≤ᵐ[μ] bound := (hle 0).mono fun a ha => (norm_nonneg _).trans ha
  exact ⟨fun h => ⟨h.1, (hasFiniteIntegral_iff_ofReal h0).1 h.2⟩,
    fun h => ⟨h.1, (hasFiniteIntegral_iff_ofReal h0).2 h.2⟩⟩

theorem dct_reform_equiv :
    (∀ (α : Type) [MeasurableSpace α] (μ : Measure α) (F : ℕ → α → ℝ) (f : α → ℝ)
      (bound : α → ℝ), (∀ n, AEStronglyMeasurable (F n) μ) → Integrable bound μ →
      (∀ n, ∀ᵐ a ∂μ, ‖F n a‖ ≤ bound a) →
      (∀ᵐ a ∂μ, Tendsto (fun n => F n a) atTop (𝓝 (f a))) →
      Tendsto (fun n => ∫ a, F n a ∂μ) atTop (𝓝 (∫ a, f a ∂μ))) ↔
    (∀ (α : Type) [MeasurableSpace α] (μ : Measure α) (F : ℕ → α → ℝ) (f : α → ℝ)
      (bound : α → ℝ), (∀ n, AEStronglyMeasurable (F n) μ) →
      (AEStronglyMeasurable bound μ ∧ ∫⁻ a, ENNReal.ofReal (bound a) ∂μ < ⊤) →
      (∀ n, ∀ᵐ a ∂μ, ‖F n a‖ ≤ bound a) →
      (∀ᵐ a ∂μ, Tendsto (fun n => F n a) atTop (𝓝 (f a))) →
      Tendsto (fun n => ∫ a, F n a ∂μ) atTop (𝓝 (∫ a, f a ∂μ))) :=
  ⟨fun h α _ μ F f bound hF hb hle hlim =>
      h α μ F f bound hF ((integrable_iff_of_dominates hle).2 hb) hle hlim,
   fun h α _ μ F f bound hF hb hle hlim =>
      h α μ F f bound hF ((integrable_iff_of_dominates hle).1 hb) hle hlim⟩

theorem isolated_condition_not_integrable :
    ¬ ∀ g : ℝ → ℝ, AEStronglyMeasurable g volume →
      ∫⁻ a, ENNReal.ofReal (g a) < ⊤ → Integrable g volume := by
  intro h
  have hi := h (fun _ => -1) aestronglyMeasurable_const
    (by simp [ENNReal.ofReal_of_nonpos (by norm_num : (-1 : ℝ) ≤ 0)])
  rcases integrable_const_iff.1 hi with h1 | h1
  · norm_num at h1
  · have h2 : (volume : Measure ℝ) Set.univ < ⊤ := by
      first
      | exact h1
      | exact @measure_lt_top _ _ _ h1 _
    simp [Real.volume_univ] at h2

#guard_independent dct_reform_equiv of tendsto_integral_of_dominated_convergence tendsto_integral_filter_of_dominated_convergence

end QAControls.SecondRoute
