# Física y química V3: variables, mediciones y verificación interna

**20 de octubre de 2026 · resultados reales de WAR, GUERRA y revisión local adicional**

**VERIFICACIÓN INTERNA: conforme para las 18 configuraciones y sus contratos numéricos; cobertura limitada por cinco mutantes sobrevivientes. NO CERTIFICACIÓN EXTERNA.**

**Aclaración editorial posterior (20 de octubre de 2026):** 51/56 cuenta pares evaluados tras excluir 16 combinaciones etiquetadas `EQUIVALENT`; no afirma que todos los 56 pares restantes sean matemáticamente no equivalentes. Los conteos y clasificaciones originales no cambian. La release V3 conserva su paquete histórico; esta copia del informe aporta la precisión de alcance.

Se calcularon nueve osciladores y nueve reacciones reversibles genéricas. Las 18 referencias pasaron los umbrales fijados antes de la campaña. Esto confirma el funcionamiento observado de **dos modelos matemáticos estipulados**, dentro de los parámetros, tiempos y pruebas descritos aquí. No confirma una teoría universal, no valida un experimento físico o químico y no constituye una acreditación de un tercero.

El resultado más directo: el mayor error RMS en los tiempos comunes fue **4,26677 × 10⁻⁸**, frente a un límite de **10⁻⁶**. Las pruebas detectaron **51 de 56 pares de configuración y mutante evaluados**, después de excluir 16 combinaciones etiquetadas `EQUIVALENT`. Los cinco restantes se conservaron como `SURVIVED`: un dato de equilibrio y un estado vacío no permiten observar determinados errores de ecuación. Esta coincidencia para los datos probados no demuestra equivalencia global de esos operadores. [Resumen reproducible](evidence/ode_v3/campaign_summary.json) · [mediciones detalladas](evidence/ode_v3/quantitative_measurements.json).

## 1. Ver los datos

### Física: desplazamiento y velocidad

![Nueve osciladores: estados calculados, oráculo analítico y errores separados](evidence/ode_v3/contacts/physics/FISICA_OSCILADORES_V3.png)

### Química: concentraciones A y B

![Nueve reacciones reversibles: estados calculados, oráculo analítico y errores separados](evidence/ode_v3/contacts/chemistry/QUIMICA_REACCIONES_V3.png)

Cada cuadro superior superpone la integración calculada con la solución analítica, en blanco discontinuo. Que ambas líneas se superpongan a simple vista no basta: el cuadro inferior amplía el **error firmado**, con su escala numérica propia. Verde y ámbar distinguen las dos variables. Las escalas de error pueden cambiar entre cuadros; se muestran para evitar confundir una diferencia diminuta con una grande.

Estas imágenes se generaron con los campos calculados, NumPy y Matplotlib, en WAR para física y GUERRA para química. No son imágenes de IA ni simulaciones espaciales 3D. El render no vuelve a integrar las ecuaciones. Los parámetros y el tiempo son **adimensionales**: no se han calibrado metros, segundos, moles ni una sustancia concreta. [Procedencia física](evidence/ode_v3/contacts/physics/contacts_summary.json) · [procedencia química](evidence/ode_v3/contacts/chemistry/contacts_summary.json).

Los [clips analíticos de calor, transporte y onda de V2](simulation/analytic_render/TRES_ESCENARIOS_ANALITICOS_5070.mp4) siguen disponibles. El fluido 3D de V1 y las ilustraciones GPT son piezas separadas, con alcances distintos.

## 2. Qué se midió y con qué unidades

