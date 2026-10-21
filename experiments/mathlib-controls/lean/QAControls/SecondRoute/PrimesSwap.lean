import Mathlib
import QAControls.Guard

namespace QAControls.SecondRoute

theorem primes_swap_false : ¬ ∃ p, ∀ n : ℕ, n < p ∧ Nat.Prime p :=
  fun ⟨p, h⟩ => lt_irrefl p (h p).1

end QAControls.SecondRoute
