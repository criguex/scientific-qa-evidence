# Batería sintética de controles multidominio

Estado: campaña v2 ejecutada y auditada en dos hosts. Cada host evaluó las mismas 84 variantes y obtuvo 27 `PASS`, 54 `KILLED` y 3 `SURVIVED`; son 84 variantes replicadas, no 168 casos independientes. Contrato, parámetros, artefactos y límites están en [`CONTRACT.md`](CONTRACT.md) y en [la evidencia por host](../../evidence/new_validation/README.md). Esta herramienta evalúa modelos sintéticos y detectabilidad de mutaciones conocidas; no valida un dispositivo, una persona, una ley perceptual, Navier–Stokes/Euler ni resultados experimentales.

Los resultados ejecutados están en [`multidomain_mac`](../../evidence/new_validation/multidomain_mac/) y [`multidomain_war`](../../evidence/new_validation/multidomain_war/); el análisis pareado y los criterios de interpretación están en el [acta](../../evidence/new_validation/README.md). `collection_complete` significa que se recolectó la cantidad prevista, no que cada resultado pasó; `all_expected_responses` permanece `null` para clasificación derivada. Retener datos brutos y registrar cualquier dictamen posterior en un artefacto separado.

## Ejecución y artefactos

Solo usa Python estándar. Antes de correr, conservar una copia/hash de todo el directorio. El operador debe proporcionar un destino nuevo y privado o publicable, según su política de datos:

```sh
python3 controls/multidomain_validation/runner.py --out /ruta/nueva/evidencia
```

La carpeta de salida debe no existir; el runner se niega a sobrescribirla. Recolecta 84 evaluaciones previstas: baseline y dos mutantes en 27 casos, más tres calibraciones RC tiny, en un proceso. Los cinco ODE se ejecutan a 64/128/256 pasos; Snell, lente, acústica y Fechner tienen una sola evaluación algebraica/integral por variante y guardan resolución `N/A`. Por evaluación escribe `case_NNN.json`; `observations.csv` conserva cuatro puntos de la trayectoria/sweep por resolución aplicable. `point_normalized_error` es el error local por fila y `max_normalized_error` repite el máximo de esa variante/resolución; los valores no finitos se dejan vacíos. En acústica cada fracción exporta el mismo par estático de presiones; las ocho celdas se etiquetan `reflected_pressure`/`transmitted_pressure` y no son ocho experimentos. `summary.json` contiene el conteo real, estados, tiempos, códigos de retorno, hashes de fuentes/artefactos y runtime sin hostname, IP, identidad ni ruta de salida. `summary.json.sha256` permite verificar el resumen sin autorreferenciar su hash. `collection_complete` solo indica que se recogió el número previsto de respuestas y no que los resultados pasaron. `all_expected_responses` permanece `null` para revisión derivada. Retener los archivos brutos; los dictámenes/reclasificaciones deben ser archivos derivados separados.

Las mutaciones no se ajustan tras ver resultados: cambian signo o coeficiente en cada SUT, o una frontera/índice según el modelo. Los oráculos tienen implementaciones independientes: fórmulas cerradas para cinco ODE, bisección para Snell, intersección de rayos para lente, sistema lineal 2×2 para acústica e integración trapezoidal de `k/I` para Fechner. La integración RK4 del SUT no comparte la función RHS ni el solver con el oráculo de Fechner (que integra directamente el observable). `test_suite.py` es un control del propio instrumento, no evidencia de una ejecución de campaña.

Pruebas locales del instrumento:

```sh
python3 -m unittest controls/multidomain_validation/test_suite.py
```

## Base física e interpretación

- RC: `V(t)=Vin+(V0−Vin)e^(−t/RC)`, convención de carga del circuito RC; [OpenStax, University Physics Vol. 2, 10.5](https://openstax.org/books/university-physics-volume-2/pages/10-5-rc-circuits).
- Enfriamiento: ley de Newton `T−Tamb=(T0−Tamb)e^(−kt)`; solución separable de primer orden, [OpenStax, Calculus Vol. 2, 4.3](https://openstax.org/books/calculus-volume-2/pages/4-3-separable-equations).
- Consumo genérico de segundo orden: `dA/dt=−kA²`, `1/A−1/A0=kt`; [OpenStax, Chemistry 2e, 12.4](https://openstax.org/books/chemistry-2e/pages/12-4-integrated-rate-laws). Es una forma cinética idealizada, no un mecanismo químico identificado.
- Beer–Lambert: la ley decádica `I=I0·10^(−εcl)` implica `dI/dx=−αI`, `α=ln(10)εc` en la forma exponencial usada aquí; [IUPAC Gold Book](https://goldbook.iupac.org/terms/view/B00626).
- Snell y lente delgada: leyes geométricas de óptica en [OpenStax, Physics key equations](https://openstax.org/books/physics/pages/16-key-equations) y [University Physics Vol. 3, 2.4](https://openstax.org/books/university-physics-volume-3/pages/2-4-thin-lenses). La lente usa altura transversal firmada negativa para la imagen real invertida; `do>f` en los tres casos.
- Interfaz acústica normal, lineal, entre medios sin pérdidas: continuidad de presión y velocidad normal; la razón de impedancias define los coeficientes y el balance de intensidad `R²+(Z1/Z2)T²=1`. Referencia de fronteras acústicas: [MIT OCW 6.013, notas, cap. 13, §13.2.1](https://live.ocw.mit.edu/courses/6-013-electromagnetics-and-applications-spring-2009/d3be4ea78b036a6362230fb41780cf54_MIT6_013S09_notes.pdf).
- Fechner: `S=k ln(I/I0)` sirve aquí como modelo ilustrativo de unidad subjetiva; se compara directamente con una integración trapezoidal de `k/I` en una sola configuración de barrido, sin refinamiento artificial. No es universal ni valida respuesta humana. Ver discusión contemporánea, [arXiv:2009.00923](https://arxiv.org/abs/2009.00923).
- Logística: `dp/dx=rp(1−p)` con `K=1`, `0<p₀<1` y `x∈[0,1]` es solo una respuesta/probabilidad sintética en función de un estímulo normalizado, no tiempo biológico ni población. Tampoco son datos o predicciones de percepción humana. Solución logística: [OpenStax, Calculus Vol. 2, 4.4](https://openstax.org/books/calculus-volume-2/pages/4-4-the-logistic-equation).

Las fuentes fijan ecuaciones estándar; no son fuente de datos experimentales de esta batería. Los números y unidades concretos están fijados en `suite.py`; las tres calibraciones tiny RC son sensibilidades numéricas deliberadas, no mutantes que se deban matar. No sumar resultados con campañas históricas de otros modelos.
