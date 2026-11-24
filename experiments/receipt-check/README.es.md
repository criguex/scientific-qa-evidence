> Traducción al español de [README.md](README.md). Si hay alguna diferencia, vale el original.

# Comprobación de recibos sobre registros auténticos: un estudio de caso de controles de integridad

¿Una comprobación de que cada recibo corresponde al artefacto que nombra detecta fallas de evidencia que el procedimiento de verificación publicado por OpenAI no detecta, sobre los mismos archivos auténticos? Dos casos registrados antes de correrlos.

| Archivo | Propósito |
| --- | --- |
| [`DESIGN.md`](DESIGN.md), [`expected.json`](expected.json) | Caso 1, registrado antes de correrlo: un recibo nombra un log que no existe |
| [`DESIGN2.md`](DESIGN2.md), [`expected2.json`](expected2.json) | Caso 2, registrado antes de correrlo: un log viejo de otra corrida con el nombre correcto |
| [`STATUS.md`](STATUS.md) | Cronología: un primer intento abortado, una enmienda, las dos corridas, los scripts tal como se corrieron, y el endurecimiento después de la revisión |
| [`RESULTS.md`](RESULTS.md), [`RESULTS2.md`](RESULTS2.md) | Resultados, la afirmación que respalda cada uno, y notas de registro |
| [`run.sh`](run.sh), [`run2.sh`](run2.sh) | Corren el procedimiento publicado sobre una copia de un árbol compilado desde la fuente, escriben el paquete de evidencia y evalúan cada variante; necesitan `QA_COMMIT`; tal como están escritos corren bajo WSL en un equipo Windows, midiendo la unidad de Windows con PowerShell y usando las rutas locales de ese equipo |
| [`preflight.sh`](preflight.sh) | Comprobaciones compartidas: espacio en disco del equipo, toolchain fijado, revisiones de `lake-manifest.json`, hashes de los binarios de herramientas y de Comparator; aborta ante cualquier discrepancia |
| [`check_p6.py`](check_p6.py) | Comprobación X1: P6 del evaluador congelado v2.2, que prueba que cada log nombrado por un recibo existe y que los pasos salieron con 0 |
| [`check_hash.py`](check_hash.py) | Comprobación X2: cada log nombrado también debe coincidir con el SHA-256 registrado cuando corrió su paso |
| [`test_results.py`](test_results.py) | Recalcula las dos comprobaciones sobre los paquetes publicados y revisa que la salida del procedimiento no haya cambiado; corre en el CI |
| [`results/`](results/), [`results2/`](results2/) | Recibos, paquetes, logs y salidas de las dos corridas |

**Conclusión.** En este experimento, P6 detecta una inconsistencia de trazabilidad que no cambia el resultado de Comparator, y un log viejo con el nombre correcto solo lo atrapa la comprobación por hash. No significa que Comparator aceptara una prueba falsa. Atar los pasos a hashes es práctica establecida ([in-toto](https://in-toto.io/), [procedencia SLSA](https://slsa.dev/provenance/v1)); esto es un estudio de caso, no una técnica nueva, y no se ha hecho ninguna comparación con esas herramientas. Solicitud de revisión: [`docs/REVIEW_REQUEST.md`](../../docs/REVIEW_REQUEST.md).
