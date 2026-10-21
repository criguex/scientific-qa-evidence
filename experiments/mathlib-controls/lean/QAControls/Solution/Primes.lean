import Mathlib

namespace QAControls

theorem primes_infinite : ∀ n : ℕ, ∃ p, n < p ∧ Nat.Prime p := fun n => by
  obtain ⟨p, hp, hpr⟩ := Nat.exists_infinite_primes (n + 1)
  exact ⟨p, by omega, hpr⟩

end QAControls
