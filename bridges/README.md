# Bridges: Clay's text in Lean, and lemmas linking it to the formal statement

Work for the semantic plan in [`evidence/formal/clay-lean-bridges.md`](../evidence/formal/clay-lean-bridges.md).

| File | Content |
| --- | --- |
| [`ClayLiteral.lean`](ClayLiteral.lean) | Row K0: Clay's equations (1)–(11), alternatives (C) and (D) and the erratum, written literally (coordinates, partial derivatives along basis vectors, one-sided time derivatives, Lebesgue integral). Definitions only, plus one sanity theorem. **Awaiting review against the PDF.** |
| [`Bridges.lean`](Bridges.lean) | Lemmas between OpenAI's statement and `ClayLiteral`, and the composition K1. It imports OpenAI's solution module, so K1 starts from OpenAI's proved theorems. |

## Readings chosen in ClayLiteral (to be reviewed)

| Reading | Choice made | How K1 handles it |
| --- | --- | --- |
| C^∞(ℝ³ × [0, ∞)), rows D4 and S4 | Two renderings: restriction of a C^∞ function on ℝ³ × ℝ (`SmoothUpToBoundary`), and derivatives of every order continuous up to t = 0 (`SmoothOneSided`, Mathlib's `ContDiffOn`) | Proved under both (`k1_*` and `k1_*_oneSided`); whether either is Clay's meaning is review point 1 in [`K0_REVIEW.md`](K0_REVIEW.md) |
| The erratum, row S7 | (D) stated both with and without periodic pressure on solutions | K1 proves the version with the erratum on solutions; the other is open |
| Exponent K in (4), (5), (9) | Ranges over the reals | A stronger requirement on data than natural K, so the data side is not weakened |
| Multi-index α | A list of directions, so order and repetition are explicit | For smooth functions the order of partials does not matter |

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

`#print axioms` was run on every theorem in `Bridges.lean` and on the sanity theorem in `ClayLiteral.lean`; each depends only on `propext`, `Classical.choice` and `Quot.sound`. The theorems are `p1`, `d1_zero`, `d2_zero`, `d3_zero`, `witness_C`, `witness_D`, `d5`, `d6`, `d7`, `clay_bound`, `s1`–`s6`, `s7_formal_side`, `k1_C`, `k1_D`, `k1_C_oneSided`, `k1_D_oneSided`, `zero_solution_C`, `zero_solution_D` and `ClayLiteral.altD_withoutErratum_imp_withErratum`. The same check was repeated from a fresh clone ([FROM_ZERO](../evidence/FROM_ZERO.md)) and against build B5 ([axioms log](../evidence/formal/b5/axioms.log)).

No `sorry`, no extra axioms, and no hypotheses in the K1 theorems. They use OpenAI's proved theorems, which are sorry-free, so the three standard axioms are the whole trust base, together with the fidelity of `ClayLiteral` to the PDF.

## What K1 does and does not establish

`k1_C : ∀ ν, 0 < ν → AltC ν` and `k1_D : ∀ ν, 0 < ν → AltD_withErratum ν` have **no hypotheses**. They start from OpenAI's internal theorems (`NavierStokesR3.theorem_1_1`, `PeriodicPaper.periodic_corollary`), whose witness is u₀ = 0 and a force smooth on all of ℝ × ℝ³, and they use only `propext`, `Classical.choice` and `Quot.sound`.

**Smoothness at t = 0 does not decide the result, between these two definitions.** `ClayLiteral` renders C^∞(ℝ³ × [0, ∞)) in two ways, as the restriction of a C^∞ function (`SmoothUpToBoundary`) and as derivatives of every order continuous up to t = 0 (`SmoothOneSided`), and K1 is proved under both: `k1_C_oneSided`, `k1_D_oneSided`. `SmoothOneSided` is defined as Mathlib's `ContDiffOn` on the closed half-space; whether that, or the restriction reading, is what Clay means is review point 1 in [`K0_REVIEW.md`](K0_REVIEW.md), and the names prove nothing by themselves. **(C) does not use the erratum;** the periodic-pressure question (S7) affects (D) only.

The result is relative to `ClayLiteral`'s fidelity to the PDF, which no independent person has reviewed; the points to check are in [`K0_REVIEW.md`](K0_REVIEW.md). (D) without the erratum on solutions is not proved (row S7). `zero_solution_C` and `zero_solution_D` check that ClayLiteral's solution conditions are satisfiable, so "no solution exists" is not vacuous.

**How D4 closed.** Reading C^∞(ℝ³ × [0, ∞)) as a restriction makes S4 immediate but requires a smooth extension of the force (D4). No general extension theorem was used: OpenAI's own construction proves the force smooth on all of ℝ × ℝ³, so it is its own extension.

All theorems, checked with `#print axioms` on Lean 4.34.0-rc2: `k1_C`, `k1_D`, `k1_C_oneSided`, `k1_D_oneSided`, `witness_C`, `witness_D`, `d1_zero`, `d2_zero`, `d3_zero`, `d5`, `d6`, `d7`, `s1`–`s6`, `s7_formal_side`, `p1`, `clay_bound`, `zero_solution_C`, `zero_solution_D`: `[propext, Classical.choice, Quot.sound]`. `Bridges.lean` contains no `sorry`.