| Modelo | Variable | Significado | Unidad empleada |
|---|---|---|---|
| Ambos | `t`, `T`, `h` | tiempo, horizonte final y paso numérico | adimensional |
| Oscilador | `x`, `x₀` | desplazamiento e inicial | adimensional |
| Oscilador | `v = dx/dt`, `v₀` | velocidad e inicial | adimensional |
| Oscilador | `ω` | frecuencia natural | adimensional; depende de la escala de tiempo elegida |
| Oscilador | `ζ` | razón de amortiguamiento | adimensional |
| Oscilador | `E = (v² + ω²x²)/2` | energía normalizada del modelo | adimensional; no julios medidos |
| Reacción | `A`, `B`, `A₀`, `B₀` | concentraciones e iniciales | adimensional |
| Reacción | `kf`, `kr` | tasas directa e inversa de primer orden | adimensional |
| Reacción | `S = A+B` | concentración total conservada | adimensional |
| Reacción | `q = kf+kr`, `τ = 1/q` | tasa y tiempo de relajación cuando `q > 0` | adimensional |

No se estimaron estas variables a partir de datos de laboratorio. Los parámetros se **eligieron previamente** para cubrir regímenes distintos; estados, errores e invariantes se calcularon a partir de ellos. La elección de unidades y del modelo es parte del contrato, no una propiedad descubierta de una sustancia real.

## 3. Física: nueve osciladores

La ecuación es:

```text
x' = v
v' = −ω²x − 2ζωv
```

El primer término restaura la posición; el segundo disipa energía cuando `ζ > 0`. La identidad del modelo continuo es `dE/dt = −2ζωv²`. Se cubren ausencia de amortiguamiento, régimen subamortiguado, crítico, sobreamortiguado y movimiento libre.

| ID | ω | ζ | x₀ | v₀ | x(4) calculado | v(4) calculada |
|---|---:|---:|---:|---:|---:|---:|
| osc01 | 0,8 | 0 | 0,7 | −0,2 | −0,684213 | 0,232348 |
| osc02 | 1,7 | 0 | −0,4 | 0,9 | −0,086170 | 1,118455 |
| osc03 | 0,8 | 0,35 | 0,7 | −0,2 | −0,226282 | 0,040090 |
| osc04 | 1,7 | 0,35 | −0,4 | 0,9 | −0,033549 | 0,086106 |
| osc05 | 0,8 | 1 | 0,7 | −0,2 | 0,087231 | −0,055110 |
| osc06 | 1,7 | 1 | −0,4 | 0,9 | 0,000535 | −0,000664 |
| osc07 | 0,8 | 1,8 | 0,7 | −0,2 | 0,260412 | −0,063195 |
| osc08 | 1,7 | 1,8 | −0,4 | 0,9 | −0,033516 | 0,017283 |
| osc09 | 0 | 0 | 0,4 | 0,3 | 1,600000 | 0,300000 |

Valores finales de la corrida fina `h = 0,0125`; se redondean solo en esta tabla. Los valores completos, energía y errores están en [mediciones](evidence/ode_v3/quantitative_measurements.json); campos originales en [WAR](evidence/ode_v3/war/results/).

Ejemplo `osc04`: la energía baja de **0,6362** a **0,00533350693**, es decir, queda aproximadamente **0,838338 %** de la inicial. Eso es compatible con disipación. Al invertir el signo del amortiguamiento, el mutante termina en **76,16496194**, equivalente a **119,718582 veces** la energía inicial. Además, su error RMS máximo es **7,913723714**, muy superior a `10⁻⁶`. No se detecta por una animación: se detecta por dos contratos numéricos distintos. [Referencia](evidence/ode_v3/war/results/osc04/baseline/run.json) · [mutante](evidence/ode_v3/war/results/osc04/damping_sign/run.json).

El caso libre `osc09` comprueba `x(t)=0,4+0,3t`, `v(t)=0,3`. Alterar un término de resorte multiplicado por `ω² = 0` es una identidad del operador para esos parámetros, por eso se clasifica `EQUIVALENT`. Congelar `x'=v` sí cambia el movimiento y se detecta. No se generaliza esa equivalencia a `ω > 0`.

## 4. Química: nueve reacciones reversibles genéricas

El sistema cerrado y bien mezclado se define por:

```text
A' = −kf A + kr B
B' =  kf A − kr B
```

Para `q > 0`, `Aeq = kr·S/q`, `A(t) = Aeq + (A₀−Aeq)exp(−qt)` y `B(t)=S−A(t)`. Si ambas tasas son cero, las concentraciones permanecen constantes y no se divide por cero.

| ID | kf | kr | A₀ | B₀ | A(4) calculada | B(4) calculada | τ = 1/q |
|---|---:|---:|---:|---:|---:|---:|---:|
| rxn01 | 0 | 0 | 1 | 0 | 1,000000 | 0,000000 | no definida; sin dinámica |
| rxn02 | 0 | 0 | 0,3 | 0,7 | 0,300000 | 0,700000 | no definida; sin dinámica |
| rxn03 | 0,4 | 0 | 1 | 0 | 0,201897 | 0,798103 | 2,5 |
| rxn04 | 0 | 0,6 | 0 | 1 | 0,909282 | 0,090718 | 1,666667 |
| rxn05 | 0,2 | 0,3 | 1 | 0 | 0,654134 | 0,345866 | 2 |
| rxn06 | 0,7 | 0,1 | 0,2 | 0,8 | 0,128057 | 0,871943 | 1,25 |
| rxn07 | 2 | 3 | 0,4 | 0,6 | 0,600000 | 0,400000 | 0,2 |
| rxn08 | 0,3 | 0,7 | 0,7 | 0,3 | 0,700000 | 0,300000 | 1 |
| rxn09 | 0,2 | 0,3 | 0 | 0 | 0,000000 | 0,000000 | 2; sin población que relajar |

El `A(4)` de `rxn07` vale **0,5999999995877685**, no exactamente `0,6`; la tabla redondeada no significa equilibrio alcanzado en tiempo finito. `rxn08` sí parte del equilibrio. `rxn09` está vacío. [Datos completos](evidence/ode_v3/quantitative_measurements.json) · [campos y controles GUERRA](evidence/ode_v3/guerra/raw/results/).

`τ` es una escala analítica del operador, no un tiempo observado o ajustado a un experimento. En `rxn08` y `rxn09` no existe desviación inicial que se reduzca: su `τ` solo caracteriza una perturbación hipotética. El JSON también conserva `t95 = ln(20)/q`, escala para reducir una desviación inicial no nula un 95 %; no acredita que ese evento haya ocurrido. Por ejemplo, para `rxn05`, `t95 ≈ 5,99146` queda fuera del horizonte ensayado `T = 4`.

En `rxn05`, el equilibrio es `Aeq = 0,6`, `Beq = 0,4`, con `τ = 2`. A `t = 4` han transcurrido dos tiempos de relajación; queda `exp(−2) ≈ 13,5335 %` de la desviación inicial respecto al equilibrio. Esta interpretación se deriva de la ecuación estipulada, no de una medición química experimental.

Dos mutantes muestran por qué no basta revisar una sola variable. Aquí “masa” en el nombre del control significa la suma invariante de concentraciones adimensionales `A+B` del modelo cerrado 1:1; no masa física medida:

- **Ruptura del balance (`mass_leak`)**: el total pasa de `1` a **1,40312647252218**, un aumento del **40,3126473 %**. Viola conservación y produce error **0,222695059**. [Resultado real](evidence/ode_v3/guerra/raw/results/rxn05_mass_leak/run.json).
- **Ecuación congelada (`frozen`)**: conserva la suma `A+B` exactamente, mantiene positividad y límites, pero deja el estado en `(1, 0)` en lugar de evolucionar. El error **0,345865887** lo rechaza. Conservar un invariante no demuestra que la solución sea correcta. [Resultado real](evidence/ode_v3/guerra/raw/results/rxn05_frozen/run.json).

## 5. Error y refinamiento: números frente a umbrales

