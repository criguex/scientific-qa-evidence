# Curated evidence allowlist

This folder contains a curated allowlist of fixtures and controls cited by the English release, not a copy of the legacy evidence tree. The package checksum list verifies its listed files. The two 84-case campaign datasets use each original host summary's `artifact_sha256` map; validate all 168 cases, both 756-row CSVs, and the cross-host comparison with `python3 evidence/verify_numerical.py` from the package root.

The root checksum list covers every curated release file, including both paired case directories, but excludes generated render outputs, dependency directories, Python caches, and the checksum list itself. The numerical verifier additionally checks the two copied original summaries and every case JSON and observation CSV against those summaries' original per-file SHA-256 maps. Its comparison is read-only; rerunning the calculation suite is a separate action described in the root README.

## Numerical suite

`numerical/summary.mac.json` is the original macOS arm64 run summary. `numerical/multidomain_derived.json` is the original paired-host summary. The complete 84-case records, original summaries, and observations CSVs for macOS arm64 and Linux x86_64 are under `numerical/paired/`. Two byte-preserved RC outputs make one baseline-versus-mutation comparison concrete. The four Python source files are the exact runner and numerical implementations named by the original source hashes. The source contract is described in English in [CLAIMS.md](../CLAIMS.md).

`numerical/source/test_runner.py` tests the runner: an oracle exception must mark the oracle invalid, a system-under-test exception must leave the variant `INCONCLUSIVE`, and a full rerun must reproduce every saved record. `runner.py` was fixed on 2026-10-21; see `SOURCE_PROVENANCE.md` for the hash of the version that produced the saved runs.

The selected results are not a substitute for the full 84-variant run. The 27 PASS, 54 KILLED, and 3 SURVIVED counts are per host. macOS arm64 and Linux x86_64 are paired executions of the same variants.

## Formal controls

`formal/fixtures/` contains the exact Lean fixture sources. `formal/kernel-mutation/` preserves the raw runner summary with its `COLLECTED_PENDING_CLASSIFICATION` status and the separate source-derived classification. Lean reports a type mismatch. nanoda reaches an internal definitional-equality assertion; pinned source analysis derives that as a typechecking rejection. The binary itself emits no structured rejection category, so the raw pending status is retained. `formal/periodic-control/` contains byte-preserved sanitized output and a source manifest for the bounded periodic control. That output lists `propext`, `Classical.choice`, and `Quot.sound` for the periodic declaration. The constant field is on a torus and does not transfer to the Euclidean problem.

`formal/clean-build/summary.en.json` translates the clean03 source-build record. The original summary and manifests are hash-linked there; no original evidence file was rewritten. The adjacent `dependency-pins.txt`, `tool-versions.txt`, and `toolchain.sha256` preserve the selected dependency pins, Lean/Lake versions, and toolchain binary hashes; see the concise [fidelity table](formal/clean-build/README.md). `build-output-excerpt.txt` preserves a sanitized excerpt of the original stdout, including the final status and reported Euler axioms. Comparator evidence is kept separate under `formal/comparator/`, with sanitized run records and original transcript hashes. The 2026-10-21 revalidation (second Comparator run, statement mutants, fresh kernel replay and from-scratch build) is under `formal/cd-validation/`, with sanitized logs, mutant diffs and machine-readable verdicts. `formal/statement-provenance/` compares OpenAI's challenge with DeepMind's public statement, and `formal/clay-lean-risk.md` reviews the formal (C)/(D) against Clay's text clause by clause. `formal/kernel-currency.md` checks the Lean kernel source and the nanoda commit used against the 2026 kernel soundness fixes.

## Privacy and interpretation

The evidence set excludes provider keys, raw voice responses, private IP addresses, host usernames, private source paths, and full legacy artifacts. The flow clip is a visual illustration only, labeled as such in the video source. No evidence here supports theorem discovery, experimental validation, or real-world certification.
