# Ampliación V2: escenarios verificables y brechas abiertas

La V2 amplía la evidencia; no reemplaza ni altera la release privada `v2026.10.20-5070`. Este documento distingue lo ya observado de lo preparado para ejecutar. Actualización: 20 de octubre de 2026. La campaña 1D terminó en ambos hosts: [resultados y explicación visual](INFORME_ESCENARIOS_V2.md).

## Qué se contrasta

| Nivel | Evidencia disponible | Lo que no acredita |
|---|---|---|
| Formal | Build Lean y axiomas de cuatro teoremas, conservados en [el resumen derivado](evidence/derived_verification_summary.json). | Por sí solos no revisan la intención matemática ni sustituyen un segundo kernel. |
| Semántico | Auditoría del enunciado y revisión del mutante de fuerza cero. | Un helper que deja de elaborar no demuestra que el testigo final necesite fuerza. |
| Numérico | Taylor–Green, pruebas analíticas y diferencia entre 32³ y 64³ en [el informe de simulación](INFORME_SIMULACION_5070.md). | No demuestra explosión; Euler 32³ tiene sensibilidad espacial importante. |
| Calibración V2 | 42 ejecuciones reales en WAR y GUERRA: seis referencias correctas, 26 rechazos, cuatro sobrevivientes y seis equivalentes. | Son réplicas de tres casos con el mismo código; no transfieren precisión ni veracidad a otra ecuación o teoría. |

## Campaña ejecutada en dos máquinas

Se ejecutó la misma fuente en WAR y GUERRA, con resultados separados por host. El cálculo de estos casos utiliza CPU y un hilo solicitado; tener RTX 5070 o RTX 4060 no convierte esta ejecución en un cálculo GPU.

Cada caso tiene una solución analítica independiente del operador discretizado. La referencia recorre tres mallas y compara dos pasos temporales. Después se ejecutan seis mutantes reales: signo, coeficiente, RHS anulado, borde incorrecto, identidad periódica algebraicamente equivalente y perturbación pequeña del coeficiente. Las tolerancias y ecuaciones están fijadas en [el contrato 1D](skills/escenarios-verificables/references/contratos-1d.md).

| Elemento | Por máquina | Estado de preparación |
|---|---:|---|
| Referencias de calor, advección y onda | 3 | `BASELINE_PASS` en ambos hosts. |
| Mutantes, seis por caso | 18 | Por host: 13 `KILLED`, dos `SURVIVED`, tres `EQUIVALENT`. |
| Autopruebas de clasificación y fingerprint | 12 | Pasaron localmente; no son pruebas de las ecuaciones. |
| Validación de estructura de skill | 1 | `quick_validate.py` pasó. |
| Forward-test no PDE | 1 revisión | Aplicación razonada a una cola FIFO; no se ejecutó un simulador de colas. |

La revisión FIFO usó una tabla independiente de llegadas, servicios, esperas y salidas. Mostró que el protocolo permite un adaptador no PDE sin imponer refinamiento de malla donde no corresponde. Es una revisión del alcance del texto, no evidencia experimental de otro motor.

El [resumen reproducible](evidence/scenarios_v2/campaign_summary.json) verifica 294 hashes de artefactos y conserva los 42 hashes de los JSON de ejecución. Las 21 clasificaciones coinciden entre máquinas. Python fue 3.10.11 en WAR y 3.12.3 en GUERRA; cada mutante usó la referencia de su propio entorno.

### Reproducción mínima

Mantener juntos `scripts/` y `references/` dentro de la skill. Ejecutar en un entorno con NumPy y Matplotlib, sin modificar la fuente ni el contrato entre referencia y mutantes:

```sh
python skills/escenarios-verificables/scripts/run_scenario.py --self-check
python skills/escenarios-verificables/scripts/run_scenario.py --case heat --mutant baseline --output resultados/war/heat_baseline
python skills/escenarios-verificables/scripts/run_scenario.py --case heat --mutant sign --baseline resultados/war/heat_baseline/run.json --output resultados/war/heat_sign
```

Repetir con `advection` y `wave`, los demás identificadores del contrato y carpetas nuevas. En GUERRA usar una referencia producida en GUERRA, no el JSON de WAR. El runner rechaza una carpeta no vacía.

Cada `run.json` enlaza comando, versiones, intérprete, host, parámetros, UTC, tiempo monotónico, estado, causas y hashes. Los campos, CSV, imagen y logs quedan junto al resumen. El fingerprint y los hashes del baseline se comprueban antes de conceder crédito de detección; no constituyen una atestación de seguridad del sistema operativo.

### Leer los resultados

`KILLED` significa violación del contrato atribuible a una modificación ejecutada y acompañada de referencia válida. `SURVIVED` significa que el contrato no la detectó. `EQUIVALENT` exige una justificación algebraica; pasar las pruebas no basta. `INFRA_FAIL` e `INCONCLUSIVE` no cuentan como detecciones. La referencia tiene el estado separado `BASELINE_PASS`.

