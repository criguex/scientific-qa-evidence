/-
Bridge lemmas between OpenAI's formal statement and the literal rendering of Clay's text
in ClayLiteral.lean. Row IDs refer to evidence/formal/clay-lean-bridges.md.

The import is OpenAI's solution module, so `navier_stokes_breakdown_R3` and
`navier_stokes_breakdown_periodic` below are OpenAI's proved theorems, not the challenge
placeholders. Its definitions come from NavierStokes.ComparatorDefinitions, which Comparator
checked against the challenge statement.

Direction, as required by the risk review:
- data rows (D*): formal data condition ⇒ Clay data condition;
- solution rows (S*): Clay solution condition ⇒ formal solution condition.

K1 composes the rows. It is relative to ClayLiteral's stated readings (READING markers there).
-/
import Mathlib
import NavierStokes.ComparatorSolution
import ClayLiteral

namespace Bridges

open ClayLiteral
open NavierStokes.Comparator
open scoped Laplacian ContDiff

/-- Row D6: formal periodic data imply Clay's condition (8). -/
theorem d6 (u0 : R3 → R3) (f : R3 → ℝ → R3)
    (hu : InitialVelocityConditionPeriodic u0) (hf : ForceConditionPeriodic f) :
    Cond8 u0 f :=
  ⟨fun x j => hu.isOnePeriodic x j, fun x t j ht => hf.isOnePeriodic t ht x j⟩

/-- Row S3: Clay's initial condition (3) gives the formal `initial_condition` field. -/
theorem s3 (u0 : R3 → R3) (u : R3 → ℝ → R3) (h : Eq3 u0 u) : ∀ x, u x 0 = u0 x := h

/-- Row S4, under ClayLiteral's reading of C^∞(ℝ³ × [0, ∞)) as the restriction of a C^∞
    function: Clay smoothness gives the formal `ContDiffOn` within the closed half-space.
    Note: this reading makes S4 immediate and moves the difficulty to D4. -/
theorem s4 {X : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X] (g : R3 → ℝ → X)
    (h : SmoothUpToBoundary g) :
    ContDiffOn ℝ ((⊤ : ℕ∞) : WithTop ℕ∞) (Function.uncurry g) (Set.univ ×ˢ Set.Ici 0) := by
  obtain ⟨G, hG, hEq⟩ := h
  exact hG.contDiffOn.congr fun p hp => (hEq p.1 p.2 hp.2).symm

/-- Row S6: Clay's (10) gives the formal periodic-velocity field. -/
theorem s6 (u : R3 → ℝ → R3) (h : Cond10 u) : ∀ t ≥ 0, IsOnePeriodic (u · t) :=
  fun t ht x j => (h x t j ht).symm

/-- Row S7, formal side: Clay's erratum condition gives the formal periodic-pressure field.
    Whether Clay's solutions must satisfy the erratum remains the open reading. -/
theorem s7_formal_side (p : R3 → ℝ → ℝ) (h : Erratum p) : ∀ t ≥ 0, IsOnePeriodic (p · t) :=
  fun t ht x j => h x t j ht

/-- Row P1: the formal theorems hold for every ν > 0, so in particular for Clay's given ν. -/
theorem p1 {P : ℝ → Prop} (h : ∀ nu : ℝ, nu > 0 → P nu) (ν : ℝ) (hν : 0 < ν) : P ν := h ν hν

/-- The zero initial datum used by OpenAI satisfies Clay's data conditions: rows D1, D2, D3
    for u₀ = 0. -/
theorem dx_zero : ∀ α : List (Fin 3), dx α (fun _ : R3 => (0 : R3)) = fun _ => 0
  | [] => rfl
  | j :: js => by funext x; simp [dx, dx_zero js]

theorem d1_zero : SmoothR3 (fun _ : R3 => (0 : R3)) := contDiff_const

theorem d2_zero : ∀ x, ClayLiteral.div (fun _ : R3 => (0 : R3)) x = 0 := by
  intro x; simp [ClayLiteral.div]

theorem d3_zero : Cond4 (fun _ : R3 => (0 : R3)) :=
  fun α _ => ⟨0, fun x => by simp [dx_zero]⟩

/-- Row D4 for OpenAI's force in (C): OpenAI's theorem, with its concrete witness exposed.
    The force is `Φ(x, t)` for a `Φ` that is `ContDiff ℝ ∞` on all of ℝ³ × ℝ, so it is its
    own smooth extension. -/
