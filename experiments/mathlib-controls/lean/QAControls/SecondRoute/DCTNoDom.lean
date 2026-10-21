import Mathlib
import QAControls.Guard

open MeasureTheory Filter Topology

namespace QAControls.SecondRoute

noncomputable def bump (n : ℕ) : ℝ → ℝ :=
  Set.indicator (Set.Ioo 0 (1 / ((n : ℝ) + 1))) fun _ => (n : ℝ) + 1

theorem bump_tendsto_zero (a : ℝ) : Tendsto (fun n => bump n a) atTop (𝓝 0) := by
  rcases le_or_gt a 0 with ha | ha
  · have h0 : ∀ n, bump n a = 0 := fun n =>
      Set.indicator_of_notMem (fun hm => absurd hm.1 (not_lt.2 ha)) _
    simp only [h0]
    exact tendsto_const_nhds
  · obtain ⟨N, hN⟩ := exists_nat_one_div_lt ha
    refine tendsto_atTop_of_eventually_const (i₀ := N) fun n hn => ?_
    apply Set.indicator_of_notMem
    intro hm
    have hNn : (N : ℝ) ≤ n := by exact_mod_cast hn
    have h1 : 1 / ((n : ℝ) + 1) ≤ 1 / ((N : ℝ) + 1) :=
      one_div_le_one_div_of_le (by positivity) (by linarith)
    linarith [hm.2]

theorem bump_integral (n : ℕ) : ∫ a, bump n a = 1 := by
  unfold bump
  rw [integral_indicator_const _ measurableSet_Ioo]
  simp only [Measure.real, Real.volume_Ioo, sub_zero, smul_eq_mul]
  rw [ENNReal.toReal_ofReal (by positivity)]
  field_simp

theorem dct_nodom_false :
    ¬ ∀ (F : ℕ → ℝ → ℝ) (f : ℝ → ℝ), (∀ n, AEStronglyMeasurable (F n) volume) →
      (∀ᵐ a ∂volume, Tendsto (fun n => F n a) atTop (𝓝 (f a))) →
      Tendsto (fun n => ∫ a, F n a) atTop (𝓝 (∫ a, f a)) := by
  intro h
  have hm : ∀ n, AEStronglyMeasurable (bump n) volume := fun n =>
    (measurable_const.indicator measurableSet_Ioo).aestronglyMeasurable
  have ht := h bump 0 hm (ae_of_all _ bump_tendsto_zero)
  simp only [bump_integral, Pi.zero_apply, integral_zero] at ht
  exact one_ne_zero (tendsto_const_nhds_iff.mp ht)

end QAControls.SecondRoute
