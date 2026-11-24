> Traducción al español de [clay-lean-bridges.md](clay-lean-bridges.md). Si hay alguna diferencia, vale el original.

# Clay ↔ Lean: afirmación → definición o lema → prueba → revisión → pendiente

Esta tabla convierte la [revisión de riesgo](clay-lean-risk.md) en un plan de trabajo para la verificación semántica y matemática independiente. Cada fila es una afirmación necesaria para concluir que las (C) y (D) formales demostradas por OpenAI implican las (C) y (D) de Clay. Registra qué establecería la afirmación, si eso existe, quién la ha revisado, y qué falta. No es un conteo de pruebas que pasan.

**Estado al 2026-10-21: K1 está demostrado en Lean sin hipótesis: para todo ν > 0, los teoremas ya demostrados por OpenAI implican la (C) de Clay y la (D) de Clay, tal como están escritas en `ClayLiteral`, con la fe de erratas leída como una condición sobre las soluciones. De las 18 filas, 16 están formalmente demostradas (D1–D4 para el testigo concreto de OpenAI, D5 y D7 para cualquier fuerza con una extensión globalmente suave), K0 está escrita y se verificó que no es vacía, y S7 es interpretativa. Todo usa solo los axiomas `propext`, `Classical.choice` y `Quot.sound`. K1 también vale bajo la segunda lectura de la suavidad en t = 0 (derivadas continuas hasta t = 0), así que esa elección no decide el resultado. (C) no usa la fe de erratas; S7 afecta solo a (D). La propia ClayLiteral no ha sido revisada contra el PDF por nadie independiente ([hoja de revisión](../../bridges/K0_REVIEW.md)), y ninguna fila ha sido revisada por un matemático.** Archivos en Lean y recibo de compilación: [`bridges/`](../../bridges/README.md). La columna "Prueba" dice qué tan lejos ha llegado cada afirmación: *lectura* significa un argumento escrito solo en este repositorio.

## Cómo se combinan las afirmaciones

(C) y (D) tienen la forma "existen datos para los cuales no existe solución". El teorema formal implica el de Clay si valen dos familias de lemas en una sola dirección:

- **Lado de los datos (filas D):** todo dato que acepta el enunciado formal es un dato que acepta Clay.
- **Lado de la solución (filas S):** toda solución en el sentido de Clay es una solución en el sentido formal.

Luego, tomando los mismos datos: si existiera una solución de Clay, sería una solución formal, lo que contradice el teorema formal. Esa composición es la fila **K1**. Por cada fila solo hace falta una dirección, que en varias filas es la fácil.

Para enunciar cualquiera de estas como lemas en Lean, primero hay que escribir el texto de Clay en Lean de forma literal: coordenadas, derivadas parciales `∂^α` como `iteratedFDeriv` aplicada a vectores base, derivadas temporales unilaterales en `t = 0`, y la integral de Lebesgue. Esa formalización literal es la fila **K0**, y necesita su propia revisión contra el PDF, porque ella misma es una interpretación.

## Tabla

