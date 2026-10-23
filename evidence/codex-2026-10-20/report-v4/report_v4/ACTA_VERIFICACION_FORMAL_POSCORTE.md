# Acta de verificación formal posterior al corte

Fecha de ejecución: 2026-10-20 (UTC). Esta acta añade resultados obtenidos
después del corte narrativo histórico de V4. El guion base congelado de las
once escenas permanece intacto; la revisión operacional de escena 08 es un
override separado para la versión de video actual. Esta acta tampoco reemplaza
el manifiesto del prerelease `v2026.10.20-informe-v4`.

## Resultado y alcance

Comparator aceptó los desafíos configurados de Navier–Stokes y Euler tanto con
nanoda como con el kernel de Lean. Ambos informaron `Your solution is okay!` y
terminaron con código 0. La verificación corresponde a las pruebas formales de
los enunciados configurados en el checkout indicado abajo; no es una
certificación externa ni verifica por sí sola que las fuentes científicas
representen todos los enunciados matemáticos deseados.

Los dos resultados enumeraron exactamente los axiomas permitidos:
`propext`, `Classical.choice` y `Quot.sound`. Las advertencias `sorry` pertenecen
a placeholders de los desafíos (`NavierStokes.lean:273,280` y
`Euler.lean:85,170`); no deben confundirse con axiomas adicionales declarados
por las soluciones.

| Desafío | Resultado | Tiempo GNU | Salida | Estado |
| --- | --- | ---: | --- | --- |
| Navier–Stokes, intento 2 | nanoda + Lean aceptan | 7:01.51 | `Your solution is okay!` | exit 0 |
| Euler | nanoda + Lean aceptan | 11:22.45 | `Your solution is okay!` | exit 0 |

El primer intento de Navier–Stokes se interrumpió al terminar la sesión del
user-manager. No tuvo status final ni EOF y no cuenta como aceptación o rechazo
matemático; queda documentado en el bundle operativo.

## Procedencia y condiciones

- Repositorio formal: `https://github.com/openai/NavierStokesAndEuler.git`.
- Commit exacto: `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`.
- Comparator: `19e111e2141cf333c7daff0f64c5f24acc91dd2e`.
- `lean4export`: `cacf989bd75f608700820f6afc595f32e7a99a4d`.
- nanoda: `9d6964f78d0fa4c93fd22fe956e17afe7e72a441`.
- Landrun: `ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a`.
- Comparator SHA-256: `514de8d2acbd6e0102575cd2c575e336b7c4a40daf3ae66abe97cef5e1e6b02a`.
- Checkout ya compilado; no fue un arranque limpio ni una revisión adversarial
  desde cero. El enunciado Euler fue adaptado por sus autores; Navier–Stokes
  incluye fuerza.
- El kernel ofrece Landlock ABI 7; la versión fijada de Landrun exige ABI 10
  por defecto y se usó
  `--best-effort` upstream junto con restricciones externas systemd/seccomp.
  Esto no equivale a probar ABI 10 ni una sandbox completa.

## Archivos de evidencia

Los logs terminales de cada ejecución se conservan sin modificar en
[`ns08_terminales/`](ns08_terminales/). El bundle operativo sanitizado contiene
los scripts, el intento NS interrumpido y registros de preflight/operación:
[`ns08_ops_bundle.tar.gz`](../../report-v4/report_v4/ns08_ops_bundle/), SHA-256
`5a29b7740ac7aa7b41811cc694a1775f0dc4eb514a841f938bedaed87a8bd6fb`.

SHA-256 de los terminales seleccionados:

| Archivo | SHA-256 |
| --- | --- |
| `ns08_terminales/ns-attempt2.stdout.log` | `86f19cfa0e008549d11147e7fe3ceefc5bfd317ffa4b0824eeb6e3327ec973bf` |
| `ns08_terminales/ns-attempt2.stderr.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `ns08_terminales/ns-attempt2.status.txt` | `bde294368bfed77c2cddf8cec271d398aee9cdbab3b26e1059281bd33adb0120` |
| `ns08_terminales/ns-attempt2.time.log` | `66129a4f5ca1c4d8914eee2c09488f0d767faf407c7ed9f834ae1d80c116264d` |
| `ns08_terminales/ns-attempt2.guard.log` | `09fbcde57bd459505dbf298fb0b2d2110cc9c70e85f4fbaf9f57429550cfd62d` |
| `ns08_terminales/euler.stdout.log` | `5f410965535ca08ed4cfca05bd9fb259ece2ef95858319a83134f92bc83b96ba` |
| `ns08_terminales/euler.stderr.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `ns08_terminales/euler.status.txt` | `bde294368bfed77c2cddf8cec271d398aee9cdbab3b26e1059281bd33adb0120` |
| `ns08_terminales/euler.time.log` | `85c9deb6655199fd1b0055ee5eee03fb513ffce5de5f19a82d81b538d169b7e9` |
| `ns08_terminales/euler.guard.log` | `09fbcde57bd459505dbf298fb0b2d2110cc9c70e85f4fbaf9f57429550cfd62d` |

Persisten pendientes distintos del resultado computacional: control global no
nulo de Euler, refinamiento espacial adicional y estudio de convergencia,
revisión matemática humana y evaluación de clean/adversarial start. Las simulaciones numéricas no
demuestran explosión ni resuelven el problema del Milenio.
