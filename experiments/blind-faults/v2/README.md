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
