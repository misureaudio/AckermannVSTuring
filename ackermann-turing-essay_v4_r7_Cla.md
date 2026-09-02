# Ackermann - Turing v4 essay review 7

##

I checked this against the actual Mathlib4 source (not just plausible-looking Lean) and worked through the math by hand. Overall: **the mathematics is essentially correct and carefully stated, and most of the specific Lean/Mathlib claims check out — but there's one concrete factual error in the Lean layer that undercuts the "everything is ✓ verified" framing.**

**Math and proof content — accurate.**

- The Péter recursion (1), the row table (2), and the closed forms are all correct. I hand-verified: `ack 3 4 = 2^7−3 = 125`, `ack 4 1 = 2↑↑4−3 = 65533`, and the digit-count claims for `A(4,2)` and `A(4,4)` (via `log₁₀2 ≈ 0.30103`) check out.
- The composition bound `A(x, A(y,z)) < A(x+y+2, z)`, the domination theorem (level-additive induction), and the diagonal-escape argument are all standard and correctly executed — including the subtle point that "each row is PR" does *not* give "the two-variable function is PR."
- Theorem 4.1 (PR ⟺ TM with a PR clock) is folklore stated correctly, and the essay is honest that Mathlib doesn't yet have the ⟸ direction as a packaged theorem.
- The F_ω vs ε₀ distinction (§7) is the correct and often-blurred point: A is provably total in PA, the Kirby–Paris hydra is not — the essay gets this exactly right, including the counterexample showing pointwise FGH-level bounds are the wrong tool (`A(3,8)=2045 < 2048=F₂(8)`, which I re-derived and confirms the essay).

**Lean/Mathlib claims — mostly verified, one real error.**
I cross-checked the cited lemma names against the live Mathlib4 docs page for `Mathlib.Computability.Ackermann`. These are all genuine, with matching statements: `ack_zero`, `ack_succ_zero`, `ack_succ_succ`, `ack_one`, `ack_two`, `ack_three`, `ack_strictMono_right/left`, `exists_lt_ack_of_nat_primrec`, `not_nat_primrec_ack_self`, `not_primrec₂_ack`, `Nat.Partrec.Code.pappAck`, `computable₂_ack`. The essay's claim that Mathlib's bound is the *max* form is also confirmed — the real lemma is `ack_ack_lt_ack_max_add_two : ack m (ack n k) < ack (max m n + 2) k`, matching exactly.

However, in §3.1 (and again in the references), the essay imports `Mathlib.Computability.TuringMachine.ToPartrec` and checks `PartrecToTM2.tr_eval`. **That module path doesn't exist.** The real file is `Mathlib.Computability.TMToPartrec`, and the relevant object lives under the namespace `Turing.PartrecToTM2` (e.g. `Turing.PartrecToTM2.tr`), not a bare `PartrecToTM2`. So that specific snippet, despite being labeled "✓ verified," would not compile as written — it's the one place the essay's formal-verification bookkeeping is wrong.

**One caveat I can't resolve:** the longer hand-written proofs (`ack_row_primrec`, `ack_comp_bound_sum`, `not_primrec_ack_essay_form`) use real-looking Mathlib API (`Primrec₂.mk`, `Primrec.nat_rec₁`, `Nat.Primrec.comp`, etc.), but I can't actually compile Lean here, so I can't independently confirm those tactic scripts succeed — only that the lemma names they cite are genuine and the target statements are correctly typed.

**Bottom line:** this is a well-built, mathematically sound essay whose Lean layer is *largely* honest and cross-checks correctly against real Mathlib — with one concrete, fixable inaccuracy (the wrong `TMToPartrec` module path) that means the "everything green-checked" claim is slightly overstated.
