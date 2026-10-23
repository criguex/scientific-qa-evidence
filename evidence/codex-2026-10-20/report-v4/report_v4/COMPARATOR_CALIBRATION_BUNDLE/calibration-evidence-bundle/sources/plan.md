# NS-08 comparator calibration plan — awaiting GO

Status: inspection and fixture preparation only. No build, comparator invocation,
or probe has been run for this calibration.

## Intended controls

All controls use the already-pinned Comparator, Lean/Lake, lean4export, nanoda,
and Landrun binaries from the NS-08 operational toolchain. Each is an isolated
minimal Lake project. The Comparator config sets `enable_nanoda: true` and the
same allowed axioms as the formal run (`propext`, `Quot.sound`, `Classical.choice`).
No user source is compiled before Comparator launches it. Runs would be serial
under the previously validated hardened systemd profile, with Landrun's pinned
upstream `--best-effort` invocation unchanged. No security restriction would be
relaxed.

1. **Positive:** both files prove `target : 0 = 0` by `rfl`. Expected Comparator
   exit 0, nanoda and Lean kernel acceptance messages, and final
   `Your solution is okay!`.
2. **Valid proof, different statement:** challenge proves `target : 0 = 0`;
   solution proves `target : 1 = 1`, each by `rfl`. Both are valid proofs and
   should compile. Expected nonzero Comparator exit with the exact
   `Challenge and solution theorem statement do not match: 'target'` diagnostic.
   A compile/export/sandbox failure does not count as a correct negative.
3. **Unpermitted axiom:** challenge proves `target : True`; solution declares
   `axiom forbidden : True` and proves the same target using it. Both theorem
   statements match. Expected nonzero exit with exact
   `Illegal axiom detected: 'forbidden'` diagnostic. A compile/export/sandbox
   failure does not count as a correct negative.

For controls 2 and 3, evidence must show both challenge and solution builds and
exports completed before the expected Comparator diagnostic. The mismatch must
not be labeled a kernel rejection: it is rejected during statement comparison.
The axiom case must not be labeled a nanoda/Lean kernel rejection: the pinned
Comparator checks the transitive axiom set before invoking either kernel.

## Proposed remote writes after GO

Only create a new, unique directory beneath
`<WSL_HOME>/ns08_validation_20261020_a5YGak/`, e.g. `calibration_<UTC>_<nonce>/`.
Copy each fixture project (`lean-toolchain`, `lakefile.toml`, `config.json`,
`Challenge.lean`, `Solution.lean`) into that directory. Add one reviewed
`run-calibration.sh` launcher there only after GO; it must invoke the existing
Comparator binary with that case's config and no extra arguments/options. For
each case, write separate stdout/stderr, GNU `time` output, wrapper status,
unit/journal metadata, guard results, exact command record, and SHA-256 manifest.
Preserve all outputs, including failed/infra cases. Do not write to the formal
checkout, its `.lake`, or any previously closed bundle. No network, sudo,
package updates, or toolchain changes.

Per case, the launcher must call `systemd-run --user --wait` (without `--pipe`)
with the previously validated properties: `RestrictAddressFamilies=~AF_UNIX`,
`SystemCallArchitectures=native`,
`SystemCallFilter=~@network-io io_uring_setup io_uring_enter io_uring_register`,
`NoNewPrivileges=yes`, `SystemCallErrorNumber=EPERM`,
`MemoryMax=28991029248`, `CPUQuota=800%`, `RuntimeMaxSec=8h`,
`StandardInput=null`, and `StandardOutput`/`StandardError` each appending to
separate, unique files in that run directory. The wrapper must record the actual
unit result and process exit independently; systemd's success alone is not the
test result.

Before each sequential run: verify binary, fixture, and config hashes; verify
the specified unit properties; verify no inherited socket descriptors and
`CapEff=0`. After each run, retain process/cgroup exit, timestamps, resource
data, and output hashes. The expected-negative classification is allowed only
when its exact Comparator diagnostic occurs after successful module builds and
exports, with no timeout, OOM, unit-property failure, or sandbox/tool failure.

## Scope and clean-root gap

These controls test a few Comparator response paths; they do not reproduce the
Navier–Stokes/Euler claims and do not establish adversarial clean-start
independence. Existing formal runs used an already compiled checkout/cache and
Landrun on WSL Landlock ABI 7 with upstream `--best-effort`; the outer systemd
restrictions passed, but this is not ABI 10. A stronger clean-root reproduction
would still need a separately authenticated source/archive and dependency graph,
fresh isolated workspace/VM, independently verified pinned toolchain and
artifacts, trusted dependency/cache preparation without first compiling
submitted solution code, execution from that fresh root under a sandbox with
the required guarantees, and independent human review of the formal statements
and proof assumptions. The fixtures cannot substitute for those steps or for
human mathematical review.

An optional fourth case (well-formed exports but an ill-typed proof, intended to
reach nanoda rejection) is deliberately not part of this batch. It would need a
separate source/config review and explicit authorization; do not add it
implicitly.

## Awaiting authorization

Do not run these controls until root explicitly approves the proposed remote
directory, exact profile/launcher, and fixture hashes.
