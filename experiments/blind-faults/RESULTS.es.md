> Traducción al español de [RESULTS.md](RESULTS.md). Si hay alguna diferencia, vale el original.

# Experimento de fallos a ciegas: resultados (v1)

> **Erratas y replanteamiento, después de una revisión externa el 2026-10-21.** Los archivos v1 de abajo se conservan sin cambios para que la corrida publicada siga siendo reproducible. Correcciones:
>
> 1. **Lee esto como un benchmark de regresión determinista, no como prueba de cegamiento.** El orden de los commits muestra que los resultados se registraron antes de comitear la clave, pero no es evidencia absoluta de cegamiento: el asistente tenía acceso de sistema de archivos a la máquina que tenía la clave, y él mismo comiteó los casos y la clave, y el evaluador es determinista, así que el resultado por clase no dependía de la asignación.
> 2. **F2 está mal etiquetada.** Su edición cambia la hipótesis `nu > 0` a `nu >= 0`, lo que relaja una hipótesis y por tanto hace el teorema más fuerte, no más débil. F2 demuestra solo que P2 detecta una diferencia textual con la referencia, no la detección de un enunciado debilitado.
> 3. **La métrica de costo planeada no se midió.** DESIGN.md listaba el costo en tiempo de reloj por caso; v1 no registró ninguno. v2 mide el tiempo del evaluador y declara qué no cubre.
> 4. **El evaluador v1 tenía defectos** encontrados después: la evidencia incompleta fallaba abierta, la evidencia ausente colapsaba, y P6 asumía un `comparator.log` que ningún caso contenía. Bajo el evaluador corregido, los seis casos «limpios» de v1 quedan marcados, así que **la afirmación de v1 de 0 falsas alarmas no se sostiene**; dependía de evidencia que el evaluador asumía. Ver [v2/README.md](v2/README.md).
> 5. **La semilla se reveló después** ([semilla-experimento.txt](semilla-experimento.txt)). Su SHA-256 coincide con el compromiso, y volver a correr `assign.py` con ella reproduce `key.json` y las 21 carpetas de casos byte por byte (ver Reproducir abajo).


**Estado:** completo. Válido bajo su propia regla de decisión congelada (el control positivo F6 fue detectado por los dos procedimientos), pero ver la errata 4: el resultado de casos limpios del evaluador v1 no se sostiene.

## Cronología (todo en el historial de git)

| Paso | Commit | Hora (UTC−5) |
| --- | --- | --- |
| Hash de la semilla publicado por el autor | `598f287` | 2026-10-21 15:21 |
| Diseño y scripts congelados (SHA-256 en [FROZEN.md](FROZEN.md)) | `4609f3e` | 2026-10-21 |
| El autor corrió `assign.py`; el hash de la semilla coincidió con el compromiso | `ae55a24` | 2026-10-21 |
| Resultados a ciegas registrados, antes de la clave ([results.json](results.json)) | `5752808` | 2026-10-21 16:09 |
| Clave revelada ([key.json](key.json)) | `a17467f` | 2026-10-21 16:10 |

Los scripts que produjeron los resultados (`protocol_lib.py`, `run_checks.py`, `score.py`) coincidieron con sus hashes congelados en el momento de correr.

## Resultados

21 casos: 3 por clase de fallo y 6 limpios. [scoreboard.json](scoreboard.json) tiene el detalle por caso.

| Clase | Fallo sembrado | Detectado por la línea base | Detectado por el protocolo | Comprobación del protocolo que se activó |
| --- | --- | ---: | ---: | --- |
| F1 | Una dependencia llegó precompilada; el log de compilación está limpio | 0/3 | **3/3** | P1, comprobación de artefactos |
| F2 | El enunciado de la prueba difiere de la referencia fijada (etiquetado «debilitado» en v1; ver errata 2) | 0/3 | **3/3** | P2, procedencia del enunciado |
| F4 | El oráculo falló, pero el harness reportó una corrida completa | 0/3 | **3/3** | P5, integridad del harness |
| F5 | Un recibo nombra un log que la compilación no escribió | 0/3 | **3/3** | P6, recibos |
| F6 | Control positivo: la prueba depende de `sorry` | 3/3 | 3/3 | Comprobación de axiomas de la línea base |
| C | Sin fallo (incompleto bajo v2; ver errata 4) | 0/6 falsas alarmas | **0/6** falsas alarmas (solo con el evaluador v1) | — |

**Clases detectadas por el protocolo y no por la línea base:** F1, F2, F4, F5.

## Qué respalda esto

En estos 21 casos controlados, el protocolo detectó cuatro clases de fallo que el procedimiento base no detectó. El evaluador v1 no levantó ninguna falsa alarma en los seis casos limpios, un resultado retirado por la errata 4. La línea base funcionó como se pretendía donde aplica: atrapó todos los controles positivos.

En los términos de [FINDINGS.md](../../FINDINGS.md): el protocolo hace visibles los artefactos precompilados ocultos, un enunciado que difiere de su referencia fijada, un harness de pruebas que esconde fallos del oráculo, y registros de corrida que no coinciden con sus artefactos. La línea base documentada no lee los artefactos donde viven estos fallos.

## Qué no respalda esto

- **No es una tasa de detección del mundo real.** Los fallos se siembran, uno por caso, en artefactos controlados.
- **El resultado se desprende del diseño.** Cada fallo vive en un artefacto que la línea base no lee, así que la línea base no puede verlo; F5 es indetectable por la línea base por construcción y se reporta solo por completitud. El experimento confirma que las comprobaciones del protocolo funcionan como se especificó y cubren esos vacíos. No muestra que atraparían fallos de otros tipos.
- **Comprobaciones sobre artefactos registrados, no Lean en vivo.** Aquí no se volvió a correr Lean, Comparator ni ningún kernel; esas corridas en vivo son el estudio principal.
- **Pequeño y determinista.** Tres instancias por clase; la semilla solo fijó qué número de caso recibió cada fallo.
- **F3 se retiró** antes de congelar ([F3_WITHDRAWN.md](F3_WITHDRAWN.md)).

## Reproducir la asignación

La semilla está publicada como [semilla-experimento.txt](semilla-experimento.txt). Desde esta carpeta:

```sh
shasum -a 256 semilla-experimento.txt        # must print 6ab9f825...614d5e, as in SEED_COMMITMENT.md
mkdir /tmp/repro && cp protocol_lib.py assign.py /tmp/repro/
(cd /tmp/repro && python3 assign.py --seed-file "$OLDPWD/semilla-experimento.txt" --out cases)
diff /tmp/repro/key.json key.json && diff -r /tmp/repro/cases cases && echo identical
```

Comprobado el 2026-10-21: el hash coincidió, y el `key.json` y las carpetas de casos regenerados fueron idénticos a los publicados.