theorem witness_C (ν : ℝ) (hν : 0 < ν) :
    ∃ Φ : R3 × ℝ → R3, ContDiff ℝ ∞ Φ ∧ ForceConditionDecay (fun x t => Φ (x, t)) ∧
      ¬ ∃ v p, NavierStokesExistenceAndSmoothnessRn ν (fun _ => 0) (fun x t => Φ (x, t)) v p := by
  obtain ⟨u, p, f, K, h, hglobal⟩ := NavierStokesR3.theorem_1_1 ν hν
  refine ⟨fun z => f (z.2, z.1), h.force_smooth.comp (contDiff_snd.prodMk contDiff_fst),
    NavierStokesR3.forceConditionDecay_of_compact h.force_smooth h.force_support.1, ?_⟩
  rintro ⟨v, q, hv⟩
  exact hglobal ⟨NavierStokesR3.globalSolutionOfComparator (f := f) hv⟩

/-- Row D4 for OpenAI's force in (D), as for (C). -/
theorem witness_D (ν : ℝ) (hν : 0 < ν) :
    ∃ Φ : R3 × ℝ → R3, ContDiff ℝ ∞ Φ ∧
      InitialVelocityConditionPeriodic (fun _ : R3 => (0 : R3)) ∧
      ForceConditionPeriodic (fun x t => Φ (x, t)) ∧
      ¬ ∃ v p, NavierStokesExistenceAndSmoothnessPeriodic ν (fun _ => 0)
        (fun x t => Φ (x, t)) v p := by
  obtain ⟨u, p, f, K, h, hno⟩ := NavierStokes.PeriodicPaper.periodic_corollary ν hν
  obtain ⟨hu, hf, hn⟩ :=
    NavierStokes.ComparatorBridge.option_D_same_force_of_paper_candidate h hno
  exact ⟨fun z => f (z.2, z.1), h.force_smooth.comp (contDiff_snd.prodMk contDiff_fst),
    hu, hf, hn⟩

/-! ### Rows D5 and D7: Clay's partial derivatives are bounded by the formal iterated derivative -/

/-- Nested directional derivatives `D_{v₁} ⋯ D_{vₖ} Φ`. -/
noncomputable def dirDeriv : List (R3 × ℝ) → (R3 × ℝ → R3) → (R3 × ℝ → R3)
  | [], g => g
  | v :: vs, g => fun z => fderiv ℝ (dirDeriv vs g) z v

theorem dirDeriv_smooth {Φ : R3 × ℝ → R3} (hΦ : ContDiff ℝ ∞ Φ) :
    ∀ vs, ContDiff ℝ ∞ (dirDeriv vs Φ)
  | [] => hΦ
  | _ :: vs => (contDiff_infty_iff_fderiv.mp (dirDeriv_smooth hΦ vs)).2.clm_apply contDiff_const

theorem dirDeriv_eq {Φ : R3 × ℝ → R3} (hΦ : ContDiff ℝ ∞ Φ) :
    ∀ (vs : List (R3 × ℝ)) (z : R3 × ℝ),
      dirDeriv vs Φ z = iteratedFDeriv ℝ vs.length Φ z vs.get
  | [], z => by simp [dirDeriv]
  | v :: vs, z => by
    have hd : Differentiable ℝ fun y => iteratedFDeriv ℝ vs.length Φ y :=
      hΦ.differentiable_iteratedFDeriv (by exact_mod_cast ENat.natCast_lt_top _)
    have hc : (v :: vs).get = Fin.cons v vs.get := by
      funext i; exact Fin.cases rfl (fun j => rfl) i
    show fderiv ℝ (dirDeriv vs Φ) z v = iteratedFDeriv ℝ (vs.length + 1) Φ z (v :: vs).get
    rw [show dirDeriv vs Φ = fun y => iteratedFDeriv ℝ vs.length Φ y vs.get from
      funext (dirDeriv_eq hΦ vs), fderiv_continuousMultilinear_apply_const_apply (hd z), hc,
      iteratedFDeriv_succ_apply_left]
    simp only [Fin.cons_zero, Fin.tail_cons]

