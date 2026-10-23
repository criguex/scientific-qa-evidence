# Tres fenómenos distintos: calor, transporte y ondas

La campaña real terminó en WAR y GUERRA: **42 ejecuciones, seis referencias correctas y 36 ejecuciones de mutantes**. En cada máquina hubo 13 mutantes detectados, dos sobrevivientes y tres algebraicamente equivalentes. Se verificaron 294 hashes de archivos; no se descartaron los sobrevivientes. [Resumen de campaña](evidence/scenarios_v2/campaign_summary.json).

Esto calibra tres implementaciones pequeñas con oráculos analíticos. No verifica por extensión los teoremas de Euler o Navier–Stokes.

## Ver los tres ejemplos

[Abrir el montaje de 30 segundos, sin audio](simulation/analytic_render/TRES_ESCENARIOS_ANALITICOS_5070.mp4).

![Tres ejemplos analíticos: calor, transporte y onda. Modelo 1D periódico representado en relieve 3D.](simulation/analytic_render/PORTADA_TRES_ESCENARIOS.png)

Clips individuales: [calor](simulation/analytic_render/01_CALOR.mp4), [transporte](simulation/analytic_render/02_TRANSPORTE.mp4) y [onda](simulation/analytic_render/03_ONDA.mp4). Se renderizaron en WAR y el montaje se abrió y reprodujo en QuickTime en el Mac. La entrega está disponible localmente; este texto no presume que una release V2 ya se haya publicado.

## Una imagen para orientarse, no para medir

![Ilustración didáctica generada con IA: calor, transporte y ondas. No es un resultado de simulación.](evidence/images_gpt/no_todo_es_agua_v1.png)

Esta lámina fue generada con GPT para explicar conceptos. No contiene campos calculados ni constituye evidencia experimental. Su [prompt y procedencia](evidence/images_gpt/no_todo_es_agua_v1.json) se conservan separados de los datos científicos.

## Cómo leer las animaciones analíticas

Los nuevos clips representan el dominio periódico como un anillo. La coordenada que recorre el círculo es `x`; el relieve tiene altura `0,75(u − media)`. El ancho de la banda es decorativo, no otra variable espacial. La curva de la derecha muestra los mismos valores desplegados entre `0` y `2π`.

Cada fotograma evalúa una fórmula analítica cerrada. **No es una nueva integración temporal ni una simulación de agua o de una ecuación 3D.** La cámara, la escala vertical y la escala de colores permanecen fijas. El tiempo del modelo es adimensional y no equivale a la duración del video.

La solución es exacta como fórmula del modelo; su evaluación usa números de punto flotante y 257 muestras para cerrar visualmente el anillo. No es aritmética certificada ni una malla nueva del solver. El extremo duplicado se utiliza solo para unir la representación gráfica.

| Clip | Qué muestra | Horizonte visual |
|---|---|---|
| Calor | Disminuye el contraste térmico y el perfil se acerca a su media. No todos los puntos evolucionan monótonamente. | `T = 12`, con `κ = 0,13`. |
| Transporte | El perfil se mueve sin cambiar de forma y completa una vuelta. | `T = 2π/1,3 ≈ 4,83`. |
| Onda | El desplazamiento oscila con velocidad inicial no nula; se muestra un periodo completo. No se afirma que sea una onda estacionaria pura. | `T = 2π/0,8 ≈ 7,85`. |

El control numérico registrado se hizo **solo hasta `T = 0,7`**. Mostrar la solución analítica a un tiempo mayor no extiende el horizonte validado del solver. Los valores de validación al final de cada clip se leen de los resultados reales de WAR, no se escriben a mano.

El avance se entrega sin audio, con tres clips de 10 segundos y montaje de 30 segundos: ocho segundos de evolución visual y dos de pausa final por caso. No acredita una voz nueva aprobada. El [resumen original del render](simulation/analytic_render/render_summary.json) conserva parámetros, fuentes, comandos y hashes.

### QA del video

La decodificación completa en WAR terminó con salida cero y sin errores. El archivo contiene 360 fotogramas H.264, 1280 × 720, 12 fps, 30 segundos y ningún stream de audio. Pasaron las 11 comprobaciones de fórmulas y la verificación de los 379 hashes originales del render. Se revisaron vistas de los tres casos, el final de calor y un fotograma intermedio de onda; no se afirma que una persona haya inspeccionado cada fotograma. [QA resumido](simulation/analytic_render/qa_summary.json), [comandos y salidas crudas](simulation/analytic_render/qa_decode_probe.json).

SHA256 del montaje: `48f6a4da8a48a6a8e827b3b22f06ef0d0eaa9f196fe830e38d0e8e33b4a48029`.

## Resultados analíticos y refinamiento

Cada referencia utilizó diferencias centradas y RK4 en `N = 32, 64, 128`, más una repetición `N = 64` con `dt/2`. El oráculo se evalúa con fórmulas exactas independientes del operador discretizado. Para onda, el error RMS incluye conjuntamente `u` y `v`.

