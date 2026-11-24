> Traducción al español de [RESULTS2.md](RESULTS2.md). Si hay alguna diferencia, vale el original.

# Resultados, caso 2: un log sustituido, y el límite de P6

Corrido el 2026-10-22 después del [registro previo](DESIGN2.md) (`a719676`), sobre una copia nueva del árbol de la compilación B4, con Lean 4.34.0-rc2 (`6a10ac8`) y Lake 5.0.0 ([`toolchain.txt`](results2/toolchain.txt)); el clon fijado usado fue `a719676`. **Los nueve resultados salieron según lo registrado.**

| Variante | Qué cambió | Procedimiento publicado por OpenAI (Z) | P6, existencia (X1) | Comprobación por hash (X2) |
| --- | --- | --- | --- | --- |
| C | nada | exit 0, `Your solution is okay!` | pass | pass |
| F5 | el recibo nombra `comparator-run.log` | exit 0, igual | marca: log faltante | marca: log faltante |
| **F7** | `comparator.log` se reemplaza por el log auténtico de Comparator de otra corrida (compilación B5); el recibo no cambia | exit 0, igual | **pass: no lo detecta** | **marca: `H:log-hash-mismatch-comparator.log`** |

La salida de Z para F5 y F7 es idéntica byte a byte, e idéntica a la de F5 en el caso 1. La salida de C difiere solo en 13 líneas `Built …`, porque la primera llamada a Comparator en una copia nueva también compiló el ejecutable de Comparator. El comando de cada paso, el hash del log y el código de salida están en [`results2/receipts.jsonl`](results2/receipts.jsonl); los paquetes y sus diferencias con C están en [`results2/`](results2/).

## La afirmación

> **En este experimento, un log viejo con el nombre correcto pasó el procedimiento publicado por OpenAI y la comprobación de existencia P6 de este estudio, y solo se marcó al compararlo con el hash registrado cuando corrió el paso.** Igual que el caso 1, esto es una inconsistencia de trazabilidad que no cambia el resultado de Comparator, no una prueba falsa aceptada.

Muestra el valor de atar los recibos a hashes de artefactos, y un límite de P6, que solo comprueba que el log nombrado exista. **Límite de la comprobación por hash:** detecta un cambio respecto de un valor de referencia confiable, aquí el hash registrado cuando corrió el paso; no autentica de dónde vino un log si alguien puede sustituir tanto el archivo como ese valor registrado. Un solo caso.

## Trabajos previos

**No es una técnica nueva.** Atar el comando, las entradas y las salidas de cada paso a hashes registrados es práctica establecida en la seguridad de la cadena de suministro de software: [in-toto](https://in-toto.io/) registra, en cada paso, el comando, los hashes de sus archivos de entrada y salida, su valor de retorno y su salida estándar y de error, los firma y los verifica contra un esquema, y la [procedencia SLSA](https://slsa.dev/provenance/v1) registra cómo se hizo una compilación y a partir de qué dependencias con hash. Las dos fallas probadas aquí son del tipo que in-toto ya detecta. Esto es, por tanto, un **estudio de caso de controles de integridad para evidencia de Lean**; no se ha hecho una comparación justa con in-toto o SLSA, y cualquier aporte en integración, diagnósticos específicos de Lean o facilidad de uso todavía tendría que demostrarse.

## Notas

- Antes del commit de registro, `check_hash.py` se probó sobre los paquetes C y F5 del caso 1 para ver que corriera; F7 no se probó antes de la corrida.
- Igual que en el caso 1, el proyecto se compiló una vez (la copia de B4 ya estaba compilada); solo Comparator se corrió una vez por variante.
- `python3 -m unittest test_results` recalcula X1 y X2 sobre los paquetes publicados y comprueba las identidades byte a byte de arriba.