| ID | Afirmación | Definición o lema | Prueba | Revisión | Pendiente |
| --- | --- | --- | --- | --- | --- |
| K0 | Existe una transcripción literal en Lean de (1)–(11), (C), (D) y la fe de erratas de Clay | [`bridges/ClayLiteral.lean`](../../bridges/ClayLiteral.lean), contra el Mathlib fijado, independiente del estilo de DeepMind. Control de no vacuidad: la solución cero satisface toda condición de solución para datos cero (`Bridges.zero_solution_C`, `_D`) | **escrita; pasa el chequeo de tipos; no vacía** | ninguna | Revisión independiente línea por línea contra el PDF de Clay: [`K0_REVIEW.md`](../../bridges/K0_REVIEW.md), 14 puntos, primero la suavidad en t = 0 |
| K1 | (C) formal ⇒ (C) de Clay, y lo mismo para (D) | `Bridges.k1_C : ∀ ν, 0 < ν → AltC ν`, `Bridges.k1_D : ∀ ν, 0 < ν → AltD_withErratum ν`, a partir de `NavierStokesR3.theorem_1_1` y `PeriodicPaper.periodic_corollary` de OpenAI | **formal, sin hipótesis** (relativo a K0), bajo las dos lecturas de C^∞ en t = 0: también `k1_C_oneSided`, `k1_D_oneSided` | ninguna | Revisión; (D) sin la fe de erratas no está cubierta (S7); (C) no depende de S7 |
| P1 | Para todo ν > 0 y n = 3, como exige Clay | `Bridges.p1`; K1 está enunciado para todo ν > 0 | **formal** | ninguna | Revisión |
| D1 | El u₀ de OpenAI es suave en el sentido de Clay | u₀ = 0: `Bridges.d1_zero` | **formal para el testigo** | ninguna | Revisión |
| D2 | El u₀ de OpenAI cumple `div u° = 0` | u₀ = 0: `Bridges.d2_zero` | **formal para el testigo** | ninguna | Revisión |
| D3 | El u₀ de OpenAI satisface la (4) de Clay | Toda derivada de 0 es 0: `Bridges.dx_zero`, `Bridges.d3_zero` | **formal para el testigo** | ninguna | Revisión |
| D4 | La fuerza de OpenAI es C^∞ en ℝ³ × [0, ∞) en el sentido de Clay | Bajo la lectura por restricción esto necesita una extensión suave. La construcción de OpenAI da `ContDiff ℝ ∞` en todo ℝ × ℝ³ (`CandidateProperties.force_smooth`, en las dos construcciones), así que la fuerza es su propia extensión: `Bridges.witness_C`, `Bridges.witness_D` | **formal para el testigo** | ninguna | Una versión general para fuerzas formales arbitrarias necesitaría un teorema de extensión (Whitney o Seeley); K1 no lo necesita |
| D5 | La fuerza de OpenAI satisface la (5) de Clay | La parcial mixta de Clay `∂x^α ∂t^m f` es igual a la derivada iterada aplicada a vectores unitarios (`Bridges.dirDeriv_eq`, `dt_eq`, `dxt_eq`), así que queda acotada por la norma formal (`Bridges.clay_bound`); luego el decaimiento formal da (5): `Bridges.d5` | **formal** para cualquier fuerza con una extensión globalmente suave | ninguna | Revisión |
| D6 | Datos periódicos formales ⇒ (8) de Clay | `Bridges.d6` | **formal** | ninguna | Revisión |
| D7 | La fuerza periódica de OpenAI satisface la (9) de Clay | Como en D5, con `(1 + abs(t))^-K`: `Bridges.d7` | **formal** para cualquier fuerza con una extensión globalmente suave | ninguna | Revisión |
| S1 | Solución de Clay de (1) ⇒ `navier_stokes` formal | Por componentes: derivada temporal, término convectivo (expansión en la base), laplaciano (`laplacian_eq` de OpenAI), gradiente (`inner_gradient_right`): `Bridges.s1` | **formal** | ninguna | Revisión |
| S2 | (2) de Clay ⇒ `div_free` formal | Traza en la base estándar (`divergence_eq` de OpenAI) y coordenadas de la derivada: `Bridges.s2` | **formal** | ninguna | Revisión |
| S3 | (3) de Clay ⇒ `initial_condition` formal | `Bridges.s3` | **formal** | ninguna | Revisión |
| S4 | (6), (11) de Clay ⇒ `velocity_smooth`, `pressure_smooth` formales | `Bridges.s4`, bajo la lectura por restricción de C^∞ en un conjunto cerrado | **formal** bajo la lectura por restricción; la identidad bajo la lectura unilateral | ninguna | Cuál lectura quiere decir Clay ya no decide K1, que está demostrado bajo ambas |
| S5 | (7) de Clay ⇒ `integrable` y `globally_bounded_energy` formales | La continuidad da medibilidad; una integral de Lebesgue finita da `Integrable` y `MemLp 2`; la integral de Bochner es la parte real de la de Lebesgue: `Bridges.s5` | **formal** | ninguna | Revisión |
| S6 | (10) de Clay ⇒ `isOnePeriodic_velocity` formal | `Bridges.s6` | **formal** | ninguna | Revisión |
| S7 | Una solución de Clay de (D) tiene presión periódica | Fe de erratas de Clay: "p(x + eⱼ, t) = p(x, t) should be made explicit in Eqn (8)" | interpretativa; lado formal demostrado (`Bridges.s7_formal_side`), usado por K1 para (D) | ninguna | **Necesita una decisión humana.** Si la fe de erratas es una condición sobre las soluciones, K1 para (D) es el resultado completo. Si no, la (D) formal es más débil: quedan excluidas las presiones no periódicas p = q + c(t)·x. Se envió la pregunta al Clay Mathematics Institute el 2026-10-21. El presidente del CMI respondió el 2026-10-22 solo que (B) y (D) son problemas periódicos (toroidales), sin interpretar la fe de erratas ([registro](clay-correspondence.md)); la lectura sigue abierta. |
| L1 | El enunciado formal y el de Clay tienen la misma forma lógica | Resuelto por K1 | **formal** (vía K1) | ninguna | — |

**Recuento:** 18 filas. Formalmente demostradas: 16 (K1, P1, D1–D7, S1–S6, L1), D1–D4 para el testigo de OpenAI. K0 escrita y verificada como no vacía. S7 interpretativa, lado formal demostrado. Revisadas: 0.

**Lo que K1 no establece.** No muestra que `ClayLiteral` sea una transcripción fiel del PDF de Clay; eso es la revisión de K0. No cubre (D) con la fe de erratas leída solo como una condición sobre los datos. Hereda la confianza en la prueba de OpenAI, que descansa en las comprobaciones del kernel en [cd-validation](cd-validation/README.md), y no dice nada sobre si la prueba en Lean de OpenAI sigue el artículo de OpenAI.

## Plan

1. **Hecho:** K0, todas las filas D y S excepto S7, y K1.
2. **Revisión independiente de K0**, línea por línea contra el PDF, por alguien distinto del autor y del asistente; registrar al revisor, la fecha y la respuesta en la columna Revisión.
3. **S7 y la lectura de C^∞ en un conjunto cerrado:** llevar ambas a un especialista en EDP y al Zulip de Lean; registrar las respuestas.
4. **Revisión matemática** de las filas de los puentes.

Una fila pasa a "formal" solo cuando su prueba en Lean compila y se publica con hashes, y a "revisada" solo cuando una persona identificada, distinta del autor y del asistente, la ha verificado.
