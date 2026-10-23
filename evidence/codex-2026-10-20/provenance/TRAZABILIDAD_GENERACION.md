# Trazabilidad de la generación audiovisual

Esta entrega combina una simulación numérica auténtica con una explicación editorial del proceso de verificación formal. No es un video creado por un modelo generativo de imágenes. Tampoco es una grabación histórica continua de la pantalla.

## 1. Qué produjo cada parte

| Capa | Herramienta y lugar | Entrada | Salida |
|---|---|---|---|
| Fluido 3D | Python/NumPy, CPU de WAR | Taylor–Green, dominio periódico, viscosidades, malla, paso y horizonte | campos y métricas calculados |
| Superficies científicas | scikit-image `marching_cubes` + Matplotlib, CPU de WAR | magnitud de vorticidad guardada | 201 fotogramas de 1920 × 1080 con dos modelos, cortes y energía |
| Curvas y láminas | Matplotlib, CPU de WAR | JSON/CSV reales | controles, límites y comparación espacial |
| Voz española | `say`, Paulina estándar de macOS, 172 palabras/minuto | guiones JSON versionados | WAV de 48 kHz estéreo, normalizados con FFmpeg |
| Codificación y unión | FFmpeg H.264 NVENC, GPU RTX 5070 de WAR | fotogramas/capítulos y voz | MP4 de simulación y video completo |
| Focos editoriales | implementación propia con `drawbox`/`drawtext`, ejecutada en WAR | plan JSON de tiempos, recuadros y rótulos | ayuda visual sobre capítulos estáticos |
| Explicación histórica Lean | Remotion 4.0.537, render inicial en Mac | diagramas, hechos y salidas auténticas | `PROCESO_5070.mp4`, 3 min 56 s |
| Informe visual | Markdown, conversión `marked` y plantilla HTML local | ambos informes y guiones | HTML navegable con reproductor y transcripción |

**No se utilizó Blender.** No hubo síntesis de video por difusión, generación de fluido por IA, imágenes inventadas como si fueran mediciones, ni proveedor de voz/video de pago. No se ha sustituido el proyecto GeneratorVideo ni modificado su producción.

La RTX 5070 codifica el video; **no ejecutó el solver FFT ni el kernel de Lean**. La generación de superficies científicas tampoco se atribuye a la GPU.

## 2. Procedencia de los datos físicos

El campo inicial es `u=(sin(x)cos(y)cos(z),−cos(x)sin(y)cos(z),0)` en `[0,2π]³` periódico. Se comparan Euler `ν=0` y Navier–Stokes `ν=0,04`, ambos sin fuerza. Se usa Fourier pseudospectral rotacional, proyección de Leray, máscara estricta 2/3 y RK4, `dt=0,01`, `T=4`.

La visualización usa los datos 32³ porque esa es la corrida dibujada y conserva sus escalas fijas. La corrida 64³ se usó como comprobación espacial independiente de la presentación. No se cambió el dato físico para obtener imágenes más atractivas.

Resultado importante: la diferencia RMS relativa de velocidad final entre 32³ y 64³ es `16,7223 %` en Euler y `0,0535176 %` en NS. El máximo muestreado de vorticidad de Euler pasa de `7,166757` a `13,684833`. La energía casi constante no compensa la falta de resolución espacial de Euler 32³. Dos mallas tampoco certifican la convergencia de 64³.

La cámara, el umbral `|ω|=0,8` y la escala de color de los cortes permanecen fijos. Las superficies son niveles de vorticidad: no son paredes, objetos sólidos, partículas ni superficie del agua. El tiempo físico del solver no equivale al tiempo de reproducción del MP4.

Evidencia vinculada:

- [Resumen 32³](../fluid-3d/simulation_results/simulation_summary.json).
- [Resumen 64³](../fluid-3d/simulation_results_n64/simulation_summary.json).
- [Comparación espacial](../fluid-3d/grid_comparison.json).
- [Procedencia del render](simulation/render/render_summary.json).
- [Actualización de las láminas](simulation/render/slides_summary.json).

## 3. Fuentes ejecutadas y versiones

| Elemento | Identidad |
|---|---|
| Solver original 32³ | SHA-256 `23d42d339f84387c714e30723ca1607181193989913751d8c1a8c0960cdaae44` |
| Solver 64³ y entregado | SHA-256 `87d3372edf646da285731f5144551c2a626987f3718c6985b47a6c816f3bdc50` |
| Cambio entre ambos | únicamente etiqueta del tamaño de malla; no cambió el cálculo |
| Campos 32³ | SHA-256 `9adab406c424e2d36bc3e0c9ee666561a7085d4a429498c197119eaf16943f6d` |
| Campos 64³ | SHA-256 `c9c16b767f9a16b0239e88aae0bf60fec99e7ded4ba39638edfdfb7a76437c16` |
| Python WAR |3.10.11 |
| NumPy |2.2.6 |
| Matplotlib |3.10.8 |
| scikit-image |0.25.2 |
| SciPy |1.15.3 |
| Pillow |12.3.0 |
| Remotion |4.0.537, fijado en `video/package-lock.json` |
| FFmpeg de WAR | 9.0.1-full_build-www.gyan.dev; versión completa en `evidence/ffmpeg_version.txt` |

