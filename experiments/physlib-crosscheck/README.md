# Physlib cross-check of ClayLiteral's equations (1) and (2)

Does [`bridges/ClayLiteral.lean`](../../bridges/ClayLiteral.lean) say the same thing as an independently written definition of the Navier–Stokes equations? This experiment compares its equations (1) and (2) with Physlib's `ConvectiveNavierStokes` (F. Wiesner, [`NavierStokes.lean`](https://github.com/leanprover-community/physlib/blob/8ddcc004043c5b537e4225fa763121c176b62a4a/Physlib/FluidDynamics/CauchyFlow/NavierStokes.lean) at `8ddcc00`) and proves in Lean that, under the hypotheses below, the two agree on equations (1) and (2).

Physlib's definition was written independently of this study and for a different purpose. Its author has not reviewed this experiment or `ClayLiteral`; this is a comparison with an independently written definition, not an independent review.

| File | Content |
| --- | --- |
| [`PhyslibCrosscheck/ClayLiteralCopy.lean`](PhyslibCrosscheck/ClayLiteralCopy.lean) | Verbatim copy of `R3`, `e`, `div`, `Eq1` and `Eq2` from `bridges/ClayLiteral.lean` |
| [`PhyslibCrosscheck/Crosscheck.lean`](PhyslibCrosscheck/Crosscheck.lean) | The Physlib flow built from Clay's data, the pointwise form of Physlib's predicate, and the theorems |
| [`Axioms.lean`](Axioms.lean) | `#print axioms` for every theorem and lemma |
| [`check_copy.py`](check_copy.py) | Checks that the copied lines are identical to the source file |
| [`receipts/`](receipts/) | Build log and exit code, axioms output, copy check, versions and SHA-256 hashes |

## Why a copy

The main study is pinned to Lean `4.34.0-rc2`; Physlib at `8ddcc00` needs Lean `4.35.0` and its own Mathlib, so it cannot be imported there. This is a separate Lake project that requires Physlib at that commit and gets Mathlib from Physlib's pin. The definitions are copied unchanged: lines 22–23, 25–26, 62–64 and 66–76 of `bridges/ClayLiteral.lean` (SHA-256 `1998dac2…acb2d`, the same hash as the [bridges receipt](../../bridges/README.md#build-receipt-2026-10-21)). `check_copy.py` compares them line by line ([output](receipts/copy-check.txt)).

## What is proved

Clay's data are a viscosity `ν : ℝ`, a force `f`, a velocity `u` and a pressure `p`, as functions of (x, t) on ℝ³ × ℝ. `clayFlow ν f u p` is the Physlib `CauchyFlow 3` with

- density ρ = 1;
- velocity u, read on Physlib's `Time` and `Space 3` through the canonical equivalences `Time.val` and `Space.basis.repr` (`transport`);
- stress equal to Physlib's `newtonianStressTensor` with pressure p, shear viscosity μ = ν and second viscosity λ = 0;
- specific body force f.

Physlib's `ConvectiveNavierStokes` quantifies over every time, including t < 0, while Clay's equations are stated for t ≥ 0. The comparison is therefore made point by point. `ConvectiveNavierStokesAt d flow p μ λ t x` is the conjunction of the three parts of Physlib's definition at one point (t, x), and `convectiveNavierStokes_iff_forall_at` proves that `ConvectiveNavierStokes d flow p μ λ` holds if and only if `ConvectiveNavierStokesAt` holds at every (t, x). That proof only takes the conjuncts apart, so Lean's kernel checks that each conjunct is Physlib's own text at (t, x).

The main theorem, verbatim:

```lean
theorem eq1_and_eq2_iff_convectiveNavierStokesAt
    (hu : ∀ s, ContDiff ℝ 2 (fun y => u y s))
    (hut : ∀ y s, DifferentiableAt ℝ (fun s => u y s) s)
    (hp : ∀ s, Differentiable ℝ (fun y => p y s)) :
    Eq1 ν f u p ∧ Eq2 u ↔
      ∀ t : Time, 0 ≤ t.val → ∀ x : Space 3,
        ConvectiveNavierStokesAt 3 (clayFlow ν f u p) (transport p) (fun _ _ => ν)
          (fun _ _ => 0) t x
```

In words: if u is C² in space and differentiable in time, and p is differentiable in space, then `ClayLiteral`'s equations (1) and (2) hold on ℝ³ × [0, ∞) if and only if Physlib's convective Navier–Stokes equations hold at every point with t ≥ 0, for ρ = 1, μ = ν, λ = 0 and body force f. It holds for every real ν.

A corollary uses Physlib's predicate itself, with no pointwise form:

```lean
theorem eq1_and_eq2_of_convectiveNavierStokes
    (hu : ∀ s, ContDiff ℝ 2 (fun y => u y s))
    (hut : ∀ y s, DifferentiableAt ℝ (fun s => u y s) s)
    (hp : ∀ s, Differentiable ℝ (fun y => p y s))
    (h : ConvectiveNavierStokes 3 (clayFlow ν f u p) (transport p) (fun _ _ => ν)
      (fun _ _ => 0)) :
    Eq1 ν f u p ∧ Eq2 u
```

The converse of the corollary is not claimed, because Physlib's predicate also constrains t < 0, where Clay says nothing.

### How the pieces match

