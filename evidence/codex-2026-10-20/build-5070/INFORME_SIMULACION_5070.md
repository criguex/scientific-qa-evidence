# Simulación 3D real de Euler y Navier–Stokes

**Ejecutada en WAR, con cálculo numérico y generación de imágenes remotos.**  
Corrida visualizada: 20 de octubre de 2026, `16:40:04.371397Z–16:40:56.439570Z`.  
Duración del cálculo 32³: **52,068 segundos**. Los tiempos del video son diferentes del tiempo físico simulado.

Se calculó la evolución de un campo de velocidad tridimensional y se produjeron imágenes a partir de sus valores. La comparación utiliza el mismo dato inicial en Euler y Navier–Stokes, sin fuerza externa en ambos casos. Navier–Stokes incorpora viscosidad `ν = 0,04`; Euler usa `ν = 0`. La máquina, tiempos y parámetros constan en el [registro real de la corrida 32³](../fluid-3d/simulation_results/simulation_summary.json).

La simulación terminó y sus controles analíticos, temporales e invariantes pasaron. **La prueba espacial detectó una limitación importante: al pasar de 32³ a 64³, la velocidad final de Euler difiere un 16,7 % y su máximo de vorticidad casi se duplica. La malla visualizada de Euler no resuelve bien las estructuras finas a `t = 4`, aunque conserve energía.** En Navier–Stokes, la diferencia de velocidad es mucho menor: `0,0535 %`. Son diferencias entre aproximaciones, no errores medidos contra una solución exacta. La evidencia está en el [comparador real 32³/64³](../fluid-3d/grid_comparison.json).

Esto permite mostrar e inspeccionar un caso concreto y sus limitaciones con evidencia reproducible. **No demuestra una singularidad, regularidad global ni los teoremas de la auditoría Lean.** La ejecución formal separada terminó a las `17:02:18 UTC`: build correcto y cuatro teoremas con axiomas estándar, sin `sorryAx`; comparadores y segundo kernel omitidos. Ese resultado se respalda en sus [logs y resumen derivado](../formal-controls/derived_verification_summary.json), no en el video de fluidos.

## 1. Cómo leer lo que ves

![Vista inicial de las superficies de vorticidad de Euler y Navier–Stokes](simulation/render/intro.png)

La imagen superior muestra dos cubos con el mismo dato inicial. El verde menta identifica Euler y el naranja identifica Navier–Stokes. Las superficies dibujadas no son una pared, la superficie del agua ni una nube de partículas: son **isosuperficies de la magnitud de vorticidad**, es decir, los puntos en los que `|ω| = 0,8`.

La vorticidad es `ω = ∇ × u`, una medida local del giro del campo de velocidad. Una superficie de nivel permite ubicar regiones del campo, pero no sigue necesariamente a las mismas partículas mientras se mueve. La transparencia y el sombreado ayudan a ver la geometría; no codifican densidad ni presión.

Se mantuvieron fijos el valor de la isosuperficie, el tamaño del cubo y la cámara. En los mapas de corte inferiores se mantuvo la misma escala de color para ambos modelos y para todos los tiempos. No se reajusta el contraste en cada fotograma. De este modo, una diferencia visual procede de los datos y no de que cada panel tenga una escala distinta.

Los cortes inferiores muestran `|ω|` en el plano `z = π/4`. Se representan valores de la malla con interpolación de imagen desactivada. La malla del solver es periódica: las caras opuestas del cubo se conectan. No hay paredes de tipo “no deslizamiento”.

El video distingue cinco partes:

1. Vista inicial congelada para explicar los modelos y la geometría.
2. Evolución de `t = 0` a `t = 4`, reproducida lentamente.
3. Curvas de la corrida completa.
4. Controles y comparación de resoluciones.
5. Límites del experimento, seguidos por el video del proceso de verificación formal.

El reloj de la animación indica **tiempo físico adimensional**. No debe leerse como segundos del MP4. Las imágenes del campo se guardaron cada `0,02` unidades de tiempo físico: hay 201 instantáneas por modelo.

## 2. Qué problema se resolvió numéricamente

El dominio es el cubo periódico `[0, 2π]³`. El campo inicial es el vórtice de Taylor–Green:

```text
uₓ(x,y,z,0) =  sin(x) cos(y) cos(z)
uᵧ(x,y,z,0) = −cos(x) sin(y) cos(z)
u_z(x,y,z,0) = 0
```

