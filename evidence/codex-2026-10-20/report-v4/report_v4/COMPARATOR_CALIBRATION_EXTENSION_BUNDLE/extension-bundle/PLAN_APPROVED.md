# NS-08 calibration extension — plan only

Status: local fixtures and reviewed-harness draft prepared. No staging, build,
Comparator invocation, or remote write has occurred. Awaiting root review/GO.

## Proposed serial cases

Use the already-pinned Comparator, Lean/Lake 4.34.0-rc2, lean4export, nanoda,
and Landrun. Keep enable_nanoda=true, the existing permitted-axiom allowlist,
upstream Landrun --best-effort, and the exact hardened outer systemd profile
from the accepted calibration. Run one transient unit per case, sequentially,
with fresh case directories and no .lake cache. No source, toolchain, package,
or formal checkout changes.

1. alpha — Positive. Challenge:
   theorem target : ∀ n : Nat, n = n := fun n => rfl
   Solution proves the identical proposition with binder name k instead of n.
   Expected exit 0, successful builds/exports, nanoda + Lean kernel acceptance,
   and Comparator's success message. This specifically checks binder-name
   irrelevance.
2. hidden_axiom — Transitive unpermitted axiom. Challenge proves target : True
   with True.intro. Solution declares forbidden : True, proves bridge : True
   from forbidden, then target : True from bridge. Expected nonzero exit 1 with
   exact diagnostic Illegal axiom detected: 'forbidden' after successful
   challenge/solution builds and exports, before either kernel.
3. weakened_condition — Valid, weaker statement. Challenge proves
   target : ∃ n : Nat, n > 0 using witness 1. Solution proves
   target : ∃ n : Nat, n ≥ 0 using witness 0. Both proofs are intended to be
   valid; the second statement admits zero and is not the same proposition.
   Expected exit 1 with exact statement-mismatch diagnostic for target after
   both builds and exports, before either kernel.

For both negatives, a compile/export failure, sandbox failure, timeout, OOM, or
missing expected diagnostic is INFRA_PENDING/inconclusive, never a successful
negative. Never label either negative as a kernel rejection.

## Candidate remote root

<WSL_HOME>/ns08_validation_20261020_a5YGak/calibration_20261020T2002Z_ns08extra_5r9k2m/

This is only a proposed path; it has not been checked for absence or created.
The v3-derived launcher verifies every fixture/config/toolchain hash, records
versions and binary hashes, checks actual active unit profile values, checks
no socket FDs and CapEff=0 / NoNewPrivs=1 / Seccomp=2, and retains stdout,
stderr, GNU time, status, journal, cgroup, guard and hashes. Post-exit transient
unit defaults are informational only. Cases are scheduled as:

- alpha (expected positive)
- hidden_axiom (expected forbidden-axiom rejection)
- weakened_condition (expected statement-mismatch rejection)

## Explicit exclusions

No fourth case, no Mathlib dependency, no install/update, no lake update, no
security relaxation, no Comparator run, and no assertion of universal
zero-false-positive behavior or adversarial clean-start independence.
These controls do not replace independent human review or mathematical
certification.
