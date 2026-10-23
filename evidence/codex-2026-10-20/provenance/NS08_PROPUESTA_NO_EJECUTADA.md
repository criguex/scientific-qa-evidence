# NS-08: propuesta de comprobación adicional

**PROPUESTA NO EJECUTADA.** No modifica el estado `SKIPPED` del comparador y nanoda en la evidencia original. Debe ejecutarse solo tras revisar recursos, herramientas y alcance. No reutilizar el script completo con `RUN_COMPARATOR=1`: repetiría etapas y alteraría la copia del mutante.

## Objetivo y límite de confianza

Contrastar los desafíos de Navier–Stokes y Euler con sus soluciones y revalidar sus términos mediante Lean y nanoda. Usar los mismos axiomas permitidos; no desactivar el segundo kernel para convertir un fallo en éxito.

El checkout de WAR ya compiló la solución antes de preparar el sandbox. Sus hashes y estado limpio permiten una comprobación adicional reproducible, pero no acreditan un arranque adversarial limpio. La garantía más fuerte de Comparator presupone confianza en el desafío y sus dependencias, y no haber compilado previamente código potencialmente hostil en ese entorno. Para ese alcance habría que preparar un entorno nuevo. [README de Comparator fijado](https://github.com/leanprover/comparator/blob/19e111e2141cf333c7daff0f64c5f24acc91dd2e/README.md).

## Revisiones fijadas

| Componente | Commit que se debe verificar |
|---|---|
| Repositorio auditado | `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` |
| Comparator | `19e111e2141cf333c7daff0f64c5f24acc91dd2e` |
| lean4export | `cacf989bd75f608700820f6afc595f32e7a99a4d` |
| nanoda | `9d6964f78d0fa4c93fd22fe956e17afe7e72a441` |
| landrun | `ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a` |

Comparator y lean4export corresponden al manifiesto de dependencias auditado. Los otros commits son pines de la propuesta, no prueba de que esos binarios se hayan construido o ejecutado en WAR.

## Preparación y preflight

1. Elegir una carpeta nueva y explícita para herramientas y otra para resultados, fuera de la evidencia anterior. No borrar ni reemplazar logs existentes.
2. Verificar Go 1.24 o posterior, Rust reciente, enlazador C y `/usr/bin/time`. Registrar versiones y rutas. El [go.mod fijado de landrun](https://raw.githubusercontent.com/Zouuup/landrun/ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a/go.mod) declara Go 1.24.
3. Clonar nanoda y landrun en esas carpetas; seleccionar los commits indicados en modo detached y verificar `git rev-parse HEAD`. Construir nanoda con `cargo build --release --locked --bin nanoda_bin` y landrun con `go build -o landrun ./cmd/landrun`. Registrar stdout, stderr, exit code y hashes de binarios. [Fuente nanoda fijada](https://github.com/ammkrn/nanoda_lib/tree/9d6964f78d0fa4c93fd22fe956e17afe7e72a441), [fuente landrun fijada](https://github.com/Zouuup/landrun/tree/ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a).
4. No usar el comando antiguo `cargo install ... nanoda_bin`: `nanoda_bin` es el nombre del binario; el paquete es `nanoda_lib`. La construcción desde el checkout fijado evita esa ambigüedad.
5. En el repositorio auditado verificar commit, hashes, manifiesto y estado Git. Construir `lake build lean4export comparator` sin ejecutar `lake update`. Registrar el estado antes y después.
6. Verificar las rutas de los tres binarios y los JSON de desafío. Confirmar `enable_nanoda: true` y no ampliar `permitted_axioms`.
7. Probar landrun real bajo la misma restricción de sockets. No usar `fake-landrun`. El preflight comunicó WSL Ubuntu 24.04, usuario `nse`, kernel 6.18 y Landlock ABI 7; volver a medirlo al ejecutar. Ese número no certifica por sí solo el sandbox.

## Invocación propuesta

`RUTA_TOOLS` es un marcador: reemplazarlo por la carpeta nueva validada antes de copiar el comando. Registrar la invocación exacta, sin secretos. Ejecutar NS y Euler secuencialmente:

```sh
systemd-run --user --wait --pipe --collect \
  --property=RestrictAddressFamilies=~AF_UNIX \
  --working-directory=<WSL_HOME>/nse_audit_20261020/NavierStokesAndEuler \
  -E PATH=<WSL_HOME>/.elan/bin:/usr/bin:/bin \
  -E COMPARATOR_LANDRUN=RUTA_TOOLS/landrun/landrun \
  -E COMPARATOR_LEAN4EXPORT=<WSL_HOME>/nse_audit_20261020/NavierStokesAndEuler/.lake/packages/lean4export/.lake/build/bin/lean4export \
  -E COMPARATOR_NANODA=RUTA_TOOLS/nanoda/target/release/nanoda_bin \
  /usr/bin/time -v \
  <WSL_HOME>/.elan/bin/lake env \
  <WSL_HOME>/nse_audit_20261020/NavierStokesAndEuler/.lake/packages/Comparator/.lake/build/bin/comparator \
  ComparatorChallenges/NavierStokes.json
```

Después, si la primera ejecución termina y se conserva su evidencia, repetir cambiando únicamente el último argumento por `ComparatorChallenges/Euler.json`. Registrar UTC de inicio y fin, duración monotónica, pico de RSS, código de salida y logs separados. No lanzar ambos en paralelo ni estimar su coste con los 39 minutos del build anterior: es otra tarea y todavía no se ha medido.

## Aceptación y contingencia

Para cada desafío se requiere salida cero, registro de aceptación por nanoda y Lean y confirmación final del comparador. Inspeccionar el log completo, no solo buscar una frase. Un error de instalación, sandbox, memoria o exportación no es una refutación matemática.

Si falla el preflight o la comprobación, conservar todo y registrar el punto de fallo como infraestructura, rechazo del contrato o resultado inconcluyente según la evidencia. No ampliar privilegios, axiomas ni alcance automáticamente. Volver al estado anterior significa detener la tarea y dejar intacta la evidencia original; esta propuesta no necesita borrar ni restaurar archivos.

Un resultado satisfactorio reforzaría la verificación de términos y declaraciones. No decidiría por sí solo la fidelidad del enunciado a una intención externa, la procedencia del desafío de Euler ni las brechas EU-06 y NS-09 descritas en [el plan V2](../scenarios-v2/PLAN_VALIDACION_V2.md).
