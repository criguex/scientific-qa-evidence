# Status

**Attempt 1, 2026-10-22: aborted during setup. No result.** Copying build B5's tree (about 26 GB) to a scratch location filled the host machine's Windows system drive, which holds the WSL virtual disk, and the copy failed with I/O errors. No step of procedure Z or check X ran, so there is nothing to compare, and the registered expectations in [`expected.json`](expected.json) are untouched. The scratch copies were deleted afterwards.

**Next.** The comparison will be rerun once the host has room again. Any change to the setup made before that run, for example running in place instead of on a copy, will be recorded here as an amendment before the run, together with the reason.

**Amendment 1, 2026-10-22, before any step ran.** B5's build tree was deleted to free the host drive (its records stay in [`evidence/formal/b5/`](../../evidence/formal/b5/README.md)), so the copy is made from build B4's tree instead, which was also compiled from source with `lake --no-cache build` ([B4 record](../../evidence/formal/cd-validation/README.md#builds-used-by-each-run)). `run.sh` now measures the host's system drive before and after the copy and aborts below 40 GB and 15 GB free. Nothing else changes: same procedure Z, same check X, same variants, same expected outcomes.
