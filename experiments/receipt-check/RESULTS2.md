# Results, case 2: a substituted log, and the limit of P6

Run on 2026-10-22 after the [pre-registration](DESIGN2.md) (`a719676`), on a fresh copy of build B4's tree, with Lean 4.34.0-rc2 (`6a10ac8`) and Lake 5.0.0 ([`toolchain.txt`](results2/toolchain.txt)); the pinned clone used was `a719676`. **All nine outcomes came out as registered.**

| Variant | What changed | OpenAI's published procedure (Z) | P6, existence (X1) | Hash check (X2) |
| --- | --- | --- | --- | --- |
| C | nothing | exit 0, `Your solution is okay!` | pass | pass |
| F5 | receipt names `comparator-run.log` | exit 0, same | flags: log missing | flags: log missing |
| **F7** | `comparator.log` replaced by the authentic Comparator log of another run (build B5); receipt unchanged | exit 0, same | **pass: does not detect it** | **flags: `H:log-hash-mismatch-comparator.log`** |

Z's output for F5 and F7 is byte-identical, and identical to F5 in case 1. C's output differs only by 13 `Built …` lines, because the first Comparator call in a fresh copy also built the Comparator executable. Every step's command, log hash and exit code are in [`results2/receipts.jsonl`](results2/receipts.jsonl); the bundles and their differences from C are in [`results2/`](results2/).

## The claim

> **In this experiment, a stale log under the right name passed OpenAI's published procedure and this study's existence check P6, and was flagged only by comparing it with the hash recorded when the step ran.** Like case 1, this is a traceability inconsistency that does not change Comparator's result, not an accepted false proof.

It shows the value of binding receipts to artifact hashes, and a limit of P6, which checks only that the named log exists. **Limit of the hash check:** it detects a change relative to a trusted reference value, here the hash recorded when the step ran; it does not authenticate where a log came from if someone can replace both the file and that recorded value. One case.

## Prior art

**Not a new technique.** Binding each step's command, inputs and outputs to recorded hashes is established practice in software supply-chain security: [in-toto](https://in-toto.io/) records, for every step, the command, the hashes of its input and output files, its return value and its standard output and error, signs them and verifies them against a layout, and [SLSA provenance](https://slsa.dev/provenance/v1) records how a build was made and from which hashed dependencies. Both faults tested here are of the kind in-toto already detects. This is therefore a **case study of integrity controls for Lean evidence**; a fair comparison with in-toto or SLSA has not been done, and any added value in integration, Lean-specific diagnostics or ease of use would still have to be shown.

## Notes

- Before the registration commit, `check_hash.py` was tried on case 1's bundles C and F5 to see that it ran; F7 was not tried before the run.
- As in case 1, the project was built once (the copy of B4 was already built); only Comparator was run once per variant.
- `python3 -m unittest test_results` recomputes X1 and X2 on the published bundles and checks the byte-identities above.
