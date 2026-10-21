# Mathlib controls: results

Run on 2026-10-21 on the same Linux host and with the same checker binaries as the main audit (Comparator `19e111e` with nanoda and the Lean kernel, Lean 4.34.0-rc2, Mathlib `85e3a25`; hashes in [`results/tools.sha256`](results/tools.sha256), identical to [`tools.tsv`](../../evidence/formal/cd-validation/receipts/tools.tsv)). Every step has a receipt in [`results/receipts.jsonl`](results/receipts.jsonl): the command, the SHA-256 of each input file (identical to the files in [`lean/`](lean/), including the registered statements), the SHA-256 of its sanitized stdout and stderr, and its exit code. Design and expectations: [`DESIGN.md`](DESIGN.md), registered in commit `046a128` and amended once before any run (`c1c6a0b`).

**All 11 cases and both controls came out as registered.** `python3 experiments/mathlib-controls/verify.py` checks every log and input against its receipt, requires exit code 0 for each second route, and recomputes the classes; CI runs it and its tests on every push. **It checks the published records; it is not an independent rerun of the theorems.**

**Record history.** The first run (commit `ac195f7`) kept no exit codes for the second routes, and its verifier missed Lean's real sorry warning, which uses backticks. Both were found by an outside reviewer. The steps were rerun with receipts on the same day, with the same verdicts; the first run's logs remain in the git history. `test_verify.py` now covers the backtick warning, an empty log with and without exit code 0, a missing receipt, and tampered logs and inputs.

| Case | Comparator | Second route | Class | As registered |
| --- | --- | --- | --- | --- |
| primes/orig | accepted, both kernels | — | ACCEPTED_BY_CHECKER | yes |
| primes/defeq | refused: `statement do not match` | equivalence, `Iff.rfl` (definitional) | CHANGED_EQUIVALENT | yes |
| primes/reform | refused | equivalence as a schema over every `P`, guard passed | CHANGED_EQUIVALENT | yes |
| primes/bounded | refused | original ⇒ changed, and a predicate where changed holds but original fails | CHANGED_WEAKER | yes |
| primes/swap | refused | refutation: `¬ ∃ p, ∀ n, n < p ∧ …` | CHANGED_FALSE | yes |
| cs/orig | accepted, both kernels | — | ACCEPTED_BY_CHECKER | yes |
| cs/reform | refused | equivalence through `abs a ≤ bc ↔ a² ≤ b²c²` for b, c ≥ 0, guard passed | CHANGED_EQUIVALENT | yes |
| cs/strict | refused | refutation with x = y = 1 in ℝ | CHANGED_FALSE | yes |
| dct/orig | accepted, both kernels | — | ACCEPTED_BY_CHECKER | yes |
| dct/reform | refused | equivalence using that domination makes the bound nonnegative a.e., guard passed | CHANGED_EQUIVALENT | yes |
| dct/nodom | refused | refutation: `(n+1)·1_(0, 1/(n+1))` tends to 0 pointwise, every integral is 1 | CHANGED_FALSE | yes |

| Control | Result |
| --- | --- |
| Cheating equivalence for primes/reform that uses `Nat.exists_infinite_primes` | **rejected by the guard**: `depends on Nat.exists_infinite_primes` |
| `g = -1` on ℝ: measurable, `∫⁻ ofReal g = 0 < ∞`, not integrable | refutation builds, so the DCT reformulation is only equivalent under domination |

## What this shows

1. **Comparator's refusal means "the statement changed", nothing more.** It refused all eight changes, including three equivalent ones and one weaker but true one. Telling them apart took a separate Lean proof each time.
2. **Comparator compares statements structurally.** It refused `n + 1 ≤ p`, which Lean reduces to `n < p` by definition (`Iff.rfl`). So an acceptance is equality as Comparator checks it, and a mathematical equivalence has to be proved separately.
3. **The guard matters.** Without it, any two true statements are "equivalent". It caught the deliberately cheating proof.
4. **A version limited to examples is not the theorem.** `∀ n ≤ 100` holds, is implied by the full statement, and does not imply it as a schema.

## Limits

The author chose every case and wrote the second-route proofs after registration, together with the assistant. The run is small (three theorems, eleven cases) and gives no detection rate. Held-out cases from someone else are still missing ([`HOLDOUT.md`](HOLDOUT.md)). Logs are sanitized only to replace host paths with `<path>`, and the receipt hashes are of the sanitized files; each Comparator run took 17–45 s.
