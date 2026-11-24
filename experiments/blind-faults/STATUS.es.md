> Traducción al español de [STATUS.md](STATUS.md). Si hay alguna diferencia, vale el original.

# Experimento de fallos a ciegas: estado

| Paso | Estado | Registro |
| --- | --- | --- |
| Semilla generada por el autor, hash publicado | Hecho, 2026-10-21 15:21 (UTC−5) | [SEED_COMMITMENT.md](SEED_COMMITMENT.md) |
| Diseño redactado, decisiones tomadas | Hecho, borrador sin congelar | [DESIGN.md](DESIGN.md) |
| Clase F3 (exploit del kernel) | Retirada antes de congelar, después de que un filtro de seguridad detuviera el trabajo en ella | [F3_WITHDRAWN.md](F3_WITHDRAWN.md) |
| Factibilidad de F3 registrada antes del retiro | Solo histórico | [feasibility/f3-exploit-reproduction.md](feasibility/f3-exploit-reproduction.md) |
| `assign.py`, las plantillas de casos y los scripts de comprobación escritos | Hecho | [protocol_lib.py](protocol_lib.py), [assign.py](assign.py), [run_checks.py](run_checks.py), [score.py](score.py) |
| Autocomprobación y ensayo de extremo a extremo (semilla de prueba) | Hecho: F6 lo atraparon los dos, F1/F2/F4/F5 solo el protocolo, 0 falsas alarmas | [test_protocol.py](test_protocol.py) |
| Diseño y scripts congelados (hash en `FROZEN.md`) | Hecho el 2026-10-21 | [FROZEN.md](FROZEN.md) |
| El autor corre la asignación con la semilla | Hecho el 2026-10-21; el hash de la semilla coincidió con el compromiso | commit `ae55a24` (21 carpetas de casos, clave retenida) |
| Comprobaciones a ciegas sobre 21 casos, resultados comiteados antes de la clave | Hecho: la línea base marcó 3 de 21, el protocolo 15 de 21; los scripts coincidieron con los hashes de FROZEN.md | [results.json](results.json) |
| Clave revelada, resultados calificados y publicados | Hecho (v1); corregido después con erratas | [RESULTS.md](RESULTS.md) |
| Revisión externa: replantear como benchmark de regresión, corregir la etiqueta de F2, el costo, los defectos del evaluador | Hecho: v1 se conserva con erratas; evaluador v2 con pruebas de evidencia ausente/incompleta y benchmark | [v2/README.md](v2/README.md) |
| Semilla revelada; asignación reproducida | Hecho: el hash coincidió; `key.json` y los 21 casos se regeneraron byte por byte | [semilla-experimento.txt](semilla-experimento.txt), [RESULTS.md](RESULTS.md#reproduce-the-assignment) |

La fase a ciegas está completa; ver [RESULTS.md](RESULTS.md).

