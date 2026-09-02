# v4 plan — *The Ackermann Function and the Turing Machine*

Companion to `ackermann-turing-essay_v3.md`. This plan is grounded in the **actual
Mathlib source** (fetched and read, not the review's paraphrase) and in the local
toolchain (Lean 4.33.1, lake, elan — all installed).

---

## 0. What v4 is (and is not)

v3's mathematics is already correct and the proofs are sound. v4 is **not** a rewrite.

> **v4 = v3 + a verified Lean 4 layer + the prose corrections the formalization forces.**

Three deliverables:

1. **A Lean layer**, interleaved with the prose (Alectryon/LeanInk-interactive where
   possible), every snippet compiled against a pinned Mathlib rev and labelled
   `✓ verified (Lean 4.33.1, Mathlib @ <rev>, <date>)`.
2. **A two-formulation spine** (the essay's multivariate proof vs Mathlib's
   unary+pairing proof), made explicit — this is the intellectual content v4 adds.
3. **A verification apparatus**: a reproducible `lake` project, a pinned Mathlib rev,
   an Alectryon render recipe, and an honest "frontier" section for the one genuinely
   new formalization (Theorem 4.1's ← direction).

---

## 1. Grounding: what is actually in Mathlib (verified)

Fetched `Mathlib/Computability/{Ackermann.lean, Primrec/Basic.lean,
TuringMachine/ToPartrec.lean, TuringMachine/Computable.lean}` from master.

| Essay object | Mathlib lemma (real name) | Status |
|---|---|---|
| `def A` (1) | `Ackermann.ack : ℕ → ℕ → ℕ` | plain total `def`; termination checker accepts it |
| rows 0–3 (table 2) | `ack_one` = `n+2`, `ack_two` = `2n+3`, `ack_three` = `2^(n+3)−3` | rows 0–3 in Mathlib; **row 4 (tetration) is not** |
| Prop 2.2 (mono, 2nd arg) | `ack_strictMono_right : ∀ m, StrictMono (ack m)` | exact |
| Prop 2.2 (mono, 1st arg) | `ack_strictMono_left` | exact |
| Lemma 5.2 (composition bound) | `ack_ack_lt_ack_max_add_two (m n k) : ack m (ack n k) < ack (max m n + 2) k` | **max form, not the essay's sum form** |
| Theorem 5.3 (domination) | `exists_lt_ack_of_nat_primrec {f} (hf : Nat.Primrec f) : ∃ m, ∀ n, f n < ack m n` | exact statement |
| Theorem 6.1 (diagonal escape) | `not_nat_primrec_ack_self : ¬Nat.Primrec (fun n => ack n n)`; `not_primrec₂_ack : ¬Primrec₂ ack` | exact |
| §3 computability | `computable₂_ack : Computable₂ ack` — via a **Partrec code** (`pappAck`), *not* a raw TM | different route than the essay's stack-machine |
| PR definition | `Nat.Primrec : (ℕ → ℕ) → Prop` (inductive: `zero, succ, left, right, pair, comp, prec`) | unary + pairing |
| textbook n-ary PR | `Nat.Primrec'` + `Nat.Primrec'.prim_iff` | the equivalence to unary+pairing |
| Partrec ⇒ TM | `TuringMachine.ToPartrec.tr_eval (c v) : eval (TM2.step tr) (init c v) = halt <$> Code.eval c v` | constructive, poly-time |
| TM + time bound | `TuringMachine.Computable`: `Turing.TM2ComputableInTime` (TM + `time : ℕ → ℕ` + proof) | the model half of Thm 4.1 |

**Key structural finding.** Mathlib's domination proof is built on the **unary +
pairing** formulation of PR. Its recursion step lands at constant `max a b + 9`
(via `ack_pair_lt`, `ack_add_one_sq_lt_ack_add_three`), and its composition bound is
the **max** form. The essay's proof is the **multivariate** textbook one with the
**sum** bound `x+y+2` and a `+1` level. These are the *same theorem in two
formulations*; `Nat.Primrec'.prim_iff` is the bridge. The file's own doc comment
admits it: *"We aren't able to use the same bounds as in that proof though, since our
approach of using pairing functions differs from their approach of using multivariate
functions."*

**Consequence (a clean, checkable claim for v4):** the essay's exact composition bound
is a **two-line corollary** of the existing lemma:
`ack x (ack y z) < ack (max x y + 2) z  ≤  ack (x + y + 2) z`,
the second step being monotonicity in the first argument (`max x y ≤ x + y`). So the
essay's Lemma 5.2 can be *proved in Lean in ~2 lines from `ack_ack_lt_ack_max_add_two`*
— no new machinery.

---

## 2. Corrections to review v3_r5 (the referee pass)

The review is directionally right and its §2.C PR sketch *does* match Mathlib's real
`Nat.Primrec` API (zero/succ/left/right/pair/comp/prec). But it has errors and
overclaims that a rigorist referee would flag:

1. **§2.B composition bound is mis-attributed.** The sketch
   `theorem ack_comp_bound (x y z) : ack x (ack y z) < ack (x + y + 2) z` is presented
   as if it mirrors an existing Mathlib lemma. **It does not.** Mathlib's bound is the
   *max* form (`ack_ack_lt_ack_max_add_two`). The `x+y+2` form is a 2-line weakening
   (§1). v4 must not cite a lemma that isn't there; it should *derive* the essay's form.
2. **§2 "totality is handled automatically by Lean's termination checker!"** — true that
   the `def` compiles, but the well-founded relation the checker synthesises is the
   nested/lexicographic one on `(m,n)`, which is *exactly* what the essay's §2.2 double
   induction mirrors. v4 should present the contrast (human constructive proof vs
   checker's automated witness), not reduce totality to "the checker said so."
3. **§3 "Theorem 4.1 … much less commonly formalized end-to-end … groundbreaking."**
   Overclaim. Mathlib *does* have `ToPartrec.tr_eval` (Partrec ⇒ TM, poly-time) and the
   `TM2ComputableInTime` model. What is genuinely new is the **← direction in the
   PR-clock form** (configuration coding + bounded iteration ⇒ `Nat.Primrec`). v4 scopes
   it precisely and drops "groundbreaking" for "the ← direction is not, as far as we can
   find, a single existing Mathlib theorem; we formalize it."
4. **§4 "LeanInk *or* Alectryon."** They are a *stack*, not alternatives: Alectryon's
   Lean 4 support **requires** LeanInk. v4's tooling section states the dependency.
5. **§2.A row-4 gap.** Mathlib proves `ack_one/ack_two/ack_three` (rows 0–3). The
   essay's table (2) goes to row 4 (tetration). v4 either proves row 4 as a new `simp`
   lemma or marks it as the one row left to the reader — it must not imply Mathlib has it.
6. **Tone.** "10/10", "beautifully written" are fine for a reviewer, but v4's own text
   should keep the essay's existing discipline (no decorative claims). Every formalization
   claim in v4 is either *verified* or *explicitly marked frontier*.

---

## 3. The two-formulation spine (v4's structural decision)

This is the load-bearing choice. Two options:

- **(A) Follow Mathlib** (unary+pairing): the Lean layer is a *direct mirror* of
  `Ackermann.lean` — every lemma is a reference. Lowest effort, but the essay's prose
  (multivariate) and its Lean (unary+pairing) then *disagree in the details*, which a
  careful reader will notice and object to.
- **(B) Keep the essay's multivariate proof as the star** and add the unary+pairing
  Mathlib proof as a **parallel development**, with `Nat.Primrec'.prim_iff` as the
  explicit bridge. More work, but it *resolves* the mismatch into a feature: v4 can say
  "here is the clean textbook proof (what you read), here is the machine-checked proof
  (what Mathlib checks), and here is the two-line argument that the formulations are
  the same class."

**Recommendation: (B).** It is what makes v4 more than v3+code, and it is the honest
way to present a proof whose informal and formal versions use different bounds. The
extra cost is bounded: the bridge is one existing lemma (`prim_iff`) plus a short remark.

Concretely, v4 restructures §5 as:

- §5 (informal, unchanged from v3): multivariate domination, sum bound, `+1` level.
- §5.x "The same theorem, machine-checked": the Mathlib unary+pairing development,
  `Nat.Primrec'`/`prim_iff` bridge, the max bound, the `+9` recursion constant, and the
  two-line derivation of the essay's sum bound from the max bound.

---

## 4. Section-by-section mapping (essay § → Lean)

| Essay § | Lean layer | Source |
|---|---|---|
| 2 (def, totality) | `#check ack`; note termination checker; `#eval ack 3 4` (small); contrast with Prop 2.1 double induction | `Ackermann.ack` |
| 2.1 (rows) | `ack_one/ack_two/ack_three` as `simp` lemmas; row 4 = new lemma or exercise | `Ackermann` |
| 2.2 (monotonicity) | `ack_strictMono_right/left`; one-line `#check` of both | `Ackermann` |
| 3 (machine) | present `M_A` (essay's stack machine) as the *conceptual* machine; note Mathlib proves computability via the Partrec code `pappAck` + `computable₂_ack`; show `#check computable₂_ack` | `Ackermann` + `PartrecCode` |
| 4 (Thm 4.1) | **state** the theorem; show the ⇒ half (PR ⇒ PR-clock TM) *informally* as in v3; show the Partrec⇒TM half via `tr_eval`; **mark the ← half (PR-clock ⇒ PR) as the frontier** | `ToPartrec`, `Computable` |
| 5.1 (each row PR) | the induction on `k` as a Lean `induction k` sketch; note Mathlib does not state "each fixed row is PR" as a single lemma (it's `∃ m, f n < ack m n` territory) — a small gap v4 can fill with a 1-line lemma | — |
| 5.2 (composition bound) | **prove** the essay's sum bound in ~2 lines from `ack_ack_lt_ack_max_add_two` | `Ackermann` |
| 5.3 (domination) | **mirror** `exists_lt_ack_of_nat_primrec`; show the `induction hf` structure; call out the `+9` recursion constant and the pairing helpers | `Ackermann` |
| 6 (Thm 6.1, diag) | **mirror** `not_primrec₂_ack` / `not_nat_primrec_ack_self`; show the 3-line contradiction | `Ackermann` |
| 7 (proof theory) | no Lean layer (FGH/ε₀ is not in Mathlib's Computability); keep prose-only, as in v3 | — |

---

## 5. Scope tiers (the real decision)

**Tier A — verified mirror (the spine; ship first).**
Every in-essay Lean snippet is (i) a reference to an existing Mathlib lemma, or
(ii) a one-to-few-line derivation from one (the §5.2 sum bound; the row-4 lemma if we
do it). All compiled, all labelled verified. Theorem 4.1 is *stated*, its Partrec⇒TM
half shown via `tr_eval`, and the ← half deferred to the frontier.
*Effort: ~1 day including the build. Risk: low. Fully verifiable now.*

**Tier B — new proofs (the frontier; optional follow-up).**
On top of A, actually prove in a **separate** `.lean` file (in the repo, referenced but
not required for the essay to be true):

- **B(i)** the essay's sum composition bound as a named lemma — *trivial* (2 lines).
- **B(ii)** the **multivariate** domination theorem in the essay's exact form, via
  `Nat.Primrec'` — *moderate* (port the v3 §5.3 proof; this makes the essay's *own*
  proof the formal one, not just Mathlib's pairing version).
- **B(iii)** **Theorem 4.1's ← direction**: "TM computes `f` within a PR time bound
  `t` ⇒ `f` is `Nat.Primrec`," via Gödel-coding of TM configs, PR-ness of the one-step
  transition, and bounded iteration. *Substantial* (the genuine contribution; Mathlib
  has the ingredients — `TM2ComputableInTime`, config encoding — but not this theorem
  as a single statement). Likely several hundred lines and real proof effort.

**Recommendation:** ship **Tier A** as the essay's verified body; put **B(i)–B(iii)**
in a clearly-labelled "formalization frontier" section that (a) states each theorem,
(b) lists exactly what Mathlib already provides, (c) gives the essay's informal proof as
the argument for the new lemma, and (d) links the repo file once completed. This keeps
the essay honest (only Tier A is claimed "verified") while making the frontier concrete
and reproducible. Offer to **execute B(i) and B(ii)** right after the build (cheap) and
treat **B(iii)** as a dedicated effort.

---

## 6. Verification & tooling protocol

1. **Fresh `lake` project** `ack-lean/` (do not reuse the `openai` project — its
   Mathlib is *not* built, only 22 `.olean`s). `lakefile.toml` pins a Mathlib rev
   compatible with the installed Lean 4.33.1 (pick a recent tagged rev; record it).
2. **`lake build`** (first build is long; cacheable). All essay snippets live in
   `AckEssay.lean` importing `Mathlib.Computability.Ackermann` etc.
3. **Every snippet compiles** before it is marked verified. Snippets that are
   illustrative-only (e.g., the §3 `M_A` sketch) are marked `-- sketch, not compiled`.
4. **Alectryon + LeanInk** render the interactive page:
   `alectryon --frontend md --backend webpage ack-essay.md -o ack-essay.html`
   (Lean 4 support *requires* LeanInk installed). Fallback deliverable: the static
   `.md` with fenced blocks + the verification banner (works without LeanInk).
5. **CI / reproducibility**: a `Makefile`/`justfile` target `build` (lake) and
   `render` (alectryon); pin the Mathlib rev and Lean toolchain in the repo so the
   "verified" banner is reproducible.

---

## 7. Prose changes v4 forces (beyond adding code)

- **§2.2**: add the Lean contrast (human double induction vs checker witness); keep the
  human proof as primary.
- **§3.1**: note Mathlib proves computability via the Partrec *code*, not a raw TM;
  present `M_A` as the conceptual machine. (This pre-empts the objection "your machine
  isn't the one in Mathlib.")
- **§4**: restate the scope of "no PR time bound" (already careful in v3) and *add* the
  precise frontier note: what `ToPartrec` gives vs what B(iii) would add. Drop any
  "groundbreaking" framing.
- **New §5.x**: the two-formulation bridge (multivariate ↔ unary+pairing via
  `prim_iff`), the max-vs-sum bound, the `+9` constant.
- **§5.4 / §7**: unchanged (prose-only; no FGH/ε₀ in Mathlib).
- **References**: add the Mathlib file paths + rev, `ToPartrec`, `Primrec.Basic`, and
  the Alectryon/LeanInk tools; keep the v3 references.

---

## 8. Decision points (need your call before I build)

1. **Scope** — (a) Tier A only (verified mirror; ship in ~a day), or
   (b) Tier A + B(i)+(ii) (also make the essay's *own* multivariate proof the formal
   one), or (c) all the way to B(iii) (the Theorem-4.1 ← formalization; the genuinely
   new contribution, multi-day). **My rec: (a) now, (b) right after, (c) as a dedicated
   follow-up.**
2. **Delivery** — (a) static Markdown with verified banners (no LeanInk needed to read),
   or (b) Alectryon/LeanInk interactive HTML (hover-to-see-goal-states). **My rec:
   both** — static `.md` as the source of truth, Alectryon HTML as the bonus.
3. **Mathlib rev** — pin to a specific recent tag (I'll propose one compatible with
   Lean 4.33.1 at build time).

---

## 9. First execution steps (once scope is confirmed)

1. `lake new ack-lean`; add `mathlib` dep pinned to a 4.33.1-compatible rev.
2. `lake build` (background; long).
3. Write `AckEssay.lean` with the Tier A snippets; compile; iterate.
4. Prove B(i) (sum bound) and, if chosen, B(ii) (multivariate domination via `Nat.Primrec'`).
5. Weave snippets into a v4 draft of the markdown (v3 text + §5.x + the §2/§3/§4 prose
   corrections).
6. Render Alectryon HTML; write the `justfile`; tag the verified banner.
