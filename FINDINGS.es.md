> Traducción al español de [What the protocol found that the documented procedure does not show](FINDINGS.md). Si hay alguna diferencia, vale el original.

# Qué encontró el protocolo que el procedimiento documentado no muestra

La pregunta útil para este estudio no es si sus técnicas son nuevas; [RELATED_WORK.md](docs/RELATED_WORK.md) muestra que no lo son. La pregunta es: **¿qué pudo detectar este protocolo, en este caso, que el procedimiento documentado anteriormente no pudo?**

**Línea base.** El procedimiento de verificación documentado en el repositorio de OpenAI en `f9e8bc5`: traer la caché de Mathlib con `lake exe cache get`, correr `lake build`, y luego comprobar las formalizaciones con Comparator como se describe en `ComparatorChallenges/README.md`.

**Alcance.** Este es un registro retrospectivo de un caso. Muestra que el protocolo produjo evidencia que la línea base no produce. No mide con qué frecuencia, a qué costo ni con cuántas falsas alarmas. Eso necesita el experimento prospectivo descrito al final.

## Hallazgos

| # | Hallazgo | Elemento del protocolo que lo detectó | ¿La línea base produce esta evidencia? | Evidencia |
| --- | --- | --- | --- | --- |
| 1 | Una compilación que se creía limpia (B3) había recibido en silencio 7 dependencias como archivos precompilados de Reservoir; el log de la compilación no lo mostraba | Comprobación de artefactos: marcas de tiempo de los `.olean` frente al inicio de la compilación, más inspección de `.lake/packages` | No. La línea base descarga Mathlib precompilado a propósito y nunca pregunta qué se compiló localmente. | [cd-validation](evidence/formal/cd-validation/README.md#b3--fresh-build-2026-10-21) |
| 2 | Una compilación completa desde la fuente (B4) es posible y se verificó: todos los `.olean` posteriores al inicio de la compilación, ningún archivo traído | `lake --no-cache build` con una caché aislada, más la misma comprobación de artefactos | No. La línea base usa la caché de Mathlib. | [cd-validation](evidence/formal/cd-validation/README.md#b4--no-cache-build-2026-10-21) |
| 3 | Dos corridas reportadas como «la misma compilación» habían usado compilaciones distintas | Recibos por corrida y hashes originales, etiquetados por compilación | No. La línea base no tiene registros de corridas. | [tabla de compilaciones](evidence/formal/cd-validation/README.md#builds-used-by-each-run) |
| 4 | Comparator rechaza cada cambio de un símbolo al enunciado y acepta un cambio de solo comentario | Mutantes del enunciado con un control negativo | No. La línea base solo muestra un resultado positivo, que por sí solo no puede distinguir una comprobación exacta de una permisiva. | [mutantes](evidence/formal/cd-validation/mutants/) |
| 5 | Las 18 declaraciones del enunciado del desafío coinciden con el enunciado público de DeepMind tras la normalización textual | Comparación de procedencia del enunciado | No. La línea base comprueba la prueba contra el desafío, no el desafío contra una fuente pública. | [procedencia del enunciado](evidence/formal/statement-provenance/README.md) |
| 6 | La fuente del kernel usada incluye todas las correcciones de solidez del kernel de 2026, y nanoda es posterior a su corrección | Comprobación de vigencia del kernel | No. La línea base no registra ni comprueba las versiones de los verificadores frente a bugs conocidos. | [vigencia del kernel](evidence/formal/kernel-currency.md) |
| 7 | La presión periódica en (D) depende de leer la errata de Clay como condición sobre las soluciones | Revisión de riesgos cláusula por cláusula, por dirección del riesgo | No. Comparator compara contra el desafío, no contra el texto de Clay. | [revisión de riesgos de Clay](evidence/formal/clay-lean-risk.md) |
| 8 | El runner numérico reportaba `oracle_valid: true` cuando el oráculo había lanzado una excepción o devuelto NaN | Probar el propio arnés de pruebas: fallos de oráculo y de simulador sembrados | No aplica a la línea base formal. Muestra que el protocolo comprueba sus propias herramientas. | [test_runner.py](evidence/numerical/source/test_runner.py) |
| 9 | Tres de los siete diffs de mutantes publicados (`domain_R3_to_periodic_data`, `force_zero_R3`, `force_zero_periodic`) no aplican tal como están publicados: a cada uno le falta su última línea, una línea de contexto formada por un solo espacio, así que `git apply` se detiene con `corrupt patch`. Con esa línea restaurada, el SHA-256 de cada archivo es igual al original registrado en `PROVENANCE.md`, así que las corridas originales usaron diffs completos y la línea se perdió al hacer las copias públicas | Volver a correr los mutantes desde los archivos publicados en la campaña de versiones (2026-11-24), comprobados contra los hashes originales de `PROVENANCE.md` | No. La línea base no tiene mutantes del enunciado ni registro de los hashes de sus entradas. | [port de versión](experiments/version-port/RESULTS.es.md#hallazgos-sobre-la-evidencia-publicada), [copias restauradas](experiments/version-port/R0/diffs/) |

Los hallazgos 1, 3, 8 y 9 fueron defectos del propio trabajo anterior de este estudio, detectados por pasos posteriores del mismo protocolo antes o después de la publicación, y declarados en público. Los hallazgos 1, 3 y 8 se corrigieron. En el hallazgo 9 los diffs publicados se dejaron sin cambios, porque editarlos cambiaría la versión de los datos y su huella; las copias restauradas y sus hashes están publicadas junto a la corrida que las usó. Se listan porque una auditoría capaz de detectar sus propios errores es parte de lo que ofrece el protocolo.

## Qué no muestra esto

- No muestra que la línea base esté equivocada. El procedimiento de OpenAI responde una pregunta más estrecha, si las pruebas verifican, y la responde.
- No muestra que el protocolo encuentre problemas con más frecuencia que otros procedimientos. Un caso no es una tasa.
- Ninguno de estos hallazgos es un defecto en las pruebas de OpenAI. El hallazgo 7 es un punto interpretativo para matemáticos, no un error.

## Cómo demostrar la diferencia

Un experimento prospectivo, definido y congelado antes de correrlo:

1. **Clases de fallo** tomadas de los hallazgos anteriores: artefactos precompilados ocultos, compilaciones mal etiquetadas, un enunciado cambiado o debilitado, un enunciado que no coincide con su fuente pública, una versión de verificador con un bug de solidez conocido, y un arnés de pruebas que reporta éxito ante un fallo.
2. **Inyección a ciegas.** Alguien distinto de quien corre las comprobaciones siembra fallos en copias de proyectos Lean pequeños y casos numéricos, con copias limpias mezcladas como controles.
3. **Los dos procedimientos sobre cada copia:** la línea base y el protocolo.
4. **Métricas:** fallos detectados, falsas alarmas en copias limpias y costo en tiempo real.

Un resultado de ese experimento, no esta tabla, respaldaría la afirmación de que el protocolo detecta clases de problemas que la línea base no detecta.

**Resultado (2026-10-21), tras la revisión.** Leído como benchmark de regresión determinista: con el evaluador v2 corregido, las comprobaciones del protocolo marcan las clases de fallo F1, F2, F4 y F5 donde la línea base pasa, los dos marcan el control positivo, y la plantilla limpia completa pasa los dos. La primera corrida (v1) se conserva con fe de erratas: su evaluador tenía defectos, su «0 falsas alarmas» no se sostiene, y F2 es una diferencia textual y no un enunciado debilitado. Registros: [v2](experiments/blind-faults/v2/README.md) y [v1 con fe de erratas](experiments/blind-faults/RESULTS.md). Su preparación se sigue en [experiments/blind-faults/STATUS.md](experiments/blind-faults/STATUS.md).
