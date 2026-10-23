# Controles de rechazo de kernels

Este control comprueba dos respuestas en un fixture mínimo exportado con `lean4export`: aceptación de una prueba válida y rechazo de la misma declaración cuando se cambia solamente su término de prueba por otro de tipo incompatible. No modifica los teoremas de Navier–Stokes/Euler ni es una validación universal del kernel.

## Fixture y mutación

El fixture local contiene:

```lean
theorem target : 0 = 0 := rfl
theorem wrong : True := True.intro
```

Se exportaron `target` y `wrong` en NDJSON 3.1.0. El baseline original tiene 212 registros y SHA-256 `e6dde97dbc98c413dbc0104958b1b546c469c0148ca56b427ee0ed1e751b4f6f`. La primera mutación que apuntaba a Expr 146 falló en el parser (`Expr not found 146`) porque esa expresión aparecía después de `target`; ese resultado queda registrado como fallo de fixture, no como rechazo del kernel.

La versión corregida coloca `target` al final tanto en el baseline normalizado como en el mutante. Ambos tienen 212 registros. La única diferencia estructural es `target.thm.value`: Expr 143 en baseline y Expr 146 en el mutante. El campo `type` permanece en Expr 140 y la lista `all` permanece sin cambios. SHA-256 del baseline normalizado: `3b19256d433ca5fec9ebdfeb2f2721968a72d6a75c5cf522a41c601fc7b12520`; del mutante: `db631fa73c15dd2eb454a744873a677ac3184400a3d0f44e24686c21eff155e1`.

## Resultados confirmados hasta ahora

| Control | Resultado observado | Interpretación permitida |
| --- | --- | --- |
| Lean, baseline normalizado | `LEAN_KERNEL_ACCEPT`, código 0 | El kernel de Lean acepta esta prueba mínima. |
| Lean, mutante normalizado | `LEAN_KERNEL_REJECT: while replaying declaration 'target': (kernel) declaration type mismatch, 'target' has type True but it is expected to have type @Eq Nat 0 0`, código 2 | Rechazo semántico por discrepancia de tipos, después de parsear el NDJSON. |
| Nanoda, baseline, runner02 | Código 0; `Checked 18 declarations with no errors` | Aceptación del export mínimo con la configuración corregida. |
| Nanoda, mutante, runner02 | Código 101; `src/tc.rs:981:71 assertion failed: self.def_eq(u, v)` | Rechazo por comprobación de igualdad definicional del typechecker. El source fijado infiere el tipo del valor de la declaración y lo compara con el tipo esperado mediante `assert_def_eq`; se documenta como dictamen derivado, no como texto explícito del binario. |
| Build limpio clean03 | `lake --no-cache build`, código 0; 11 424 jobs completados | Compilación de fuentes fijadas con dependencias/toolchain reutilizados; no es bootstrap ni validación matemática. |

La colección durable runner02 terminó entre 2026-10-20 21:04:39 y 21:04:42 UTC. El baseline nanoda del runner01 no se acreditó: `print_axioms=true` sin destino produjo un error de pretty-printer aunque el proceso acabó en 0. Runner02 mantiene la misma allowlist estricta y configura `pp_to_stdout=true`, sin aceptar salidas parciales. El mutante nanoda provoca una aserción dentro de la comprobación `def_eq`; la revisión de fuente identificó que la igualdad comparada es el tipo inferido contra el tipo esperado. Los primeros fallos de desarrollo del harness —API Lean incorrecta en ReplayExport v1— tampoco cuentan como resultados de kernel.

Runner02 conserva comandos, stdout/stderr, código, UTC, duración y hashes. SHA-256 de stdout nanoda baseline: `b3e03ae0b75d093b505b15f21d77c7416e4f909409d50c1fa4b39665dca6ab5f`; stderr mutante: `faccbd3af0b28764112451c78081fa9c894db2a9f52c7c55fef1338e871a9b17`. El source nanoda está fijado en commit `9d6964f78d0fa4c93fd22fe956e17afe7e72a441`; SHA-256 de `tc.rs`: `d6126a91f3bf13928be8fd0f5dd051d064c1a4c99d6677cd2bd8996d132fb436`. El JSON raw de runner02 conserva su `COLLECTED_PENDING_CLASSIFICATION`; este párrafo es el dictamen derivado y no altera la evidencia bruta.

## Arranque de build limpio

El intento clean01 terminó antes de ejecutar el build, pero su resumen inicial indicó erróneamente PASS. Se reclasifica como fallo del harness / inconcluso: no hubo `build.exit_code`, timestamp final ni log de compilación. El journal mostró que systemd detuvo la unidad y el proceso shell recibió `Terminated` al cerrarse WSL.

Clean02 clasificó `INFRA_INCONCLUSIVE`; el preflight rechazó un socket heredado asociado a stdout/stderr de systemd y no se relajó el guard. Clean03 corrigió el arranque y finalizó como PASS de compilación de fuentes: 11 424 jobs, código 0. El resumen saneado, logs y manifiesto están en [`evidence/new_validation/clean_build03/`](../../formal-controls/clean_build03/); detalle del límite y verificación en el [acta](../README.md). Clean01/02 no se reescriben. Estas incidencias no son evidencia matemática ni de rechazo de kernels.

## Control positivo periódico (D)

El control compiló con Lean, código 0. Sobre el toro, construyó explícitamente `u₀(x)=v(x,t)=c≠0`, `p=0`, `f=0`, `ν=1`, y probó las condiciones periódicas de dato inicial, fuerza y solución. La periodicidad no es vacía: la instancia comprueba las obligaciones periódicas en el dominio y el testigo constante satisface la condición concreta; no presupone que cualquier campo la satisfaga. `#print axioms periodic_nonzero_control` informó `[propext, Classical.choice, Quot.sound]`, sin `sorryAx`. SHA-256 fuente: `907c81c5b301e7745cf92a8bc74c7f16bbc9b2c83a85b521da2b51331defa51d`; bundle privado: `295508f4480f78f00d5341dfee83f0948117768b8aee0f03fdd21ebdd2726cfa`. El resumen derivado está en `evidence/new_validation/periodic_positive_derived.json`.

Las condiciones de `InitialVelocityConditionPeriodic` piden suavidad, divergencia nula y periodicidad; las de fuerza periódica piden suavidad, periodicidad y decaimiento temporal. No piden energía finita ni decaimiento espacial. Esta constante no nula no sirve como control global de energía finita en ℝ³.

Un campo constante no nulo no tiene energía finita en todo ℝ³. Este control periódico comprueba una instancia concreta y no demuestra fidelidad de todas las hipótesis del problema de Clay, no cierra EU-06 ni establece la alternativa de ruptura. Véase la [tabla de correspondencia documental Clay–Lean](../../../formal/clay-lean-fidelity.md) y sus puentes aún no probados.

## Autoría y límites de atribución

La atribución aprobada se detalla en [`PROCEDENCIA_IA_Y_APORTES.md`](../../provenance/PROCEDENCIA_IA_Y_APORTES.md). La aceptación de la identidad no equivale a revisar cada output ni a consentimiento editorial final.

No se ha reescrito ningún informe V4 ni se ha hecho pública esta evidencia. Los resultados descritos están confirmados y limitados a los artefactos indicados; la atribución aprobada se rige por [`PROCEDENCIA_IA_Y_APORTES.md`](../../provenance/PROCEDENCIA_IA_Y_APORTES.md), sin implicar revisión humana de todos los outputs ni consentimiento editorial final.