No se exige una tasa del 100 %. El mutante pequeño puede sobrevivir o ser detectado por un invariante más sensible; ambas observaciones son útiles. Cualquier tasa debe mostrar los denominadores y excluir equivalentes, infraestructura y ejecuciones inconcluyentes del conjunto de mutantes no equivalentes evaluables.

## Qué falta en la auditoría formal

### NS-08: comparador y segundo kernel

No ejecutados en la evidencia original. La propuesta reproducible está en [NS08_PROPUESTA_NO_EJECUTADA.md](NS08_PROPUESTA_NO_EJECUTADA.md). Debe conservar logs, códigos de salida y recursos, sin desactivar nanoda ni ampliar axiomas permitidos para lograr un resultado favorable. Una comprobación sobre el checkout ya usado no equivale a preparar desde cero un entorno de confianza adversarial.

### EU-06: control positivo no trivial

Sigue pendiente construir y comprobar un ejemplo global de Euler no nulo dentro de la clase exacta del enunciado auditado. No sustituirlo por `1 + 1 = 2`, una solución con otra condición de borde o una simulación periódica. Antes de implementarlo se necesita especificar el candidato y demostrar que cumple cada hipótesis pertinente. Aquí no se afirma que ese ejemplo ya exista en el repositorio ni que el control se haya ejecutado.

### NS-09: mejorar la prueba semántica de fuerza cero

El mutante realizado añadió un campo a una estructura y rompió la elaboración de un helper genérico y una obligación `toComparator`. El fallo ocurrió antes de una comprobación directa del testigo final. Por tanto, acredita incompatibilidad de la prueba tal como estaba escrita con la estructura modificada, no necesidad matemática de fuerza ni imposibilidad de reparar la prueba.

Hay además una diferencia de dominio temporal: exigir `f = 0` como igualdad de funciones sobre todo tiempo real es más fuerte que exigir fuerza cero solo para `t ≥ 0`. Un siguiente experimento debe expresar exactamente la condición que se quiere auditar, conservar los demás supuestos y separar adaptación mecánica del helper de la obligación sustantiva sobre el testigo. Hasta hacerlo no se atribuye un resultado a ese experimento.

## Contrastes numéricos 3D: uno realizado y siguientes pendientes

La comparación 32³/64³ ya detectó una limitación espacial importante en Euler. Para investigar su magnitud hacen falta experimentos dirigidos, no únicamente más invariantes:

1. **Realizado en GUERRA:** repetir Taylor–Green con `dt = 0,01` y `0,005`, conservando `N = 32`, dato y `T = 4`. Ambas corridas pasaron sus controles. La diferencia relativa final de velocidad fue `1,1509 × 10⁻⁹` en Euler y `7,5994 × 10⁻¹²` en NS. Es sensibilidad temporal a malla fija; no establece orden observado con solo dos pasos ni resuelve la discrepancia espacial. [Comparación registrada](evidence/fluid_temporal_v2/temporal-comparison.json).
2. Añadir una tercera malla en un horizonte acotado si los recursos lo permiten. Fijar antes el coste máximo y el criterio de comparación. Dos o tres mallas sin régimen asintótico claro no proporcionan una cota rigurosa de error.
3. Comparar campos tanto sin filtrar como tras aplicar el mismo filtro definido de antemano. Registrar corte, normalización y norma; mostrar ambos resultados. El filtro puede distinguir desacuerdos en escalas gruesas y finas, pero no debe elegirse después para ocultar una discrepancia.
4. Contrastar con un segundo esquema implementado de forma independiente. Ejecutar el mismo código en dos PC comprueba reproducibilidad de esa implementación; no proporciona independencia algorítmica.
5. Registrar el máximo de vorticidad muestreado y una integral temporal discreta tipo BKM, indicando discretización y resolución. Un valor grande o creciente durante un intervalo finito no demuestra divergencia de la integral continua ni explosión en tiempo finito.

Salvo la comparación con `dt/2`, los pasos restantes siguen propuestos y no ejecutados en esta V2. No son necesarios para interpretar la calibración 1D ni convierten el caso periódico Taylor–Green en el dato compacto sobre `R³` del teorema auditado.

## Criterio de entrega V2

Publicar las fuentes y los resultados reales de ambas máquinas, con discrepancias y sobrevivientes visibles. Conservar la versión audiovisual anterior; cualquier nueva voz necesita duración medida y QA propio. El [montaje analítico V2 de 30 segundos](simulation/analytic_render/TRES_ESCENARIOS_ANALITICOS_5070.mp4) está disponible y pasó el [QA registrado](simulation/analytic_render/qa_summary.json). Va sin audio; no hay una voz nueva aprobada.

La [lámina didáctica GPT](evidence/images_gpt/no_todo_es_agua_v1.png) y su [prompt](evidence/images_gpt/no_todo_es_agua_v1.json) se entregan como ilustración identificada, no como fotograma calculado. La [muestra de voz](evidence/voice_preview_v2/audio/voz.mp3) espera aprobación del usuario. El [informe V2](INFORME_ESCENARIOS_V2.md) reúne esos materiales y la explicación de los clips analíticos, manteniendo separados ilustración, cálculo y narración.