| Caso | Error RMS en N128 | Orden observado 64→128 | Diferencia RMS al dividir dt por dos, N64 |
|---|---:|---:|---:|
| [Calor en WAR](evidence/scenarios_v2/war/heat_baseline/run.json) | 2,93253 × 10⁻⁵ | 1,99926 | 9,16432 × 10⁻¹³ |
| [Transporte en WAR](evidence/scenarios_v2/war/advection_baseline/run.json) | 5,77593 × 10⁻⁴ | 1,99822 | 5,51746 × 10⁻⁹ |
| [Onda en WAR](evidence/scenarios_v2/war/wave_baseline/run.json) | 1,29854 × 10⁻⁴ | 1,99951 | 2,80664 × 10⁻⁹ |

Las referencias de [calor](evidence/scenarios_v2/guerra/heat_baseline/run.json), [transporte](evidence/scenarios_v2/guerra/advection_baseline/run.json) y [onda](evidence/scenarios_v2/guerra/wave_baseline/run.json) en GUERRA también pasaron y registraron los mismos errores RMS finales N128. Los detalles completos, incluidos medias e invariantes, están en cada JSON y su CSV contiguo. La concordancia entre máquinas comprueba reproducibilidad de este código, no independencia algorítmica.

Los umbrales se fijaron antes de observar mutantes: error final menor que `10⁻³`, orden entre `1,7` y `2,3`, consistencia temporal y límites de deriva de medias e invariantes. No se interpreta la pequeña diferencia temporal como una medición del orden cuatro de RK4 cuando domina el error espacial. [Contrato completo](skills/escenarios-verificables/references/contratos-1d.md).

## Mutantes: también importan los que sobreviven

La tabla es igual en ambos hosts:

| Cambio del operador | Calor | Transporte | Onda |
|---|---|---|---|
| Invertir signo | `KILLED` | `KILLED` | `KILLED` |
| Coeficiente × 1,25 | `KILLED` | `KILLED` | `KILLED` |
| RHS anulado | `KILLED` | `KILLED` | `KILLED` |
| Borde cero en vez de periódico | `KILLED` | `KILLED` | `KILLED` |
| Desplazamiento de exactamente N posiciones | `EQUIVALENT` | `EQUIVALENT` | `EQUIVALENT` |
| Coeficiente × 1,000001 | `SURVIVED` | `SURVIVED` | `KILLED` |

El desplazamiento de N posiciones es la identidad algebraica de un arreglo periódico. No se declaró equivalente porque simplemente pasara las pruebas.

Los cambios pequeños de [calor](evidence/scenarios_v2/war/heat_tiny_coefficient/run.json) y [transporte](evidence/scenarios_v2/war/advection_tiny_coefficient/run.json) sobrevivieron: el contrato no distingue esa alteración con sus tolerancias. **No son equivalentes al problema original.** En [onda](evidence/scenarios_v2/war/wave_tiny_coefficient/run.json), la misma escala de alteración produjo deriva energética relativa de `3,19124 × 10⁻⁷`, superior al límite `10⁻⁷`, y fue detectada por ese criterio.

Por máquina: `13 / 15 ≈ 86,7 %` de detección entre mutantes no equivalentes evaluables. Los tres equivalentes quedan fuera de ese denominador. No hubo `INFRA_FAIL` ni `INCONCLUSIVE` en esta campaña. La cifra no es una probabilidad de corrección de la teoría ni una cobertura universal de errores.

## Un contraste adicional del fluido 3D original

Además de las 42 ejecuciones 1D, GUERRA realizó dos integraciones Taylor–Green a malla fija `32³`, horizonte `T = 4` y pasos `dt = 0,01` y `0,005`. Ambas finalizaron con salida cero y pasaron sus controles. Los tiempos de simulación registrados fueron 100,23 y 203,56 segundos. Se conservaron fuente, logs, campos, parámetros y [control de ejecución](evidence/fluid_temporal_v2/remote/run-control.json).

| Modelo | Diferencia RMS de velocidad final | Diferencia relativa L2 |
|---|---:|---:|
| Euler | 3,32228 × 10⁻¹⁰ | 1,15087 × 10⁻⁹ |
| Navier–Stokes | 1,22411 × 10⁻¹² | 7,59940 × 10⁻¹² |

La diferencia relativa usa como denominador la norma del campo refinado, `dt = 0,005`, sobre las tres componentes y todas las celdas. Las integraciones usaron NumPy 2.2.6 en GUERRA; el análisis posterior de sus archivos utilizó NumPy 2.0.2 en el entorno local. Se conservan los [comandos exactos de comparación](evidence/fluid_temporal_v2/comparison-commands.txt).

La deriva relativa máxima de energía de Euler bajó de `1,55828 × 10⁻¹¹` a `9,29812 × 10⁻¹³`. La [comparación temporal](evidence/fluid_temporal_v2/temporal-comparison.json) registra 14 de 14 hashes remotos correctos y conserva los diagnósticos de ambos modelos.

