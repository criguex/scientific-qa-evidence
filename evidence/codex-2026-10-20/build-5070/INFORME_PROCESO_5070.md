# Verificación de Navier–Stokes y Euler en WAR / RTX 5070

**Informe de ejecución y controles reproducibles — 20 de octubre de 2026.**  
**Corte de evidencia de los controles:** 16:24:46 UTC / 11:24:46 de Bogotá.  
**Corte histórico del video del proceso:** aproximadamente 16:25 UTC / 11:25 de Bogotá.  
**Actualización final de esta edición:** 17:02:18 UTC / 12:02:18 de Bogotá.  
**Estado final observado:** compilación correcta; los cuatro teoremas usan únicamente axiomas estándar, sin `sorryAx`; comparadores y segundo kernel omitidos.

La compilación principal terminó correctamente en **2.342 segundos, 39 minutos y 2 segundos**, con caché Mathlib. Se construyó `Euler.Solution` y se inspeccionaron los dos teoremas de Navier–Stokes y los dos de Euler. En los cuatro aparecen exactamente `propext`, `Classical.choice` y `Quot.sound`. Esto cierra los controles de compilación y axiomas NS-06, NS-07 y EU-05 de esta ejecución, no toda la auditoría semántica ni una verificación con segundo kernel.

El mutante que añade fuerza cero fue rechazado, pero el resultado tiene **alcance limitado**: el constructor pasa de dos a tres campos y la prueba existente no proporciona el nuevo campo ni demuestra `toComparator f = 0`. Esto no acredita que la fuerza sea esencial ni que sea imposible reparar la prueba. NS-08 sigue abierto: ambos comparadores se omitieron y no hubo segundo kernel.

El archivo `PROCESO_5070.mp4` es una **reconstrucción explicativa narrada**, elaborada a partir de la configuración y de los logs auténticos disponibles. No es una grabación histórica de todas las pulsaciones de teclado. Conserva el corte de las 11:25; el video completo añade **al final** una tarjeta y narración de actualización para que ese estado histórico no se confunda con el resultado final. La simulación física aparece primero y se documenta en `INFORME_SIMULACION_5070.md`.

Evidencia final: [log de ejecución](../build-5070/resultados_5070/run.log), [axiomas de los cuatro teoremas](../build-5070/resultados_5070/axioms.txt), [fallo del mutante](../build-5070/resultados_5070/mutant_force_zero.log) y [resumen derivado sin claves duplicadas](../formal-controls/derived_verification_summary.json).

![Actualización final de la ejecución formal](simulation/render/focused/final_update.png)

## 1. Qué se pidió y qué se hizo

La petición fue ejecutar en la máquina con la RTX 5070 el script que ya estaba preparado en la auditoría, usando la conexión SSH sobre Tailscale. Después se pidió explicar el proceso en video, entregar un informe amplio y añadir pruebas de control para evaluar la credibilidad del resultado.

Se encontró y utilizó la máquina `war`. El equipo corre Windows 11; no era un servidor Linux convencional al que bastara copiar el script y ejecutar `bash`. WSL 2 ya estaba instalado, pero no había una distribución Linux utilizable. Se instaló Ubuntu 24.04 dentro de WSL, se creó el usuario `nse` y se preparó un directorio de trabajo aislado.

Se fijó el commit auditado, se verificaron externamente los ocho hashes de referencia, se instaló la versión exacta de Lean y se inició el script original. El lanzamiento quedó en una tarea de Windows para que cerrar la sesión SSH no matara el trabajo. Se limitó el uso de CPU para que la máquina siguiera disponible.

Además se escribieron y ejecutaron tres archivos Lean independientes de Mathlib: una proposición verdadera, una falsa con una táctica que debe fallar y una falsa aceptada mediante `sorry`. Se probó también que un cambio de un byte altera el hash esperado. Estas son pruebas del **comportamiento del verificador y de los controles de integridad**, no pruebas sustitutivas de Navier–Stokes o Euler.

## 2. Topología y recursos utilizados

