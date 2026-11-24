> Traducción al español de [DESIGN2.md](DESIGN2.md). Si hay alguna diferencia, vale el original.

# Caso 2: un log sustituido, y el límite de P6

**Registrado antes de correrlo el 2026-10-22, antes de cualquier corrida.** **Resultados: [RESULTS2.md](RESULTS2.md)** — los nueve resultados salieron según lo registrado. Resultados esperados: [`expected2.json`](expected2.json); scripts: [`run2.sh`](run2.sh), [`check_hash.py`](check_hash.py), [`check_p6.py`](check_p6.py).

## Por qué un segundo caso

El caso 1 ([resultados](RESULTS.md)) mostró a P6 atrapando un recibo que nombra un log faltante. Pero P6 solo comprueba que el log nombrado **exista**. Una falla realista es un log que existe con el nombre correcto pero viene de otra corrida: un log viejo o cambiado. P6 no lo atraparía. Este caso prueba abiertamente ese límite, y si una comprobación contra el hash registrado cuando se escribió el paquete sí lo atrapa.

## Variantes, sobre el mismo paquete y una copia nueva del árbol de la compilación B4

| Variante | Cambio | Z esperado | X1 esperado (P6) | X2 esperado (hash) |
| --- | --- | --- | --- | --- |
| C | ninguno | exit 0 | pass | pass |
| F5 | el recibo nombra `comparator-run.log` (como en el caso 1) | exit 0 | marca: log faltante | marca: log faltante |
| **F7** | `comparator.log` se reemplaza por el log auténtico de Comparator de otra corrida del mismo paso (compilación B5, también aceptada); el recibo no cambia | exit 0 | **pass: P6 no lo detecta** | **marca: discrepancia de hash** |

El paquete es el paquete limpio del caso 1, cuyos hashes de logs de paso se registraron en el momento en que corrió cada paso (`results/receipts.jsonl`, variante `bundle`). X2 compara contra esos hashes registrados.

## La afirmación que esto puede respaldar

> En este caso, un log viejo con el nombre correcto pasó el procedimiento publicado por OpenAI y la comprobación de existencia P6 de este estudio, y solo se atrapó al compararlo con el hash registrado cuando corrió el paso.

Eso muestra tanto el valor de los recibos atados a hashes como un límite de P6. Se trata de la trazabilidad de la evidencia, no de la prueba. Si X2 no detecta F7, o marca a C, eso se reportará.
