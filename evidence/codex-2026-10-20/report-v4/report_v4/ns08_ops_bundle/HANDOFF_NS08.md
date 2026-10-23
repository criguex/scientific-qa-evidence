# NS-08 — relevo operativo para Luna

Estado actualizado (2026-10-20 19:26 UTC): **preflight terminado y NS-08/Euler
ejecutados secuencialmente con Comparator fijado; ambos aceptados por nanoda y
el kernel Lean; resultados terminales exit 0**. El addendum final de este
documento prevalece sobre las notas históricas previas, que se conservan para
documentar por qué se detuvo antes de recibir el GO.

### Estado acumulado posterior al primer relevo

- Toolchains portables instalados tras verificar manifiestos/hashes oficiales:
  Go 1.27.3 (`tools/go-1.27.3/go/bin/go`), Rust 1.98.1
  (`tools/rust-1.98.1/bin/rustc`, cargo) y Zig 0.17.0
  (`tools/zig-0.17.0/zig-x86_64-linux-0.17.0/zig`). No hubo sudo ni cambios
  del sistema. Versiones y evidencia: `results/install-portable-toolchains.log`,
  `results/zig-toolchain.log`, `results/ns08-linker-archive-prebuild.log`.
- Construidos secuencialmente nanoda fijado `9d6964f78d0fa4c93fd22fe956e17afe7e72a441`
  (`cargo build --release --locked --bin nanoda_bin`) y Landrun fijado
  `ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a`; los logs están en
  `results/nanoda-build.log` y `results/landrun-build.log`.
- `lake build lean4export comparator` finalizó correctamente sin `lake update`;
  evidencia `results/lake-build.log`.
- Landrun 0.1.18 real pasó controles de lectura/escritura y TCP solamente en
  perfil `--best-effort`; el resultado está en `results/landrun-controls.log`.
  En perfil normal sin ese flag, los cuatro controles no pudieron llegar a los
  procesos por ABI Landlock 7 vs requisito 10; error completo en
  `results/landrun-no-best-effort.log`. Ninguno de esos controles ejecuta el
  Comparator principal ni lo aprueba.
- Backup formal exacto en scratch Mac:
  `<TMP>/NavierStokesAndEuler-f9e8bc5b38b6e212696e8a30e3e91517af887bbd.tar.gz`,
  6,550,235 bytes, SHA256
  `afd4d2263a4cabefd1317e890b49bc04f8538402c322db4317a08161e834b4b5`,
  2,674 entradas listadas en `formal-repo-archive-listing.txt`. Es copia del
  commit exacto `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, incluye licencias y
  README versionados/originales y excluye `.git`, `.lake` y cache; no se ejecutó.
  Remoto Git: `https://github.com/openai/NavierStokesAndEuler.git`. El listado
  incluye `LICENSE`, `README.md` y `ComparatorChallenges/README.md`.
- Los dos terminales Comparator se ejecutaron únicamente tras GO explícito de
  raíz. Ver el addendum final y sus logs; no interpretar estos resultados como
  prueba de arranque adversarial limpio o de ABI Landlock 10.

Addendum 2026-10-20 18:53 UTC: el perfil exterior estricto propuesto por raíz
NO quedó validado: systemd rechazó la unidad transitoria antes del `exec` con
`Failed to set unit properties: Invalid argument`. No se ejecutó Comparator ni
se probaron controles de red/archivos/C/Rust/Lean bajo ese perfil. Ver
`strict-profile-probe-mac.log` y el script de la llamada en este scratch. La
prueba best-effort previa corresponde a otro perfil, no aprueba éste.

Las instrucciones de relevo citadas en las secciones históricas quedaron
superadas por los GO explícitos de raíz para NS y Euler descritos al final.

## Qué está autorizado y qué no

El usuario autorizó preparar las validaciones necesarias. La raíz asignó NS-08 en WAR, con una sola tarea pesada en ese host, sin voz ni render simultáneo. Permite herramientas aisladas user-local si hacen falta, pero no sudo, cambios del sistema, desactivar sandbox, ampliar axiomas, editar fuentes científicas ni alterar el worktree V4 del escritor.

