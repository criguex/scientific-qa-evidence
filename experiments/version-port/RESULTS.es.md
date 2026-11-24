> Traducción al español de [RESULTS.md](RESULTS.md). Si hay alguna diferencia, vale el original.

# Port de versión: resultados

**Estado: borrador.** Plan: [`PLAN.md`](PLAN.md), registrado antes de cualquier corrida y sin editar. Corrido el 2026-11-24 (UTC).

- **R0 · v4.34.0-rc2: completo.** Todas las revisiones dieron lo registrado, incluido lean4lean, el tercer kernel.
- **R1 · v4.34.0 y R2 · v4.35.0: la compilación falla** en el código de las pruebas de OpenAI, no en los enunciados. Los enunciados de los dos retos siguen compilando sin cambios. No se editó ninguna prueba, así que los pasos 5–10 no corrieron para R1 ni R2. Por decisión del autor, ahora se está intentando portar las pruebas sin límite de tiempo, bajo la [Enmienda 1](PLAN.es.md) del plan; sus resultados se agregarán aquí como una actualización con fecha.

Cada número de abajo sale de un archivo de esta carpeta. [`R0/`](R0/), [`R1/`](R1/), [`R2/`](R2/) y [`tools/`](tools/) guardan los recibos y los logs. Cada paso tiene una línea en `receipts/steps.tsv` (comando, directorio de trabajo, inicio y fin UTC, código de salida, SHA-256 y tamaño de su log) y un recibo de GNU `time -v`. Cada veredicto tiene una línea en `receipts/checks.tsv`, esperado contra obtenido. Cada carpeta tiene un `PROVENANCE.tsv` que da, para cada archivo, el SHA-256 del original en el equipo y el de la copia publicada. Las copias difieren de los originales solo donde se reemplazaron rutas del equipo por `<path>` o el nombre del equipo por `<host>`, y en los tres extractos de logs de compilación descritos en R1 y R2. Antes de publicar, cada original se comprobó contra una lista SHA-256 hecha en el equipo. Los scripts que manejaron las corridas están en [`scripts/`](scripts/).

Equipo: el equipo Linux de pruebas del autor (WSL2, Ubuntu 24.04.5, kernel 6.18.33.2-microsoft-standard-WSL2, 12 vCPU, 30 GiB), corrido como root y con asistencia de IA. Esto no es una reproducción independiente y no cambia AC-5.4.

## Resumen

| Paso | R0 · v4.34.0-rc2 | R1 · v4.34.0 | R2 · v4.35.0 |
| --- | --- | --- | --- |
| 1 Clon limpio, manifiesto de contenido `95bb21c9…52e95fc` | como se esperaba | como se esperaba | como se esperaba |
| 2 Versiones | rc2, Mathlib `85e3a25`, Comparator `19e111e` | v4.34.0, Mathlib `5ed2965`, Comparator `d03acab`, como se registró | v4.35.0, Mathlib `56a0058`, Comparator `e3dcf30`, como se registró |
| 3 Enunciados idénticos a `f9e8bc5` | sí | sí | sí |
| 4 Compilación | exit 0 | **exit 1**: fallan 15 módulos, 103 errores | **exit 1**: fallan 20 módulos, 121 errores |
| 5 Axiomas de los 4 teoremas finales | solo los estándar | no corrió | no corrió |
| 6 Comparator, nanoda + kernel de Lean | ambas aceptadas | no corrió | no corrió |
| 7 leanchecker --fresh | ambas exit 0 | no corrió | no corrió |
| 8 lean4lean --fresh | ambas exit 0 | no corrió | no corrió |
| 9 Mutantes | 6 de 6 rechazados, control aceptado | no corrió | no corrió |
| 10 Puentes | 35 de 35 teoremas, solo axiomas estándar | no corrió | no corrió |

**Ningún verificador rechazó ninguna de las dos soluciones en ninguna corrida.**