theorem dt_eq {Φ : R3 × ℝ → R3} (hΦ : ContDiff ℝ ∞ Φ) :
    ∀ (m : ℕ) (x : R3) (t : ℝ), 0 ≤ t →
      dt m (fun x t => Φ (x, t)) x t = dirDeriv (List.replicate m ((0 : R3), (1 : ℝ))) Φ (x, t)
  | 0, _, _, _ => rfl
  | m + 1, x, t, ht => by
    have hd : HasDerivAt (fun s => dirDeriv (List.replicate m ((0 : R3), (1 : ℝ))) Φ (x, s))
        (fderiv ℝ (dirDeriv (List.replicate m ((0 : R3), (1 : ℝ))) Φ) (x, t)
          ((0 : R3), (1 : ℝ))) t :=
      ((contDiff_infty_iff_fderiv.mp (dirDeriv_smooth hΦ _)).1 (x, t)).hasFDerivAt.comp_hasDerivAt
        t ((hasDerivAt_const t x).prodMk (hasDerivAt_id t))
    show derivWithin (fun s => dt m (fun x t => Φ (x, t)) x s) (Set.Ici 0) t = _
    refine (derivWithin_congr (s := Set.Ici 0)
      (f := fun s => dirDeriv (List.replicate m ((0 : R3), (1 : ℝ))) Φ (x, s))
      (fun s hs => dt_eq hΦ m x s hs) (dt_eq hΦ m x t ht)).trans ?_
    exact hd.hasDerivWithinAt.derivWithin (uniqueDiffOn_Ici 0 t ht)

theorem dxt_eq {Φ : R3 × ℝ → R3} (hΦ : ContDiff ℝ ∞ Φ) (g : R3 → ℝ → R3)
    (L : List (R3 × ℝ)) (hg : ∀ x t, 0 ≤ t → g x t = dirDeriv L Φ (x, t)) :
    ∀ (α : List (Fin 3)) (x : R3) (t : ℝ), 0 ≤ t →
      dxt α g x t = dirDeriv (α.map (fun j => (e j, (0 : ℝ))) ++ L) Φ (x, t)
  | [], x, t, ht => hg x t ht
  | j :: js, x, t, ht => by
    have hfun : (fun y => dxt js g y t) =
        fun y => dirDeriv (js.map (fun j => (e j, (0 : ℝ))) ++ L) Φ (y, t) :=
      funext fun y => dxt_eq hΦ g L hg js y t ht
    have hd : HasFDerivAt (fun y => dirDeriv (js.map (fun j => (e j, (0 : ℝ))) ++ L) Φ (y, t))
        ((fderiv ℝ (dirDeriv (js.map (fun j => (e j, (0 : ℝ))) ++ L) Φ) (x, t)).comp
          (ContinuousLinearMap.inl ℝ R3 ℝ)) x :=
      ((contDiff_infty_iff_fderiv.mp (dirDeriv_smooth hΦ _)).1 (x, t)).hasFDerivAt.comp x
        (hasFDerivAt_prodMk_left x t)
    show fderiv ℝ (fun y => dxt js g y t) x (e j) = _
    rw [hfun, hd.fderiv]
    rfl

theorem dirs_norm (α : List (Fin 3)) (m : ℕ) :
    ∀ v ∈ α.map (fun j => (e j, (0 : ℝ))) ++ List.replicate m ((0 : R3), (1 : ℝ)), ‖v‖ ≤ 1 := by
  intro v hv
  simp only [List.mem_append, List.mem_map, List.mem_replicate] at hv
  rcases hv with ⟨j, -, rfl⟩ | ⟨-, rfl⟩
  · simp [e]
  · simp

/-- Every mixed partial of Clay's (5) and (9) is bounded by the norm of the formal iterated
    derivative of the same order, because it is that multilinear map applied to unit vectors. -/
theorem clay_bound {Φ : R3 × ℝ → R3} (hΦ : ContDiff ℝ ∞ Φ) (α : List (Fin 3)) (m : ℕ)
    (x : R3) (t : ℝ) (ht : 0 ≤ t) :
    ‖dxt α (dt m (fun x t => Φ (x, t))) x t‖ ≤
      ‖iteratedFDerivWithin ℝ
        (α.map (fun j => (e j, (0 : ℝ))) ++ List.replicate m ((0 : R3), (1 : ℝ))).length
        Φ (Set.univ ×ˢ Set.Ici 0) (x, t)‖ := by
  rw [dxt_eq hΦ _ _ (dt_eq hΦ m) α x t ht, dirDeriv_eq hΦ,
    iteratedFDerivWithin_eq_iteratedFDeriv (uniqueDiffOn_univ.prod (uniqueDiffOn_Ici 0))
      (hΦ.of_le (WithTop.coe_le_coe.mpr le_top)).contDiffAt
      (show (x, t) ∈ Set.univ ×ˢ Set.Ici (0 : ℝ) from ⟨Set.mem_univ _, ht⟩)]
  exact ((iteratedFDeriv ℝ _ Φ (x, t)).le_opNorm _).trans
    (mul_le_of_le_one_right (norm_nonneg _) (Finset.prod_le_one (fun i _ => norm_nonneg _)
      (fun i _ => dirs_norm α m _ (List.get_mem _ _))))

