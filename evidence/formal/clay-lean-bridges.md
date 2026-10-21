# Clay ↔ Lean: claim → definition or lemma → proof → review → pending

This table turns the [risk review](clay-lean-risk.md) into a work plan for semantic and independent mathematical verification. Each row is one claim needed to conclude that the formal (C) and (D) proved by OpenAI imply Clay's (C) and (D). It records what would establish the claim, whether that exists, who has reviewed it, and what is missing. It is not a count of passing tests.

**State on 2026-10-21: K1 is proved in Lean without hypotheses: for every ν > 0, OpenAI's proved theorems imply Clay's (C) and Clay's (D), as written in `ClayLiteral`, with the erratum read as a condition on solutions. All 18 rows except S7 are formally proved, D1–D5 and D7 for OpenAI's concrete witness. Everything uses only the axioms `propext`, `Classical.choice` and `Quot.sound`. K1 also holds under the second reading of smoothness at t = 0 (derivatives continuous up to t = 0), so that choice does not decide the result. (C) does not use the erratum; S7 affects (D) only. ClayLiteral itself has not been reviewed against the PDF by anyone independent ([review sheet](../../bridges/K0_REVIEW.md)), and no row has been reviewed by a mathematician.** Lean files and build receipt: [`bridges/`](../../bridges/README.md). The "Proof" column says how far each claim has got: *reading* means a written argument in this repository only.

## How the claims combine

(C) and (D) have the shape "there exist data for which no solution exists". The formal theorem implies Clay's if two families of one-directional lemmas hold:

- **Data side (D-rows):** every datum the formal statement accepts is a datum Clay accepts.
- **Solution side (S-rows):** every solution in Clay's sense is a solution in the formal sense.

Then take the same data; if a Clay solution existed it would be a formal solution, contradicting the formal theorem. That composition is row **K1**. Only one direction is needed per row, which in several rows is the easy one.

To state any of these as Lean lemmas, Clay's text must first be written in Lean literally: coordinates, partial derivatives `∂^α` as `iteratedFDeriv` applied to basis vectors, one-sided time derivatives at `t = 0`, and the Lebesgue integral. That literal formalization is row **K0**, and it needs its own review against the PDF, because it is itself an interpretation.

## Table

