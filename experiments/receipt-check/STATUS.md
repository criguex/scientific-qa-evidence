# Status

| Date | Event | Script as run |
| --- | --- | --- |
| 2026-10-22 | Case 1 pre-registered | `8478f68` |
| 2026-10-22 | **Attempt 1 aborted during setup, no result.** Copying build B5's tree (about 26 GB) filled the host's Windows system drive, which holds the WSL virtual disk; the copy failed with I/O errors before any step of Z or X ran. The scratch copies were deleted. | `8478f68` |
| 2026-10-22 | **Amendment 1, before any step ran.** B5's tree had been deleted to free the host, so the copy is made from build B4's tree, also compiled from source with `lake --no-cache build`; the script measures the host drive before and after the copy. Nothing else changed. | `db1da97` |
| 2026-10-22 | **Case 1 run, as registered** ([results](RESULTS.md)) | `run.sh` at `db1da97` |
| 2026-10-22 | Case 2 pre-registered | `a719676` |
| 2026-10-22 | **Case 2 run, as registered** ([results](RESULTS2.md)) | `run2.sh` at `a719676` |
| 2026-10-22 | Scripts hardened after outside review (below); the observed results are unchanged | this commit |

**What was repeated in each run.** The project tree was copied from B4, which was already built; `lake exe cache get` and `lake build` ran once to write the bundle (case 1) and were not repeated per variant. Only Comparator was run once per variant, on the same tree with that variant's bundle in it.

**Reproducibility gaps found in review, and fixed for future reruns.** The scripts as run (1) did not abort if the host's free space could not be measured, or if the clone, the copy or the toolchain record failed; (2) cloned `main` instead of a pinned commit (the commit actually used is recorded in each run's `versions.txt` or `toolchain.txt`: `db1da97` and `a719676`); (3) did not assert the toolchain, the `lake-manifest.json` revisions or the tool hashes, which were only recorded; (4) case 2 relied on tool links created by case 1 in a shared directory that case 1's script deletes at start. The current `run.sh` and `run2.sh` take a required `QA_COMMIT`, use one directory per case, and load [`preflight.sh`](preflight.sh), which aborts on any of these and checks Lean `v4.34.0-rc2`, the Comparator `19e111e`, Mathlib `85e3a25` and lean4export `cacf989` revisions, and the landrun, lean4export, nanoda and Comparator binary hashes. These fixes do not change the observed results; the scripts exactly as run stay in the git history at the commits above.

**Second hardening, 2026-10-22, after outside review.** The scripts as run could still print `DONE` after an unexpected failure of a stage. Every stage now goes through `expect` (in `preflight.sh`): its receipt is written first, and the script stops unless the exit code is one it should have. The procedure's steps and Comparator must exit 0; the checks P6 and hash may exit 0 or 1, since 1 is a finding; copies, edits and placing the bundle must succeed. The published receipts show every stage succeeded as expected, so this does not change the observed results.
