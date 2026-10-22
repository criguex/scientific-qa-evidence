# Receipt check on authentic records: a case study of integrity controls

Does a check that each receipt corresponds to the artifact it names catch evidence faults that OpenAI's published verification procedure does not, on the same authentic files? Two pre-registered cases.

| File | Purpose |
| --- | --- |
| [`DESIGN.md`](DESIGN.md), [`expected.json`](expected.json) | Case 1, pre-registered: a receipt names a log that does not exist |
| [`DESIGN2.md`](DESIGN2.md), [`expected2.json`](expected2.json) | Case 2, pre-registered: a stale log from another run under the right name |
| [`STATUS.md`](STATUS.md) | Timeline: an aborted first attempt, one amendment, both runs, the scripts as run, and the hardening after review |
| [`RESULTS.md`](RESULTS.md), [`RESULTS2.md`](RESULTS2.md) | Outcomes, the claim each supports, and recording notes |
| [`run.sh`](run.sh), [`run2.sh`](run2.sh) | Run the published procedure on a copy of a from-source build tree, write the evidence bundle and evaluate each variant; need `QA_COMMIT`; as written they run under WSL on a Windows host, measuring the Windows drive with PowerShell and using that host's local paths |
| [`preflight.sh`](preflight.sh) | Shared checks: host disk space, pinned toolchain, `lake-manifest.json` revisions, tool and Comparator binary hashes; aborts on any mismatch |
| [`check_p6.py`](check_p6.py) | Check X1: P6 from the frozen evaluator v2.2, which tests that each log named by a receipt exists and that steps exited 0 |
| [`check_hash.py`](check_hash.py) | Check X2: each named log must also match the SHA-256 recorded when its step ran |
| [`test_results.py`](test_results.py) | Recomputes both checks on the published bundles and checks that the procedure's output did not change; runs in CI |
| [`results/`](results/), [`results2/`](results2/) | Receipts, bundles, logs and outputs of the two runs |

**Conclusion.** In this experiment, P6 detects a traceability inconsistency that does not change Comparator's result, and a stale log under the right name is caught only by the hash check. It does not mean Comparator accepted a false proof. Binding steps to hashes is established practice ([in-toto](https://in-toto.io/), [SLSA provenance](https://slsa.dev/provenance/v1)); this is a case study, not a new technique, and no comparison with those tools has been made. Review request: [`docs/REVIEW_REQUEST.md`](../../docs/REVIEW_REQUEST.md).
