# Request for review: receipt-to-artifact checks

This page asks for review of one narrow result about the **traceability of evidence** in a reproducible Lean verification workflow. It is not about the mathematics: OpenAI's proof was accepted in every run.

## The result

On the same authentic files (a from-source build of [openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler) at `f9e8bc5`, Lean 4.34.0-rc2, the pinned Comparator `19e111e`), OpenAI's published procedure (`lake exe cache get`, `lake build`, `lake exe comparator ComparatorChallenges/NavierStokes.json`) was recorded step by step. Then only the evidence bundle was altered:

| Variant | Published procedure | Existence check P6 | Hash check |
| --- | --- | --- | --- |
| Clean | exit 0, `Your solution is okay!` | pass | pass |
| A receipt names a log that is not in the bundle | exit 0, byte-identical output | flags | flags |
| A stale log from another run, under the right name | exit 0, byte-identical output | **passes: does not detect it** | flags |

**Conclusion.** In this experiment, P6 detects a traceability inconsistency that does not change Comparator's result, and a stale log under the right name is caught only by comparing it with the hash recorded when the step ran. This supports the added value of hash-bound receipts for the traceability of evidence. **It does not mean Comparator accepted a false proof.**

Both cases were pre-registered before running, with an aborted first attempt and one amendment recorded: [case 1](../experiments/receipt-check/RESULTS.md), [case 2](../experiments/receipt-check/RESULTS2.md), [status](../experiments/receipt-check/STATUS.md).

## Reproduce

- **About a minute, no Lean:** `cd experiments/receipt-check && python3 -m unittest -v test_results` recomputes both checks from the published bundles and checks that the procedure's output did not change.
- **Full rerun, Linux with a built tree:** `QA_COMMIT=<commit> bash run.sh` and `run2.sh`; [`preflight.sh`](../experiments/receipt-check/preflight.sh) checks the toolchain, the `lake-manifest.json` revisions and the tool hashes, and aborts on any mismatch or lack of space.

## The question

**Does binding each receipt to the hash of the artifact it names add a useful traceability guarantee to a reproducible verification workflow, or is it redundant with what Lake and Comparator already ensure?**

## Objections already known

- The published procedure does not claim to check receipts, so "it does not detect it" is expected. The point is that the workflow, as published, leaves no verifiable record of what was run, and a cheap check closes that gap.
- P6, this study's own check, only tests that a named log exists; case 2 shows it misses a substituted log.
- Two cases on one host, designed by the author. No detection rate is claimed.

## Status of the review

Requested from: the outside reviewer who suggested the comparison. Not yet sent to anyone else. Replies, and who gave them, will be recorded here.
