# Case 2: a substituted log, and the limit of P6

**Pre-registered on 2026-10-22, before any run.** **Results: [RESULTS2.md](RESULTS2.md)** — all nine outcomes as registered. Expected outcomes: [`expected2.json`](expected2.json); scripts: [`run2.sh`](run2.sh), [`check_hash.py`](check_hash.py), [`check_p6.py`](check_p6.py).

## Why a second case

Case 1 ([results](RESULTS.md)) showed P6 catching a receipt that names a missing log. But P6 only checks that the named log **exists**. A realistic fault is a log that exists under the right name but comes from another run: a stale or swapped log. P6 would not catch it. This case tests that limit openly, and whether a check against the hash recorded when the bundle was written does catch it.

## Variants, on the same bundle and a fresh copy of build B4's tree

| Variant | Change | Expected Z | Expected X1 (P6) | Expected X2 (hash) |
| --- | --- | --- | --- | --- |
| C | none | exit 0 | pass | pass |
| F5 | receipt names `comparator-run.log` (as in case 1) | exit 0 | flag: log missing | flag: log missing |
| **F7** | `comparator.log` replaced by the authentic Comparator log of another run of the same step (build B5, also accepted); receipt unchanged | exit 0 | **pass: P6 does not detect it** | **flag: hash mismatch** |

The bundle is case 1's clean bundle, whose step log hashes were recorded at the moment each step ran (`results/receipts.jsonl`, variant `bundle`). X2 compares against those recorded hashes.

## The claim this can support

> In this case, a stale log under the right name passed OpenAI's published procedure and this study's existence check P6, and was caught only by comparing it with the hash recorded when the step ran.

That shows both the value of hash-bound receipts and a limit of P6. It is about the traceability of evidence, not the proof. If X2 misses F7 or flags C, that will be reported.