**AC-2.4 puede pasar a sí.** lean4lean `0048ed7`, **recompilado sobre Lean v4.34.0-rc2** (su toolchain upstream es v4.34.0), reprodujo los dos módulos de solución en entornos nuevos y terminó con exit 0. `NavierStokes.ComparatorSolution`: `checked 806768 declarations`. `Euler.Solution`: `checked 788326 declarations`. Como pide el plan, queda la nota de que este binario de lean4lean no se compiló con su toolchain upstream. En sus toolchains nativos (R1, R2) no se pudo correr, porque ahí las pruebas no compilan.

## Herramientas

Compiladas en el equipo para este experimento ([`tools/receipts/tools.tsv`](tools/receipts/tools.tsv), logs de compilación en [`tools/logs/`](tools/logs/)).

| Herramienta | Revisión | SHA-256 | Nota |
| --- | --- | --- | --- |
| comparator (v4.34.0-rc2) | `19e111e` | `514de8d2acbd6e0102575cd2c575e336b7c4a40daf3ae66abe97cef5e1e6b02a` | idéntico al binario de la auditoría principal; el ejecutable que Lake compiló dentro de R0 tiene el mismo hash ([recibo](R0/receipts/comparator_exe.txt)) |
| lean4export (v4.34.0-rc2) | `cacf989` | `4fa9e14cada304109e85da5048bcd411cf781a03539b3e50953e5c537074bd9e` | idéntico al binario de la auditoría principal |
| comparator (v4.34.0) | `d03acab` | `8efd5e1532b5e47d5ed5ead9ea42483068fbba81ad76e486ff8d2dbcf76e00f2` | compilado, no usado (R1 no compiló) |
| lean4export (v4.34.0) | `076e8e5` | `cbf95bb18e3fc19bbe39ad2a250d9cfce4ca01315b2acf8f630d1e315498bf60` | revisión que fija Comparator v4.34.0; no usado |
| comparator (v4.35.0) | `e3dcf30` | `3300f5a725ae8dcbfb88b3eb0c605c5737ec8e02bc3033f80665a182d997b023` | compilado, no usado (R2 no compiló) |
| lean4export (v4.35.0) | `5a9a355` | `87f4fe988dfe97a2a607cf38a8777a625b482f833985c16dbc1ddafa525f4bba` | revisión que fija Comparator v4.35.0; no usado |
| nanoda_bin | `0da9f98` | `23fe7e2e1f904021eed2cf1bd74bbeb5c18d693d6a1d3ba9c21f60d41b3229f8` | más nuevo que el `9d6964f` de la auditoría, como se registró |
| landrun | `ec104f6` | `1c35440a6ceb32badfe51f392ae0489eb9da4b37c7e08d8c57b9bd803d803153` | misma revisión que la auditoría; binario distinto (Go 1.27.4) |
| lean4lean (R0) | `0048ed7`, compilado sobre rc2 | `176afe26174008221f0c00f07759c5c5c00739207025e37a57025558a72233ef` | compilado por un script aparte, `l4l.sh` ([log](R0/l4l_original/run.log)), 113 s |
| lean, lake, leanchecker (rc2) | `6a10ac8` | `e8baaa71…5d550`, `6f53827d…dd995d`, `ccef1bfe…6fcbe` | idénticos a la auditoría ([`R0/receipts/versions.txt`](R0/receipts/versions.txt)) |

Rust 1.100.0, Go 1.27.4.

**Aquí landrun corre en modo best-effort.** El kernel reporta Landlock ABI v7. landrun `ec104f6` pide v10 y no arranca sin `--best-effort`. Comparator siempre pasa `--best-effort`. Una prueba manual mostró que el sandbox sigue bloqueando escrituras fuera de las rutas permitidas: `touch` en `/etc` fue denegado y en `/tmp` fue permitido. Esa prueba se hizo a mano y no tiene log. El README de Comparator también supone un usuario sin privilegios y un envoltorio `systemd-run`; estas corridas usaron root y no usaron el envoltorio. Ninguno de los dos puntos cambia lo que aceptan los kernels. Los dos debilitan el sandbox, lo que solo importa ante soluciones adversarias.

