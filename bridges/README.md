# Bridges: Clay's text in Lean, and lemmas linking it to the formal statement

Work for the semantic plan in [`evidence/formal/clay-lean-bridges.md`](../evidence/formal/clay-lean-bridges.md).

| File | Content |
| --- | --- |
| [`ClayLiteral.lean`](ClayLiteral.lean) | Row K0: Clay's equations (1)–(11), alternatives (C) and (D) and the erratum, written literally (coordinates, partial derivatives along basis vectors, one-sided time derivatives, Lebesgue integral). Definitions only, plus one sanity theorem. **Awaiting review against the PDF.** |
| [`Bridges.lean`](Bridges.lean) | Lemmas between OpenAI's statement and `ClayLiteral`, and the conditional composition K1. It imports OpenAI's solution module, so K1 starts from OpenAI's proved theorems. |

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
| `ClayLiteral.lean` SHA-256 | `f5dd67fc765eca76029b88515381e3288083e53d1724e3ef804715f5dda06f78` |
| `Bridges.lean` SHA-256 | `4060b88671e959b3e8e1840693786c7ce9cd377fdb44da7c01fc5d5057e669c0` |
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
| `Bridges.k1_C` | K1 for (C), conditional | propext, Classical.choice, Quot.sound |
| `Bridges.k1_D` | K1 for (D), conditional | propext, Classical.choice, Quot.sound |
| `Bridges.s7_formal_side` | S7 (formal side only) | propext, Classical.choice, Quot.sound |
| `ClayLiteral.altD_withoutErratum_imp_withErratum` | sanity | propext, Classical.choice, Quot.sound |

No `sorry`, no extra axioms. `k1_C` and `k1_D` use OpenAI's proved theorems, which are sorry-free, so the standard axioms above are the whole trust base apart from the named hypotheses.

## What K1 does and does not establish

`k1_C` proves: *if* the bridges D1, D2, D3, D4, D5, S1, S2 and S5 hold, *then* OpenAI's theorem implies Clay's (C) as written in `ClayLiteral`. `k1_D` does the same for (D), with the erratum read as a condition on solutions, from D1, D2, D4, D7, S1 and S2. Each assumption is a named hypothesis in the Lean statement, so nothing is hidden. The implication is **conditional** until each hypothesis is proved, and it is only as faithful as `ClayLiteral`, which still needs independent review against the PDF.

**Where the difficulty sits.** Reading C^∞(ℝ³ × [0, ∞)) as the restriction of a C^∞ function makes S4 immediate (`Bridges.s4`) but makes D4 require an extension of OpenAI's force to all of ℝ³ × ℝ. Either an extension theorem or a check that OpenAI's concrete forces are globally smooth would close D4. The other reading would reverse which side needs the extension.

## Reproduce

From an extracted and built `openai/NavierStokesAndEuler` at `f9e8bc5` (see [`REPRODUCE.md`](../REPRODUCE.md)):

```sh
cd bridges && echo leanprover/lean4:v4.34.0-rc2 > lean-toolchain
LP="$(cd <OpenAI-project> && lake env printenv LEAN_PATH):$PWD"
LEAN_PATH="$LP" lean --root=. -o ClayLiteral.olean ClayLiteral.lean
LEAN_PATH="$LP" lean --root=. -o Bridges.olean Bridges.lean
```
