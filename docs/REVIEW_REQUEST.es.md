> Traducción al español de [Request for review: a case study of integrity controls for Lean evidence](REVIEW_REQUEST.md). Si hay alguna diferencia, vale el original.

# Solicitud de revisión: un estudio de caso de controles de integridad para evidencia de Lean

Esta página pide revisión de un resultado estrecho sobre la **trazabilidad de la evidencia** en un flujo de verificación en Lean reproducible. No se trata de la matemática: la prueba de OpenAI fue aceptada en cada corrida.

## El resultado

Sobre los mismos archivos auténticos (una compilación desde la fuente de [openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler) en `f9e8bc5`, Lean 4.34.0-rc2, el Comparator fijado `19e111e`), se registró paso a paso el procedimiento publicado de OpenAI (`lake exe cache get`, `lake build`, `lake exe comparator ComparatorChallenges/NavierStokes.json`). Luego solo se alteró el paquete de evidencia:

| Variante | Procedimiento publicado | Comprobación de existencia P6 | Comprobación por hash |
| --- | --- | --- | --- |
| Limpia | exit 0, `Your solution is okay!` | pasa | pasa |
| Un recibo nombra un log que no está en el paquete | exit 0, salida idéntica byte a byte a la corrida limpia | marca | marca |
| Un log viejo de otra corrida, con el nombre correcto | exit 0, salida idéntica byte a byte a la corrida del log ausente | **pasa: no lo detecta** | marca |

Idéntica byte a byte significa: en el caso 1, entre la corrida limpia y la del log ausente; en el caso 2, entre la del log ausente y la del log viejo, que además coinciden con el caso 1. La corrida limpia del caso 2 tiene 13 líneas `Built …` de más, porque su primera llamada a Comparator en una copia nueva también compiló el ejecutable de Comparator.

**Conclusión.** En este experimento, P6 detecta una inconsistencia de trazabilidad que no cambia el resultado de Comparator, y un log viejo con el nombre correcto solo se detecta comparándolo con el hash registrado cuando corrió el paso. **No significa que Comparator aceptara una prueba falsa.**

**No es una técnica nueva.** Atar el comando, las entradas y las salidas de cada paso a hashes registrados es práctica establecida en la seguridad de la cadena de suministro de software: [in-toto](https://in-toto.io/) registra, para cada paso, el comando, los hashes de sus archivos de entrada y salida, su valor de retorno y su salida estándar y de error, los firma y los verifica contra un layout, y la [procedencia SLSA](https://slsa.dev/provenance/v1) registra cómo se hizo una compilación y a partir de qué dependencias con hash. Los dos fallos probados aquí son del tipo que in-toto ya detecta. Esto es, por tanto, un **estudio de caso de controles de integridad para evidencia de Lean**; no se ha hecho una comparación justa con in-toto o SLSA, y cualquier valor añadido en integración, diagnósticos específicos de Lean o facilidad de uso todavía tendría que demostrarse.

Los dos casos se registraron antes de correrlos, con un primer intento abortado y una enmienda registrada: [caso 1](../experiments/receipt-check/RESULTS.md), [caso 2](../experiments/receipt-check/RESULTS2.md), [estado](../experiments/receipt-check/STATUS.md).

## Reproducir

- **Cerca de un minuto, sin Lean:** `cd experiments/receipt-check && python3 -m unittest -v test_results` recalcula las dos comprobaciones a partir de los paquetes publicados y comprueba que la salida del procedimiento no cambió.
- **Corrida completa:** `QA_COMMIT=<commit> bash run.sh` y `run2.sh`. Tal como están escritos corren bajo WSL en una máquina Windows: miden la unidad del sistema Windows con PowerShell y usan las rutas locales de esa máquina para el árbol de compilación y las herramientas. En otra máquina hay que adaptar esas líneas de [`preflight.sh`](../experiments/receipt-check/preflight.sh); también comprueba el toolchain, las revisiones de `lake-manifest.json` y los hashes de las herramientas, y aborta ante cualquier discrepancia o falta de espacio.

## La pregunta

Los recibos atados a hash no son nuevos, así que las preguntas son más estrechas:

1. ¿Es este un **estudio de caso** justo y útil de controles de integridad aplicados a evidencia de verificación en Lean?
2. ¿Cómo sería una comparación justa con la procedencia de in-toto o SLSA sobre los mismos pasos y fallos, y qué fallos específicos de Lean (cambios al enunciado, axiomas, artefactos precompilados, fallos del arnés del oráculo) no verían esas herramientas sin comprobaciones de dominio?
3. ¿Hay un aporte que valga la pena demostrar en integración, diagnósticos o facilidad de uso, y cómo debería medirse?

## Objeciones ya conocidas

- **Trabajo previo.** in-toto ya registra el comando de cada paso, los hashes de entrada y salida, el valor de retorno y la salida, y los verifica; SLSA describe la procedencia de la compilación. Detectar un log cambiado por SHA-256 no es una técnica nueva, y la comparación aquí es solo con Comparator, no con esas herramientas.
- El procedimiento publicado no afirma comprobar recibos, así que «no lo detecta» es lo esperado. El punto es que el verificador publicado no comprueba por sí mismo que un recibo corresponda al log que referencia, y una comprobación del tipo que ofrece in-toto cierra ese vacío.
- P6, la propia comprobación de este estudio, solo prueba que un log nombrado existe; el caso 2 muestra que no detecta un log sustituido, y que una segunda comprobación sí lo atrapa. Documentar dónde falla la propia comprobación del estudio es parte del resultado.
- La comprobación por hash detecta un cambio frente a un valor de referencia confiable, aquí el hash registrado cuando corrió el paso. No autentica de dónde vino un log si alguien puede reemplazar tanto el archivo como ese valor registrado.
- Dos casos en una máquina, diseñados por el autor. No se afirma ninguna tasa de detección.

## Estado de la revisión

Solicitada a: el revisor externo que sugirió la comparación. Todavía no se ha enviado a nadie más. Las respuestas, y quién las dio, se registrarán aquí.