Los JSON de render, láminas, unión y montaje registran por separado el hash de la fuente usada en cada etapa. Que el renderer reciba después una mejora editorial no altera el hash histórico de los fotogramas que ya se habían producido. El manifiesto de entrega debe corresponder a la versión finalmente revisada.

## 4. Montaje y referencia a GeneratorVideo

Se inspeccionó en modo de solo lectura el componente local `factory/assets/remotion/src/Foco.tsx:12` del proyecto `replica-fosil-metal`. Su idea editorial describe focos mediante una caja normalizada, un rótulo y un instante temporal.

Se adoptó únicamente ese patrón de guía de atención. **No se copió el componente ni se invocó su cámara.** La implementación de esta entrega usa filtros FFmpeg y está contenida en [`simulation/render_simulation.py`](simulation/render_simulation.py), con parámetros explícitos en [`simulation/montage_focus.json`](simulation/montage_focus.json).

No hay zoom, recorte, viñeta, deriva de cámara, distorsión de la imagen ni cambio de velocidad del fluido. Los bordes de los recuadros no rellenan ni ocultan los datos. Los rótulos ocupan una zona libre de la cabecera. El capítulo 2, que contiene el movimiento, su reloj y sus escalas, no recibe overlays.

Los tiempos de foco se fijan por segmentos narrativos y se contrastan con la duración real de cada capítulo. Son ayudas editoriales, no subtítulos palabra por palabra ni una transcripción alineada automáticamente. Las comprobaciones rechazan focos fuera de duración y prohíben modificar el capítulo animado.

La versión base se conserva. Los archivos terminados en `_MONTAJE.mp4` permiten revisar la mejora antes de seleccionar la versión de entrega.

## 5. Voz, fuentes y licencias

La voz es Paulina, instalada como voz estándar de macOS, sin clonación de una persona. Los guiones completos están en `simulation/narration.json` y `video/narration.json`. Los comandos de síntesis están versionados; el motor y los recursos propietarios de voz no se redistribuyen.