## R0 · v4.34.0-rc2 (la versión auditada)

| # | Paso | Esperado | Obtenido | Log (SHA-256 del original) |
| --- | --- | --- | --- | --- |
| 1 | Clon limpio en `f9e8bc5`, manifiesto de contenido | `95bb21c9…52e95fc` | `95bb21c93e834581e1400e31e33a9fb7943db2f64f11425b034f97b9b52e95fc` | `logs/s1_manifest.log` (`b3f8a3b6…`) |
| 2 | Versiones | rc2, Mathlib `85e3a25`, Comparator `19e111e` | iguales | `receipts/manifest_revs.tsv` |
| 3 | Revisión de enunciados (`git diff` de `ComparatorChallenges/` y de los dos archivos de solución contra `f9e8bc5`) | vacío | vacío, exit 0; repetido después de compilar, vacío | `logs/s3_statements.log` (`81bff35b…`) |
| 4 | Compilación | exit 0 | exit 0, `Build completed successfully (11424 jobs)`, ver nota | `logs/s4_build.log` (`d1b23d12…`) |
| 5 | `#print axioms` de los 4 teoremas nombrados en las dos configuraciones de Comparator | solo axiomas estándar | 4 de 4: `[propext, Classical.choice, Quot.sound]` | `logs/s5_axioms.log` (`9541bf73…`) |
| 6 | Comparator · Navier–Stokes | okay, exit 0 | `nanoda kernel accepts the solution`, `Lean default kernel accepts the solution`, `Your solution is okay!`, exit 0, 7 min 20 s | `logs/s6_comparator_NavierStokes.log` (`86f19cfa…`) |
| 6 | Comparator · Euler | okay, exit 0 | las mismas tres líneas, exit 0, 12 min 14 s | `logs/s6_comparator_Euler.log` (`5f410965…`) |
| 7 | leanchecker --fresh · Navier–Stokes | exit 0 | exit 0, log vacío, 34 min 36 s, 10,8 GB de memoria máxima | `logs/s7_leanchecker_NavierStokes.ComparatorSolution.log` (vacío) |
| 7 | leanchecker --fresh · Euler | exit 0 | exit 0, log vacío, 50 min 34 s, 10,7 GB de memoria máxima | `logs/s7_leanchecker_Euler.Solution.log` (vacío) |
| 8 | lean4lean --fresh · Navier–Stokes | exit 0 | exit 0, `checked 806768 declarations`, 1.459 s | `l4l_original/NavierStokes.ComparatorSolution.log` (`44a5967c…`) |
| 8 | lean4lean --fresh · Euler | exit 0 | exit 0, `checked 788326 declarations`, 29 min 44 s | `logs/s8_lean4lean_Euler.Solution.log` (`ce143b05…`) |
| 9 | Control: cambio solo en un comentario | aceptado | aceptado, exit 0 | `logs/s9_mutant_control_comment.log` |
| 9 | 6 mutantes de enunciado | rechazados | 6 de 6 rechazados, exit 1, cada uno con `Challenge and solution theorem statement do not match` y el nombre del teorema modificado; entre 1 min 44 s y 1 min 57 s cada uno | `logs/s9_mutant_*.log` |
| 10 | Puentes: compilar `ClayLiteral` y `Bridges`, `#print axioms` | exit 0, axiomas estándar | exit 0 las tres veces; 35 de 35 teoremas (34 de `Bridges` y `ClayLiteral.altD_withoutErratum_imp_withErratum`) `[propext, Classical.choice, Quot.sound]` | `logs/s10_bridge_axioms.log` (`51c2f814…`) |

