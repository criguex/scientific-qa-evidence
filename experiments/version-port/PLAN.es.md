> Traducción al español de [PLAN.md](PLAN.md). Si hay alguna diferencia, vale el original.

# Migración de versión: volver a revisar las pruebas de OpenAI en versiones más recientes de Lean

**Estado: registrado antes de correr.** Escrito el 2026-11-24, antes de cualquiera de las corridas de abajo. Los resultados irán a `RESULTS.md` en esta carpeta sin editar este plan; cualquier cambio al plan se añadirá como enmienda fechada al final.

## Por qué

Hasta ahora, cada comprobación corrió sobre el toolchain que fijó OpenAI, `leanprover/lean4:v4.34.0-rc2`, con Mathlib, Comparator y lean4export en sus etiquetas `v4.34.0-rc2`. De ahí surgen dos preguntas:

1. **Un tercer kernel (AC-2.4).** lean4lean nunca examinó las pruebas porque no compilaba para Lean 4.34 ([recibo](../../evidence/formal/cd-validation/receipts/lean4lean.txt)). El 2026-11-21 su upstream pasó a v4.34.0 (commit `0048ed7`), luego a v4.35.0 (`b73a4e7`) y a v4.36.0 (`23fd034`).
2. **Robustez ante un cambio de toolchain.** Si las pruebas siguen compilando, y todos los verificadores las siguen aceptando, en versiones posteriores con correcciones de kernel más recientes, el resultado no depende de un solo release candidate.

## Objetivos

| ID | Lean | Mathlib | Comparator | lean4lean | Por qué este objetivo |
| --- | --- | --- | --- | --- | --- |
| R0 | v4.34.0-rc2 | v4.34.0-rc2 (`85e3a25`) | v4.34.0-rc2 (`19e111e`) | `0048ed7` recompilado sobre rc2 (su upstream dice v4.34.0) | La versión auditada, sin cambios. Solo lean4lean es nuevo |
| R1 | v4.34.0 | v4.34.0 (`5ed2965`) | v4.34.0 (`d03acab`) | `0048ed7` (nativo de v4.34.0) | El paso más pequeño: el release final de la misma versión menor |
| R2 | v4.35.0 | v4.35.0 (`56a0058`) | v4.35.0 (`e3dcf30`) | `b73a4e7` (nativo de v4.35.0) | El release más reciente con Lean, Mathlib y Comparator todos etiquetados. v4.36.0 queda fuera de alcance: Comparator no tiene etiqueta v4.36.0 |

nanoda: la última de `ammkrn/nanoda_lib` (`0da9f98`, 2026-11-07). lean4export: la revisión que fija cada etiqueta de Comparator.

## Qué se permite cambiar

- Las revisiones de `lean-toolchain`, `lakefile.toml` y `lake-manifest.json`.
- Código de la **prueba**, solo si una prueba deja de compilar, con cada edición conservada como diff y explicada.
- **Nunca** un enunciado. `ComparatorChallenges/*.lean` y las líneas `theorem` de las soluciones deben ser idénticas byte a byte a `f9e8bc5`. Una migración que necesite cambiar el enunciado cuenta como una migración fallida.

## Pasos por objetivo

| # | Paso | Comando (resumen) | Esperado |
| --- | --- | --- | --- |
| 1 | Clon limpio en `f9e8bc5`, en su propia carpeta | `git clone`, `git checkout f9e8bc5` | — |
| 2 | Fijar versiones (solo R1, R2) | editar el toolchain y las revisiones, `lake update` | — |
| 3 | Revisión del enunciado | `diff` de `ComparatorChallenges/` contra `f9e8bc5` | vacío |
| 4 | Compilar con la caché de Mathlib | `lake exe cache get`, `lake build` | exit 0 (R1, R2 pueden necesitar ediciones a la prueba) |
| 5 | Axiomas de los teoremas finales y los puentes | `#print axioms` | solo `propext`, `Classical.choice`, `Quot.sound` |
| 6 | Comparator, los dos kernels | `lake exe comparator ComparatorChallenges/{NavierStokes,Euler}.json` | `Your solution is okay!`, exit 0, para los dos |
| 7 | Revisión del kernel desde cero | `leanchecker --fresh` en las dos soluciones | exit 0 |
| 8 | Tercer kernel | `lean4lean --fresh` en las dos soluciones | exit 0 |
| 9 | Mutantes del enunciado | los 6 mutantes de un símbolo y el control de solo comentario de [cd-validation](../../evidence/formal/cd-validation/mutants/) | 6 rechazados, control aceptado |
| 10 | Puentes | compilar `bridges/` contra el objetivo, `#print axioms` | como en el paso 5 |

Cada paso registra su comando, hora de inicio y fin, código de salida y el SHA-256 de su log, en un recibo como los de [cd-validation](../../evidence/formal/cd-validation/receipts/).

## Cómo se leerán los resultados

- **AC-2.4 pasa a sí** solo si lean4lean acepta las dos soluciones en al menos un objetivo. Si eso ocurre en R0, la nota dice que lean4lean se recompiló sobre rc2 en vez de sobre su propio toolchain upstream.
- **Una compilación fallida, una solución rechazada o un mutante que sobrevive** se reporta tal como se encuentra, con su log, y no se vuelve a intentar en silencio. Que un verificador rechace una solución sería el resultado posible más importante, y se reportaría antes que cualquier otra cosa.
- Esto no es una reproducción independiente: el autor la corre, en su propia máquina (Linux sobre WSL2, 12 núcleos, 30 GB), con asistencia de IA. No cambia AC-5.4.
- Usar la caché de Mathlib significa que Mathlib no se compila desde la fuente en estas corridas; B4 y B5 ya lo hicieron para rc2.

## Enmienda 1 · 24 de noviembre de 2026, antes de usar cualquier cambio de demostración en un resultado

R0 terminó como se registró. R1 y R2 no compilaron: falla el código de las demostraciones por cambios en la API de Mathlib, mientras los enunciados de los desafíos siguen compilando sin cambios. Por decisión del autor, el port se intenta sin límite de tiempo. Apareció un caso no previsto: en Mathlib v4.34.0, `eLpNorm f p μ` vale ∞ cuando `f` no es `AEStronglyMeasurable`, y `MemLp` pasó a ser solo `eLpNorm < ∞`. Por eso algunos lemas **internos** de la demostración de OpenAI son falsos tal como están escritos con las definiciones nuevas (por ejemplo `NavierStokesR3.WeightedInterpolation.eLpNorm_le_rpow_mul`, que acota `eLpNorm h` sin suponer que `h` sea medible).

Qué cambia en «Qué se permite cambiar»:

- El enunciado de un lema **interno** puede recibir una hipótesis, u otro ajuste, **solo cuando lo exija un cambio de definiciones de Mathlib**. Cada cambio de este tipo se lista aparte en `R1/port/` (y `R2/port/`) con el enunciado antes y después y la razón.
- Sin cambios: `ComparatorChallenges/*.lean` y las líneas `theorem` de `NavierStokes/ComparatorSolution.lean` y `Euler/Solution.lean` siguen idénticas byte a byte a `f9e8bc5`; Comparator compara los enunciados finales con el desafío, así que un enunciado final debilitado sería rechazado. Sin `sorry`, sin axiomas nuevos, sin opciones que relajen el kernel o las comprobaciones, sin apagar linters ni `warningAsError`.
- Un port que necesite cambiar un enunciado de desafío o una línea `theorem` final sigue contando como fallido.
