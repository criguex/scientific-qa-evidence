# language: en
# Evidence: evidence/formal/cd-validation/mutants/, evidence/formal/statement-provenance/, experiments/mathlib-controls/
# Step-by-step explanation: docs/METODOLOGIA.md#hu-3--el-enunciado-no-deja-pasar-trampas

@US-3
Feature: The statement lets no trap through
  As a reviewer
  I want to know that the checker compares the exact statement
  So that I can be sure that what was proved is what was published and not an easier version

  Background:
    Given build B2
    And a copy of the challenge statement

  @AC-3.1 @met
  Scenario Outline: Every one-symbol trap is rejected
    Given I change one symbol of the statement: "<trap>"
    When I run Comparator with the changed statement
    Then Comparator rejects it with "statements do not match"
    And the exit code is not 0

    Examples:
      | trap                                                 |
      | (C) no external force: f = 0                         |
      | (D) no external force: f = 0                         |
      | (C) periodic data instead of data on ℝ³              |
      | (C) viscosity ≥ 0 instead of > 0                     |
      | (D) negation dropped: existence instead of breakdown |
      | Euler: time T* ≤ 1/2 instead of T* ≤ 1               |

  @AC-3.2 @met
  Scenario: A change with no meaning is accepted (control)
    Given I only change a comment of the statement
    When I run Comparator
    Then Comparator answers "Your solution is okay!"
    # Without this control, an exact check cannot be told apart from one that rejects everything.

  @AC-3.3 @met
  Scenario: The statement is the one Google DeepMind published
    Given the 18 declarations of OpenAI's challenge
    And the public Formal Conjectures statement from Google DeepMind
    When I compare them after normalizing the text
    Then the 18 declarations match
    But name resolution was not verified

  @AC-3.4 @met
  Scenario: A rejection means "the statement changed", not "the theorem is false"
    Given three theorems that Mathlib already proves
    And 11 cases registered before running them
    When I pass Comparator 8 changes to the statement, 4 of them equivalent
    Then Comparator rejects all 8
    And a second method classifies each change as equivalent, weaker or false
