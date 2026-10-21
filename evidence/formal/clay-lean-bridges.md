# Clay ↔ Lean: claim → definition or lemma → proof → review → pending

This table turns the [risk review](clay-lean-risk.md) into a work plan for semantic and independent mathematical verification. Each row is one claim needed to conclude that the formal (C) and (D) proved by OpenAI imply Clay's (C) and (D). It records what would establish the claim, whether that exists, who has reviewed it, and what is missing. It is not a count of passing tests.

**State on 2026-10-21: no bridge lemma is formally proved, and no row has been reviewed by a mathematician.** The "Proof" column says how far each claim has got: *reading* means a written argument in this repository only.

## How the claims combine

(C) and (D) have the shape "there exist data for which no solution exists". The formal theorem implies Clay's if two families of one-directional lemmas hold:

- **Data side (D-rows):** every datum the formal statement accepts is a datum Clay accepts.
- **Solution side (S-rows):** every solution in Clay's sense is a solution in the formal sense.

Then take the same data; if a Clay solution existed it would be a formal solution, contradicting the formal theorem. That composition is row **K1**. Only one direction is needed per row, which in several rows is the easy one.

To state any of these as Lean lemmas, Clay's text must first be written in Lean literally: coordinates, partial derivatives `∂^α` as `iteratedFDeriv` applied to basis vectors, one-sided time derivatives at `t = 0`, and the Lebesgue integral. That literal formalization is row **K0**, and it needs its own review against the PDF, because it is itself an interpretation.

## Table

