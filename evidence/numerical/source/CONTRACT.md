# Frozen contract — multidomain synthetic campaign

Version 1.1 (CSV export correction; criteria and models unchanged). Scope: sensitivity of a synthetic suite of nine simple models to two known mutations per model. Some configurations are dimensionless rescalings, not three independent mathematical regimes. There are no empirical data: this suite does not validate an apparatus, patient, person, experiment, industrial system, or scientific result from the project.

## Design

Each model has three nondegenerate configurations. For each configuration, evaluate the baseline and two mutants: 9 × 3 × 3 = 81 variant evaluations. Add three RC calibrations with a relative time-constant perturbation of `5e-8`; the design therefore expects 84 variant evaluations in one process, not 84 separate processes. The five ODE models use 64, 128, and 256 steps. Snell, thin-lens, acoustic-interface, and Fechner evaluations do not have an applicable step refinement; run each once per variant and report `resolution: N/A`, rather than fabricating three copies. Report actual execution counts; do not presume 84.

The SUT models are implemented in `sut.py`; independent oracles are in `oracles.py`. The SUT and oracle do not share an RHS, solver, or solution function. RC, cooling, second-order consumption, Beer–Lambert attenuation, and logistic response use scalar RK4 and are compared at four common observation fractions: 1/4, 1/2, 3/4, and 1 of the interval. Snell uses `asin` against bisection; the thin lens uses the lens equation against two-ray tracing; the acoustic interface uses closed-form coefficients against a 2×2 linear system; Fechner compares `k ln(I/I₀)` with numerical trapezoidal integration of `k/I`. These four algebraic/integral cases are one evaluation per variant, not a false refinement sequence.

## Tolerance and classification

The fine tolerance is `1e-6` in absolute error normalized by the declared physical scale for each output. Exact inputs, units, scales, and horizons are recorded in each case JSON. ODE models use the 256-step error; algebraic models use their single evaluation. Do not infer a convergence order when rounding dominates.

- A baseline passes only if its output is finite, satisfies the model invariants, and its normalized error at the last applicable resolution is at most `1e-6`.
- An invalid baseline blocks classification of its mutants; it cannot produce `KILLED`.
- A mutant is `KILLED` only when its corresponding baseline passes and, at the last applicable resolution, the mutant is non-finite, violates an invariant, or exceeds tolerance.
- Otherwise report `SURVIVED`, `BASELINE_INVALID`, `BLOCKED_BASELINE`, or `INCONCLUSIVE` as appropriate; never force a mutant to die.
- NaN and infinity are never `PASS`. A tiny mutation may survive; that is a valid calibration result, not a false negative to be reclassified.

The checked invariants are: RC remains within the source/initial interval and charging is monotone; cooling remains bounded by ambient/initial temperature and is monotone; concentration is positive and non-increasing; intensity is nonnegative and non-increasing; refraction angle stays in the valid half-plane and satisfies Snell's law within the comparison; thin-lens transverse image height is negative for an inverted image and agrees with the ray oracle; acoustic energy balance is `R² + (Z₁/Z₂)T² = 1`; the illustrative Fechner response is non-decreasing with intensity; and the synthetic logistic response stays between zero and its probability capacity `K=1` and is non-decreasing for normalized stimulus. ODE invariants are checked at the fine point; algebraic invariants at the single evaluation. Known mutations are also compared with the oracle: energy conservation alone is insufficient if a boundary condition is violated. A non-finite oracle result or incompatible vector length is `INCONCLUSIVE`, never `KILLED`.

## Determinism and evidence

There is no randomness (seed: not applicable). Only the Python standard library is used. Supply a new output directory; if it already exists, abort without writing. The runner saves all observation/resolution CSV rows, one JSON per variant, status summaries, evaluation times and return codes, and SHA-256 hashes of sources, contract, and artifacts. `point_normalized_error` is the row's `|value − oracle| / scale`; `max_normalized_error` is the maximum for the variant/resolution, repeated by row to support filtering. Non-finite values are exported as empty cells, not numeric values. For acoustics, each of four observation positions repeats the same static reflected/transmitted pressure pair; all eight components are labeled and are not four independent experiments. Times and return codes do not alone imply `PASS`. Do not store hostnames, IP addresses, user identities, or private output paths in a publishable package.

## Configuration data

Exact parameters and units are declared in `suite.py` and repeated in each execution JSON. Ranges avoid zero denominators, discontinuities, and regime changes (for example, total internal reflection); they are not calibrated against an external implementation. Models are synthetic and illustrative. Fechner is not a universal law of perception, and the logistic response is only a synthetic normalized-stimulus response/probability with capacity `K=1` and `p₀∈(0,1)`, not population growth or a predictor of human perception.
