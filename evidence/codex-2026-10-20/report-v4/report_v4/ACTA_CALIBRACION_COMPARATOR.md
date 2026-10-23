# Acta de calibración acotada de respuestas de Comparator

Fecha: 2026-10-20 (UTC). Esta calibración es posterior a la verificación de los desafíos y al corte del epílogo narrado (19:25:32 UTC). No modifica las pruebas aceptadas en el acta [poscorte](ACTA_VERIFICACION_FORMAL_POSCORTE.md) ni su narración.

## Alcance y resultados

Se ejecutaron tres casos pequeños con Comparator y las mismas herramientas fijadas que en la corrida formal. El caso positivo comprobó una solución válida; los dos casos negativos comprobaron controles de entrada de Comparator. Los resultados observados coincidieron con el resultado esperado en esos tres casos:

| Caso | Resultado observado | Capa que respondió | Tiempo GNU | Interpretación |
| --- | --- | --- | ---: | --- |
| Prueba válida | Comparator informó `Your solution is okay!`; nanoda y el kernel predeterminado de Lean aceptaron; código 0 | Ambos kernels | 2,82 s | Aceptación positiva del fixture configurado |
| Enunciados distintos | Rechazo con `Challenge and solution theorem statement do not match: 'target'`; código 1 | Comparator, etapa `compareAt`, antes de los kernels | 1,44 s | Detección del desacuerdo del fixture; no es rechazo de un kernel |
| Axioma no permitido | Rechazo con `Illegal axiom detected: 'forbidden'`; código 1 | Comparator, revisión de axiomas, antes de los kernels | 1,49 s | Detección del axioma prohibido del fixture; no es rechazo de un kernel |

Esto demuestra únicamente que la ruta configurada produjo las respuestas esperadas para estos tres fixtures. No demuestra ausencia general de falsos positivos, no prueba que los kernels rechacen cualquier prueba inválida y no constituye revisión matemática independiente. Los dos negativos terminaron antes de invocar nanoda o Lean.

## Historial de intentos

- Intento 1: el preflight de elan falló porque no había toolchain predeterminado; no se ejecutó ningún caso Comparator.
- Intento 2: el caso positivo fue aceptado por ambos kernels, pero el launcher se detuvo antes de los negativos al exigir la propiedad inexistente `RestrictAddressFamiliesAllowList`. Se conserva como resultado positivo parcial, no como calibración completa.
- Intento 3: launcher revisado, tres casos ejecutados en serie en un directorio de trabajo nuevo. Inicio registrado `2026-10-20T19:57:51Z`; fin `2026-10-20T19:57:57Z` (duraciones individuales de Comparator en la tabla; el intervalo del launcher no es tiempo de cálculo agregado).

## Procedencia y controles de ejecución