| ID | Claim | Definition or lemma | Proof | Review | Pending |
| --- | --- | --- | --- | --- | --- |
| K0 | A literal Lean rendering of Clay's (1)–(11), (C), (D) and the erratum exists | New file `ClayLiteral.lean` against the pinned Mathlib, written from the PDF, independent of DeepMind's style | none | none | Write it; review it line by line against the Clay PDF |
| K1 | Formal (C) ⇒ Clay (C), and the same for (D) | Composition: same `u₀, f`; D-rows map data, S-rows map a Clay solution to a formal one | reading | none | Formal proof once K0, D-rows and S-rows exist |
| P1 | For every ν > 0 and n = 3, as Clay requires | Specialize the formal `∀ nu > 0` to Clay's ν | reading (immediate) | none | One-line Lean term |
| D1 | Formal `ContDiff ℝ ∞ u₀` ⇒ Clay "u° smooth" | `∞ = ((⊤ : ℕ∞) : WithTop ℕ∞)` (checked in Mathlib); C^k in the Fréchet sense gives continuous partials of order k | reading | none | Lean lemma from `ContDiff` to continuity of all partials |
| D2 | Formal divergence-free ⇒ Clay `div u° = 0` | `(fderiv ℝ v x).trace = Σᵢ ∂ᵢvᵢ(x)` for `v` differentiable at `x` | reading | none | Lean lemma: trace of the derivative in the standard basis of `EuclideanSpace ℝ (Fin 3)` |
| D3 | Formal decay (4) ⇒ Clay decay (4) | `abs(∂^α uᵢ(x)) ≤ ‖Dᵐu(x)‖` for `abs(α) = m`, because `∂^α uᵢ(x)` is the m-linear map `Dᵐu(x)` applied to unit vectors, read in one coordinate. So the formal constant works for Clay | reading | none | Lean lemma via the operator-norm bound for multilinear maps; this is the easy direction |
| D4 | Formal `ContDiffOn ℝ ∞ (↿f) (univ ×ˢ Ici 0)` ⇒ Clay "f smooth on ℝ³ × [0, ∞)" | `univ ×ˢ Ici 0` has unique derivatives, so derivatives within the set are continuous and equal the one-sided partials | reading | none | Lean lemma identifying `iteratedFDerivWithin` with one-sided partials |
| D5 | Formal decay (5) ⇒ Clay decay (5) | As D3, for mixed partials `∂x^α ∂t^k` of `↿f` within the half-space; the basis vectors of ℝ³ × ℝ have norm 1 in Mathlib's product norm | reading | none | Lean lemma, as D3 plus D4 |
| D6 | Formal periodic data ⇒ Clay (8) | `IsOnePeriodic u₀` and `∀ t ≥ 0, IsOnePeriodic (f · t)` unfold to `f(x + eᵢ) = f(x)` | reading (definitional) | none | `Iff.rfl`-style Lean term |
| D7 | Formal decay (9) ⇒ Clay decay (9) | As D5 with `(1 + t)^-K`; Clay's `abs(t)` equals `t` for `t ≥ 0` | reading | none | Lean lemma, as D5 |
| S1 | Clay solution of (1) ⇒ formal `navier_stokes` | One-sided time derivative = `derivWithin … (Ici 0)`; Σⱼ uⱼ∂ⱼuᵢ = `fderiv ℝ (v · t) x (v x t)` componentwise; Mathlib's `Δ` = Σᵢ ∂ᵢ²; `gradient` components = ∂ᵢp | reading | none | Three Lean lemmas: Laplacian, gradient and convective term in coordinates |
| S2 | Clay (2) ⇒ formal `div_free` | D2 applied to `v(·, t)` | reading | none | Follows from D2 |
| S3 | Clay (3) ⇒ formal `initial_condition` | Same statement | reading (definitional) | none | Lean term |
| S4 | Clay (6), (11) ⇒ formal `velocity_smooth`, `pressure_smooth` | From C^∞ up to the boundary of ℝ³ × [0, ∞) to `ContDiffOn ℝ ∞` within `univ ×ˢ Ici 0` | reading | none | **Hardest row.** If Clay's C^∞ on a closed set means "restriction of a C^∞ function", it is immediate from `ContDiff.contDiffOn`. If it means "one-sided partials of every order are continuous", it needs an extension theorem (Seeley 1964) that Mathlib does not appear to have. Which reading Clay intends is itself a review question |
| S5 | Clay (7) ⇒ formal `integrable` and `globally_bounded_energy` | `u(·, t)` continuous, hence measurable; finite Lebesgue integral of `‖u‖²` gives `MemLp 2`; the Bochner integral then equals the Lebesgue integral; Mathlib's volume on `EuclideanSpace` is Lebesgue measure | reading | none | Lean lemma chaining these Mathlib facts |
| S6 | Clay (10) ⇒ formal `isOnePeriodic_velocity` | Same statement | reading (definitional) | none | Lean term |
| S7 | A Clay solution of (D) has periodic pressure | Clay's erratum: "p(x + eⱼ, t) = p(x, t) should be made explicit in Eqn (8)" | none: interpretive | none | **Needs a human decision.** If the erratum is read as a solution condition, S7 holds by definition. If not, the formal (D) is weaker, since non-periodic pressures p = q + c(t)·x are excluded. Ask Clay or a PDE specialist; optionally test whether OpenAI's construction also rules out such pressures |
| L1 | The formal and Clay statements have the same logical shape | `∃ u₀ f, data ∧ ¬ ∃ v p, solution` versus "there exist u°, f … for which there exist no solutions (p, u)" | reading | none | Covered by K1 |

**Count:** 18 rows. Formally proved: 0. Reviewed: 0. Needing a human decision: S7, and the reading question inside S4.

## Plan

1. **K0:** write `ClayLiteral.lean` from the PDF and publish it for review before proving anything, so the bridges cannot shape it.
2. **Easy rows first:** P1, D6, S3, S6, then D2, D3, D5, D7 and S2. These are short Lean proofs against the pinned Mathlib, checked on the same toolchain as the main study.
3. **Mid rows:** D1, D4, S1, S5.
4. **S4 and S7:** take them to independent review (the Lean Zulip and a PDE specialist) with the precise question each raises. Record the reviewer, date and answer in the Review column.
5. **K1:** prove the composition once the rows it depends on are closed or explicitly assumed.

A row moves to "formal" only when its Lean proof builds and is published with hashes, and to "reviewed" only when a named person other than the author and the assistant has checked it.
