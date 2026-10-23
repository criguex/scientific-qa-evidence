# Contratos ODE V3: oscilador y reacción reversible

Estos son dos modelos estipulados y adimensionales, con oráculos analíticos. Se verifica su implementación numérica, no que describan cualquier objeto físico o sustancia real. No incluyen mediciones experimentales, unidades calibradas, temperatura variable, ruido ni acoplamiento espacial.

## Escenarios fijados antes de la campaña

### Oscilador lineal

```text
x' = v
v' = −ω²x − 2ζωv
```

`x` es desplazamiento, `v` su derivada respecto al tiempo adimensional, `ω` la frecuencia natural adimensional y `ζ` la razón de amortiguamiento. Se aceptan parámetros finitos, `ω ≥ 0`, `ζ ≥ 0`. El caso libre `ω = 0` se define aquí solo con `ζ = 0`.

| ID | ω | ζ | x inicial | v inicial |
|---|---:|---:|---:|---:|
| osc01 | 0,8 | 0 | 0,7 | −0,2 |
| osc02 | 1,7 | 0 | −0,4 | 0,9 |
| osc03 | 0,8 | 0,35 | 0,7 | −0,2 |
| osc04 | 1,7 | 0,35 | −0,4 | 0,9 |
| osc05 | 0,8 | 1 | 0,7 | −0,2 |
| osc06 | 1,7 | 1 | −0,4 | 0,9 |
| osc07 | 0,8 | 1,8 | 0,7 | −0,2 |
| osc08 | 1,7 | 1,8 | −0,4 | 0,9 |
| osc09 | 0 | 0 | 0,4 | 0,3 |

Se cubren los regímenes sin amortiguamiento, subamortiguado, crítico, sobreamortiguado y libre. No se aproxima arbitrariamente un valor cercano a `ζ = 1` por el caso crítico: la rama crítica utiliza igualdad exacta para los valores fijados.

### Reacción reversible genérica A ⇌ B

```text
A' = −kf A + kr B
B' =  kf A − kr B
```

`A`, `B` representan concentraciones adimensionales; `kf`, `kr` son tasas adimensionales de primer orden. El sistema es cerrado y bien mezclado. Todos los parámetros y estados iniciales deben ser finitos y no negativos. No se asignan nombres de sustancias ni se dan instrucciones de laboratorio.

| ID | kf | kr | A inicial | B inicial |
|---|---:|---:|---:|---:|
| rxn01 | 0 | 0 | 1 | 0 |
| rxn02 | 0 | 0 | 0,3 | 0,7 |
| rxn03 | 0,4 | 0 | 1 | 0 |
| rxn04 | 0 | 0,6 | 0 | 1 |
| rxn05 | 0,2 | 0,3 | 1 | 0 |
| rxn06 | 0,7 | 0,1 | 0,2 | 0,8 |
| rxn07 | 2 | 3 | 0,4 | 0,6 |
| rxn08 | 0,3 | 0,7 | 0,7 | 0,3 |
| rxn09 | 0,2 | 0,3 | 0 | 0 |

`rxn08` parte del equilibrio; `rxn09` tiene masa total cero. `rxn07` no está en equilibrio: los flujos iniciales son `0,8` y `1,8`. Estos casos prueban también límites de cobertura, no solo dinámicas que faciliten detectar mutantes.

## Oráculos independientes del integrador

Para el oscilador, sea `α = ζω`.

```text
ω = 0:
  x = x₀ + v₀t
  v = v₀

ζ < 1, β = ω sqrt(1−ζ²):
  x = exp(−αt)[x₀cos(βt) + (v₀+αx₀)sin(βt)/β]
  v = exp(−αt)[v₀cos(βt) − (αv₀+ω²x₀)sin(βt)/β]

ζ = 1, d = v₀+ωx₀:
  x = exp(−ωt)(x₀+dt)
  v = exp(−ωt)(v₀−ωdt)

ζ > 1, β = ω sqrt(ζ²−1), r± = −α±β:
  C+ = (v₀−r−x₀)/(r+−r−)
  C− = (r+x₀−v₀)/(r+−r−)
  x = C+exp(r+t) + C−exp(r−t)
  v = r+C+exp(r+t) + r−C−exp(r−t)
```

En las dos últimas expresiones `r+t` y `r−t` significan `r₊·t` y `r₋·t`, no suma o resta de tiempo.

Para la reacción, `S = A₀+B₀`, `q = kf+kr`. Si `q = 0`, ambos estados permanecen constantes y no se divide por cero. En otro caso:

```text
Aeq = kr S / q
A(t) = Aeq + (A₀−Aeq)exp(−qt)
B(t) = S−A(t)
```

Las autopruebas contrastan estados iniciales y derivadas iniciales del oráculo con el operador original, rechazan parámetros inválidos y revisan casos de redondeo y equivalencia. Son controles de implementación; la fórmula analítica sigue siendo parte del contrato que requiere revisión matemática.

## Integración y aceptación

Tiempo final `T = 4`, RK4 en pasos `h = 0,05`, `0,025` y `0,0125`: 80, 160 y 320 pasos. El error `E_h` es el máximo, sobre los **81 tiempos comunes** `t = j·0,05`, del RMS de los dos componentes respecto al oráculo. Se comprueba finitud e invariantes en **todos** los pasos, no solo en esos tiempos comunes.

