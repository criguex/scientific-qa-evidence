# Blind-fault experiment: design (DRAFT, not frozen)

**Question.** On small, controlled cases, which planted faults does this study's protocol detect that the baseline procedure does not, and at what cost in false alarms and time?

**Status.** Draft for review by the author. It becomes binding when its SHA-256 is published in `FROZEN.md`. After that, any change is a new experiment.

## 1. The two procedures

**Baseline (B).** The procedure documented in OpenAI's repository: build the Lean project with `lake build`, run Comparator with its JSON configuration, and accept if it prints `Your solution is okay!`. For numerical cases: run the case's test suite and accept if it reports success.

**Protocol (P).** The baseline, plus the protocol's own checks:

| Check | What it does |
| --- | --- |
| P1 · artifact check | Compare `.olean` timestamps with the build start and look for downloaded archives |
| P2 · statement provenance | Compare the challenge file with a pinned public reference using `compare_statements.py` |
| P3 · statement mutants | One-symbol mutants of the challenge plus a comment-only control; Comparator must refuse the mutants and accept the control |
| P4 · kernel currency | Compare the toolchain's `src/kernel` tree and the nanoda commit with known soundness fixes |
| P5 · harness fault injection | Force oracle and simulator failures and check the harness reports them |
| P6 · receipts | Check that every reported run has a command, exit code and original hash that match its artifacts |

## 2. Cases

Each case is a small, fast copy: a core-Lean project without Mathlib (a challenge statement, a solution and a Comparator configuration), or one numerical model from this repository's suite. All cases use the same templates, so a fault is the only difference.

| Class | Planted fault | Instances | Why B could pass it |
| --- | --- | ---: | --- |
| F1 | Prebuilt `.olean` files for a dependency placed in the build directory instead of compiling it | 3 | The build succeeds and Comparator accepts |
| F2 | The challenge statement is weakened and the solution proves the weaker statement; the case's reference statement is unchanged | 3 | Comparator compares the solution with the challenge, and they match |
| F4 | The numerical oracle raises an exception, and the harness reports the case as passing | 3 | The suite reports success |
| F5 | A run receipt names a different build or log than the one actually used | 3 | B keeps no receipts |
| F6 | Positive control: the solution uses `sorry` or a non-permitted axiom | 3 | It should not; Comparator rejects this, so both procedures should detect it |
| C | Clean copies with no fault | 6 | Measures false alarms |

**Total:** 21 cases, named `case-01` to `case-21`. Class F3 was withdrawn before freezing; see [F3_WITHDRAWN.md](F3_WITHDRAWN.md).

F6 checks that the baseline works as intended; if B misses F6, the setup is broken. F5 cannot be detected by B by construction, and it is reported separately so it does not inflate the comparison.

## 3. Assignment and blinding

1. The seed committed in [SEED_COMMITMENT.md](SEED_COMMITMENT.md) is the only source of randomness.
2. `assign.py` (to be written and frozen with this design) builds the list of 21 slots above, shuffles it with Python's `random.Random(seed)`, plants each fault into its copy, and writes `key.json` mapping case to class.
3. The author runs `assign.py` on his machine and keeps `key.json` and the seed out of the assistant's reach until all results are recorded.
4. The checks are run with case names only. Each result is committed before the key is opened.

## 4. Outcomes and metrics

- **Flagged:** a procedure reports a problem for a case, recorded with the check that raised it.
- **Detection rate:** flagged faulty cases ÷ faulty cases, per class and per procedure.
- **False alarm rate:** flagged clean cases ÷ clean cases, per procedure.
- **Cost:** wall-clock time per case and procedure.
- Results are reported as counts (for example "B 0/3, P 3/3"). With 3 instances per class there are no significance tests; the experiment shows whether a difference exists on these cases, not how large it is in general.

## 5. Decision rules, fixed in advance

- A case counts as detected by a procedure only if that procedure flags it during the blind phase.
- No case is removed after unblinding. A case that cannot be run counts as not detected, with the reason recorded.
- If F6 is not detected by both procedures, the experiment is reported as invalid, not partially.

## 6. What it can and cannot support

**Can support:** "On these 21 planted cases, the protocol detected classes F1, F2, F4 and F5 that the baseline did not, with N false alarms on 6 clean cases, at a cost of T."

**Cannot support:** detection rates for real-world faults, behavior on large projects, or superiority over procedures other than this baseline.

## Decisions taken (2026-10-21)

1. Three instances per class, 21 cases in total.
2. F3 was first included, then **withdrawn before freezing** after an automated safety filter stopped the assistant's work on it; see [F3_WITHDRAWN.md](F3_WITHDRAWN.md).
3. F5 stays and is reported separately, because the baseline cannot detect it by construction.

## Feasibility checks before freezing

| Item | Status |
| --- | --- |
| `assign.py`, case templates and check scripts | Pending |
