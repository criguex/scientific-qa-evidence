# Version port: re-checking OpenAI's proofs on newer Lean releases

**Status: registered before running.** Written on 2026-11-24, before any of the runs below. Results will go to `RESULTS.md` in this folder without editing this plan; any change to the plan will be added as a dated amendment at the end.

## Why

Every check so far ran on the toolchain OpenAI pinned, `leanprover/lean4:v4.34.0-rc2`, with Mathlib, Comparator and lean4export at their `v4.34.0-rc2` tags. Two questions follow from that:

1. **A third kernel (AC-2.4).** lean4lean never examined the proofs because it did not build for Lean 4.34 ([receipt](../../evidence/formal/cd-validation/receipts/lean4lean.txt)). On 2026-11-21 its upstream moved to v4.34.0 (commit `0048ed7`), then v4.35.0 (`b73a4e7`) and v4.36.0 (`23fd034`).
2. **Robustness to a toolchain change.** If the proofs still build, and every checker still accepts them, on later releases with later kernel fixes, the result does not hinge on one release candidate.

## Targets

| ID | Lean | Mathlib | Comparator | lean4lean | Why this target |
| --- | --- | --- | --- | --- | --- |
| R0 | v4.34.0-rc2 | v4.34.0-rc2 (`85e3a25`) | v4.34.0-rc2 (`19e111e`) | `0048ed7` rebuilt on rc2 (upstream says v4.34.0) | The audited version, unchanged. Only lean4lean is new |
| R1 | v4.34.0 | v4.34.0 (`5ed2965`) | v4.34.0 (`d03acab`) | `0048ed7` (native v4.34.0) | Smallest step: the final release of the same minor version |
| R2 | v4.35.0 | v4.35.0 (`56a0058`) | v4.35.0 (`e3dcf30`) | `b73a4e7` (native v4.35.0) | Newest release with Lean, Mathlib and Comparator all tagged. v4.36.0 is out of scope: Comparator has no v4.36.0 tag |

nanoda: latest `ammkrn/nanoda_lib` (`0da9f98`, 2026-11-07). lean4export: the revision each Comparator tag pins.

## What is allowed to change

- `lean-toolchain`, `lakefile.toml` revisions and `lake-manifest.json`.
- **Proof** code, only if a proof stops building, with every edit kept as a diff and explained.
- **Never** a statement. `ComparatorChallenges/*.lean` and the `theorem` lines of the solutions must be byte-identical to `f9e8bc5`. A port that needs a statement change counts as a failed port.

## Steps per target

| # | Step | Command (summary) | Expected |
| --- | --- | --- | --- |
| 1 | Clean clone at `f9e8bc5` in its own folder | `git clone`, `git checkout f9e8bc5` | — |
| 2 | Set versions (R1, R2 only) | edit toolchain and revisions, `lake update` | — |
| 3 | Statement check | `diff` of `ComparatorChallenges/` against `f9e8bc5` | empty |
| 4 | Build with the Mathlib cache | `lake exe cache get`, `lake build` | exit 0 (R1, R2 may need proof edits) |
| 5 | Axioms of the final theorems and bridges | `#print axioms` | only `propext`, `Classical.choice`, `Quot.sound` |
| 6 | Comparator, both kernels | `lake exe comparator ComparatorChallenges/{NavierStokes,Euler}.json` | `Your solution is okay!`, exit 0, for both |
| 7 | Fresh kernel replay | `leanchecker --fresh` on both solutions | exit 0 |
| 8 | Third kernel | `lean4lean --fresh` on both solutions | exit 0 |
| 9 | Statement mutants | the 6 one-symbol mutants and the comment control of [cd-validation](../../evidence/formal/cd-validation/mutants/) | 6 rejected, control accepted |
| 10 | Bridges | build `bridges/` against the target, `#print axioms` | as in step 5 |

Every step records its command, start and end time, exit code and the SHA-256 of its log, in a receipt like those of [cd-validation](../../evidence/formal/cd-validation/receipts/).

## How results will be read

- **AC-2.4 turns to yes** only if lean4lean accepts both solutions on at least one target. If that happens on R0, the note says lean4lean was rebuilt on rc2 rather than on its upstream toolchain.
- **A failed build, a refused solution or a surviving mutant** is reported as found, with its log, and is not retried silently. A checker refusing a solution would be the most important possible result and would be reported before anything else.
- This is not an independent reproduction: the author runs it, on his own machine (Linux on WSL2, 12 cores, 30 GB), with AI assistance. It does not change AC-5.4.
- Using the Mathlib cache means Mathlib is not compiled from source in these runs; B4 and B5 already did that for rc2.
