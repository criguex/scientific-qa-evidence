# What the protocol found that the documented procedure does not show

The useful question for this study is not whether its techniques are new; [RELATED_WORK.md](docs/RELATED_WORK.md) shows they are not. The question is: **what could this protocol detect, in this case, that the previously documented procedure could not?**

**Baseline.** The verification procedure documented in OpenAI's repository at `f9e8bc5`: fetch the Mathlib cache with `lake exe cache get`, run `lake build`, then check the formalizations with Comparator as described in `ComparatorChallenges/README.md`.

**Scope.** This is a retrospective record of one case. It shows that the protocol produced evidence the baseline does not produce. It does not measure how often, at what cost, or with how many false alarms. That needs the prospective experiment described at the end.

## Findings

| # | Finding | Protocol element that caught it | Does the baseline produce this evidence? | Evidence |
| --- | --- | --- | --- | --- |
| 1 | A build believed to be clean (B3) had silently received 7 dependencies as prebuilt Reservoir archives; the build log did not show it | Artifact check: `.olean` timestamps against the build start, plus inspection of `.lake/packages` | No. The baseline downloads prebuilt Mathlib on purpose and never asks what was compiled locally. | [cd-validation](evidence/formal/cd-validation/README.md#b3--fresh-build-2026-10-21) |
| 2 | A full from-source build (B4) is possible and was verified: every `.olean` newer than the build start, no archives fetched | `lake --no-cache build` with an isolated cache, plus the same artifact check | No. The baseline uses the Mathlib cache. | [cd-validation](evidence/formal/cd-validation/README.md#b4--no-cache-build-2026-10-21) |
| 3 | Two runs reported as using "the same build" had used different builds | Per-run receipts and original hashes, labeled by build | No. The baseline has no run records. | [builds table](evidence/formal/cd-validation/README.md#builds-used-by-each-run) |
| 4 | Comparator refuses every one-symbol change to the statement and accepts a comment-only change | Statement mutants with a negative control | No. The baseline only shows a positive result, which by itself cannot distinguish an exact check from a permissive one. | [mutants](evidence/formal/cd-validation/mutants/) |
| 5 | The challenge statement's 18 declarations match DeepMind's public statement after textual normalization | Statement provenance comparison | No. The baseline checks the proof against the challenge, not the challenge against a public source. | [statement provenance](evidence/formal/statement-provenance/README.md) |
| 6 | The kernel source used includes every 2026 kernel soundness fix, and nanoda postdates its fix | Kernel currency check | No. The baseline does not record or check checker versions against known bugs. | [kernel currency](evidence/formal/kernel-currency.md) |
| 7 | Periodic pressure in (D) rests on reading Clay's erratum as a solution condition | Clause-by-clause risk review by direction of risk | No. Comparator compares against the challenge, not against Clay's text. | [Clay risk review](evidence/formal/clay-lean-risk.md) |
| 8 | The numerical runner reported `oracle_valid: true` when the oracle had raised an exception or returned NaN | Testing the test harness: injected oracle and simulator failures | Not applicable to the formal baseline. It shows the protocol checks its own tooling. | [test_runner.py](evidence/numerical/source/test_runner.py) |
| 9 | Three of the seven published mutant diffs (`domain_R3_to_periodic_data`, `force_zero_R3`, `force_zero_periodic`) do not apply as published: each lacks its last line, a context line made of a single space, so `git apply` stops with `corrupt patch`. With that line restored, each file's SHA-256 equals the original recorded in `PROVENANCE.md`, so the original runs used complete diffs and the line was lost when the public copies were made | Rerunning the mutants from the published files in the version-port campaign (2026-11-24), checked against the original hashes in `PROVENANCE.md` | No. The baseline has no statement mutants and no record of the hashes of its inputs. | [version port](experiments/version-port/RESULTS.md#findings-about-the-published-evidence), [restored copies](experiments/version-port/R0/diffs/) |

Findings 1, 3, 8 and 9 were defects in this study's own earlier work, caught by later steps of the same protocol before or after publication and disclosed in the open. Findings 1, 3 and 8 were corrected. For finding 9 the published diffs were left unchanged, because editing them would change the data version and its fingerprint; the restored copies and their hashes are published next to the run that used them. They are listed because an audit that can catch its own errors is part of what the protocol offers.

## What this does not show

- It does not show that the baseline is wrong. OpenAI's procedure answers a narrower question, whether the proofs check, and it answers it.
- It does not show that the protocol finds problems more often than other procedures. One case is not a rate.
- None of these findings is a defect in OpenAI's proofs. Finding 7 is an interpretive point for mathematicians, not an error.

## How to demonstrate the difference

A prospective experiment, defined and frozen before it is run:

1. **Fault classes** taken from the findings above: hidden prebuilt artifacts, mislabeled builds, a changed or weakened statement, a statement that does not match its public source, a checker version with a known soundness bug, and a test harness that reports success on failure.
2. **Blind injection.** Someone other than the person running the checks plants faults in copies of small Lean projects and numerical cases, with clean copies mixed in as controls.
3. **Both procedures on every copy:** the baseline and the protocol.
4. **Metrics:** faults detected, false alarms on clean copies, and wall-clock cost.

A result of that experiment, not this table, would support a claim that the protocol detects classes of problems the baseline does not.

**Result (2026-10-21), after review.** Read as a deterministic regression benchmark: with the corrected v2 evaluator, the protocol's checks flag fault classes F1, F2, F4 and F5 where the baseline passes, both flag the positive control, and the complete clean template passes both. The first (v1) run is kept with errata: its evaluator had defects, its "0 false alarms" does not hold, and F2 is a textual difference rather than a weakened statement. Records: [v2](experiments/blind-faults/v2/README.md) and [v1 with errata](experiments/blind-faults/RESULTS.md). Its preparation is tracked in [experiments/blind-faults/STATUS.md](experiments/blind-faults/STATUS.md).
