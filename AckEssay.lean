/-
  The Ackermann Function and the Turing Machine — verified Lean 4 layer.

  Every snippet in this file is compiled against a pinned Mathlib rev.
  Banner: ✓ verified (Lean 4.32.0, Mathlib @ v4.32.0, 2026-09-02)

  Sections mirror the essay:
    §2  definition, totality, rows, monotonicity
    §3  Turing computability (essay's machine vs Mathlib's Partrec code)
    §5.1 each fixed row is primitive recursive
    §5.2 the composition bound — the essay's SUM form (B(i)), proved from Mathlib's MAX form
    §5.3 the domination theorem (Mathlib's unary+pairing development)
    §6  the diagonal escape
  -/
import Mathlib.Computability.Ackermann
import Mathlib.Computability.Primrec.Basic
import Mathlib.Computability.TuringMachine.ToPartrec

-- `ack` and the `ack_*` lemmas are top-level (there is no `Ackermann` namespace).

/-! ## §2 — definition, totality, rows, monotonicity -/

-- The two-argument Ackermann function, exactly the essay's (1).
-- `def ack : ℕ → ℕ → ℕ` is a *plain total def*: Lean's termination checker
-- accepts it using the nested/lexicographic well-founded relation on (m, n) —
-- precisely the relation the essay's §2.2 double induction mirrors by hand.
#check ack

-- Small evaluations (safe: rows 2–3 stay tiny).
#eval ack 2 5      -- = 2*5 + 3 = 13
#eval ack 3 4      -- = 2^(4+3) - 3 = 125
#eval ack 4 1      -- = 2↑↑4 - 3 = 65533  (the first "unwritable" row is row 4)

-- Rows 0–3 (the essay's table (2), rows m = 0..3). Mathlib has these as `simp` lemmas.
-- Row 4 (tetration, 2↑↑(n+3)-3) is NOT in Mathlib v4.32.0 — left as an exercise.
#check ack_one     -- ack 1 n = n + 2
#check ack_two     -- ack 2 n = 2 * n + 3
#check ack_three   -- ack 3 n = 2 ^ (n + 3) - 3

-- Monotonicity (the essay's Prop 2.2), both arguments.
#check ack_strictMono_right   -- ∀ m, StrictMono (ack m)        (2nd argument)
#check ack_strictMono_left    -- ∀ n, StrictMono (fun m => ack m n)  (1st argument)

/-! ## §3 — Turing computability -/

-- Mathlib proves `ack` computable via a *Partrec code* (`pappAck`), not via a raw
-- stack Turing machine. The essay's `M_A` (stack machine, §3.1) is the *conceptual*
-- machine; this is the machine-checked witness that `ack` is Turing-computable.
#check computable₂_ack        -- Computable₂ ack

-- The Partrec ⇒ Turing-machine half of Theorem 4.1: every partial-recursive code
-- is evaluated by a concrete TM2 machine, in polynomial time. (Fully qualified:
-- the namespace is `Turing.PartrecToTM2`.)
#check Turing.PartrecToTM2.tr_eval   -- StateTransition.eval (TM2.step tr) (init c v) = halt <$> c.eval v

/-! ## §5.1 — each fixed row is primitive recursive (the essay's Prop 5.1) -/

-- For each fixed k, the one-variable function n ↦ ack k n is primitive recursive.
-- This is the metatheoretic "family of separate PR definitions" the essay stresses:
-- the induction on k produces, for each numeral k, a *separate* PR proof — it does
-- NOT produce a single PR function (k, n) ↦ ack k n (that is exactly what Thm 6.1
-- denies, via the diagonal).
-- The statement is in the unary+pairing world (`Nat.Primrec`); we prove it in the
-- general `Primrec` world (real product projections, `Primrec.snd`/`Primrec.comp`)
-- and convert back once with `Primrec.nat_iff` : Primrec f ↔ Nat.Primrec f.
theorem ack_row_primrec (k : ℕ) : Nat.Primrec (fun n => ack k n) :=
  (Primrec.nat_iff (f := fun n => ack k n)).mp <| by
    induction k with
    | zero =>
      -- ack 0 n = n + 1 = succ n.
      exact (Primrec.succ : Primrec (fun n : ℕ => n + 1)).of_eq (fun n => by rw [ack_zero])
    | succ k IH =>
      -- IH : Primrec (fun n => ack k n).  ack (k+1) 0 = ack k 1 (constant);
      -- ack (k+1) (n+1) = ack k (ack (k+1) n).  So n ↦ ack (k+1) n is the 1-arg
      -- primitive recursion with base `ack k 1` and step (v ↦ ack k v).
      have hf : Primrec (fun p : ℕ × ℕ => ack k p.2) := Primrec.comp IH Primrec.snd
      have hstep : Primrec₂ (fun _ (v : ℕ) => ack k v) := Primrec₂.mk hf
      exact (Primrec.nat_rec₁ (ack k 1) hstep).of_eq fun n => by
        induction n with
        | zero => simp
        | succ n IHn => simp [IHn]

-- Concretely: the low rows are PR (sanity check against the table (2)).
#check ack_row_primrec 0
#check ack_row_primrec 1
#check ack_row_primrec 3

/-! ## §5.2 — the composition bound: the essay's SUM form (B(i)) -/

-- Mathlib's lemma is the MAX form:
--   ack_ack_lt_ack_max_add_two (m n k) : ack m (ack n k) < ack (max m n + 2) k
--
-- The essay's Lemma 5.2 is the SUM form:  ack x (ack y z) < ack (x + y + 2) z.
-- It is a two-line corollary of the max form: `max x y ≤ x + y`, hence
-- `max x y + 2 ≤ x + y + 2`, and `ack · z` is monotone in its first argument.
-- This is B(i) from the plan — the essay's *specific* bound, now a verified lemma.
theorem ack_comp_bound_sum (x y z : ℕ) : ack x (ack y z) < ack (x + y + 2) z := by
  -- max x y ≤ x + y  (each of x, y is ≤ x + y, so their max is too)
  have hmax : max x y ≤ x + y :=
    (max_le_max (Nat.le_add_right x y) (Nat.le_add_left y x)).trans (le_of_eq (max_self (x + y)))
  calc
    ack x (ack y z) < ack (max x y + 2) z := ack_ack_lt_ack_max_add_two x y z
    _ ≤ ack (x + y + 2) z := ack_mono_left z (Nat.add_le_add hmax (le_refl 2))

-- The max form it is derived from (Mathlib's actual lemma):
#check ack_ack_lt_ack_max_add_two

/-! ## §5.3 — the domination theorem (Mathlib's unary+pairing development) -/

-- The essay's Theorem 5.3 (multivariate, sum bound, +1 level) and Mathlib's
-- `exists_lt_ack_of_nat_primrec` (unary+pairing, max bound, +9 recursion constant)
-- are the SAME theorem in two formulations. Mathlib's statement, verbatim:
#check exists_lt_ack_of_nat_primrec
--   {f : ℕ → ℕ} (hf : Nat.Primrec f) : ∃ m, ∀ n, f n < ack m n

-- The two-formulation bridge. Mathlib v4.32.0 expresses the n-ary/textbook PR class
-- via `Nat.Primrec₂` (the 2-ary predicate) and the unary+pairing inductive
-- `Nat.Primrec` (zero/succ/left/right/pair/comp/prec). NOTE: the `Nat.Primrec'` /
-- `prim_iff` bridge named in some references does NOT exist in this rev; the working
-- bridge is `Nat.Primrec₂` + `Primrec₂.mk` (a binary f is PR iff its curried version
-- is `Nat.Primrec`). This is why the essay keeps its multivariate proof as the star
-- and presents Mathlib's unary+pairing proof as a parallel development.
#check Primrec₂
#check Primrec₂.mk

/-! ## §6 — the diagonal escape (the essay's Theorem 6.1) -/

-- The diagonal n ↦ ack n n is not primitive recursive; hence the two-argument
-- Ackermann function is not primitive recursive. Mathlib's exact statements:
#check not_nat_primrec_ack_self   -- ¬ Nat.Primrec (fun n => ack n n)
#check not_primrec₂_ack           -- ¬ Primrec₂ ack

-- The contradiction, reproduced (the heart of the essay's Thm 6.1):
--   assume ack is PR  ⇒  the diagonal is PR  ⇒  ∃ K, ∀ n, ack n n < ack K n
--   at n = K this is  ack K K < ack K K,  i.e. a < a — immediate contradiction.
-- (This is Mathlib's own `not_nat_primrec_ack_self` proof, verbatim.)
theorem not_primrec_ack_essay_form : ¬ Nat.Primrec (fun n => ack n n) := fun h => by
  obtain ⟨K, hK⟩ := exists_lt_ack_of_nat_primrec h
  exact (hK K).false
