# Revalidation of alternatives (C) and (D), 2026-10-21

State: **in progress** · 14 of 15 checks recorded · 0 unexpected · last update 2026-10-21T17:20:09Z.

This run repeats and extends the [2026-10-20 Comparator record](../comparator/README.md) for OpenAI's [NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler) at commit `f9e8bc5` (leanprover/lean4:v4.34.0-rc2) on one host: Linux x86_64 · WSL2 · 12 vCPU · 30 GiB. It answers the gaps listed under "Known limitations" in the top-level README:

1. **A second Comparator run** on the existing build, for the Navier–Stokes challenge (alternatives C and D) and for Euler.
2. **Statement mutants.** Each mutant edits only the challenge file `ComparatorChallenges/*.lean` in a copy of the repository and leaves OpenAI's solution untouched. Comparator must refuse every mutant. A comment-only control must still be accepted, which shows that refusals come from the statement change and not from the edit itself.
3. **Fresh kernel replay** with `leanchecker --fresh`, which re-adds every declaration, Mathlib included, to an empty environment. It runs the same C++ kernel that Comparator already uses, so it adds a from-scratch replay, not a new implementation. `lean4lean`, a kernel written in Lean, is attempted as well; its upstream pin is Lean v4.33.0-rc2, so a toolchain failure is recorded as such, not as a verdict on the proofs.
4. **A from-scratch build** of the pinned source archive with an empty cache directory and `MATHLIB_NO_CACHE_ON_UPDATE=1`, so Mathlib is compiled rather than downloaded, followed by a third Comparator run on that build. The Comparator, lean4export, nanoda and landrun binaries are reused from the 2026-10-20 setup.

| Check | Expected | Verdict | Elapsed | Comparator decision | Record |
| --- | --- | --- | ---: | --- | --- |
| Comparator run 2 · Navier–Stokes (C, D) | accept | **ACCEPTED** | 7.0 min | `Your solution is okay!` | [log](logs/comparator2_NavierStokes.sanitized.log) |
| Comparator run 2 · Euler | accept | **ACCEPTED** | 11.2 min | `Your solution is okay!` | [log](logs/comparator2_Euler.sanitized.log) |
| Comparator run 3 · Navier–Stokes on the from-scratch build | accept | **ACCEPTED** | 6.6 min | `Your solution is okay!` | [log](logs/comparator3_clean_NavierStokes.sanitized.log) |
| Comparator run 3 · Euler on the from-scratch build | accept | **ACCEPTED** | 11.2 min | `Your solution is okay!` | [log](logs/comparator3_clean_Euler.sanitized.log) |
| Control · comment-only edit to the challenge | accept | **CONTROL_ACCEPTED** | 7.0 min | `Your solution is okay!` | [log](logs/mutant_control_comment.sanitized.log) · [diff](mutants/control_comment.diff) |
| (C) add f = 0 · forceless statement | reject | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'NavierStokes.Comparator.navier_stokes_breakdown_R3'` | [log](logs/mutant_force_zero_R3.sanitized.log) · [diff](mutants/force_zero_R3.diff) |
| (D) add f = 0 · forceless statement | reject | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'NavierStokes.Comparator.navier_stokes_breakdown_periodic'` | [log](logs/mutant_force_zero_periodic.sanitized.log) · [diff](mutants/force_zero_periodic.diff) |
| (C) swap ℝ³ decay data for periodic data | reject | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'NavierStokes.Comparator.navier_stokes_breakdown_R3'` | [log](logs/mutant_domain_R3_to_periodic_data.sanitized.log) · [diff](mutants/domain_R3_to_periodic_data.diff) |
| (C) weaken nu > 0 to nu ≥ 0 | reject | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'NavierStokes.Comparator.navier_stokes_breakdown_R3'` | [log](logs/mutant_viscosity_nonneg_R3.sanitized.log) · [diff](mutants/viscosity_nonneg_R3.diff) |
| (D) drop ¬ · existence instead of breakdown | reject | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'NavierStokes.Comparator.navier_stokes_breakdown_periodic'` | [log](logs/mutant_existence_not_breakdown_periodic.sanitized.log) · [diff](mutants/existence_not_breakdown_periodic.diff) |
| Euler · tighten T* ≤ 1 to T* ≤ 1/2 | reject | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'Euler.exists_compact_smooth_euler_singularity'` | [log](logs/mutant_euler_tstar_half.sanitized.log) · [diff](mutants/euler_tstar_half.diff) |
| From-scratch build · empty caches, Mathlib compiled | ok | **OK** | — | — | — |
| leanchecker --fresh · Navier–Stokes solution | ok | **OK** | 19.6 min | — | [log](logs/leanchecker_fresh_NavierStokes.ComparatorSolution.sanitized.log) |
| leanchecker --fresh · Euler solution | ok | **OK** | 22.5 min | — | [log](logs/leanchecker_fresh_Euler.Solution.sanitized.log) |
| lean4lean --fresh · Navier–Stokes solution (best effort) | ok | **PENDING** | — | — | — |

## How to read the verdicts

- `ACCEPTED`: Comparator printed `Your solution is okay!` after both nanoda and the Lean kernel accepted the solution.
- `KILLED`: Comparator refused a mutated statement. The decision column quotes its message. `Challenge and solution theorem statement do not match` means the mutated challenge compiled and the refusal came from the statement comparison.
- `PENDING`: not finished yet. Any verdict outside the expected column would be listed as unexpected above.
- A killed mutant says nothing about whether the mutated statement is true or false. In particular, the two `f = 0` mutants only show that Comparator will not accept the forced proofs for a forceless statement. They are not evidence about the forceless alternatives (A) and (B).

Logs are sanitized with [`../comparator/sanitize_comparator_logs.py`](../comparator/sanitize_comparator_logs.py): private paths and private IPs are redacted. Machine-readable results are in [`results.json`](results.json).