```text
Mac del operador
    │
    │ SSH autenticado, transportado por Tailscale
    ▼
WAR — Windows 11
    │
    │ Tarea: ADV050-NSE-20261020
    ▼
WSL 2 — Ubuntu 24.04 — usuario nse
    │
    ├── Git + commit fijado + verificación SHA-256
    ├── Lean 4.34.0-rc2 + Lake
    ├── Mathlib fijado + descarga de caché
    ├── lake build
    ├── #print axioms de cuatro teoremas
    └── copia mutante con fuerza cero
```

| Recurso | Valor observado |
|---|---|
| Alias SSH | `war` |
| Dirección Tailscale | `100.77.196.62` |
| Usuario Windows | `War\criguex` |
| Sistema anfitrión | Windows 11 |
| Procesador | AMD Ryzen 5 9600X, 6 núcleos / 12 hilos |
| RAM del anfitrión | 64 GB |
| Disco libre observado antes del trabajo | aproximadamente 225 GB |
| GPU | NVIDIA GeForce RTX 5070, 12.227 MiB de VRAM informados |
| WSL preexistente | 2.7.11 |
| Distribución instalada | Ubuntu 24.04 |
| Kernel observado | `6.18.33.2-microsoft-standard-WSL2` |
| Usuario Linux | `nse` |
| Memoria visible en WSL | aproximadamente 30 GiB + 8 GiB de swap |
| Afinidad del trabajo | CPU lógicas 0–5, mediante `taskset` |
| Prioridad | `nice 10` |
| Hilos Lean | `LEAN_NUM_THREADS=6` |
| Inicio del trabajo | `2026-10-20T16:15:57Z` / 11:15:57 Bogotá |

La RTX 5070 identifica el equipo, pero **Lean no utiliza la GPU en este procedimiento**. La compilación depende de CPU, RAM, disco y descarga de dependencias. Los seis identificadores de CPU de `taskset` son procesadores lógicos; esta configuración no debe describirse como una garantía de usar seis núcleos físicos independientes.

La tarea programada aísla el trabajo de la vida de la conexión SSH. Eso no lo hace inmune a un apagado, suspensión, reinicio de Windows, cierre de WSL o falta de memoria/disco.

## 3. Identidad exacta de lo que se verifica

| Elemento | Valor fijado u observado |
|---|---|
| Repositorio | `https://github.com/openai/NavierStokesAndEuler` |
| Commit del proyecto | `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` |
| Toolchain | Lean `4.34.0-rc2` |
| Commit del binario Lean | `6a10ac8c22beadecabdbb0919c2b50214762f91d` |
| Revisión Mathlib observada | `85e3a25e006c35636f0e53b0e9296caca2685bc0` |
| Archivos Lean versionados del proyecto | 2.659 |
| Líneas en esos archivos | 641.332 |
| Directorio Linux | `<WSL_HOME>/nse_audit_20261020` |
| Checkout | `<WSL_HOME>/nse_audit_20261020/NavierStokesAndEuler` |

La cifra de **850.000 líneas** del mensaje inicial no corresponde al recuento comprobado del checkout. El total verificado es **641.332 líneas en 2.659 archivos Lean**, incluyendo Navier–Stokes y Euler y excluyendo las dependencias descargadas. No se debe sumar de nuevo el subtotal de Euler a un total que ya lo incluye.

El recuento se obtuvo a partir de archivos seguidos por Git:

```sh
git ls-files -- '*.lean' | wc -l
git ls-files -z -- '*.lean' | xargs -0 cat | wc -l
```

Fijar el commit evita que un cambio futuro de `main` cambie silenciosamente lo que se estaba verificando. Los hashes permiten comparar bytes concretos con el manifiesto de la auditoría. Ninguno de los dos demuestra por sí mismo que el enunciado formal exprese correctamente la matemática que interesa.

### Ocho hashes comparados con el manifiesto

Los ocho valores reales coincidieron con los ocho esperados:

