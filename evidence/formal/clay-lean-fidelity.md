# Documentary Clay–Lean correspondence: Navier–Stokes

**Status:** documentary comparison of statement clauses only. This is not a proof that the Lean statements are equivalent to the Clay formulation, is not a specialist mathematical opinion, and has not received independent expert review. Read the cited statements; similar names alone do not establish correspondence.

| Clay text (official PDF, pages 1–2 and 6) | Visible Lean declaration or clause in the pinned OpenAI snapshot | Scope note |
| --- | --- | --- |
| (1) Navier–Stokes equation | `NavierStokesExistenceAndSmoothness.navier_stokes` | Similar purpose and form; operator and convention details still need comparison. |
| (2) Incompressibility | `div_free` | Definition and coordinate conventions still need comparison. |
| (3) Initial data | `initial_condition` | The name alone does not establish equality of admissible data classes. |
| (4) Decay of initial velocity | `InitialVelocityConditionDecay.decay` | Compare the exact quantifier and decay form. |
| (5) Decay of force | `ForceConditionDecay.decay` | Compare the full conditions. |
| (6), (11) Smoothness of velocity and pressure | `velocity_smooth`, `pressure_smooth` | Spatial and temporal regularity and the domain require comparison. |
| (7) Energy | `MemLp` and `globally_bounded_energy` | Norm, exponent, measure, and quantifiers require verification. |
| (8) Periodicity of initial data and force | `IsOnePeriodic u₀`, `IsOnePeriodic f` | Check period convention and domain. |
| (9) Temporal decay of periodic force | `ForceConditionPeriodic.decay` | The concrete zero-force instance satisfies this condition. |
| (10) Periodicity of velocity | `isOnePeriodic_velocity` | Check period, domain, and representation. |
| Page 6 erratum to (8): pressure periodicity | `isOnePeriodic_pressure` | Editorial correction associated with (8), not a separately numbered (10) condition. |
| (C), (D) Breakdown with positive viscosity | `ν > 0`, `n = 3`, existence of `u₀, f`, and nonexistence of `v, p` in the breakdown theorem | Compare all hypotheses, conclusion, and logical structure. Euler is separate and is not part of this Clay A–D comparison. |

## Pinned sources

- [Clay Mathematics Institute, official Navier–Stokes description (PDF)](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf), pages 1–2 and 6. SHA-256: `c1b5f27b1a64705cfaf1afceea513db5deedca8a18ca56ab32e7f86445a06d0c`.
- [Google DeepMind FormalConjectures, pinned Navier–Stokes source](https://github.com/google-deepmind/formal-conjectures/blob/8bf45ed70d48b2b2a501de9c00b26bfa38c573ee/FormalConjectures/Millenium/NavierStokes.lean), commit `8bf45ed70d48b2b2a501de9c00b26bfa38c573ee`.
- OpenAI's formal source repository, commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`. The formal proofs belong to their original authors; this QA package does not claim authorship of those proofs.

## Open bridges to equivalence

An equivalence argument would still need to justify at least: (a) multi-index derivatives versus norms of Fréchet derivatives; (b) the real exponent `K` and its decay convention against the formal definitions; (c) regularity at `t = 0` and the use of `derivWithin`; (d) integrability and measure formulations, including avoidance of vacuous integrals; and (e) equivalence of coordinates and operators. A transfer of nonexistence also needs both directions: admissible formal data must imply admissible Clay data, and every Clay solution must induce a solution in the formalization.

A clause-by-clause [risk review](clay-lean-risk.md) now locates each of these bridges and flags the one interpretive point, periodic pressure in (D).

The nonzero periodic positive control is a concrete torus instance and reports standard axioms. It does not establish these bridges, cover every Clay hypothesis, or prove the global conclusion.
