> Traducción al español de [DESIGN.md](DESIGN.md). Si hay alguna diferencia, vale el original.

# Controles con Mathlib: ¿distingue el protocolo «el enunciado cambió» de «el teorema es falso»?

**Registrado antes de correrlo el 2026-10-21, antes de correr cualquier caso.** Los casos, los enunciados en [`lean/QAControls/Challenge/`](lean/QAControls/Challenge/), las pruebas en [`lean/QAControls/Solution/`](lean/QAControls/Solution/) y los resultados esperados en [`expected.json`](expected.json) quedan fijos en el commit que añade este archivo. Los resultados se añaden en commits posteriores y se comparan contra él. **Resultados: [RESULTS.md](RESULTS.md).**

> **Enmienda 1 (2026-10-21, después de una revisión externa y antes de correr cualquier caso).** El registro original es el commit `046a128`. Cambios: (1) *SAME* se renombra como **ACCEPTED_BY_CHECKER**, porque una aceptación de Comparator significa que los enunciados coinciden tal como los compara Comparator, lo que no necesariamente es identidad textual ni es una equivalencia matemática probada por separado; un caso nuevo, `primes/defeq`, prueba exactamente eso. (2) **CHANGED_WEAKER** ahora exige dos pruebas: original ⇒ cambiado, y que el cambiado no implique el original en el esquema evaluado; la sola no implicación también podría significar un enunciado más fuerte o incomparable, lo que da **CHANGED_NOT_EQUIVALENT**. (3) La equivalencia de `dct/reform` debe usar que la hipótesis de dominación hace que la cota sea no negativa en casi todo punto; un control muestra que la condición alternativa aislada no es equivalente a la integrabilidad para una función que toma valores negativos.

## Por qué

Un verificador de enunciados como Comparator responde una sola pregunta: *¿el teorema entregado es exactamente el enunciado del desafío?* Un rechazo no dice que el enunciado cambiado sea falso, y puede rechazar una reformulación que es matemáticamente equivalente. Este experimento usa tres teoremas que Mathlib ya prueba, para que cada resultado se pueda comprobar, y pregunta si el protocolo distingue cuatro situaciones:

- Comparator acepta el enunciado (**ACCEPTED_BY_CHECKER**), que es igualdad tal como la ve el verificador, no la prueba de ninguna otra cosa;
- el enunciado cambió pero es equivalente, probado por separado (**CHANGED_EQUIVALENT**);
- el enunciado cambió a algo más débil, por ejemplo una versión limitada a ejemplos: se prueba original ⇒ cambiado, y se muestra en el esquema que cambiado ⇏ original (**CHANGED_WEAKER**);
- el enunciado cambió y se muestra que no implica el original, sin el recíproco (**CHANGED_NOT_EQUIVALENT**);
- el enunciado cambió a algo falso (**CHANGED_FALSE**).

## Teoremas y casos

| Teorema | Correcto | Reformulación equivalente | Error deliberado |
| --- | --- | --- | --- |
| Infinitud de los primos | `∀ n, ∃ p, n < p ∧ p.Prime` | `n ≤ p` en vez de `n < p`; y `n + 1 ≤ p`, que es `n < p` por definición (`primes/defeq`) | **Limitado a ejemplos:** `∀ n ≤ 100, …` (verdadero, pero más débil). **Cuantificadores invertidos:** `∃ p, ∀ n, n < p ∧ p.Prime` (falso) |
| Cauchy–Schwarz | `abs ⟪x, y⟫ ≤ ‖x‖ ‖y‖` | `⟪x, y⟫² ≤ ‖x‖² ‖y‖²` | `<` en vez de `≤`: falso para dos vectores iguales y distintos de cero |
| Convergencia dominada | Hipótesis de Mathlib | `Integrable bound` escrito como medible con integral de Lebesgue finita de `ofReal bound`; equivalente solo porque la dominación obliga a que `bound ≥ 0` en casi todo punto | **Dominación eliminada:** falso; `f_n = (n+1)` en `(0, 1/(n+1))` y 0 en el resto tiende a 0 puntualmente, pero cada integral vale 1 |