| Archivo | SHA-256 esperado y observado |
|---|---|
| `lean-toolchain` | `8190e75a201741065fe508b28955dd64dd72d090babe5f70ce6848879d68ae88` |
| `lakefile.toml` | `97b2804da5b9a2cd0aaf44ce42b7c39e9947beff9d2ac01a11e0d3d867af1c09` |
| `lake-manifest.json` | `5ec1dc8e009008d0efb9601cd38f6ba54e753fd538b0e5f8c3e6c5ec72ee1e09` |
| `formalization.yaml` | `d9866d5c1fdc16832f098e5f2affa96baf0b156a5f34b9be015d793e1abe2fdd` |
| `ComparatorChallenges/NavierStokes.lean` | `0cd193b8d5cbd0266e6e2f72e68dd5abcdcf2430ebd435dd9289737e9aa7da61` |
| `ComparatorChallenges/NavierStokes.json` | `7610ecead7b390d80ff7f4229a3ff8f18d630e046f7ad1de4f92c7e8e76845b8` |
| `NavierStokes/ComparatorDefinitions.lean` | `8d90e0f9eee14f8b01773852083a02fd58bda59d4de2abb60d1787bbc9f6ebf4` |
| `NavierStokes/ComparatorSolution.lean` | `52950d5d618a8d34c9bfbdb16641c81c276e97b6d7fd2a76c08577353f0b0227` |

Estos ocho hashes proceden del manifiesto existente. No son un manifiesto exhaustivo de los 2.659 archivos; en particular, no incluyen los archivos de Euler. Se comprobó además `git status --porcelain`, cuya salida estaba vacía, y `git fsck --full --no-reflogs`, que terminó con código 0 sin errores. Esto añade evidencia de un checkout limpio y de integridad de los objetos Git al momento observado. El script principal imprime adicionalmente hashes de archivos de Euler; imprimirlos sin un valor de referencia no constituye una comparación independiente.

| Artefacto de entrada | SHA-256 |
|---|---|
| `build_on_5070.sh` original | `906beffeec5c9265ecdb658c5106e785d2ffaae56bc43846f5962520dd079473` |
| `audit_static.json` | `2cf2a09b8bfbe85a2d30c06b61ccfe9038f48eb4b2fdb35188e9a4e27b542fa5` |

La copia del script realmente ejecutado se recuperó de WAR y se conserva en [evidence/build_on_5070.sh](../build-5070/build_on_5070.sh). Una versión local modificada posteriormente no debe atribuirse a esta ejecución por compartir el nombre: la identidad de esta corrida es la copia preservada y su hash.

## 4. Qué hace el trabajo principal

El script original se ejecutó **sin editar**, invocado con `bash -e`. La opción `-e` añade salida temprana ante ciertos errores no gestionados; no hace abortar automáticamente los comandos cuyo error el propio script captura dentro de un `if`.

### 4.1 Entorno, Git y toolchain

Registra el sistema, CPU, memoria y disco; instala Elan si hace falta; clona el repositorio si todavía no existe; hace `fetch`; selecciona el commit fijado y muestra `lean --version`. Elan administra el toolchain y Lake es el gestor de compilación del proyecto Lean.

Un error de instalación, permisos o descarga es un problema de infraestructura, no un contraejemplo matemático. Por eso se conserva tanto el código de salida como el mensaje de error.

### 4.2 Mathlib y caché

`lake exe cache get` obtiene dependencias y artefactos precompilados. La descarga terminó con **8.747 de 8.747 archivos descomprimidos**. El log registra `2026-10-20T16:21:50Z lake build (full project)`: a esa hora comenzó la compilación principal. Obtener la caché no equivale a aceptar las pruebas del proyecto.

La caché reduce trabajo repetido, pero mantiene una frontera de confianza: en esta ejecución no se ha comprobado toda la dependencia Mathlib con un segundo kernel independiente. Las afirmaciones del informe no deben expandirse a una verificación independiente de todo el ecosistema Lean.

### 4.3 Compilación de referencia

`lake build` compila el proyecto según sus objetivos y dependencias declaradas. Esta es la ejecución de referencia sin el requisito artificial de fuerza cero. Su éxito debe comprobarse en `lake_build.log` y en el resumen final, con atención al código de salida.

El tamaño del checkout no implica que cada una de sus líneas se recompile desde cero: los objetivos declarados y los artefactos existentes determinan el trabajo efectivo. La afirmación relevante al cierre será qué objetivos se construyeron satisfactoriamente y qué teoremas se pudieron importar e inspeccionar.

