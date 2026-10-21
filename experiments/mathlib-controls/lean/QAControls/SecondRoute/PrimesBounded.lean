import Mathlib
import QAControls.Guard

namespace QAControls.SecondRoute

theorem bounded_of_full (P : ℕ → Prop) :
    (∀ n : ℕ, ∃ p, n < p ∧ P p) → ∀ n : ℕ, n ≤ 100 → ∃ p, n < p ∧ P p :=
  fun h n _ => h n

theorem bounded_not_imp_full :
    ∃ P : ℕ → Prop, (∀ n : ℕ, n ≤ 100 → ∃ p, n < p ∧ P p) ∧ ¬ ∀ n : ℕ, ∃ p, n < p ∧ P p :=
  ⟨fun p => p = 101, fun _ hn => ⟨101, by omega, rfl⟩, fun h => by
    obtain ⟨p, hp, rfl⟩ := h 101
    omega⟩

#guard_independent bounded_of_full of Nat.exists_infinite_primes Nat.infinite_setOf_prime
#guard_independent bounded_not_imp_full of Nat.exists_infinite_primes Nat.infinite_setOf_prime

end QAControls.SecondRoute