Cada enunciado cambiado reemplaza el desafío; al estilo OpenAI, la prueba nunca se toca. Once corridas de Comparator en total.

## Procedimiento

1. **Comparator** (fijado en `19e111e`, con nanoda y el kernel de Lean, el mismo toolchain y Mathlib que la auditoría principal) revisa cada caso: la prueba correcta contra el desafío posiblemente cambiado.
2. **Segunda vía**, solo para los casos rechazados, en Lean puro, aparte de Comparator:
   - *equivalencia*: probar `changed ↔ original` (para los primos, como un esquema sobre todo predicado `P`, para que no valga solo porque los dos lados son verdaderos);
   - *más débil*: probar original ⇒ cambiado como esquema, **y** exhibir un predicado para el que la forma cambiada vale y la original falla;
   - *refutación*: probar `¬ changed`.
3. **Guarda**: una equivalencia cuenta solo si una revisión sobre las dependencias transitivas de su prueba no encuentra ningún uso del teorema bajo prueba (`Nat.exists_infinite_primes`, los lemas de Cauchy–Schwarz, `tendsto_integral_of_dominated_convergence`). Sin esto, dos enunciados verdaderos cualesquiera serían «equivalentes».
4. **Regla de clasificación**: aceptado → ACCEPTED_BY_CHECKER (una equivalencia puede probarse igual por separado, y se reporta junto a él); rechazado y la equivalencia pasa la guarda → CHANGED_EQUIVALENT; rechazado y la refutación compila → CHANGED_FALSE; rechazado, original ⇒ cambiado compila y la no implicación del esquema compila → CHANGED_WEAKER; rechazado y solo compila la no implicación → CHANGED_NOT_EQUIVALENT; de lo contrario → CHANGED_UNKNOWN.

**Controles:** una prueba de equivalencia para `primes/reform` que haga trampa usando `Nat.exists_infinite_primes` debe ser rechazada por la guarda; y para `g = -1` en ℝ, medible con `∫⁻ ofReal g = 0 < ∞` pero no integrable, una refutación debe compilar, mostrando que la reformulación de DCT necesita la no negatividad que da la dominación.

## Resultados esperados

| Caso | Comparator | Segunda vía | Clase |
| --- | --- | --- | --- |
| primes/orig | accept | — | ACCEPTED_BY_CHECKER |
| primes/defeq | reject si Comparator compara las expresiones de forma estructural; la aceptación se reporta como un hallazgo | equivalencia | CHANGED_EQUIVALENT, o ACCEPTED_BY_CHECKER |
| primes/reform | reject | equivalencia | CHANGED_EQUIVALENT |
| primes/bounded | reject | original ⇒ cambiado, y la no implicación del esquema | CHANGED_WEAKER |
| primes/swap | reject | refutación | CHANGED_FALSE |
| cs/orig | accept | — | ACCEPTED_BY_CHECKER |
| cs/reform | reject | equivalencia | CHANGED_EQUIVALENT |
| cs/strict | reject | refutación | CHANGED_FALSE |
| dct/orig | accept | — | ACCEPTED_BY_CHECKER |
| dct/reform | reject | equivalencia | CHANGED_EQUIVALENT |
| dct/nodom | reject | refutación | CHANGED_FALSE |

Si Comparator acepta una reformulación, eso en sí mismo es un hallazgo (compararía los enunciados más allá de la sintaxis) y se reporta como tal, sin ocultarlo.

## Límites, declarados de antemano

- El autor diseñó cada caso, y las pruebas de la segunda vía se escriben después de este registro, por el mismo autor y el mismo asistente, así que un caso podría fallar por un error en una prueba de la segunda vía y no en el protocolo; esos fallos se reportan, no se reintentan en silencio.
- **Todavía faltan casos reservados (held-out) de otra persona.** Casos preparados por alguien que no haya visto el evaluador lo probarían sin ajustarse a las decisiones del autor. La plantilla está en [`HOLDOUT.md`](HOLDOUT.md); todavía no se ha recibido ninguno.
- Once casos sobre tres teoremas no dan una tasa de detección.
