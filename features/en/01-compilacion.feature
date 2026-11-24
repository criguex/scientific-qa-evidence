# language: en
# Evidence: evidence/formal/cd-validation/, evidence/formal/b5/, evidence/lean-cloud-2026-10-23/
# Step-by-step explanation: docs/METODOLOGIA.md#hu-1--las-demostraciones-compilan

@US-1
Feature: OpenAI's proofs build
  As a reviewer of the proof
  I want the code OpenAI published to build from a pinned version
  So that I know Lean checked every step and no step is left unproved

  Background:
    Given the repository openai/NavierStokesAndEuler at commit "f9e8bc5"
    And Lean version "v4.34.0-rc2"

  @AC-1.1 @met
  Scenario Outline: The code builds from the pinned commit
    When I build it in build "<build>"
    Then the build exits with code 0
    And the record is kept in "<evidence>"

    Examples:
      | build                        | evidence                                  |
      | B1 · 20 Oct                  | evidence/formal/cd-validation/README.md   |
      | B2 · 20 Oct · official cache | evidence/formal/cd-validation/README.md   |
      | cloud · 23 Oct · 609 of 609  | evidence/lean-cloud-2026-10-23/README.md  |

  @AC-1.2 @met
  Scenario Outline: It builds without pieces compiled by others
    Given an empty cache folder
    When I build with "lake --no-cache build" in build "<build>"
    Then the build exits with code 0
    And every ".olean" file is newer than the build start
    And no prebuilt package was downloaded

    Examples:
      | build                       |
      | B4 · 21 Oct · 1 h 29 min    |
      | B5 · 21/22 Oct · 1 h 15 min |

  @AC-1.3 @met
  Scenario: The conclusions use only the standard axioms
    Given build B5
    When I ask Lean for the axioms of "k1_C" and "k1_D"
    Then the list is exactly "propext", "Classical.choice" and "Quot.sound"
    But "sorryAx" and any extra axiom are absent
