# Version port: results

**Status: draft.** Plan: [`PLAN.md`](PLAN.md), registered before any run and not edited. Run on 2026-11-24 (UTC).

- **R0 · v4.34.0-rc2: complete.** Every check came out as registered, including lean4lean, the third kernel.
- **R1 · v4.34.0 and R2 · v4.35.0: the build fails** in OpenAI's proof code, not in the statements. The statements of both challenges still compile unchanged. No proof was edited, so steps 5–10 did not run for R1 and R2. On the author's decision a proof port is now being attempted with no time limit, under [Amendment 1](PLAN.md#amendment-1--2026-11-24-before-any-proof-edit-was-used-for-a-result) of the plan; its results will be added here as a dated update.

Every number below comes from a file in this folder. [`R0/`](R0/), [`R1/`](R1/), [`R2/`](R2/) and [`tools/`](tools/) hold the receipts and logs. Each step has a line in `receipts/steps.tsv` (command, working directory, start and end UTC, exit code, SHA-256 and size of its log) and a GNU `time -v` receipt. Each verdict has a line in `receipts/checks.tsv`, expected against obtained. Every folder has a `PROVENANCE.tsv` giving, for each file, the SHA-256 of the original on the host and of the published copy. Copies differ from the originals only where host paths were replaced by `<path>` or the host name by `<host>`, and in the three build-log excerpts described under R1 and R2. Before publishing, every original was checked against a SHA-256 list made on the host. The driver scripts are in [`scripts/`](scripts/).

Host: the author's Linux test host (WSL2, Ubuntu 24.04.5, kernel 6.18.33.2-microsoft-standard-WSL2, 12 vCPU, 30 GiB), run as root, with AI assistance. This is not an independent reproduction and does not change AC-5.4.

## Summary

| Step | R0 · v4.34.0-rc2 | R1 · v4.34.0 | R2 · v4.35.0 |
| --- | --- | --- | --- |
| 1 Clean clone, content manifest `95bb21c9…52e95fc` | as expected | as expected | as expected |
| 2 Versions | rc2, Mathlib `85e3a25`, Comparator `19e111e` | v4.34.0, Mathlib `5ed2965`, Comparator `d03acab`, as registered | v4.35.0, Mathlib `56a0058`, Comparator `e3dcf30`, as registered |
| 3 Statements identical to `f9e8bc5` | yes | yes | yes |
| 4 Build | exit 0 | **exit 1**: 15 modules fail, 103 errors | **exit 1**: 20 modules fail, 121 errors |
| 5 Axioms of the 4 final theorems | standard only | not run | not run |
| 6 Comparator, nanoda + Lean kernel | both accepted | not run | not run |
| 7 leanchecker --fresh | both exit 0 | not run | not run |
| 8 lean4lean --fresh | both exit 0 | not run | not run |
| 9 Mutants | 6 of 6 refused, control accepted | not run | not run |
| 10 Bridges | 35 of 35 theorems, standard axioms only | not run | not run |

**No checker refused either solution on any run.**

**AC-2.4 can turn to yes.** lean4lean `0048ed7`, **rebuilt on Lean v4.34.0-rc2** (its upstream toolchain is v4.34.0), replayed both solution modules into fresh environments and exited 0. `NavierStokes.ComparatorSolution`: `checked 806768 declarations`. `Euler.Solution`: `checked 788326 declarations`. As the plan requires, the note is that this lean4lean binary was not built on its upstream toolchain. On its native toolchains (R1, R2) it could not be run, because the proofs do not build there.

## Tools

Built on the host for this experiment ([`tools/receipts/tools.tsv`](tools/receipts/tools.tsv), build logs in [`tools/logs/`](tools/logs/)).

| Tool | Revision | SHA-256 | Note |
| --- | --- | --- | --- |
| comparator (v4.34.0-rc2) | `19e111e` | `514de8d2acbd6e0102575cd2c575e336b7c4a40daf3ae66abe97cef5e1e6b02a` | identical to the binary of the main audit; the executable Lake built inside R0 has the same hash ([receipt](R0/receipts/comparator_exe.txt)) |
| lean4export (v4.34.0-rc2) | `cacf989` | `4fa9e14cada304109e85da5048bcd411cf781a03539b3e50953e5c537074bd9e` | identical to the binary of the main audit |
| comparator (v4.34.0) | `d03acab` | `8efd5e1532b5e47d5ed5ead9ea42483068fbba81ad76e486ff8d2dbcf76e00f2` | built, not used (R1 did not build) |
| lean4export (v4.34.0) | `076e8e5` | `cbf95bb18e3fc19bbe39ad2a250d9cfce4ca01315b2acf8f630d1e315498bf60` | revision pinned by Comparator v4.34.0; not used |
| comparator (v4.35.0) | `e3dcf30` | `3300f5a725ae8dcbfb88b3eb0c605c5737ec8e02bc3033f80665a182d997b023` | built, not used (R2 did not build) |
| lean4export (v4.35.0) | `5a9a355` | `87f4fe988dfe97a2a607cf38a8777a625b482f833985c16dbc1ddafa525f4bba` | revision pinned by Comparator v4.35.0; not used |
| nanoda_bin | `0da9f98` | `23fe7e2e1f904021eed2cf1bd74bbeb5c18d693d6a1d3ba9c21f60d41b3229f8` | newer than the audit's `9d6964f`, as registered |
| landrun | `ec104f6` | `1c35440a6ceb32badfe51f392ae0489eb9da4b37c7e08d8c57b9bd803d803153` | same revision as the audit; a different binary (Go 1.27.4) |
| lean4lean (R0) | `0048ed7`, built on rc2 | `176afe26174008221f0c00f07759c5c5c00739207025e37a57025558a72233ef` | built by a separate script, `l4l.sh` ([log](R0/l4l_original/run.log)), 113 s |
| lean, lake, leanchecker (rc2) | `6a10ac8` | `e8baaa71…5d550`, `6f53827d…dd995d`, `ccef1bfe…6fcbe` | identical to the audit ([`R0/receipts/versions.txt`](R0/receipts/versions.txt)) |

Rust 1.100.0, Go 1.27.4.

**landrun runs in best-effort mode here.** The kernel reports Landlock ABI v7. landrun `ec104f6` asks for v10 and refuses to start without `--best-effort`. Comparator always passes `--best-effort`. A manual check showed the sandbox still blocking writes outside the allowed paths: `touch` in `/etc` was denied, in `/tmp` it was allowed. That check was run by hand and has no log. Comparator's README also assumes an unprivileged user and a `systemd-run` wrapper; these runs used root and no wrapper. Neither point changes what the kernels accept. Both weaken the sandbox, which matters only for adversarial solutions.

## R0 · v4.34.0-rc2 (the audited version)

| # | Step | Expected | Obtained | Log (SHA-256 of the original) |
| --- | --- | --- | --- | --- |
| 1 | Clean clone at `f9e8bc5`, content manifest | `95bb21c9…52e95fc` | `95bb21c93e834581e1400e31e33a9fb7943db2f64f11425b034f97b9b52e95fc` | `logs/s1_manifest.log` (`b3f8a3b6…`) |
| 2 | Versions | rc2, Mathlib `85e3a25`, Comparator `19e111e` | same | `receipts/manifest_revs.tsv` |
| 3 | Statement check (`git diff` of `ComparatorChallenges/` and both solution files against `f9e8bc5`) | empty | empty, exit 0; repeated after the build, empty | `logs/s3_statements.log` (`81bff35b…`) |
| 4 | Build | exit 0 | exit 0, `Build completed successfully (11424 jobs)`, see note | `logs/s4_build.log` (`d1b23d12…`) |
| 5 | `#print axioms` of the 4 theorems named in the two Comparator configs | standard axioms only | 4 of 4: `[propext, Classical.choice, Quot.sound]` | `logs/s5_axioms.log` (`9541bf73…`) |
| 6 | Comparator · Navier–Stokes | okay, exit 0 | `nanoda kernel accepts the solution`, `Lean default kernel accepts the solution`, `Your solution is okay!`, exit 0, 7 min 20 s | `logs/s6_comparator_NavierStokes.log` (`86f19cfa…`) |
| 6 | Comparator · Euler | okay, exit 0 | the same three lines, exit 0, 12 min 14 s | `logs/s6_comparator_Euler.log` (`5f410965…`) |
| 7 | leanchecker --fresh · Navier–Stokes | exit 0 | exit 0, empty log, 34 min 36 s, 10.8 GB peak memory | `logs/s7_leanchecker_NavierStokes.ComparatorSolution.log` (empty) |
| 7 | leanchecker --fresh · Euler | exit 0 | exit 0, empty log, 50 min 34 s, 10.7 GB peak memory | `logs/s7_leanchecker_Euler.Solution.log` (empty) |
| 8 | lean4lean --fresh · Navier–Stokes | exit 0 | exit 0, `checked 806768 declarations`, 1,459 s | `l4l_original/NavierStokes.ComparatorSolution.log` (`44a5967c…`) |
| 8 | lean4lean --fresh · Euler | exit 0 | exit 0, `checked 788326 declarations`, 29 min 44 s | `logs/s8_lean4lean_Euler.Solution.log` (`ce143b05…`) |
| 9 | Control: comment-only edit | accepted | accepted, exit 0 | `logs/s9_mutant_control_comment.log` |
| 9 | 6 statement mutants | refused | 6 of 6 refused, exit 1, each with `Challenge and solution theorem statement do not match`, naming the theorem that was changed; 1 min 44 s to 1 min 57 s each | `logs/s9_mutant_*.log` |
| 10 | Bridges: compile `ClayLiteral` and `Bridges`, `#print axioms` | exit 0, standard axioms | exit 0 three times; 35 of 35 theorems (34 in `Bridges` and `ClayLiteral.altD_withoutErratum_imp_withErratum`) `[propext, Classical.choice, Quot.sound]` | `logs/s10_bridge_axioms.log` (`51c2f814…`) |

**The Comparator logs are byte-identical to those of the audit.** The two step-6 logs have the same SHA-256 as the stdout of Comparator runs 2, 3 and 4 in [`PROVENANCE.md`](../../evidence/formal/cd-validation/PROVENANCE.md) (`86f19cfa…`, `5f410965…`).

**Build note.** Step 4 for R0 is the build made by a separate setup run in another folder on the same host: `lake exe cache get`, 353 s, then `lake build`, 1,610 s, exit 0 ([`receipts/original_build_pasos.tsv`](R0/receipts/original_build_pasos.tsv)). That run kept no log of its own. Its `.lake` directory was copied into R0's clean clone, where `lake build` took 12 s, finished with `Build completed successfully (11424 jobs)` and compiled 0 modules. The Mathlib cache was used, as registered.

**Step 8 note.** lean4lean on R0 was run by `l4l.sh`, not by this experiment's driver. It checked the Navier–Stokes module in the original build folder, then was killed while checking Euler (see [Incidents](#incidents)). Only the Euler half was run again, with the same binary, in R0's copy of that build ([`run/l4l_R0_euler.log`](R0/run/l4l_R0_euler.log)). The `l4l.sh` run log is [`l4l_original/run.log`](R0/l4l_original/run.log). Its empty `Euler.Solution.log` is the log of the killed attempt.

**Step 9 note.** The first attempt at mutant `domain_R3_to_periodic_data` did not run, because the published diff does not apply (see [Findings](#findings-about-the-published-evidence)). `checks.tsv` keeps that line as `UNEXPECTED`. The mutant was then run with the restored diff and refused as expected. The control was run twice, before and after the WSL shutdown, and was accepted both times.

## R1 and R2: the build fails

| | R1 · v4.34.0 | R2 · v4.35.0 |
| --- | --- | --- |
| `lake update` | exit 0, 5 min 18 s | exit 0, 1 min 0 s |
| `lake exe cache get` | exit 0 | exit 0 |
| `lake build` | **exit 1** | **exit 1** |
| Modules that failed | 15 (12 in NavierStokes, 3 in Euler) | 20 (17 in NavierStokes, 3 in Euler) |
| Error messages | 103 | 121 |
| Project modules with an `.olean` afterwards, out of 2,655 | 403 | 369 |
| `ComparatorChallenges.NavierStokes`, `ComparatorChallenges.Euler` | built, with only the expected `sorry` warnings | built, with only the expected `sorry` warnings |
| `NavierStokes.ComparatorSolution`, `Euler.Solution` | not built (blocked) | not built (blocked) |

Logs: [`R1/logs/s4_build.errors.log`](R1/logs/s4_build.errors.log) and [`R2/logs/s4_build.errors.log`](R2/logs/s4_build.errors.log). These are excerpts: each keeps every failing module (`✖`) with its error blocks and the final summary, and drops the compiler command lines and the lines of modules that built. The header of each excerpt gives the size and SHA-256 of the full original. Version changes: [`R1/diffs/versions.diff`](R1/diffs/versions.diff), [`R2/diffs/versions.diff`](R2/diffs/versions.diff).

**The statements survive the version change; the proofs do not.** Both challenge files compile unchanged on v4.34.0 and v4.35.0. So the port does not fail on a statement, which would have been the failure that counts under the plan. It fails on proofs, which the plan allows to be edited. No proof was edited.

Errors per file (R1): `Euler/EulerProof.lean` 54, `NavierStokes/R3ConvolutionYoung.lean` 20, `R3/PairedKernelBound` 6, `R3/WeightedInterpolation` 5, `R3/LpNormTools` 4, `EdgeWeightJets` 4, `WeightedRadialPrimitive` 2, and one each in `AppendixHeatResults`, `R3/ComparisonCutoffs`, `R3/H3Products`, `R3/ComparatorBridge`, `R3/PressureFunctionals`, `R3PressureFourier`, `Euler/GevreyComposition`, `Euler/GevreyGeneratingComposition`. R2 fails in the same 15 files, with 59 errors in `EulerProof`, and in five more: `SmoothCovariance`, `SquaredPartition`, `TerminalPressure`, `ModulatedStockBounds`, `HeatedOutgoing`.

What the messages show, read from the logs and without fixing anything:

- **Changes in Mathlib's L^p API.** `eLpNorm_mono_ae`, `eLpNorm_add_le` and `eLpNorm_smul_le_mul_eLpNorm` now take an `AEStronglyMeasurable` argument first. `eLpNorm f p μ < ⊤` now unfolds to `WithTop.LT`, so the anonymous constructors `⟨…⟩` and the projections `.1`/`.2` applied to it fail. This accounts for most errors in the NavierStokes R3 files.
- **`failed to synthesize MulLeftMono ℝ`**: `AppendixHeatResults`, `Euler/GevreyComposition`.
- **`Finset.prod_le_prod`** changed its arguments: `Euler/GevreyGeneratingComposition`.
- **Linters.** In `Euler/EulerProof.lean` some of the errors are linter warnings (`unusedTactic`, `unnecessarySeqFocus`, `unusedSimpArgs`). They count as errors because the `Euler` library sets `warningAsError = true`. The rest of that file has `rfl` that no longer closes, unsolved goals and type mismatches.

How much work a fix would need is not known. 2,252 (R1) and 2,286 (R2) modules never ran, because a failing module blocks every module that imports it, and those may hold more errors. That is not the "minimal fix" the brief allowed, so none was attempted in this run. A full port started afterwards under Amendment 1 of the plan: every edit is kept as a diff in `R1/port/` (and `R2/port/`), internal statement changes are listed separately, and steps 3–10 will run on the result.

## Findings about the published evidence

**Three of the seven published mutant diffs do not apply as published.** `evidence/formal/cd-validation/mutants/domain_R3_to_periodic_data.diff`, `force_zero_R3.diff` and `force_zero_periodic.diff` each lack their last line. That line is a context line made of a single space: the blank line after `sorry`. Each hunk header announces 7 lines per side and the file has only 6, so `git apply` stops with `corrupt patch at line 13` ([log of the failed attempt](R0/run/target-R0.first.log)). The missing line, as `diff <published> <restored>` prints it:

```
12a13
>  
```

Adding that one line (a space and a newline) gives files whose SHA-256 equals the original SHA-256 recorded in [`PROVENANCE.md`](../../evidence/formal/cd-validation/PROVENANCE.md):

| Diff | SHA-256 with the line restored | Original SHA-256 in PROVENANCE.md |
| --- | --- | --- |
| `domain_R3_to_periodic_data` | `63beb94d90c79fd543a1c645f4f7bd839e46247e69a1bb523ac93ef7339823f5` | same |
| `force_zero_R3` | `2125f51c41c03dbf4d6d5dbc5aea80a9343e59eb1cc80895855d467a4e714709` | same |
| `force_zero_periodic` | `43db52345f01c64c7b134888f109e83f3dc0ba0d374a42ae75c3a7135f96b343` | same |

So the original runs used complete diffs, and the line was lost when the public copies were made. The published files were left unchanged. The restored copies, with their hashes, are in [`R0/diffs/`](R0/diffs/) (`*.restored.diff`, `SHA256SUMS`). Every successful mutant run used them. The other four published diffs already match their original hashes ([`R0/receipts/mutant_inputs.sha256`](R0/receipts/mutant_inputs.sha256)).

## Incidents

Recorded as they happened in [`R1/run/INCIDENT.txt`](R1/run/INCIDENT.txt).

- **WSL shutdown, 01:27:56Z.** The WSL virtual machine stopped (`journalctl --list-boots`: the boot ended at 20:27:56 −05:00). A command sent at that moment returned `Wsl/Service/0x8007274c`. Every background job died. That included the R0 driver, which was running mutant `euler_tstar_half`, started 01:26:44Z; its partial log is kept as `s9_mutant_euler_tstar_half.interrupted.log`. It also included the R0 lean4lean run (Euler, started 01:21:29Z) and a first attempt at `domain_R3_to_periodic_data`. Jobs were restarted at about 01:38Z from step 9 of R0, with an idle session kept open to hold the VM up. The interrupted steps have no exit code. Each was run again from the start.
- **Logins refused, then a second shutdown.** From about 02:00Z, the host's SSH server refused new logins for long stretches (`kex_exchange_identification: banner line 0: Exceeded MaxStartups`). The R0 driver finished at 03:26:59Z. The R1 build started at 03:34:28Z. Its log was last written at 03:40:05Z, and it never got an exit code. The VM's boot ended at 05:57:59Z, according to `journalctl`. Logins worked again at 16:09Z. The interrupted R1 build log is kept, as an excerpt, in `R1/logs/s4_build.interrupted.errors.log`. It already showed 9 of the 15 failing modules. The R1 build was then run again, continuing the partial `.lake` (16:10:28Z → 16:13:46Z, exit 1). R2 ran after it (16:17Z → 16:24Z).
- **Tool builds.** The first landrun build hung while downloading Go modules and was killed (exit 143). The first nanoda build failed because no C linker was installed (exit 101). Both were rebuilt at the same revisions once the cause was fixed. The failed attempts stay in `tools/receipts/steps.tsv`.

## Limits

The author ran every step on his own machine, with an AI assistant writing and driving the scripts. The Mathlib cache was used, so Mathlib was not compiled from source in these runs. lean4lean on R0 was built on a toolchain other than its upstream one. A refused mutant says only that Comparator saw a different statement. R1 and R2 say nothing about whether the proofs are correct. They show that OpenAI's proof code, as written for v4.34.0-rc2, does not compile against the Mathlib of later releases.
