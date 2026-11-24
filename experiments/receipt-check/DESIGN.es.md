> Traducción al español de [DESIGN.md](DESIGN.md). Si hay alguna diferencia, vale el original.

# Una comparación concreta: correspondencia entre recibo y log sobre registros auténticos

**Registrado antes de correrlo el 2026-10-22, antes de cualquier corrida.** **Resultados: [RESULTS.md](RESULTS.md)** — las dos variantes salieron según lo registrado. Los resultados esperados están en [`expected.json`](expected.json), y los scripts son [`run.sh`](run.sh) y [`check_p6.py`](check_p6.py).

## Pregunta

¿La comprobación **P6** de este estudio, la correspondencia entre recibos y logs, detecta una falla que el procedimiento de verificación publicado por OpenAI no detecta, cuando los dos corren exactamente sobre los mismos archivos auténticos?

El benchmark de fallos a ciegas (caso C/F5) mostró esto sobre registros sintéticos, con un modelo en Python de la línea base. Aquí la línea base es el procedimiento real, corrido de verdad.

## Montaje

- **Archivos:** una copia de un árbol de `openai/NavierStokesAndEuler` compilado desde la fuente en `f9e8bc5` (B5 según lo registrado; B4 después de la enmienda 1, ver [STATUS](STATUS.md)), el mismo toolchain Lean 4.34.0-rc2, y los mismos binarios de Comparator, lean4export, nanoda y landrun.
- **Procedimiento Z**, exactamente como lo publica OpenAI, con las tres herramientas en `PATH`: `lake exe cache get`, `lake build`, `lake exe comparator ComparatorChallenges/NavierStokes.json`.
- **Paquete de evidencia:** un envoltorio delgado registra cada paso de Z en `receipt.tsv` (paso, comando, log, código de salida), con los logs al lado, en el formato que lee P6.
- **Comprobación X:** P6 de [`protocol_lib_v2.py`](../blind-faults/v2/protocol_lib_v2.py), sin cambios desde el evaluador v2.2. `check_p6.py` llama a `protocol()` y reporta solo las marcas de P6.

## Variantes, sobre los mismos archivos

| Variante | Cambio | Z esperado | X esperado |
| --- | --- | --- | --- |
| C, control limpio | ninguno | exit 0, `Your solution is okay!` | exit 0, sin marca de P6 |
| F5, falla conocida | la fila `comparator` de `receipt.tsv` nombra `comparator-run.log`, un log que no existe; nada más cambia | exit 0, `Your solution is okay!` | exit 1, `P6:receipt-log-missing-comparator-run.log` |

Para cada variante, el paquete se coloca en el árbol del proyecto, se vuelve a correr el paso de Comparator de Z, y X se corre sobre el paquete. Cada paso se registra con su comando, el SHA-256 de su log saneado y su código de salida.

## La afirmación que esto puede respaldar, si sale como se espera

> En este caso, la comprobación de correspondencia entre recibo y log (P6) detectó un recibo que nombra un log que no está en la evidencia, y el procedimiento publicado por OpenAI, corrido sobre los mismos archivos, no lo detectó: salió con 0, porque no lee recibos.

Esa es una afirmación acotada sobre la **trazabilidad de la evidencia**, no sobre la prueba. No dice que P6 atrape todos los errores, que el procedimiento sea deficiente en su propia tarea (revisar la prueba), ni nada sobre el Problema del Milenio. Si los dos detectan lo mismo, o ninguno detecta nada, este caso no muestra valor agregado, y eso se reportará.

**La pregunta para los revisores:** ¿una comprobación de que los recibos corresponden a los artefactos que nombran añade una garantía de trazabilidad útil a un flujo de verificación reproducible?