**El resultado acota una diferencia temporal observada en esta malla, no el error respecto a una solución continua exacta.** Dos pasos no establecen un orden temporal observado. La pequeña diferencia no corrige el cambio de velocidad de Euler de 16,7 % entre 32³ y 64³: sensibilidad temporal y espacial son preguntas distintas.

La corrida GUERRA `dt = 0,01` produjo arrays guardados exactamente iguales a los de WAR con los mismos parámetros. Los archivos NPZ no son idénticos byte a byte, pero sus arrays sí lo fueron en la [comparación entre hosts](evidence/fluid_temporal_v2/war-guerra-comparison.json). Las fuentes difieren en una sola cadena de diagnóstico que sustituye el texto fijo «32³» por el valor de `n`; no cambia el cálculo. Se conserva el [diff de fuente](evidence/fluid_temporal_v2/war-original-source-diff.txt). Es reproducibilidad del mismo esquema, no contraste con un solver independiente.

## Trazabilidad y reproducción

- [Skill reutilizable](skills/escenarios-verificables/SKILL.md): protocolo dominio-agnóstico, no motor universal.
- [Runner de experimentos](skills/escenarios-verificables/scripts/run_scenario.py): SHA256 `cc9259992eee682d9ebb7c368e0cb91454b3f777d4b41ae3a87baf72e19094b9`.
- [Agregador](controls/summarize_scenarios.py): verifica matriz de casos, identidad de referencias, versiones y hashes antes de resumir.
- [Renderer analítico](simulation/render_analytic_scenarios.py): evalúa las fórmulas, contrasta el oráculo guardado a `T = 0,7`, revisa datos iniciales, periodicidad y retorno temporal.

WAR utilizó Python 3.10.11 y GUERRA Python 3.12.3; ambos, NumPy 2.2.6 y Matplotlib 3.10.8. Cada ejecución solicita un hilo y usa CPU. En el video, Matplotlib calcula la representación en CPU; NVENC usa la GPU para codificar, no para resolver estas ecuaciones.

Para reproducir el resumen, elegir un archivo nuevo de salida:

```sh
python controls/summarize_scenarios.py --root evidence/scenarios_v2 --output resultados/campaign_summary.json
```

Para preparar vistas del video en WAR, usando la ruta de resultados de esa máquina:

```sh
python simulation/render_analytic_scenarios.py --results RUTA_RESULTADOS_WAR --output VISTAS_NUEVAS --mode preview
python simulation/render_analytic_scenarios.py --results RUTA_RESULTADOS_WAR --output VIDEO_NUEVO --mode render
```

Los comandos no sobrescriben carpetas con evidencia. Conservar juntos los MP4, previews y `render_summary.json`. El renderer usa la API pública de [superficies 3D de Matplotlib](https://matplotlib.org/stable/api/_as_gen/mpl_toolkits.mplot3d.axes3d.Axes3D.plot_surface.html); el relieve es una decisión de representación, no parte de la PDE.

### Muestra de voz: todavía sin aprobar

Se conserva una [muestra de Chatterbox](evidence/voice_preview_v2/audio/voz.mp3) generada en WAR mediante el servicio de voz de GeneratorVideo. Dura 13,95 segundos, con ritmo informado de 202 palabras por minuto. Se abrió y reprodujo en QuickTime para presentarla; todavía no consta aprobación del usuario sobre timbre, ritmo o pronunciación.

El [registro de verificación](evidence/voice_preview_v2/verification.json) acredita coincidencia de hashes y decodificación sin errores, no una escucha humana certificada. No se guardó una transcripción independiente de Whisper; el SRT procede del guion suministrado y no sirve como comprobación independiente de lo pronunciado. La muestra no se ha aplicado a los 15 capítulos anteriores ni a estos clips sin audio.

### Manifiesto V2 separado

Tras reunir y revisar los artefactos finales, generar un manifiesto nuevo:

```sh
python controls/hash_v2_artifacts.py --output SHA256SUMS_V2.txt
```

Este helper exige las carpetas de entrega, no sobrescribe un manifiesto existente y rechaza el nombre `SHA256SUMS.txt` de V1. Verifica primero los 379 hashes del render: al resolver las rutas convierte el separador Windows `\` a `/`, sin reescribir el JSON original. Registra fuentes, contratos, resultados de ambos hosts, contraste temporal 3D, lámina GPT, muestra de voz y render analítico. Los hashes detectan cambios de bytes; no son una certificación independiente de las afirmaciones matemáticas.

## Qué falta

La [hoja de ruta V2](PLAN_VALIDACION_V2.md) separa segundo kernel, control positivo de Euler, revisión semántica de fuerza cero y nuevos contrastes 3D. Ninguna de esas brechas se da por cerrada por estas 42 ejecuciones. La versión audiovisual original y sus hashes permanecen intactos.
