# Bridges: Clay's text in Lean, and lemmas linking it to the formal statement

Work for the semantic plan in [`evidence/formal/clay-lean-bridges.md`](../evidence/formal/clay-lean-bridges.md).

| File | Content |
| --- | --- |
| [`ClayLiteral.lean`](ClayLiteral.lean) | Row K0: Clay's equations (1)–(11), alternatives (C) and (D) and the erratum, written literally (coordinates, partial derivatives along basis vectors, one-sided time derivatives, Lebesgue integral). Definitions only, plus one sanity theorem. **Awaiting review against the PDF.** |
| [`Bridges.lean`](Bridges.lean) | Lemmas between OpenAI's challenge statement (`ComparatorChallenges.NavierStokes`) and `ClayLiteral`. |

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
| `Bridges.lean` SHA-256 | `bdadf3fa7dd0baeba81e3aeb45de0d5f27e69d6a9ac5dd213dac7b061376e6e9` |
| `ClayLiteral.lean` | typechecks, exit 0 |
| `Bridges.lean` | typechecks, exit 0 |

`#print axioms` for every theorem proved so far:

| Theorem | Row | Axioms |
| --- | --- | --- |
| `Bridges.d6` | D6 | propext, Classical.choice, Quot.sound |
| `Bridges.s3` | S3 | propext, Classical.choice, Quot.sound |
| `Bridges.s6` | S6 | propext, Classical.choice, Quot.sound |
| `Bridges.p1` | P1 | propext, Classical.choice, Quot.sound |
| `Bridges.s7_formal_side` | S7 (formal side only) | propext, Classical.choice, Quot.sound |
| `ClayLiteral.altD_withoutErratum_imp_withErratum` | sanity | propext, Classical.choice, Quot.sound |

No `sorry`, no extra axioms. These rows are the definitional ones; they establish that the two formalizations line up where they should, not any deep fact.

## Reproduce

From an extracted and built `openai/NavierStokesAndEuler` at `f9e8bc5` (see [`REPRODUCE.md`](../REPRODUCE.md)):

```sh
cd bridges && echo leanprover/lean4:v4.34.0-rc2 > lean-toolchain
LP="$(cd <OpenAI-project> && lake env printenv LEAN_PATH):$PWD"
LEAN_PATH="$LP" lean --root=. -o ClayLiteral.olean ClayLiteral.lean
LEAN_PATH="$LP" lean --root=. -o Bridges.olean Bridges.lean
```
