> Traducción al español de [README.md](README.md). Si hay alguna diferencia, vale el original.

# Evaluador v2 y benchmark de regresión determinista

v1 (`../protocol_lib.py`, congelado en `../FROZEN.md`) se conserva sin cambios para que sus resultados publicados sigan siendo reproducibles. v2 es un evaluador aparte, corregido, escrito después de una revisión externa de los resultados de v1 el 2026-10-21.

## Qué corrige v2

| Defecto de v1 | Comportamiento de v1 | Comportamiento de v2 |
| --- | --- | --- |
| Evidencia incompleta | Un reporte de axiomas vacío o truncado era **aceptado** por los dos procedimientos | Falla cerrado: `axioms-incomplete` |
| Evidencia ausente | Un artefacto faltante lanzaba `KeyError`, sin dar veredicto | Falla cerrado: `missing:<artifact>`, en los dos procedimientos |
| Recibos | P6 asumía que `comparator.log` existía; **ningún caso lo contenía** | Los recibos se comprueban contra los archivos realmente presentes |
| Salida de Comparator | No era parte del caso | `comparator.log` es un artefacto obligatorio; la línea base exige `Your solution is okay!` |

Pruebas para evidencia ausente e incompleta: [`test_protocol_v2.py`](test_protocol_v2.py) (10 pruebas, corren en el CI).

### v2.1: segunda ronda de revisión (2026-10-21)

Una segunda revisión encontró tres casos más donde v2 no fallaba cerrado. Cada uno ahora tiene una prueba de regresión, y las cinco pruebas nuevas fallan contra la versión anterior (`793ff3b`):

| Defecto | Antes (v2) | Ahora (v2.1) |
| --- | --- | --- |
| Un resumen numérico que es JSON válido pero no un objeto, como `[]` | `AttributeError`, sin veredicto | Rechazado: `numeric-summary-not-object` |
| Tablas de recibos y artefactos con encabezado pero sin filas | Aceptado | Rechazado: `receipt-no-rows`, `oleans-no-rows`; los encabezados incorrectos también se rechazan |
| Recibos cuyo código de salida no es 0 | Aceptado | Rechazado: `receipt-exit-<step>-<code>`; los recibos también deben cubrir tanto `build` como `comparator` |

15 pruebas en total. El resultado del benchmark no cambia.

### Rondas de revisión 3 y 4 (2026-10-21, por el asistente)

| Ronda | Método | Encontrado | Corregido en | Evidencia |
| --- | --- | --- | --- | --- |
| 3 · robustez | Fuzzer determinista ([`fuzz_v2.py`](fuzz_v2.py), semilla 20261021): 8.000 evaluaciones de artefactos mutados (truncamiento, basura, CRLF, BOM, líneas mezcladas, duplicadas y eliminadas, JSON que no es un objeto). Invariante: nunca lanzar una excepción. | **0 colapsos** en v2.1. El fuzzer no es débil: contra v2 (`793ff3b`) encuentra 52 colapsos, el defecto `[]` de la ronda 2. | — | `python3 fuzz_v2.py`; corre en el CI |
| 4 · semántica | Intentos dirigidos a que evidencia mala pase y evidencia buena falle | **7 defectos**, abajo | v2.2 | 8 pruebas en `Round4SemanticTests`; 7 fallan contra v2.1 (`94244a4`) |

Defectos de la ronda 4:

