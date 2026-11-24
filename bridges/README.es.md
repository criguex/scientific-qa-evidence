> Traducción al español de [README.md](README.md). Si hay alguna diferencia, vale el original.

# Puentes: el texto de Clay en Lean, y los lemas que lo conectan con el enunciado formal

Trabajo para el plan semántico en [`evidence/formal/clay-lean-bridges.md`](../evidence/formal/clay-lean-bridges.md).

| Archivo | Contenido |
| --- | --- |
| [`ClayLiteral.lean`](ClayLiteral.lean) | Fila K0: las ecuaciones (1)–(11) de Clay, las alternativas (C) y (D) y la fe de erratas, escritas literalmente (coordenadas, derivadas parciales a lo largo de vectores base, derivadas temporales unilaterales, integral de Lebesgue). Solo definiciones, más un teorema de sanidad. **Pendiente de revisión contra el PDF.** |
| [`Bridges.lean`](Bridges.lean) | Lemas entre el enunciado de OpenAI y `ClayLiteral`, y la composición K1. Importa el módulo de soluciones de OpenAI, así que K1 parte de los teoremas ya demostrados por OpenAI. |

## Lecturas elegidas en ClayLiteral (por revisar)

| Lectura | Elección hecha | Cómo la maneja K1 |
| --- | --- | --- |
| C^∞(ℝ³ × [0, ∞)), filas D4 y S4 | Dos transcripciones: restricción de una función C^∞ en ℝ³ × ℝ (`SmoothUpToBoundary`), y derivadas de todo orden continuas hasta t = 0 (`SmoothOneSided`, el `ContDiffOn` de Mathlib) | Demostrado bajo ambas (`k1_*` y `k1_*_oneSided`); si alguna es el significado de Clay es el punto de revisión 1 en [`K0_REVIEW.md`](K0_REVIEW.md) |
| La fe de erratas, fila S7 | (D) enunciada tanto con como sin presión periódica sobre las soluciones | K1 demuestra la versión con la fe de erratas sobre las soluciones; la otra queda abierta |
| Exponente K en (4), (5), (9) | Recorre los reales | Una exigencia más fuerte sobre los datos que K natural, así que el lado de los datos no se debilita |
| Multiíndice α | Una lista de direcciones, así que el orden y la repetición quedan explícitos | Para funciones suaves el orden de las parciales no importa |

## Recibo de compilación (2026-10-21)

Compilado en el equipo Linux de prueba contra la compilación B4 sin caché del `f9e8bc5` de OpenAI, así que con el mismo Lean y Mathlib que el estudio principal.

| Elemento | Valor |
| --- | --- |
| Lean | `4.34.0-rc2`, commit `6a10ac8c22beadecabdbb0919c2b50214762f91d` |
| Mathlib | `85e3a25e006c35636f0e53b0e9296caca2685bc0` (B4, compilado localmente) |
| SHA-256 de `ClayLiteral.lean` | `1998dac2bee2477b8cc1d100f5345574624bf62290d1f85abf27203b9f8acb2d` |
| SHA-256 de `Bridges.lean` | `b22ddc0e09bf21778700b9ac8b5674b683aa365cafc99aac3ac354d3c1c73278` |
| `ClayLiteral.lean` | pasa el chequeo de tipos, exit 0 |
| `Bridges.lean` | pasa el chequeo de tipos, exit 0 |

Se corrió `#print axioms` sobre cada teorema de `Bridges.lean` y sobre el teorema de sanidad de `ClayLiteral.lean`; la salida en cada caso es `[propext, Classical.choice, Quot.sound]`. Los teoremas son `p1`, `d1_zero`, `d2_zero`, `d3_zero`, `witness_C`, `witness_D`, `d5`, `d6`, `d7`, `clay_bound`, `s1`–`s6`, `s7_formal_side`, `k1_C`, `k1_D`, `k1_C_oneSided`, `k1_D_oneSided`, `zero_solution_C`, `zero_solution_D` y `ClayLiteral.altD_withoutErratum_imp_withErratum`. La misma comprobación se repitió desde un clon nuevo ([FROM_ZERO](../evidence/FROM_ZERO.md)) y contra la compilación B5 ([log de axiomas](../evidence/formal/b5/axioms.log)).

`Bridges.lean` no contiene ningún `sorry`, no hay axiomas extra, y los teoremas K1 no tienen hipótesis. Usan los teoremas ya demostrados de OpenAI, que están libres de `sorry`, así que los tres axiomas estándar son toda la base de confianza, junto con la fidelidad de `ClayLiteral` al PDF.

## Qué establece K1 y qué no

`k1_C : ∀ ν, 0 < ν → AltC ν` y `k1_D : ∀ ν, 0 < ν → AltD_withErratum ν` **no tienen hipótesis**. Parten de los teoremas internos de OpenAI (`NavierStokesR3.theorem_1_1`, `PeriodicPaper.periodic_corollary`), cuyo testigo es u₀ = 0 y una fuerza suave en todo ℝ × ℝ³, y usan solo `propext`, `Classical.choice` y `Quot.sound`.

**La suavidad en t = 0 no decide el resultado, entre estas dos definiciones.** `ClayLiteral` transcribe C^∞(ℝ³ × [0, ∞)) de dos maneras, como la restricción de una función C^∞ (`SmoothUpToBoundary`) y como derivadas de todo orden continuas hasta t = 0 (`SmoothOneSided`), y K1 está demostrado bajo ambas: `k1_C_oneSided`, `k1_D_oneSided`. `SmoothOneSided` se define como el `ContDiffOn` de Mathlib en el semiespacio cerrado; si eso, o la lectura por restricción, es lo que Clay quiere decir es el punto de revisión 1 en [`K0_REVIEW.md`](K0_REVIEW.md), y los nombres no demuestran nada por sí mismos. **(C) no usa la fe de erratas;** la pregunta sobre la presión periódica (S7) afecta solo a (D).

El resultado es relativo a la fidelidad de `ClayLiteral` al PDF, que ninguna persona independiente ha revisado; los puntos por verificar están en [`K0_REVIEW.md`](K0_REVIEW.md). (D) sin la fe de erratas sobre las soluciones no está demostrado (fila S7). `zero_solution_C` y `zero_solution_D` comprueban que las condiciones de solución de ClayLiteral se pueden satisfacer, así que "no existe solución" no es vacío.

**Cómo se cerró D4.** Leer C^∞(ℝ³ × [0, ∞)) como una restricción vuelve inmediata a S4, pero exige una extensión suave de la fuerza (D4). No se usó ningún teorema general de extensión: la propia construcción de OpenAI demuestra que la fuerza es suave en todo ℝ × ℝ³, así que es su propia extensión.

Todos los teoremas, comprobados con `#print axioms` en Lean 4.34.0-rc2: `k1_C`, `k1_D`, `k1_C_oneSided`, `k1_D_oneSided`, `witness_C`, `witness_D`, `d1_zero`, `d2_zero`, `d3_zero`, `d5`, `d6`, `d7`, `s1`–`s6`, `s7_formal_side`, `p1`, `clay_bound`, `zero_solution_C`, `zero_solution_D`: `[propext, Classical.choice, Quot.sound]`. `Bridges.lean` no contiene ningún `sorry`.