**Resultado final:** el log registra `Build completed successfully (11424 jobs).` a continuación de la construcción de `Euler.Solution`. La fase de impresión de axiomas comienza a las `17:00:52 UTC`. Los 11.424 trabajos incluyen objetivos y dependencias; no se traducen en 11.424 teoremas nuevos ni en la recompilación completa de Mathlib desde cero.

Los objetivos predeterminados incluyen `NavierStokes`, `Euler` y `ComparatorChallenges`. El log mostró, por ejemplo, `Built NavierStokes.R3.CompactEnergy (3.4s)`. En las observaciones posteriores había seis procesos Lean activos y alrededor de 3 GiB de RAM WSL usados, con swap sin uso. Un contador como `9024/9580` incluye dependencias y objetivos que pueden variar: **no se interpreta como porcentaje de las pruebas propias completado**.

### 4.4 Inspección de axiomas

Después del build se importan las soluciones y se solicita:

```lean
import NavierStokes.ComparatorSolution
import Euler.Solution

#print axioms NavierStokes.Comparator.navier_stokes_breakdown_R3
#print axioms NavierStokes.Comparator.navier_stokes_breakdown_periodic
#print axioms Euler.euler_breakdown_R3
#print axioms Euler.exists_compact_smooth_euler_singularity
```

Se esperan dependencias estándar como `propext`, `Classical.choice` y `Quot.sound`. Una aparición de `sorryAx` mostraría que el teorema depende de un hueco admitido. Aceptar esos axiomas estándar sigue siendo una elección del fundamento lógico; no significa que la prueba carezca literalmente de axiomas.

Los archivos `ComparatorChallenges/*.lean` contienen `sorry` esperados como huecos del desafío. Un warning en esos archivos no demuestra por sí solo que las soluciones estén incompletas. La comprobación decisiva recae en los axiomas de los cuatro teoremas finales importados desde sus módulos de solución.

El script original busca una cadena con los tres nombres **en un orden concreto**, exactamente cuatro veces. Si Lean presenta un orden diferente o una dependencia más pequeña, puede emitir `CHECK_MANUALLY` aunque el contenido sea aceptable. Es necesario leer las cuatro declaraciones y analizar sus conjuntos de axiomas, en vez de interpretar cualquier etiqueta del script como un veredicto definitivo.

### 4.5 Mutante de fuerza cero

El script copia el checkout a `mutant_force_zero` y agrega a `ForceConditionDecay`:

```lean
zero : f = 0
```

Después intenta construir `NavierStokes.ComparatorSolution` en esa copia. La intención es comprobar si el argumento de Navier–Stokes depende de poder elegir una fuerza externa no nula.

La condición de aceptación de este ensayo es más estricta que “el proceso terminó con error”:

1. La compilación de referencia debe haber terminado correctamente.
2. Debe comprobarse que la modificación se aplicó al lugar previsto.
3. El mutante debe fallar por una obligación de prueba relacionada con la nueva condición.
4. Un error de red, archivo faltante, timeout, memoria insuficiente o proceso matado no cuenta como mutación detectada.

El script original asigna `KILLED` a cualquier build fallido del mutante. Esa etiqueta por sí sola es insuficiente. El log debe justificar la causa. Incluso un error de construcción de la estructura por faltar el campo `zero` es evidencia de que el testigo existente no satisface automáticamente el requisito añadido; no demuestra por sí mismo un teorema de imposibilidad para todas las posibles pruebas sin fuerza.

El mutante se aplica a la copia de Navier–Stokes, no a la prueba de Euler. Tampoco convierte una prueba con fuerza en una demostración del caso sin fuerza.

### 4.6 Comparator y segundo kernel

La opción `RUN_COMPARATOR` quedó en `0`. No se ejecutan Comparator ni `nanoda` en este trabajo. NS-08 permanece fuera del resultado de esta ejecución. No debe presentarse una comparación textual previa como si fuera la comprobación de términos por un segundo kernel.

## 5. Controles pequeños ejecutados realmente

