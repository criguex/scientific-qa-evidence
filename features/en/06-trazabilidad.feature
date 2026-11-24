# language: en
# Evidence: evidence/SHA256SUMS.txt, evidence/test_consistency.py, experiments/receipt-check/, evidence/numerical/
# Step-by-step explanation: docs/METODOLOGIA.md#hu-6--la-evidencia-es-trazable-y-la-herramienta-se-revisa-a-sí-misma

@US-6
Feature: The evidence is traceable and the tool checks itself
  As an auditor
  I want every result to point to an intact file and the tools to report their own failures
  So that I can trust the evidence and not just the report

  @AC-6.1 @met
  Scenario: Every evidence file is intact
    Given the hashes recorded in "evidence/SHA256SUMS.txt"
    When I recompute the SHA-256 of every file
    Then all of them match their recorded hash

  @AC-6.2 @met
  Scenario: The documents state the same numbers as the records
    Given the README, CLAIMS.md and the machine-readable records
    When I run "evidence/test_consistency.py"
    Then every published number matches its record

  @AC-6.3 @met
  Scenario: A receipt naming a missing log is detected
    Given the authentic files of a run
    And a receipt that names a log that does not exist
    When I run the published procedure and the receipt check P6
    Then the published procedure exits with code 0 and does not notice
    But P6 exits with code 1 and reports "P6:receipt-log-missing-comparator-run.log"

  @AC-6.4 @met
  Scenario: The numerical tests catch the planted errors
    Given nine synthetic models with 84 variants per host
    When I run the campaign on macOS and on Linux
    Then each host gives 27 PASS, 54 KILLED and 3 SURVIVED
    And the two hosts classify every variant the same way
    And the 3 survivors stay visible on purpose

  @AC-6.5 @met
  Scenario: The tool gives no false success when the oracle fails
    Given an oracle that raises an exception or returns NaN
    When the numerical runner processes the case
    Then it marks the case "INCONCLUSIVE" with "oracle_valid: false"
    And if export fails, it marks the run as incomplete and exits with code 2
