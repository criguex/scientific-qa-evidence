# Contrato congelado — batería sintética multidominio

Versión 1.1 (correcciones de exportación CSV; criterios y modelos sin cambios). Alcance: sensibilidad de un banco sintético de nueve modelos sencillos ante dos mutaciones conocidas por modelo. Algunas configuraciones son reescalados adimensionalmente similares, no tres regímenes matemáticos independientes. No hay datos ni experiencia empírica: no valida un aparato, paciente, persona, experimento, sistema industrial ni resultado científico del proyecto.

## Diseño

Cada familia tiene tres configuraciones no degeneradas. Para cada configuración se evalúan baseline y dos mutantes: 9 × 3 × 3 = 81 variantes. Se añaden tres calibraciones RC con una perturbación relativa de constante de tiempo de `5e-8`; total esperado por diseño: 84 evaluaciones de variante en un proceso, no 84 procesos. Los cinco ODE se evalúan con refinamientos 64, 128 y 256. Snell, lente, interfaz acústica y Fechner no tienen refinamiento de pasos aplicable; se evalúan una vez por variante y se registran con `resolution: N/A`, sin fabricar tres copias. El reporte publica el conteo realmente ejecutado, nunca presupone que sean 84.

Los modelos SUT se implementan en `sut.py`; los oráculos independientes, en `oracles.py`. No comparten RHS, solver ni función de solución. RC, enfriamiento, consumo de segundo orden, Beer–Lambert y respuesta logística se integran con RK4 escalar y se comparan en cuatro observaciones comunes de fracción 1/4, 1/2, 3/4 y 1 del intervalo. Snell usa `asin` contra bisección; lente usa la relación de lente delgada contra trazado de dos rayos; la interfaz acústica usa coeficientes cerrados contra un sistema lineal 2×2; Fechner compara `k ln(I/I₀)` con la integral trapezoidal numérica de `k/I`. Estos cuatro casos son una evaluación cada uno, no una falsa serie de refinamientos.

## Tolerancia y clasificación

La tolerancia fina es `1e-6` en error absoluto normalizado por la escala física declarada para cada salida. Todas las entradas, unidades, escalas y horizontes exactos se escriben en cada JSON de caso. Los ODE usan el error de 256 pasos; los algebraicos usan su única evaluación. No se inferirá orden de convergencia si el redondeo domina.

- Un baseline solo pasa si su salida es finita, cumple los invariantes del modelo y su error normalizado en la última resolución aplicable no supera `1e-6`.
- Un baseline inválido bloquea el dictamen de sus mutantes: no puede producir `KILLED`.
- Un mutante solo se marca `KILLED` si el baseline correspondiente pasa y, en la última resolución aplicable, el mutante es no finito, infringe un invariante o supera la tolerancia.
- Si no satisface esas condiciones, se informa `SURVIVED`, `BASELINE_INVALID`, `BLOCKED_BASELINE` o `INCONCLUSIVE`; no se fuerza la muerte de ningún mutante.
- NaN/Inf nunca es un PASS. Una mutación tiny puede sobrevivir; esa supervivencia es un resultado válido de calibración, no un falso negativo que se reclasifique.

Los invariantes evaluados son: RC dentro del intervalo fuente/inicial y monotonicidad de carga; enfriamiento acotado al ambiente/inicial y monotonicidad; concentración positiva y no creciente; intensidad no negativa y no creciente; ángulo de refracción dentro del semiplano y ley de Snell dentro de la comparación; para lente, altura transversal firmada negativa de la imagen invertida y coincidencia con el oráculo de rayos; balance de energía acústica `R² + (Z₁/Z₂)T² = 1`; sensación ilustrativa no decreciente con intensidad; respuesta logística sintética entre cero y su capacidad de probabilidad `K=1`, no decreciente en un estímulo normalizado. Los invariantes se comprueban en el punto fino de los ODE y en la única evaluación algebraica. Las mutaciones conocidas también se evalúan por su error respecto del oráculo; conservar energía no basta si se viola la condición de frontera. Un valor no finito del oráculo o una longitud incompatible produce `INCONCLUSIVE`, nunca `KILLED`.

## Determinismo y evidencia

No hay aleatoriedad (semilla: n/a). Solo se usa Python estándar. El proceso se debe invocar con un directorio de salida nuevo; si existe, aborta sin escribir. Guarda filas CSV de todas las observaciones/resoluciones, un JSON por variante, resumen de estados y hashes SHA-256 de fuentes, contrato y artefactos. `point_normalized_error` es `|valor−oráculo|/escala` de esa fila; `max_normalized_error` es el máximo de la variante/resolución y se repite por fila para facilitar filtros. NaN/Inf de valor u oráculo se exporta vacío, no como un número. Para acústica, cada una de las cuatro posiciones de observación repite el mismo par estático `(presión reflejada, presión transmitida)`; se exportan las ocho componentes etiquetadas, no son cuatro experimentos independientes. Tiempos y códigos de retorno registran cada evaluación; no equivalen por sí solos a PASS. No guardar hostname, IP, identidad de usuario ni rutas privadas en el paquete publicable.

## Datos de configuración

Todos los parámetros y unidades exactos se declaran en `suite.py` y se repiten en cada JSON de ejecución. Rangos escogidos evitan denominadores nulos, discontinuidades y cambio de régimen (p. ej., reflexión total interna), sin calibrar contra una implementación externa. Los modelos son sintéticos e ilustrativos; Fechner no es una ley perceptual universal y la logística es solo una respuesta/probabilidad sintética con capacidad `K=1`, entrada de estímulo normalizada y `p₀∈(0,1)`, nunca crecimiento de población ni predictor de percepción humana.
