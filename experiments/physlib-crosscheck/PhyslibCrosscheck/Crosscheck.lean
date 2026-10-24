/-
Cross-check of `ClayLiteral`'s equations (1) and (2) against Physlib's `ConvectiveNavierStokes`
(F. Wiesner, Physlib/FluidDynamics/CauchyFlow/NavierStokes.lean at commit
8ddcc004043c5b537e4225fa763121c176b62a4a), an independently written definition.

Clay's u, p, f are moved to Physlib's `Time` and `Space 3` along the canonical equivalences
`Time.val` and `Space.basis.repr`, with density 1, shear viscosity ν and second viscosity 0.
Physlib's predicate quantifies over all times, so the comparison is made point by point;
`convectiveNavierStokes_iff_forall_at` checks that the pointwise form is Physlib's definition.
-/
import PhyslibCrosscheck.ClayLiteralCopy
import Physlib.FluidDynamics.CauchyFlow.NavierStokes

open scoped Time
open FluidDynamics ClayLiteral

namespace PhyslibCrosscheck

/-- A field g(x, t) on ℝ³ × ℝ, read on Physlib's `Time` and `Space 3`. -/
noncomputable def transport {X : Type} (g : R3 → ℝ → X) : Time → Space 3 → X :=
  fun t x => g (Space.basis.repr x) t.val

lemma deriv_transport {X : Type} [NormedAddCommGroup X] [NormedSpace ℝ X]
    (g : R3 → X) (x : Space 3) (j : Fin 3) :
    ∂[j] (fun x' => g (Space.basis.repr x')) x = fderiv ℝ g (Space.basis.repr x) (e j) := by
  rw [Space.deriv_eq]
  have : (fun x' => g (Space.basis.repr x')) = g ∘ Space.basis.repr.toContinuousLinearEquiv :=
    rfl
  rw [this, ContinuousLinearEquiv.comp_right_fderiv]
  simp [e]

lemma timeDeriv_transport {X : Type} [NormedAddCommGroup X] [NormedSpace ℝ X]
    (g : ℝ → X) (t : Time) : ∂ₜ (fun t' : Time => g t'.val) t = deriv g t.val := by
  rw [Time.deriv_eq]
  have : (fun t' : Time => g t'.val) = g ∘ Time.toRealCLE := rfl
  rw [this, ContinuousLinearEquiv.comp_right_fderiv]
  change fderiv ℝ g t.val (Time.val 1) = _
  rw [Time.one_val]
  rfl

/-- Clay's data as a Physlib flow: density 1, velocity u, Newtonian stress with pressure p,
    shear viscosity ν and second viscosity 0, and specific body force f. -/
noncomputable def clayFlow (ν : ℝ) (f u : R3 → ℝ → R3) (p : R3 → ℝ → ℝ) : CauchyFlow 3 where
  rho := fun _ _ => 1
  velocity := transport u
  stress := FluidFlow.newtonianStressTensor 3 ⟨fun _ _ => 1, transport u⟩ (transport p)
    (fun _ _ => ν) (fun _ _ => 0)
  specificBodyForce := transport f