NS y Euler se ejecutaron secuencialmente, con `enable_nanoda: true`, sin `lake
update` y sin cambiar fuentes científicas, axiomas, configuración o perfiles
globales. Una ejecución exitosa sobre este checkout ya compilado no acredita un
arranque adversarial limpio.

## Rutas exactas

- SSH Windows: alias local `war`; los detalles de conexión no se exportan.
- WSL: `Ubuntu-24.04`, usuario `nse`, uid/gid 1000.
- Checkout auditado: `<WSL_HOME>/nse_audit_20261020/NavierStokesAndEuler`.
- Directorio operativo NUEVO creado: `<WSL_HOME>/ns08_validation_20261020_a5YGak/`.
- Dentro de él: `tools/`, `downloads/`, `ops/` vacíos; `results/preflight-tools-and-afunix.log` contiene el segundo preflight.
- Scratch Mac de este relevo: `<TMP>/`.
- Documentos originales leídos íntegros:
  - `<HOME>/Projects/adv-050-auditoria/NS08_PROPUESTA_NO_EJECUTADA.md`
  - `<HOME>/Projects/adv-050-auditoria/PLAN_VALIDACION_V2.md`
- No se modificó ningún archivo de esos repositorios.

## Resultado comprobado

Mediciones 2026-10-20 18:30–18:33 UTC:

- Windows WAR: Ryzen 5 9600X, 6 núcleos/12 hilos, carga observada 10%; unos 49,8 GiB libres de RAM.
- RTX 5070: 3338/12227 MiB, utilización 0%; NS-08 es CPU.
- WSL estaba detenido y se inició mediante la llamada de preflight. Ahora queda el entorno WSL en marcha, sin tarea de validación nuestra.
- Ubuntu 24.04.5; kernel `6.18.33.2-microsoft-standard-WSL2`; 12 CPU visibles; 29 GiB disponibles de un límite de unos 30 GiB; swap 8 GiB sin uso; 918 GiB libres en filesystem.
- `nse` no es root y `CapEff`/`CapPrm` son cero.
- systemd es PID 1 y `systemctl --user is-system-running` devuelve `running`.
- Consulta Landlock por syscall: ABI 7. `/sys/kernel/security/lsm` no existe; no interpretar esa ausencia como falta de Landlock ni la ABI como prueba suficiente del sandbox.
- No se observó runner relevante de voz/render/simulación/Comparator activo en el inventario inicial.

### Prueba real AF_UNIX: aprobada

Se creó y cerró un socket AF_UNIX sin restricciones: permitido, exit 0.

Se ejecutó una unidad transitoria de usuario:

```sh
systemd-run --user --wait --pipe --collect \
  --unit=ns08-afunix-probe-a5ygak \
  --property=RestrictAddressFamilies=~AF_UNIX \
  /usr/bin/python3 -c '...'
```

El código completo está en `preflight-tools-and-afunix.sh`. Bajo esa unidad, crear AF_UNIX falló con errno 97 (`EAFNOSUPPORT`), mientras crear AF_INET siguió permitido. Unidad finalizó exit 0 y fue recolectada; runtime 17 ms, pico informado 256 KiB. **Esto no es todavía una prueba de landrun**: no está construido.

## Pins y fuentes

| Componente | Pin | Estado observado |
|---|---|---|
| Repositorio | `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` | Checkout exacto, `git status --porcelain` vacío |
| Comparator | `19e111e2141cf333c7daff0f64c5f24acc91dd2e` | Paquete exacto y limpio |
| lean4export | `cacf989bd75f608700820f6afc595f32e7a99a4d` | Paquete exacto y limpio |
| nanoda | `9d6964f78d0fa4c93fd22fe956e17afe7e72a441` | Pin de propuesta; NO clonado/construido |
| landrun | `ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a` | Pin de propuesta; NO clonado/construido |

El manifiesto del checkout contiene los mismos pins de Comparator y lean4export. Toolchain: `leanprover/lean4:v4.34.0-rc2`.

Se calcularon hashes de todos los archivos versionados, conservados en `wsl-preflight.log`; no cargar ese log entero al contexto: son unas 2800 líneas. Los ocho hashes de `evidence/resultados_5070/sha256.txt` fueron contrastados automáticamente y todos coinciden; salida breve en `original-eight-hashes-check.txt`.

