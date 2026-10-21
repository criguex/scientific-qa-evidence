# Reproducing this release

How to repeat every result in this package from a clean checkout, and which results are recomputed versus only verified by hash.

## 1. What each step proves

| Result | How you check it | Recomputed or verified? |
| --- | --- | --- |
| Every curated file is the one that was published | `shasum -a 256 -c evidence/SHA256SUMS.txt` | Verified by hash |
| The saved 84-case runs are intact and agree across hosts | `python3 evidence/verify_numerical.py` | Verified: recorded hashes and cross-host comparison of saved values |
| The numerical campaign gives the same results | `test_runner.py` (below) | **Recomputed:** all 84 variants run again and are compared with the saved records |
| The runner handles oracle and simulator failures | `test_runner.py` | **Recomputed:** forced exceptions, NaN oracles, export failure |
| README, CLAIMS and the records agree | `python3 evidence/test_consistency.py` | Checked against the machine-readable records |
| The animation pages and manifest come from the evidence | `animations/test_build.py` | **Recomputed:** pages and manifest regenerated, hashes of inputs checked |
| OpenAI's challenge text matches DeepMind's statement | `compare_statements.py` (below) | **Recomputed** from the two pinned files you download |
| Lean builds, Comparator runs, statement mutants, leanchecker | Section 4 | Not reproducible from this repository alone; the saved logs and receipts are verified by hash |

## 2. Quick check (Python only, about a minute)

Requires git and Python 3.9 or newer. No third-party packages.

```sh
git clone https://github.com/criguex/scientific-qa-evidence.git
cd scientific-qa-evidence
git checkout v1.0
shasum -a 256 -c evidence/SHA256SUMS.txt          # on Linux, sha256sum -c also works
python3 evidence/verify_numerical.py
(cd evidence/numerical/source && python3 -m unittest -v test_runner)
python3 evidence/test_consistency.py -v
python3 -m unittest discover -s animations -p 'test_*.py'
(cd evidence/formal/comparator && python3 -m unittest test_sanitize_comparator_logs)
(cd evidence/formal/statement-provenance && python3 -m unittest test_compare_statements)
```

The same commands run in [GitHub Actions](.github/workflows/verify.yml) on Ubuntu and macOS with Python 3.9 and 3.12. The release notes of tag `v1.0` link the successful run for that exact commit, with its logs.

To rerun the numerical suite into a new folder and inspect the raw output:

```sh
cd evidence/numerical/source
python3 runner.py --out /tmp/sqe-rerun     # must not exist yet
```

Expected: 84 variants, `KILLED: 54, PASS: 27, SURVIVED: 3`, `collection_complete: true`, no `export_errors`.

## 3. Statement comparison

```sh
cd evidence/formal/statement-provenance
curl -fL -o deepmind.lean https://raw.githubusercontent.com/google-deepmind/formal-conjectures/8bf45ed70d48b2b2a501de9c00b26bfa38c573ee/FormalConjectures/Millenium/NavierStokes.lean
curl -fL -o openai.lean https://raw.githubusercontent.com/openai/NavierStokesAndEuler/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/ComparatorChallenges/NavierStokes.lean
python3 compare_statements.py deepmind.lean openai.lean > /tmp/result.json
diff <(python3 -m json.tool --sort-keys result.json) <(python3 -m json.tool --sort-keys /tmp/result.json)
```

No output from `diff` means the same result: 18 named declarations matching after textual normalization.

## 4. The formal runs (Lean, Comparator, kernels)

These need OpenAI's repository and a Linux host; they cannot be rerun from this package. What was used:

| Item | Version or hash |
| --- | --- |
| Source | `openai/NavierStokesAndEuler` at `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, archive SHA-256 `afd4d2263a4cabefd1317e890b49bc04f8538402c322db4317a08161e834b4b5` |
| Lean and Lake | `leanprover/lean4:v4.34.0-rc2`, commit `6a10ac8`; binary hashes in [`receipts/tools.tsv`](evidence/formal/cd-validation/receipts/tools.tsv) |
| Mathlib and dependencies | Pinned in the source's `lake-manifest.json`; the resolved revisions are in [`receipts/fresh_build_versions.txt`](evidence/formal/cd-validation/receipts/fresh_build_versions.txt) |
| Comparator, lean4export, nanoda, landrun | Revisions and binary hashes in [`receipts/`](evidence/formal/cd-validation/receipts/) |
| Host | Linux x86_64 (WSL2), 12 vCPU, 30 GiB RAM; about 28 GB of disk per build. `landrun` needs Linux Landlock. |

Commands, run from the extracted source:

```sh
# Full build with no downloaded build caches (B4)
XDG_CACHE_HOME="$(mktemp -d)" MATHLIB_NO_CACHE_ON_UPDATE=1 lake --no-cache build

# Comparator (with COMPARATOR_LANDRUN, COMPARATOR_LEAN4EXPORT and COMPARATOR_NANODA pointing to the tools)
lake env <path-to>/comparator ComparatorChallenges/NavierStokes.json
lake env <path-to>/comparator ComparatorChallenges/Euler.json

# Fresh kernel replay
lake env leanchecker --fresh NavierStokes.ComparatorSolution
lake env leanchecker --fresh Euler.Solution
```

A statement mutant is a one-line edit to `ComparatorChallenges/NavierStokes.lean` or `Euler.lean`, followed by the Comparator command. The exact edits are the diffs in [`evidence/formal/cd-validation/mutants/`](evidence/formal/cd-validation/mutants/). Every recorded run, its build, its times, exit code and the SHA-256 of its original log are in [`evidence/formal/cd-validation/README.md`](evidence/formal/cd-validation/README.md) and [`PROVENANCE.md`](evidence/formal/cd-validation/PROVENANCE.md).

## 5. Optional: GIF previews

`python3 animations/export_gifs.py` needs Python Playwright with Chromium and FFmpeg. GIFs are not part of the evidence; they are previews of the HTML scenes.