| ID | Claim | Definition or lemma | Proof | Review | Pending |
| --- | --- | --- | --- | --- | --- |
| K0 | A literal Lean rendering of Clay's (1)–(11), (C), (D) and the erratum exists | [`bridges/ClayLiteral.lean`](../../bridges/ClayLiteral.lean), against the pinned Mathlib, independent of DeepMind's style. Non-vacuity control: the zero solution satisfies every solution condition for zero data (`Bridges.zero_solution_C`, `_D`) | **written; typechecks; non-vacuous** | none | Independent line-by-line review against the Clay PDF: [`K0_REVIEW.md`](../../bridges/K0_REVIEW.md), 14 points, smoothness at t = 0 first |
| K1 | Formal (C) ⇒ Clay (C), and the same for (D) | `Bridges.k1_C : ∀ ν, 0 < ν → AltC ν`, `Bridges.k1_D : ∀ ν, 0 < ν → AltD_withErratum ν`, from OpenAI's `NavierStokesR3.theorem_1_1` and `PeriodicPaper.periodic_corollary` | **formal, no hypotheses** (relative to K0), under both readings of C^∞ at t = 0: also `k1_C_oneSided`, `k1_D_oneSided` | none | Review; (D) without the erratum is not covered (S7); (C) does not depend on S7 |
| P1 | For every ν > 0 and n = 3, as Clay requires | `Bridges.p1`; K1 is stated for every ν > 0 | **formal** | none | Review |
| D1 | OpenAI's u₀ is smooth in Clay's sense | u₀ = 0: `Bridges.d1_zero` | **formal for the witness** | none | Review |
| D2 | OpenAI's u₀ has `div u° = 0` | u₀ = 0: `Bridges.d2_zero` | **formal for the witness** | none | Review |
| D3 | OpenAI's u₀ satisfies Clay's (4) | Every derivative of 0 is 0: `Bridges.dx_zero`, `Bridges.d3_zero` | **formal for the witness** | none | Review |
| D4 | OpenAI's force is C^∞ on ℝ³ × [0, ∞) in Clay's sense | Under the restriction reading this needs a smooth extension. OpenAI's construction gives `ContDiff ℝ ∞` on all of ℝ × ℝ³ (`CandidateProperties.force_smooth`, both constructions), so the force is its own extension: `Bridges.witness_C`, `Bridges.witness_D` | **formal for the witness** | none | A general version for arbitrary formal forces would need an extension theorem (Whitney or Seeley); K1 does not need it |
| D5 | OpenAI's force satisfies Clay's (5) | Clay's mixed partial `∂x^α ∂t^m f` equals the iterated derivative applied to unit vectors (`Bridges.dirDeriv_eq`, `dt_eq`, `dxt_eq`), so it is bounded by the formal norm (`Bridges.clay_bound`); then the formal decay gives (5): `Bridges.d5` | **formal** for any force with a globally smooth extension | none | Review |
| D6 | Formal periodic data ⇒ Clay (8) | `Bridges.d6` | **formal** | none | Review |
| D7 | OpenAI's periodic force satisfies Clay's (9) | As D5, with `(1 + abs(t))^-K`: `Bridges.d7` | **formal** for any force with a globally smooth extension | none | Review |
| S1 | Clay solution of (1) ⇒ formal `navier_stokes` | Componentwise: time derivative, convective term (basis expansion), Laplacian (OpenAI's `laplacian_eq`), gradient (`inner_gradient_right`): `Bridges.s1` | **formal** | none | Review |
| S2 | Clay (2) ⇒ formal `div_free` | Trace in the standard basis (OpenAI's `divergence_eq`) and coordinates of the derivative: `Bridges.s2` | **formal** | none | Review |
| S3 | Clay (3) ⇒ formal `initial_condition` | `Bridges.s3` | **formal** | none | Review |
| S4 | Clay (6), (11) ⇒ formal `velocity_smooth`, `pressure_smooth` | `Bridges.s4`, under the restriction reading of C^∞ on a closed set | **formal** under the restriction reading; the identity under the one-sided reading | none | Which reading Clay intends no longer decides K1, which is proved under both |
| S5 | Clay (7) ⇒ formal `integrable` and `globally_bounded_energy` | Continuity gives measurability; a finite Lebesgue integral gives `Integrable` and `MemLp 2`; the Bochner integral is the real part of the Lebesgue one: `Bridges.s5` | **formal** | none | Review |
| S6 | Clay (10) ⇒ formal `isOnePeriodic_velocity` | `Bridges.s6` | **formal** | none | Review |
| S7 | A Clay solution of (D) has periodic pressure | Clay's erratum: "p(x + eⱼ, t) = p(x, t) should be made explicit in Eqn (8)" | interpretive; formal side proved (`Bridges.s7_formal_side`), used by K1 for (D) | none | **Needs a human decision.** If the erratum is a solution condition, K1 for (D) is the full result. If not, the formal (D) is weaker: non-periodic pressures p = q + c(t)·x are excluded. Question sent to the Clay Mathematics Institute on 2026-10-21 |
| L1 | The formal and Clay statements have the same logical shape | Discharged by K1 | **formal** (via K1) | none | — |

**Count:** 18 rows. Formally proved: 16 (K1, P1, D1–D7, S1–S6, L1), D1–D4 for OpenAI's witness. K0 written and checked non-vacuous. S7 interpretive, formal side proved. Reviewed: 0.

**What K1 does not establish.** It does not show that `ClayLiteral` is a faithful rendering of Clay's PDF; that is K0's review. It does not cover (D) with the erratum read only as a condition on data. It inherits trust in OpenAI's proof, which rests on the kernel checks in [cd-validation](cd-validation/README.md), and it says nothing about whether OpenAI's Lean proof follows OpenAI's paper.

## Plan

1. **Done:** K0, every D- and S-row except S7, and K1.
2. **Independent review of K0**, line by line against the PDF, by someone other than the author and the assistant; record the reviewer, date and answer in the Review column.
3. **S7 and the reading of C^∞ on a closed set:** take both to a PDE specialist and the Lean Zulip; record the answers.
4. **Mathematical review** of the bridge rows.

A row moves to "formal" only when its Lean proof builds and is published with hashes, and to "reviewed" only when a named person other than the author and the assistant has checked it.
