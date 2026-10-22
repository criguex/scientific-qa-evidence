# Revalidation of alternatives (C) and (D), 2026-10-21

State: **complete** · 18 of 18 checks recorded · 0 unexpected · 1 not run (toolchain mismatch).

This record repeats and extends the [2026-10-20 Comparator record](../comparator/README.md) for OpenAI's [NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler) at commit `f9e8bc5` (leanprover/lean4:v4.34.0-rc2) on one host: Linux x86_64 · WSL2 · 12 vCPU · 30 GiB. Machine-readable results are in [`results.json`](results.json); every public file is traced to its original and that original's SHA-256 in [`PROVENANCE.md`](PROVENANCE.md).

## Results

| Check | Build | Expected | Verdict | Elapsed | Comparator decision | Records |
| --- | --- | --- | --- | ---: | --- | --- |
| Comparator run 2 · Navier–Stokes (C, D) | B2 | accept | **ACCEPTED** | 7.0 min | `Your solution is okay!` | [log](logs/comparator2_NavierStokes.sanitized.log) |
| Comparator run 2 · Euler | B2 | accept | **ACCEPTED** | 11.2 min | `Your solution is okay!` | [log](logs/comparator2_Euler.sanitized.log) |
| Comparator run 3 · Navier–Stokes on B3 | B3 | accept | **ACCEPTED** | 6.6 min | `Your solution is okay!` | [log](logs/comparator3_clean_NavierStokes.sanitized.log) |
| Comparator run 3 · Euler on B3 | B3 | accept | **ACCEPTED** | 11.2 min | `Your solution is okay!` | [log](logs/comparator3_clean_Euler.sanitized.log) |
| Comparator run 4 · Navier–Stokes on B4 | B4 | accept | **ACCEPTED** | 6.7 min | `Your solution is okay!` | [log](logs/comparator4_nocache_NavierStokes.sanitized.log) |
| Comparator run 4 · Euler on B4 | B4 | accept | **ACCEPTED** | 11.2 min | `Your solution is okay!` | [log](logs/comparator4_nocache_Euler.sanitized.log) |
| Control · comment-only edit to the challenge | B2 | accept | **CONTROL_ACCEPTED** | 7.0 min | `Your solution is okay!` | [log](logs/mutant_control_comment.sanitized.log) · [diff](mutants/control_comment.diff) |
| (C) add f = 0 · forceless statement | B2 | reject | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'NavierStokes.Comparator.navier_stokes_breakdown_R3'` | [log](logs/mutant_force_zero_R3.sanitized.log) · [diff](mutants/force_zero_R3.diff) |
| (D) add f = 0 · forceless statement | B2 | reject | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'NavierStokes.Comparator.navier_stokes_breakdown_periodic'` | [log](logs/mutant_force_zero_periodic.sanitized.log) · [diff](mutants/force_zero_periodic.diff) |
| (C) swap ℝ³ decay data for periodic data | B2 | reject | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'NavierStokes.Comparator.navier_stokes_breakdown_R3'` | [log](logs/mutant_domain_R3_to_periodic_data.sanitized.log) · [diff](mutants/domain_R3_to_periodic_data.diff) |
| (C) weaken nu > 0 to nu ≥ 0 | B2 | reject | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'NavierStokes.Comparator.navier_stokes_breakdown_R3'` | [log](logs/mutant_viscosity_nonneg_R3.sanitized.log) · [diff](mutants/viscosity_nonneg_R3.diff) |
| (D) drop ¬ · existence instead of breakdown | B2 | reject | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'NavierStokes.Comparator.navier_stokes_breakdown_periodic'` | [log](logs/mutant_existence_not_breakdown_periodic.sanitized.log) · [diff](mutants/existence_not_breakdown_periodic.diff) |
| Euler · tighten T* ≤ 1 to T* ≤ 1/2 | B2 | reject | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'Euler.exists_compact_smooth_euler_singularity'` | [log](logs/mutant_euler_tstar_half.sanitized.log) · [diff](mutants/euler_tstar_half.diff) |
| B3 · fresh build, Mathlib compiled locally | B3 | ok | **OK** | 1 h 27 min | — | [log](logs/clean_build.excerpt.log) |
| B4 · no-cache build, everything compiled locally | B4 | ok | **OK** | 1 h 29 min | — | [log](logs/nocache_build.excerpt.log) |
| leanchecker --fresh · Navier–Stokes solution | B2 | ok | **OK** | 19.6 min | — | [log](logs/leanchecker_fresh_NavierStokes.ComparatorSolution.log) · [receipt](receipts/leanchecker_fresh_NavierStokes.ComparatorSolution.txt) |
| leanchecker --fresh · Euler solution | B2 | ok | **OK** | 22.5 min | — | [log](logs/leanchecker_fresh_Euler.Solution.log) · [receipt](receipts/leanchecker_fresh_Euler.Solution.txt) |
| lean4lean --fresh · Navier–Stokes solution (best effort) | B2 | ok | **FAILED_TOOLCHAIN_MISMATCH** | — | — | [log](logs/lean4lean_build.error-excerpt.log) · [receipt](receipts/lean4lean.txt) |

