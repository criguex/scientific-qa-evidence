# Build B5: a second build from source, for release v1.3.0

On 2026-10-21/22 OpenAI's repository was built again from the pinned tarball, with nothing prebuilt, to check that the result does not depend on any earlier build. Same host, toolchain and checker binaries as B4 ([B4 record](../cd-validation/README.md#builds-used-by-each-run), [tool hashes](../cd-validation/receipts/tools.tsv)).

| Step | Command | Start (UTC) | End (UTC) | Exit | Result |
| --- | --- | --- | --- | --- | --- |
| Tarball | `sha256sum -c` against `afd4d226…` | | | 0 | OK ([`tarball_sha.txt`](tarball_sha.txt)) |
| Build | `XDG_CACHE_HOME=<empty dir> MATHLIB_NO_CACHE_ON_UPDATE=1 lake --no-cache build` | 2026-10-21T23:56:44Z | 2026-10-22T01:12:24Z | 0 | 11,424 jobs, 1 h 15 min 39 s |
| Comparator · Navier–Stokes (C, D) | `lake env <comparator> ComparatorChallenges/NavierStokes.json` | 01:12:24Z | 01:19:02Z | 0 | **ACCEPTED** by nanoda and the Lean kernel, 6 min 38 s |
| Comparator · Euler | `lake env <comparator> ComparatorChallenges/Euler.json` | 01:19:02Z | 01:30:08Z | 0 | **ACCEPTED** by nanoda and the Lean kernel, 11 min 6 s |
| Clay bridges | `lean --root=. ClayLiteral.lean`, then `Bridges.lean`, against B5 | 01:30:09Z | 01:30:17Z | 0 | `k1_C`, `k1_D`, `k1_C_oneSided`, `k1_D_oneSided` and both non-vacuity controls: `[propext, Classical.choice, Quot.sound]` |

**Nothing was prebuilt** ([`build_facts.txt`](build_facts.txt)): 0 Reservoir barrels, 0 files in the build cache directory, and every one of the 11,406 `.olean` files (Mathlib 8,371, project 2,659, dependencies 376) is newer than the build start. The bridge inputs have the same SHA-256 as in [`bridges/README.md`](../../../bridges/README.md) ([`inputs.sha256`](inputs.sha256)).

Records: [`receipts.tsv`](receipts.tsv), [`versions.txt`](versions.txt) (**empty**: the wrapper ran the version commands outside the project, where no toolchain is configured; the versions, recorded afterwards from the same binaries, whose hashes match the B4 record, are in [`versions-recorded-after.txt`](versions-recorded-after.txt)), [`build.time.txt`](build.time.txt), the SHA-256 of the full build log ([`build.log.sha256`](build.log.sha256); the log itself is not published), Comparator stdout, stderr and timing per challenge, and the Lean compile and axiom logs. Host paths are replaced with `<path>`.

**Limits.** Same single Linux host and the same reused Lean toolchain and checker binaries as B1–B4; an outside rebuild remains the stronger check.
