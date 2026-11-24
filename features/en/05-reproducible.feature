# language: en
# Evidence: verificar.py, .github/workflows/verify.yml, evidence/reproductions/
# Step-by-step explanation: docs/METODOLOGIA.md#hu-5--otra-persona-lo-repite-sin-mí

@US-5
Feature: Someone else repeats it without me
  As a person who wants to review this work
  I want to run the checks on my computer and get the same result
  So that I do not have to trust what the author says

  @AC-5.1 @met
  Scenario Outline: The same fingerprint on different systems
    Given data version "c8edd482375d"
    When I run "python verificar.py" on "<system>" with Python "<python>"
    Then all six checks say OK
    And the fingerprint is "5292-A47D-AFA5"

    Examples:
      | system  | python |
      | Ubuntu  | 3.12   |
      | macOS   | 3.9    |
      | macOS   | 3.12   |
      | Windows | 3.9    |
      | Windows | 3.12   |

  @AC-5.2 @met
  Scenario Outline: Other people get the same fingerprint
    Given data version "26791fe6546f"
    When a person runs "python verificar.py" on "<system>" and reports it in issue "<issue>"
    Then their fingerprint is "C5F0-F1A8-2F4D", the same as the reference

    Examples:
      | system                | issue |
      | Windows 11             | #1    |
      | macOS, Apple Silicon   | #2    |
      | macOS, Apple Silicon   | #3    |
      | macOS, Apple Silicon   | #4    |

  @AC-5.3 @pending
  Scenario: A person reports it from Linux
    When a person runs "python verificar.py" on Linux and reports it
    Then their fingerprint matches the reference for their version
    # Actual result: there is still no report from Linux. This criterion stays at NO.

  @AC-5.4 @pending
  Scenario: Someone other than the author rebuilds the proofs in Lean
    Given the guide "docs/INDEPENDENT_REPRODUCTION.md" and its report template
    When someone else rebuilds without the author's involvement
    Then they get 609 of 609 modules and Comparator accepts (C), (D) and Euler
    # Actual result: nobody has done it yet. This criterion stays at NO.
