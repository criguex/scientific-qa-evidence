# Review sheet for `ClayLiteral.lean` (row K0)

K1 proves that OpenAI's theorems imply Clay's (C) and (D) **as written in [`ClayLiteral.lean`](ClayLiteral.lean)**. That conclusion is only as good as the rendering, so this sheet lists every place where a reviewer should compare the Lean text with Fefferman's Clay PDF (SHA-256 `c1b5f27b…a06d0c`). It is meant for someone other than the author and the assistant.

**These are points to compare, not 14 defects.** Our own inspection found no concrete error in any of them. The sheet exists so that the reasoning can be checked by someone else instead of resting on our opinion, or on the standing of whoever signs a review. Points 1–9 and 14 bear on (C), the alternative OpenAI's (C) proof answers; points 10–13 bear on (D) only. Page and equation numbers refer to the PDF with the hash above ([download](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)); line numbers refer to `ClayLiteral.lean` as of SHA-256 `1998dac2…`.

**How to answer.** A bare "looks fine" cannot be checked. For each point you review, please give:

- **Verdict:** agree, object, or unsure.
- **Citation:** the PDF page and equation, and the Lean line, you rely on.
- **Argument:** why the Lean text does or does not say what Clay's text says.
- **Resolution,** if you object: the Lean change you propose, or the reading you think Clay intends.

Partial reviews are welcome; point 1 and point 14 matter most for (C). Send the answers, with your name and the date, as an issue on this repository or by e-mail, and they will be recorded below as received, without editing what you wrote.

| # | For | Where: Clay PDF · `ClayLiteral.lean` | Clay text | `ClayLiteral` | What to check | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | C, D | p. 1 (6); p. 2 (11) and the statements of (C), (D) · [L52–62](ClayLiteral.lean#L52-L62), [L92–100](ClayLiteral.lean#L92-L100) | p, u ∈ C^∞(ℝ³ × [0, ∞)), (6) and (11); f smooth on ℝ³ × [0, ∞) | `SmoothUpToBoundary` (restriction of a C^∞ function on ℝ³ × ℝ) and `SmoothOneSided` (derivatives of every order continuous up to t = 0, `ContDiffOn` within the closed half-space) | **Smoothness at t = 0.** Is Clay's meaning one of these two? K1 is proved under both (`k1_C`, `k1_D`, `k1_C_oneSided`, `k1_D_oneSided`), so the result does not depend on which one. **But both are definitions:** `SmoothOneSided` is Mathlib's `ContDiffOn` within the closed half-space, and its name proves nothing. Check that `ContDiffOn` there (derivatives within the set, continuous on it) is the smoothness Clay means, and whether there is a third reading, for example C^∞ only for t > 0 with continuity at t = 0. | |
| 2 | C, D | p. 1 (1) · [L68–75](ClayLiteral.lean#L68-L75) | (1) holds "for x ∈ ℝⁿ, t ≥ 0" | `Eq1` requires (1) for every t ≥ 0, with the time derivative one-sided at t = 0 (`derivWithin … (Set.Ici 0)`) | Is requiring (1) at t = 0 with a right derivative what Clay means? For t > 0 the one-sided derivative equals the ordinary one | |
| 3 | C, D | p. 1 (5); p. 2 (9) · [L39–44](ClayLiteral.lean#L39-L44) | ∂uᵢ/∂t, ∂_t^m | `dt` iterates `derivWithin` on `[0, ∞)` | As 2, for higher time derivatives in (5) and (9) | |
| 4 | C, D | p. 1 (4), (5); p. 2 (9) · [L34–38](ClayLiteral.lean#L34-L38), [L45–51](ClayLiteral.lean#L45-L51) | ∂_x^α, multi-index α | `dx`, `dxt`: a list of directions, applied after the time derivatives | For smooth functions the order of partials does not matter; check the list encoding covers every α | |
| 5 | C, D | p. 1 (1) and the definition of Δ below (3) · [L68–75](ClayLiteral.lean#L68-L75) | Σⱼ uⱼ ∂uᵢ/∂xⱼ, Δ = Σ ∂²/∂xₖ², ∂p/∂xᵢ | Written in coordinates in `Eq1` | Coefficients and signs: ν multiplies only Δu; the pressure enters with a minus sign | |
| 6 | C, D | p. 1 (2), (3) · [L63–67](ClayLiteral.lean#L63-L67), [L76](ClayLiteral.lean#L76), [L79](ClayLiteral.lean#L79) | div u = Σ ∂uᵢ/∂xᵢ | `div` | Same | |
| 7 | C | p. 1 (4) · [L83–86](ClayLiteral.lean#L83-L86) | (4): abs(∂^α u°(x)) ≤ C_{αK} (1 + abs(x))^-K "for any α and K" | `Cond4`, with K real and C depending on α and K | K real is a stronger requirement on data than K integer, so the data side is not weakened by this choice | |
| 8 | C | p. 1 (5) · [L87–91](ClayLiteral.lean#L87-L91) | (5): abs(∂_x^α ∂_t^m f) ≤ C_{αmK} (1 + abs(x) + t)^-K on ℝ³ × [0, ∞) | `Cond5` | As 7 | |
| 9 | C | p. 1 (7) · [L101–104](ClayLiteral.lean#L101-L104) | (7): ∫ abs(u(x, t))² dx < C for all t ≥ 0 | `Cond7`, a Lebesgue integral of a nonnegative function, one C for all t | Is "< C" one uniform constant? | |
| 10 | D | p. 1 (8), continued on p. 2 · [L105–108](ClayLiteral.lean#L105-L108) | (8): u°(x + eⱼ) = u°(x), f(x + eⱼ, t) = f(x, t) | `Cond8`, for t ≥ 0 | Periodicity in each unit direction | |
| 11 | D | p. 2 (9) · [L109–113](ClayLiteral.lean#L109-L113) | (9): abs(∂_x^α ∂_t^m f) ≤ C (1 + abs(t))^-K | `Cond9` | As 8 | |
| 12 | D | p. 2 (10) · [L114](ClayLiteral.lean#L114) | (10): u(x, t) = u(x + eⱼ, t) | `Cond10` | Same | |
| 13 | D | p. 6, Errata · [L118](ClayLiteral.lean#L118), [L130–143](ClayLiteral.lean#L130-L143) | Erratum: "p(x + eⱼ, t) = p(x, t) should be made explicit in Eqn (8)" | `Erratum`, used as a solution condition in `AltD_withErratum`; `AltD_withoutErratum` drops it | **Affects (D) only; (C) does not use it.** K1 proves the version with the erratum on solutions | |
| 14 | C, D | p. 2, statements (C) and (D) · [L123–157](ClayLiteral.lean#L123-L157) | (C) and (D): "there exist … for which there exist no solutions (p, u)" | `AltC`, `AltD_*` | Logical form and the list of conditions on each side | |

`Bridges.zero_solution_C` and `zero_solution_D` check that the solution conditions can be met (the zero solution, for zero data), so "no solution exists" is not vacuous.

**Reviews received:** none yet.
