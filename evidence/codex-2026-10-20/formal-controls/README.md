# Acta de evidencia de validación — 2026-10-20

Este paquete reúne tres controles acotados: una batería sintética de sensibilidad a mutaciones, una prueba pequeña de aceptación/rechazo de kernels y un control positivo de una solución periódica constante no nula. No es una demostración de un teorema abierto, una validación universal de kernels, ni una validación experimental o de sistemas reales.

## Resultado principal: batería sintética multidominio

El contrato previo a la ejecución está en [`controls/multidomain_validation/CONTRACT.md`](../../controls/multidomain_validation/CONTRACT.md); código congelado y fuentes de modelos están en [`controls/multidomain_validation/`](../../controls/multidomain_validation/). Los modelos, ecuaciones de referencia, unidades, escalas, parámetros y límites se detallan en su [README](../../controls/multidomain_validation/README.md). La referencia de campaña v2 se conserva en [`multidomain_source_v2.tar.gz`](multidomain_source_v2.tar.gz), SHA-256 `8a98368e7ac53aeb3fedb777ba13073afe42f03b9204d0cfec77120a1f218f99`; hash del contrato `9c48dae363e549243ea5bab36da0d56c51ddec21903bd8dc3c982c2bdb520efb`.

Se ejecutó el mismo banco en macOS arm64 (Python 3.9.6) y Linux x86_64 (Python 3.12.3). En cada host: 84 evaluaciones de variantes dentro de un proceso, 27 baselines, 54 mutantes ordinarios y 3 calibraciones tiny RC; resultados `27 PASS`, `54 KILLED`, `3 SURVIVED`. Son dos ejecuciones pareadas de las mismas variantes, no 168 casos distintos. Las tres supervivencias tiny se conservaron como resultado; no se forzó su rechazo.

| Métrica | Resultado por host / comparación |
|---|---:|
| Casos/configuraciones baseline distintos | 27 |
| Evaluaciones de variante | 84 por host; 1 invocación del proceso por host |
| CSV v2 | 756 filas por host |
| Errores puntuales finitos recalculados / no finitos vacíos | 738 / 18 por host |
| Estados, parámetros y configuraciones iguales entre hosts | 84 de 84 |
| Valores finitos pareados / nulos pareados | 738 / 18 |
| Máxima diferencia normalizada entre hosts | `1.1102230246251565e-16` |
| Tolerancia fijada antes de ejecutar | `1e-6` |

Los 18 resultados no finitos pertenecen al mutante conocido `rhs_sign` de las tres configuraciones de consumo químico de segundo orden; fueron detectados después de que el baseline correspondiente pasó y se clasificaron como respuesta de mutación, no como fallo de infraestructura. El máximo error normalizado fino ODE fue `1.1215475770320893e-9` (logística sintética 01, 256 pasos). El máximo entre los modelos con resolución aplicable y N/A fue `7.629393805608231e-8` (Fechner 03, integral trapezoidal frente a logaritmo). Para Fechner, la cota de truncamiento trapezoidal indicada en el acta es solo bajo aritmética exacta (`6.357828776041666e-7`); excluye redondeo y no certifica un error total por intervalos. Los órdenes de refinamiento ODE observados (15 baselines, aprox. 3.960676–4.028201) son diagnósticos, no cotas.

Los resultados íntegros y resúmenes de ejecución están en [`multidomain_mac/`](multidomain_mac/) y [`multidomain_war/`](multidomain_war/). Cada resumen incluye los hashes de sus 84 JSON y CSV; sus SHA-256 externos son, respectivamente, `d45fe458dd10c1c5053cb7ba49796b84a2fd178e7627b46fa74c5e71eb95e0ec` y `867ce78201e211a587dcec4a6c89900963d54b92b6b5f6d78a73c52f84954b17`. Las ventanas UTC fueron `21:17:20.994955Z–21:17:21.037904Z` y `21:17:32.313714Z–21:17:32.336451Z` del 20 de octubre de 2026. Un verificador local, solo de lectura y basado en Python estándar, está en [`verify_evidence.py`](verify_evidence.py); desde la raíz del checkout se ejecuta `python3 evidence/new_validation/verify_evidence.py`.

Historial de exportación: la campaña v1 se conserva fuera del paquete publicable. Sus JSON, parámetros y clasificaciones coincidían con v2 en las 84 variantes por host, pero su CSV omitía 36 valores acústicos (720 filas frente a 756). V2 corrigió únicamente el exportador: etiqueta las presiones reflejada/transmitida y añade errores puntuales y máximos separados. SUT, oráculos, parámetros y tolerancias no cambiaron. Las cuatro posiciones de observación acústica repiten el mismo par estático; no son cuatro experimentos ni ocho componentes independientes.

## Control de kernels

El fixture reproducible está en [`kernel_fixture_v2/`](kernel_fixture_v2/): baseline y mutante NDJSON v2, la fuente Lean y el harness de replay. En los dos exportes, el único cambio semántico es `target.thm.value` (`target.type` y dependencias `target.all` permanecen iguales). La baseline `0 = 0 := rfl` fue aceptada y el valor mutado, de tipo incompatible `True`, fue rechazado.

- Lean default kernel replay: baseline ACCEPT (rc 0); mutante rechazado por incompatibilidad de tipo (rc 2), diagnóstico esperado `True` frente a `@Eq Nat 0 0`.
- nanoda: baseline ACCEPT (rc 0, “Checked 18 declarations with no errors”); mutante rechazado durante la comprobación de tipos (rc 101, assertion `self.def_eq(u, v)`). En nanoda la categoría se deriva del código fuente fijado, porque el binario no ofrece una categoría estructurada para ese rechazo.