- Continuity: with ρ = 1, Physlib's `∂ₜ ρ + div (ρ u) = 0` is div u = 0, which is `Eq2`. Physlib asserts it only where ρ and ρu are differentiable; under `hu` both are, so the guard is always met.
- Time derivative: `Eq1` uses the one-sided derivative on [0, ∞); Physlib uses the two-sided derivative. They are equal at every t ≥ 0, including t = 0, because `hut` makes u differentiable in time on all of ℝ.
- Stress: the divergence of −pI + ν(∇u + ∇uᵀ) is −∇p + νΔu + ν∇(div u). The last term needs the symmetry of second derivatives (from C², via Mathlib's `ContDiffAt.isSymmSndFDerivAt`) and vanishes because div u = 0 at that time for every x. The λ term is zero because λ = 0.
- Derivatives along Physlib's basis vectors of `Space 3` equal Clay's derivatives along e_j (`deriv_transport`).

## Hypotheses and reading choices

| Choice | Made here | Note |
| --- | --- | --- |
| Smoothness of u | `hu`: y ↦ u(y, t) is C² for every t ∈ ℝ; `hut`: t ↦ u(x, t) is differentiable at every t ∈ ℝ | Assumed, not derived from Clay's condition (6) |
| Smoothness of p | `hp`: y ↦ p(y, t) is differentiable for every t ∈ ℝ | Assumed, not derived from (6) |
| Force f | No hypothesis | f enters both sides pointwise |
| Density | ρ = 1 | Clay's equations have no density; ρ = 1 is the usual reading |
| Shear viscosity | μ = ν, constant | |
| Second viscosity | λ = 0 | Only λ = 0 is proved; with div u = 0 the λ term would also vanish for other constant λ, but that is not checked here |
| Stress | Set to Physlib's `newtonianStressTensor` | So Physlib's `IsNewtonian` holds by construction; the content is in the momentum equation |
| Form of the equations | Physlib's convective form | Physlib's own theorem `navier_stokes_iff_convective_navier_stokes` relates it to the conservative `NavierStokes`; that link is not used here |
| Coordinates | `Space.basis.repr : Space 3 ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)` and `Time.val` | The canonical identifications in Physlib |

## What this does not cover

- Clay's conditions (3)–(11), the erratum, and alternatives (C) and (D). Physlib has no initial data, decay, finite energy or periodicity, so it cannot speak to them.
- Whether the smoothness hypotheses follow from Clay's condition (6) under either reading in `ClayLiteral` (`SmoothUpToBoundary`, `SmoothOneSided`). Under the restriction reading, u agrees on t ≥ 0 with a C^∞ function on ℝ³ × ℝ, and the theorem would be applied to that extension; that step is not formalized here.
- Times t < 0, where Physlib's predicate also applies and Clay's does not.
- Whether either definition matches Clay's PDF. Agreement between two independently written definitions makes a transcription error in equations (1) and (2) less likely, but a mistake shared by both would not be detected. `ClayLiteral`'s fidelity to the PDF is still review point K0 ([`K0_REVIEW.md`](../../bridges/K0_REVIEW.md)).
- The rest of `ClayLiteral` and `Bridges.lean`, which were not compiled in this project.

## Receipt (2026-10-24)

Run on the operator's Mac (arm64, macOS 26.2). Physlib's needed modules were compiled locally; Mathlib's were downloaded with `lake exe cache get`.

| Item | Value |
| --- | --- |
| Lean | `4.35.0`, commit `eb6cafb7290e8bd5f2937522d8d804f58f02bafc` |
| Physlib | `8ddcc004043c5b537e4225fa763121c176b62a4a` |
| Mathlib (from `lake-manifest.json`) | `56a005855ea17e0b0958f73ec801ae140b0a1679` |
| `bridges/ClayLiteral.lean` SHA-256 | `1998dac2bee2477b8cc1d100f5345574624bf62290d1f85abf27203b9f8acb2d` |
| `PhyslibCrosscheck/ClayLiteralCopy.lean` SHA-256 | `31761ef2e62fe2e3937302ce2319478668ad63aa9daea9b63f81d042c4a97c72` |
| `PhyslibCrosscheck/Crosscheck.lean` SHA-256 | `9de4db5a9092047657b11ccf95c3e6c15b5b1060a72127bd1c53355651cbec4a` |
| `PhyslibCrosscheck.lean` SHA-256 | `9544231bf69c7ce87d81b4b366c2e69d7b84a8edd3ecc66556c68e6ff380d6e7` |
| `Axioms.lean` SHA-256 | `d22a27436cf5d33fc7cc9c663cc468d9273fe82ba61282837d1e7c174ff4f9f8` |
| Physlib `NavierStokes.lean` SHA-256 | `a2e05f67b26d17e0e5d4d2c48fc208dca61fd5f231a858b1d888522c3190d4b4` |
| `lake build` | exit 0, 129.7 s wall ([log](receipts/build.log)); Physlib dependencies 41.6 s wall ([log](receipts/physlib-deps-build.log)) |
| `#print axioms` | `[propext, Classical.choice, Quot.sound]` for all 13 declarations ([output](receipts/axioms.log)) |
| `sorry` | none |
| Copy check | identical ([output](receipts/copy-check.txt)) |

All hashes and package revisions are in [`receipts/versions.txt`](receipts/versions.txt). To reproduce:

```sh
cd experiments/physlib-crosscheck
lake exe cache get   # clones the packages pinned in lake-manifest.json and downloads Mathlib's build cache
lake build
lake env lean Axioms.lean
python3 check_copy.py
```
