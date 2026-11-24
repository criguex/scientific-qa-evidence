> Traducción al español de [RESULTS.md](RESULTS.md). Si hay alguna diferencia, vale el original.

# Resultados: correspondencia entre recibo y log sobre registros auténticos

Corrido el 2026-10-22, después del [registro previo](DESIGN.md) (`8478f68`) y la [enmienda 1](STATUS.md) (`db1da97`), sobre una copia del árbol de la compilación B4 de `openai/NavierStokesAndEuler` en `f9e8bc5`. Lean 4.34.0-rc2 (`6a10ac8`), Lake 5.0.0; `lake exe comparator` compiló el mismo binario de Comparator usado en la auditoría (SHA-256 `514de8d2…`, como en [`tools.tsv`](../../evidence/formal/cd-validation/receipts/tools.tsv)); landrun, lean4export y nanoda según los hashes en [`versions.txt`](results/versions.txt).

**Las dos variantes salieron exactamente según lo registrado.**

| Variante | Qué cambió | Procedimiento publicado por OpenAI (Z) | Comprobación P6 (X) |
| --- | --- | --- | --- |
| C, control limpio | nada | exit 0, `Your solution is okay!` | exit 0, sin marca |
| F5, falla conocida | una fila del recibo nombra `comparator-run.log` en vez de `comparator.log` | exit 0, `Your solution is okay!`; salida idéntica byte a byte a C | **exit 1**, `P6:receipt-log-missing-comparator-run.log` |

**Qué se repitió.** El proyecto se compiló una vez, cuando se escribió el paquete (los tres pasos de abajo). Para cada variante solo se volvió a correr el paso de Comparator de Z, sobre el mismo árbol con el paquete de esa variante dentro; la compilación no se repitió por variante.

| Paso de Z, registrado en el paquete | Comando | Salida |
| --- | --- | --- |
| cache | `lake exe cache get` | 0 |
| build | `lake build` | 0 |
| comparator | `lake exe comparator ComparatorChallenges/NavierStokes.json` | 0 (los dos kernels aceptan) |

El comando de cada paso, el SHA-256 de su log saneado, su código de salida y sus tiempos están en [`results/receipts.jsonl`](results/receipts.jsonl); los paquetes son [`results/C/`](results/C/) y [`results/F5/`](results/F5/), que difieren solo en esa fila del recibo ([`F5.receipt.diff`](results/F5.receipt.diff)).

## La afirmación

> **En este experimento, P6 detecta una inconsistencia de trazabilidad que no cambia el resultado de Comparator.** Un recibo que nombra un log que no está en el paquete de evidencia fue marcado por P6, mientras que el procedimiento publicado por OpenAI, corrido sobre los mismos archivos, salió con 0 y con salida idéntica byte a byte, porque no lee recibos.

Esto muestra un vacío de trazabilidad en el procedimiento publicado, cerrado por una comprobación del tipo que ya ofrecen herramientas de cadena de suministro como in-toto (ver [RESULTS2](RESULTS2.md#prior-art)); no es una técnica nueva. **No significa que Comparator aceptara una prueba falsa:** la prueba es la misma en las dos variantes y fue aceptada en las dos. No dice que P6 atrape todos los errores, que el procedimiento publicado falle en su propia tarea de revisar la prueba, ni nada sobre el Problema del Milenio. Es un solo caso.

**Pregunta para los revisores:** ¿una comprobación de que los recibos corresponden a los artefactos que nombran añade una garantía de trazabilidad útil a un flujo de verificación reproducible?

## Reproducir

`python3 -m unittest test_results` (corre en el CI) recalcula P6 sobre los paquetes publicados con el `protocol_lib_v2.py` congelado, comprueba que los dos paquetes difieren solo en esa fila del recibo, y que la salida registrada de Z es idéntica para los dos. El propio Z necesita la compilación de Lean y se reproduce con [`run.sh`](run.sh).

## Notas de registro

- Los primeros `lake --version` y `lean --version` del envoltorio corrieron fuera del directorio del proyecto, donde no hay ningún toolchain por defecto configurado, así que fallaron y no aparecen en `versions.txt`. Las versiones se leyeron después, dentro del mismo árbol, y están en [`toolchain.txt`](results/toolchain.txt); el commit de Lean también aparece en el log de la compilación.
- `lake exe cache get` tomó 18 s y `lake build` 36 s porque el árbol ya estaba compilado; la copia de B4 se hizo con `cp -a`.