- Checkout formal ya compilado: commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`.
- Comparator `19e111e2141cf333c7daff0f64c5f24acc91dd2e`; Lean4export `cacf989bd75f608700820f6afc595f32e7a99a4d`; nanoda `9d6964f78d0fa4c93fd22fe956e17afe7e72a441`; Landrun `ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a`.
- Landrun de la versión fijada exige ABI 10 por defecto; el host ofrece Landlock ABI 7. Se utilizó `--best-effort` upstream y controles externos systemd/seccomp. Esto no acredita ABI 10 ni una sandbox completa.
- El perfil activo se inspeccionó por valores: `NoNewPrivileges=yes`, `CapEff=0`, `Seccomp=2`, sin descriptores de socket heredados, denegación seccomp de operaciones de red/socketpair y tres syscalls io_uring, `EPERM=1`, límite de memoria de 27 GiB y límite de CPU del 800 %. No debe extrapolarse a otros perfiles o máquinas.
- No fue un arranque adversarial limpio: se reutilizó el checkout precompilado y binarios fijados. Los controles no prueban la cadena completa desde una máquina vacía.

## Artefactos

El bundle operativo incluye los tres intentos, fixtures, lanzadores, resultados por caso, estado y propiedades de la unidad, tiempos, logs, hashes por archivo, pins y versiones. No contiene los binarios de toolchain, cachés `.lake` ni directorios `.git`.

- [Bundle de calibración](COMPARATOR_CALIBRATION_BUNDLE.tar.gz), SHA-256 `6a5a56631a0e82dbb91791ac8b640596656d1cea283aaca3f470356d676d117e`.
- SHA-256 del conjunto de resultados del intento 3, valor registrado en su manifiesto: `b973ebee4152fff9a7442223834ba20d6e896b6c9b2a208a2e94942924a5f8e0`.
- El README y los manifiestos internos del bundle preservan los hashes de lanzadores, fuentes, binarios, archivos de salida y cada resultado.

## Relación con las pruebas formales y pendientes

### Extensión posterior: tres fixtures adicionales

El 2026-10-20 entre 20:06:16 y 20:06:22 UTC se ejecutó una extensión separada con el mismo checkout, herramientas fijadas y perfil endurecido. Un control de renombrado alfa fue aceptado por nanoda y Lean (3,16 s; código 0). Un axioma oculto bajo un lema fue rechazado en `checkAxioms` por Comparator (1,52 s; código 1), y debilitar `∃ n > 0` a `n ≥ 0` con testigo cero fue rechazado en la comparación de enunciados (1,45 s; código 1). En ambos negativos hubo builds y exports antes del rechazo, pero no se invocaron los kernels.

| Fixture adicional | Resultado observado | Capa | Tiempo GNU | Interpretación |
| --- | --- | --- | ---: | --- |
| Renombrado alfa | Aceptado por nanoda y Lean; código 0 | Ambos kernels | 3,16 s | El cambio de nombres ligado no alteró este fixture válido |
| Axioma oculto | `Illegal axiom detected: 'forbidden'`; código 1 | `checkAxioms` de Comparator, antes de kernels | 1,52 s | Rechazo del axioma en este fixture |
| Condición debilitada | `Challenge and solution theorem statement do not match: 'target'`; código 1 | Comparación de enunciados de Comparator, antes de kernels | 1,45 s | Rechazo del cambio de contrato con testigo cero |

Sumando ambas tandas hay seis controles: dos positivos aceptados por ambos kernels y cuatro rechazos de Comparator anteriores a los kernels. Esta suma describe únicamente los fixtures enumerados; no es una tasa de falsos positivos, ni una puntuación general de seguridad, ni se suma a los cuatro teoremas formales o a las 150 ejecuciones numéricas.

El [bundle de extensión](COMPARATOR_CALIBRATION_EXTENSION_BUNDLE.tar.gz) preserva salidas, estados, perfiles activos y hashes de la segunda tanda. SHA-256: `ccbe70b9418a11c3198800d26b79395412665ff2cd16ffff58d9009c7cb58e4f`. Su archivo de resultados crudos exportados de WSL tiene SHA-256 `7367f7dbbeef93287b21e4e7db0efb02fd3b202b302c8e444440f97cbb1dff89`.

La segunda tanda tampoco fue un arranque adversarial limpio: se reutilizaron el checkout y las herramientas fijadas. No establece cero falsos positivos fuera de los seis fixtures. El bundle separa esa extensión de los intentos 1–3 de la primera tanda.

La aceptación formal previa cubre los cuatro teoremas configurados para los desafíos de Navier–Stokes y Euler en ese checkout, con los tres axiomas autorizados, como se detalla en el [acta poscorte](ACTA_VERIFICACION_FORMAL_POSCORTE.md). Esta calibración no amplía el enunciado ni cambia esa evidencia. En particular, no es el control positivo global no nulo de Euler y no resuelve NS-09.

Continúan pendientes el control positivo global no nulo de Euler, refinamiento espacial adicional y estudio de convergencia, revisión matemática humana y un arranque clean/adversarial. Las simulaciones numéricas no constituyen demostraciones de explosión ni resuelven el problema del Milenio. Seis respuestas esperadas no son una garantía universal.

El epílogo del video conserva el corte previo de las 19:25:32 UTC; esta acta registra una actualización posterior y no se incorporó a su audio.
