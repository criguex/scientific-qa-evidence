import Mathlib
import QAControls.Guard

namespace QAControls.SecondRoute

theorem lt_le_schema (P : ℕ → Prop) :
    (∀ n : ℕ, ∃ p, n < p ∧ P p) ↔ (∀ n : ℕ, ∃ p, n ≤ p ∧ P p) :=
  ⟨fun h n => let ⟨p, hp, hP⟩ := h n; ⟨p, hp.le, hP⟩,
   fun h n => let ⟨p, hp, hP⟩ := h (n + 1); ⟨p, by omega, hP⟩⟩

theorem primes_reform_equiv :
    (∀ n : ℕ, ∃ p, n < p ∧ Nat.Prime p) ↔ (∀ n : ℕ, ∃ p, n ≤ p ∧ Nat.Prime p) :=
  lt_le_schema Nat.Prime

#guard_independent primes_reform_equiv of Nat.exists_infinite_primes Nat.infinite_setOf_prime

end QAControls.SecondRoute
