# Were the checkers current with the 2026 kernel soundness fixes?

In 2026 several Lean 4 kernel soundness bugs were found and fixed, and in one case the independent checker nanoda had a separate bug that let the same exploit through ([de Moura, postmortem for #14576](https://leodemoura.github.io/blog/2026-8-1-postmortem-for-kernel-soundness-bug-14576/); [postmortem for the bug hunt](https://leodemoura.github.io/blog/2026-8-24-postmortem-for-the-kernel-soundness-bug-hunt/); [Lean 4.34.0 release notes](https://lean-lang.org/doc/reference/latest/releases/v4.34.0/)). A green Comparator run is only as good as the kernels behind it, so this checks the versions used here against those fixes. Checked on 2026-10-21.

## Lean kernel

The toolchain in every run reports `Lean (version 4.34.0-rc2, … commit 6a10ac8c22beadecabdbb0919c2b50214762f91d)`. The Git tree of `src/kernel` at each release tag of `leanprover/lean4`:

| Tag | Commit | `src/kernel` tree | Relation to the fixes |
| --- | --- | --- | --- |
| v4.33.0 | `d8b1897` | `2de8c537…` | Before the v4.33.1 soundness patch |
| v4.33.1 | `819816b` | `636837af…` | Soundness patch (#14806, #14807, #14808) |
| v4.34.0-rc1 | `3447a66` | `2066bfde…` | Different kernel; listed as affected by advisories |
| **v4.34.0-rc2 (used here)** | **`6a10ac8`** | **`636837af…`** | **Same kernel source as v4.33.1, v4.34.0 and v4.34.1** |
| v4.34.0 | `293d5d0` | `636837af…` | Release announcing three fixed soundness issues |
| v4.34.1 | `5045d00` | `636837af…` | Runtime fixes only; kernel unchanged |

**Result.** The kernel source used in every run is byte-identical, as a Git tree, to the kernel of v4.34.0 and v4.34.1, so it contains every kernel soundness fix released through v4.34.1. The #14576 fix predates both (v4.32.2).

**Not covered.** v4.34.1 also fixes runtime issues outside `src/kernel`; the toolchain used here does not have those. This check compares source trees; it does not rebuild the binaries from source.

Reproduce:

```sh
for t in v4.33.1 v4.34.0-rc1 v4.34.0-rc2 v4.34.0 v4.34.1; do
  gh api "repos/leanprover/lean4/contents/src?ref=$t" -q '.[] | select(.name=="kernel") | "'$t' " + .sha'
done
```

## nanoda

The nanoda used by Comparator is `ammkrn/nanoda_lib` at `9d6964f78d0fa4c93fd22fe956e17afe7e72a441` (2026-10-19, "Merge pull request #58 from ammkrn/nat_fvar"). Per the #14576 postmortem, nanoda's projection-check bug was fixed about a week before that Lean bug was reported in late July 2026, so this commit postdates the fix.

**Not covered.** The fix was located from the postmortem's date, not by identifying the fixing commit in nanoda's history.

## Positive control

The public exploit for #14576 ([`endrazine/lean-cve-poc`](https://github.com/endrazine/lean-cve-poc) at `db52dfd`) proves `0 = 1` with no axioms on Lean v4.31.0, and is refused by the kernel of the v4.34.0-rc2 toolchain used here (exit 1, the forged declaration is not admitted). Details: [F3 reproduction](../../experiments/blind-faults/feasibility/f3-exploit-reproduction.md).

## What this does not change

Two agreeing kernels rule out a bug in only one of them passing a false proof. They do not rule out a shared bug, or two coincident bugs, which is what happened in July 2026. Being current with known fixes says nothing about unknown ones.