Ambos JSON de desafío mantienen:

```json
{"enable_nanoda": true, "permitted_axioms": ["propext", "Quot.sound", "Classical.choice"]}
```

Theorems NS:

- `NavierStokes.Comparator.navier_stokes_breakdown_R3`
- `NavierStokes.Comparator.navier_stokes_breakdown_periodic`

Theorems Euler:

- `Euler.euler_breakdown_R3`
- `Euler.exists_compact_smooth_euler_singularity`

Binarios esperados que todavía NO existen:

- `.lake/packages/Comparator/.lake/build/bin/comparator`
- `.lake/packages/lean4export/.lake/build/bin/lean4export`

### Fuentes externas consultadas

Se leyó íntegro y conservó el [README de Comparator fijado](https://raw.githubusercontent.com/leanprover/comparator/19e111e2141cf333c7daff0f64c5f24acc91dd2e/README.md) como `Comparator-README-pinned.md`.

Su SHA256 `cfdf0ff608755d56f3bad62acc86273bc0c11591335678344bf53cb733b61772` coincide con el README del paquete en WAR.

Se consultó el [go.mod fijado de landrun](https://raw.githubusercontent.com/Zouuup/landrun/ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a/go.mod): declara Go 1.24.0.

Se conservó el [Cargo.toml fijado de nanoda](https://raw.githubusercontent.com/ammkrn/nanoda_lib/9d6964f78d0fa4c93fd22fe956e17afe7e72a441/Cargo.toml) como `nanoda-Cargo-pinned.toml`, SHA256 `4e236937ef83d1cdefa0d59a3dee3f5f46e15ac00666e4fd845db914795e703c`.

El paquete se llama `nanoda_lib` 0.4.25, edición 2021; el binario es `nanoda_bin`. No se eligió todavía una versión de Rust/Go para instalar. La raíz está verificando fuentes externas.

## Herramientas y hueco del compilador

Presentes: `/usr/bin/ld` (binutils 2.42), `/usr/bin/time`, systemd/systemctl, curl, git y Python3.

No aparecen en el PATH de bash no-login: Go, rustc, cargo, cc, gcc, clang, make. Tampoco están instalados por dpkg `gcc`, `g++`, `clang`, `libc6-dev`, `linux-libc-dev`, `build-essential`; make figura no instalado.

**No concluir aún que se necesita sudo:** Lean trae un toolchain autocontenido en:

`<WSL_HOME>/.elan/toolchains/leanprover--lean4---v4.34.0-rc2/`

Su `bin/` contiene `clang`, `ld.lld`, `llvm-ar`, `leanc`; `lib/` contiene CRT objects, `glibc/`, LLVM22, libc++, libgcc_s, etc. Esto se inventarió pero **no se probó que sirva como enlazador C para Rust/CGO**. No se ejecutó ningún probe C ni se instaló una alternativa. Es el siguiente punto técnico a resolver de forma acotada.

El elan existente está en `<WSL_HOME>/.elan/bin`; usar ruta explícita o añadirla al PATH solo para el comando. `lake --version` comprobado: Lake 5.0.0-src+6a10ac8, Lean 4.34.0-rc2.

## Comandos ya ejecutados y registros

Patrón SSH→WSL que funciona y evita problemas de quoting de Windows:

```sh
ssh -o BatchMode=yes -o ConnectTimeout=12 war \
  'wsl.exe -d Ubuntu-24.04 -u nse -- bash -s' \
  < <TMP>/preflight.sh \
  2>&1 | tee <TMP>/wsl-preflight.log
```

No repetir ciegamente `preflight-tools-and-afunix.sh`: exige que el directorio operativo no exista y ahora ya existe. Es registro del comando, no script idempotente.

Archivos del scratch:

- `preflight.sh`, `wsl-preflight.log`
- `preflight-tools-and-afunix.sh`, `preflight-tools-and-afunix.log`
- `windows-preflight.txt` (incluye salida WSL UTF-16 con NUL)
- `original-eight-hashes-check.txt`
- `Comparator-README-pinned.md`
- `nanoda-Cargo-pinned.toml`
- este relevo

El primer preflight es un inventario, no un gate todo-o-nada: conserva errores esperados de binarios ausentes y de `/sys/kernel/security/lsm`. El exit observado del pipeline con `tee` no acredita que todos esos comandos internos pasaran. La prueba AF_UNIX sí registra ambos códigos explícitamente.

## Siguientes pasos seguros — no realizados

1. Confirmar con raíz que continúa la reserva de WAR y la preparación user-local. No lanzar voz/render allí.
2. Resolver el enlazador C sin sudo: prueba pequeña controlada del toolchain existente o alternativa portable oficial aprobada. Si exige cambios del sistema, informar y detenerse.
3. Seleccionar y registrar versiones exactas de Go >=1.24 y Rust reciente; descargar solo distribuciones oficiales con hashes, bajo `tools/` y `downloads/`. No cambiar perfiles globales ni el PATH permanente.
4. Clonar nanoda/landrun a las carpetas nuevas; detached a sus pines; verificar commit y árbol limpio. Construir secuencialmente:
   - `cargo build --release --locked --bin nanoda_bin`
   - `go build -o landrun ./cmd/landrun`
5. Registrar versiones, hashes de binarios, UTC, comandos exactos, stdout/stderr, códigos y RSS con `/usr/bin/time -v`.
6. Construir `lake build lean4export comparator` en el checkout auditado, sin `lake update`; registrar estado/hashes antes y después.
7. Probar **landrun real** bajo `RestrictAddressFamilies=~AF_UNIX`, incluyendo operaciones permitidas y denegadas verificables. No `fake-landrun` ni relajaciones.
8. Presentar preparación completa a raíz y esperar su gate explícito. Sólo después ejecutar Comparator NS y luego Euler con las rutas precisas de la propuesta y `enable_nanoda: true`.
9. Inspeccionar logs completos y aceptación de ambos kernels. Un fallo de herramientas, sandbox, exportación o memoria no es refutación matemática.

No se propone borrar/restaurar nada como rollback: basta detener la tarea y conservar el material nuevo. La evidencia anterior permanece intacta.

## Procesos vivos al relevo

Ningún job propio de validación, compilación, descarga o prueba continúa vivo. Todas las sesiones SSH de este preflight finalizaron. La unidad AF_UNIX transitoria terminó y se recolectó. WSL sí quedó iniciado con sus servicios normales; no se apagó ni se alteró producción.

## Addendum de perfil systemd exterior (2026-10-20 18:53 UTC)

La petición de raíz fue validar, sin relajaciones, una unidad transitoria con:

```text
RestrictAddressFamilies=none
SystemCallArchitectures=native
SystemCallFilter=~@network-io io_uring_setup io_uring_enter io_uring_register
```

La versión local es systemd 255 (`255.4-1ubuntu8.17`), con manager de usuario
activo. El `man systemd.exec` de esa instalación confirma que `none` bloquea
todas las familias de `socket(2)`, que `native` excluye ABI alternas, y que la
denylist usa `~`. También advierte que `RestrictAddressFamilies=` por sí solo
no restringe sockets heredados ni `socketpair()`; el grupo local `@network-io`
enumerado por `systemd-analyze syscall-filter` sí incluye `socket` y
`socketpair`.

Se intentó la unidad con los tres valores exactos y Python de solo diagnóstico.
systemd rechazó aplicar las propiedades (`Invalid argument`); ninguno de los
procesos de prueba llegó a ejecutarse. El mismo rechazo ocurrió al lanzar los
dos controles Landrun (sin `--best-effort`) bajo idéntico perfil. No hay
resultado de prueba de bloqueo de AF_INET/AF_INET6, AF_UNIX, `socketpair`,
`io_uring`, CapEff/herencia de sockets, ni lecturas/escrituras bajo el perfil
estricto. No se intentó un perfil más débil ni se ejecutó Comparator.

La inspección de `systemd-analyze syscall-filter` devolvió el grupo
`@network-io` con sus llamadas; una consulta separada de nombre `io_uring`
devolvió `Filter set "io_uring" not found` (la herramienta esperaba conjuntos,
por lo que esto no prueba por sí solo que los nombres de syscalls individuales
no estén soportados). La causa exacta del `Invalid argument` queda sin aislar;
no se gastó otra corrección sintáctica ni se eliminó ninguna restricción.

La llamada archivada es `strict-profile-probe.sh`; su salida local completa es
`strict-profile-probe-mac.log` (UTC 18:53:42). El archivo remoto correspondiente
es `<WSL_HOME>/ns08_validation_20261020_a5YGak/results/strict-profile-probe.log`.
El script también intentó descubrir herramientas usando rutas supuestas que no
corresponden al layout real; sus líneas C/Rust/Lean no son prueba de
disponibilidad ni ejecución bajo el perfil. Ninguna fuente científica se
editó. Los intentos terminaron durante validación de propiedades, antes de
crear procesos de servicio.

La documentación upstream consultada por raíz es
[systemd.exec](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html);
advierte que el bloqueo de familias no cubre por sí solo `socketpair()`,
sockets heredados ni `io_uring`.

### Aislamiento de propiedades (2026-10-20 18:56 UTC)

Raíz autorizó aislar cada propiedad con `/usr/bin/true`, sin Comparator ni
Landrun. Resultado en systemd 255:

| Propiedad aislada | Resultado |
|---|---|
| `RestrictAddressFamilies=none` | Rechazada antes de iniciar unidad: `Failed to set unit properties: Invalid argument`; journal sin entradas. |
| `SystemCallArchitectures=native` | Unidad arrancó/terminó con exit 0; journal `Started`. |
| `SystemCallFilter=~@network-io io_uring_setup io_uring_enter io_uring_register` | Unidad arrancó/terminó con exit 0; journal `Started`. |

Esto localiza el rechazo combinado en `RestrictAddressFamilies=none` dentro de
la API transient del manager; no explica por qué el valor que el `man`
instalado documenta como válido se rechaza. No se probó una expresión
alternativa: `SystemCallFilter=~@network-io` sí bloquea `socket` y
`socketpair`, pero no es equivalente para sockets heredados o I/O hecho con
`read`/`write`; no se acepta como reemplazo completo. Queda pendiente obtener
una expresión compatible con el manager que conserve la semántica, o declarar
el perfil exterior sin aprobar. No hubo payload en estas tres unidades.

Log completo en scratch `strict-property-isolation-mac.log` (1309 bytes,
SHA256 `9fef104c600b3a3b0a9776c47977eba908a6e2a7bf9bd8e2ba408e600c379516`);
script `strict-property-isolation.sh` (SHA256
`85ce0edede2cb8f7aec34f35365bd25751b65a17dcbc960278b6bd43a785f1de`). Log
remoto: `<WSL_HOME>/ns08_validation_20261020_a5YGak/results/strict-property-isolation.log`.

La prueba Landrun previa bajo perfil estricto no llegó a lanzar Landrun porque
systemd falló al validar RAF. En cualquier perfil ulterior, Landrun deberá
conservar su `--best-effort` upstream por ABI Landlock 7 vs 10; eso no se
presentará como validación ABI 10. Solo se podrá evaluar Comparator principal
con GO explícito de raíz y las restricciones exteriores aprobadas.

### Corrección de perfil para probes (2026-10-20 18:58 UTC)

Raíz autorizó una corrección solo para controles preflight. Se ejecutó una
única unidad transitoria con `/usr/bin/bash` y los probes dentro de la misma
unidad, usando el perfil upstream ya probado más restricciones exteriores:

```text
RestrictAddressFamilies=~AF_UNIX
SystemCallArchitectures=native
SystemCallFilter=~@network-io io_uring_setup io_uring_enter io_uring_register
NoNewPrivileges=yes
SystemCallErrorNumber=EPERM
MemoryMax=28991029248
CPUQuota=800%
RuntimeMaxSec=8h
```

Antes de iniciar la unidad, el runner no tenía descriptores socket; el proceso
de prueba confirmó `inherited_socket_fds=[]`. `CapEff=0000000000000000` al
inicio y al final. Los intentos de crear TCP, UDP, AF_UNIX, `socketpair` y
`io_uring_setup`/`enter`/`register` devolvieron `EPERM`; si alguno hubiese sido
permitido, el probe habría fallado cerrado. Landrun real fijado `0.1.18`, con
`--best-effort` upstream (necesario porque el kernel expone Landlock ABI 7 y el
binario fijado exige ABI 10 para el perfil completo), permitió lectura y
escritura dentro de allowlist (exit 0), denegó escritura fuera (`Permission
denied`, exit 1; archivo no creado). Lean 4.34.0-rc2 ejecutó un `main` vacío
con exit 0 bajo la misma unidad. Unidad completa: exit 0, runtime 1.5 s, RSS
pico 768 KiB; MemoryMax/CPUQuota/RuntimeMax quedaron aplicados. Hashes de
binarios: Landrun `e3d26ebf2f7c786f8d34b7051ad2c655329aeadbb863404e3dd05d3a97b0518a`;
Lean `e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550`.

Este resultado valida los controles de la unidad corregida, no el valor
`RestrictAddressFamilies=none` rechazado antes, no ABI 10, y no el Comparator
principal. Perfil `--best-effort` y restricciones exteriores quedan declarados
explícitamente; no son una prueba equivalente a la sandbox ABI 10 completa.
Sin el GO separado de raíz, NS/Euler no se ejecutan.

Evidencia: `strict-correction-runner-mac.log` (stdout, límites, códigos y
journal) y `strict-correction-controls.sh`. Resultado duplicado en WAR en
`results/strict-correction-controls.log`. Runner exacto:
`strict-correction-runner.sh`. El test temporal se creó únicamente bajo
`<WSL_HOME>/ns08_validation_20261020_a5YGak/ops/strict-correction-185840/`.

## Addendum final — terminales NS/Euler bajo GO explícito (2026-10-20 19:26 UTC)

### Perfil y condiciones conservadas

NS y Euler se ejecutaron secuencialmente tras GO de raíz, usando las mismas
versiones, binarios, pins, repositorio precompilado, JSON originales y
restricciones. Unidad transitoria systemd con `--wait` sin `--pipe`, stdin null,
stdout/stderr append a archivos dedicados y sesión SSH/WSL mantenida en primer
plano:

```text
RestrictAddressFamilies=~AF_UNIX
SystemCallArchitectures=native
SystemCallFilter=~@network-io io_uring_setup io_uring_enter io_uring_register
NoNewPrivileges=yes
SystemCallErrorNumber=EPERM
MemoryMax=28991029248
CPUQuota=800%
RuntimeMaxSec=8h
StandardInput=null
StandardOutput=append:<run-dir>/unit-stdout.log
StandardError=append:<run-dir>/unit-stderr.log
```

Landrun es el binario real, y Comparator upstream pasa `--best-effort`; no se
inyectó ese flag ni se usó wrapper. El kernel reporta Landlock ABI 7, mientras
Landrun completo requiere ABI 10. Por tanto, el perfil no demuestra sandbox
Landlock ABI 10 ni equivalencia con él. `RestrictAddressFamilies=~AF_UNIX` más
el filtro seccomp de `@network-io` y tres syscalls io_uring son controles
exteriores explícitos, no una afirmación de cobertura de todas las rutas del
kernel. No hubo sockets heredados al inicio, y todos los procesos observados
en el cgroup conservaron `CapEff=0` y `socketfds=[]`. Límites no alcanzados:
NS pico systemd 13.6 GiB; Euler 13.1 GiB, ambos dentro de 27 GiB; swap 0.

### Intentos y resultados

- NS intento 1, `ns08-comparator-ns-20261020-1901`, UTC 19:01:56Z: se
  interrumpió al cerrarse la sesión user-manager tras salir SSH. WSL seguía en
  ejecución en ese primer diagnóstico; journal mostró el manager de usuario
  finalizar. Se conserva como `INTERRUPTED_USER_MANAGER_LIFECYCLE`, sin status,
  sin EOF y sin aceptación. No es resultado matemático. Su boot ID fue
  `4335f650-ac13-4a3c-beec-17c3d064fb59`; intento 2 corrió bajo boot ID
  `72c20c35-cb56-4304-bcbb-b6f7432938e3`. No se habilitó linger ni se cambió
  configuración global.
- NS intento 2, `ns08-comparator-ns-attempt2-20261020-1905`, 19:05:54–19:12:56Z:
  Comparator informó `nanoda kernel accepts the solution`, `Lean default kernel
  accepts the solution` y `Your solution is okay!`. Wrapper y proceso Comparator
  exit 0. GNU time: 7:01.51 wall, 386.48 s user, 33.90 s system, max RSS
  8,128,500 KiB; unidad systemd: pico 13.6 GiB, swap 0. stdout contiene
  warnings `sorry` en los placeholders del desafío
  `ComparatorChallenges/NavierStokes.lean:273,280`. La solución compilada
  enumera exactamente `[propext, Classical.choice, Quot.sound]`; no confundir
  los placeholders/warnings del desafío con axiomas adicionales usados por la
  solución.
- Euler, `ns08-comparator-euler-20261020-1914`, 19:14:09–19:25:32Z, únicamente
  después del resultado NS: mismo Comparator informó `nanoda kernel accepts the
  solution`, `Lean default kernel accepts the solution` y `Your solution is
  okay!`. Wrapper y proceso Comparator exit 0. GNU time: 11:22.45 wall,
  646.06 s user, 34.82 s system, max RSS 7,923,188 KiB; unidad systemd: pico
  13.1 GiB, swap 0. stdout registra warnings `sorry` en los placeholders del
  desafío `ComparatorChallenges/Euler.lean:85,170`; ambos teoremas de solución
  enumeran exactamente `[propext, Classical.choice, Quot.sound]`.

### Integridad y límites de la afirmación

Ambos jobs usaron Comparator SHA256
`514de8d2acbd6e0102575cd2c575e336b7c4a40daf3ae66abe97cef5e1e6b02a`, lean4export
`4fa9e14cada304109e85da5048bcd411cf781a03539b3e50953e5c537074bd9e`, nanoda
`ccda52587ef42760dff9bc2de26edca0cb6ad207c8719cfffcd1e7daab22ccfb`, Landrun
`e3d26ebf2f7c786f8d34b7051ad2c655329aeadbb863404e3dd05d3a97b0518a`. Pins de
fuente: Comparator `19e111e2141cf333c7daff0f64c5f24acc91dd2e`, lean4export
`cacf989bd75f608700820f6afc595f32e7a99a4d`, nanoda
`9d6964f78d0fa4c93fd22fe956e17afe7e72a441`, Landrun
`ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a`. Checkout permaneció en commit
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, limpio al auditarlo después de los
dos terminales. JSON: `enable_nanoda=true`, axiomas permitidos solo
`propext`, `Quot.sound`, `Classical.choice`; sus SHA256 permanecen
`7610ecead7b390d80ff7f4229a3ff8f18d630e046f7ad1de4f92c7e8e76845b8` (NS) y
`56bc185a931f68d9a0f0265a3c00cb12771dccc85384eaf6546b37844b8adc84` (Euler).

Estos resultados son aceptación de ambos kernels sobre un checkout ya
compilado y los inputs/pins enumerados. **No** son evidencia de arranque
adversarial limpio, independencia de revisión humana, prueba formal de la
corrección de las fuentes científicas, ni garantía de sandbox Landlock ABI 10.
No se cambió repo formal ni se ejecutaron modificaciones de código o axiomas.

Logs remotos completos:

- NS: `<WSL_HOME>/ns08_validation_20261020_a5YGak/results/comparator-ns-attempt2-20261020-1905/`
- Euler: `<WSL_HOME>/ns08_validation_20261020_a5YGak/results/comparator-euler-20261020-1914/`

Copias de evidencia terminal local en este scratch: `ns-attempt2.stdout.log`,
`ns-attempt2.stderr.log` (archivo vacío), `ns-attempt2.status.txt`,
`ns-attempt2.time.log`, `ns-attempt2.guard.log`, y equivalentes `euler.*`.
Los stdout/status/time se comprobaron contra SHA256 remoto; stderr real son
archivos de cero bytes con SHA256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
