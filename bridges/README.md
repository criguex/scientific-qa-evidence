# Bridges: Clay's text in Lean, and lemmas linking it to the formal statement

Work for the semantic plan in [`evidence/formal/clay-lean-bridges.md`](../evidence/formal/clay-lean-bridges.md).

| File | Content |
| --- | --- |
| [`ClayLiteral.lean`](ClayLiteral.lean) | Row K0: Clay's equations (1)–(11), alternatives (C) and (D) and the erratum, written literally (coordinates, partial derivatives along basis vectors, one-sided time derivatives, Lebesgue integral). Definitions only, plus one sanity theorem. **Awaiting review against the PDF.** |
| [`Bridges.lean`](Bridges.lean) | Lemmas between OpenAI's statement and `ClayLiteral`, and the composition K1. It imports OpenAI's solution module, so K1 starts from OpenAI's proved theorems. |

## Readings chosen in ClayLiteral (to be reviewed)

| Reading | Choice made | Alternative left open |
| --- | --- | --- |
| C^∞(ℝ³ × [0, ∞)), row S4 | Restriction of a C^∞ function on ℝ³ × ℝ | Continuous one-sided derivatives of every order up to t = 0 |
| The erratum, row S7 | (D) stated both with and without periodic pressure on solutions | — |
| Exponent K in (4), (5), (9) | Ranges over the reals | Natural numbers only (a weaker requirement) |
| Multi-index α | A list of directions, so order and repetition are explicit | — |

## Build receipt (2026-10-21)

Built on the Linux test host against the no-cache build B4 of OpenAI's `f9e8bc5`, so with the same Lean and Mathlib as the main study.

| Item | Value |
| --- | --- |
| Lean | `4.34.0-rc2`, commit `6a10ac8c22beadecabdbb0919c2b50214762f91d` |
| Mathlib | `85e3a25e006c35636f0e53b0e9296caca2685bc0` (B4, compiled locally) |
| `ClayLiteral.lean` SHA-256 | `1998dac2bee2477b8cc1d100f5345574624bf62290d1f85abf27203b9f8acb2d` |
| `Bridges.lean` SHA-256 | `b22ddc0e09bf21778700b9ac8b5674b683aa365cafc99aac3ac354d3c1c73278` |
| `ClayLiteral.lean` | typechecks, exit 0 |
| `Bridges.lean` | typechecks, exit 0 |

`#print axioms` for every theorem proved so far:

| Theorem | Row | Axioms |
| --- | --- | --- |
| `Bridges.d6` | D6 | propext, Classical.choice, Quot.sound |
| `Bridges.s3` | S3 | propext, Classical.choice, Quot.sound |
| `Bridges.s6` | S6 | propext, Classical.choice, Quot.sound |
| `Bridges.p1` | P1 | propext, Classical.choice, Quot.sound |
| `Bridges.s4` | S4, restriction reading | propext, Classical.choice, Quot.sound |
| `Bridges.d1_zero`, `d2_zero`, `d3_zero` | D1, D2, D3 for u₀ = 0 | propext, Classical.choice, Quot.sound |
| `Bridges.witness_C`, `witness_D` | D4 for OpenAI's forces | propext, Classical.choice, Quot.sound |
| `Bridges.k1_C` | K1 for (C), no hypotheses | propext, Classical.choice, Quot.sound |
| `Bridges.k1_D` | K1 for (D), no hypotheses | propext, Classical.choice, Quot.sound |
| `Bridges.s7_formal_side` | S7 (formal side only) | propext, Classical.choice, Quot.sound |
| `ClayLiteral.altD_withoutErratum_imp_withErratum` | sanity | propext, Classical.choice, Quot.sound |

No `sorry`, no extra axioms. `k1_C` and `k1_D` use OpenAI's proved theorems, which are sorry-free, so the standard axioms above are the whole trust base apart from the named hypotheses.

## What K1 does and does not establish

`k1_C : ∀ ν, 0 < ν → AltC ν` and `k1_D : ∀ ν, 0 < ν → AltD_withErratum ν` have **no hypotheses**. They start from OpenAI's internal theorems (`NavierStokesR3.theorem_1_1`, `PeriodicPaper.periodic_corollary`), whose witness is u₀ = 0 and a force smooth on all of ℝ × ℝ³, and they use only `propext`, `Classical.choice` and `Quot.sound`.

**Smoothness at t = 0 does not decide the result.** `ClayLiteral` renders C^∞(ℝ³ × [0, ∞)) in two ways, as the restriction of a C^∞ function (`SmoothUpToBoundary`) and as derivatives of every order continuous up to t = 0 (`SmoothOneSided`), and K1 is proved under both: `k1_C_oneSided`, `k1_D_oneSided`. **(C) does not use the erratum;** the periodic-pressure question (S7) affects (D) only.

The result is relative to `ClayLiteral`'s fidelity to the PDF, which no independent person has reviewed; the points to check are in [`K0_REVIEW.md`](K0_REVIEW.md). (D) without the erratum on solutions is not proved (row S7). `zero_solution_C` and `zero_solution_D` check that ClayLiteral's solution conditions are satisfiable, so "no solution exists" is not vacuous.

**How D4 closed.** Reading C^∞(ℝ³ × [0, ∞)) as a restriction makes S4 immediate but requires a smooth extension of the force (D4). No general extension theorem was used: OpenAI's own construction proves the force smooth on all of ℝ × ℝ³, so it is its own extension.

All theorems, checked with `#print axioms` on Lean 4.34.0-rc2: `k1_C`, `k1_D`, `k1_C_oneSided`, `k1_D_oneSided`, `witness_C`, `witness_D`, `d1_zero`, `d2_zero`, `d3_zero`, `d5`, `d6`, `d7`, `s1`–`s6`, `s7_formal_side`, `p1`, `clay_bound`, `zero_solution_C`, `zero_solution_D`: `[propext, Classical.choice, Quot.sound]`. `Bridges.lean` contains no `sorry`.