Los controles se ejecutaron con el binario absoluto del toolchain fijado, sin importar Mathlib. La tercera corrida, que además prueba `sha256sum -c` de extremo a extremo, comenzó a las `16:24:46.347895Z` y terminó a las `16:24:46.992411Z`, aproximadamente **0,645 segundos**. No hay que confundir esta duración con la del build principal.

El registro completo está en `evidence/controles_20261020_v3/controls_summary.json`; cada fixture deja además su `stdout` y `stderr` en archivos separados. Las corridas v1 y v2 se conservan. Se trata de ocho categorías de control, no de ocho pruebas matemáticas independientes: dos categorías comparan el mismo commit en fuentes distintas.

| Control | Resultado esperado | Resultado observado |
|---|---|---|
| Commit del manifiesto | coincide con el commit fijado | coincide |
| `git rev-parse HEAD` | coincide con el commit fijado | coincide, salida 0 |
| Integridad de ocho archivos | 8/8 iguales | 8/8 iguales |
| Mutación de un byte | original aceptado y copia alterada rechazada por `sha256sum -c` | original salida 0 / `OK`; alterada salida 1 / `FAILED` |
| Toolchain | versión y commit exactos | coinciden |
| Proposición verdadera | aceptación, sin axiomas | salida 0; sin axiomas |
| Proposición falsa | rechazo por error lógico | salida 1; meta `False` no resuelta |
| Proposición falsa con `sorry` | aceptación, con `sorryAx` | salida 0; `sorryAx` visible |

`all_controls_passed: true` significa únicamente que **estos ocho controles cumplieron sus expectativas**. El JSON incluye explícitamente el alcance: “CONTROLES DEL VERIFICADOR; NO SON UNA PRUEBA DE NS NI EULER”.

### 5.1 Control positivo: el verificador acepta algo válido

Archivo `controls/positive.lean`:

```lean
theorem control_true : 1 + 1 = 2 := by rfl
#print axioms control_true
```

Salida real:

```text
'control_true' does not depend on any axioms
```

Código de salida: `0`.

Este ensayo descarta una configuración evidentemente rota que rechace incluso un teorema elemental. No certifica la completitud de Lean para cualquier proposición verdadera ni la fidelidad del modelo de fluidos.

### 5.2 Control negativo: el verificador rechaza una demostración inválida

Archivo `controls/negative.lean`:

```lean
theorem control_false : False := by trivial
```

Parte relevante de la salida real:

```text
error: Tactic `assumption` failed

⊢ False
```

Código de salida: `1`.

La táctica `trivial` termina intentando `assumption`; por eso el diagnóstico menciona `assumption`. La meta `False` no queda resuelta. Este resultado comprueba que el ejecutable no acepta ciegamente ese archivo inválido. No es un test exhaustivo de todos los caminos del kernel.

### 5.3 Control de hueco admitido: compilar no basta

Archivo `controls/sorry.lean`:

```lean
theorem control_sorry : False := by sorry
#print axioms control_sorry
```

Parte relevante de la salida real:

```text
warning: declaration uses `sorry`
'control_sorry' depends on axioms: [sorryAx]
```

Código de salida: `0`.

Es un resultado deliberadamente esperado: Lean permite usar `sorry` durante el desarrollo. Por ello “el comando acabó bien” no basta para afirmar que una prueba está completa. La dependencia `sorryAx` hace visible el hueco y justifica inspeccionar axiomas de los cuatro teoremas principales.

### 5.4 Corrupción simulada: un byte distinto

Se leyó `lean-toolchain`, se copió su contenido a un `bytearray` en memoria y se aplicó `XOR 1` al primer byte. Se comprobó que la longitud no cambió y que exactamente un byte era diferente. Se guardaron original y copia alterada, junto con sendos manifiestos, **en el directorio de resultados, fuera del checkout**.

La tercera corrida ejecutó el comando real `sha256sum -c` contra ambas copias, usando como referencia el hash original. Resultado del original: `hash_original.bin: OK`, código 0. Resultado alterado: `hash_mutated.bin: FAILED`, código 1, con advertencia de una suma que no coincide. Esto prueba también el comando utilizado en el precheck, no solo la desigualdad de dos hashes calculados en Python.