Cada referencia debe cumplir:

- `E_fino < 10⁻⁶`.
- En cada pareja de pasos, `p = log₂(E_h/E_h/2)` entre `3,6` y `4,4`, solo si ambos errores superan `10⁻¹²`.
- Si uno de los errores es menor o igual que `10⁻¹²`, registrar `ROUND_OFF_LIMITED` y `p = null`. No inventar un orden cuatro para soluciones exactas o dominadas por redondeo.
- Oscilador: energía `E = 0,5(v²+ω²x²)`. Sin amortiguamiento, deriva relativa máxima `≤ 10⁻⁶`; si la energía inicial es cero, usar deriva absoluta `≤ 10⁻¹²` sin dividir por cero. Con amortiguamiento, incremento por paso `≤ 10⁻¹²`.
- Reacción: `|A+B−S| ≤ 10⁻¹²`, `A,B ≥ −10⁻¹²`, `A,B ≤ S+10⁻¹²`.

La identidad continua `dE/dt = −2ζωv²` fundamenta el criterio energético del oscilador. Los umbrales se calibraron antes de la campaña con una implementación independiente en Python estándar: los 16 escenarios no añadidos posteriormente dieron error fino máximo aproximado `4,27×10⁻⁸` en oscilador y `9,86×10⁻⁹` en reacción; los órdenes no limitados por redondeo estuvieron entre `3,995` y `4,169`. Libre y masa cero usan ramas analíticas degeneradas que se comprobarán explícitamente. Estas cifras de calibración no sustituyen los resultados que debe generar el runner en cada máquina.

## Mutantes reales

Cada mutante se ejecuta con `h = 0,0125`, conservando el oráculo y los parámetros originales. Exigir `E_fino < 10⁻⁶` e invariantes; no exigir al mutante un refinamiento de tres pasos.

| Caso | Identificador | Cambio |
|---|---|---|
| Oscilador | `spring_sign` | `−ω²x` pasa a `+ω²x`. |
| Oscilador | `damping_sign` | `−2ζωv` pasa a `+2ζωv`. |
| Oscilador | `spring_coefficient` | Solo `−ω²x` se multiplica por `1,25`. |
| Oscilador | `frozen` | Ambos campos del RHS se anulan. |
| Reacción | `reverse_sign` | Cambian ambos signos del flujo inverso: `A'=−kfA−krB`, `B'=kfA+krB`. |
| Reacción | `forward_coefficient` | `kf` se multiplica por `1,25` en ambas ecuaciones. |
| Reacción | `mass_leak` | Se omite `−krB` solo en `B'`. |
| Reacción | `frozen` | Ambos campos del RHS se anulan. |

Una equivalencia se justifica para el **operador con los parámetros fijados**, no para todos los parámetros de la teoría:

- `ω = 0`: los cambios de resorte son identidad del operador; `ζω = 0`: cambiar el signo del amortiguamiento también.
- `kr = 0`: `reverse_sign` y `mass_leak` no cambian el operador.
- `kf = 0`: `forward_coefficient` no cambia el operador.
- `kf = kr = 0`: `frozen` coincide con el operador de reacción original.

El estado inicial de equilibrio o la masa cero pueden hacer que un operador diferente produzca la misma trayectoria observada. Eso se registra como `SURVIVED` con cobertura limitada, **no** como equivalencia global. En particular, el oscilador libre mantiene `x'=v`; congelarlo no es una identidad del operador.

## Procedencia y clasificación

El adaptador depende del helper V2 `run_scenario.py`, fijado a SHA256 `cc9259992eee682d9ebb7c368e0cb91454b3f777d4b41ae3a87baf72e19094b9`. Verifica ese hash antes de importarlo; no lo modifica.

Un mutante requiere referencia válida de su misma familia, ID de escenario, parámetros, método, contrato, fuentes, dependencia auxiliar, host e intérprete/entorno. Además verifica los hashes de los artefactos de referencia. Una referencia de otra configuración no concede crédito de detección.

Se conservan `KILLED`, `SURVIVED`, `EQUIVALENT`, `INFRA_FAIL` e `INCONCLUSIVE`. Una referencia correcta se marca `BASELINE_PASS`. Timeout sin causa diagnosticada es inconcluyente; importación, dependencia o ejecución rota es infraestructura. No se fuerza una tasa de detección ni se ocultan escenarios degenerados.

## CLI

```sh
python scripts/run_ode_scenario.py --list-scenarios
python scripts/run_ode_scenario.py --self-check
python scripts/run_ode_scenario.py --case oscillator --scenario osc03 --mutant baseline --output resultados/osc03_base
python scripts/run_ode_scenario.py --case oscillator --scenario osc03 --mutant damping_sign --baseline resultados/osc03_base/run.json --output resultados/osc03_signo
python scripts/run_ode_scenario.py --case reaction --scenario rxn05 --mutant baseline --output resultados/rxn05_base
```

Conservar juntos ambos scripts y la carpeta `references/`. Cada ejecución escribe campos, CSV, gráfico de estados/oráculo y error, logs, código de salida, UTC, duración monotónica y hashes. El cálculo es CPU con un hilo solicitado. Comparar hosts replica la implementación; no la convierte en un modelo experimentalmente validado.
