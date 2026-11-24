> Traducción al español de [DESIGN.md](DESIGN.md). Si hay alguna diferencia, vale el original.

# Experimento de fallos a ciegas: diseño (BORRADOR, sin congelar)

**Pregunta.** En casos pequeños y controlados, ¿qué fallos sembrados detecta el protocolo de este estudio que el procedimiento base no detecta, y a qué costo en falsas alarmas y tiempo?

**Estado.** Borrador para revisión del autor. Se vuelve vinculante cuando su SHA-256 se publica en `FROZEN.md`. Después de eso, cualquier cambio es un experimento nuevo.

## 1. Los dos procedimientos

**Línea base (B).** El procedimiento documentado en el repositorio de OpenAI: compilar el proyecto de Lean con `lake build`, correr Comparator con su configuración JSON, y aceptar si imprime `Your solution is okay!`. Para los casos numéricos: correr la suite de pruebas del caso y aceptar si reporta éxito.

**Protocolo (P).** La línea base, más las comprobaciones propias del protocolo:

| Comprobación | Qué hace |
| --- | --- |
| P1 · comprobación de artefactos | Compara las marcas de tiempo de los `.olean` con el inicio de la compilación y busca archivos descargados |
| P2 · procedencia del enunciado | Compara el archivo del desafío con una referencia pública fijada, usando `compare_statements.py` |
| P3 · mutantes del enunciado | Mutantes de un símbolo del desafío más un control de solo comentario; Comparator debe rechazar los mutantes y aceptar el control |
| P4 · vigencia del kernel | Compara el árbol `src/kernel` del toolchain y el commit de nanoda con las correcciones de solidez conocidas |
| P5 · inyección de fallos en el harness | Fuerza fallos del oráculo y del simulador y comprueba que el harness los reporte |
| P6 · recibos | Comprueba que cada corrida reportada tenga un comando, código de salida y hash original que coincidan con sus artefactos |

## 2. Casos

Cada caso es una copia pequeña y rápida: un proyecto Lean núcleo sin Mathlib (un enunciado de desafío, una prueba y una configuración de Comparator), o un modelo numérico de la suite de este repositorio. Todos los casos usan las mismas plantillas, así que un fallo es la única diferencia.

| Clase | Fallo sembrado | Instancias | Por qué B podría pasarlo |
| --- | --- | ---: | --- |
| F1 | Archivos `.olean` precompilados de una dependencia, colocados en el directorio de compilación en vez de compilarla | 3 | La compilación tiene éxito y Comparator acepta |
| F2 | El enunciado del desafío se debilita y la prueba demuestra el enunciado más débil; el enunciado de referencia del caso no cambia | 3 | Comparator compara la prueba con el desafío, y coinciden |
| F4 | El oráculo numérico lanza una excepción, y el harness reporta el caso como aprobado | 3 | La suite reporta éxito |
| F5 | Un recibo de corrida nombra una compilación o un log distinto del que realmente se usó | 3 | B no guarda recibos |
| F6 | Control positivo: la prueba usa `sorry` o un axioma no permitido | 3 | No debería; Comparator rechaza esto, así que los dos procedimientos deberían detectarlo |
| C | Copias limpias sin fallo | 6 | Mide las falsas alarmas |

**Total:** 21 casos, nombrados `case-01` a `case-21`. La clase F3 se retiró antes de congelar; ver [F3_WITHDRAWN.md](F3_WITHDRAWN.md).

F6 comprueba que la línea base funciona como se pretende; si B no detecta F6, el montaje está roto. F5 no puede ser detectado por B por construcción, y se reporta aparte para que no infle la comparación.

## 3. Asignación y cegamiento

1. La semilla comprometida en [SEED_COMMITMENT.md](SEED_COMMITMENT.md) es la única fuente de aleatoriedad.
2. `assign.py` (por escribir y congelar junto con este diseño) construye la lista de los 21 cupos de arriba, la mezcla con `random.Random(seed)` de Python, siembra cada fallo en su copia, y escribe `key.json`, que mapea cada caso a su clase.
3. El autor corre `assign.py` en su máquina y mantiene `key.json` y la semilla fuera del alcance del asistente hasta que todos los resultados queden registrados.
4. Las comprobaciones se corren solo con los nombres de los casos. Cada resultado se comitea antes de abrir la clave.

