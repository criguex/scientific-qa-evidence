import Mathlib
import QAControls.Guard

namespace QAControls.SecondRoute

theorem primes_reform_equiv_cheat :
    (∀ n : ℕ, ∃ p, n < p ∧ Nat.Prime p) ↔ (∀ n : ℕ, ∃ p, n ≤ p ∧ Nat.Prime p) :=
  ⟨fun _ n => let ⟨p, hp, hP⟩ := Nat.exists_infinite_primes n; ⟨p, hp, hP⟩,
   fun _ n => let ⟨p, hp, hP⟩ := Nat.exists_infinite_primes (n + 1); ⟨p, by omega, hP⟩⟩

#guard_independent primes_reform_equiv_cheat of Nat.exists_infinite_primes Nat.infinite_setOf_prime

end QAControls.SecondRoute
