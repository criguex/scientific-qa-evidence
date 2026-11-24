# language: en
# Evidence: evidence/formal/comparator/, evidence/formal/cd-validation/, evidence/formal/kernel-currency.md, experiments/version-port/
# Step-by-step explanation: docs/METODOLOGIA.md#hu-2--otros-verificadores-dicen-lo-mismo

@US-2
Feature: Other checkers agree
  As a reviewer
  I want separately written checkers to accept the same proof
  So that I do not depend on a single program that might have a bug

  @AC-2.1 @AC-2.2 @met
  Scenario Outline: Comparator accepts with two different kernels
    Given build "<build>"
    When I run Comparator on "<challenge>" with Lean's kernel and with nanoda
    Then both answer "Your solution is okay!"
    And the exit code is 0

    Examples:
      | build | challenge                 |
      | B1    | Navier–Stokes (C) and (D) |
      | B1    | Euler                     |
      | B2    | Navier–Stokes (C) and (D) |
      | B2    | Euler                     |
      | B3    | Navier–Stokes (C) and (D) |
      | B3    | Euler                     |
      | B4    | Navier–Stokes (C) and (D) |
      | B4    | Euler                     |
      | B5    | Navier–Stokes (C) and (D) |
      | B5    | Euler                     |

  @AC-2.1 @met
  Scenario: A kernel check from scratch also accepts
    Given build B2
    When I run "leanchecker --fresh" on the Navier–Stokes and Euler solutions
    Then both exit with code 0

  @AC-2.3 @met
  Scenario: The checkers are current with the known bugs
    Given the kernel source of Lean v4.34.0-rc2 and the nanoda commit used
    When I compare them with the versions that fix the kernel bugs known in 2026
    Then Lean's kernel is identical to that of v4.33.1, v4.34.0 and v4.34.1
    And the nanoda commit is later than its July 2026 fix

  @AC-2.4 @met
  Scenario: A third kernel implementation checks the proofs
    Given build R0 of the version campaign, on Lean v4.34.0-rc2 and commit f9e8bc5
    And lean4lean 0048ed7 rebuilt on Lean v4.34.0-rc2
    When I run "lean4lean --fresh" on "NavierStokes.ComparatorSolution" and on "Euler.Solution"
    Then both exit with code 0
    And lean4lean reports "checked 806768 declarations" for Navier–Stokes
    And lean4lean reports "checked 788326 declarations" for Euler
