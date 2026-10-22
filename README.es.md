# Scientific QA Evidence

Este repositorio contiene una auditoría de QA independiente de las formalizaciones en Lean 4 de [openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler), que acompañan a “[Finite time blowup for Navier–Stokes](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)” y “[Finite time blowup for the Euler equation](https://cdn.openai.com/pdf/315b36cd-ec98-4023-8342-93345194ece1/euler.pdf)” de OpenAI, más una campaña de pruebas de mutación sobre nueve modelos numéricos. Las pruebas son de OpenAI. Este repositorio no demuestra nada nuevo, no reclama ningún resultado del Premio del Milenio y no es una revisión matemática: recompila los artefactos publicados, los vuelve a verificar con verificadores independientes, comprueba si la cadena de verificación detecta errores y publica cada paso con hashes.

- [Leer el resumen de cinco páginas (PDF, en inglés)](docs/report/scientific-qa-evidence-report-v1.3.0.pdf)
- [Leer cada afirmación con su evidencia y sus límites](CLAIMS.md) (en inglés)
- [Ver las trece escenas de evidencia](animations/index.html)
- [Read in English](README.md)

Por **Cristian Guerra**, QA Automation, Medellín, Colombia ([@criguex](https://github.com/criguex)).

## Navier–Stokes y Euler

Sobre las pruebas de OpenAI en el commit `f9e8bc5`, comprobamos:

- **Verifican desde cero:** Comparator, con los kernels de nanoda y de Lean, aceptó Navier–Stokes (C), (D) y Euler sobre cinco compilaciones, las dos últimas compiladas enteras desde la fuente sin nada precompilado. Una revisión nueva con `leanchecker` coincidió, y el kernel incluye todas las correcciones de solidez conocidas de 2026.
- **El enunciado es el exacto:** Comparator rechazó los seis cambios de un símbolo al desafío y aceptó un control de solo comentario. Las 18 declaraciones del desafío coinciden con el enunciado público de Google DeepMind tras normalización textual (la resolución de nombres no se verificó).
- **Fuera de alcance:** si la prueba en Lean sigue el artículo de OpenAI, algo que [arXiv:2610.08144](https://arxiv.org/abs/2610.08144) (Bastounis, Circelli y Hansen) disputa sin afirmar que algún teorema de Lean sea falso.

## El enunciado del problema de Clay

Los teoremas formales de OpenAI están escritos al estilo de DeepMind. La [descripción oficial](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf) de Clay es un texto. Escribimos literalmente en Lean las ecuaciones (1)–(11), las alternativas **(C)** y **(D)** y la errata de Clay, y probamos:

- **Los teoremas de OpenAI implican la (C) y la (D) de Clay tal como están escritas aquí,** para toda viscosidad ν > 0, sin hipótesis y solo con los axiomas estándar, bajo las dos lecturas de la suavidad en t = 0 (`k1_C`, `k1_D`, `k1_C_oneSided`, `k1_D_oneSided` en [`bridges/`](bridges/README.md)).
- **Abierto:** nadie independiente ha revisado todavía la transcripción literal frente al PDF de Clay ([14 puntos de revisión](bridges/K0_REVIEW.md)), y la (D) lee la errata de Clay sobre la presión periódica como condición sobre las soluciones; la (C) no la usa. Ningún matemático ha revisado los puentes.

## La cadena de verificación

- **Un rechazo no es una refutación:** con tres teoremas que Mathlib ya prueba, Comparator rechazó los ocho enunciados cambiados, incluso uno definicionalmente igual. Una segunda vía en Lean, con una guarda que impide usar el teorema bajo prueba, clasificó cada uno como equivalente, más débil o falso, todo según lo registrado de antemano ([controles Mathlib](experiments/mathlib-controls/RESULTS.md)).
- **Fallos sembrados:** en un benchmark prerregistrado con semilla comprometida, el protocolo marcó cuatro clases de fallo que el procedimiento documentado de OpenAI deja pasar; cuatro rondas de revisión encontraron 17 problemas en el propio experimento ([benchmark](experiments/blind-faults/v2/README.md)).
- **Una comparación concreta:** sobre los mismos archivos auténticos, un recibo que nombra un log ausente pasa el procedimiento publicado de OpenAI con salida idéntica, mientras que la comprobación de recibos P6 lo marca; el control limpio pasa ambos, según lo registrado de antemano ([comprobación de recibos](experiments/receipt-check/RESULTS.md), en inglés). Es una afirmación sobre la trazabilidad de la evidencia, no sobre la prueba.
- **Qué aporta este caso:** ocho hallazgos que el procedimiento de verificación documentado no muestra, tres de ellos defectos corregidos de este mismo estudio ([FINDINGS.md](FINDINGS.md), en inglés). No se afirma novedad metodológica ([RELATED_WORK.md](RELATED_WORK.md)).

## Resultados en resumen

| Pregunta | Resultado | Registro |
| --- | --- | --- |
| ¿Compila desde la fuente? | Sí. Cinco compilaciones; las dos últimas (B4 y B5, `lake --no-cache build`) exit 0, 11.424 jobs, 1 h 29 min y 1 h 16 min, todas las dependencias compiladas localmente. | [compilaciones](evidence/formal/cd-validation/README.md#builds-used-by-each-run), [B5](evidence/formal/b5/README.md) |
| ¿La aceptan kernels independientes? | Sí. Comparator con nanoda y el kernel de Lean aceptó Navier–Stokes (C, D) y Euler en las cinco corridas, una por compilación. | [revalidación](evidence/formal/cd-validation/README.md) |
| ¿Comparator revisa el enunciado exacto? | Sí. 6 de 6 mutantes del enunciado rechazados; control de solo comentario aceptado. | [mutantes](evidence/formal/cd-validation/mutants/) |
| ¿El desafío es el enunciado público? | Las 18 declaraciones coinciden tras normalización textual; la resolución de nombres no se verificó. | [procedencia](evidence/formal/statement-provenance/README.md) |
| ¿Los verificadores están al día? | El código del kernel incluye todas las correcciones de solidez de 2026; nanoda es posterior a su corrección. | [vigencia del kernel](evidence/formal/kernel-currency.md) |
| ¿Rechazan una prueba errónea? | Sí. Lean reporta un error de tipos; nanoda se detiene con un rechazo por aserción. | [mutación del kernel](evidence/formal/kernel-mutation/) |
| ¿El enunciado formal coincide con el texto de Clay? | De 16 cláusulas, 6 coinciden directamente, 9 por hechos estándar y 1 necesita una decisión humana. En Lean, los teoremas de OpenAI implican una transcripción literal de la (C) y la (D) de Clay; esa transcripción aún no tiene revisión independiente. | [revisión de riesgos](evidence/formal/clay-lean-risk.md), [puentes](bridges/README.md) |
| ¿Las pruebas numéricas detectan errores? | 27 PASS · 54 KILLED · 3 SURVIVED por máquina, idénticos en macOS arm64 y Linux x86_64. | [numérica](evidence/README.md) |
| ¿El protocolo detecta lo que el procedimiento base deja pasar? | Con fallos sembrados, sí: cuatro clases de fallo que el protocolo marca y el procedimiento base deja pasar. | [benchmark](experiments/blind-faults/v2/README.md) |
| ¿Un rechazo significa que el teorema es falso? | No. Con tres teoremas de Mathlib, Comparator rechazó los 8 enunciados cambiados, incluidos 3 equivalentes; una vía aparte en Lean clasificó cada uno como equivalente, más débil o falso, todo según lo registrado de antemano. | [controles Mathlib](experiments/mathlib-controls/RESULTS.md) |

Cada afirmación con su evidencia, resultado y limitación está en [CLAIMS.md](CLAIMS.md) (en inglés).

## Verifícalo tú mismo

Python 3.9 o más reciente, sin dependencias, alrededor de un minuto:

```sh
git clone https://github.com/criguex/scientific-qa-evidence.git
cd scientific-qa-evidence
shasum -a 256 -c evidence/SHA256SUMS.txt                           # cada archivo curado es el publicado
python3 evidence/verify_numerical.py                               # corridas guardadas intactas e idénticas entre máquinas
(cd evidence/numerical/source && python3 -m unittest test_runner)  # vuelve a correr las 84 variantes numéricas
python3 evidence/test_consistency.py                               # README, CLAIMS y registros coinciden
python3 experiments/mathlib-controls/verify.py                     # comprueba recibos de los controles Mathlib y recalcula clases
```

Las mismas comprobaciones, y los tests de todos los demás scripts, corren en [GitHub Actions](.github/workflows/verify.yml) en Ubuntu y macOS en cada push. [REPRODUCE.md](REPRODUCE.md) (en inglés) da las versiones, los pasos desde un checkout limpio y qué resultados se recalculan y cuáles solo se verifican por hash. Las compilaciones de Lean necesitan el repositorio de OpenAI y una máquina Linux; aquí sus registros se verifican por hash. Una corrida completa desde un clon nuevo está registrada en [FROM_ZERO.md](evidence/FROM_ZERO.md) (en inglés).

## Parte A · Auditoría formal de (C), (D) y Euler

```mermaid
flowchart LR
    A[Pruebas de OpenAI<br/>commit fijado f9e8bc5] --> B[Cinco compilaciones<br/>B4, B5: nada precompilado]
    B --> C[Comparator]
    C --> D[nanoda + kernel de Lean<br/>aceptan en todas las corridas]
    A --> E[Mutantes del enunciado<br/>6/6 rechazados]
    A --> F[leanchecker --fresh<br/>revisión OK]
    A --> G[Procedencia del enunciado<br/>coincide con DeepMind]
```

Comparator comprueba que la solución prueba exactamente el teorema del archivo de desafío, usando solo los axiomas permitidos (`propext`, `Quot.sound`, `Classical.choice`). La primera corrida (2026-10-20) está en [`evidence/formal/comparator/`](evidence/formal/comparator/README.md). La revalidación del 2026-10-21 añadió tres corridas más, mutantes del enunciado y una revisión desde cero. Terminaron las 18 pruebas: ninguna dio un resultado inesperado y una no pudo correr. Una quinta compilación, B5, repitió la compilación completa desde la fuente para la versión v1.3.0, y Comparator volvió a aceptar los dos desafíos ([registro de B5](evidence/formal/b5/README.md), en inglés).

| Animación | Qué muestra |
| --- | --- |
| <a href="animations/rerun.html"><img src="docs/assets/rerun-preview.gif" width="380" alt="Corridas de Comparator sobre cuatro compilaciones, todas aceptadas"></a><br><a href="docs/media/rerun.mp4">▶ MP4 1080p</a> | **Recompilar y volver a verificar.** Cuatro compilaciones: el registro del 2026-10-20 (B1), una de auditoría cuyo Mathlib vino de la caché precompilada (B2), una nueva (B3) y una completa con `lake --no-cache build` (B4), con todas las dependencias compiladas localmente. Comparator aceptó los dos desafíos en cada una. B3 había recibido en silencio 7 dependencias pequeñas como archivos precompilados de [Reservoir](https://reservoir.lean-lang.org); por eso existe B4. Se reutilizaron la toolchain de Lean y los binarios de los verificadores. |
| <a href="animations/mutants.html"><img src="docs/assets/mutants-preview.gif" width="380" alt="Seis mutantes rechazados y un control aceptado"></a><br><a href="docs/media/mutants.mp4">▶ MP4 1080p</a> | **Cambiar el enunciado: debe ser rechazado.** La prueba de OpenAI nunca se toca. Seis cambios de un símbolo al desafío fueron rechazados con `Challenge and solution theorem statement do not match`; un control de solo comentario fue aceptado. Que un mutante sea rechazado no dice si el enunciado mutado es verdadero, y los mutantes con `f = 0` no dicen nada sobre (A) o (B). |
| <a href="animations/replay.html"><img src="docs/assets/replay-preview.gif" width="380" alt="Revisión del kernel desde cero"></a><br><a href="docs/media/replay.mp4">▶ MP4 1080p</a> | **Revisar cada paso desde un entorno vacío.** `leanchecker --fresh` aceptó las dos soluciones. Usa el kernel de Lean, así que no es una tercera implementación. `lean4lean` no compiló para Lean 4.34 y nunca revisó las pruebas. |
| <a href="animations/provenance.html"><img src="docs/assets/provenance-preview.gif" width="380" alt="El texto del desafío coincide con el enunciado público de DeepMind"></a><br><a href="docs/media/provenance.mp4">▶ MP4 1080p</a> | **De dónde viene el enunciado.** Las 18 declaraciones coinciden tras normalización textual; la resolución de nombres no se verificó. Las diferencias restantes con el archivo de Formal Conjectures de Google DeepMind son el import, el namespace, notación copiada con la misma definición y (A)/(B) excluidos. |

**Frente al texto de Clay.** (C) y (D) dicen "existen datos para los que no existe solución", así que la versión formal solo podría ser más fácil si permitiera datos que Clay prohíbe o si exigiera a las soluciones más que Clay. De 16 cláusulas, 6 coinciden directamente, 9 por hechos estándar de análisis y 1 necesita una decisión humana: la errata de Clay pide presión periódica "en la Ec. (8)", la lista de datos, mientras que la formalización la exige a las soluciones en (D). Ver la [revisión de riesgos](evidence/formal/clay-lean-risk.md) y la Parte D.

## Parte B · Pruebas de mutación numéricas

Las pruebas de mutación preguntan si una suite nota cuando el código se rompe a propósito. El contrato y su tolerancia (10⁻⁶) se congelaron antes de cualquier corrida ([`CONTRACT.md`](evidence/numerical/source/CONTRACT.md), en inglés), y cada modelo tiene un oráculo independiente que no comparte código de solver con la implementación bajo prueba. Los nueve modelos son: circuito RC, enfriamiento de Newton, cinética química de segundo orden, atenuación de Beer–Lambert, respuesta logística, refracción de Snell, lente delgada, interfaz acústica y respuesta de Fechner.

Cada máquina registró **27 PASS, 54 KILLED y 3 SURVIVED** sobre las mismas **84 variantes pareadas**, no 168 distintas; la diferencia escalada máxima entre máquinas es 1,11 × 10⁻¹⁶. Los 54 KILLED cuentan casos, no comportamientos: dos mutantes acústicos dan salidas idénticas, lo que deja 51 comportamientos eliminados distintos. Los tres sobrevivientes son un cambio de RC deliberadamente diminuto, que se deja visible a propósito. Todos los modelos y entradas son sintéticos; nada de esto es una medición empírica.

## Parte C · Qué aporta el protocolo

**Pregunta de investigación.** ¿Pueden las técnicas habituales de QA de software (un contrato congelado, un oráculo independiente, mutaciones deliberadas y corridas repetidas) darle a un lector externo una confianza verificable en una prueba verificada por máquina y en código científico, sin confiar en el montaje de los autores originales?

| Elemento | Código numérico | Cadena de verificación formal |
| --- | --- | --- |
| Contrato, congelado primero | [`CONTRACT.md`](evidence/numerical/source/CONTRACT.md), tolerancia 10⁻⁶ | El enunciado oficial del desafío y los axiomas permitidos |
| Oráculo independiente | Una solución programada aparte para cada modelo | Comparator con dos kernels, más una revisión con `leanchecker --fresh` |
| Mutación deliberada | Dos errores conocidos por modelo y un cambio cerca del umbral | Un valor de prueba erróneo y seis mutantes del enunciado con un control |
| Repetición | Las mismas 84 variantes en dos máquinas | Comparator sobre cinco compilaciones |
| Revisión de la especificación | El propio contrato | Procedencia del enunciado, revisión de riesgos frente a Clay y los puentes en Lean (Parte D) |

### Hallazgos en este caso

Frente al procedimiento de verificación del README de OpenAI, el protocolo produjo ocho hallazgos que ese procedimiento no muestra, tres de ellos defectos corregidos de este mismo estudio ([FINDINGS.md](FINDINGS.md), en inglés).

### Benchmark de fallos a ciegas

Un experimento prerregistrado sembró fallos en casos controlados, asignados con una semilla comprometida. Con el evaluador corregido, los checks del protocolo marcan cuatro clases de fallo que el procedimiento base deja pasar, los dos marcan el control positivo y el caso limpio pasa los dos. La primera corrida se conserva con fe de erratas, y cuatro rondas de revisión encontraron 17 problemas en el propio experimento ([resultados y erratas](experiments/blind-faults/RESULTS.md), [benchmark corregido](experiments/blind-faults/v2/README.md), en inglés).

<a href="animations/experiment.html"><img src="docs/assets/experiment-preview.gif" width="380" alt="Fallos sembrados detectados por cada procedimiento y cuatro rondas de revisión"></a><br><a href="docs/media/experiment.mp4">▶ MP4 1080p</a>

### Una comparación concreta con registros auténticos

El caso C/F5 del benchmark pasó de registros sintéticos a registros reales. Sobre una copia de un árbol compilado desde la fuente se registró paso a paso el procedimiento publicado por OpenAI (`lake exe cache get`, `lake build`, `lake exe comparator ComparatorChallenges/NavierStokes.json`), y luego se corrió otra vez sobre un paquete limpio y sobre uno cuyo recibo nombra un log que no existe.

| Variante | Procedimiento publicado de OpenAI | Comprobación P6 |
| --- | --- | --- |
| Limpia | exit 0, `Your solution is okay!` | exit 0, sin marcas |
| El recibo nombra `comparator-run.log` | exit 0, misma salida byte a byte | exit 1, `P6:receipt-log-missing-comparator-run.log` |
| Log viejo de otra corrida con el nombre correcto (caso 2) | exit 0, misma salida byte a byte | **pasa: P6 solo comprueba que el log exista**; una comprobación contra el hash registrado al correr el paso lo marca |

**En este experimento, P6 detecta una inconsistencia de trazabilidad que no cambia el resultado de Comparator:** el procedimiento publicado, corrido sobre los mismos archivos, salió con 0 y salida idéntica porque no lee recibos. Eso respalda el valor adicional de la comprobación para la trazabilidad de la evidencia; no significa que Comparator aceptara una demostración falsa, porque la prueba era la misma y fue aceptada en ambas variantes. El caso 2 muestra el límite de P6: un log viejo con el nombre correcto lo pasa, y solo atar cada recibo al hash registrado al correr el paso lo detecta. Los dos casos se registraron de antemano, con comandos, versiones, salidas y códigos de retorno ([caso 1](experiments/receipt-check/RESULTS.md), [caso 2](experiments/receipt-check/RESULTS2.md), [estado y enmiendas](experiments/receipt-check/STATUS.md), en inglés).

### Controles con Mathlib: «el enunciado cambió» no es «el teorema es falso»

Un verificador de enunciados responde una sola pregunta: ¿el teorema entregado es exactamente el del desafío? Para ver qué significan sus respuestas, a tres teoremas que Mathlib ya prueba se les dio el enunciado correcto, reformulaciones equivalentes y errores deliberados, con el resultado esperado registrado antes de correr nada. Cada caso rechazado recibió luego una **segunda vía** en Lean: una prueba de equivalencia, una prueba de que es más débil (en las dos direcciones) o una refutación.

| Teorema | Enunciado probado | Comparator | Segunda vía en Lean | Clase |
| --- | --- | --- | --- | --- |
| Primos | `∀ n, ∃ p, n < p ∧ p.Prime` | ✅ aceptado | — | aceptado por el verificador |
| | `n + 1 ≤ p` en vez de `n < p` | ❌ rechazado | `Iff.rfl`: la misma definición | equivalente |
| | `n ≤ p` en vez de `n < p` | ❌ rechazado | equivalencia para todo predicado `P`, no solo primos | equivalente |
| | `∀ n ≤ 100, …` (comprobar ejemplos) | ❌ rechazado | completo ⇒ acotado; acotado ⇏ completo (con `P p := p = 101`) | más débil |
| | `∃ p, ∀ n, n < p ∧ p.Prime` (cuantificadores invertidos) | ❌ rechazado | refutado: tomar n = p | falso |
| Cauchy–Schwarz | `abs ⟪x, y⟫ ≤ ‖x‖ * ‖y‖` | ✅ aceptado | — | aceptado por el verificador |
| | `⟪x, y⟫ ^ 2 ≤ ‖x‖ ^ 2 * ‖y‖ ^ 2` | ❌ rechazado | `abs a ≤ bc ↔ a² ≤ b²c²` si b, c ≥ 0 | equivalente |
| | `<` en vez de `≤` | ❌ rechazado | refutado con x = y = 1 | falso |
| Convergencia dominada | hipótesis de Mathlib | ✅ aceptado | — | aceptado por el verificador |
| | `Integrable bound` como «medible y ∫⁻ ofReal bound < ∞» | ❌ rechazado | equivalente solo porque la dominación obliga a bound ≥ 0 | equivalente |
| | sin dominación | ❌ rechazado | refutado: (n+1) en (0, 1/(n+1)) tiende a 0 y cada integral vale 1 | falso |

**Qué muestra.** Un rechazo solo significa «el enunciado cambió»: Comparator rechazó los ocho cambios, incluso `n + 1 ≤ p`, que para Lean es por definición lo mismo que `n < p`. Una aceptación es igualdad tal como la comprueba Comparator, no la prueba de nada más. Distinguir equivalente, más débil y falso exigió una prueba aparte en cada caso.

**La guarda.** Dos enunciados verdaderos cualesquiera son trivialmente «equivalentes», así que una equivalencia solo cuenta si su prueba no usa el teorema bajo prueba. Un comando de Lean recorre todas las dependencias transitivas de la prueba:

```text
guard: QAControls.SecondRoute.primes_reform_equiv uses none of the theorems under test (1485 constants checked)
error: guard: QAControls.SecondRoute.primes_reform_equiv_cheat depends on Nat.exists_infinite_primes
```

<a href="animations/controls.html"><img src="docs/assets/controls-preview.gif" width="380" alt="Once casos Mathlib: veredictos de Comparator, clases de la segunda vía y la guarda"></a><br><a href="docs/media/controls.mp4">▶ MP4 1080p</a>

La segunda línea es una prueba tramposa a propósito, rechazada según lo registrado. Los 11 casos y los dos controles salieron según lo registrado de antemano. Cada paso tiene un recibo (comando, hashes de entrada y de salida, código de retorno), y `python3 experiments/mathlib-controls/verify.py` comprueba los registros contra ellos y recalcula cada clase; eso comprueba los registros, no vuelve a ejecutar Lean ([diseño](experiments/mathlib-controls/DESIGN.md), [resultados](experiments/mathlib-controls/RESULTS.md), en inglés). Faltan casos preparados por otra persona ([cómo contribuir](experiments/mathlib-controls/HOLDOUT.md)).

### Trabajos previos

Análisis de mutación (DeMillo, Lipton y Sayward, 1978), mutación de especificaciones (1985, 2000), análisis de mutación de proyectos de verificación en Coq (mCoq, 2019), análisis de mutación de verificadores de benchmarks (2026), el criterio de De Bruijn, [Comparator](https://github.com/leanprover/comparator) y [Formal Conjectures](https://github.com/google-deepmind/formal-conjectures) de Google DeepMind. El aporte es la combinación y su aplicación a la propia cadena de verificación; no se afirma novedad metodológica ([RELATED_WORK.md](RELATED_WORK.md), en inglés).

## Parte D · Del teorema de OpenAI al texto de Clay

OpenAI prueba un enunciado formal escrito al estilo de Google DeepMind. ¿Dice lo mismo que el texto de Clay? Para obtener de él la (C) y la (D) de Clay basta una dirección por cláusula: los datos de OpenAI deben cumplir las condiciones de Clay, y toda solución de Clay debe ser una solución formal. Así, si existiera una solución de Clay sería una solución formal, y el teorema de OpenAI lo descarta.

### Qué está probado

Las ecuaciones (1)–(11), la (C), la (D) y la errata de Clay están escritas literalmente en Lean, en coordenadas y con derivadas temporales laterales, en [`bridges/ClayLiteral.lean`](bridges/ClayLiteral.lean). Luego [`bridges/Bridges.lean`](bridges/Bridges.lean) prueba, a partir de los teoremas de OpenAI y sin hipótesis:

```lean
theorem k1_C          (ν : ℝ) (hν : 0 < ν) : ClayLiteral.AltC ν               -- la (C) de Clay
theorem k1_D          (ν : ℝ) (hν : 0 < ν) : ClayLiteral.AltD_withErratum ν   -- la (D) de Clay
theorem k1_C_oneSided (ν : ℝ) (hν : 0 < ν) : ClayLiteral.AltC_oneSided ν      -- (C), otra lectura de C^∞ en t = 0
theorem k1_D_oneSided (ν : ℝ) (hν : 0 < ν) : ClayLiteral.AltD_withErratum_oneSided ν
```

Los cuatro usan solo `propext`, `Classical.choice` y `Quot.sound`. Un control prueba que la solución cero cumple todas las condiciones de solución de Clay, así que «no existe solución» no es verdadero de forma vacía.

<a href="animations/bridges.html"><img src="docs/assets/bridges-preview.gif" width="380" alt="Filas puente del teorema de OpenAI al texto de Clay y los cuatro teoremas K1"></a><br><a href="docs/media/bridges.mp4">▶ MP4 1080p</a>

### Cómo se une cada cláusula

| Texto de Clay (como en `ClayLiteral`) | Versión formal de OpenAI | Puente en Lean |
| --- | --- | --- |
| u° suave, `div u° = 0`, decaimiento (4) | el testigo de OpenAI tiene u₀ = 0 | `d1_zero`, `d2_zero`, `d3_zero` |
| f suave en ℝ³ × [0, ∞), con cualquiera de las dos lecturas en t = 0 | la fuerza de OpenAI es suave en todo ℝ × ℝ³, así que es su propia extensión | `witness_C`, `witness_D` |
| decaimiento (5) y (9) de cada derivada mixta ∂x^α ∂t^m f | una cota de la norma de la derivada m-ésima | `d5`, `d7`: una parcial es esa derivada aplicada a vectores unitarios (`clay_bound`) |
| ecuación (1) en coordenadas, con Σⱼ uⱼ∂ⱼuᵢ y Σₖ ∂ₖ² | la ecuación vectorial con `Δ` y `gradient` de Mathlib | `s1` |
| (2): Σᵢ ∂uᵢ/∂xᵢ = 0 | traza del jacobiano = 0 | `s2` |
| (3) condición inicial | la misma | `s3` |
| (6), (11): u, p ∈ C^∞(ℝ³ × [0, ∞)) | `ContDiffOn` en el semiespacio cerrado | `s4` |
| (7): ∫ abs(u)² dx < C de Lebesgue | `MemLp 2` y una cota de la integral de Bochner | `s5` |
| (8), (10), errata: periodicidad | `IsOnePeriodic` | `d6`, `s6`, `s7_formal_side` |

Cada fila con su estado está en [clay-lean-bridges.md](evidence/formal/clay-lean-bridges.md) (en inglés); el recibo de compilación está en [`bridges/README.md`](bridges/README.md).

### Qué falta

- **Fidelidad de `ClayLiteral`.** El resultado solo es tan fiel como la transcripción literal, que nadie independiente ha revisado frente al PDF. En particular, `SmoothOneSided` está definido directamente como el `ContDiffOn` de Mathlib en el semiespacio cerrado; su nombre no demuestra que esa sea la suavidad que usa Clay, y esa correspondencia es en sí un punto de revisión. Los 14 puntos a revisar, primero la suavidad en t = 0, están en [`bridges/K0_REVIEW.md`](bridges/K0_REVIEW.md) (en inglés).
- **Presión periódica, solo en (D).** K1 para la (D) lee la errata de Clay como condición sobre las soluciones; la (C) no la usa. Ante la pregunta, el presidente del CMI respondió el 2026-10-22 que debe evitar interpretar los enunciados oficiales más allá del texto oficial, y dijo solo que (B) y (D) son problemas en el contexto periódico (toral). Eso no resuelve la lectura de la errata, así que sigue abierta; no es un aval de esta lectura, de la formalización ni de ninguna solución ([registro](evidence/formal/clay-correspondence.md), en inglés).
- **Ningún matemático ha revisado nada de esto.**

## Animaciones

Trece escenas offline, cada una como página HTML interactiva, GIF de vista previa y MP4 en 1080p. Abre la [galería](animations/index.html) o lee la [guía de animaciones](animations/README.md) (en inglés) con ecuaciones, parámetros y trazas de fuente.

| Modelos numéricos | Verificaciones formales |
| --- | --- |
| <a href="animations/rc.html">RC · constante de tiempo duplicada</a> · <a href="docs/media/rc.mp4">▶ MP4</a><br><img src="docs/assets/rc-mutation.gif" width="360" alt="Comparación RC base y mutación"> | <a href="animations/formal.html">Formal · control de tipado del valor de prueba</a> · <a href="docs/media/formal.mp4">▶ MP4</a><br><img src="docs/assets/formal-preview.gif" width="360" alt="Valor de prueba base aceptado y mutación rechazada"> |
| <a href="animations/chemistry.html">Química · tasa de reacción duplicada</a> · <a href="docs/media/chemistry.mp4">▶ MP4</a><br><img src="docs/assets/chemistry-preview.gif" width="360" alt="Comparación de concentración de segundo orden"> | <a href="animations/rerun.html">C/D · recompilar y verificar</a> · <a href="docs/media/rerun.mp4">▶ MP4</a><br><img src="docs/assets/rerun-preview.gif" width="360" alt="Corridas de Comparator sobre cuatro compilaciones"> |
| <a href="animations/cooling.html">Enfriamiento · constante a la mitad</a> · <a href="docs/media/cooling.mp4">▶ MP4</a><br><img src="docs/assets/cooling-preview.gif" width="360" alt="Comparación de enfriamiento base y mutación"> | <a href="animations/mutants.html">C/D · mutantes del enunciado</a> · <a href="docs/media/mutants.mp4">▶ MP4</a><br><img src="docs/assets/mutants-preview.gif" width="360" alt="Mutantes rechazados y control aceptado"> |
| <a href="animations/snell.html">Snell · índices de refracción intercambiados</a> · <a href="docs/media/snell.mp4">▶ MP4</a><br><img src="docs/assets/snell-preview.gif" width="360" alt="Rayos de refracción y barrido de ángulo"> | <a href="animations/replay.html">C/D · revisión del kernel desde cero</a> · <a href="docs/media/replay.mp4">▶ MP4</a><br><img src="docs/assets/replay-preview.gif" width="360" alt="Revisión desde cero y kernels"> |
| <a href="animations/campaign.html">Campaña · clasificaciones pareadas</a> · <a href="docs/media/campaign.mp4">▶ MP4</a><br><img src="docs/assets/campaign-preview.gif" width="360" alt="Clasificaciones de la campaña por máquina"> | <a href="animations/provenance.html">Procedencia del enunciado · OpenAI vs DeepMind</a> · <a href="docs/media/provenance.mp4">▶ MP4</a><br><img src="docs/assets/provenance-preview.gif" width="360" alt="Declaraciones que coinciden en OpenAI y DeepMind"> |
| | <a href="animations/bridges.html">Puentes Clay ↔ Lean · K1</a> · <a href="docs/media/bridges.mp4">▶ MP4</a><br><img src="docs/assets/bridges-preview.gif" width="360" alt="Filas puente del teorema de OpenAI al texto de Clay y los cuatro teoremas K1"> |
| | <a href="animations/controls.html">Controles Mathlib · rechazo no es refutación</a> · <a href="docs/media/controls.mp4">▶ MP4</a><br><img src="docs/assets/controls-preview.gif" width="360" alt="Once casos Mathlib: veredictos de Comparator y clases de la segunda vía"> |
| | <a href="animations/experiment.html">Benchmark de fallos a ciegas</a> · <a href="docs/media/experiment.mp4">▶ MP4</a><br><img src="docs/assets/experiment-preview.gif" width="360" alt="Fallos sembrados detectados por cada procedimiento"> |

![Clip ilustrativo de flujo Taylor–Green, separado de las escenas de evidencia](docs/assets/flow-preview.gif)

El clip de flujo 3D es solo contexto visual, no dato de la campaña, ni evidencia de explosión, ni una construcción formal; su procedencia está en [SOURCE_PROVENANCE.md](evidence/SOURCE_PROVENANCE.md).

## Limitaciones conocidas

Un informe de QA solo sirve si dice lo que no probó.

- **Una sola máquina, herramientas reutilizadas.** Todas las corridas formales usaron una sola máquina Linux. Todas las compilaciones reutilizaron la toolchain de Lean instalada y los binarios de Comparator, lean4export, nanoda y landrun, cuyos hashes están [registrados](evidence/formal/cd-validation/README.md#reused-tools).
- **Dos implementaciones de kernel.** Solo el kernel de Lean y nanoda han revisado las pruebas. `leanchecker` usa el kernel de Lean, y `lean4lean` no compiló para Lean 4.34.
- **Solo bugs de kernel conocidos.** Los verificadores están al día con las correcciones conocidas de 2026, pero en julio de 2026 un bug de Lean y otro distinto de nanoda dejaron pasar la misma prueba falsa, así que el acuerdo entre dos kernels no dice nada sobre bugs desconocidos.
- **Comparator independiente.** Las corridas usaron la herramienta fijada en `19e111e`, no el posterior `lake check` de Lean v4.35.0.
- **No se prueba la correspondencia con el artículo.** Si la prueba en Lean sigue el artículo de OpenAI está fuera de alcance; [arXiv:2610.08144](https://arxiv.org/abs/2610.08144) sostiene que no, sin afirmar que algún teorema de Lean sea falso.
- **La comparación con Clay no está revisada.** La implicación en Lean es relativa a la transcripción literal del texto de Clay de este repositorio, que nadie independiente ha revisado, y deja abierta la (D) sin la errata sobre soluciones.
- **Los mutantes del enunciado prueban la igualdad del enunciado**, no que la prueba fallaría si estuviera mal. Hay un solo fixture de prueba errónea, no una campaña de mutación sobre las pruebas de OpenAI.
- **Límites numéricos.** Los 54 KILLED cuentan casos, no los 51 comportamientos eliminados distintos; los mutantes son gruesos, así que no se mide el umbral de detección; todos los modelos son sintéticos.
- **El benchmark usa fallos sembrados** sobre artefactos grabados, no Lean en vivo, y no da una tasa de detección en el mundo real.
- **Los controles con Mathlib son pocos y los diseñó el autor:** 11 casos con tres teoremas, todavía sin casos de otra persona.

## Cómo se usó la IA

El trabajo fue asistido por IA y dirigido por una persona. OpenAI Codex fue al principio el agente principal de código, y Claude Code de Anthropic hizo los cambios posteriores de auditoría, documentación y experimento. Cada commit nombra al agente en un trailer `Co-Authored-By`. Cristian Guerra eligió las preguntas, congeló los contratos, decidió qué cuenta como evidencia y responde por cada afirmación. Los detalles, incluido un cambio a mitad de sesión del modelo reportado del asistente, están en [AUTHORSHIP.md](AUTHORSHIP.md).

## Mapa del repositorio

```text
README.md, README.es.md   esta presentación, en inglés y en español
CLAIMS.md                 cada afirmación → evidencia → resultado → limitación
FINDINGS.md               qué encontró el protocolo que el procedimiento documentado no muestra
RELATED_WORK.md           trabajos previos y evaluación de novedad
REPRODUCE.md              versiones, pasos, qué se recalcula y qué se verifica por hash
AUTHORSHIP.md             autoría y declaración de uso de IA
evidence/
  formal/                 compilaciones, corridas de Comparator, mutantes, revisiones, procedencia,
                          vigencia del kernel, revisión frente a Clay y plan de puentes
                          (cd-validation/ guarda los registros del 2026-10-21)
  numerical/              contrato congelado, fuente y tests, corridas de 84 casos en macOS y Linux
  SHA256SUMS.txt          checksums de cada archivo curado
experiments/blind-faults/ benchmark prerregistrado: semilla, diseño congelado, casos, resultados, erratas, evaluador v2
experiments/mathlib-controls/ enunciado cambiado frente a teorema falso, con tres teoremas de Mathlib
bridges/                  el texto de Clay en Lean y la prueba de que los teoremas de OpenAI lo implican
animations/               trece escenas offline, scripts de build y exportación, tests
docs/                     GIF, videos MP4 y resumen en PDF
.github/workflows/        CI que corre todas las comprobaciones en cada push
```

## Créditos, derechos y estado

- **Pruebas originales:** OpenAI, [openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler) en `f9e8bc5` (Apache-2.0), con los artículos [Finite time blowup for Navier–Stokes](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf) y [for the Euler equation](https://cdn.openai.com/pdf/315b36cd-ec98-4023-8342-93345194ece1/euler.pdf).
- **Enunciado del problema:** C. L. Fefferman, [Existence and smoothness of the Navier–Stokes equation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf), Clay Mathematics Institute. **Enunciado del desafío:** Google DeepMind, [Formal Conjectures](https://github.com/google-deepmind/formal-conjectures) en `8bf45ed` (Apache-2.0).
- **Herramientas, en las revisiones usadas:** [Lean 4](https://github.com/leanprover/lean4) v4.34.0-rc2 (`6a10ac8`), [Mathlib](https://github.com/leanprover-community/mathlib4) (`85e3a25`), [Comparator](https://github.com/leanprover/comparator) (`19e111e`), [lean4export](https://github.com/leanprover/lean4export) (`cacf989`), [nanoda](https://github.com/ammkrn/nanoda_lib) (`9d6964f`), todas Apache-2.0, y [landrun](https://github.com/Zouuup/landrun) (`ec104f6`, MIT). Se comprobó que cada revisión existe en su repositorio; los hashes de los binarios están en [`receipts/`](evidence/formal/cd-validation/receipts/).
- **Análisis relacionado:** Bastounis, Circelli y Hansen, [arXiv:2610.08144](https://arxiv.org/abs/2610.08144); el resto de los trabajos previos está en [RELATED_WORK.md](RELATED_WORK.md).
- **Este estudio de QA:** Cristian Guerra. Para citarlo, usa [CITATION.cff](CITATION.cff).
- **Derechos:** la publicación está autorizada, pero no se concede ninguna licencia de código abierto. Ver [LICENSE_STATUS.md](LICENSE_STATUS.md).
- **Estado:** última versión [v1.3.0](https://github.com/criguex/scientific-qa-evidence/releases/tag/v1.3.0), que añade los puentes en Lean hacia el texto de Clay, los controles con Mathlib y la compilación B5.

No se afirma ningún descubrimiento de teoremas, certificación científica, validación empírica ni prueba sobre un sistema del mundo real.
