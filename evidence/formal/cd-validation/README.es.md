> Traducción al español de [README.md](README.md). Si hay alguna diferencia, vale el original.

# Revalidación de las alternativas (C) y (D), 2026-10-21

Estado: **completo** · 18 de 18 comprobaciones registradas · 0 inesperadas · 1 no corrida (toolchain no coincide).

Este registro repite y extiende el [registro de Comparator del 2026-10-20](../comparator/README.md) para [NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler) de OpenAI en el commit `f9e8bc5` (leanprover/lean4:v4.34.0-rc2) en un equipo: Linux x86_64 · WSL2 · 12 vCPU · 30 GiB. Los resultados legibles por máquina están en [`results.json`](results.json); cada archivo público se rastrea hasta su original y el SHA-256 de ese original en [`PROVENANCE.md`](PROVENANCE.md).

## Resultados

| Comprobación | Compilación | Esperado | Veredicto | Transcurrido | Decisión de Comparator | Registros |
| --- | --- | --- | --- | ---: | --- | --- |
| Comparator corrida 2 · Navier–Stokes (C, D) | B2 | aceptar | **ACCEPTED** | 7.0 min | `Your solution is okay!` | [log](logs/comparator2_NavierStokes.sanitized.log) |
| Comparator corrida 2 · Euler | B2 | aceptar | **ACCEPTED** | 11.2 min | `Your solution is okay!` | [log](logs/comparator2_Euler.sanitized.log) |
| Comparator corrida 3 · Navier–Stokes en B3 | B3 | aceptar | **ACCEPTED** | 6.6 min | `Your solution is okay!` | [log](logs/comparator3_clean_NavierStokes.sanitized.log) |
| Comparator corrida 3 · Euler en B3 | B3 | aceptar | **ACCEPTED** | 11.2 min | `Your solution is okay!` | [log](logs/comparator3_clean_Euler.sanitized.log) |
| Comparator corrida 4 · Navier–Stokes en B4 | B4 | aceptar | **ACCEPTED** | 6.7 min | `Your solution is okay!` | [log](logs/comparator4_nocache_NavierStokes.sanitized.log) |
| Comparator corrida 4 · Euler en B4 | B4 | aceptar | **ACCEPTED** | 11.2 min | `Your solution is okay!` | [log](logs/comparator4_nocache_Euler.sanitized.log) |
| Control · edición solo en comentarios al desafío | B2 | aceptar | **CONTROL_ACCEPTED** | 7.0 min | `Your solution is okay!` | [log](logs/mutant_control_comment.sanitized.log) · [diff](mutants/control_comment.diff) |
| (C) agregar f = 0 · enunciado sin fuerza | B2 | rechazar | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'NavierStokes.Comparator.navier_stokes_breakdown_R3'` | [log](logs/mutant_force_zero_R3.sanitized.log) · [diff](mutants/force_zero_R3.diff) |
| (D) agregar f = 0 · enunciado sin fuerza | B2 | rechazar | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'NavierStokes.Comparator.navier_stokes_breakdown_periodic'` | [log](logs/mutant_force_zero_periodic.sanitized.log) · [diff](mutants/force_zero_periodic.diff) |
| (C) cambiar los datos de decaimiento en ℝ³ por datos periódicos | B2 | rechazar | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'NavierStokes.Comparator.navier_stokes_breakdown_R3'` | [log](logs/mutant_domain_R3_to_periodic_data.sanitized.log) · [diff](mutants/domain_R3_to_periodic_data.diff) |
| (C) debilitar nu > 0 a nu ≥ 0 | B2 | rechazar | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'NavierStokes.Comparator.navier_stokes_breakdown_R3'` | [log](logs/mutant_viscosity_nonneg_R3.sanitized.log) · [diff](mutants/viscosity_nonneg_R3.diff) |
| (D) quitar ¬ · existencia en vez de ruptura | B2 | rechazar | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'NavierStokes.Comparator.navier_stokes_breakdown_periodic'` | [log](logs/mutant_existence_not_breakdown_periodic.sanitized.log) · [diff](mutants/existence_not_breakdown_periodic.diff) |
| Euler · ajustar T* ≤ 1 a T* ≤ 1/2 | B2 | rechazar | **KILLED** | 1.4 min | `uncaught exception: Challenge and solution theorem statement do not match: 'Euler.exists_compact_smooth_euler_singularity'` | [log](logs/mutant_euler_tstar_half.sanitized.log) · [diff](mutants/euler_tstar_half.diff) |
| B3 · compilación nueva, Mathlib compilado localmente | B3 | ok | **OK** | 1 h 27 min | — | [log](logs/clean_build.excerpt.log) |
| B4 · compilación sin caché, todo compilado localmente | B4 | ok | **OK** | 1 h 29 min | — | [log](logs/nocache_build.excerpt.log) |
| leanchecker --fresh · solución de Navier–Stokes | B2 | ok | **OK** | 19.6 min | — | [log](logs/leanchecker_fresh_NavierStokes.ComparatorSolution.log) · [recibo](receipts/leanchecker_fresh_NavierStokes.ComparatorSolution.txt) |
| leanchecker --fresh · solución de Euler | B2 | ok | **OK** | 22.5 min | — | [log](logs/leanchecker_fresh_Euler.Solution.log) · [recibo](receipts/leanchecker_fresh_Euler.Solution.txt) |
| lean4lean --fresh · solución de Navier–Stokes (mejor esfuerzo) | B2 | ok | **FAILED_TOOLCHAIN_MISMATCH** | — | — | [log](logs/lean4lean_build.error-excerpt.log) · [recibo](receipts/lean4lean.txt) |

## Compilaciones usadas por cada corrida

Hay cuatro compilaciones distintas involucradas en este registro. Se diferencian en de dónde vinieron Mathlib y las dependencias más pequeñas, así que cada corrida está etiquetada con su compilación. Una quinta compilación, B5, se hizo después desde la fuente para la versión v1.3.0 y está registrada en [`../b5/`](../b5/README.md).

| Compilación | Comando | De dónde vinieron las bibliotecas compiladas | Usada por |
| --- | --- | --- | --- |
| **B1 · clean03 · 2026-10-20** | `lake --no-cache build` | compilado; el registro de clean03 indica que se reutilizaron las cachés de dependencias y de toolchain | Comparator corrida 1 (el registro del 2026-10-20) |
| **B2 · compilación de auditoría · 2026-10-20** | `lake exe cache get, then lake build` | caché de Mathlib precompilada descargada con `lake exe cache get` (8,747 archivos intentados) | Comparator corrida 2, mutantes del enunciado, leanchecker --fresh, lean4lean --fresh |
| **B3 · compilación nueva · 2026-10-21** | `XDG_CACHE_HOME=<dir vacío> MATHLIB_NO_CACHE_ON_UPDATE=1 lake build` | compilado localmente; 7 dependencias más pequeñas llegaron como barriles de Reservoir precompilados | Comparator corrida 3 |
| **B4 · compilación sin caché · 2026-10-21** | `XDG_CACHE_HOME=<dir vacío> MATHLIB_NO_CACHE_ON_UPDATE=1 lake --no-cache build` | todo compilado localmente (se le indicó a Lake que no descargara cachés de compilación) | Comparator corrida 4 |

## B3 · compilación nueva, 2026-10-21

- **Comando:** `XDG_CACHE_HOME=<dir vacío> MATHLIB_NO_CACHE_ON_UPDATE=1 lake build`, corrido en una extracción nueva del archivo fuente fijado `NavierStokesAndEuler-f9e8bc5…tar.gz` (SHA-256 `afd4d226…834b4b5`, verificado antes de extraerlo).
- **Inicio / fin (UTC):** 2026-10-21T15:35:41Z → 2026-10-21T17:02:23Z · 1 h 27 min · código de salida **0**.
- **Versiones:** Lean y Lake 4.34.0-rc2 (commit `6a10ac8`), Mathlib `85e3a25`, y todas las revisiones de dependencias en [el recibo de versiones](receipts/fresh_build_versions.txt).
- **Log:** [primeras 40 y últimas 15 líneas](logs/clean_build.excerpt.log). El original completo no se distribuye; su SHA-256 es `627f1474a9cf3ac698693aa295445574343239364b563a89975e4efbe8522011`.

### Qué significan los contadores

| Número | Qué cuenta | Cómo se obtuvo |
| ---: | --- | --- |
| 11,432 | El total de tareas de Lake, de la línea final `Build completed successfully (11432 jobs)`. Una tarea es cualquier paso de compilación de Lake, no solo un módulo compilado. | Última línea del log. |
| 11,030 | Líneas de progreso que Lake imprimió como `[n/N] Built X`: 8,371 para Mathlib, 1,840 para Euler, 817 para NavierStokes y 2 para ComparatorChallenges. | `grep -cE '\] Built ' build.log`, luego agrupado por el primer componente del nombre. |
| 8,371 | Archivos `.olean` bajo el directorio de compilación de Mathlib, uno por módulo compilado, incluida la raíz `Mathlib`. La cifra anterior de 8,370 solo contaba los submódulos `Built Mathlib.`. | `find … -name '*.olean' \| wc -l`, que coincide con las líneas de Mathlib impresas. |
| 402 | Tareas que Lake corrió sin imprimir una línea `Built`. Incluyen traer y desempaquetar los archivos de dependencias de abajo. La división exacta no se registró. | 11,432 − 11,030. |

### Verificación de la caché, y qué no se compiló localmente

- **Caché aislada:** `XDG_CACHE_HOME` apuntaba a un directorio creado vacío al inicio de la compilación; después tenía 0 archivos. Se fijó `MATHLIB_NO_CACHE_ON_UPDATE=1`, y nunca se corrió `lake exe cache get`. La caché de Mathlib más antigua del equipo, del 2026-10-20, no se modificó (archivo más reciente del 2026-10-20).
- **Lo que el log no mostró:** una búsqueda en el log de `fetched`, `unpack` o `downloading` devolvió 0. Esa búsqueda **no fue suficiente**. Lake trajo archivos precompilados (`build.barrel`) del registro de paquetes [Reservoir](https://reservoir.lean-lang.org) para siete dependencias sin imprimir esas tareas. Se encontraron después en `.lake/packages/*/.lake/`:

| Paquete | Bytes | SHA-256 del barril | Fuente |
| --- | ---: | --- | --- |
| LeanSearchClient | 1,110,298 | `3261fb4aeea5c924815272a52b398eb66c899e82b181c010d66dcf8b79fff67a` | `https://reservoir.lean-lang.org/api/v1/packages/leanprover-community/LeanSearchClient/barrel` |
| Qq | 4,671,641 | `b89ab157960dc0c10c9b6963fa230273d10b446276860421eb95fe396be59233` | `https://reservoir.lean-lang.org/api/v1/packages/leanprover-community/Qq/barrel` |
| aesop | 30,521,889 | `7f1e07f0fa8b63f54af124350c9b0504d28ef9f5c120cbe1745844b39b5910a7` | `https://reservoir.lean-lang.org/api/v1/packages/leanprover-community/aesop/barrel` |
| batteries | 99,850,446 | `694bf9ca49d5450f82419ff7034ecd90393d2a44c2e0e23bf776f29153bc53c5` | `https://reservoir.lean-lang.org/api/v1/packages/leanprover-community/batteries/barrel` |
| importGraph | 61,390,129 | `dc1fe957970c455d5b086106d6d3df34e106599b9ee170d6c510fd977e5dbc16` | `https://reservoir.lean-lang.org/api/v1/packages/leanprover-community/importGraph/barrel` |
| plausible | 3,010,777 | `8e3d14110256a72e960f1ad955f9f6465dda100b6ee636d10b0bf16777abb159` | `https://reservoir.lean-lang.org/api/v1/packages/leanprover-community/plausible/barrel` |
| proofwidgets | 10,715,826 | `8f0969afc70a21ae5714e3ec029cf1de88b71febadab957ff5d0306152a7db9f` | `https://reservoir.lean-lang.org/api/v1/packages/leanprover-community/proofwidgets/barrel` |

- **Las marcas de tiempo de los artefactos confirman la división.** Todo `.olean` de Mathlib y del proyecto de OpenAI es más reciente que el inicio de la compilación; todo `.olean` de los siete paquetes de barril es más antiguo, porque se empaquetó previamente en otro lugar.

| Paquete | archivos .olean | más antiguos que el inicio de la compilación |
| --- | ---: | ---: |
| LeanSearchClient | 4 | 4 |
| Qq | 14 | 14 |
| aesop | 132 | 132 |
| batteries | 191 | 191 |
| importGraph | 21 | 21 |
| mathlib | 8371 | 0 |
| plausible | 13 | 13 |
| proofwidgets | 24 | 24 |
| _project | 2659 | 0 |

Así que B3 compiló **11,030 módulos localmente** (Mathlib y el proyecto) y recibió **399 módulos de dependencias precompilados** desde Reservoir. No es un arranque completo desde cero; B4 lo repite con `--no-cache`.

## B4 · compilación sin caché, 2026-10-21

- **Comando:** `XDG_CACHE_HOME=<RUN>/nocache/xdg MATHLIB_NO_CACHE_ON_UPDATE=1 lake --no-cache build` en una extracción nueva del mismo archivo.
- **Inicio / fin (UTC):** 2026-10-21T17:45:04Z → 2026-10-21T19:14:27Z · 1 h 29 min (GNU `time`, [recibo](receipts/nocache_build.time.txt)) · código de salida **0** · 11424 tareas.
- **Descargas:** 0 archivos `build.barrel` en `.lake/packages`; 0 archivos en el directorio de caché vacío después.
- **Log:** [extracto](logs/nocache_build.excerpt.log), SHA-256 original `7afcff48807c0c231536bc825d6d338dd53390d6328677a8d1931b85dccd9668`. Versiones: [recibo](receipts/nocache_build_versions.txt).

| Paquete | archivos .olean | más antiguos que el inicio de la compilación |
| --- | ---: | ---: |
| LeanSearchClient | 4 | 0 |
| Qq | 14 | 0 |
| aesop | 132 | 0 |
| batteries | 190 | 0 |
| importGraph | 10 | 0 |
| mathlib | 8371 | 0 |
| plausible | 13 | 0 |
| proofwidgets | 13 | 0 |
| _project | 2659 | 0 |

## Recibos

### leanchecker --fresh (en B2)

leanchecker no imprime nada cuando se aceptan todas las declaraciones, así que ambos logs están vacíos. Se publican exactamente como se registraron, no rellenados.

| Módulo | Comando | Inicio (UTC) | Fin (UTC) | Exit | Transcurrido | Log |
| --- | --- | --- | --- | ---: | ---: | --- |
| `NavierStokes.ComparatorSolution` | `timeout 10h lake env leanchecker --fresh NavierStokes.ComparatorSolution` | 2026-10-21T14:53:37Z | 2026-10-21T15:13:12Z | 0 | 19.6 min | 0 bytes ([tal como se registró](logs/leanchecker_fresh_NavierStokes.ComparatorSolution.log)) |
| `Euler.Solution` | `timeout 10h lake env leanchecker --fresh Euler.Solution` | 2026-10-21T15:13:12Z | 2026-10-21T15:35:41Z | 0 | 22.5 min | 0 bytes ([tal como se registró](logs/leanchecker_fresh_Euler.Solution.log)) |

Ejecutable: `leanchecker` del toolchain de Lean 4.34.0-rc2, SHA-256 `ccef1bfe9bfeecea65137d94a69033c1a89f360711f50fa3178e7ba3e696fcbe`. Los recibos de GNU `time` con el RSS máximo están en [`receipts/`](receipts/).

### lean4lean (no corrido sobre las pruebas)

- **Versiones:** lean4lean commit `67f63b0c818920dfaed2ad07ccff187a6a8fe1e3`; su toolchain fijado es `leanprover/lean4:v4.33.0-rc2`, forzado a `leanprover/lean4:v4.34.0-rc2` para igualar las pruebas; Batteries `76e1c118b0700b4ceafe99532e887d6431625e1a` según lo resolvió `lake update`.
- **Comando:** `lake update && lake build (lean-toolchain set to leanprover/lean4:v4.34.0-rc2)` · 2026-10-21T17:20:09Z → 2026-10-21T17:20:36Z · código de salida **1**.
- **Error:** [extracto](logs/lean4lean_build.error-excerpt.log). Batteries no logró compilar bajo Lean 4.34 (`Tactic unfold failed to unfold cond` en `Batteries/Data/List/Basic.lean`). lean4lean en sí nunca se compiló, así que **nunca examinó las pruebas**. Esto es un vacío de herramientas, no un veredicto.

### Herramientas reutilizadas

Las compilaciones desde cero no recompilaron los verificadores. Estos binarios se reutilizaron en las corridas 2–4 de Comparator y en las corridas de mutantes (la corrida 1 está documentada en su propio registro):

| Herramienta | SHA-256 | Revisión |
| --- | --- | --- |
| comparator | `514de8d2acbd6e0102575cd2c575e336b7c4a40daf3ae66abe97cef5e1e6b02a` | 19e111e2141cf333c7daff0f64c5f24acc91dd2e |
| lean4export | `4fa9e14cada304109e85da5048bcd411cf781a03539b3e50953e5c537074bd9e` | cacf989bd75f608700820f6afc595f32e7a99a4d |
| nanoda_bin | `ccda52587ef42760dff9bc2de26edca0cb6ad207c8719cfffcd1e7daab22ccfb` | 9d6964f78d0fa4c93fd22fe956e17afe7e72a441 |
| landrun | `e3d26ebf2f7c786f8d34b7051ad2c655329aeadbb863404e3dd05d3a97b0518a` | ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a |
| leanchecker | `ccef1bfe9bfeecea65137d94a69033c1a89f360711f50fa3178e7ba3e696fcbe` | toolchain de Lean 4.34.0-rc2 |
| lean | `e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550` | toolchain de Lean 4.34.0-rc2 |
| lake | `6f53827dab18010d6c690d14c8401cacabc1db958edb3552a877ed4cf1dd995d` | toolchain de Lean 4.34.0-rc2 |

## Cómo leer los veredictos

- `ACCEPTED`: Comparator imprimió `Your solution is okay!` después de que tanto nanoda como el kernel de Lean aceptaron la solución.
- `KILLED`: Comparator rechazó un enunciado mutado; la columna de decisión cita su mensaje.
- `FAILED_TOOLCHAIN_MISMATCH`: el propio verificador no se pudo compilar para esta versión de Lean, así que nunca examinó las pruebas.
- `PENDING`: todavía no terminado.
- Un mutante eliminado no dice nada sobre si el enunciado mutado es verdadero o falso. Los mutantes `f = 0` no son evidencia sobre las alternativas sin fuerza (A) y (B).
