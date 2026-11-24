> Traducción al español de [K0_REVIEW.md](K0_REVIEW.md). Si hay alguna diferencia, vale el original.

# Hoja de revisión para `ClayLiteral.lean` (fila K0)

K1 demuestra que los teoremas de OpenAI implican (C) y (D) de Clay **tal como están escritas en [`ClayLiteral.lean`](ClayLiteral.lean)**. Esa conclusión vale solo lo que valga la transcripción, así que esta hoja enumera cada punto en que un revisor debería comparar el texto en Lean con el PDF de Clay de Fefferman (SHA-256 `c1b5f27b…a06d0c`). Está pensada para alguien distinto del autor y del asistente.

**Estos son puntos para comparar, no 14 defectos.** Nuestra propia inspección no encontró ningún error concreto en ninguno de ellos. La hoja existe para que el razonamiento lo pueda comprobar otra persona, en vez de apoyarse en nuestra opinión o en el prestigio de quien firme una revisión. Los puntos 1–9 y 14 inciden en (C), la alternativa que responde la prueba de (C) de OpenAI; los puntos 10–13 inciden solo en (D). Los números de página y de ecuación se refieren al PDF con el hash de arriba ([descarga](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)); los números de línea se refieren a `ClayLiteral.lean` en la versión con SHA-256 `1998dac2…`.

**Cómo responder.** Un simple "se ve bien" no se puede verificar. Para cada punto que revises, por favor da:

- **Veredicto:** de acuerdo, objeción o sin certeza.
- **Cita:** la página y la ecuación del PDF, y la línea de Lean, en las que te apoyas.
- **Argumento:** por qué el texto en Lean dice o no dice lo que dice el texto de Clay.
- **Resolución,** si tienes una objeción: el cambio en Lean que propones, o la lectura que crees que Clay quiere decir.

Las revisiones parciales son bienvenidas; el punto 1 y el punto 14 son los que más importan para (C). Envía las respuestas, con tu nombre y la fecha, como un issue en este repositorio o por correo, y quedarán registradas abajo tal como se reciban, sin editar lo que escribiste.