/-- Row D5 for a globally smooth force. -/
theorem d5 {Φ : R3 × ℝ → R3} (hΦ : ContDiff ℝ ∞ Φ)
    (hF : ForceConditionDecay (fun x t => Φ (x, t))) : Cond5 (fun x t => Φ (x, t)) := by
  intro α m K
  obtain ⟨C, hC⟩ := hF.decay
    (α.map (fun j => (e j, (0 : ℝ))) ++ List.replicate m ((0 : R3), (1 : ℝ))).length K
  refine ⟨C, fun x t ht => (clay_bound hΦ α m x t ht).trans ?_⟩
  rw [Real.rpow_neg (by positivity), ← div_eq_mul_inv]
  exact hC x t ht

/-- Row D7 for a globally smooth force. -/
theorem d7 {Φ : R3 × ℝ → R3} (hΦ : ContDiff ℝ ∞ Φ)
    (hF : ForceConditionPeriodic (fun x t => Φ (x, t))) : Cond9 (fun x t => Φ (x, t)) := by
  intro α m K
  obtain ⟨C, hC⟩ := hF.decay
    (α.map (fun j => (e j, (0 : ℝ))) ++ List.replicate m ((0 : R3), (1 : ℝ))).length K
  refine ⟨C, fun x t ht => (clay_bound hΦ α m x t ht).trans ?_⟩
  rw [abs_of_nonneg ht, Real.rpow_neg (by positivity), ← div_eq_mul_inv]
  exact hC x t ht

/-! ### Rows S1, S2, S5: a Clay solution is a formal solution -/

/-- The i-th coordinate, as a continuous linear map. -/
noncomputable abbrev cmp (i : Fin 3) : R3 →L[ℝ] ℝ := EuclideanSpace.proj i

theorem fderiv_cmp {v : R3 → R3} {x : R3} (hv : DifferentiableAt ℝ v x) (i : Fin 3) (w : R3) :
    fderiv ℝ (fun y => v y i) x w = fderiv ℝ v x w i :=
  congrArg (fun L : R3 →L[ℝ] ℝ => L w) ((cmp i).hasFDerivAt.comp x hv.hasFDerivAt).fderiv

theorem slice_smooth {X : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X] {g : R3 → ℝ → X}
    (hU : ContDiffOn ℝ ∞ (↿g) (Set.univ ×ˢ Set.Ici 0)) {t : ℝ} (ht : 0 ≤ t) :
    ContDiff ℝ ∞ (g · t) :=
  hU.comp_contDiff (contDiff_id.prodMk contDiff_const) fun _ => ⟨Set.mem_univ _, ht⟩

theorem clm_expand (L : R3 →L[ℝ] ℝ) (w : R3) : L w = ∑ j, w j * L (e j) := by
  conv_lhs => rw [← (EuclideanSpace.basisFun (Fin 3) ℝ).sum_repr w]
  simp [map_sum, EuclideanSpace.basisFun_apply, e]

theorem gradient_cmp (q : R3 → ℝ) (x : R3) (i : Fin 3) :
    cmp i (gradient q x) = fderiv ℝ q x (e i) := by
  have h := EuclideanSpace.inner_single_left i (1 : ℝ) (gradient q x)
  rw [inner_gradient_right] at h
  simpa [e] using h.symm

