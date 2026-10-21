import Mathlib
import QAControls.Guard

namespace QAControls.SecondRoute

theorem primes_defeq_equiv :
    (∀ n : ℕ, ∃ p, n < p ∧ Nat.Prime p) ↔ (∀ n : ℕ, ∃ p, n + 1 ≤ p ∧ Nat.Prime p) :=
  Iff.rfl

#guard_independent primes_defeq_equiv of Nat.exists_infinite_primes Nat.infinite_setOf_prime

end QAControls.SecondRoute