Todas las referencias usan RK4 con `h = 0,05`, `0,025` y `0,0125`, durante `T = 4`: 80, 160 y 320 pasos. El error de aceptación es:

```text
E_h = max sobre los 81 tiempos t=j·0,05
      sqrt(((y₁_num−y₁_exacta)² + (y₂_num−y₂_exacta)²)/2)

p = log₂(E_h / E_h/2)
```

El contrato exige `E_fino < 10⁻⁶`. Solo se mide `p` cuando los dos errores comparados son mayores que `10⁻¹²`; de lo contrario, queda `null / ROUND_OFF_LIMITED`. Finitud e invariantes se revisan en **todos los pasos**, no solo en los 81 tiempos comunes. [Contrato congelado](skills/escenarios-verificables/references/contratos-ode-v3.md).

| ID | E fino, 81 tiempos comunes | p: 0,05→0,025 | p: 0,025→0,0125 |
|---|---:|---:|---:|
| osc01 | 1,1666202 × 10⁻¹⁰ | 3,995686 | 3,997803 |
| osc02 | 7,4699137 × 10⁻⁹ | 4,009345 | 4,004780 |
| osc03 | 4,5428120 × 10⁻¹¹ | 4,004740 | 4,002450 |
| osc04 | 1,2637544 × 10⁻⁹ | 4,015770 | 4,007115 |
| osc05 | 3,7988507 × 10⁻¹¹ | 4,031642 | 4,015834 |
| osc06 | 9,0880459 × 10⁻¹⁰ | 4,057531 | 4,028752 |
| osc07 | 9,3282436 × 10⁻¹¹ | 4,079442 | 4,039675 |
| osc08 | 4,2667693 × 10⁻⁸ | 4,169308 | 4,084433 |
| osc09 | 6,5943883 × 10⁻¹⁵ | N/A: redondeo | N/A: redondeo |
| rxn01 | 0 | N/A: redondeo | N/A: redondeo |
| rxn02 | 0 | N/A: redondeo | N/A: redondeo |
| rxn03 | 1,9239887 × 10⁻¹² | 4,012043 | 4,006033 |
| rxn04 | 9,7603037 × 10⁻¹² | 4,018044 | 4,009014 |
| rxn05 | 1,8807733 × 10⁻¹² | 4,015031 | 4,007619 |
| rxn06 | 2,3185065 × 10⁻¹² | 4,024064 | 4,012014 |
| rxn07 | 9,8562258 × 10⁻⁹ | 4,150961 | 4,075308 |
| rxn08 | 3,9252311 × 10⁻¹⁷ | N/A: redondeo | N/A: redondeo |
| rxn09 | 0 | N/A: redondeo | N/A: redondeo |

Son **26 parejas con orden medido**, entre **3,9956858966 y 4,1693084770**, dentro de `[3,6; 4,4]`. Las otras diez parejas están limitadas por redondeo y no acreditan orden cuatro. [Mediciones sin redondear](evidence/ode_v3/quantitative_measurements.json).

| Comprobación de referencias | Peor valor observado | Umbral previamente fijado | Lectura correcta |
|---|---:|---:|---|
| Error fino en 81 tiempos comunes | 4,2667692985 × 10⁻⁸ | < 10⁻⁶ | usa el 4,26677 % de la tolerancia; no es un porcentaje de error relativo del fenómeno |
| Error fino en **todos los 321 tiempos** | 4,2949212712 × 10⁻⁸ | diagnóstico adicional | no sustituye retrospectivamente el criterio de aceptación |
| Deriva relativa de energía sin amortiguamiento, todos los pasos/tamaños | 4,1867647251 × 10⁻⁷ | ≤ 10⁻⁶ | conservación aproximada dentro del umbral |
| Mayor incremento de energía por paso con amortiguamiento | −2,1738059944 × 10⁻¹¹ | ≤ 10⁻¹² | todos los incrementos observados son negativos |
| Deriva de `A+B`, todos los pasos/tamaños | 8,8817841970 × 10⁻¹⁶ | ≤ 10⁻¹² | usa el 0,0888178 % de la tolerancia |
| Concentraciones | todos los controles pasan | ≥ −10⁻¹² y ≤ S₀+10⁻¹² | positividad/límites discretos, no garantía universal de cualquier RK4 |

