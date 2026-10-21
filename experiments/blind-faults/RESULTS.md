# Blind-fault experiment: results

**Status:** complete and valid. The positive control F6 was detected by both procedures, as the frozen decision rule requires.

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
| F2 | The proved statement was weakened; it no longer matches the pinned reference | 0/3 | **3/3** | P2 statement provenance |
| F4 | The oracle failed, but the harness reported a complete run | 0/3 | **3/3** | P5 harness integrity |
| F5 | A receipt names a log the build did not write | 0/3 | **3/3** | P6 receipts |
| F6 | Positive control: the solution depends on `sorry` | 3/3 | 3/3 | Baseline axioms check |
| C | No fault | 0/6 false alarms | **0/6** false alarms | — |

**Classes detected by the protocol and not by the baseline:** F1, F2, F4, F5.

## What this supports

On these 21 controlled cases, the protocol detected four classes of fault that the baseline procedure did not, with no false alarms on the six clean cases. The baseline worked as intended where it applies: it caught every positive control.

In the terms of [FINDINGS.md](../../FINDINGS.md): the protocol makes visible hidden prebuilt artifacts, a weakened statement that still matches its own challenge, a test harness that hides oracle failures, and run records that do not match their artifacts. The documented baseline does not read the artifacts where these faults live.

## What it does not support

- **Not a real-world detection rate.** The faults are planted, one per case, in controlled artifacts.
- **The outcome follows from the design.** Each fault lives in an artifact the baseline does not read, so the baseline cannot see it; F5 is undetectable by the baseline by construction and is reported only for completeness. The experiment confirms that the protocol's checks work as specified and cover those gaps. It does not show they would catch faults of other kinds.
- **Checks over recorded artifacts, not live Lean.** No Lean, Comparator or kernel was re-run here; those live runs are the main study.
- **Small and deterministic.** Three instances per class; the seed only fixed which case number got which fault.
- **F3 was withdrawn** before freezing ([F3_WITHDRAWN.md](F3_WITHDRAWN.md)).

## Pending

The author reveals the seed file itself, so anyone can rerun `assign.py` and reproduce `key.json` exactly ([SEED_COMMITMENT.md](SEED_COMMITMENT.md), rule 3).