theorem time_cmp {u : R3 → ℝ → R3} (hU : ContDiffOn ℝ ∞ (↿u) (Set.univ ×ˢ Set.Ici 0))
    (x : R3) {t : ℝ} (ht : 0 ≤ t) (i : Fin 3) :
    cmp i (derivWithin (u x ·) (Set.Ici 0) t) = derivWithin (fun s => u x s i) (Set.Ici 0) t := by
  have hdiff : DifferentiableWithinAt ℝ (↿u) (Set.univ ×ˢ Set.Ici 0) (x, t) :=
    hU.differentiableOn (by simp) (x, t) ⟨Set.mem_univ _, ht⟩
  have hd : HasDerivWithinAt (fun s => u x s)
      (fderivWithin ℝ (↿u) (Set.univ ×ˢ Set.Ici 0) (x, t) ((0 : R3), (1 : ℝ))) (Set.Ici 0) t :=
    hdiff.hasFDerivWithinAt.comp_hasDerivWithinAt t
      ((hasDerivWithinAt_const t (Set.Ici 0) x).prodMk (hasDerivWithinAt_id t (Set.Ici 0)))
      fun s hs => ⟨Set.mem_univ _, hs⟩
  have h1 : derivWithin (u x ·) (Set.Ici 0) t =
      fderivWithin ℝ (↿u) (Set.univ ×ˢ Set.Ici 0) (x, t) ((0 : R3), (1 : ℝ)) :=
    hd.derivWithin (uniqueDiffOn_Ici 0 t ht)
  have h2 : derivWithin (fun s => u x s i) (Set.Ici 0) t =
      cmp i (fderivWithin ℝ (↿u) (Set.univ ×ˢ Set.Ici 0) (x, t) ((0 : R3), (1 : ℝ))) :=
    ((cmp i).hasFDerivAt.comp_hasDerivWithinAt t hd).derivWithin (uniqueDiffOn_Ici 0 t ht)
  rw [h1, h2]

/-- Row S1: Clay's equation (1), componentwise, gives the formal vector equation. -/
theorem s1 (ν : ℝ) (f u : R3 → ℝ → R3) (p : R3 → ℝ → ℝ) (h : Eq1 ν f u p)
    (hu : ContDiffOn ℝ ∞ (↿u) (Set.univ ×ˢ Set.Ici 0)) :
    ∀ x, ∀ t ≥ (0 : ℝ), derivWithin (u x ·) (Set.Ici 0) t + fderiv ℝ (u · t) x (u x t) =
      ν • Δ (u · t) x - gradient (p · t) x + f x t := by
  intro x t ht
  have hvs := slice_smooth hu ht
  have hv := (contDiff_infty_iff_fderiv.mp hvs).1
  have hdk : ∀ k, Differentiable ℝ (fun y => fderiv ℝ (u · t) y (e k)) := fun k =>
    (contDiff_infty_iff_fderiv.mp
      ((contDiff_infty_iff_fderiv.mp hvs).2.clm_apply contDiff_const)).1
  have hL : Δ (u · t) x = ∑ k, fderiv ℝ (fun y => fderiv ℝ (u · t) y (e k)) x (e k) :=
    (NavierStokes.ComparatorBridge.laplacian_eq (NavierStokes.ComparatorBridge.fromComparator u)
      t x (hvs.of_le (WithTop.coe_le_coe.mpr le_top))).symm
  apply PiLp.ext
  intro i
  have hC : cmp i (fderiv ℝ (u · t) x (u x t)) =
      ∑ j, u x t j * fderiv ℝ (fun y => u y t i) x (e j) := by
    rw [← clm_expand]
    exact (fderiv_cmp (hv x) i (u x t)).symm
  have hLk : ∀ k, cmp i (fderiv ℝ (fun y => fderiv ℝ (u · t) y (e k)) x (e k)) =
      fderiv ℝ (fun y => fderiv ℝ (fun z => u z t i) y (e k)) x (e k) := by
    intro k
    rw [show (fun y => fderiv ℝ (fun z => u z t i) y (e k)) =
        fun y => fderiv ℝ (u · t) y (e k) i from funext fun y => fderiv_cmp (hv y) i (e k)]
    exact (fderiv_cmp (hdk k x) i (e k)).symm
  show cmp i (derivWithin (u x ·) (Set.Ici 0) t + fderiv ℝ (u · t) x (u x t)) =
    cmp i (ν • Δ (u · t) x - gradient (p · t) x + f x t)
  rw [map_add, map_add, map_sub, map_smul, hL, map_sum, time_cmp hu x ht i, hC,
    gradient_cmp, smul_eq_mul]
  simp only [hLk]
  exact h x t ht i