El límite de error es una tolerancia de ensayo, no un intervalo de confianza estadístico. Se usó `float64`, sin azar ni muestreo Monte Carlo. Los diagnósticos de energía final, tiempo de relajación y máximo sobre los 321 tiempos se extrajeron después de la campaña; **no se cambiaron los umbrales**. [Comandos exactos de extracción](evidence/ode_v3/derived_commands.txt).

## 6. Mutantes ejecutados y límites detectados

Se ejecutaron cuatro cambios reales del operador por configuración: signo, coeficiente, congelación y, según la familia, amortiguamiento o conservación. No se “simularon” sus fallos en un informe: cada ejecución dejó campos, CSV, logs, código de salida y clasificación.

| Campaña principal | Referencias | KILLED | SURVIVED | EQUIVALENT | Total |
|---|---:|---:|---:|---:|---:|
| Física en WAR | 9 | 31 | 0 | 5 | 45 |
| Química en GUERRA | 9 | 20 | 5 | 11 | 45 |
| Total principal | 18 | 51 | 5 | 16 | 90 |

La tasa observada es `51 / (51+5) = 91,0714 %`. La unidad del denominador es **par configuración-mutante evaluado**, después de excluir 16 combinaciones etiquetadas `EQUIVALENT` por identidades algebraicas para los parámetros fijados. Este denominador operativo no afirma que cada uno de los 56 pares restantes sea matemáticamente no equivalente: `SURVIVED` significa que el contrato no distinguió el operador con los datos y parámetros probados. Una trayectoria coincidente en equilibrio o en estado cero no demuestra equivalencia global del operador. La tasa no representa “teorías”, fallos independientes elegidos aleatoriamente ni probabilidad de que una teoría sea verdadera. [Clasificaciones y contratos que fallaron](evidence/ode_v3/campaign_summary.json).

Los cinco sobrevivientes son:

- `rxn08/frozen`: el dato inicial ya está en equilibrio; congelarlo produce la misma trayectoria constante. Error observado `3,9252311467 × 10⁻¹⁷`.
- `rxn09/reverse_sign`, `forward_coefficient`, `mass_leak` y `frozen`: sin concentración inicial, los operadores lineales mutados conservan el estado cero. Error observado cero.

No son equivalencias globales del modelo. Una nueva prueba con datos fuera del equilibrio o no vacíos puede distinguir esos operadores; de hecho, otros escenarios de esta misma campaña los detectan. Tampoco se concluye que la implementación esté libre de otros fallos.

## 7. Réplicas e independencia: tres grupos distintos

| Grupo | Ejecuciones CLI | Alcance |
|---|---:|---|
| Campaña principal | 90 | 18 configuraciones × referencia y cuatro mutantes |
| Réplicas entre WAR y GUERRA | 30 | seis configuraciones ya existentes; mismos cinco operadores por configuración |
| Revisión local adicional | 30 | 18 referencias y 12 controles de clasificación/procedencia |
| Copia de referencia alterada | **no es ejecución** | fixture con `ω` cambiado; se conserva y cuenta aparte |

En las 30 parejas remotas comparadas, estados, oráculos y tiempos guardados son **exactamente iguales como arrays**, con diferencia máxima cero. Coinciden las 30 clasificaciones. Se verificaron 420 hashes de artefactos de esos 30 pares antes de contrastarlos. Los bytes de un contenedor NPZ no tienen que ser idénticos para que sus arrays lo sean. Usar el mismo código en dos hosts acredita esta reproducibilidad observada, no independencia algorítmica. [Comparación cruzada](evidence/ode_v3/cross_host_comparison.json).