| # | Tipo | Entrada | v2.1 | v2.2 |
| --- | --- | --- | --- | --- |
| 1 | Falso positivo | Una segunda línea de axiomas que lista `sorryAx` | Solo se leía la primera línea | Se revisa cada línea de axiomas |
| 2 | Falso positivo | Un reporte de axiomas de un teorema distinto | El nombre del teorema se ignoraba | El teorema probado debe tener su propia línea de axiomas |
| 3 | Falso positivo | Log de Comparator con `Your solution is okay!` y también un fallo | Aceptado | Cualquier marca de fallo rechaza |
| 4 | Falso positivo | Log de compilación con una línea `error:` y la línea de éxito | Aceptado | Cualquier línea de error rechaza |
| 5 | Falso positivo | Resumen con `oracle_valid: false` pero marcado como completo | Aceptado | Rechazado: `oracle-not-valid` |
| 6 | Falsa alarma | Un recibo que empieza con un BOM UTF-8 | Rechazado como encabezado inválido | El BOM y el CRLF se normalizan |
| 7 | Falsa alarma | Un comentario inofensivo en el enunciado probado | Marcado como un enunciado distinto | Los comentarios se eliminan antes de comparar; un cambio real se sigue marcando (prueba de guarda) |

Resistieron la ronda 4 sin cambios: los finales de línea CRLF, axiomas en otro orden, un recibo duplicado cuya segunda corrida falló, y una fila de `.olean` inconsistente.

**Total: 24 pruebas** (23 pruebas unitarias más el fuzzer). El resultado del benchmark no cambia en ninguna ronda.

## v2 aplicado a los casos de v1

Correr v2 sobre los 21 casos publicados de v1 ([`v2_on_v1_cases.json`](v2_on_v1_cases.json)) marca **los 21, incluidos los 6 limpios**: sus recibos nombran un `comparator.log` que no existe, y no contienen ninguna salida de Comparator. Así que el resultado de v1 de «0 falsas alarmas en los casos limpios» dependía de que el evaluador v1 asumiera evidencia que no estaba ahí. Los casos limpios de v1 estaban incompletos, no limpios.

## Benchmark de v2

Un benchmark de regresión determinista, no un ensayo a ciegas: un caso por clase, construido a partir de la plantilla completa de v2, porque un evaluador determinista da el mismo veredicto para cada instancia de una clase. [`benchmark_v2.json`](benchmark_v2.json), producido por [`run_benchmark_v2.py`](run_benchmark_v2.py):

| Clase | Fallo sembrado | Línea base | Protocolo | Comprobación del protocolo |
| --- | --- | --- | --- | --- |
| C | ninguno (limpio) | pass | pass | — |
| F1 | una dependencia llegó precompilada; log de compilación limpio | pass | **flag** | P1 |
| F2 | el enunciado de la prueba difiere textualmente de la referencia fijada | pass | **flag** | P2 |
| F4 | el oráculo falló pero el harness reporta una corrida completa | pass | **flag** | P5 |
| F5 | un recibo nombra un log que la compilación no escribió | pass | **flag** | P6 |
| F6 | control positivo: depende de `sorry` | flag | flag | axiomas de la línea base |

**F2 es una diferencia textual, no un debilitamiento.** Su edición cambia la hipótesis `nu > 0` a `nu >= 0`. Relajar una hipótesis hace el teorema más fuerte, no más débil. F2 muestra solo que P2 detecta un enunciado que difiere de su referencia.

## Costo

| Qué | Medido |
| --- | --- |
| Evaluar los artefactos de un caso | Línea base ≈ 10–11 µs, protocolo ≈ 20 µs en el Mac del autor (`seconds_per_case` en el `benchmark_v2.json` actual, de la corrida v2.2, commit `2a73983`). La primera corrida de v2 (`793ff3b`) registró cerca de 3–4 y 8–9 µs; estos tiempos varían entre corridas y con la carga de la máquina, así que solo su orden de magnitud tiene sentido |
| Producir la evidencia que lee el protocolo | No la mide este benchmark. Del estudio principal: una compilación de Lean sin caché tomó 1 h 29 min, cada corrida de Comparator 7–11 min, y cada revisión `leanchecker --fresh` unos 20 min ([cd-validation](../../../evidence/formal/cd-validation/README.md)). |

Las cifras en microsegundos son el costo de comprobar artefactos que ya existen. No dicen nada sobre el costo de generarlos, que domina en la práctica.
