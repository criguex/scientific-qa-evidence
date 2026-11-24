# La auditoría paso a paso: historias, criterios y casos de prueba

Esta página cuenta la auditoría como la cuenta un equipo de QA cuando revisa una versión de software antes de salir a producción. Hay historias de usuario, criterios de aceptación que se responden con **sí** o **no**, escenarios escritos en Gherkin, casos de prueba, ejecuciones con fecha y, al final, los defectos encontrados y lo que falta.

Todo sale de la evidencia que ya está en este repositorio. Cada criterio enlaza el registro que lo respalda. Si un criterio no se puede responder con evidencia, la respuesta es **no**, aunque yo crea que sí.

**Versión interactiva, con ejemplos visuales:** [criguex.github.io/scientific-qa-evidence/metodologia](https://criguex.github.io/scientific-qa-evidence/metodologia/) · [in English](https://criguex.github.io/scientific-qa-evidence/methodology/)

[Volver al README](../README.es.md) · [Versión en inglés de esta página](METHODOLOGY.md) · [Escenarios en Gherkin](../features/) · [Cada afirmación con su evidencia](../CLAIMS.md) · [Glosario](GLOSSARY.md)

## Las palabras que se usan aquí

| Palabra | Qué es | Ejemplo en esta auditoría |
| --- | --- | --- |
| Historia de usuario (HU) | Lo que alguien necesita y para qué | «Como revisor, quiero que las demostraciones compilen, para saber que Lean revisó cada paso» |
| Criterio de aceptación (CA) | Una pregunta de sí o no que decide si la historia se cumple | «¿Compila desde el commit fijado con código de salida 0?» |
| Escenario (Gherkin) | El criterio escrito como **Dado** (el contexto), **Cuando** (la acción) y **Entonces** (el resultado que se puede medir) | Dado el commit `f9e8bc5`, cuando lo compilo, entonces termina con código 0 |
| Caso de prueba (CP) | Lo que se hace concretamente para responder el criterio | Compilar sin caché y revisar que cada archivo `.olean` sea nuevo |
| Ejecución | Una corrida real del caso, con fecha, comando y resultado | B4, 21 de octubre de 2026, 1 h 29 min, código 0 |
| Evidencia | El registro que cualquiera puede revisar | El log, el recibo con su hash, el JSON de resultados |
| Defecto | Algo que no hizo lo que debía | Una compilación que creía limpia había recibido paquetes ya compilados |

Una aclaración importante: **la demostración es de OpenAI**. Aquí no se demuestra nada nuevo. Lo que se prueba es la evidencia: si compila, si el enunciado es el correcto, si corresponde a la pregunta de Clay y si otra persona lo puede repetir.

## El método, en siete pasos

1. **Entender qué se pide.** Se escribe la necesidad como historia de usuario: quién la tiene, qué quiere y para qué.
2. **Analizar antes de probar.** Se pregunta «¿qué podría salir mal?» y se ordenan los riesgos. Por ejemplo, que el enunciado verificado no sea la pregunta oficial, o que una compilación use piezas ya hechas sin decirlo.
3. **Escribir los criterios de aceptación.** Cada riesgo se vuelve una pregunta de sí o no. Si no se puede responder con evidencia, no sirve como criterio.
4. **Escribir los escenarios en Gherkin.** Cada criterio se escribe con Dado, Cuando y Entonces, en lenguaje natural, antes de ejecutar nada.
5. **Diseñar los casos de prueba.** Cada escenario se vuelve una o más acciones concretas: compilar, correr el verificador o cambiar un símbolo del enunciado para ver si lo nota.
6. **Ejecutar y guardar la evidencia.** Cada corrida deja su comando, su versión, su hash y su código de salida, incluidas las que fallaron.
7. **Decidir y reportar.** Cada criterio queda en sí o no, con su evidencia. Los defectos se registran, también los míos. Lo que falta se dice claramente.

Hay una regla que atraviesa todo: **la máquina revisa la cuenta, las trampas revisan a la máquina y una persona revisa la pregunta.** Verificar (la máquina) no es lo mismo que validar (una persona decide si era la pregunta correcta).

## Resumen: seis historias, 24 criterios

| HU | La pregunta, en palabras simples | Criterios que cumplen | Escenarios |
| --- | --- | --- | --- |
| [HU-1](#hu-1--las-demostraciones-compilan) | ¿Lean revisó cada paso de la demostración? | **3 de 3** | [01-compilacion.feature](../features/01-compilacion.feature) |
| [HU-2](#hu-2--otros-verificadores-dicen-lo-mismo) | ¿Otros verificadores dicen lo mismo? | **4 de 4** | [02-verificadores.feature](../features/02-verificadores.feature) |
| [HU-3](#hu-3--el-enunciado-no-deja-pasar-trampas) | ¿El enunciado verificado es exactamente el publicado? | **4 de 4** | [03-trampas-al-enunciado.feature](../features/03-trampas-al-enunciado.feature) |
| [HU-4](#hu-4--es-la-pregunta-de-clay) | ¿Es la pregunta oficial del Instituto Clay? | **2 de 4** | [04-pregunta-de-clay.feature](../features/04-pregunta-de-clay.feature) |
| [HU-5](#hu-5--otra-persona-lo-repite-sin-mí) | ¿Otra persona lo puede repetir sin mí? | **2 de 4** | [05-reproducible.feature](../features/05-reproducible.feature) |
| [HU-6](#hu-6--la-evidencia-es-trazable-y-la-herramienta-se-revisa-a-sí-misma) | ¿La evidencia es confiable y la herramienta se revisa a sí misma? | **5 de 5** | [06-trazabilidad.feature](../features/06-trazabilidad.feature) |
| **Total** | | **20 de 24** | |

**Lectura rápida.** Lo que depende de máquinas y de trampas cumple. Lo que depende de otras personas todavía no: falta que un experto revise la transcripción de Clay y que alguien distinto a mí recompile en Lean. Por eso esto no es una certificación.

---

## HU-1 · Las demostraciones compilan

> **Como** revisor de la demostración,
> **quiero** que el código que publicó OpenAI compile desde una versión fija,
> **para** saber que Lean revisó cada paso y que no hay pasos sin demostrar.

**Por qué importa.** En Lean, si un paso de la demostración está mal, el programa no compila. Compilar es la primera prueba: si no pasa, no tiene sentido seguir. El riesgo es que la compilación use piezas que otra persona compiló antes y que nadie volvió a revisar.

### Criterios de aceptación

| CA | Pregunta | ¿Cumple? | Evidencia |
| --- | --- | --- | --- |
| CA-1.1 | ¿El código de OpenAI en el commit `f9e8bc5` compila y termina con código de salida 0? | **Sí** | [compilaciones B1–B4](../evidence/formal/cd-validation/README.md), [B5](../evidence/formal/b5/), [nube](../evidence/lean-cloud-2026-10-23/README.md) |
| CA-1.2 | ¿Compila con todas las dependencias de Lean construidas en la máquina, sin descargar piezas ya compiladas? | **Sí** | [B4 y B5 sin caché](../evidence/formal/cd-validation/README.md#b4--no-cache-build-2026-10-21) |
| CA-1.3 | ¿Las conclusiones dependen solo de los tres axiomas estándar de Lean, sin pasos pendientes (`sorry`)? | **Sí** | [auditoría de axiomas](../evidence/formal/b5/axioms.log) |

### Casos de prueba y ejecuciones

| Caso | Qué se hizo | Ejecución | Resultado |
| --- | --- | --- | --- |
| CP-1.1 | Compilar desde el commit fijado, reutilizando las cachés de dependencias | B1 · 20-oct · 11.424 tareas | Código 0 |
| CP-1.1 | Compilar con la caché oficial de Mathlib, como lo indica OpenAI | B2 · 20-oct | Código 0 |
| CP-1.1 | Recompilar en un contenedor en la nube, operado por un agente de IA bajo mi dirección | 23-oct · Lean v4.34.0-rc2 | **609 de 609** módulos, código 0 |
| CP-1.2 | Compilar Mathlib en la máquina, con la caché vacía | B3 · 21-oct · 1 h 27 min | Código 0, pero **con un defecto mío**: 7 dependencias llegaron ya compiladas ([D-1](#defectos-encontrados)) |
| CP-1.2 | Compilar todo sin caché (`lake --no-cache build`) y revisar que cada `.olean` sea más nuevo que el inicio | B4 · 21-oct · 1 h 29 min | Código 0, ningún paquete descargado |
| CP-1.2 | Repetir la compilación sin caché para la versión 1.3.0 | B5 · 21/22-oct · 1 h 15 min 39 s | Código 0, los 11.406 `.olean` nuevos |
| CP-1.3 | Preguntarle a Lean de qué axiomas dependen los teoremas finales | B5 | Solo `propext`, `Classical.choice` y `Quot.sound` |

**Qué no prueba.** Todas las compilaciones reutilizaron el instalador de Lean y los binarios de los verificadores, y corrieron en máquinas que yo escogí. Compilar demuestra que la cuenta está bien hecha, no que sea la cuenta correcta (eso es HU-3 y HU-4).

**Campaña de versiones (24-nov).** Repetí las comprobaciones sobre tres versiones de Lean, con un plan registrado antes de correr ([resultados](../experiments/version-port/RESULTS.es.md)). En R0, la versión auditada (v4.34.0-rc2), todo dio lo registrado: compilación con código 0, solo axiomas estándar, Comparator con los dos kernels, `leanchecker --fresh`, lean4lean, las 6 trampas y los 35 teoremas de los puentes. En R1 (v4.34.0) y R2 (v4.35.0) los enunciados de los dos retos compilan sin cambios, pero las pruebas no: fallan 15 módulos con 103 errores en R1 y 20 módulos con 121 errores en R2, por cambios en la API de Mathlib. No es un defecto de las demostraciones, que siguen compilando en la versión fijada; dice que están atadas a esa versión. El port de las pruebas está en curso. Ninguno de estos resultados cambia los criterios de HU-1, que se refieren a la versión fijada.

---

## HU-2 · Otros verificadores dicen lo mismo

> **Como** revisor,
> **quiero** que verificadores distintos acepten la misma demostración,
> **para** no depender de un solo programa que podría tener un error.

**Por qué importa.** Si el revisor tiene un error, puede aceptar algo falso. Con varios revisores escritos por separado, ese riesgo baja, aunque no desaparece.

### Criterios de aceptación

| CA | Pregunta | ¿Cumple? | Evidencia |
| --- | --- | --- | --- |
| CA-2.1 | ¿Comparator, con el kernel de Lean, acepta las soluciones de (C), (D) y Euler en todas las compilaciones? | **Sí** | [revalidación](../evidence/formal/cd-validation/README.md), [registro del 20-oct](../evidence/formal/comparator/README.md) |
| CA-2.2 | ¿Un segundo verificador escrito aparte (nanoda) también las acepta? | **Sí** | las mismas corridas |
| CA-2.3 | ¿Los verificadores usados incluyen todas las correcciones conocidas de errores del kernel? | **Sí** | [vigencia del kernel](../evidence/formal/kernel-currency.md) |
| CA-2.4 | ¿Las revisó una tercera implementación del kernel? | **Sí** | lean4lean `0048ed7`, recompilado sobre rc2, aceptó las dos soluciones el 24-nov ([campaña de versiones](../experiments/version-port/RESULTS.es.md)). Antes no había compilado para Lean 4.34 ([recibo](../evidence/formal/cd-validation/receipts/lean4lean.txt)) |

### Casos de prueba y ejecuciones

| Caso | Qué se hizo | Ejecución | Resultado |
| --- | --- | --- | --- |
| CP-2.1 | Correr Comparator sobre cada compilación, para Navier–Stokes y para Euler | Corridas 1 a 5, sobre B1 a B5 | Las **18 pruebas** terminaron: `Your solution is okay!` y código 0 en todas |
| CP-2.2 | Repetir la revisión del kernel desde cero (`leanchecker --fresh`) | Sobre B2 · 19,6 y 22,5 min | Código 0 en las dos soluciones |
| CP-2.3 | Comparar el código del kernel usado con las versiones que corrigen errores conocidos de 2026 | Revisión del código fuente | Idéntico a v4.33.1, v4.34.0 y v4.34.1 |
| CP-2.4 | Intentar una tercera revisión con lean4lean | Sobre B2 | No compiló: versión de Lean incompatible |
| CP-2.4 | Recompilar lean4lean `0048ed7` sobre Lean v4.34.0-rc2 y correr `lean4lean --fresh` sobre las dos soluciones | Campaña de versiones, compilación R0 · 24-nov · 24 y 30 min | Código 0 en las dos: `checked 806768 declarations` (Navier–Stokes) y `checked 788326 declarations` (Euler) ([resultados](../experiments/version-port/RESULTS.es.md)) |

**Qué no prueba.** Que tres verificadores coincidan no dice nada sobre un error que ninguno conoce. Las corridas fueron en equipos Linux míos. lean4lean se recompiló sobre rc2 y no sobre su toolchain upstream (v4.34.0), porque en las versiones nativas de lean4lean las pruebas no compilan; y corrió sobre la compilación R0 de la campaña de versiones, no sobre B1–B5.

---

## HU-3 · El enunciado no deja pasar trampas

> **Como** revisor,
> **quiero** saber que el verificador compara el enunciado exacto,
> **para** estar seguro de que lo demostrado es lo que se publicó y no una versión más fácil.

**Por qué importa.** Que algo «pase» no dice mucho si la prueba deja pasar cualquier cosa. Por eso se le ponen trampas: se cambia un solo símbolo del enunciado y se mira si el verificador lo nota. Es lo que en QA se llama **probar la prueba** (pruebas de mutación).

### Criterios de aceptación

| CA | Pregunta | ¿Cumple? | Evidencia |
| --- | --- | --- | --- |
| CA-3.1 | ¿El verificador rechaza cada cambio de un símbolo en el enunciado? | **Sí, 6 de 6** | [mutantes](../evidence/formal/cd-validation/mutants/) |
| CA-3.2 | ¿Acepta un cambio que no altera el significado (solo un comentario)? | **Sí** | [control](../evidence/formal/cd-validation/mutants/control_comment.diff) |
| CA-3.3 | ¿El enunciado del desafío coincide con el que publicó Google DeepMind? | **Sí** | [procedencia](../evidence/formal/statement-provenance/README.md) |
| CA-3.4 | ¿Sabemos qué significa un rechazo: «el enunciado cambió» y no «el teorema es falso»? | **Sí** | [controles con Mathlib](../experiments/mathlib-controls/RESULTS.md) |

### Casos de prueba y ejecuciones

Las seis trampas y el control corrieron sobre la compilación B2. Cada una tardó 1,4 minutos (el control, 7 minutos):

| Caso | La trampa | Resultado esperado | Resultado |
| --- | --- | --- | --- |
| CP-3.1a | (C) sin fuerza externa (`f = 0`) | Rechazo | **Rechazado** |
| CP-3.1b | (D) sin fuerza externa (`f = 0`) | Rechazo | **Rechazado** |
| CP-3.1c | (C) con datos periódicos en vez de datos en ℝ³ | Rechazo | **Rechazado** |
| CP-3.1d | (C) con viscosidad ≥ 0 en vez de > 0 | Rechazo | **Rechazado** |
| CP-3.1e | (D) sin la negación: existencia en vez de ruptura | Rechazo | **Rechazado** |
| CP-3.1f | Euler con tiempo T* ≤ 1/2 en vez de T* ≤ 1 | Rechazo | **Rechazado** |
| CP-3.2 | Control: cambiar solo un comentario | Aceptación | **Aceptado** |
| CP-3.3 | Comparar las 18 declaraciones con el texto público de DeepMind | Coinciden | **Coinciden**, tras normalización textual |
| CP-3.4 | 11 casos con tres teoremas que Mathlib ya demuestra, registrados antes de correrlos | Comparator rechaza todo cambio, incluso los equivalentes | **8 de 8 cambios rechazados**, 4 de ellos equivalentes |

**Repetición en la campaña de versiones (24-nov).** Sobre la compilación R0, las 6 trampas fueron rechazadas otra vez y el control fue aceptado dos veces. Para correrlas encontré que tres de los diffs publicados no aplican tal como están ([D-4](#defectos-encontrados)); se usaron las copias restauradas, cuyo hash coincide con el original.

**Qué no prueba.** Un rechazo solo dice que el enunciado cambió. Las trampas con `f = 0` no dicen nada sobre las alternativas (A) y (B) del problema, que siguen abiertas. La comparación con DeepMind es de texto: no se verificó que cada nombre apunte a lo mismo.

---

## HU-4 · Es la pregunta de Clay

> **Como** comunidad matemática,
> **quiero** que el enunciado en Lean diga lo mismo que el texto oficial del Instituto Clay,
> **para** saber si lo demostrado responde las alternativas (C) y (D) del problema.

**Por qué importa.** Este es el paso de **validar**: la máquina puede verificar una cuenta perfecta que responde otra pregunta. Ninguna herramienta lo decide sola; hace falta una persona que conozca el problema.

### Criterios de aceptación

| CA | Pregunta | ¿Cumple? | Evidencia |
| --- | --- | --- | --- |
| CA-4.1 | ¿Se revisaron una por una las 16 cláusulas del texto de Clay frente al enunciado formal? | **Sí** | [revisión de riesgos](../evidence/formal/clay-lean-risk.md) |
| CA-4.2 | ¿Los teoremas de OpenAI implican, en Lean, una transcripción literal de (C) y (D) de Clay? | **Sí** | [puentes](../bridges/README.md) |
| CA-4.3 | ¿Un experto independiente revisó esa transcripción contra el PDF de Clay? | **No** | [hoja de revisión K0](../bridges/K0_REVIEW.md), sin revisar |
| CA-4.4 | ¿Está decidida la lectura de la presión periódica en (D)? | **No** | [correspondencia con Clay](../evidence/formal/clay-correspondence.md) |

### Casos de prueba y ejecuciones

| Caso | Qué se hizo | Resultado |
| --- | --- | --- |
| CP-4.1 | Comparar cada cláusula de Clay con el enunciado formal, ordenadas por riesgo | **16 cláusulas**: 6 coinciden directamente, 9 coinciden mediante hechos estándar y **1 necesita una decisión humana** |
| CP-4.2 | Escribir en Lean el texto de Clay tal cual (`ClayLiteral.lean`) y demostrar que los teoremas de OpenAI lo implican | `k1_C` y `k1_D` demostrados para toda viscosidad > 0, con los tres axiomas estándar y bajo las dos lecturas de «suave» en el tiempo cero. De 18 filas de puentes: 16 demostradas, K0 escrita y no vacía, S7 interpretativa |
| CP-4.2 | Control: comprobar que la solución cero cumple todas las condiciones de Clay | Cumple, así que el resultado no es vacío |
| CP-4.3 | Pedir revisión de la transcripción, con 14 puntos para comparar contra el PDF | **Pendiente**: nadie la ha revisado |
| CP-4.4 | Consultar al Instituto Clay sobre la presión periódica en (D) | **Sin decisión**: no la interpretaron |

**Qué no prueba.** La conexión con Clay es tan buena como mi transcripción, y nadie independiente la ha revisado. Tampoco se revisa si la demostración en Lean sigue el artículo escrito de OpenAI; eso lo discute [arXiv:2610.08144](https://arxiv.org/abs/2610.08144).

---

## HU-5 · Otra persona lo repite sin mí

> **Como** persona que quiere revisar este trabajo,
> **quiero** correr las comprobaciones en mi computador y obtener el mismo resultado,
> **para** no tener que confiar en lo que dice el autor.

**Por qué importa.** Una evidencia que solo funciona en la máquina de quien la hizo no es evidencia para nadie más. La **huella** es un código corto que resume el resultado: si la tuya y la mía coinciden para la misma versión de los datos, vimos exactamente lo mismo.

### Criterios de aceptación

| CA | Pregunta | ¿Cumple? | Evidencia |
| --- | --- | --- | --- |
| CA-5.1 | ¿`python verificar.py` da la misma huella en Windows, macOS y Linux? | **Sí** | [GitHub Actions](../.github/workflows/verify.yml) |
| CA-5.2 | ¿Otras personas lo corrieron en su computador y les dio la misma huella? | **Sí** | [reportes](../evidence/reproductions/README.md) |
| CA-5.3 | ¿Hay un reporte de una persona desde Linux? | **No** | [reportes](../evidence/reproductions/README.md) |
| CA-5.4 | ¿Alguien distinto a mí recompiló las demostraciones en Lean? | **No** | [guía de reproducción](INDEPENDENT_REPRODUCTION.md) |

### Casos de prueba y ejecuciones

| Caso | Qué se hizo | Ejecución | Resultado |
| --- | --- | --- | --- |
| CP-5.1 | Correr las seis comprobaciones de `verificar.py` en cada push | CI en cada push: Ubuntu (Python 3.12), macOS y Windows (Python 3.9 y 3.12) | Misma huella en todos. Versión vigente `c8edd482375d` → **`5292-A47D-AFA5`** |
| CP-5.2 | Pedir a otras personas que lo corran y lo reporten con el formulario | 24-oct · 4 reportes de 3 personas (Windows 11 y tres Mac) | Los 4 coinciden con su versión: `C5F0-F1A8-2F4D` |
| CP-5.3 | Recibir un reporte desde Linux hecho por una persona | — | **Pendiente** |
| CP-5.4 | Recompilar en Lean sin mi intervención, con la guía y la plantilla de reporte | — | **Pendiente** |

**Qué no prueba.** Ninguna de esas personas es independiente en sentido estricto. `verificar.py` revisa la evidencia guardada; no recompila Lean, que toma más de una hora.

---

## HU-6 · La evidencia es trazable y la herramienta se revisa a sí misma

> **Como** auditor,
> **quiero** que cada resultado apunte a un archivo intacto y que las herramientas reporten sus propios fallos,
> **para** confiar en la evidencia y no solo en el informe.

**Por qué importa.** Un informe puede decir «todo pasó» aunque un log se haya cambiado o la herramienta haya fallado en silencio. Este paso prueba la evidencia y prueba las pruebas.

### Criterios de aceptación

| CA | Pregunta | ¿Cumple? | Evidencia |
| --- | --- | --- | --- |
| CA-6.1 | ¿Cada archivo de evidencia conserva el hash SHA-256 registrado? | **Sí** | [SHA256SUMS.txt](../evidence/SHA256SUMS.txt) |
| CA-6.2 | ¿El README, CLAIMS.md y los registros dicen los mismos números? | **Sí** | [test_consistency.py](../evidence/test_consistency.py) |
| CA-6.3 | ¿Se detecta un log alterado o que falta, aunque el procedimiento publicado no lo note? | **Sí** | [revisión de recibos](../experiments/receipt-check/RESULTS.md) |
| CA-6.4 | ¿Las pruebas numéricas atrapan los errores sembrados y dejan visibles los que no? | **Sí** | [evidencia numérica](../evidence/README.md) |
| CA-6.5 | ¿La herramienta reporta sus propios fallos en vez de dar un éxito falso? | **Sí** | [test_runner.py](../evidence/numerical/source/test_runner.py) |

### Casos de prueba y ejecuciones

| Caso | Qué se hizo | Resultado |
| --- | --- | --- |
| CP-6.1 | Recalcular el SHA-256 de cada archivo de evidencia (paso 1 de `verificar.py`) | OK en cada corrida del CI |
| CP-6.2 | Cruzar los números del README y de CLAIMS.md con los registros legibles por máquina (paso 4) | OK |
| CP-6.3 | Sobre archivos auténticos, nombrar en un recibo un log que no existe | El procedimiento publicado sale con código 0; la revisión de recibos (P6) sale con código 1 y lo detecta |
| CP-6.4 | Correr 84 variantes numéricas por equipo, en macOS y Linux | **27 PASS · 54 KILLED · 3 SURVIVED**, idéntico en los dos equipos. Las 54 eliminadas son 51 comportamientos distintos; los 3 sobrevivientes son cambios mínimos que se dejaron visibles a propósito |
| CP-6.5 | Inyectar fallos en el oráculo y en el simulador | Antes del arreglo decía `oracle_valid: true` ([D-3](#defectos-encontrados)); ahora marca `INCONCLUSIVE` y sale con código 2 |

**Qué no prueba.** Los modelos numéricos son sintéticos: son cálculos de software, no mediciones físicas. Un hash detecta cambios frente a un valor confiable, pero no prueba quién creó el archivo si alguien puede cambiar el archivo y el valor a la vez.

---

## Defectos encontrados

| ID | Defecto | Dónde | Cómo se encontró | Estado |
| --- | --- | --- | --- | --- |
| D-1 | Una compilación que creía limpia (B3) había recibido 7 dependencias ya compiladas, y el log no lo mostraba | Mi trabajo | Revisando las fechas de los `.olean` contra el inicio de la compilación | Corregido: B4 y B5 compilan todo en la máquina |
| D-2 | Dos corridas reportadas como «la misma compilación» habían usado compilaciones distintas | Mi trabajo | Recibos por corrida, con sus hashes originales | Corregido: cada corrida dice su compilación |
| D-3 | El ejecutor numérico decía `oracle_valid: true` cuando el oráculo fallaba o devolvía NaN | Mi trabajo | Probando la propia herramienta con fallos inyectados | Corregido: ahora da `INCONCLUSIVE` |
| D-4 | Tres de los siete diffs de mutantes publicados (`domain_R3_to_periodic_data`, `force_zero_R3`, `force_zero_periodic`) no aplican tal como están: les falta la última línea de contexto. Restaurada esa línea, el SHA-256 coincide con el original de `PROVENANCE.md` | Mi trabajo | Al repetir los mutantes en la campaña de versiones (24-nov), `git apply` se detuvo con `corrupt patch` | Documentado: copias restauradas en [`R0/diffs/`](../experiments/version-port/R0/diffs/); los publicados no se cambian, para conservar la huella |
| — | Defectos en las demostraciones de OpenAI | — | Todas las historias de arriba | **Ninguno encontrado** dentro de este alcance |

Los cuatro defectos fueron míos, y la auditoría los encontró y los declaró en público. Están en [FINDINGS.md](../FINDINGS.md) como hallazgos 1, 3, 8 y 9. Los tres primeros se corrigieron. El cuarto se documentó sin tocar los archivos publicados, porque cambiarlos cambiaría la versión de los datos y la huella. Además, el hallazgo 7 no es un defecto: la presión periódica en (D) es un punto que deben interpretar los matemáticos (CA-4.4).

## Matriz de trazabilidad

| Criterio | Escenario Gherkin | Caso | Ejecución | ¿Cumple? |
| --- | --- | --- | --- | --- |
| CA-1.1 | Compila desde el commit fijado | CP-1.1 | B1, B2, nube 23-oct | Sí |
| CA-1.2 | Compila sin piezas ya compiladas | CP-1.2 | B4, B5 | Sí |
| CA-1.3 | Solo los axiomas estándar | CP-1.3 | B5 | Sí |
| CA-2.1 | El kernel de Lean acepta | CP-2.1 | Corridas 1–5 | Sí |
| CA-2.2 | nanoda acepta | CP-2.1 | Corridas 1–5 | Sí |
| CA-2.3 | Kernel al día | CP-2.3 | Revisión del código fuente | Sí |
| CA-2.4 | Tercera implementación | CP-2.4 | lean4lean sobre R0, 24-nov | Sí |
| CA-3.1 | Rechaza cada trampa | CP-3.1a–f | 6 mutantes sobre B2 | Sí |
| CA-3.2 | Acepta el control | CP-3.2 | Control sobre B2 | Sí |
| CA-3.3 | Coincide con DeepMind | CP-3.3 | Comparación textual | Sí |
| CA-3.4 | Un rechazo no es un «falso» | CP-3.4 | 11 casos con Mathlib | Sí |
| CA-4.1 | 16 cláusulas revisadas | CP-4.1 | Revisión de riesgos | Sí |
| CA-4.2 | Implica la transcripción de Clay | CP-4.2 | `k1_C`, `k1_D` | Sí |
| CA-4.3 | Transcripción revisada por un experto | CP-4.3 | — | No |
| CA-4.4 | Presión periódica decidida | CP-4.4 | — | No |
| CA-5.1 | Misma huella en tres sistemas | CP-5.1 | CI en cada push | Sí |
| CA-5.2 | Misma huella en otras personas | CP-5.2 | 4 reportes, 24-oct | Sí |
| CA-5.3 | Reporte de Linux | CP-5.3 | — | No |
| CA-5.4 | Recompilación independiente | CP-5.4 | — | No |
| CA-6.1 | Hashes intactos | CP-6.1 | CI | Sí |
| CA-6.2 | Documentos consistentes | CP-6.2 | CI | Sí |
| CA-6.3 | Log alterado detectado | CP-6.3 | P6 | Sí |
| CA-6.4 | Trampas numéricas | CP-6.4 | macOS y Linux | Sí |
| CA-6.5 | La herramienta reporta sus fallos | CP-6.5 | Fallos inyectados | Sí |

## Qué falta para que los 24 criterios digan sí

1. **CA-4.3:** que alguien que sepa Lean o conozca el problema revise [`bridges/ClayLiteral.lean`](../bridges/ClayLiteral.lean) con la [hoja K0](../bridges/K0_REVIEW.md).
2. **CA-4.4:** que un matemático decida cómo leer la presión periódica en (D).
3. **CA-5.4:** que alguien distinto a mí recompile en Lean con la [guía](INDEPENDENT_REPRODUCTION.md).
4. **CA-5.3:** un reporte de `verificar.py` desde Linux, con el [formulario](https://github.com/criguex/scientific-qa-evidence/issues/new?template=reproduccion.yml).

Los cuatro dependen de personas, no de máquinas. Esa es la última puerta: **sean el árbitro**.