La revisión local sí añadió un camino de cálculo distinto para el oráculo: exponencial matricial 2×2 por serie, escalado y cuadrados, frente a las fórmulas por regímenes del adaptador. La diferencia máxima entre oráculos en 90 puntos fue **9,1038288019 × 10⁻¹⁵**. Las 18 referencias locales pasaron, con error máximo en los tiempos comunes **4,2667693016 × 10⁻⁸**. Los 12 controles adicionales confirmaron, entre otros, el rechazo de referencias de otro escenario, familia o parámetros. Es un agente revisor independiente de la implementación dentro del mismo flujo, **no una auditoría externa humana**. [Transcripción y evidencia](evidence/ode_v3/independent_review/PROCEDENCIA.md).

El agregador vuelve a verificar **1.020 hashes de artefactos de 150 ejecuciones**, más seis artefactos de la copia deliberada. Registra 151 hashes de `run.json`, comprueba matriz, parámetros, fuente, contrato, dependencia, resultado crudo, referencia válida y entorno, y reproduce la clasificación. No se suman los grupos como si fueran 150 escenarios científicos independientes.

## 8. Acta de verificación interna reproducible

**Objeto:** implementación numérica y trazabilidad de los 18 escenarios ODE fijados en el contrato V3.

**Dictamen interno:** las 18 referencias son conformes a sus pruebas; la campaña de mutación tiene cobertura limitada y explícita. No se emitió una certificación externa, acreditación, firma de un certificador, sello temporal confiable ni validación experimental.

| Afirmación | Estado | Evidencia y límite |
|---|---|---|
| Las 18 referencias cumplen error, refinamiento aplicable e invariantes | Conforme | datos crudos y contratos congelados |
| Detectamos todos los cambios posibles de ecuación | **No** | sobreviven cinco pares; otros cambios no se ensayaron |
| Los resultados se replican en el subconjunto remoto seleccionado | Conforme | 30 parejas exactas; mismo código |
| Hay contraste numérico de oráculo por una implementación distinta | Conforme, acotado | 90 puntos y 18 referencias locales; no demostración formal |
| Los modelos describen una sustancia u objeto real medido | **No evaluado** | no hay experimentos, calibración de unidades ni incertidumbre instrumental |
| Existe certificación externa acreditada | **No** | no intervino una entidad certificadora |
| SHA256 demuestra autoría, fecha cierta o verdad matemática | **No** | detecta alteraciones respecto al manifiesto; no firma identidad ni acredita el resultado |
| Esto cierra la auditoría formal de Euler/Navier–Stokes | **No** | son modelos y pruebas distintos |

Los horarios UTC y relojes monotónicos provienen de los sistemas de ejecución. Son trazabilidad operativa, no un servicio externo de sellado temporal. La verificación de hashes comprueba igualdad con los bytes registrados; la exactitud científica requiere además contratos adecuados, revisión y límites de cobertura.

## 9. Reproducir sin alterar la evidencia original

Fuentes principales congeladas:

| Archivo | SHA256 |
|---|---|
| `run_ode_scenario.py` | `f118929e692f90ff86cc9bda0f1e3a5288abd0191dceaae432eafaf0c00db9a8` |
| `contratos-ode-v3.md` | `cee74957ddab6f5fa196d06840cfa642f5c08c15eb7b70540eb7e56c9bf5ed06` |
| helper V2 `run_scenario.py` | `cc9259992eee682d9ebb7c368e0cb91454b3f777d4b41ae3a87baf72e19094b9` |
| render final `render_ode_contacts.py` | `e379be05d61bbfde291de07779d3796ec1fb731bf3ba3f0d19eebe3173b67c8e` |