/-- Row S2: Clay's (2) gives the formal divergence-free field. -/
theorem s2 (u : R3 → ℝ → R3) (h : Eq2 u) (hu : ContDiffOn ℝ ∞ (↿u) (Set.univ ×ˢ Set.Ici 0)) :
    ∀ x, ∀ t ≥ (0 : ℝ), divergence (u · t) x = 0 := by
  intro x t ht
  have hv := (contDiff_infty_iff_fderiv.mp (slice_smooth hu ht)).1
  have hd : divergence (u · t) x = ∑ i, fderiv ℝ (u · t) x (e i) i :=
    (NavierStokes.ComparatorBridge.divergence_eq
      (NavierStokes.ComparatorBridge.fromComparator u) t x).symm
  rw [hd]
  refine Eq.trans ?_ (h x t ht)
  exact Finset.sum_congr rfl fun i _ => (fderiv_cmp (hv x) i (e i)).symm

/-- Row S5: Clay's (7), a finite Lebesgue integral, gives the formal `MemLp` and energy bound. -/
theorem s5 (u : R3 → ℝ → R3) (h7 : Cond7 u) (hu : ContDiffOn ℝ ∞ (↿u) (Set.univ ×ˢ Set.Ici 0)) :
    (∀ t ≥ (0 : ℝ), MeasureTheory.MemLp (‖u · t‖) 2) ∧
      ∃ E, ∀ t ≥ (0 : ℝ), (∫ x, ‖u x t‖ ^ 2) < E := by
  obtain ⟨C, hC⟩ := h7
  have h0 : ∀ t : ℝ, 0 ≤ᵐ[MeasureTheory.volume] fun x => ‖u x t‖ ^ 2 := fun t =>
    MeasureTheory.ae_of_all _ fun x => by simp only [Pi.zero_apply]; positivity
  have hm : ∀ t ≥ (0 : ℝ), MeasureTheory.AEStronglyMeasurable (fun x => ‖u x t‖ ^ 2) :=
    fun t ht => ((slice_smooth hu ht).continuous.norm.pow 2).aestronglyMeasurable
  have hint : ∀ t ≥ (0 : ℝ), MeasureTheory.Integrable (fun x => ‖u x t‖ ^ 2) := fun t ht =>
    ⟨hm t ht, (MeasureTheory.hasFiniteIntegral_iff_ofReal (h0 t)).mpr
      ((hC t ht).trans ENNReal.ofReal_lt_top)⟩
  refine ⟨fun t ht => ?_, C, fun t ht => ?_⟩
  · exact (MeasureTheory.memLp_two_iff_integrable_sq_norm
      (slice_smooth hu ht).continuous.norm.aestronglyMeasurable).mpr (by simpa using hint t ht)
  · rw [MeasureTheory.integral_eq_lintegral_of_nonneg_ae (h0 t) (hm t ht)]
    exact ENNReal.toReal_lt_of_lt_ofReal (hC t ht)

/-! ### Row K1 -/

/-- Row K1 for (C): OpenAI's proved theorem implies Clay's (C) as written in ClayLiteral. -/
theorem k1_C (ν : ℝ) (hν : 0 < ν) : AltC ν := by
  obtain ⟨Φ, hΦ, hf, hno⟩ := witness_C ν hν
  refine ⟨fun _ => 0, fun x t => Φ (x, t), d1_zero, d2_zero, ⟨Φ, hΦ, fun _ _ _ => rfl⟩, d3_zero,
    d5 hΦ hf, ?_⟩
  rintro ⟨p, u, h1, h2, h3, ⟨hu6, hp6⟩, h7⟩
  obtain ⟨hint, henergy⟩ := s5 u h7 (s4 u hu6)
  exact hno ⟨u, p,
    { navier_stokes := s1 ν _ u p h1 (s4 u hu6)
      div_free := s2 u h2 (s4 u hu6)
      initial_condition := s3 _ u h3
      velocity_smooth := s4 u hu6
      pressure_smooth := s4 p hp6
      integrable := hint
      globally_bounded_energy := henergy }⟩

/-- Row K1 for (D), with the erratum read as a condition on solutions (row S7). -/
theorem k1_D (ν : ℝ) (hν : 0 < ν) : AltD_withErratum ν := by
  obtain ⟨Φ, hΦ, hu, hf, hno⟩ := witness_D ν hν
  refine ⟨fun _ => 0, fun x t => Φ (x, t), d1_zero, d2_zero, ⟨Φ, hΦ, fun _ _ _ => rfl⟩,
    d6 _ _ hu hf, d7 hΦ hf, ?_⟩
  rintro ⟨p, u, h1, h2, h3, h10, ⟨hu6, hp6⟩, hErr⟩
  exact hno ⟨u, p,
    { navier_stokes := s1 ν _ u p h1 (s4 u hu6)
      div_free := s2 u h2 (s4 u hu6)
      initial_condition := s3 _ u h3
      velocity_smooth := s4 u hu6
      pressure_smooth := s4 p hp6
      isOnePeriodic_velocity := s6 u h10
      isOnePeriodic_pressure := s7_formal_side p hErr }⟩

