# Contratos de calibración 1D

Estos tres ejemplos tienen soluciones analíticas conocidas y se usan para comprobar el método de evidencia. No transfieren automáticamente su validación a Euler 3D ni a una teoría nueva.

## Malla y método

Dominio periódico `[0, 2π)`, sin duplicar el extremo. Nodos `x_j=2πj/N`, tamaños `N=32,64,128`, diferencias centradas de segundo orden y RK4. Tiempo final `T=0,7`.

El paso máximo es `0,2 dx²/κ` para calor y `0,2 dx/|c|` para advección/onda. Se fija `nsteps=ceil(T/dt_max)` y `dt=T/nsteps`, de modo que se compara exactamente el mismo tiempo.

## Ecuaciones y oráculos

| Caso | Ecuación y parámetros | Dato y solución exacta |
|---|---|---|
| Calor | `u_t=κu_xx`, `κ=0,13` | `u₀=1+0,5sin(x)+0,2cos(2x)`; `u*=1+0,5exp(−κt)sin(x)+0,2exp(−4κt)cos(2x)` |
| Advección | `u_t=−c u_x`, `c=1,3` | `u₀=0,2+sin(x)+0,25cos(2x)`; `u*=0,2+sin(x−ct)+0,25cos(2(x−ct))` |
| Onda | `u_t=v`, `v_t=c²u_xx`, `c=0,8` | `u₀=sin(x)+0,25cos(2x)`, `v₀=0,3cos(x)`; fórmulas completas abajo |

Para la onda:

```text
u* = sin(x)cos(ct) + 0,25cos(2x)cos(2ct) + (0,3/c)cos(x)sin(ct)
v* = −c sin(x)sin(ct) − 0,5c cos(2x)sin(2ct) + 0,3cos(x)cos(ct)
```

El oráculo evalúa estas fórmulas, no integra el mismo operador que se intenta verificar. La velocidad inicial no nula impide que una ecuación incorrecta de `v` pase por una degeneración accidental del dato.

## Aceptación de la referencia

- Todos los valores finitos.
- Error RMS final `E128 < 10⁻³`. Para onda se calcula sobre ambos campos conjuntamente.
- Orden observado `p=log₂(E_N/E_2N)` entre `1,7` y `2,3` en ambas parejas. Son tres mallas y un ejemplo suave, no una cota rigurosa de error.
- En `N=64`, comparar `dt` con `dt/2`: RMS de la diferencia menor que `10⁻⁶` y menor que `0,02 E64`. No anunciar orden temporal cuatro a partir de diferencias dominadas por el error espacial.
- Deriva absoluta de la media menor que `10⁻¹⁰`; en onda se revisan las medias de `u` y `v` por separado.
- Calor: varianza no creciente. Advección: deriva relativa de `mean(u²)` menor que `10⁻⁷`.
- Onda: deriva relativa menor que `10⁻⁷` de la energía discreta `0,5 mean(v²+c²((roll(u,−1)−u)/dx)²)`.

Una implementación independiente en Python estándar dio errores RMS aproximados:

| Caso | N32 | N64 | N128 |
|---|---:|---:|---:|
| Calor | 4,6800e−4 | 1,1724e−4 | 2,9325e−5 |
| Advección | 9,1843e−3 | 2,3075e−3 | 5,7759e−4 |
| Onda, u y v | 2,0741e−3 | 5,1924e−4 | 1,2985e−4 |

Estos valores orientan la calibración; el runner debe calcular y conservar sus propios resultados.

## Mutantes

Se ejecutan en `N=64`, conservando el oráculo del problema original y un umbral RMS de `0,005`, además de finitud e invariantes pertinentes. No se exige orden espacial al mutante para declararlo rechazado si ya viola el contrato.

Las modificaciones, tolerancias y resultados deben permanecer separados. La clasificación usa una referencia válida del mismo caso, fuente y entorno. Un mutante aceptado por estos umbrales puede ser `SURVIVED`; solo una equivalencia algebraica explícita permite `EQUIVALENT`.

| Identificador | Cambio real |
|---|---|
| `sign` | Invierte el signo del RHS de calor/advección o solo la aceleración `c²Δu` de onda. |
| `coefficient` | Multiplica por `1,25` el coeficiente del RHS; en onda cambia solo `c²Δu`. |
| `frozen` | Sustituye por cero todos los campos del RHS. |
| `boundary_zero` | Reemplaza por cero los vecinos que cruzan el borde, destruyendo la periodicidad. |
| `equivalent_periodic_shift` | Aplica `roll` de exactamente `N` posiciones antes del operador: identidad algebraica en la malla discreta. |
| `tiny_coefficient` | Multiplica el coeficiente por `1,000001`; calibra la sensibilidad del contrato. |

El cambio pequeño no es equivalente aunque sobreviva. Tampoco se exige que sobreviva: por ejemplo, el contrato energético de onda puede detectar la alteración de `c²`. La tasa de detección, si se calcula, incluye los mutantes no equivalentes ejecutados y muestra los sobrevivientes.

El runner verifica fuente, contrato, caso, host, versión e implementación de Python, ruta del intérprete, versión y ruta de NumPy, arquitectura y hashes de los artefactos de la referencia. Registra ese fingerprint antes de integrar, incluso si la ejecución numérica falla. Es una comprobación de procedencia reproducible, no una certificación criptográfica del sistema operativo ni de todas las bibliotecas cargadas.
