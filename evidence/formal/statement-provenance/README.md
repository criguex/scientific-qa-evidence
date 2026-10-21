# Is OpenAI's challenge the public DeepMind statement?

**Finding (2026-10-21):** The 18 declarations match after textual normalization; name resolution was not verified. After removing comments, attributes and whitespace, every named declaration in OpenAI's Comparator challenge, including the breakdown theorems (C) and (D), is textually the same as in Google DeepMind's public Formal Conjectures file. The remaining differences are imports, namespace and notation.

**Scope.** This is a textual comparison. It does not show semantic identity. That would require comparing the elaborated declarations and their constants and dependencies in Lean, to prove that the different imports, namespace and notation do not change the meaning. That comparison was not done.

| | Reference | Candidate |
| --- | --- | --- |
| File | [`FormalConjectures/Millenium/NavierStokes.lean`](https://github.com/google-deepmind/formal-conjectures/blob/8bf45ed70d48b2b2a501de9c00b26bfa38c573ee/FormalConjectures/Millenium/NavierStokes.lean) | [`ComparatorChallenges/NavierStokes.lean`](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/ComparatorChallenges/NavierStokes.lean) |
| Repository and commit | google-deepmind/formal-conjectures `8bf45ed` | openai/NavierStokesAndEuler `f9e8bc5` |
| SHA-256 | `f446284f2aa54375f558c263a580b34e2e7bc9f44a28829637199cc72257d25d` | `0cd193b8d5cbd0266e6e2f72e68dd5abcdcf2430ebd435dd9289737e9aa7da61` |

## Result

**20 blocks are identical** after removing comments, attributes and whitespace: `open scoped Laplacian`, `variable {n : ℕ}` and 18 named declarations. Those are `divergence` and its five helper lemmas, `IsOnePeriodic`, the six initial-velocity and force conditions, the three solution classes, and the two breakdown theorems `navier_stokes_breakdown_R3` (C) and `navier_stokes_breakdown_periodic` (D).

The only differences:

| Difference | Why it does not change the mathematics |
| --- | --- |
| `import FormalConjecturesUtil` → `import Mathlib` | The challenge must compile without DeepMind's helper library. |
| Namespace `NavierStokes` → `NavierStokes.Comparator` | A name prefix only. |
| `EuclideanGeometry` dropped from the `open` line | Upstream it supplies the scoped `ℝ^n` and `ℝ³` notation, which is now defined locally. OpenAI's file compiles without the `open`; the "Not checked" note below covers name resolution. |
| `ℝ^n` and `ℝ³` notation copied into the file as `local notation` | Upstream defines them as `EuclideanSpace ℝ (Fin n)` and `EuclideanSpace ℝ (Fin 3)` in `FormalConjecturesForMathlib/Geometry/Euclidean.lean` and `Geometry/3d.lean` at the same commit. The copies are the same definitions. |
| `∇⬝` notation made `local` | Scope only. |
| The existence theorems (A) and (B) are removed | OpenAI's submission addresses (C) and (D), so only those are challenged. |

Also checked by reading the pinned Mathlib: `∞` in `ContDiff ℝ ∞` is `((⊤ : ℕ∞) : WithTop ℕ∞)`, i.e. C^∞ smoothness, not analyticity (`ω`). `Δ` is Mathlib's `Laplacian.laplacian`, and `gradient` is Mathlib's `gradient`.

**Not checked:** whether any name resolves differently in the two files, for example because DeepMind's helper library or the `EuclideanGeometry` namespace shadows a Mathlib name such as `gradient`. In OpenAI's file those names resolve to Mathlib.

## What this does and does not show

Within that scope, it shows that OpenAI's challenge text was not adapted from the public statement. The question "does the formal statement say what Clay says?" now concerns the public DeepMind statement, not a file written by the prover. It does not answer that question; see [`../clay-lean-risk.md`](../clay-lean-risk.md).

## Reproduce

```sh
curl -fLO https://raw.githubusercontent.com/google-deepmind/formal-conjectures/8bf45ed70d48b2b2a501de9c00b26bfa38c573ee/FormalConjectures/Millenium/NavierStokes.lean
mv NavierStokes.lean deepmind.lean
curl -fLO https://raw.githubusercontent.com/openai/NavierStokesAndEuler/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/ComparatorChallenges/NavierStokes.lean
mv NavierStokes.lean openai.lean
python3 compare_statements.py deepmind.lean openai.lean
```

The output must match [`result.json`](result.json). The comparator uses only the Python standard library and has its own tests in [`test_compare_statements.py`](test_compare_statements.py).
