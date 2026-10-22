# Validation from a fresh clone, 2026-10-21

Everything below started from `git clone https://github.com/criguex/scientific-qa-evidence.git` at commit `a92acbc`, with nothing carried over from the working copy.

## On a Mac, without Lean

| Check | Result |
| --- | --- |
| `shasum -a 256 -c evidence/SHA256SUMS.txt` | PASS, 561 files |
| `python3 evidence/verify_numerical.py` | PASS |
| Rerun the 84 numerical variants (`test_runner`) | PASS |
| `python3 evidence/test_consistency.py` | PASS |
| Animation package tests, 13 scenes | PASS |
| Comparator log sanitizer, statement provenance, blind-fault v1, v2 and fuzzer | PASS |
| Mathlib controls: `verify.py` and `test_verify` | PASS |
| `python3 animations/build.py` regenerates every scene byte-identical | PASS |

## On the Linux host, with Lean

| Check | Result |
| --- | --- |
| `ClayLiteral.lean` and `Bridges.lean` compiled from the clone into an empty directory (no `.olean` reused) | exit 0, 0 warnings, no `sorry`; SHA-256 equal to [`bridges/README.md`](../bridges/README.md) |
| `#print axioms` for `k1_C`, `k1_D`, `k1_C_oneSided`, `k1_D_oneSided`, `zero_solution_C`, `zero_solution_D` | `[propext, Classical.choice, Quot.sound]` for each |
| All 21 Mathlib-control steps (11 Comparator runs, the guard build, 9 second routes) rerun from the clone's files | same exit codes and same input hashes as the published receipts; receipts in [`rerun-from-clone.receipts.jsonl`](../experiments/mathlib-controls/results/rerun-from-clone.receipts.jsonl). Every logged output is identical to a published log except the guard build's stdout, which lacks Lake's progress line `✔ [2/2] Built QAControls.Guard (2.0s)` and is otherwise the same; it is published in [`rerun-from-clone/Guard.stdout.log`](../experiments/mathlib-controls/results/rerun-from-clone/Guard.stdout.log) |

## Not repeated here

- The OpenAI and Mathlib build itself. These checks used build B4, which was compiled from source with `lake --no-cache build` earlier the same day (1 h 29 min, [record](formal/cd-validation/README.md#builds-used-by-each-run)), and the checker binaries recorded in [`receipts/`](formal/cd-validation/receipts/).
- An independent person's run. This was done by the author with the assistant on the same two machines; an outside rebuild is the stronger check. The [independent reproduction guide](../docs/INDEPENDENT_REPRODUCTION.md) gives the steps and a report template.
