# Results: receipt-to-log correspondence on authentic records

Run on 2026-10-22, after the [pre-registration](DESIGN.md) (`8478f68`) and [amendment 1](STATUS.md) (`db1da97`), on a copy of build B4's tree of `openai/NavierStokesAndEuler` at `f9e8bc5`. Lean 4.34.0-rc2 (`6a10ac8`), Lake 5.0.0; `lake exe comparator` built the same Comparator binary used in the audit (SHA-256 `514de8d2…`, as in [`tools.tsv`](../../evidence/formal/cd-validation/receipts/tools.tsv)); landrun, lean4export and nanoda by the hashes in [`versions.txt`](results/versions.txt).

**Both variants came out exactly as registered.**

| Variant | What changed | OpenAI's published procedure (Z) | Check P6 (X) |
| --- | --- | --- | --- |
| C, clean control | nothing | exit 0, `Your solution is okay!` | exit 0, no flag |
| F5, known fault | one receipt row names `comparator-run.log` instead of `comparator.log` | exit 0, `Your solution is okay!`; output byte-identical to C | **exit 1**, `P6:receipt-log-missing-comparator-run.log` |

| Step of Z, recorded in the bundle | Command | Exit |
| --- | --- | --- |
| cache | `lake exe cache get` | 0 |
| build | `lake build` | 0 |
| comparator | `lake exe comparator ComparatorChallenges/NavierStokes.json` | 0 (both kernels accept) |

Every step's command, the SHA-256 of its sanitized log, its exit code and its times are in [`results/receipts.jsonl`](results/receipts.jsonl); the bundles are [`results/C/`](results/C/) and [`results/F5/`](results/F5/), which differ only in that receipt row ([`F5.receipt.diff`](results/F5.receipt.diff)).

## The claim

> **In this case, the receipt-to-log correspondence check (P6) detected a receipt naming a log that is not in the evidence bundle, and OpenAI's published procedure, run on the same files, did not: it exited 0 with the same output, because it does not read receipts.**

This is about the traceability of the evidence, not about the proof: the proof was accepted in both variants and is the same. It does not say P6 catches every error, that the published procedure fails at its own job of checking the proof, or anything about the Millennium Prize. It is one case.

**Question for reviewers:** does a check that receipts correspond to the artifacts they name add a useful traceability guarantee to a reproducible verification workflow?

## Reproduce

`python3 -m unittest test_results` (run in CI) recomputes P6 on the published bundles with the frozen `protocol_lib_v2.py`, checks that the two bundles differ only in that receipt row, and that Z's recorded output is identical for both. Z itself needs the Lean build and is reproduced with [`run.sh`](run.sh).

## Recording notes

- The wrapper's first `lake --version` and `lean --version` ran outside the project directory, where no default toolchain is configured, so they failed and are missing from `versions.txt`. The versions were read afterwards inside the same tree and are in [`toolchain.txt`](results/toolchain.txt); the Lean commit also appears in the build log.
- `lake exe cache get` took 18 s and `lake build` 36 s because the tree was already built; the copy of B4 was made with `cp -a`.