## 4. Resultados y métricas

- **Marcado:** un procedimiento reporta un problema para un caso, registrado junto con la comprobación que lo levantó.
- **Tasa de detección:** casos con fallo marcados ÷ casos con fallo, por clase y por procedimiento.
- **Tasa de falsas alarmas:** casos limpios marcados ÷ casos limpios, por procedimiento.
- **Costo:** tiempo de reloj por caso y procedimiento.
- Los resultados se reportan como conteos (por ejemplo «B 0/3, P 3/3»). Con 3 instancias por clase no hay pruebas de significancia; el experimento muestra si existe una diferencia en estos casos, no qué tan grande es en general.

## 5. Reglas de decisión, fijadas de antemano

- Un caso cuenta como detectado por un procedimiento solo si ese procedimiento lo marca durante la fase ciega.
- Ningún caso se elimina después de revelar la clave. Un caso que no se pueda correr cuenta como no detectado, con la razón registrada.
- Si F6 no es detectado por los dos procedimientos, el experimento se reporta como inválido, no parcialmente.

## 6. Qué puede y no puede respaldar

**Puede respaldar:** «En estos 21 casos sembrados, el protocolo detectó las clases F1, F2, F4 y F5 que la línea base no detectó, con N falsas alarmas sobre 6 casos limpios, a un costo de T».

**No puede respaldar:** tasas de detección para fallos del mundo real, comportamiento en proyectos grandes, ni superioridad sobre procedimientos distintos de esta línea base.

## Decisiones tomadas (2026-10-21)

1. Tres instancias por clase, 21 casos en total.
2. F3 se incluyó primero, y luego se **retiró antes de congelar** después de que un filtro de seguridad automatizado detuviera el trabajo del asistente en ella; ver [F3_WITHDRAWN.md](F3_WITHDRAWN.md).
3. F5 se mantiene y se reporta aparte, porque la línea base no puede detectarla por construcción.

## Comprobaciones de factibilidad antes de congelar

| Elemento | Estado |
| --- | --- |
| `assign.py`, las plantillas de casos y los scripts de comprobación | Pendiente |

## Implementación y su alcance

El experimento está implementado en Python para que sea totalmente reproducible en el CI, sin necesitar Lean ni un equipo remoto:

- `protocol_lib.py` — la plantilla del caso limpio, los inyectores de fallo de un solo artefacto, y los dos procedimientos `baseline` y `protocol` como funciones sobre los artefactos de un caso.
- `assign.py` — lee la semilla comprometida y escribe `case-01..21` más `key.json`.
- `run_checks.py` — corre los dos procedimientos sobre cada caso, ciego a `key.json`.
- `score.py` — une los resultados con la clave revelada para obtener las métricas.
- `test_protocol.py` — verifica el patrón esperado (lo limpio pasa los dos; F6 lo atrapan los dos; F1, F2, F4, F5 pasan la línea base pero el protocolo los marca).

**Qué modela esto y qué no.** Un caso es un directorio de artefactos registrados del tipo que lee el protocolo real: un log de compilación, una tabla de marcas de tiempo de artefactos, un enunciado de la prueba y su referencia, un reporte de axiomas, recibos, y un resumen numérico. Las comprobaciones corren sobre estos artefactos exactamente como las comprobaciones reales corren sobre los logs, la fuente y los recibos reales. El experimento **no** vuelve a correr Lean, Comparator ni los kernels; esas corridas en vivo son el estudio principal bajo `evidence/formal/`. Así que el experimento muestra las comprobaciones del protocolo sobre artefactos controlados, no una segunda verificación en vivo.

**Determinismo.** El resultado por clase no depende de la semilla: las comprobaciones son deterministas, así que un fallo de una clase dada se detecta de la misma manera sin importar en qué número de caso caiga. La semilla solo fija la asignación, y su compromiso más los hashes de los scripts congelados evitan que las comprobaciones se ajusten a ella.