WAR utilizó Python 3.10.11 y GUERRA Python 3.12.3; ambos usaron NumPy 2.2.6 y Matplotlib 3.10.8. La revisión local usó Python 3.12.13 y NumPy 2.5.4. Cada `run.json` conserva el ejecutable, arquitectura, ubicación de NumPy, host, parámetros y huellas. Cálculo y gráficas ODE son **CPU**, con un hilo solicitado; disponer de RTX 5070/4060 no implica que estas integraciones usaran GPU.

Desde la raíz del repositorio, usando un intérprete con las dependencias fijadas y salidas nuevas:

```sh
python skills/escenarios-verificables/scripts/run_ode_scenario.py --self-check
python skills/escenarios-verificables/scripts/run_ode_scenario.py --case oscillator --scenario osc04 --mutant baseline --output nueva_corrida/osc04/baseline
python skills/escenarios-verificables/scripts/run_ode_scenario.py --case oscillator --scenario osc04 --mutant damping_sign --baseline nueva_corrida/osc04/baseline/run.json --output nueva_corrida/osc04/damping_sign
python controls/summarize_ode_v3.py --root evidence/ode_v3 --output nueva_verificacion_ode.json
python simulation/render_ode_contacts.py --case oscillator --results evidence/ode_v3/war/results --output nuevas_graficas_fisica
```

Para reproducir las matrices remotas completas, los comandos y launchers exactos se conservan en [WAR](evidence/ode_v3/war/run_oscillator_war.ps1), [réplica WAR](evidence/ode_v3/war/run_reaction_cross_war.ps1), [GUERRA principal](evidence/ode_v3/guerra/launch-command.txt) y [réplica GUERRA](evidence/ode_v3/guerra/cross-launch-command.txt). Sus rutas son históricas; adaptar únicamente las rutas del entorno nuevo, no fuentes ni criterios para hacer pasar pruebas.

Los logs y JSON crudos conservan sus bytes, incluidos CRLF/BOM cuando existen. El agregador admite BOM en los JSON que lee. Las rutas absolutas Windows describen el origen; no se ejecutan al inspeccionar la evidencia. `.gitattributes` evita la normalización automática de texto. Los NPZ grandes se distribuyen en el paquete privado, no como blobs del historial Git.

El [QA visual V3](evidence/ode_v3/contacts/qa_visual_v3.json) registra la revisión de los 18 paneles finales y la corrección del margen del render preliminar. El cambio fue exclusivamente de composición gráfica: las fuentes del integrador y el contrato conservaron sus hashes.

## 10. Qué falta y qué no cambia respecto a V1/V2

Esta ampliación prueba contratos finitos de modelos lineales. No cubre reacción no lineal, temperatura variable, difusión espacial de especies, ruido, ecuaciones rígidas arbitrarias, mediciones experimentales ni parámetros infinitos. Incorporar otro fenómeno exige seleccionar un nuevo contrato, oráculo y adaptador; la skill no promete simular cualquier teoría.

Los resultados formales Lean de V1 permanecen como evidencia separada. `NS08` —comparadores y segundo kernel— sigue pendiente; `EU06` —control positivo global no nulo— sigue pendiente. `NS09` tiene cierre limitado: falló un helper genérico al añadir fuerza cero, no se demostró que todo testigo final necesitara fuerza, ni que no pudiera repararse. Además, `f = 0` sobre todos los tiempos reales es más fuerte que exigirlo solo para `t ≥ 0`. Ninguna ODE de este informe resuelve esas cuestiones semánticas.

En el fluido 3D, la comprobación temporal V2 a malla fija no elimina la sensibilidad espacial de Euler observada entre `32³` y `64³`. Una tercera malla, comparación filtrada/sin filtrar con criterio previo y un segundo esquema independiente siguen siendo próximos ensayos, no resultados ejecutados aquí. Un máximo de vorticidad grande pero finito en un cálculo no demuestra divergencia de BKM.

Las releases V1 y V2, sus manifiestos y sus fuentes fijadas se preservan. V3 mantiene resumen y manifiesto propios; no se reescriben resultados anteriores para aparentar una validación más fuerte.