La voz está sujeta a las condiciones aplicables de Apple. Esta entrega privada no constituye un dictamen de licencia para explotación comercial o publicación. Antes de reutilizarla con otro fin, se deben comprobar las [licencias oficiales de Apple](https://www.apple.com/legal/sla/) que correspondan al sistema utilizado.

El renderer usa DejaVu Sans del entorno Matplotlib existente. El código de montaje localiza ese archivo para dibujar el rótulo; no copia fuentes del sistema a este repositorio. Las dependencias conservan sus propias licencias; el repositorio privado no cambia sus condiciones.

La narración se normaliza hacia −16 LUFS con objetivo de pico verdadero −1,5 dB. El objetivo de normalización no reemplaza la medición del archivo final ni una revisión auditiva humana.

## 6. Reproducción en WAR

El entorno Python se creó aislado del software de producción. Los pasos de cálculo y render se documentan en el [informe numérico](../build-5070/INFORME_SIMULACION_5070.md). Para revisar únicamente los focos sobre los capítulos existentes:

```sh
python render_simulation.py --montage-only --preview-only --input simulation_render --output simulation_videos --process-video PROCESO_5070.mp4 --audio audio --verification-summary derived_verification_summary.json
```

Tras revisar las imágenes `simulation_videos/focused/preview_*.png`:

```sh
python render_simulation.py --montage-only --input simulation_render --output simulation_videos --process-video PROCESO_5070.mp4 --audio audio --verification-summary derived_verification_summary.json
```

La ruta del plan puede cambiarse con `--focus-plan`. Los comandos no necesitan Blender, Node ni Chromium para esta pasada. Mantienen dos hilos por decodificador/codificador y dos hilos de filtros. No recomputan el fluido ni los 201 fotogramas. La opción de resumen añade la voz `06.wav` y una tarjeta de resultado formal **después** del proceso histórico.

Para unir los capítulos sin focos:

```sh
python render_simulation.py --join-only --input simulation_render --output simulation_videos --audio audio --process-video PROCESO_5070.mp4
```

La primera concatenación directa de AAC produjo avisos de timestamps. Se corrigió usando el filtro `concat`, reinicio de timestamps por entrada y continuidad de audio por número de muestras. La repetición de unión terminó a las `16:59:28 UTC`, código 0, y su [log](evidence/compose_v2.log) no contiene avisos de retroceso de tiempo, DTS no monótono, errores ni warnings.

La versión base corregida pasó una decodificación completa con FFmpeg, sin salida de error. Se midieron −15,47 LUFS, pico verdadero −4,14 dBTP y LRA 2,40; duración de video 432,266667 s y de audio 432,300000 s, diferencia de 0,033333 s. Esos controles pertenecen a la **base**, no sustituyen el QA de la versión posterior con focos y cierre. Tampoco equivalen a afirmar una escucha auditiva humana completa.

### QA de la versión final con focos y cierre

La versión final terminó en WAR a las `17:11:39.456704 UTC`. El archivo `VIDEO_COMPLETO_5070_MONTAJE.mp4` dura **470,700 segundos, aproximadamente 7 min 51 s**, y ocupa **32.986.206 bytes**.

| Comprobación final | Resultado observado |
|---|---|
| Decodificación completa, FFmpeg nivel `error` | código 0; salida vacía |
| Log de montaje | sin `error`, `warning`, retroceso temporal ni DTS no monótono |
| Video | H.264 por NVENC, 1920 × 1080, 30 fps, 470,600 s |
| Audio | AAC, 48 kHz, estéreo, 470,700 s |
| Diferencia de duración | cola de audio de 0,100 s respecto al video |
| Sonoridad integrada | −15,58 LUFS |
| Pico verdadero | −4,14 dBTP |
| Rango de sonoridad | LRA 2,80 |
| Revisión visual | 15 previews y tarjeta final legibles; borde inicial corregido para no cruzar un valor |
| Procedencia | hashes de renderer, plan, resumen formal y voz final coinciden con el registro del montaje |

El SHA-256 del MP4 final es `a87f54738a7021c0078c2e5f6834a7bd68a3d4b8d5e2838c542fb44bfcbc900c`. Estos resultados se conservan en el [resumen de QA](evidence/qa_audiovisual_final.json), junto con el [registro de montaje](montage_summary.json) y su [log](evidence/montage_final.log). Los metadatos y hashes se recomprobaron en el Mac. **No se afirma haber realizado una escucha humana completa** ni que medir duraciones por sí solo pruebe la sincronía perceptual en cada instante.

También se conservan los registros de [decodificación](evidence/video_final_decode.log), [sonoridad](evidence/video_final_loudness.log) y [metadatos FFprobe](evidence/video_final_ffprobe.json). En el log de sonoridad, `input_i`, `input_tp` e `input_lra` son las mediciones del archivo entregado; los valores `output_*` describen la pasada de análisis a salida nula, no un segundo MP4 de entrega.

## 7. Git privado y artefactos

El código, guiones, parámetros, versiones, hashes, informes, CSV y resúmenes JSON pertenecen al historial privado. Los PNG pequeños seleccionados permiten revisar los diagramas sin descargar todo el video. Los logs que se incorporen deben revisarse para excluir credenciales, tokens, variables de entorno privadas y datos ajenos al trabajo; no se altera su contenido matemático relevante.

Los MP4, WAV/AIFF, NPZ, entornos y dependencias instaladas quedan fuera del historial Git mediante `.gitignore`. Las fuentes se registran en el [repositorio privado](https://github.com/criguex/adv-050-auditoria). El destino previsto para artefactos grandes es la [release privada `v2026.10.20-5070`](https://github.com/criguex/adv-050-auditoria/releases/tag/v2026.10.20-5070), con paquete `ADV050_5070_EVIDENCIAS.tar.gz`, MP4 principal y `SHA256SUMS.txt`. La existencia del repositorio no significa que la carga de la release ya esté completada.

Una copia de un hash no aporta una firma independiente; permite detectar cambios respecto a la evidencia conservada.

No se incluyen memoria operativa atribuida al usuario, secretos, acceso SSH ni configuración de cuentas. No se publican artefactos ni se paga a proveedores sin autorización.

## 8. Límites de interpretación

Las 18 comprobaciones numéricas verifican casos analíticos, funciones auxiliares, rechazo y refinamiento temporal; no son 18 pruebas de teoremas. La diferencia entre mallas es un diagnóstico, no el error contra la solución continua exacta.

El flujo Taylor–Green periódico no equivale al dato compacto en todo `ℝ³` de parte de la auditoría formal. La compilación Lean, sus axiomas y el mutante de fuerza cero tienen evidencia y criterios de aceptación separados. La reconstrucción del proceso indica expresamente su fecha de corte.

Referencias primarias del experimento: [NASA, modelado y validación](https://www.nasa.gov/glenn/research/inlets-and-nozzles/physics-modeling-validation/), [Nektar++, Taylor–Green periódico](https://doc.nektar.info/tutorials/latest/incns/taylor-green-vortex/incns-taylor-green-vortexch2.html), [FFmpeg, filtros](https://ffmpeg.org/ffmpeg-filters.html), [Clay, enunciado matemático](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf).