/-- The three conjuncts of Physlib's `ConvectiveNavierStokes` at one point (t, x). -/
def ConvectiveNavierStokesAt (d : ℕ) (flow : CauchyFlow d)
    (pressure shearViscosity secondViscosity : ScalarField d) (t : Time) (x : Space d) : Prop :=
  (DifferentiableAt ℝ (flow.rho · x) t →
      DifferentiableAt ℝ (fun x' => flow.rho t x' • flow.velocity t x') x →
        ∂ₜ (flow.rho · x) t + (∇ ⬝ fun x' => flow.rho t x' • flow.velocity t x') x = 0) ∧
    flow.rho t x • FluidFlow.materialAcceleration d flow.toFluidFlow t x =
      Space.matrixDiv d (flow.stress t) x + flow.rho t x • flow.specificBodyForce t x ∧
    flow.stress t x =
      FluidFlow.newtonianStressTensor d flow.toFluidFlow pressure shearViscosity secondViscosity t x

/-- `ConvectiveNavierStokesAt` is Physlib's `ConvectiveNavierStokes` read point by point. -/
theorem convectiveNavierStokes_iff_forall_at (d : ℕ) (flow : CauchyFlow d)
    (pressure shearViscosity secondViscosity : ScalarField d) :
    ConvectiveNavierStokes d flow pressure shearViscosity secondViscosity ↔
      ∀ t x, ConvectiveNavierStokesAt d flow pressure shearViscosity secondViscosity t x :=
  ⟨fun h t x => ⟨h.1 t x, h.2.1 t x, h.2.2 t x⟩,
    fun h => ⟨fun t x => (h t x).1, fun t x => (h t x).2.1, fun t x => (h t x).2.2⟩⟩

lemma fderiv_fderiv_comm (g : R3 → ℝ) (hg : ContDiff ℝ 2 g) (x v w : R3) :
    fderiv ℝ (fun y => fderiv ℝ g y v) x w = fderiv ℝ (fun y => fderiv ℝ g y w) x v := by
  have hd : Differentiable ℝ (fderiv ℝ g) :=
    (hg.fderiv_right (m := 1) (by norm_num)).differentiable (by norm_num)
  rw [fderiv_clm_apply (hd x) (differentiableAt_const v),
    fderiv_clm_apply (hd x) (differentiableAt_const w)]
  simp
  exact (hg.contDiffAt.isSymmSndFDerivAt (by simp)).eq w v

lemma div_clayFlow (ν : ℝ) (f u : R3 → ℝ → R3) (p : R3 → ℝ → ℝ) (t : Time) (x : Space 3) :
    (∇ ⬝ fun x' => (clayFlow ν f u p).rho t x' • (clayFlow ν f u p).velocity t x') x =
      div (fun y => u y t.val) (Space.basis.repr x) := by
  simp only [clayFlow, one_smul, transport, Space.div, ClayLiteral.div]
  exact Finset.sum_congr rfl fun i _ => deriv_transport (fun y => u y t.val i) x i

section

variable (ν : ℝ) (f u : R3 → ℝ → R3) (p : R3 → ℝ → ℝ)

lemma stress_clayFlow (t : Time) (x : Space 3) (i j : Fin 3) :
    (clayFlow ν f u p).stress t x i j =
      -(p (Space.basis.repr x) t.val * (1 : Matrix (Fin 3) (Fin 3) ℝ) i j) +
        (ν * fderiv ℝ (fun y => u y t.val i) (Space.basis.repr x) (e j) +
          ν * fderiv ℝ (fun y => u y t.val j) (Space.basis.repr x) (e i)) := by
  simp [clayFlow, FluidFlow.newtonianStressTensor, FluidFlow.velocityGradient, transport]
  rw [deriv_transport (fun y => u y t.val i), deriv_transport (fun y => u y t.val j)]

lemma matrixDiv_clayFlow (hu : ∀ s, ContDiff ℝ 2 (fun y => u y s))
    (hp : ∀ s, Differentiable ℝ (fun y => p y s)) (t : Time)
    (hdiv : ∀ y, div (fun z => u z t.val) y = 0) (x : Space 3) (i : Fin 3) :
    Space.matrixDiv 3 ((clayFlow ν f u p).stress t) x i =
      ν * ∑ k : Fin 3, fderiv ℝ (fun y => fderiv ℝ (fun z => u z t.val i) y (e k))
          (Space.basis.repr x) (e k)
        - fderiv ℝ (fun y => p y t.val) (Space.basis.repr x) (e i) := by
  have hui : ∀ k, ContDiff ℝ 2 (fun z => u z t.val k) := fun k => contDiff_euclidean.mp (hu t.val) k
  have hG : ∀ k l, Differentiable ℝ (fun y => fderiv ℝ (fun z => u z t.val k) y (e l)) :=
    fun k l => (((hui k).fderiv_right (m := 1) (by norm_num)).differentiable
      (by norm_num)).clm_apply (differentiable_const _)
  have h1 : ∀ j, ∂[j] (fun x' => (clayFlow ν f u p).stress t x' i j) x =
      fderiv ℝ (fun y => -(p y t.val * (1 : Matrix (Fin 3) (Fin 3) ℝ) i j) +
        (ν * fderiv ℝ (fun z => u z t.val i) y (e j) +
          ν * fderiv ℝ (fun z => u z t.val j) y (e i))) (Space.basis.repr x) (e j) := by
    intro j
    rw [← deriv_transport]
    exact congrArg (fun F => Space.deriv j F x)
      (funext fun x' => stress_clayFlow ν f u p t x' i j)
  have h2 : ∀ j y, fderiv ℝ (fun y => -(p y t.val * (1 : Matrix (Fin 3) (Fin 3) ℝ) i j) +
        (ν * fderiv ℝ (fun z => u z t.val i) y (e j) +
          ν * fderiv ℝ (fun z => u z t.val j) y (e i))) y (e j) =
      -(fderiv ℝ (fun y => p y t.val) y (e j) * (1 : Matrix (Fin 3) (Fin 3) ℝ) i j) +
        (ν * fderiv ℝ (fun y => fderiv ℝ (fun z => u z t.val i) y (e j)) y (e j) +
          ν * fderiv ℝ (fun y => fderiv ℝ (fun z => u z t.val j) y (e i)) y (e j)) := by
    intro j y
    rw [fderiv_fun_add, fderiv_fun_neg, fderiv_mul_const, fderiv_fun_add, fderiv_const_mul,
      fderiv_const_mul]
    · simp [mul_comm]
    all_goals fun_prop
  have hB : ∑ j : Fin 3,
      fderiv ℝ (fun y => fderiv ℝ (fun z => u z t.val j) y (e i)) (Space.basis.repr x) (e j) =
        0 := by
    rw [Finset.sum_congr rfl fun j _ => fderiv_fderiv_comm _ (hui j) _ (e i) (e j),
      ← sum_apply, ← fderiv_fun_sum fun j _ => (hG j j) _]
    have : (fun y => ∑ j : Fin 3, fderiv ℝ (fun z => u z t.val j) y (e j)) = fun _ => 0 :=
      funext hdiv
    rw [this]
    simp
  rw [Space.matrixDiv_apply]
  simp_rw [h1, h2]
  simp only [Finset.sum_add_distrib, Finset.sum_neg_distrib, ← Finset.mul_sum, hB,
    Matrix.one_apply, mul_ite, mul_one, mul_zero, Finset.sum_ite_eq, Finset.mem_univ, ite_true]
  ring

lemma continuity_clayFlow (t : Time) (x : Space 3) :
    ∂ₜ ((clayFlow ν f u p).rho · x) t +
        (∇ ⬝ fun x' => (clayFlow ν f u p).rho t x' • (clayFlow ν f u p).velocity t x') x =
      div (fun z => u z t.val) (Space.basis.repr x) := by
  rw [div_clayFlow]
  simp [clayFlow, Time.deriv_eq]

lemma div_of_convectiveNavierStokesAt (hu : ∀ s, ContDiff ℝ 2 (fun y => u y s)) (t : Time)
    (x : Space 3)
    (h : ConvectiveNavierStokesAt 3 (clayFlow ν f u p) (transport p) (fun _ _ => ν)
      (fun _ _ => 0) t x) :
    div (fun z => u z t.val) (Space.basis.repr x) = 0 := by
  have hd : Differentiable ℝ (transport u t) :=
    ((hu t.val).differentiable (by norm_num)).comp
      Space.basis.repr.toContinuousLinearEquiv.differentiable
  rw [← continuity_clayFlow ν f u p t x]
  refine h.1 (differentiableAt_const (1 : ℝ)) ?_
  simp only [clayFlow, one_smul]
  exact hd x

lemma materialAcceleration_clayFlow (hu : ∀ s, ContDiff ℝ 2 (fun y => u y s))
    (hut : ∀ y s, DifferentiableAt ℝ (fun s => u y s) s) (t : Time) (x : Space 3) (i : Fin 3) :
    FluidFlow.materialAcceleration 3 (clayFlow ν f u p).toFluidFlow t x i =
      deriv (fun s => u (Space.basis.repr x) s i) t.val +
        ∑ j : Fin 3, u (Space.basis.repr x) t.val j *
          fderiv ℝ (fun y => u y t.val i) (Space.basis.repr x) (e j) := by
  have hd : Differentiable ℝ (transport u t) :=
    ((hu t.val).differentiable (by norm_num)).comp
      Space.basis.repr.toContinuousLinearEquiv.differentiable
  change (∂ₜ (fun t' : Time => u (Space.basis.repr x) t'.val) t +
    ∑ j, transport u t x j • ∂[j] (transport u t) x) i = _
  rw [timeDeriv_transport (fun s => u (Space.basis.repr x) s)]
  simp only [PiLp.add_apply, WithLp.ofLp_sum, Finset.sum_apply, PiLp.smul_apply, smul_eq_mul]
  congr 1
  · exact (((EuclideanSpace.proj i : R3 →L[ℝ] ℝ).hasFDerivAt.comp_hasDerivAt _
      (hut _ _).hasDerivAt).deriv).symm
  · refine Finset.sum_congr rfl fun j _ => ?_
    rw [← Space.deriv_euclid hd]
    exact congrArg (u (Space.basis.repr x) t.val j * ·)
      (deriv_transport (fun y => u y t.val i) x j)

lemma convectiveNavierStokesAt_clayFlow_iff (hu : ∀ s, ContDiff ℝ 2 (fun y => u y s))
    (hut : ∀ y s, DifferentiableAt ℝ (fun s => u y s) s)
    (hp : ∀ s, Differentiable ℝ (fun y => p y s)) (t : Time) (ht : 0 ≤ t.val)
    (hdiv : ∀ y, div (fun z => u z t.val) y = 0) (x : Space 3) :
    ConvectiveNavierStokesAt 3 (clayFlow ν f u p) (transport p) (fun _ _ => ν) (fun _ _ => 0)
        t x ↔
      ∀ i : Fin 3,
        derivWithin (fun s => u (Space.basis.repr x) s i) (Set.Ici 0) t.val
          + ∑ j : Fin 3, u (Space.basis.repr x) t.val j *
              fderiv ℝ (fun y => u y t.val i) (Space.basis.repr x) (e j)
        = ν * ∑ k : Fin 3, fderiv ℝ (fun y => fderiv ℝ (fun z => u z t.val i) y (e k))
              (Space.basis.repr x) (e k)
          - fderiv ℝ (fun y => p y t.val) (Space.basis.repr x) (e i)
            + f (Space.basis.repr x) t.val i := by
  have hcont := continuity_clayFlow ν f u p t
  have hderiv : ∀ i : Fin 3,
      derivWithin (fun s => u (Space.basis.repr x) s i) (Set.Ici 0) t.val =
        deriv (fun s => u (Space.basis.repr x) s i) t.val := fun i =>
    (((EuclideanSpace.proj i : R3 →L[ℝ] ℝ).differentiableAt.comp _ (hut _ _)).derivWithin
      (uniqueDiffOn_Ici 0 _ ht))
  have hnewt : (clayFlow ν f u p).stress t x = FluidFlow.newtonianStressTensor 3
      (clayFlow ν f u p).toFluidFlow (transport p) (fun _ _ => ν) (fun _ _ => 0) t x := rfl
  have hrho : (clayFlow ν f u p).rho t x = 1 := rfl
  have hf : (clayFlow ν f u p).specificBodyForce t x = f (Space.basis.repr x) t.val := rfl
  simp only [ConvectiveNavierStokesAt, hcont, hdiv, hnewt, implies_true, and_true, true_and]
  rw [hrho, hf, one_smul, one_smul]
  refine ⟨fun h i => ?_, fun h => ?_⟩
  · have hi := congrArg (fun v : R3 => v i) h
    simp only [PiLp.add_apply] at hi
    rw [hderiv, ← materialAcceleration_clayFlow ν f u p hu hut, hi,
      matrixDiv_clayFlow ν f u p hu hp t hdiv]
  · ext i
    rw [PiLp.add_apply, materialAcceleration_clayFlow ν f u p hu hut,
      matrixDiv_clayFlow ν f u p hu hp t hdiv, ← hderiv]
    exact h i

/-- Clay's equations (1) and (2) on ℝ³ × [0, ∞) hold if and only if Physlib's convective
    Navier–Stokes equations hold at every (t, x) with t ≥ 0, for density 1, shear viscosity ν,
    second viscosity 0 and specific body force f, when u is C² in space and differentiable in
    time and p is differentiable in space. -/
theorem eq1_and_eq2_iff_convectiveNavierStokesAt
    (hu : ∀ s, ContDiff ℝ 2 (fun y => u y s))
    (hut : ∀ y s, DifferentiableAt ℝ (fun s => u y s) s)
    (hp : ∀ s, Differentiable ℝ (fun y => p y s)) :
    Eq1 ν f u p ∧ Eq2 u ↔
      ∀ t : Time, 0 ≤ t.val → ∀ x : Space 3,
        ConvectiveNavierStokesAt 3 (clayFlow ν f u p) (transport p) (fun _ _ => ν)
          (fun _ _ => 0) t x := by
  have hL : ∀ y : R3, Space.basis.repr (Space.basis.repr.symm y) = y := fun y => by simp
  constructor
  · rintro ⟨h1, h2⟩ t ht x
    exact (convectiveNavierStokesAt_clayFlow_iff ν f u p hu hut hp t ht
      (fun y => h2 y t.val ht) x).2 (h1 _ _ ht)
  · intro h
    have h2 : Eq2 u := fun y s hs => by
      simpa only [hL] using
        div_of_convectiveNavierStokesAt ν f u p hu ⟨s⟩ (Space.basis.repr.symm y) (h ⟨s⟩ hs _)
    refine ⟨fun y s hs i => ?_, h2⟩
    simpa only [hL] using (convectiveNavierStokesAt_clayFlow_iff ν f u p hu hut hp ⟨s⟩ hs
      (fun y => h2 y s hs) (Space.basis.repr.symm y)).1 (h ⟨s⟩ hs _) i

/-- Physlib's convective Navier–Stokes equations for all times imply Clay's (1) and (2). -/
theorem eq1_and_eq2_of_convectiveNavierStokes
    (hu : ∀ s, ContDiff ℝ 2 (fun y => u y s))
    (hut : ∀ y s, DifferentiableAt ℝ (fun s => u y s) s)
    (hp : ∀ s, Differentiable ℝ (fun y => p y s))
    (h : ConvectiveNavierStokes 3 (clayFlow ν f u p) (transport p) (fun _ _ => ν)
      (fun _ _ => 0)) :
    Eq1 ν f u p ∧ Eq2 u :=
  (eq1_and_eq2_iff_convectiveNavierStokesAt ν f u p hu hut hp).2 fun t _ x =>
    (convectiveNavierStokes_iff_forall_at 3 _ _ _ _).1 h t x

end

end PhyslibCrosscheck