| Contenido | SHA-256 |
|---|---|
| Original | `8190e75a201741065fe508b28955dd64dd72d090babe5f70ce6848879d68ae88` |
| Un byte alterado en memoria | `ca3ca5d8d9db5b4fd339e8abd0004d3c6e1cf7653d8c31b2467a2402b585805b` |

Esto confirma la detección de esta corrupción concreta y que el control compara bytes, no solo nombres. No autentica por sí mismo el origen del manifiesto: si alguien cambiara simultáneamente archivo y manifiesto antes de establecer una referencia confiable, una comparación posterior podría coincidir.

### 5.5 Una corrección real del clasificador

La primera corrida quedó registrada a las `16:20:15.587911Z–16:20:16.166187Z`. Lean rechazó correctamente el teorema falso, pero el clasificador exigía que el mensaje contuviera literalmente `trivial`. Al aparecer `assumption`, ese control se marcó incorrectamente como fallido.

Se corrigió el clasificador para reconocer ambos diagnósticos, siempre exigiendo salida no nula, `error:`, `failed` y la meta `False`. Se añadió un test con el diagnóstico exacto observado y se repitió la ejecución en una carpeta nueva. La primera evidencia se conserva; no se sustituyeron sus resultados.

El self-check también comprueba que una salida `137` con `Killed` y un timeout **no** se acepten como rechazo matemático. Esa distinción es relevante para interpretar posteriormente el mutante de fuerza cero.

## 6. Cómo reproducir los controles

Dentro de WAR/WSL, con los fixtures juntos en la carpeta `controls`:

```sh
python3 <WIN_HOME_WSL>/nse-audit-20261020/controls/run_controls.py \
  <WSL_HOME>/nse_audit_20261020/NavierStokesAndEuler \
  <WIN_HOME_WSL>/nse-audit-20261020/audit_static.json \
  <WSL_HOME>/controls_repeticion
```

El directorio de salida debe estar fuera del repositorio auditado. Conviene usar uno nuevo por corrida para preservar la evidencia anterior. El script usa solo la biblioteca estándar de Python; no instala paquetes ni modifica los archivos del proyecto.

La salida `0` del runner requiere que todos sus controles pasen. Una salida `1` significa que al menos un control no cumplió la expectativa; el JSON permite distinguir un hash diferente, una versión incorrecta, un fallo de infraestructura o un diagnóstico inesperado.

Para inspeccionar la versión:

```sh
<WSL_HOME>/.elan/toolchains/leanprover--lean4---v4.34.0-rc2/bin/lean --version
```

Para el estado del trabajo principal, sin volver a lanzarlo:

```sh
ssh war 'schtasks /Query /TN ADV050-NSE-20261020 /V /FO LIST'
```

Los comandos anteriores son instrucciones de reproducción o inspección. No prueban que una ejecución futura vaya a producir idénticos tiempos ni que un build pendiente ya haya terminado.

## 7. Qué significan Navier–Stokes y Euler aquí

Esta sección resume la **auditoría estática preexistente** `AUDITORIA_NAVIER_STOKES.md` y su `audit_static.json`. No es una nueva revisión independiente de las 641.332 líneas ni de los documentos externos que esa auditoría compara.

### Navier–Stokes con fuerza

Según esa auditoría, las declaraciones de la solución coinciden con el desafío formal y este reproduce las alternativas de ruptura (C) y (D) examinadas allí. Los testigos de la construcción parten de velocidad inicial cero y utilizan una fuerza externa construida en la prueba.

El enunciado existencial permite elegir una fuerza. Por tanto, si los teoremas pasan la verificación, la conclusión corresponde al **enunciado con fuerza que realmente expresan**. No autoriza a eliminar la fuerza de la conclusión.

La lectura de condiciones, cuantificadores, regularidad y energía pertenece a la auditoría semántica. La compilación comprueba derivaciones dentro de esas definiciones, pero no decide por sí sola si la formalización expresa la interpretación física deseada.

### Euler sin fuerza

El documento estático informa que las 13 declaraciones compartidas entre el desafío de Euler y la solución son idénticas, y que la ecuación elimina viscosidad y fuerza:

```text
∂ₜv + (v · ∇)v = −∇p
```

