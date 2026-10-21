# Review sheet for `ClayLiteral.lean` (row K0)

K1 proves that OpenAI's theorems imply Clay's (C) and (D) **as written in [`ClayLiteral.lean`](ClayLiteral.lean)**. That conclusion is only as good as the rendering, so this sheet lists every place where a reviewer should compare the Lean text with Fefferman's Clay PDF (SHA-256 `c1b5f27b…a06d0c`). It is meant for someone other than the author and the assistant. Write the answer, your name and the date in the last column, or send them and they will be recorded here.

| # | Clay text | `ClayLiteral` | What to check | Answer |
| --- | --- | --- | --- | --- |
| 1 | p, u ∈ C^∞(ℝ³ × [0, ∞)), (6) and (11); f smooth on ℝ³ × [0, ∞) | `SmoothUpToBoundary` (restriction of a C^∞ function on ℝ³ × ℝ) and `SmoothOneSided` (derivatives of every order continuous up to t = 0, `ContDiffOn` within the closed half-space) | **Smoothness at t = 0.** Is Clay's meaning one of these two? K1 is proved under both (`k1_C`, `k1_D`, `k1_C_oneSided`, `k1_D_oneSided`), so the result does not depend on which one. **But both are definitions:** `SmoothOneSided` is Mathlib's `ContDiffOn` within the closed half-space, and its name proves nothing. Check that `ContDiffOn` there (derivatives within the set, continuous on it) is the smoothness Clay means, and whether there is a third reading, for example C^∞ only for t > 0 with continuity at t = 0. | |
| 2 | (1) holds "for x ∈ ℝⁿ, t ≥ 0" | `Eq1` requires (1) for every t ≥ 0, with the time derivative one-sided at t = 0 (`derivWithin … (Set.Ici 0)`) | Is requiring (1) at t = 0 with a right derivative what Clay means? For t > 0 the one-sided derivative equals the ordinary one | |
| 3 | ∂uᵢ/∂t, ∂_t^m | `dt` iterates `derivWithin` on `[0, ∞)` | As 2, for higher time derivatives in (5) and (9) | |
| 4 | ∂_x^α, multi-index α | `dx`, `dxt`: a list of directions, applied after the time derivatives | For smooth functions the order of partials does not matter; check the list encoding covers every α | |
| 5 | Σⱼ uⱼ ∂uᵢ/∂xⱼ, Δ = Σ ∂²/∂xₖ², ∂p/∂xᵢ | Written in coordinates in `Eq1` | Coefficients and signs: ν multiplies only Δu; the pressure enters with a minus sign | |
| 6 | div u = Σ ∂uᵢ/∂xᵢ | `div` | Same | |
| 7 | (4): abs(∂^α u°(x)) ≤ C_{αK} (1 + abs(x))^-K "for any α and K" | `Cond4`, with K real and C depending on α and K | K real is a stronger requirement on data than K integer, so the data side is not weakened by this choice | |
| 8 | (5): abs(∂_x^α ∂_t^m f) ≤ C_{αmK} (1 + abs(x) + t)^-K on ℝ³ × [0, ∞) | `Cond5` | As 7 | |
| 9 | (7): ∫ abs(u(x, t))² dx < C for all t ≥ 0 | `Cond7`, a Lebesgue integral of a nonnegative function, one C for all t | Is "< C" one uniform constant? | |
| 10 | (8): u°(x + eⱼ) = u°(x), f(x + eⱼ, t) = f(x, t) | `Cond8`, for t ≥ 0 | Periodicity in each unit direction | |
| 11 | (9): abs(∂_x^α ∂_t^m f) ≤ C (1 + abs(t))^-K | `Cond9` | As 8 | |
| 12 | (10): u(x, t) = u(x + eⱼ, t) | `Cond10` | Same | |
| 13 | Erratum: "p(x + eⱼ, t) = p(x, t) should be made explicit in Eqn (8)" | `Erratum`, used as a solution condition in `AltD_withErratum`; `AltD_withoutErratum` drops it | **Affects (D) only; (C) does not use it.** K1 proves the version with the erratum on solutions | |
| 14 | (C) and (D): "there exist … for which there exist no solutions (p, u)" | `AltC`, `AltD_*` | Logical form and the list of conditions on each side | |

`Bridges.zero_solution_C` and `zero_solution_D` check that the solution conditions can be met (the zero solution, for zero data), so "no solution exists" is not vacuous.

**Reviews received:** none yet.
