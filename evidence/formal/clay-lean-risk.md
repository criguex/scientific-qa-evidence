# Clay ↔ Lean: could the formal (C) and (D) be easier than Clay's?

A reading-based risk review of the formal statement that OpenAI proved, which is identical to Google DeepMind's public statement ([provenance](statement-provenance/README.md)). It compares each clause of the official Clay text (Fefferman, [PDF](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf), SHA-256 `c1b5f27b…a06d0c`) with the Lean declarations at OpenAI commit `f9e8bc5`.

> **Status:** written by a QA engineer with AI assistance on 2026-10-21. It has **not** been reviewed by a mathematician, and the "standard fact" rows are not formalized here. It refines the [fidelity table](clay-lean-fidelity.md); it does not replace an expert review.

## Why direction matters

(C) and (D) have the shape **"there exist data such that no solution exists"**. A formalization can make that easier to prove than Clay's version in exactly two ways:

| Risk | What would go wrong | Safe when |
| --- | --- | --- |
| **Data loophole** | The formal statement lets the prover pick an initial velocity or force that Clay does not allow. | Every formal data condition implies the Clay condition. |
| **Solution loophole** | The formal solution class is stricter than Clay's, so "no solution" excludes fewer candidates. | Every Clay solution is also a formal solution. |

A clause that is stricter than Clay on the data side, or looser on the solution side, only makes the formal theorem harder to prove, so it is harmless for (C) and (D).

## Clause by clause

Status: **direct** means the same condition when read literally. **Standard fact** means equal by a textbook result that is named but not formalized here. **Attention** means it depends on interpretation.

| Clay clause | Side | Lean | Reading | Status |
| --- | --- | --- | --- | --- |
| ν > 0, n = 3 | parameter | `(nu : ℝ) (hnu : nu > 0)`, `ℝ³ = EuclideanSpace ℝ (Fin 3)` | Lean proves it for every ν > 0, which covers Clay's given ν. | direct |
| u° smooth | data | `ContDiff ℝ ∞ u₀` | `∞` is C^∞ (`(⊤ : ℕ∞)`), not analytic `ω`. | direct |
| div u° = 0 | data | `∀ x, ∇⬝ u₀ x = 0`, divergence = trace of `fderiv` | For a differentiable field the trace of the Jacobian is Σ ∂uᵢ/∂xᵢ. | standard fact (e) |
| (4) decay of u° | data, (C) | `∀ m K, ∃ C, ∀ x, ‖iteratedFDeriv ℝ m u₀ x‖ ≤ C / (1 + ‖x‖) ^ K` | The operator norm of the m-th derivative and the largest partial ∂^α with abs(α) = m bound each other up to constants depending on m and n. `K : ℝ` ranges over every exponent Clay uses. | standard fact (a), (b) |
| f smooth on ℝ³ × [0, ∞) | data | `ContDiffOn ℝ ∞ (↿f) (univ ×ˢ Ici 0)` | Smoothness within a closed half-space equals smoothness up to the boundary. | standard fact (c) |
| (5) decay of f | data, (C) | `iteratedFDerivWithin ℝ m (↿f) (univ ×ˢ Ici 0) (x, t)` bounded by `C / (1 + ‖x‖ + t) ^ K` for t ≥ 0 | The joint derivative of order m in (x, t) controls and is controlled by the mixed partials ∂x^α ∂t^k with abs(α) + k = m. | standard fact (a), (c) |
| (8) u°, f periodic | data, (D) | `IsOnePeriodic u₀`; `∀ t ≥ 0, IsOnePeriodic (f · t)` | `f (x + eᵢ) = f x` for each unit vector. | direct |
| (9) decay of periodic f | data, (D) | same derivative bound with `C / (1 + t) ^ K` | As for (5). | standard fact (a), (c) |
| (1) the equation | solution | `derivWithin (v x ·) (Ici 0) t + fderiv ℝ (v · t) x (v x t) = nu • Δ (v · t) x - gradient (p · t) x + f x t` for t ≥ 0 | (u·∇)u is the spatial derivative applied to u. `Δ` and `gradient` are Mathlib's coordinate-free versions of Clay's sums. The one-sided time derivative at t = 0 matches "t ≥ 0". Solutions are smooth, so no junk values arise. | standard fact (c), (e) |
| (2) div u = 0 | solution | `∀ x, ∀ t ≥ 0, ∇⬝ (v · t) x = 0` | As for div u°. | standard fact (e) |
| (3) initial condition | solution | `∀ x, v x 0 = u₀ x` | Same. | direct |
| (6), (11) p, u ∈ C^∞(ℝ³ × [0, ∞)) | solution | `ContDiffOn ℝ ∞ (↿v) …`, `ContDiffOn ℝ ∞ (↿p) …` on `univ ×ˢ Ici 0` | On a closed half-space, smooth-within-the-set agrees with C^∞ up to the boundary, which by Seeley's extension theorem (Proc. AMS 15, 1964) is the restriction of a C^∞ function. Neither class is stricter. | standard fact (c) |
| (7) bounded energy | solution, (C) | `∀ t ≥ 0, MemLp (‖v · t‖) 2` and `∃ E, ∀ t ≥ 0, ∫ x, ‖v x t‖ ^ 2 < E` | The `MemLp` clause stops Lean's Bochner integral, which is 0 for non-integrable functions, from making the bound vacuous. Any Clay solution satisfies it, because a finite Lebesgue integral of the continuous ‖u‖² means u(·, t) ∈ L². The constant comes before "for all t", as in Clay. | standard fact (d) |
| (10) u periodic | solution, (D) | `∀ t ≥ 0, IsOnePeriodic (v · t)` | Same. | direct |
| Erratum: p periodic | solution, (D) | `∀ t ≥ 0, IsOnePeriodic (p · t)` | See below. | **attention** |
| Logical form of (C), (D) | — | `∃ u₀ f, data ∧ ¬ ∃ v p, solution` | "there exist u°, f … for which there exist no solutions (p, u)". | direct |

**Count:** 16 rows. 6 direct, 9 equal by a standard fact, 1 needing attention, none found to open a loophole.

## The one point that needs attention: periodic pressure in (D)

Clay's erratum says: *"The further condition p(x + e_j, t) = p(x, t) should be made explicit in Eqn (8)."* Equation (8) is the list of conditions on the data u° and f, but p is part of the solution. The formalization reads the erratum as a condition on solutions, the only reading in which it constrains anything, and adds `isOnePeriodic_pressure` to the periodic solution class.

This is a solution-side restriction, so it matters for (D):

- With u and f periodic, equation (1) forces ∇p to be periodic, but p itself may then carry a spatially linear part, p = q + c(t)·x, with q periodic. That part is a uniform pressure gradient: integrating (1) over the torus gives d/dt ∫u dx = ∫f dx − c(t), so it changes the mean velocity.
- Without the erratum, such pressures are allowed, the solution class is larger, and "no solution exists" would be a **stronger** claim than the formal (D).
- With the erratum read as a requirement on solutions, the classes match.

So the formal (D) proves the problem as amended by the erratum. (C) is on ℝ³ and is not affected. Whether the amended statement is the intended prize problem is a question for Clay and expert reviewers, not one this review can settle.

## Bridges that remain

The standard facts (a)–(e) are the [open bridges](clay-lean-fidelity.md#open-bridges-to-equivalence) of the fidelity table, now located clause by clause. They are textbook analysis, and all are statable in Mathlib, so the natural next step is to prove them as Lean lemmas instead of citing them. The erratum point needs a human decision, not a proof.