Para el segundo teorema documenta un dato inicial suave, de soporte compacto y no nulo; un tiempo positivo de vida; existencia hasta ese tiempo; maximalidad; y explosión de cantidades ligadas a la norma C¹ y a la vorticidad. Estas cláusulas buscan evitar que “no existe una solución global” se cumpla por un enunciado vacío.

La misma auditoría señala una limitación de procedencia: el desafío de Euler fue adaptado por los autores de la solución y no quedó fijado previamente por el tercero considerado allí. El presente trabajo no resuelve esa limitación ni verifica disputas de autoría, prioridad científica o reconocimiento comunitario.

**EU-06 sigue pendiente:** falta el control positivo formal recomendado para mostrar una solución global de la clase pertinente con dato inicial no nulo. El control `1 + 1 = 2` no cubre esa cuestión.

## 8. Cierre por criterio después de revisar los logs finales

| Criterio | Evidencia necesaria | Estado final observado |
|---|---|---|
| Identidad del checkout | commit correcto, archivos esperados, integridad | commit y ocho hashes comprobados; checkout limpio y `git fsck` sin errores |
| NS-06 | build de referencia completo y correcto | cerrado: build `OK`, 2.342 s con caché |
| NS-07 | axiomas de los dos teoremas NS, sin `sorryAx` ni axiomas extra injustificados | cerrado: únicamente los tres axiomas estándar en ambos |
| NS-08 | Comparator y segundo kernel aceptan las soluciones | abierto: comparadores `SKIPPED`, sin segundo kernel |
| NS-09 | baseline válido y mutación comprobada | alcance limitado: falla el constructor ampliado y falta justificar la nueva condición; no demuestra fuerza esencial |
| EU-05 | build/importación de Euler + axiomas de sus dos teoremas | cerrado: `Euler.Solution` construido y ambos teoremas con axiomas estándar |
| EU-06 | control global positivo con dato no nulo | no ejecutado |
| Campaña ADV-050 B01–B08 | registros de esa campaña y sus resultados | no comprobada en este trabajo |

El cierre se apoya en los logs efectivos de build y axiomas, no solamente en que la tarea de Windows terminara. `axioms.txt` contiene las cuatro declaraciones citadas en la sección 4.4, cada una con `[propext, Classical.choice, Quot.sound]`.

### Interpretación limitada del mutante

La compilación mutante falla en `NavierStokes/CompactSpatialForceDecay.lean:89`, porque `ForceConditionDecay.mk` ahora tiene tres campos explícitos y el constructor existente ofrece dos. La línea siguiente deja la meta `ComparatorBridge.toComparator f = 0`.

Es un fallo reproducible relacionado con el endurecimiento introducido, no un OOM ni una descarga fallida. Pero demuestra solamente que **la prueba existente no satisface sin cambios la estructura modificada**. No se ha ejecutado una búsqueda de reparación, ni se ha demostrado que el nuevo teorema sea falso, ni que la fuerza no nula sea matemáticamente indispensable.

### Corrección del resumen, sin modificar el original

El `summary.json` original repite la clave `commit`: primero contiene el SHA y después `"OK"`. Un lector JSON habitual conserva solo la última aparición. Por eso se preservó el [archivo original](resultados_5070/summary.json) y se generó [derived_verification_summary.json](../formal-controls/derived_verification_summary.json), con campos distintos `commit_sha` y `commit_status`, las dos apariciones originales y hashes de los logs fuente.

El script [`derive_verification_summary.py`](../formal-controls/derive_verification_summary.py) comprueba el SHA contra el manifiesto, el éxito de build, los cuatro listados de axiomas y los diagnósticos exactos del mutante. No reescribe los logs ni constituye un segundo kernel.

## 9. Archivos y trazabilidad

### En la máquina remota