**Los logs de Comparator son idénticos byte a byte a los de la auditoría.** Los dos logs del paso 6 tienen el mismo SHA-256 que la salida estándar de las corridas 2, 3 y 4 de Comparator en [`PROVENANCE.md`](../../evidence/formal/cd-validation/PROVENANCE.md) (`86f19cfa…`, `5f410965…`).

**Nota sobre la compilación.** El paso 4 de R0 es la compilación que hizo una corrida de instalación aparte, en otra carpeta del mismo equipo: `lake exe cache get`, 353 s, y luego `lake build`, 1.610 s, exit 0 ([`receipts/original_build_pasos.tsv`](R0/receipts/original_build_pasos.tsv)). Esa corrida no guardó un log propio. Su directorio `.lake` se copió al clon limpio de R0. Ahí `lake build` tardó 12 s, terminó con `Build completed successfully (11424 jobs)` y compiló 0 módulos. Se usó el caché de Mathlib, como se registró.

**Nota sobre el paso 8.** lean4lean en R0 lo corrió `l4l.sh`, no el controlador de este experimento. Revisó el módulo de Navier–Stokes en la carpeta de la compilación original y lo mataron mientras revisaba Euler (ver [Incidentes](#incidentes)). Solo se repitió la mitad de Euler, con el mismo binario, en la copia de esa compilación que tiene R0 ([`run/l4l_R0_euler.log`](R0/run/l4l_R0_euler.log)). El log de `l4l.sh` es [`l4l_original/run.log`](R0/l4l_original/run.log). Su `Euler.Solution.log` vacío es el log del intento que se mató.

**Nota sobre el paso 9.** El primer intento del mutante `domain_R3_to_periodic_data` no corrió, porque el diff publicado no aplica (ver [Hallazgos](#hallazgos-sobre-la-evidencia-publicada)). `checks.tsv` conserva esa línea como `UNEXPECTED`. Después el mutante se corrió con el diff restaurado y fue rechazado, como se esperaba. El control se corrió dos veces, antes y después del apagado de WSL, y fue aceptado las dos veces.

## R1 y R2: la compilación falla

| | R1 · v4.34.0 | R2 · v4.35.0 |
| --- | --- | --- |
| `lake update` | exit 0, 5 min 18 s | exit 0, 1 min 0 s |
| `lake exe cache get` | exit 0 | exit 0 |
| `lake build` | **exit 1** | **exit 1** |
| Módulos que fallaron | 15 (12 de NavierStokes, 3 de Euler) | 20 (17 de NavierStokes, 3 de Euler) |
| Mensajes de error | 103 | 121 |
| Módulos del proyecto con `.olean` al terminar, de 2.655 | 403 | 369 |
| `ComparatorChallenges.NavierStokes`, `ComparatorChallenges.Euler` | compilaron, solo con las advertencias de `sorry` esperadas | compilaron, solo con las advertencias de `sorry` esperadas |
| `NavierStokes.ComparatorSolution`, `Euler.Solution` | no compilaron (bloqueados) | no compilaron (bloqueados) |

Logs: [`R1/logs/s4_build.errors.log`](R1/logs/s4_build.errors.log) y [`R2/logs/s4_build.errors.log`](R2/logs/s4_build.errors.log). Son extractos: cada uno conserva todos los módulos que fallaron (`✖`) con sus bloques de error y el resumen final, y quita las líneas de comando del compilador y las de los módulos que compilaron. El encabezado de cada extracto da el tamaño y el SHA-256 del original completo. Cambios de versiones: [`R1/diffs/versions.diff`](R1/diffs/versions.diff), [`R2/diffs/versions.diff`](R2/diffs/versions.diff).

**Los enunciados sobreviven al cambio de versión; las pruebas no.** Los dos archivos de retos compilan sin cambios en v4.34.0 y en v4.35.0. O sea que el port no falla por un enunciado, que habría sido la falla que cuenta según el plan. Falla por pruebas, que el plan permite editar. No se editó ninguna prueba.

Errores por archivo (R1): `Euler/EulerProof.lean` 54, `NavierStokes/R3ConvolutionYoung.lean` 20, `R3/PairedKernelBound` 6, `R3/WeightedInterpolation` 5, `R3/LpNormTools` 4, `EdgeWeightJets` 4, `WeightedRadialPrimitive` 2, y uno en cada uno de `AppendixHeatResults`, `R3/ComparisonCutoffs`, `R3/H3Products`, `R3/ComparatorBridge`, `R3/PressureFunctionals`, `R3PressureFourier`, `Euler/GevreyComposition`, `Euler/GevreyGeneratingComposition`. R2 falla en los mismos 15 archivos, con 59 errores en `EulerProof`, y en cinco más: `SmoothCovariance`, `SquaredPartition`, `TerminalPressure`, `ModulatedStockBounds`, `HeatedOutgoing`.

Lo que muestran los mensajes, leído en los logs y sin arreglar nada:

- **Cambios en la API de L^p de Mathlib.** `eLpNorm_mono_ae`, `eLpNorm_add_le` y `eLpNorm_smul_le_mul_eLpNorm` ahora reciben primero un argumento `AEStronglyMeasurable`. `eLpNorm f p μ < ⊤` ahora se despliega como `WithTop.LT`, así que fallan los constructores anónimos `⟨…⟩` y las proyecciones `.1`/`.2` que se le aplican. Esto explica la mayoría de los errores en los archivos R3 de NavierStokes.
- **`failed to synthesize MulLeftMono ℝ`**: `AppendixHeatResults`, `Euler/GevreyComposition`.
- **`Finset.prod_le_prod`** cambió sus argumentos: `Euler/GevreyGeneratingComposition`.
- **Linters.** En `Euler/EulerProof.lean` parte de los errores son advertencias de linters (`unusedTactic`, `unnecessarySeqFocus`, `unusedSimpArgs`). Cuentan como errores porque la biblioteca `Euler` fija `warningAsError = true`. El resto de ese archivo son `rfl` que ya no cierran, metas sin resolver y tipos que no coinciden.

No se sabe cuánto trabajo necesitaría un arreglo. 2.252 (R1) y 2.286 (R2) módulos nunca corrieron, porque un módulo que falla bloquea a todos los que lo importan, y esos pueden tener más errores. Eso no es el "arreglo mínimo" que permitía el encargo, así que no se intentó en esta corrida. Después empezó un port completo bajo la Enmienda 1 del plan: cada edición se guarda como diff en `R1/port/` (y `R2/port/`), los cambios de enunciados internos se listan aparte y los pasos 3–10 correrán sobre el resultado.

## Hallazgos sobre la evidencia publicada

**Tres de los siete diffs de mutantes publicados no aplican tal como están publicados.** A `evidence/formal/cd-validation/mutants/domain_R3_to_periodic_data.diff`, `force_zero_R3.diff` y `force_zero_periodic.diff` les falta la última línea. Esa línea es una línea de contexto formada por un solo espacio: la línea en blanco después de `sorry`. Cada encabezado de hunk anuncia 7 líneas por lado y el archivo tiene solo 6, así que `git apply` se detiene con `corrupt patch at line 13` ([log del intento fallido](R0/run/target-R0.first.log)). La línea que falta, tal como la imprime `diff <publicado> <restaurado>`:

```
12a13
>  
```

Al agregar esa sola línea (un espacio y un salto de línea) se obtienen archivos cuyo SHA-256 es igual al SHA-256 original registrado en [`PROVENANCE.md`](../../evidence/formal/cd-validation/PROVENANCE.md):

| Diff | SHA-256 con la línea restaurada | SHA-256 original en PROVENANCE.md |
| --- | --- | --- |
| `domain_R3_to_periodic_data` | `63beb94d90c79fd543a1c645f4f7bd839e46247e69a1bb523ac93ef7339823f5` | igual |
| `force_zero_R3` | `2125f51c41c03dbf4d6d5dbc5aea80a9343e59eb1cc80895855d467a4e714709` | igual |
| `force_zero_periodic` | `43db52345f01c64c7b134888f109e83f3dc0ba0d374a42ae75c3a7135f96b343` | igual |

O sea que las corridas originales usaron diffs completos y la línea se perdió al hacer las copias públicas. Los archivos publicados no se tocaron. Las copias restauradas, con sus hashes, están en [`R0/diffs/`](R0/diffs/) (`*.restored.diff`, `SHA256SUMS`). Todas las corridas de mutantes que terminaron las usaron. Los otros cuatro diffs publicados ya coinciden con sus hashes originales ([`R0/receipts/mutant_inputs.sha256`](R0/receipts/mutant_inputs.sha256)).

## Incidentes

Registrados a medida que pasaron en [`R1/run/INCIDENT.txt`](R1/run/INCIDENT.txt).

- **Apagado de WSL, 01:27:56Z.** La máquina virtual de WSL se detuvo (`journalctl --list-boots`: el arranque terminó a las 20:27:56 −05:00). Un comando enviado en ese momento devolvió `Wsl/Service/0x8007274c`. Murieron todos los trabajos en segundo plano. Eso incluyó el controlador de R0, que corría el mutante `euler_tstar_half`, empezado a las 01:26:44Z; su log parcial se guarda como `s9_mutant_euler_tstar_half.interrupted.log`. También incluyó la corrida de lean4lean de R0 (Euler, empezada a las 01:21:29Z) y un primer intento de `domain_R3_to_periodic_data`. Los trabajos se relanzaron hacia las 01:38Z desde el paso 9 de R0, con una sesión inactiva abierta para mantener viva la VM. Los pasos interrumpidos no tienen código de salida. Cada uno se corrió de nuevo desde el principio.
- **Inicios de sesión rechazados y un segundo apagado.** Desde cerca de las 02:00Z, el servidor SSH del equipo rechazó inicios de sesión nuevos durante largos tramos (`kex_exchange_identification: banner line 0: Exceeded MaxStartups`). El controlador de R0 terminó a las 03:26:59Z. La compilación de R1 empezó a las 03:34:28Z. Su log se escribió por última vez a las 03:40:05Z, y nunca recibió un código de salida. El arranque de la VM terminó a las 05:57:59Z, según `journalctl`. Los inicios de sesión volvieron a funcionar a las 16:09Z. El log de la compilación interrumpida de R1 se guarda, como extracto, en `R1/logs/s4_build.interrupted.errors.log`. Ya mostraba 9 de los 15 módulos que fallan. Después la compilación de R1 se corrió de nuevo, continuando el `.lake` parcial (16:10:28Z → 16:13:46Z, exit 1). R2 corrió a continuación (16:17Z → 16:24Z).
- **Compilación de herramientas.** La primera compilación de landrun se colgó al descargar módulos de Go y se mató (exit 143). La primera compilación de nanoda falló porque no había un enlazador de C instalado (exit 101). Las dos se recompilaron en las mismas revisiones una vez corregida la causa. Los intentos fallidos quedan en `tools/receipts/steps.tsv`.

## Límites

El autor corrió cada paso en su propia máquina, con un asistente de IA que escribió y manejó los scripts. Se usó el caché de Mathlib, así que en estas corridas Mathlib no se compiló desde el código fuente. lean4lean en R0 se compiló con un toolchain distinto de su upstream. Un mutante rechazado solo dice que Comparator vio un enunciado distinto. R1 y R2 no dicen nada sobre si las pruebas son correctas. Muestran que el código de las pruebas de OpenAI, tal como se escribió para v4.34.0-rc2, no compila contra el Mathlib de versiones posteriores.
