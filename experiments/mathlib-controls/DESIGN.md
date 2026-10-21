# Mathlib controls: does the pipeline tell "the statement changed" from "the theorem is false"?

**Pre-registered on 2026-10-21, before any case was run.** The cases, the statements in [`lean/QAControls/Challenge/`](lean/QAControls/Challenge/), the proofs in [`lean/QAControls/Solution/`](lean/QAControls/Solution/) and the expected outcomes in [`expected.json`](expected.json) are fixed in the commit that adds this file. Results are added in later commits and compared against it.

> **Amendment 1 (2026-10-21, after an outside review and before any case was run).** The original registration is commit `046a128`. Changes: (1) *SAME* is renamed **ACCEPTED_BY_CHECKER**, because a Comparator acceptance means the statements agree as Comparator checks them, which need not be textual identity and is not a separately proved mathematical equivalence; a new case, `primes/defeq`, probes exactly that. (2) **CHANGED_WEAKER** now requires two proofs: original ⇒ changed, and that changed does not imply original in the evaluated schema; non-implication alone could also mean a stronger or incomparable statement, and gives **CHANGED_NOT_EQUIVALENT**. (3) The `dct/reform` equivalence must use that the domination hypothesis makes the bound nonnegative almost everywhere; a control shows the isolated alternative condition is not equivalent to integrability for a function that takes negative values.

## Why

A statement comparator such as Comparator answers one question: *is the submitted theorem exactly the challenge statement?* A refusal does not say the changed statement is false, and it can refuse a reformulation that is mathematically equivalent. This experiment uses three theorems that Mathlib already proves, so that every outcome can be checked, and asks whether the protocol separates four situations:

- Comparator accepts the statement (**ACCEPTED_BY_CHECKER**), which is equality as the checker sees it, not a proof of anything else;
- the statement changed but is equivalent, proved separately (**CHANGED_EQUIVALENT**);
- the statement changed into something weaker, for example a version limited to examples: original ⇒ changed is proved, and changed ⇏ original is shown in the schema (**CHANGED_WEAKER**);
- the statement changed and is shown not to imply the original, without the converse (**CHANGED_NOT_EQUIVALENT**);
- the statement changed into something false (**CHANGED_FALSE**).

## Theorems and cases

| Theorem | Correct | Equivalent reformulation | Deliberate error |
| --- | --- | --- | --- |
| Infinitude of primes | `∀ n, ∃ p, n < p ∧ p.Prime` | `n ≤ p` instead of `n < p`; and `n + 1 ≤ p`, which is definitionally `n < p` (`primes/defeq`) | **Limited to examples:** `∀ n ≤ 100, …` (true, but weaker). **Quantifier swap:** `∃ p, ∀ n, n < p ∧ p.Prime` (false) |
| Cauchy–Schwarz | `abs ⟪x, y⟫ ≤ ‖x‖ ‖y‖` | `⟪x, y⟫² ≤ ‖x‖² ‖y‖²` | `<` instead of `≤`: false for two equal non-zero vectors |
| Dominated convergence | Mathlib's hypotheses | `Integrable bound` written as measurable with finite Lebesgue integral of `ofReal bound`; equivalent only because domination forces `bound ≥ 0` a.e. | **Domination removed:** false; `f_n = (n+1)` on `(0, 1/(n+1))` and 0 elsewhere tends to 0 pointwise, but every integral is 1 |

Each changed statement replaces the challenge; OpenAI-style, the proof is never touched. Eleven Comparator runs in total.

## Procedure

1. **Comparator** (pinned `19e111e`, with nanoda and the Lean kernel, same toolchain and Mathlib as the main audit) checks each case: correct proof against the possibly changed challenge.
2. **Second route**, only for refused cases, in plain Lean, separate from Comparator:
   - *equivalence*: prove `changed ↔ original` (for primes, as a schema over every predicate `P`, so that it cannot hold just because both sides are true);
   - *weaker*: prove original ⇒ changed as a schema, **and** exhibit a predicate for which the changed form holds and the original fails;
   - *refutation*: prove `¬ changed`.
3. **Guard**: an equivalence counts only if a check over the transitive dependencies of its proof finds no use of the theorem under test (`Nat.exists_infinite_primes`, the Cauchy–Schwarz lemmas, `tendsto_integral_of_dominated_convergence`). Without this, any two true statements would be "equivalent".
4. **Classification rule**: accepted → ACCEPTED_BY_CHECKER (an equivalence may still be proved separately and is reported next to it); refused and equivalence passes the guard → CHANGED_EQUIVALENT; refused and refutation builds → CHANGED_FALSE; refused, original ⇒ changed builds and schema non-implication builds → CHANGED_WEAKER; refused and only the non-implication builds → CHANGED_NOT_EQUIVALENT; otherwise → CHANGED_UNKNOWN.

**Controls:** an equivalence proof for `primes/reform` that cheats by using `Nat.exists_infinite_primes` must be rejected by the guard; and for `g = -1` on ℝ, measurable with `∫⁻ ofReal g = 0 < ∞` but not integrable, a refutation must build, showing the DCT reformulation needs the nonnegativity that domination provides.

## Expected outcomes

| Case | Comparator | Second route | Class |
| --- | --- | --- | --- |
| primes/orig | accept | — | ACCEPTED_BY_CHECKER |
| primes/defeq | reject if Comparator compares expressions structurally; acceptance is reported as a finding | equivalence | CHANGED_EQUIVALENT, or ACCEPTED_BY_CHECKER |
| primes/reform | reject | equivalence | CHANGED_EQUIVALENT |
| primes/bounded | reject | original ⇒ changed, and schema non-implication | CHANGED_WEAKER |
| primes/swap | reject | refutation | CHANGED_FALSE |
| cs/orig | accept | — | ACCEPTED_BY_CHECKER |
| cs/reform | reject | equivalence | CHANGED_EQUIVALENT |
| cs/strict | reject | refutation | CHANGED_FALSE |
| dct/orig | accept | — | ACCEPTED_BY_CHECKER |
| dct/reform | reject | equivalence | CHANGED_EQUIVALENT |
| dct/nodom | reject | refutation | CHANGED_FALSE |

If Comparator accepts a reformulation, that is itself a finding (it would compare statements up to more than syntax) and is reported as such, not hidden.

## Limits, stated in advance

- The author designed every case, and the second-route proofs are written after this registration by the same author and assistant, so a case could fail through a bug in a second-route proof rather than in the protocol; such failures are reported, not retried silently.
- **Held-out cases from someone else are still needed.** Cases prepared by a person who has not seen the evaluator would test it without tuning to the author's choices. The template is in [`HOLDOUT.md`](HOLDOUT.md); none have been received yet.
- Eleven cases on three theorems give no detection rate.
