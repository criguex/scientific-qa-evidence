# One concrete comparison: receipt-to-log correspondence on authentic records

**Pre-registered on 2026-10-22, before any run.** The expected outcomes are in [`expected.json`](expected.json), and the scripts are [`run.sh`](run.sh) and [`check_p6.py`](check_p6.py).

## Question

Does this study's check **P6**, the correspondence between receipts and logs, detect a fault that OpenAI's published verification procedure does not, when both are run on exactly the same authentic files?

The blind-fault benchmark (case C/F5) showed this on synthetic records, with a Python model of the baseline. Here the baseline is the real procedure, run for real.

## Setup

- **Files:** a copy of a from-source build tree of `openai/NavierStokesAndEuler` at `f9e8bc5` (B5 as registered; B4 after amendment 1, see [STATUS](STATUS.md)), the same Lean 4.34.0-rc2 toolchain, and the same Comparator, lean4export, nanoda and landrun binaries.
- **Procedure Z**, exactly as OpenAI publishes it, with the three tools on `PATH`: `lake exe cache get`, `lake build`, `lake exe comparator ComparatorChallenges/NavierStokes.json`.
- **Evidence bundle:** a thin wrapper records each step of Z as `receipt.tsv` (step, command, log, exit code), with the logs next to it, in the format P6 reads.
- **Check X:** P6 from [`protocol_lib_v2.py`](../blind-faults/v2/protocol_lib_v2.py), unchanged since evaluator v2.2. `check_p6.py` calls `protocol()` and reports only the P6 flags.

## Variants, on the same files

| Variant | Change | Expected Z | Expected X |
| --- | --- | --- | --- |
| C, clean control | none | exit 0, `Your solution is okay!` | exit 0, no P6 flag |
| F5, known fault | the `comparator` row of `receipt.tsv` names `comparator-run.log`, a log that does not exist; nothing else changes | exit 0, `Your solution is okay!` | exit 1, `P6:receipt-log-missing-comparator-run.log` |

For each variant the bundle is placed in the project tree, Z's Comparator step is run again, and X is run on the bundle. Every step is recorded with its command, the SHA-256 of its sanitized log and its exit code.

## The claim this can support, if it comes out as expected

> In this case, the receipt-to-log correspondence check (P6) detected a receipt naming a log that is not in the evidence, and OpenAI's published procedure, run on the same files, did not: it exited 0, because it does not read receipts.

That is a narrow claim about the **traceability of the evidence**, not about the proof. It does not say P6 catches every error, that the procedure is deficient at its own job (checking the proof), or anything about the Millennium Prize. If both detect the same thing, or neither does, this case shows no added value, and that will be reported.

**The question for reviewers:** does a check that receipts correspond to the artifacts they name add a useful traceability guarantee to a reproducible verification workflow?
