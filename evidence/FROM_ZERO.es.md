> Traducción al español de [FROM_ZERO.md](FROM_ZERO.md). Si hay alguna diferencia, vale el original.

# Validación desde un clon nuevo, 2026-10-21

Todo lo de abajo partió de `git clone https://github.com/criguex/scientific-qa-evidence.git` en el commit `a92acbc`, sin nada heredado de la copia de trabajo.

## En un Mac, sin Lean

| Comprobación | Resultado |
| --- | --- |
| `shasum -a 256 -c evidence/SHA256SUMS.txt` | PASS, 561 archivos |
| `python3 evidence/verify_numerical.py` | PASS |
| Repetir las 84 variantes numéricas (`test_runner`) | PASS |
| `python3 evidence/test_consistency.py` | PASS |
| Tests del paquete de animaciones, 13 escenas | PASS |
| Saneador de logs de Comparator, procedencia del enunciado, fallos a ciegas v1, v2 y fuzzer | PASS |
| Controles con Mathlib: `verify.py` y `test_verify` | PASS |
| `python3 animations/build.py` regenera cada escena idéntica byte a byte | PASS |

## En el equipo Linux, con Lean

| Comprobación | Resultado |
| --- | --- |
| `ClayLiteral.lean` y `Bridges.lean` compilados desde el clon en un directorio vacío (sin reutilizar ningún `.olean`) | exit 0, 0 warnings, sin `sorry`; SHA-256 igual al de [`bridges/README.md`](../bridges/README.md) |
| `#print axioms` para `k1_C`, `k1_D`, `k1_C_oneSided`, `k1_D_oneSided`, `zero_solution_C`, `zero_solution_D` | `[propext, Classical.choice, Quot.sound]` en cada uno |
| Los 21 pasos de los controles con Mathlib (11 corridas de Comparator, la compilación de la guarda, 9 segundas vías) repetidos desde los archivos del clon | mismos códigos de salida y mismos hashes de entrada que los recibos publicados; recibos en [`rerun-from-clone.receipts.jsonl`](../experiments/mathlib-controls/results/rerun-from-clone.receipts.jsonl). Cada salida registrada es idéntica a un log publicado, salvo el stdout de la compilación de la guarda, al que le falta la línea de progreso de Lake `✔ [2/2] Built QAControls.Guard (2.0s)` y que por lo demás es igual; está publicado en [`rerun-from-clone/Guard.stdout.log`](../experiments/mathlib-controls/results/rerun-from-clone/Guard.stdout.log) |

## No se repitió aquí

- La compilación misma de OpenAI y Mathlib. Estas comprobaciones usaron la compilación B4, compilada desde la fuente con `lake --no-cache build` antes ese mismo día (1 h 29 min, [registro](formal/cd-validation/README.md#builds-used-by-each-run)), y los binarios de los verificadores registrados en [`receipts/`](formal/cd-validation/receipts/).
- La corrida de una persona independiente. Esto lo hizo el autor con el asistente en las mismas dos máquinas; una recompilación externa es la comprobación más fuerte. La [guía de reproducción independiente](../docs/INDEPENDENT_REPRODUCTION.md) da los pasos y una plantilla de reporte.