| # | Para | Dónde: PDF de Clay · `ClayLiteral.lean` | Texto de Clay | `ClayLiteral` | Qué revisar | Respuesta |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | C, D | p. 1 (6); p. 2 (11) y los enunciados de (C), (D) · [L52–62](ClayLiteral.lean#L52-L62), [L92–100](ClayLiteral.lean#L92-L100) | p, u ∈ C^∞(ℝ³ × [0, ∞)), (6) y (11); f suave en ℝ³ × [0, ∞) | `SmoothUpToBoundary` (restricción de una función C^∞ en ℝ³ × ℝ) y `SmoothOneSided` (derivadas de todo orden continuas hasta t = 0, `ContDiffOn` dentro del semiespacio cerrado) | **Suavidad en t = 0.** ¿El significado de Clay es alguno de estos dos? K1 está demostrado bajo ambos (`k1_C`, `k1_D`, `k1_C_oneSided`, `k1_D_oneSided`), así que el resultado no depende de cuál sea. **Pero ambas son definiciones:** `SmoothOneSided` es el `ContDiffOn` de Mathlib dentro del semiespacio cerrado, y su nombre no demuestra nada. Verifica que ese `ContDiffOn` (derivadas dentro del conjunto, continuas en él) es la suavidad que Clay quiere decir, y si hay una tercera lectura, por ejemplo C^∞ solo para t > 0 con continuidad en t = 0. | |
| 2 | C, D | p. 1 (1) · [L68–75](ClayLiteral.lean#L68-L75) | (1) vale "para x ∈ ℝⁿ, t ≥ 0" | `Eq1` exige (1) para todo t ≥ 0, con la derivada temporal unilateral en t = 0 (`derivWithin … (Set.Ici 0)`) | ¿Es exigir (1) en t = 0 con derivada por la derecha lo que Clay quiere decir? Para t > 0 la derivada unilateral coincide con la ordinaria | |
| 3 | C, D | p. 1 (5); p. 2 (9) · [L39–44](ClayLiteral.lean#L39-L44) | ∂uᵢ/∂t, ∂_t^m | `dt` itera `derivWithin` en `[0, ∞)` | Como en 2, para derivadas temporales de orden superior en (5) y (9) | |
| 4 | C, D | p. 1 (4), (5); p. 2 (9) · [L34–38](ClayLiteral.lean#L34-L38), [L45–51](ClayLiteral.lean#L45-L51) | ∂_x^α, multiíndice α | `dx`, `dxt`: una lista de direcciones, aplicada después de las derivadas temporales | Para funciones suaves el orden de las parciales no importa; verifica que la codificación como lista cubra todo α | |
| 5 | C, D | p. 1 (1) y la definición de Δ debajo de (3) · [L68–75](ClayLiteral.lean#L68-L75) | Σⱼ uⱼ ∂uᵢ/∂xⱼ, Δ = Σ ∂²/∂xₖ², ∂p/∂xᵢ | Escrito en coordenadas en `Eq1` | Coeficientes y signos: ν multiplica solo a Δu; la presión entra con signo menos | |
| 6 | C, D | p. 1 (2), (3) · [L63–67](ClayLiteral.lean#L63-L67), [L76](ClayLiteral.lean#L76), [L79](ClayLiteral.lean#L79) | div u = Σ ∂uᵢ/∂xᵢ | `div` | Lo mismo | |
| 7 | C | p. 1 (4) · [L83–86](ClayLiteral.lean#L83-L86) | (4): abs(∂^α u°(x)) ≤ C_{αK} (1 + abs(x))^-K "para cualquier α y K" | `Cond4`, con K real y C dependiendo de α y K | K real es una exigencia más fuerte sobre los datos que K entero, así que el lado de los datos no se debilita con esta elección | |
| 8 | C | p. 1 (5) · [L87–91](ClayLiteral.lean#L87-L91) | (5): abs(∂_x^α ∂_t^m f) ≤ C_{αmK} (1 + abs(x) + t)^-K en ℝ³ × [0, ∞) | `Cond5` | Como en 7 | |
| 9 | C | p. 1 (7) · [L101–104](ClayLiteral.lean#L101-L104) | (7): ∫ abs(u(x, t))² dx < C para todo t ≥ 0 | `Cond7`, una integral de Lebesgue de una función no negativa, un solo C para todo t | ¿Es "< C" una sola constante uniforme? | |
| 10 | D | p. 1 (8), continúa en p. 2 · [L105–108](ClayLiteral.lean#L105-L108) | (8): u°(x + eⱼ) = u°(x), f(x + eⱼ, t) = f(x, t) | `Cond8`, para t ≥ 0 | Periodicidad en cada dirección unitaria | |
| 11 | D | p. 2 (9) · [L109–113](ClayLiteral.lean#L109-L113) | (9): abs(∂_x^α ∂_t^m f) ≤ C (1 + abs(t))^-K | `Cond9` | Como en 8 | |
| 12 | D | p. 2 (10) · [L114](ClayLiteral.lean#L114) | (10): u(x, t) = u(x + eⱼ, t) | `Cond10` | Lo mismo | |
| 13 | D | p. 6, fe de erratas · [L118](ClayLiteral.lean#L118), [L130–143](ClayLiteral.lean#L130-L143) | Fe de erratas: "p(x + eⱼ, t) = p(x, t) should be made explicit in Eqn (8)" | `Erratum`, usado como condición de solución en `AltD_withErratum`; `AltD_withoutErratum` la omite | **Afecta solo a (D); (C) no la usa.** K1 demuestra la versión con la fe de erratas sobre las soluciones | |
| 14 | C, D | p. 2, enunciados (C) y (D) · [L123–157](ClayLiteral.lean#L123-L157) | (C) y (D): "there exist … for which there exist no solutions (p, u)" | `AltC`, `AltD_*` | Forma lógica y la lista de condiciones en cada lado | |

`Bridges.zero_solution_C` y `zero_solution_D` comprueban que las condiciones de solución se pueden cumplir (la solución cero, para datos cero), así que "no existe solución" no es vacío.

**Revisiones recibidas:** ninguna todavía.