/-! ### Row K1 under the second reading of C^∞ on a closed set

Under `SmoothOneSided`, Clay's smoothness is the formal `ContDiffOn` itself, so S4 is the
identity and the force's smoothness follows from its global smoothness. K1 therefore does not
depend on which reading of smoothness at t = 0 Clay intends. -/

theorem k1_C_oneSided (ν : ℝ) (hν : 0 < ν) : AltC_oneSided ν := by
  obtain ⟨Φ, hΦ, hf, hno⟩ := witness_C ν hν
  refine ⟨fun _ => 0, fun x t => Φ (x, t), d1_zero, d2_zero, hΦ.contDiffOn, d3_zero,
    d5 hΦ hf, ?_⟩
  rintro ⟨p, u, h1, h2, h3, ⟨hu6, hp6⟩, h7⟩
  obtain ⟨hint, henergy⟩ := s5 u h7 hu6
  exact hno ⟨u, p,
    { navier_stokes := s1 ν _ u p h1 hu6
      div_free := s2 u h2 hu6
      initial_condition := s3 _ u h3
      velocity_smooth := hu6
      pressure_smooth := hp6
      integrable := hint
      globally_bounded_energy := henergy }⟩

theorem k1_D_oneSided (ν : ℝ) (hν : 0 < ν) : AltD_withErratum_oneSided ν := by
  obtain ⟨Φ, hΦ, hu, hf, hno⟩ := witness_D ν hν
  refine ⟨fun _ => 0, fun x t => Φ (x, t), d1_zero, d2_zero, hΦ.contDiffOn,
    d6 _ _ hu hf, d7 hΦ hf, ?_⟩
  rintro ⟨p, u, h1, h2, h3, h10, ⟨hu6, hp6⟩, hErr⟩
  exact hno ⟨u, p,
    { navier_stokes := s1 ν _ u p h1 hu6
      div_free := s2 u h2 hu6
      initial_condition := s3 _ u h3
      velocity_smooth := hu6
      pressure_smooth := hp6
      isOnePeriodic_velocity := s6 u h10
      isOnePeriodic_pressure := s7_formal_side p hErr }⟩

/-! ### Non-vacuity control

If ClayLiteral's solution conditions could never hold, "no solution exists" would be trivially
true and K1 would say nothing. With zero data, the zero velocity and pressure satisfy every
condition, so the solution predicates are satisfiable and K1 has content. -/

theorem zero_solution_C (ν : ℝ) :
    ∃ (p : R3 → ℝ → ℝ) (u : R3 → ℝ → R3), Eq1 ν (fun _ _ => 0) u p ∧ Eq2 u ∧
      Eq3 (fun _ => 0) u ∧ Cond6 u p ∧ Cond7 u :=
  ⟨fun _ _ => 0, fun _ _ => 0, fun x t _ i => by simp, fun x t _ => by simp [ClayLiteral.div],
    fun _ => rfl, ⟨⟨fun _ => 0, contDiff_const, fun _ _ _ => rfl⟩,
      ⟨fun _ => 0, contDiff_const, fun _ _ _ => rfl⟩⟩, ⟨1, fun t _ => by simp⟩⟩

theorem zero_solution_D (ν : ℝ) :
    ∃ (p : R3 → ℝ → ℝ) (u : R3 → ℝ → R3), Eq1 ν (fun _ _ => 0) u p ∧ Eq2 u ∧
      Eq3 (fun _ => 0) u ∧ Cond10 u ∧ Cond6 u p ∧ Erratum p :=
  ⟨fun _ _ => 0, fun _ _ => 0, fun x t _ i => by simp, fun x t _ => by simp [ClayLiteral.div],
    fun _ => rfl, fun _ _ _ _ => rfl, ⟨⟨fun _ => 0, contDiff_const, fun _ _ _ => rfl⟩,
      ⟨fun _ => 0, contDiff_const, fun _ _ _ => rfl⟩⟩, fun _ _ _ _ => rfl⟩

end Bridges