Aunque la tercera componente de velocidad empieza en cero, el campo depende de las tres coordenadas y su aceleración inicial tiene una componente vertical no nula. No se trata de una simulación bidimensional extruida.

Se integró la ecuación de fluido incompresible:

```text
∂ₜu + (u · ∇)u = −∇p + ν Δu
∇ · u = 0
```

| Parámetro | Corrida visualizada |
|---|---|
| Modelo Euler | `ν = 0` |
| Modelo Navier–Stokes | `ν = 0,04` |
| Fuerza externa | cero en ambos |
| Dominio | `[0, 2π]³`, periódico |
| Malla | `32 × 32 × 32` |
| Paso temporal | `dt = 0,01` |
| Horizonte | `T = 4` |
| Pasos | 400 por modelo |
| Guardado | cada `0,02`; 201 tiempos |
| Precisión de cálculo | `float64` / `complex128` |
| Campos visuales guardados | magnitud de vorticidad en `float32` |
| Velocidad inicial y final guardadas | `float64` |
| Dispositivo de cálculo | CPU de WAR |

Taylor–Green es un caso de referencia usado para estudiar la evolución de vórtices y la energía en simulaciones de fluidos. El uso como benchmark no convierte automáticamente una corrida concreta en una solución exacta. Véanse la [descripción de NASA](https://www.nasa.gov/glenn/research/inlets-and-nozzles/physics-modeling-validation/) y el [tutorial periódico de Nektar++](https://doc.nektar.info/tutorials/latest/incns/taylor-green-vortex/incns-taylor-green-vortexch2.html).

## 3. Cómo se calcula

El solver usa derivadas en Fourier y la forma rotacional de la ecuación. Para cada etapa temporal:

```text
velocidad û en Fourier
    → proyección de divergencia cero + máscara espectral
    → velocidad u y vorticidad ω en el espacio físico
    → producto u × ω
    → transformada de Fourier
    → proyección de Leray
    → restar ν |k|² û
    → etapa Runge–Kutta
```

La proyección de Leray elimina la componente paralela al vector de onda `k` y, con ella, la parte gradiente absorbida por la presión. El modo `k = 0` se trata sin dividir por cero.

El término no lineal se obtiene como `P[FFT(u × ω)]`. Para Navier–Stokes se añade el término disipativo `−ν |k|² û`. La presión no se integra como una variable independiente: queda implícita en la proyección.

La evolución temporal usa Runge–Kutta clásico de cuarto orden, con cuatro evaluaciones por paso. Se proyecta y filtra en cada etapa. La máscara retiene únicamente modos con `|kᵢ| < n/3` en cada dirección; es el tratamiento de aliasing de tipo 2/3 aplicado aquí. Por ello, una malla de 32 puntos por eje no conserva todos sus modos de Fourier.

Estas elecciones producen una aproximación espectral truncada. Conservar muy bien su energía no garantiza que todas las escalas de la solución continua estén resueltas.

## 4. Qué ocurrió en la corrida 32³

![Evolución intermedia a tiempo físico t = 2](simulation/render/frames/frame_0100.png)

En `t = 2` ya se separan los comportamientos: Euler conserva energía y redistribuye el giro; Navier–Stokes disipa energía. Las formas corresponden siempre al mismo nivel `|ω| = 0,8`, no a una cantidad fija de fluido.

![Estado final de la visualización 32³ a tiempo físico t = 4](simulation/render/frames/frame_0200.png)

En `t = 4`, las superficies de Euler son más complejas y ocupan visualmente gran parte del cubo, mientras las regiones de nivel `0,8` de NS se reducen. No significa que aparezca o desaparezca materia: cambia la distribución de vorticidad respecto al umbral elegido. La geometría fina de Euler depende apreciablemente de la resolución, como cuantifica la sección 6.

![Curvas reales de energía, enstrofía, máximo muestreado de vorticidad y cola espectral](simulation/render/curvas.png)

| Magnitud | Euler, inicial | Euler, `t = 4` | Navier–Stokes, inicial | Navier–Stokes, `t = 4` |
|---|---:|---:|---:|---:|
| Energía media `E = ½ media(|u|²)` | 0,125 | 0,12499999999805216 | 0,125 | 0,03892002202084956 |
| Enstrofía `Z = ½ media(|ω|²)` | 0,375 | 1,5700736466820184 | 0,375 | 0,16457561163715306 |
| Máximo de `|ω|` en la malla | 2 | 7,1667570384816335 | 2 | 0,956057966198048 |

Fuente de esta tabla y los diagnósticos siguientes: [resumen numérico 32³](../fluid-3d/simulation_results/simulation_summary.json) y [serie temporal CSV completa](../fluid-3d/simulation_results/metrics.csv).

En Euler, la energía de la aproximación se mantiene casi constante mientras aumenta la intensidad del giro y aparecen estructuras más finas. La deriva relativa máxima de energía fue `1,558275730673131 × 10⁻¹¹`.

En Navier–Stokes, la viscosidad reduce la energía. Al final queda aproximadamente el **31,136 %** de la energía inicial: una reducción de aproximadamente **68,864 %**. La energía no aumentó entre instantáneas guardadas; el mayor incremento entre dos muestras fue negativo, `−2,6415843436507214 × 10⁻⁴`.

El máximo de vorticidad indicado es un **máximo muestreado sobre la malla**, no una demostración del supremo continuo. Que crezca hasta 7,17 durante un intervalo finito no demuestra que diverja al infinito en un tiempo posterior.

La mayor divergencia absoluta observada fue `1,7014902155302333 × 10⁻¹⁶`. El indicador CFL máximo fue aproximadamente `0,073805`. Son diagnósticos útiles de esta corrida; no son una garantía universal de estabilidad o precisión.

### Una advertencia importante de resolución

Se midió la fracción de energía contenida cerca del corte espectral: modos retenidos con alguna componente de onda mayor o igual al 80 % del corte. En Euler alcanzó aproximadamente **1,9283 %**. En Navier–Stokes su máximo fue aproximadamente `0,0005218 %`.

La mayor acumulación relativa de Euler cerca del corte justifica comprobar sensibilidad espacial. La energía total puede conservarse con mucha precisión aunque la distribución entre escalas pequeñas dependa de la malla. La imagen 32³ se usa como visualización ilustrativa, no como una afirmación de turbulencia plenamente resuelta.

## 5. Pruebas numéricas reales y qué cubre cada una

![Resultados de las comprobaciones numéricas](simulation/render/pruebas.png)

Se ejecutaron 18 comprobaciones internas antes de la corrida. Todas pasaron. No son 18 demostraciones matemáticas independientes: incluyen comparaciones analíticas, controles de funciones auxiliares, verificaciones de rechazo y refinamiento temporal. Los valores y umbrales completos están en [numerical_controls.json](../fluid-3d/simulation_results/numerical_controls.json).

| Cobertura de pruebas | Resultado o evidencia | Qué queda fuera |
|---|---|---|
| Fórmulas analíticas | cizalla exacta y aceleración inicial de Taylor–Green, aprobadas | no existe aquí una solución exacta independiente de toda la evolución 3D |
| Consistencia temporal | razones de refinamiento ≈16 a malla fija | no da una cota certificada del error continuo |
| Sensibilidad espacial | Euler `16,7223 %`; NS `0,0535 %` de diferencia relativa de velocidad final | Euler 32³ no está bien resuelto a `t = 4`; dos mallas no prueban convergencia completa |
| Integridad | hashes de campos, CSV, fuentes y manifiesto de entrega | no hay firma independiente de un tercero |
| Imagen y audio | revisión de fotogramas, escalas, formato y señal de audio | no acredita física por el aspecto visual |
| Verificación formal | controles Lean elementales separados | sin cierre de los teoremas principales, BKM ni segundo kernel en esta evidencia |

### 5.1 Valores iniciales conocidos

La energía inicial esperada es `1/8 = 0,125` y la enstrofía inicial es `3/8 = 0,375`. La primera coincidió dentro de la representación usada; la diferencia de la segunda fue aproximadamente `5,55 × 10⁻¹⁷`.

### 5.2 Aceleración inicial de Taylor–Green

Se comparó el lado derecho numérico con esta expresión analítica:

```text
Rₓ = −¼ sin(x) cos(x) cos(2z)
Rᵧ = −¼ sin(y) cos(y) cos(2z)
R_z = ⅛ [cos(2x) + cos(2y)] sin(2z)
```

Para Navier–Stokes se añade `−3νu₀`, porque cada componente inicial es un modo con `|k|² = 3`.

El error máximo fue aproximadamente `4,72 × 10⁻¹⁶` en Euler y `5,00 × 10⁻¹⁶` en Navier–Stokes, frente al umbral `10⁻¹²`. Esta comparación verifica el signo y la estructura inicial del término no lineal, incluida la componente vertical. Comprobar solo energía y una cizalla no detectaría todos esos errores.

### 5.3 Cizalla exacta

Se utilizó `u₀ = (sin y, 0, 0)`. Su vorticidad es `(0, 0, −cos y)`. En Euler permanece estacionaria; con viscosidad evoluciona como:

```text
u(t) = exp(−νt) (sin y, 0, 0)
```

Se comparó la solución numérica a `T = 1` con la fórmula exacta. Los errores máximos fueron aproximadamente `2,22 × 10⁻¹⁶` para Euler y `6,66 × 10⁻¹⁶` para Navier–Stokes, frente a `10⁻¹⁰`.

También se comprobó que la proyección elimine un gradiente, que el rotacional de la cizalla coincida con su expresión analítica y que la forma rotacional del lado derecho coincida con una implementación de la forma convectiva en el dato inicial.

### 5.4 Refinamiento temporal

Sobre una malla fija de 16³ y hasta `T = 1`, se repitió el cálculo con `dt = 0,04`, `0,02` y `0,01`. Se midió la norma RMS de la diferencia entre soluciones sucesivas.

| Modelo | Diferencia `0,04` frente a `0,02` | Diferencia `0,02` frente a `0,01` | Razón |
|---|---:|---:|---:|
| Euler | `6,037586124142581e−9` | `3,775481579320042e−10` | 15,9915655719606 |
| Navier–Stokes | `2,3486309415083155e−9` | `1,4453581502477408e−10` | 16,24947381454036 |

Las diferencias estaban por encima del piso de ruido adoptado (`10⁻¹²`) y las razones superaron el mínimo requerido de 8. Son compatibles con el comportamiento de orden cuatro esperado al reducir el paso a la mitad. Es una comprobación temporal a malla fija, no un certificado de convergencia espacial.

### 5.5 Controles negativos y límites de su alcance

Las funciones de aceptación rechazaron valores deliberadamente excesivos de divergencia, deriva energética de Euler y crecimiento energético de Navier–Stokes. Se comprobó además que el crecimiento viscoso con signo contrario y la inversión del término no lineal no coincidan con las referencias analíticas.

Estos son **controles negativos internos**. No se ejecutaron cinco versiones completas del solver corruptas ni se trata de la campaña ADV-050 B01–B08 mencionada en otro trabajo. Esa diferencia de alcance es importante para no exagerar la validación.

## 6. Sensibilidad espacial: 32³ frente a 64³

Se ejecutó una segunda corrida con el mismo dato inicial, viscosidades, paso temporal y tiempo final, pero con 64 puntos por eje. Terminó en WAR a las `16:51:39 UTC`, tras `504,035 segundos` de cálculo. El comparador real terminó a las `16:51:54 UTC`. El [registro de 64³](../fluid-3d/simulation_results_n64/simulation_summary.json) y el [resultado de comparación](../fluid-3d/grid_comparison.json) conservan los parámetros, valores y hashes.

![Sensibilidad espacial real entre las mallas 32³ y 64³](simulation/render/resolucion.png)

El comparador confronta la velocidad final de la malla fina muestreada cada dos puntos con la de la malla gruesa, en posiciones físicas coincidentes y sin filtrado adicional. La norma RMS abarca las tres componentes y todos esos puntos.

La magnitud comparada es:

```text
diferencia relativa = RMS(u₃₂ − u₆₄ muestreada) / RMS(u₆₄ muestreada)
```

| Magnitud a `t = 4` | Euler 32³ | Euler 64³ | NS 32³ | NS 64³ |
|---|---:|---:|---:|---:|
| Energía cinética media | 0,1249999999981 | 0,1249999999931 | 0,03892002202 | 0,03892001873 |
| Enstrofía | 1,57007365 | 1,82309451 | 0,164575612 | 0,164575640 |
| Máximo muestreado de `|ω|` | 7,166757 | 13,684833 | 0,956058 | 0,956423 |
| Diferencia relativa RMS de velocidad entre mallas | **16,7223 %** | referencia de comparación | **0,0535176 %** | referencia de comparación |

La energía de Euler coincide extraordinariamente bien y, sin embargo, las velocidades presentan una diferencia apreciable y el máximo muestreado de vorticidad pasa de `7,17` a `13,68`. Esto muestra por qué conservar energía no basta para certificar precisión espacial. Con el filtrado y el horizonte usados, **Euler 32³ debe tratarse como una visualización ilustrativa de resolución insuficiente para describir cuantitativamente las estructuras finas finales**.

En Navier–Stokes, la viscosidad amortigua escalas pequeñas y ambas resoluciones producen resultados mucho más próximos en las magnitudes medidas. La diferencia relativa de velocidad es de aproximadamente cinco centésimas de uno por ciento. Es evidencia favorable de estabilidad frente a este refinamiento concreto, no una cota rigurosa del error.

La corrida 64³ también pasó los controles internos y de invariantes: divergencia máxima `1,4451 × 10⁻¹⁶`, deriva relativa máxima de energía Euler `5,5390 × 10⁻¹¹` y energía NS no creciente. **No se asigna una etiqueta de “convergencia espacial aprobada”**: ninguna de las dos resoluciones es una solución exacta y no se ha establecido una tendencia con tres o más mallas, una cota del error continuo ni resolución de todas las escalas. El máximo de vorticidad de 64³ sigue siendo un máximo sobre una malla, no un supremo continuo demostrado.

## 7. Dónde se hizo el trabajo y qué usa la GPU

El solver y Matplotlib se ejecutan en **WAR**, dentro de un entorno Python aislado. El cálculo FFT usa CPU; la generación científica de superficies y gráficos también usa CPU. La RTX 5070 se usa para codificar H.264 mediante NVENC, cuya disponibilidad se comprobó en WAR.

La narración se sintetizó en español con la voz estándar Paulina de macOS y se transfirió a WAR. No imita a una persona concreta. Se normalizó a un objetivo de −16 LUFS y pico verdadero objetivo de −1,5 dB. El montaje y codificación final se realizan en WAR y el MP4 terminado se trae al Mac para reproducirlo.

El render de los 201 fotogramas terminó en WAR a las `16:53:59 UTC`, en `507,809 segundos`. Las láminas de controles y límites se actualizaron a las `16:55:10 UTC` para incorporar la comparación de mallas, conservando los fotogramas ya calculados. El [registro del render](simulation/render/render_summary.json) y el [registro de láminas](simulation/render/slides_summary.json) fijan sus fuentes, parámetros y procedencia. Se entregan los fotogramas 0, 100 y 200 como revisión estática; el conjunto de 201 queda en WAR y puede reproducirse desde los datos guardados.

El montaje final añade recuadros y rótulos temporales solo en capítulos estáticos; conserva íntegro el plano animado. Tras la reconstrucción histórica aparece un cierre narrado con el resultado formal final. `VIDEO_COMPLETO_5070_MONTAJE.mp4` dura 470,700 s y pasó decodificación completa sin errores; mide −15,58 LUFS y pico verdadero −4,14 dBTP. El [QA audiovisual](evidence/qa_audiovisual_final.json) y la [trazabilidad de generación](../provenance/TRAZABILIDAD_GENERACION.md) separan esas comprobaciones de una escucha humana completa, que no se afirma.

| Software observado | Versión |
|---|---|
| Python del solver | 3.10.11 |
| NumPy | 2.2.6 |
| Matplotlib | 3.10.8 |
| scikit-image | 0.25.2 |
| SciPy | 1.15.3 |
| Pillow | 12.3.0 |

Las superficies se extraen mediante `marching_cubes` y se dibujan como colecciones de triángulos. El sombreado es una decisión de presentación aplicada a campos ya calculados. Las referencias de las herramientas son [NumPy FFT](https://numpy.org/doc/stable/reference/generated/numpy.fft.fftn.html), [marching cubes](https://scikit-image.org/docs/stable/api/skimage.measure.html#skimage.measure.marching_cubes) y [Poly3DCollection](https://matplotlib.org/stable/api/_as_gen/mpl_toolkits.mplot3d.art3d.Poly3DCollection.html).

## 8. Archivos, integridad y reproducción

| Artefacto | Función |
|---|---|
| `simulation/fluid_solver.py` | solver, diagnósticos y autopruebas |
| `simulation/compare_grids.py` | comparación espacial entre dos corridas |
| `simulation/render_simulation.py` | imágenes, láminas y montaje remoto |
| `simulation/requirements.txt` | dependencias fijadas |
| `simulation/simulation_results/metrics.csv` | métricas reales 32³ en cada tiempo guardado |
| `simulation/simulation_results/fields.npz` | campos para reproducir la visualización y velocidades extremas |
| `simulation/simulation_results/simulation_summary.json` | parámetros, host, tiempos, pruebas y hashes |
| `simulation/simulation_results_n64/` | campos, métricas y registro real de la segunda resolución |
| `simulation/grid_comparison.json` | resultado real de sensibilidad espacial a `t = 4` |
| `simulation/render/` | imágenes seleccionadas y procedencia del render |
| `SIMULACION_5070.mp4` | explicación del cálculo y la visualización |
| `PROCESO_5070.mp4` | explicación de la ejecución de la auditoría Lean |
| `VIDEO_COMPLETO_5070.mp4` | versión base preservada como historial |
| `VIDEO_COMPLETO_5070_MONTAJE.mp4` | entrega principal: simulación con focos, proceso histórico y actualización final |
| `ACTUALIZACION_FINAL_5070.mp4` | cierre narrado con el resultado formal |

La fuente ejecutada en 32³ tenía SHA-256:

```text
23d42d339f84387c714e30723ca1607181193989913751d8c1a8c0960cdaae44
```

Se conservó esa versión. La posterior corrección de una etiqueta para indicar el tamaño de malla dinámicamente no cambió el cálculo. La nueva fuente tiene SHA-256:

```text
87d3372edf646da285731f5144551c2a626987f3718c6985b47a6c816f3bdc50
```

Hashes de la corrida visualizada:

```text
fields.npz   9adab406c424e2d36bc3e0c9ee666561a7085d4a429498c197119eaf16943f6d
metrics.csv  d887e5e59b8f84e6b20c0080be83afda3d33cda04b7f5dfed56a89461a4a96bb
```

El archivo `simulation_results_n64/fields.npz` tiene SHA-256 `c9c16b767f9a16b0239e88aae0bf60fec99e7ded4ba39638edfdfb7a76437c16`. El comparador verificó los hashes de ambas corridas antes de usar los campos. El manifiesto de entrega es una ayuda de integridad, no una certificación independiente.

Comandos de reproducción, dentro del entorno aislado en WAR:

```sh
python fluid_solver.py --simulate --n 32 --dt 0.01 --T 4 --output simulation_results
python fluid_solver.py --simulate --n 64 --dt 0.01 --T 4 --output simulation_results_n64
python compare_grids.py --coarse simulation_results --fine simulation_results_n64 --output grid_comparison.json
python render_simulation.py --render --input simulation_results --output simulation_render
python render_simulation.py --slides --input simulation_results --output simulation_render --comparison grid_comparison.json
python render_simulation.py --compose --input simulation_render --output simulation_videos --audio audio --process-video PROCESO_5070.mp4
```

Estos comandos crean resultados; no deben relanzarse encima de una entrega cuya evidencia se quiera conservar. Para una repetición usa carpetas nuevas. El renderer compara los hashes de campos y métricas antes de dibujar y detiene el trabajo si no coinciden.

Si los cinco `chapter_*.mp4` ya existen y sus duraciones corresponden a las voces actuales, `--join-only` sustituye a `--compose` para repetir únicamente las dos uniones. La unión usa el filtro `concat`, reinicia las marcas temporales de cada entrada y recodifica H.264/AAC; el audio recibe marcas continuas por número de muestras. Evita depender de la concatenación directa de paquetes AAC de archivos separados. Esta normalización de tiempo sigue la [documentación de filtros FFmpeg](https://ffmpeg.org/ffmpeg-filters.html#concat).

## 9. Por qué esto no resuelve la cuestión formal

El caso visualizado es un flujo periódico particular durante un intervalo finito. La auditoría formal incluye enunciados distintos, entre ellos condiciones sobre datos compactos en todo `ℝ³`. Compartir los nombres “Euler” y “Navier–Stokes” no hace equivalentes los dominios, los cuantificadores, los datos iniciales ni los criterios de explosión.

Una aproximación finita tampoco puede mostrar literalmente una cantidad infinita. Puede mostrar crecimiento, errores, pérdida de resolución o sensibilidad a parámetros. Para inferir una singularidad haría falta un argumento que vaya mucho más allá de estas imágenes y de estos controles.

La [descripción oficial del problema del Clay](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf) establece los enunciados matemáticos y distingue el valor de la evidencia numérica del de una demostración. Este experimento no emite un veredicto sobre el premio.

La conclusión respaldada es más concreta: **se calculó y visualizó un caso 3D real; sus pruebas analíticas, temporales e invariantes pasaron; la comparación espacial detectó una limitación importante de Euler 32³ y mostró mucha menor sensibilidad en NS; se conservan datos, código y logs para inspección.** La aceptación de los teoremas Lean y la interpretación del mutante de fuerza cero requieren la evidencia de aquel trabajo separado.
