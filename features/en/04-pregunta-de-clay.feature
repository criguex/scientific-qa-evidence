# language: en
# Evidence: evidence/formal/clay-lean-risk.md, bridges/, evidence/formal/clay-correspondence.md
# Step-by-step explanation: docs/METODOLOGIA.md#hu-4--es-la-pregunta-de-clay

@US-4
Feature: It is the Clay Institute's question
  As the mathematical community
  I want the Lean statement to say the same as the Clay Institute's official text
  So that we know whether what was proved answers alternatives (C) and (D) of the problem

  Background:
    Given Clay's official text, written by C. L. Fefferman, with its erratum
    And the formal statements of (C) and (D)

  @AC-4.1 @met
  Scenario: Each Clay clause is reviewed against the formal statement
    When I compare the 16 clauses one by one, ranked by risk
    Then 6 match directly
    And 9 match through named standard facts
    And 1 needs a human decision: periodic pressure in (D)

  @AC-4.2 @met
  Scenario: OpenAI's theorems imply Clay's literal text in Lean
    Given my literal transcription of Clay in "bridges/ClayLiteral.lean"
    When I prove "k1_C" and "k1_D" in Lean from OpenAI's theorems
    Then both are proved for every viscosity greater than 0
    And they hold under both readings of "smooth" at time zero
    And the zero solution meets every Clay condition, so the result is not vacuous

  @AC-4.3 @pending
  Scenario: An independent expert reviews the Clay transcription
    Given the review sheet "bridges/K0_REVIEW.md" with 14 points
    When someone who knows Lean or the problem compares it with Clay's PDF
    Then they confirm the transcription is faithful
    # Actual result: nobody has reviewed it yet. This criterion stays at NO.

  @AC-4.4 @pending
  Scenario: The reading of periodic pressure in (D) is decided
    Given Clay's erratum on periodic pressure
    When a mathematician decides whether it is a condition of the solution
    Then clause 16 is resolved
    # Actual result: the Clay Institute did not interpret it. This criterion stays at NO.
