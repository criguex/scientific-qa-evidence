# Request for review: receipt-to-artifact checks

This page asks for review of one narrow result about the **traceability of evidence** in a reproducible Lean verification workflow. It is not about the mathematics: OpenAI's proof was accepted in every run.

## The result

On the same authentic files (a from-source build of [openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler) at `f9e8bc5`, Lean 4.34.0-rc2, the pinned Comparator `19e111e`), OpenAI's published procedure (`lake exe cache get`, `lake build`, `lake exe comparator ComparatorChallenges/NavierStokes.json`) was recorded step by step. Then only the evidence bundle was altered:

| Variant | Published procedure | Existence check P6 | Hash check |
| --- | --- | --- | --- |
| Clean | exit 0, `Your solution is okay!` | pass | pass |
| A receipt names a log that is not in the bundle | exit 0, output byte-identical to the clean run | flags | flags |
| A stale log from another run, under the right name | exit 0, output byte-identical to the missing-log run | **passes: does not detect it** | flags |

Byte-identical means: in case 1, the clean and missing-log runs; in case 2, the missing-log and stale-log runs, which also match case 1. Case 2's clean run has 13 extra `Built …` lines, because its first Comparator call in a fresh copy also built the Comparator executable.

**Conclusion.** In this experiment, P6 detects a traceability inconsistency that does not change Comparator's result, and a stale log under the right name is caught only by comparing it with the hash recorded when the step ran. This supports the added value of hash-bound receipts for the traceability of evidence. **It does not mean Comparator accepted a false proof.**

Both cases were pre-registered before running, with an aborted first attempt and one amendment recorded: [case 1](../experiments/receipt-check/RESULTS.md), [case 2](../experiments/receipt-check/RESULTS2.md), [status](../experiments/receipt-check/STATUS.md).

## Reproduce

- **About a minute, no Lean:** `cd experiments/receipt-check && python3 -m unittest -v test_results` recomputes both checks from the published bundles and checks that the procedure's output did not change.
- **Full rerun:** `QA_COMMIT=<commit> bash run.sh` and `run2.sh`. As written they run under WSL on a Windows host: they measure the Windows system drive with PowerShell and use that host's local paths for the build tree and the tools. On another machine those lines of [`preflight.sh`](../experiments/receipt-check/preflight.sh) must be adapted; it also checks the toolchain, the `lake-manifest.json` revisions and the tool hashes, and aborts on any mismatch or lack of space.

## The question

**Does binding each receipt to the hash of the artifact it names add a useful traceability guarantee to a reproducible verification workflow, or is it redundant with what Lake and Comparator already ensure?**

## Objections already known

- The published procedure does not claim to check receipts, so "it does not detect it" is expected. The point is that the published verifier does not by itself check that a receipt corresponds to the log it references, and a cheap check closes that gap.
- P6, this study's own check, only tests that a named log exists; case 2 shows it misses a substituted log, and that a second check catches it. Documenting where the study's own check fails is part of the result.
- The hash check detects a change relative to a trusted reference value, here the hash recorded when the step ran. It does not authenticate where a log came from if someone can replace both the file and that recorded value.
- Two cases on one host, designed by the author. No detection rate is claimed.

## Status of the review

Requested from: the outside reviewer who suggested the comparison. Not yet sent to anyone else. Replies, and who gave them, will be recorded here.
