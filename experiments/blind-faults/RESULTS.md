# Blind-fault experiment: results (v1)

> **Errata and reframing, after external review on 2026-10-21.** The v1 files below are kept unchanged so the published run stays reproducible. Corrections:
>
> 1. **Read this as a deterministic regression benchmark, not as proof of blinding.** The commit order shows the results were recorded before the key was committed, but it is not absolute evidence of blinding: the assistant had filesystem access to the machine holding the key and itself committed the cases and the key, and the evaluator is deterministic, so the outcome per class did not depend on the assignment.
> 2. **F2 is mislabeled.** Its edit changes the hypothesis `nu > 0` to `nu >= 0`, which relaxes a hypothesis and therefore makes the theorem stronger, not weaker. F2 demonstrates only that P2 detects a textual difference from the reference, not detection of a weakened statement.
> 3. **The planned cost metric was not measured.** DESIGN.md listed wall-clock cost per case; v1 recorded none. v2 measures evaluator time and states what it does not cover.
> 4. **The v1 evaluator had defects** found afterwards: incomplete evidence failed open, absent evidence crashed, and P6 assumed a `comparator.log` that no case contained. Under the corrected evaluator the six v1 "clean" cases are flagged, so **the v1 claim of 0 false alarms does not hold**; it depended on evidence the evaluator assumed. See [v2/README.md](v2/README.md).
> 5. **The seed is not yet revealed**, so the assignment in `key.json` cannot yet be reproduced independently.


**Status:** complete. Valid under its own frozen decision rule (the positive control F6 was detected by both procedures), but see errata 4: the v1 evaluator's clean-case result does not hold.

## Timeline (all in git history)

| Step | Commit | Time (UTC−5) |
| --- | --- | --- |
| Seed hash published by the author | `598f287` | 2026-10-21 15:21 |
| Design and scripts frozen (SHA-256 in [FROZEN.md](FROZEN.md)) | `4609f3e` | 2026-10-21 |
| Author ran `assign.py`; seed hash matched the commitment | `ae55a24` | 2026-10-21 |
| Blind results recorded, before the key ([results.json](results.json)) | `5752808` | 2026-10-21 16:09 |
| Key revealed ([key.json](key.json)) | `a17467f` | 2026-10-21 16:10 |

The scripts that produced the results (`protocol_lib.py`, `run_checks.py`, `score.py`) matched their frozen hashes at run time.

## Results

21 cases: 3 per fault class and 6 clean. [scoreboard.json](scoreboard.json) has the per-case detail.

| Class | Planted fault | Baseline detected | Protocol detected | Protocol check that fired |
| --- | --- | ---: | ---: | --- |
| F1 | A dependency arrived prebuilt; the build log is clean | 0/3 | **3/3** | P1 artifact check |
| F2 | The solution statement differs from the pinned reference (labeled "weakened" in v1; see errata 2) | 0/3 | **3/3** | P2 statement provenance |
| F4 | The oracle failed, but the harness reported a complete run | 0/3 | **3/3** | P5 harness integrity |
| F5 | A receipt names a log the build did not write | 0/3 | **3/3** | P6 receipts |
| F6 | Positive control: the solution depends on `sorry` | 3/3 | 3/3 | Baseline axioms check |
| C | No fault (incomplete under v2; see errata 4) | 0/6 false alarms | **0/6** false alarms (v1 evaluator only) | — |

**Classes detected by the protocol and not by the baseline:** F1, F2, F4, F5.

## What this supports

On these 21 controlled cases, the protocol detected four classes of fault that the baseline procedure did not. The v1 evaluator raised no false alarms on the six clean cases, a result withdrawn by errata 4. The baseline worked as intended where it applies: it caught every positive control.

In the terms of [FINDINGS.md](../../FINDINGS.md): the protocol makes visible hidden prebuilt artifacts, a statement that differs from its pinned reference, a test harness that hides oracle failures, and run records that do not match their artifacts. The documented baseline does not read the artifacts where these faults live.

## What it does not support

- **Not a real-world detection rate.** The faults are planted, one per case, in controlled artifacts.
- **The outcome follows from the design.** Each fault lives in an artifact the baseline does not read, so the baseline cannot see it; F5 is undetectable by the baseline by construction and is reported only for completeness. The experiment confirms that the protocol's checks work as specified and cover those gaps. It does not show they would catch faults of other kinds.
- **Checks over recorded artifacts, not live Lean.** No Lean, Comparator or kernel was re-run here; those live runs are the main study.
- **Small and deterministic.** Three instances per class; the seed only fixed which case number got which fault.
- **F3 was withdrawn** before freezing ([F3_WITHDRAWN.md](F3_WITHDRAWN.md)).

## Pending

The author reveals the seed file itself, so anyone can rerun `assign.py` and reproduce `key.json` exactly ([SEED_COMMITMENT.md](SEED_COMMITMENT.md), rule 3).