| Ruta | Uso |
|---|---|
| `<WSL_HOME>/nse_audit_20261020/nse_results/run.log` | log principal Linux |
| `<WSL_HOME>/nse_audit_20261020/nse_results/lake_build.log` | compilación de referencia completada |
| `<WSL_HOME>/nse_audit_20261020/nse_results/axioms.txt` | axiomas observados de los cuatro teoremas |
| `<WSL_HOME>/nse_audit_20261020/nse_results/mutant_force_zero.log` | fallo efectivo del mutante |
| `<WSL_HOME>/nse_audit_20261020/nse_results/summary.json` | resumen original preservado, con clave duplicada |
| `<WIN_HOME>\nse-audit-20261020\launcher.log` | log vivo del lanzador Windows |
| `<WIN_HOME>\nse-audit-20261020\exit_code.txt` | código final del lanzador, al terminar |

El lanzador está preparado para copiar `nse_results` al directorio Windows al terminar. En una ejecución interrumpida puede faltar el resumen final, aunque existan logs parciales útiles. La ausencia de `summary.json` no debe suplirse inventando un estado.

### En el paquete entregado

| Archivo o carpeta | Contenido |
|---|---|
| `INFORME_PROCESO_5070.md` | fuente editable de este informe |
| `INFORME_PROCESO_5070.html` | lectura local e impresión |
| `video/` | proyecto reproducible de Remotion y narración |
| `PROCESO_5070.mp4` | reconstrucción explicativa en español |
| `controls/` | fixtures y runner de controles |
| `evidence/controles_20261020/` | primera corrida conservada |
| `evidence/controles_20261020_v2/` | corrida corregida, ocho controles satisfactorios |
| `evidence/controles_20261020_v3/` | comprobación final que añade `sha256sum -c` contra original y copia alterada |
| `evidence/launcher.log` | instantánea del log remoto a la hora de recogida |

Los logs son evidencia local de ejecución; no constituyen una certificación firmada por un tercero. Los hashes facilitan detectar cambios posteriores cuando se conserva una referencia confiable.

## 10. Límites de la conclusión

Una simulación numérica de fluidos puede ilustrar fenómenos o detectar problemas en un modelo numérico, pero no sustituye una demostración formal de explosión de una ecuación continua. La simulación 3D añadida a esta entrega se presenta como experimento numérico ilustrativo con sus propios controles, separado de la evidencia de aceptación de los teoremas.

Los controles ejecutados comprueban casos concretos, no la ausencia de cualquier bug en Lean, en el compilador del sistema, en WSL, en el hardware o en las dependencias. La inspección de axiomas añade información valiosa, pero no garantiza la fidelidad semántica de las definiciones. El manifiesto verifica ocho archivos y el commit fijado; no es una firma independiente de toda la cadena de suministro.

El script principal tampoco es un oráculo: su comprobación de hashes solo imprime valores, la clasificación `KILLED` del mutante es amplia y su detección de axiomas depende de una cadena exacta. En esta ejecución se añadió una comparación externa de hashes y se documentó la revisión manual necesaria de los otros resultados.

**Conclusión final de la ejecución:** identidad de commit, toolchain y ocho hashes comprobada; controles elementales satisfactorios; build de referencia correcto; los cuatro teoremas inspeccionados dependen solo de axiomas estándar y no de `sorryAx`. El mutante aporta un rechazo de alcance limitado. Siguen abiertos Comparator/segundo kernel, EU-06 y las cautelas semánticas y de procedencia señaladas en el informe. No se afirma resolver el problema del milenio ni se emite un juicio sobre premios o prioridad científica.

## 11. Referencias utilizadas

- Auditoría local preexistente: `AUDITORIA_NAVIER_STOKES.md`.
- Manifiesto local: `audit_static.json`.
- Script ejecutado sin modificaciones: `build_on_5070.sh`.
- Evidencia generada en WAR: logs y `controls_summary.json` de las dos corridas.
- [Código en el commit auditado](https://github.com/openai/NavierStokesAndEuler/tree/f9e8bc5b38b6e212696e8a30e3e91517af887bbd).
- Documentación primaria del procedimiento: [comandos básicos WSL](https://learn.microsoft.com/en-us/windows/wsl/basic-commands) y [tareas e hilos en Lean](https://lean-lang.org/doc/reference/latest/IO/Tasks-and-Threads/).
- Para la producción audiovisual, documentación oficial de [Remotion Audio](https://www.remotion.dev/docs/media/audio) y [exportación](https://www.remotion.dev/docs/cli/render).
