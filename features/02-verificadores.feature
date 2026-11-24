# language: es
# Evidencia: evidence/formal/comparator/, evidence/formal/cd-validation/, evidence/formal/kernel-currency.md, experiments/version-port/
# Explicación paso a paso: docs/METODOLOGIA.md#hu-2--otros-verificadores-dicen-lo-mismo

@HU-2
Característica: Otros verificadores dicen lo mismo
  Como revisor
  Quiero que verificadores distintos acepten la misma demostración
  Para no depender de un solo programa que podría tener un error

  @CA-2.1 @CA-2.2 @cumple
  Esquema del escenario: Comparator acepta con dos kernels distintos
    Dado la compilación "<compilación>"
    Cuando corro Comparator sobre "<desafío>" con el kernel de Lean y con nanoda
    Entonces los dos responden "Your solution is okay!"
    Y el código de salida es 0

    Ejemplos:
      | compilación | desafío                 |
      | B1          | Navier–Stokes (C) y (D) |
      | B1          | Euler                   |
      | B2          | Navier–Stokes (C) y (D) |
      | B2          | Euler                   |
      | B3          | Navier–Stokes (C) y (D) |
      | B3          | Euler                   |
      | B4          | Navier–Stokes (C) y (D) |
      | B4          | Euler                   |
      | B5          | Navier–Stokes (C) y (D) |
      | B5          | Euler                   |

  @CA-2.1 @cumple
  Escenario: Una revisión del kernel desde cero también acepta
    Dado la compilación B2
    Cuando corro "leanchecker --fresh" sobre las soluciones de Navier–Stokes y de Euler
    Entonces las dos terminan con código de salida 0

  @CA-2.3 @cumple
  Escenario: Los verificadores están al día con los errores conocidos
    Dado el código del kernel de Lean v4.34.0-rc2 y el commit de nanoda usado
    Cuando los comparo con las versiones que corrigen los errores de kernel conocidos en 2026
    Entonces el kernel de Lean es idéntico al de v4.33.1, v4.34.0 y v4.34.1
    Y el commit de nanoda es posterior a su corrección de julio de 2026

  @CA-2.4 @cumple
  Escenario: Una tercera implementación del kernel revisa las demostraciones
    Dado la compilación R0 de la campaña de versiones, en Lean v4.34.0-rc2 y el commit f9e8bc5
    Y lean4lean 0048ed7 recompilado sobre Lean v4.34.0-rc2
    Cuando corro "lean4lean --fresh" sobre "NavierStokes.ComparatorSolution" y sobre "Euler.Solution"
    Entonces las dos terminan con código de salida 0
    Y lean4lean reporta "checked 806768 declarations" para Navier–Stokes
    Y lean4lean reporta "checked 788326 declarations" para Euler
