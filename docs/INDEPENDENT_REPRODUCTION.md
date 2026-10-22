# Independent reproduction guide

Every run recorded in this repository was made by its author, with an AI assistant, on the same two machines. Those runs count, but they are not independent. This guide is for someone else who wants to rebuild OpenAI's proofs from a fixed version, check them, and publish what they got. A run that disagrees with ours is as useful as one that agrees.

## What is fixed

| Input | Pin | How to check it |
| --- | --- | --- |
| OpenAI's source | [openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler), commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` | Content manifest below. The archive bytes are not stable: the archive we pinned in October 2026 has SHA-256 `afd4d226…834b4b5`, a fresh GitHub download has a different one, and both extract to the same 2,669 files |
| Content manifest | `95bb21c93e834581e1400e31e33a9fb7943db2f64f11425b034f97b9b52e95fc` | Command in step 1; the same value on macOS and on Linux |
| Lean toolchain | `leanprover/lean4:v4.34.0-rc2` (commit `6a10ac8`), from the project's `lean-toolchain` | `lean --version` inside the project |
| Comparator and its checkers | [leanprover/comparator](https://github.com/leanprover/comparator) `19e111e2141cf333c7daff0f64c5f24acc91dd2e`; lean4export `cacf989bd75f608700820f6afc595f32e7a99a4d`; nanoda_lib `9d6964f78d0fa4c93fd22fe956e17afe7e72a441`; landrun `ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a` | Build them following Comparator's README at those revisions and record the SHA-256 of each binary you use. Ours are in [the B4 record](../evidence/formal/cd-validation/README.md#reused-tools) |
| Clay bridges | [`bridges/ClayLiteral.lean`](../bridges/ClayLiteral.lean) and [`bridges/Bridges.lean`](../bridges/Bridges.lean) from this repository | SHA-256 listed in [`bridges/README.md`](../bridges/README.md) |

## Steps

Linux x86_64 with about 30 GB of free disk and 16 GB of memory is enough; our build took 1 h 15 min on 12 cores. Run every step in Bash, from the project directory, after defining this helper. It sends each command's output to a log and records the command's own exit code (not that of `tee`) with its start and end time in `../exit_codes.tsv`:

```
set -o pipefail
step() {
  local name=$1 start rc; shift
  start=$(date -u +%FT%TZ)
  "$@" 2>&1 | tee "../$name.log"; rc=${PIPESTATUS[0]}
  printf '%s\t%s\t%s\t%s\n' "$name" "$start" "$(date -u +%FT%TZ)" "$rc" >> ../exit_codes.tsv
  return "$rc"
}
```

1. **Get the source and check it.**
   ```
   git clone https://github.com/openai/NavierStokesAndEuler.git && cd NavierStokesAndEuler
   git checkout f9e8bc5b38b6e212696e8a30e3e91517af887bbd
   (LC_ALL=C find . -path ./.git -prune -o -type f -print | LC_ALL=C sort | while IFS= read -r f; do sha256sum "$f"; done) | sha256sum
   ```
   Expected: `95bb21c9…52e95fc`. (On macOS use `shasum -a 256` for both `sha256sum`.)
2. **Build from source, with no prebuilt files.**
   ```
   mkdir -p ../xdg
   step build env XDG_CACHE_HOME=$PWD/../xdg MATHLIB_NO_CACHE_ON_UPDATE=1 lake --no-cache build
   ```
   Expected: exit 0. Ours: 11,424 jobs.
3. **Run Comparator on both challenges.**
   ```
   step comparator_NavierStokes lake env <path-to-comparator> ComparatorChallenges/NavierStokes.json
   step comparator_Euler lake env <path-to-comparator> ComparatorChallenges/Euler.json
   ```
   Expected: exit 0 and `Your solution is okay!` for each.
4. **Compile the Clay bridges against your build and print their axioms.** Copy `ClayLiteral.lean` and `Bridges.lean` from this repository into the project root, check their SHA-256, and create `Axioms.lean` there:
   ```
   import Bridges
   #print axioms Bridges.k1_C
   #print axioms Bridges.k1_D
   #print axioms Bridges.k1_C_oneSided
   #print axioms Bridges.k1_D_oneSided
   #print axioms Bridges.zero_solution_C
   #print axioms Bridges.zero_solution_D
   ```
   Then:
   ```
   step clay lake env lean -o .lake/build/lib/lean/ClayLiteral.olean ClayLiteral.lean
   step bridges lake env lean -o .lake/build/lib/lean/Bridges.olean Bridges.lean
   step axioms lake env lean Axioms.lean
   ```
   Expected: exit 0 for all three, and `depends on axioms: [propext, Classical.choice, Quot.sound]` for each of the six theorems. The three `lake env lean` commands were tested on 2026-10-22 against build B4.
5. **Record the versions,** inside the project directory: `lean --version`, `lake --version`, `uname -a`, and the SHA-256 of `lean`, `lake` and each checker binary.

## What to publish

A public page (a gist, a repository, an issue on [this repository](https://github.com/criguex/scientific-qa-evidence/issues)) with the following, filled in:

```
Reproducer:            name or handle, and whether you used AI tools
Date (UTC):
Machine:               OS, CPU, cores, memory
Source commit:         f9e8bc5b38b6e212696e8a30e3e91517af887bbd
Content manifest:      <value from step 1>
lean --version:
lake --version:
Checker binaries:      <name, revision, SHA-256 for comparator, lean4export, nanoda, landrun>
| Step | Command | Start | End | Exit code | Result |
| build | ... | | | | <jobs; any downloaded caches?> |
| comparator NavierStokes | ... | | | | <last line> |
| comparator Euler | ... | | | | <last line> |
| bridges | ... | | | | <axioms printed> |
exit_codes.tsv:         <contents>
Full logs or their SHA-256:
Differences from the expected results, if any:
Deviations from this guide, if any:
```

Results that differ from ours, steps that failed, or steps you could not run are worth publishing too. If you open an issue here, it will be linked from this page as received, without editing what you wrote.

## Reproductions received

None yet.