## Builds used by each run

Four different builds are involved in this record. They differ in where Mathlib and the smaller dependencies came from, so each run is labeled with its build. A fifth build, B5, was made later from source for release v1.3.0 and is recorded in [`../b5/`](../b5/README.md).

| Build | Command | Where the compiled libraries came from | Used by |
| --- | --- | --- | --- |
| **B1 · clean03 · 2026-10-20** | `lake --no-cache build` | compiled; the clean03 record states that dependency and toolchain caches were reused | Comparator run 1 (the 2026-10-20 record) |
| **B2 · audit build · 2026-10-20** | `lake exe cache get, then lake build` | prebuilt Mathlib cache downloaded with `lake exe cache get` (8,747 files attempted) | Comparator run 2, statement mutants, leanchecker --fresh, lean4lean --fresh |
| **B3 · fresh build · 2026-10-21** | `XDG_CACHE_HOME=<empty dir> MATHLIB_NO_CACHE_ON_UPDATE=1 lake build` | compiled locally; 7 smaller dependencies arrived as prebuilt Reservoir barrels | Comparator run 3 |
| **B4 · no-cache build · 2026-10-21** | `XDG_CACHE_HOME=<empty dir> MATHLIB_NO_CACHE_ON_UPDATE=1 lake --no-cache build` | everything compiled locally (Lake told not to download build caches) | Comparator run 4 |

## B3 · fresh build, 2026-10-21

- **Command:** `XDG_CACHE_HOME=<empty dir> MATHLIB_NO_CACHE_ON_UPDATE=1 lake build`, run in a fresh extraction of the pinned source archive `NavierStokesAndEuler-f9e8bc5…tar.gz` (SHA-256 `afd4d226…834b4b5`, checked before extraction).
- **Started / finished (UTC):** 2026-10-21T15:35:41Z → 2026-10-21T17:02:23Z · 1 h 27 min · exit code **0**.
- **Versions:** Lean and Lake 4.34.0-rc2 (commit `6a10ac8`), Mathlib `85e3a25`, and all dependency revisions in [the versions receipt](receipts/fresh_build_versions.txt).
- **Log:** [first 40 and last 15 lines](logs/clean_build.excerpt.log). The full original is not distributed; its SHA-256 is `627f1474a9cf3ac698693aa295445574343239364b563a89975e4efbe8522011`.

### What the counters mean

| Number | What it counts | How it was obtained |
| ---: | --- | --- |
| 11,432 | Lake's own job total, from the final line `Build completed successfully (11432 jobs)`. A job is any Lake build step, not only a compiled module. | Last line of the log. |
| 11,030 | Progress lines that Lake printed as `[n/N] Built X`: 8,371 for Mathlib, 1,840 for Euler, 817 for NavierStokes and 2 for ComparatorChallenges. | `grep -cE '\] Built ' build.log`, then grouped by the first name component. |
| 8,371 | `.olean` files under Mathlib's build directory, one per compiled module, root `Mathlib` included. The earlier figure 8,370 counted only `Built Mathlib.` submodules. | `find … -name '*.olean' \| wc -l`, which matches the printed Mathlib lines. |
| 402 | Jobs that Lake ran without printing a `Built` line. They include fetching and unpacking the dependency archives below. The exact split was not recorded. | 11,432 − 11,030. |

### Cache check, and what was not compiled locally

