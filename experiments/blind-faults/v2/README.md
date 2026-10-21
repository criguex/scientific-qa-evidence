# Evaluator v2 and deterministic regression benchmark

v1 (`../protocol_lib.py`, frozen in `../FROZEN.md`) is kept unchanged so its published results stay reproducible. v2 is a separate, corrected evaluator, written after an external review of the v1 results on 2026-10-21.

## What v2 fixes

| v1 defect | v1 behavior | v2 behavior |
| --- | --- | --- |
| Incomplete evidence | An empty or truncated axioms report was **accepted** by both procedures | Fails closed: `axioms-incomplete` |
| Absent evidence | A missing artifact raised `KeyError`, giving no verdict | Fails closed: `missing:<artifact>`, in both procedures |
| Receipts | P6 assumed `comparator.log` existed; **no case contained it** | Receipts are checked against the files actually present |
| Comparator output | Not part of the case | `comparator.log` is a required artifact; the baseline requires `Your solution is okay!` |

Tests for absent and incomplete evidence: [`test_protocol_v2.py`](test_protocol_v2.py) (10 tests, run in CI).

### v2.1: second review round (2026-10-21)

A second review found three more cases where v2 did not fail closed. Each now has a regression test, and all five new tests fail against the previous version (`793ff3b`):

| Defect | Before (v2) | Now (v2.1) |
| --- | --- | --- |
| A numerical summary that is valid JSON but not an object, such as `[]` | `AttributeError`, no verdict | Rejected: `numeric-summary-not-object` |
| Receipt and artifact tables with a header but no rows | Accepted | Rejected: `receipt-no-rows`, `oleans-no-rows`; wrong headers are also rejected |
| Receipts whose exit code is not 0 | Accepted | Rejected: `receipt-exit-<step>-<code>`; receipts must also cover both `build` and `comparator` |

15 tests in total. The benchmark outcome is unchanged.

### Review rounds 3 and 4 (2026-10-21, by the assistant)

| Round | Method | Found | Fixed in | Evidence |
| --- | --- | --- | --- | --- |
| 3 · robustness | Deterministic fuzzer ([`fuzz_v2.py`](fuzz_v2.py), seed 20261021): 8,000 evaluations of mutated artifacts (truncation, garbage, CRLF, BOM, shuffled, duplicated and dropped lines, non-object JSON). Invariant: never raise. | **0 crashes** in v2.1. The fuzzer is not weak: against v2 (`793ff3b`) it finds 52 crashes, the round-2 `[]` defect. | — | `python3 fuzz_v2.py`; runs in CI |
| 4 · semantics | Targeted attempts to make bad evidence pass and good evidence fail | **7 defects**, below | v2.2 | 8 tests in `Round4SemanticTests`; 7 fail against v2.1 (`94244a4`) |

Round 4 defects:

| # | Kind | Input | v2.1 | v2.2 |
| --- | --- | --- | --- | --- |
| 1 | False accept | A second axioms line listing `sorryAx` | Only the first line was read | Every axioms line is checked |
| 2 | False accept | An axioms report for a different theorem | Theorem name ignored | The proved theorem must have its own axioms line |
| 3 | False accept | Comparator log with `Your solution is okay!` and also a failure | Accepted | Any failure marker rejects |
| 4 | False accept | Build log with an `error:` line and the success line | Accepted | Any error line rejects |
| 5 | False accept | Summary with `oracle_valid: false` but marked complete | Accepted | Rejected: `oracle-not-valid` |
| 6 | False alarm | A receipt starting with a UTF-8 BOM | Rejected as a bad header | BOM and CRLF are normalized away |
| 7 | False alarm | A harmless comment in the proved statement | Flagged as a different statement | Comments are stripped before comparing; a real change is still flagged (guard test) |

Resisted in round 4 without changes: CRLF line endings, axioms in a different order, a duplicated receipt whose second run failed, and an inconsistent `.olean` row.

**Total: 24 tests** (23 unit tests plus the fuzzer). The benchmark outcome is unchanged in every round.

## v2 applied to the v1 cases

Running v2 over the 21 published v1 cases ([`v2_on_v1_cases.json`](v2_on_v1_cases.json)) flags **all 21, including the 6 clean ones**: their receipts name a `comparator.log` that does not exist, and they contain no Comparator output. So the v1 result of "0 false alarms on clean cases" depended on the v1 evaluator assuming evidence that was not there. The v1 clean cases were incomplete, not clean.

## v2 benchmark

A deterministic regression benchmark, not a blind trial: one case per class built from the complete v2 template, because a deterministic evaluator gives the same verdict for every instance of a class. [`benchmark_v2.json`](benchmark_v2.json), produced by [`run_benchmark_v2.py`](run_benchmark_v2.py):

| Class | Planted fault | Baseline | Protocol | Protocol check |
| --- | --- | --- | --- | --- |
| C | none (clean) | pass | pass | — |
| F1 | a dependency arrived prebuilt; build log clean | pass | **flag** | P1 |
| F2 | the solution statement differs textually from the pinned reference | pass | **flag** | P2 |
| F4 | the oracle failed but the harness reports a complete run | pass | **flag** | P5 |
| F5 | a receipt names a log the build did not write | pass | **flag** | P6 |
| F6 | positive control: depends on `sorry` | flag | flag | baseline axioms |

**F2 is a textual difference, not a weakening.** Its edit changes the hypothesis `nu > 0` to `nu >= 0`. Relaxing a hypothesis makes the theorem stronger, not weaker. F2 shows only that P2 detects a statement that differs from its reference.

## Cost

| What | Measured |
| --- | --- |
| Evaluating one case's artifacts | Baseline ≈ 3–4 µs, protocol ≈ 8–9 µs on the author's Mac (`seconds_per_case` in `benchmark_v2.json`) |
| Producing the evidence the protocol reads | Not measured by this benchmark. From the main study: a no-cache Lean build took 1 h 29 min, each Comparator run 7–11 min, and each `leanchecker --fresh` replay about 20 min ([cd-validation](../../../evidence/formal/cd-validation/README.md)). |

The microsecond figures are the cost of checking artifacts that already exist. They say nothing about the cost of generating them, which dominates in practice.