Los manifiestos de archivos públicos y resúmenes derivados están en [`kernel01/`](kernel01/), [`kernel02/`](kernel02/) y [`kernel_controls_derived.json`](kernel_controls_derived.json). Los hashes de bundles completos privados (`kernel01`: `8110f582c2af81c405824d6ebbb44a0314cad5b22c87e1c5ee5cf8a08e0222b2`; `kernel02`: `5e575e3a3a817cf4c0cb8a83ef20fe890e9a6adb082a7b0875aacfca3ccd7a91`) no son hashes de los manifiestos públicos. Intentos de desarrollo no acreditados —mutación v1 rechazada por el parser, harness Lean inicial no compilable y primer baseline nanoda con error de pretty-printer— se mantienen descritos en el resumen derivado y no cuentan como evidencia de kernel.

El alcance es un fixture mínimo y una mutación de un único valor de prueba. No establece corrección universal de Lean o nanoda ni prueba ningún teorema Navier–Stokes/Euler.

## Control positivo periódico

[`periodic05/`](periodic05/) conserva la fuente compilada, salida saneada, duración, código de retorno y manifiesto. Lean terminó con rc 0; el hash de fuente es `907c81c5b301e7745cf92a8bc74c7f16bbc9b2c83a85b521da2b51331defa51d`. La construcción usa velocidad constante explícita `c ≠ 0`, presión y fuerza cero, viscosidad 1, sobre el dominio periódico (toro). `#print axioms` reportó `[propext, Classical.choice, Quot.sound]`; no se reportó `sorryAx` para el control. El bundle privado completo tiene SHA-256 `295508f4480f78f00d5341dfee83f0948117768b8aee0f03fdd21ebdd2726cfa`; el manifiesto público se verifica por separado. El resumen es [`periodic_positive_derived.json`](periodic_positive_derived.json).

Esta constante no nula no tiene energía finita en ℝ³. El control no cierra EU-06 y no establece regularidad o blow-up de Euler.

## Construcción limpia y límites operativos

Clean01 produjo un falso PASS del launcher: WSL terminó el proceso antes del build, aunque el resumen confundió la fase preflight con éxito. Clean02 quedó `INFRA_INCONCLUSIVE` tras detectar un socket heredado; no se relajó el guard. En clean03, sobre el commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, `lake --no-cache build` terminó con código 0 y `Build completed successfully (11424 jobs).` La fase fue `complete`; el build duró 2448,86 s y el wrapper 2496 s. Se reutilizaron dependencias y caché del toolchain; no fue un bootstrap de cero. El preflight registró `CapEff=0`, `NoNewPrivs=1`, `Seccomp=2`, ambos tipos de socket denegados por `EPERM` y cero sockets heredados. Esto es evidencia de un build limpio de fuentes con dependencias existentes, no validación de teoremas ni prueba de sandbox hermética.

La salida pública saneada, sin logs raw, está en [`clean_build03/`](clean_build03/); `public_manifest.sha256` fija los artefactos. Su inventario contiene 2669 entradas y el digest registrado es `95bb21c93e834581e1400e31e33a9fb7943db2f64f11425b034f97b9b52e95fc`. El verificador de solo lectura comprueba el manifiesto, fase, códigos 0, mensaje final, conteo de jobs y correspondencia del inventario. Los lanzamientos clean01/02 no se reescriben. El resultado de Comparator que se está reejecutando en el workspace de clean03 continúa `PENDING` hasta evidencia final separada.

## Créditos y alcance de autoría

La declaración aprobada de atribución y contribuciones está en [`PROCEDENCIA_IA_Y_APORTES.md`](../../PROCEDENCIA_IA_Y_APORTES.md): Cristian Guerra (criguex), QA Automation, autor responsable del estudio; herramientas de IA, asistencia. La tabla de correspondencia documental Clay–Lean y sus puentes pendientes está en [`docs/TABLA_FIDELIDAD_CLAY_LEAN.md`](../../docs/TABLA_FIDELIDAD_CLAY_LEAN.md). Esta evidencia acotada no es una equivalencia formal ni una revisión matemática humana.

## Fuentes, reproducibilidad y límites generales

Las fuentes físicas y matemáticas de referencia están enlazadas en el README del instrumento: [OpenStax RC](https://openstax.org/books/university-physics-volume-2/pages/10-5-rc-circuits), [IUPAC Beer–Lambert](https://goldbook.iupac.org/terms/view/B00626), [OpenStax óptica](https://openstax.org/books/physics/pages/16-key-equations), [lente delgada](https://openstax.org/books/university-physics-volume-3/pages/2-4-thin-lenses), [ley de velocidad de segundo orden](https://openstax.org/books/chemistry-2e/pages/12-4-integrated-rate-laws), [MIT OCW acústica](https://live.ocw.mit.edu/courses/6-013-electromagnetics-and-applications-spring-2009/d3be4ea78b036a6362230fb41780cf54_MIT6_013S09_notes.pdf) y [discusión sobre Fechner](https://arxiv.org/abs/2009.00923). Son referencias de ecuaciones, no datos experimentales de esta batería.

Todo aquí es un control de reproducción/QA acotado. No se modificaron teoremas fuente del proyecto, no se presenta validación empírica, no se agregan las corridas pareadas como casos independientes y no se extrapolan los resultados a una prueba matemática general.