- **Isolated cache:** `XDG_CACHE_HOME` pointed to a directory created empty at the build start; it held 0 files afterwards. `MATHLIB_NO_CACHE_ON_UPDATE=1` was set, and `lake exe cache get` was never run. The host's older Mathlib cache from 2026-10-20 was not modified (newest file 2026-10-20).
- **What the log did not show:** a search of the log for `fetched`, `unpack` or `downloading` returned 0. That search was **not sufficient**. Lake fetched prebuilt archives (`build.barrel`) from the [Reservoir](https://reservoir.lean-lang.org) package registry for seven dependencies without printing those jobs. They were found afterwards in `.lake/packages/*/.lake/`:

| Package | Bytes | Barrel SHA-256 | Source |
| --- | ---: | --- | --- |
| LeanSearchClient | 1,110,298 | `3261fb4aeea5c924815272a52b398eb66c899e82b181c010d66dcf8b79fff67a` | `https://reservoir.lean-lang.org/api/v1/packages/leanprover-community/LeanSearchClient/barrel` |
| Qq | 4,671,641 | `b89ab157960dc0c10c9b6963fa230273d10b446276860421eb95fe396be59233` | `https://reservoir.lean-lang.org/api/v1/packages/leanprover-community/Qq/barrel` |
| aesop | 30,521,889 | `7f1e07f0fa8b63f54af124350c9b0504d28ef9f5c120cbe1745844b39b5910a7` | `https://reservoir.lean-lang.org/api/v1/packages/leanprover-community/aesop/barrel` |
| batteries | 99,850,446 | `694bf9ca49d5450f82419ff7034ecd90393d2a44c2e0e23bf776f29153bc53c5` | `https://reservoir.lean-lang.org/api/v1/packages/leanprover-community/batteries/barrel` |
| importGraph | 61,390,129 | `dc1fe957970c455d5b086106d6d3df34e106599b9ee170d6c510fd977e5dbc16` | `https://reservoir.lean-lang.org/api/v1/packages/leanprover-community/importGraph/barrel` |
| plausible | 3,010,777 | `8e3d14110256a72e960f1ad955f9f6465dda100b6ee636d10b0bf16777abb159` | `https://reservoir.lean-lang.org/api/v1/packages/leanprover-community/plausible/barrel` |
| proofwidgets | 10,715,826 | `8f0969afc70a21ae5714e3ec029cf1de88b71febadab957ff5d0306152a7db9f` | `https://reservoir.lean-lang.org/api/v1/packages/leanprover-community/proofwidgets/barrel` |

- **Artifact timestamps confirm the split.** Every `.olean` from Mathlib and from OpenAI's project is newer than the build start; every `.olean` of the seven barrel packages is older, because it was packed upstream.

| Package | .olean files | older than the build start |
| --- | ---: | ---: |
| LeanSearchClient | 4 | 4 |
| Qq | 14 | 14 |
| aesop | 132 | 132 |
| batteries | 191 | 191 |
| importGraph | 21 | 21 |
| mathlib | 8371 | 0 |
| plausible | 13 | 13 |
| proofwidgets | 24 | 24 |
| _project | 2659 | 0 |

So B3 compiled **11,030 modules locally** (Mathlib and the project) and received **399 prebuilt dependency modules** from Reservoir. It is not a complete bootstrap; B4 repeats it with `--no-cache`.

## B4 · no-cache build, 2026-10-21

- **Command:** `XDG_CACHE_HOME=<RUN>/nocache/xdg MATHLIB_NO_CACHE_ON_UPDATE=1 lake --no-cache build` in a fresh extraction of the same archive.
- **Started / finished (UTC):** 2026-10-21T17:45:04Z → 2026-10-21T19:14:27Z · 1 h 29 min (GNU `time`, [receipt](receipts/nocache_build.time.txt)) · exit code **0** · 11424 jobs.
- **Downloads:** 0 `build.barrel` files in `.lake/packages`; 0 files in the empty cache directory afterwards.
- **Log:** [excerpt](logs/nocache_build.excerpt.log), original SHA-256 `7afcff48807c0c231536bc825d6d338dd53390d6328677a8d1931b85dccd9668`. Versions: [receipt](receipts/nocache_build_versions.txt).

| Package | .olean files | older than the build start |
| --- | ---: | ---: |
| LeanSearchClient | 4 | 0 |
| Qq | 14 | 0 |
| aesop | 132 | 0 |
| batteries | 190 | 0 |
| importGraph | 10 | 0 |
| mathlib | 8371 | 0 |
| plausible | 13 | 0 |
| proofwidgets | 13 | 0 |
| _project | 2659 | 0 |

## Receipts

### leanchecker --fresh (on B2)

leanchecker prints nothing when every declaration is accepted, so both logs are empty. They are published exactly as recorded, not filled in.

| Module | Command | Started (UTC) | Finished (UTC) | Exit | Elapsed | Log |
| --- | --- | --- | --- | ---: | ---: | --- |
| `NavierStokes.ComparatorSolution` | `timeout 10h lake env leanchecker --fresh NavierStokes.ComparatorSolution` | 2026-10-21T14:53:37Z | 2026-10-21T15:13:12Z | 0 | 19.6 min | 0 bytes ([as recorded](logs/leanchecker_fresh_NavierStokes.ComparatorSolution.log)) |
| `Euler.Solution` | `timeout 10h lake env leanchecker --fresh Euler.Solution` | 2026-10-21T15:13:12Z | 2026-10-21T15:35:41Z | 0 | 22.5 min | 0 bytes ([as recorded](logs/leanchecker_fresh_Euler.Solution.log)) |

Executable: `leanchecker` from the Lean 4.34.0-rc2 toolchain, SHA-256 `ccef1bfe9bfeecea65137d94a69033c1a89f360711f50fa3178e7ba3e696fcbe`. GNU `time` receipts with maximum RSS are in [`receipts/`](receipts/).

### lean4lean (not run on the proofs)

- **Versions:** lean4lean commit `67f63b0c818920dfaed2ad07ccff187a6a8fe1e3`; its pinned toolchain is `leanprover/lean4:v4.33.0-rc2`, overridden to `leanprover/lean4:v4.34.0-rc2` to match the proofs; Batteries `76e1c118b0700b4ceafe99532e887d6431625e1a` as resolved by `lake update`.
- **Command:** `lake update && lake build (lean-toolchain set to leanprover/lean4:v4.34.0-rc2)` · 2026-10-21T17:20:09Z → 2026-10-21T17:20:36Z · exit code **1**.
- **Error:** [excerpt](logs/lean4lean_build.error-excerpt.log). Batteries failed to compile under Lean 4.34 (`Tactic unfold failed to unfold cond` in `Batteries/Data/List/Basic.lean`). lean4lean itself was never built, so it **never examined the proofs**. This is a tooling gap, not a verdict.

### Reused tools

The from-scratch builds did not rebuild the checkers. These binaries were reused in Comparator runs 2–4 and in the mutant runs (run 1 is documented in its own record):

| Tool | SHA-256 | Revision |
| --- | --- | --- |
| comparator | `514de8d2acbd6e0102575cd2c575e336b7c4a40daf3ae66abe97cef5e1e6b02a` | 19e111e2141cf333c7daff0f64c5f24acc91dd2e |
| lean4export | `4fa9e14cada304109e85da5048bcd411cf781a03539b3e50953e5c537074bd9e` | cacf989bd75f608700820f6afc595f32e7a99a4d |
| nanoda_bin | `ccda52587ef42760dff9bc2de26edca0cb6ad207c8719cfffcd1e7daab22ccfb` | 9d6964f78d0fa4c93fd22fe956e17afe7e72a441 |
| landrun | `e3d26ebf2f7c786f8d34b7051ad2c655329aeadbb863404e3dd05d3a97b0518a` | ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a |
| leanchecker | `ccef1bfe9bfeecea65137d94a69033c1a89f360711f50fa3178e7ba3e696fcbe` | Lean 4.34.0-rc2 toolchain |
| lean | `e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550` | Lean 4.34.0-rc2 toolchain |
| lake | `6f53827dab18010d6c690d14c8401cacabc1db958edb3552a877ed4cf1dd995d` | Lean 4.34.0-rc2 toolchain |

## How to read the verdicts

- `ACCEPTED`: Comparator printed `Your solution is okay!` after both nanoda and the Lean kernel accepted the solution.
- `KILLED`: Comparator refused a mutated statement; the decision column quotes its message.
- `FAILED_TOOLCHAIN_MISMATCH`: the checker itself could not be built for this Lean version, so it never examined the proofs.
- `PENDING`: not finished yet.
- A killed mutant says nothing about whether the mutated statement is true or false. The `f = 0` mutants are not evidence about the forceless alternatives (A) and (B).
