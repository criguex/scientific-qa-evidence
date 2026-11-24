> Traducción al español de [CONTRACT.md](CONTRACT.md). Si hay alguna diferencia, vale el original.

# Contrato congelado — campaña sintética multidominio

Versión 1.1 (corrección en la exportación a CSV; los criterios y los modelos no cambian). Alcance: sensibilidad de una suite sintética de nueve modelos simples a dos mutaciones conocidas por modelo. Algunas configuraciones son reescalamientos adimensionales, no tres regímenes matemáticos independientes. No hay datos empíricos: esta suite no valida ningún aparato, paciente, persona, experimento, sistema industrial ni resultado científico del proyecto.

## Diseño

Cada modelo tiene tres configuraciones no degeneradas. Para cada configuración, evalúa la línea base y dos mutantes: 9 × 3 × 3 = 81 evaluaciones de variantes. Suma tres calibraciones de RC con una perturbación relativa de la constante de tiempo de `5e-8`; el diseño espera entonces 84 evaluaciones de variantes en un solo proceso, no 84 procesos separados. Los cinco modelos de EDO usan 64, 128 y 256 pasos. Las evaluaciones de Snell, lente delgada, interfaz acústica y Fechner no tienen un refinamiento de paso aplicable; corre cada una una vez por variante y reporta `resolution: N/A`, en vez de fabricar tres copias. Reporta los conteos reales de ejecución; no asumas 84.

Los modelos SUT (sistema bajo prueba) están implementados en `sut.py`; los oráculos independientes están en `oracles.py`. El SUT y el oráculo no comparten lado derecho (RHS), solver ni función de solución. RC, enfriamiento, consumo de segundo orden, atenuación de Beer–Lambert y respuesta logística usan RK4 escalar y se comparan en cuatro fracciones de observación comunes: 1/4, 1/2, 3/4 y 1 del intervalo. Snell usa `asin` frente a bisección; la lente delgada usa la ecuación de la lente frente al trazado de dos rayos; la interfaz acústica usa coeficientes de forma cerrada frente a un sistema lineal 2×2; Fechner compara `k ln(I/I₀)` con integración trapezoidal numérica de `k/I`. Estos cuatro casos algebraicos/integrales son una evaluación por variante, no una secuencia de refinamiento falsa.

## Tolerancia y clasificación

La tolerancia fina es `1e-6` de error absoluto normalizado por la escala física declarada de cada salida. Las entradas exactas, las unidades, las escalas y los horizontes quedan registrados en cada JSON de caso. Los modelos de EDO usan el error del paso de 256; los modelos algebraicos usan su única evaluación. No infieras un orden de convergencia cuando el redondeo domina.

- Una línea base pasa solo si su salida es finita, cumple los invariantes del modelo y su error normalizado en la última resolución aplicable es de a lo sumo `1e-6`.
- Una línea base inválida bloquea la clasificación de sus mutantes; no puede producir `KILLED`.
- Un mutante es `KILLED` solo cuando su línea base correspondiente pasa y, en la última resolución aplicable, el mutante es no finito, viola un invariante o excede la tolerancia.
- De lo contrario, reporta `SURVIVED`, `BASELINE_INVALID`, `BLOCKED_BASELINE` o `INCONCLUSIVE` según corresponda; nunca fuerces a que un mutante muera.
- NaN e infinito nunca son `PASS`. Una mutación diminuta puede sobrevivir; eso es un resultado de calibración válido, no un falso negativo que haya que reclasificar.

Los invariantes comprobados son: RC permanece dentro del intervalo fuente/inicial y la carga es monótona; el enfriamiento permanece acotado por la temperatura ambiente/inicial y es monótono; la concentración es positiva y no creciente; la intensidad es no negativa y no creciente; el ángulo de refracción se mantiene en el semiplano válido y cumple la ley de Snell dentro de la comparación; la altura transversal de la imagen en la lente delgada es negativa para una imagen invertida y concuerda con el oráculo de rayos; el balance de energía acústica es `R² + (Z₁/Z₂)T² = 1`; la respuesta ilustrativa de Fechner es no decreciente con la intensidad; y la respuesta logística sintética se mantiene entre cero y su capacidad de probabilidad `K=1` y es no decreciente para el estímulo normalizado. Los invariantes de EDO se comprueban en el punto fino; los invariantes algebraicos, en la única evaluación. Las mutaciones conocidas también se comparan con el oráculo: la sola conservación de energía es insuficiente si se viola una condición de frontera. Un resultado no finito del oráculo o una longitud de vector incompatible es `INCONCLUSIVE`, nunca `KILLED`.

## Determinismo y evidencia

No hay aleatoriedad (semilla: no aplica). Solo se usa la biblioteca estándar de Python. Suministra un directorio de salida nuevo; si ya existe, aborta sin escribir. El runner guarda todas las filas de CSV de observación/resolución, un JSON por variante, resúmenes de estado, tiempos de evaluación y códigos de retorno, y hashes SHA-256 de las fuentes, el contrato y los artefactos. `point_normalized_error` es el `|valor − oráculo| / escala` de la fila; `max_normalized_error` es el máximo para la variante/resolución, repetido por fila para facilitar el filtrado. Los valores no finitos se exportan como celdas vacías, no como valores numéricos. Para acústica, cada una de las cuatro posiciones de observación repite el mismo par estático de presión reflejada/transmitida; los ocho componentes están etiquetados y no son cuatro experimentos independientes. Los tiempos y los códigos de retorno no implican `PASS` por sí solos. No guardes nombres de equipo, direcciones IP, identidades de usuario ni rutas de salida privadas en un paquete publicable.

## Datos de configuración

Los parámetros y unidades exactos están declarados en `suite.py` y se repiten en cada JSON de ejecución. Los rangos evitan denominadores cero, discontinuidades y cambios de régimen (por ejemplo, reflexión interna total); no están calibrados contra una implementación externa. Los modelos son sintéticos e ilustrativos. Fechner no es una ley universal de la percepción, y la respuesta logística es solo una respuesta/probabilidad sintética de estímulo normalizado con capacidad `K=1` y `p₀∈(0,1)`, no crecimiento poblacional ni un predictor de la percepción humana.
