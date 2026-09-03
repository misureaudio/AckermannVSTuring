# v4 plan (revised) — *The Ackermann Function and the Turing Machine*

Companion to `ackermann-turing-essay_v4.md` (currently a verbatim copy of v3 — the v4
content has not yet been written). This is the **revised** plan: it folds in the r6
review's decisions (`ackermann-turing-essay_v4_plan_r6_Gem.md`) and is grounded in the
**actual Mathlib source and the local toolchain** (verified, not paraphrased).

> **v4 = v3 + a verified Lean 4 layer + the prose corrections the formalization forces.**

Three deliverables:

1. **A Lean layer**, interleaved with the prose, every snippet compiled against a pinned
   Mathlib rev and labelled `✓ verified (Lean <ver>, Mathlib @ <rev>, <date>)`.
2. **A two-formulation spine** (the essay's multivariate proof vs Mathlib's
   unary+pairing proof), made explicit — the intellectual content v4 adds.
3. **A verification apparatus**: a reproducible `lake` project, a pinned Mathlib rev, an
   Alectryon render recipe, and an honest "frontier" section for the genuinely-new
   formalization (Theorem 4.1's ← direction).

---

## 0. Review r6 — decisions incorporated

r6 approved the plan (Option B spine, tiering, tooling) and answered the three
decision points in §8. This revision bakes those answers in and corrects two of the
original plan's now-stale claims against what is actually on this machine:

| # | r6 call | How this plan changes |
|---|---|---|
| 1 | **Scope: Tier A + B(i).** Hold B(ii), B(iii). | The **sum composition bound (B(i)) is promoted into the verified body** as the named Lemma 5.2 (2-line derivation, §4 row 5.2). B(ii) multivariate-domination and B(iii) Thm 4.1 ← move to a clearly-labelled **Frontier** (stated, not proven). |
| 2 | **Delivery: both.** Static `.md` first (durable source of truth), Alectryon/LeanInk HTML second. | §6 makes the static `.md` the primary deliverable and the interactive HTML the bonus; the render step is non-blocking. |
| 3 | **Pin a stable `v4.x.0` tag** matching the local toolchain. | **Corrected against reality** (§1): no stable tag pairs with Lean 4.33.1. The pin is **Mathlib `v4.32.0` + toolchain 4.32.0**, which is *already built on this machine* (8674 oleans). This makes the build fast and reproducible, and the "verified" banner honest. |

Two stale claims in the original plan, corrected here:

- **"The `openai` project's Mathlib is not built, only 22 `.olean`s."** False now:
  `openai/ten-prrofs` pins Mathlib `v4.32.0` (toolchain 4.32.0) and has a **full build**
  (8674 `.olean`s). We do **not** reuse that project, but its already-built `v4.32.0`
  cache is what a fresh project pinning `v4.32.0` will reuse — so the first build is
  short, not a multi-hour full mathlib compile.
- **r6's "pick a `v4.x.0` tag matching 4.33.1" is not satisfiable.** Mathlib release
  tags pin the *same-minor* Lean (v4.9.1→Lean 4.9.1, …, v4.32.0→4.32.0); master→4.34.0-rc2.
  The closest stable, *already-built* pin is **`v4.32.0`/4.32.0**. (4.33.1 is installed
  but unused by this build; elan has 4.32.0 ready.)

---

## 1. Grounding: what is actually in Mathlib (verified at `v4.32.0`)

Fetched and read `Mathlib/Computability/{Ackermann.lean (391 ln),
Primrec/Basic.lean (904 ln), TuringMachine/ToPartrec.lean}` **at tag `v4.32.0`** — the
rev we will pin — not master.

| Essay object | Mathlib lemma (real name, v4.32.0) | Status |
|---|---|---|
| `def A` (1) | `Ackermann.ack : ℕ → ℕ → ℕ` | plain total `def`; termination checker accepts it |
| rows 0–3 (table 2) | `ack_one` = `n+2`, `ack_two` = `2n+3`, `ack_three` = `2^(n+3)−3` | rows 0–3 in Mathlib; **row 4 (tetration) is not** |
| Prop 2.2 (mono, 2nd arg) | `ack_strictMono_right : ∀ m, StrictMono (ack m)` | exact |
| Prop 2.2 (mono, 1st arg) | `ack_strictMono_left (n) : StrictMono (fun m => ack m n)` | exact |
| Lemma 5.2 (composition bound) | `ack_ack_lt_ack_max_add_two (m n k) : ack m (ack n k) < ack (max m n + 2) k` | **max form, not the essay's sum form** |
| Theorem 5.3 (domination) | `exists_lt_ack_of_nat_primrec {f} (hf : Nat.Primrec f) : ∃ m, ∀ n, f n < ack m n` | exact statement |
| Theorem 6.1 (diagonal escape) | `not_primrec₂_ack : ¬Primrec₂ ack`; `not_nat_primrec_ack_self : ¬Nat.Primrec (fun n => ack n n)` | exact |
| §3 computability | `computable₂_ack : Computable₂ ack` — via a **Partrec code** (`pappAck`), *not* a raw TM | different route than the essay's stack-machine |
| PR definition | `Nat.Primrec : (ℕ → ℕ) → Prop` (inductive: `zero, succ, left, right, pair, comp, prec`) | unary + pairing |
| textbook n-ary PR | `Nat.Primrec₂` + `Primrec₂.mk` (a binary `f` is PR iff its curried version is `Nat.Primrec`) | the bridge (NOT `Nat.Primrec'.prim_iff` — absent in v4.32.0) |
| Partrec ⇒ TM | `PartrecToTM2.tr_eval (c v) : eval (TM2.step tr) (init c v) = halt <$> Code.eval c v` | constructive, poly-time |
| TM + time bound | `TuringMachine.Computable` / `Turing.TM2ComputableInTime` (TM + `time : ℕ → ℕ` + proof) | the model half of Thm 4.1 |

**Key structural finding.** Mathlib's domination proof is built on the **unary +
pairing** formulation of PR. Its composition bound is the **max** form, and its
recursion step lands at a constant `max a b + 9` (via `ack_pair_lt`,
`ack_add_one_sq_lt_ack_add_three`). The essay's proof is the **multivariate** textbook
one with the **sum** bound `x+y+2` and a `+1` level. These are the *same theorem in two
formulations*. The file's own doc comment admits it: *"We aren't able to use the same
bounds as in that proof though, since our approach of using pairing functions differs
from their approach of using multivariate functions."*

**Bridge correction (verified at v4.32.0).** The original plan named the bridge
`Nat.Primrec'` / `Nat.Primrec'.prim_iff`. **That does not exist in v4.32.0** — it appears
only as a forward-reference doc comment in `Primrec/Basic.lean`. The working bridge in
this rev is **`Nat.Primrec₂`** (the 2-ary predicate, defined as
`Primrec fun p : α × β => f p.1 p.2`) with **`Primrec₂.mk`** (a binary `f` is PR iff its
curried version is `Nat.Primrec`). v4's §5.x uses `Nat.Primrec₂`/`Primrec₂.mk` as the
bridge, not `prim_iff`. (The essay keeps its multivariate proof as the star and presents
Mathlib's unary+pairing proof as a parallel development — the mismatch becomes a feature.)

**Consequence (the checkable claim that becomes verified Lemma 5.2):** the essay's exact
composition bound is a **two-line corollary** of the existing lemma:

```
ack x (ack y z) < ack (max x y + 2) z        -- ack_ack_lt_ack_max_add_two
              ≤ ack (x + y + 2) z            -- monotonicity in the 1st arg (max x y ≤ x + y)
```

So the essay's Lemma 5.2 is **proved in Lean in ~2 lines from
`ack_ack_lt_ack_max_add_two` + `ack_strictMono_left`** — no new machinery. Per r6, this
is a *named, verified* lemma in the body (B(i)), not just a remark.

---

## 2. Corrections to review v3_r5 (the referee pass) — unchanged, still valid

The r5 review is directionally right and its §2.C PR sketch *does* match Mathlib's real
`Nat.Primrec` API (zero/succ/left/right/pair/comp/prec — confirmed at v4.32.0). Its
errors, which v4 corrects:

1. **§2.B composition bound is mis-attributed.** The sketch
   `theorem ack_comp_bound (x y z) : ack x (ack y z) < ack (x + y + 2) z` is not an
   existing Mathlib lemma (Mathlib has the *max* form). v4 does not cite a lemma that
   isn't there; it **derives** the essay's form (§1, and now as verified Lemma 5.2).
2. **"Totality is handled automatically by Lean's termination checker!"** — true that the
   `def` compiles, but the well-founded relation the checker synthesises is the nested/
   lexicographic one on `(m,n)`, which is *exactly* what the essay's §2.2 double
   induction mirrors. v4 presents the contrast (human constructive proof vs checker's
   automated witness), not "the checker said so."
3. **"Theorem 4.1 … groundbreaking."** Overclaim. Mathlib *does* have
   `PartrecToTM2.tr_eval` (Partrec ⇒ TM, poly-time) and the `TM2ComputableInTime` model.
   What is genuinely new is the **← direction in the PR-clock form** (configuration
   coding + bounded iteration ⇒ `Nat.Primrec`). v4 scopes it precisely and drops
   "groundbreaking" for "the ← direction is not, as far as we can find, a single
   existing Mathlib theorem; we state it as a frontier item."
4. **"LeanInk *or* Alectryon."** They are a *stack*, not alternatives: Alectryon's Lean 4
   support **requires** LeanInk. v6. §6 states the dependency.
5. **§2.A row-4 gap.** Mathlib proves `ack_one/ack_two/ack_three` (rows 0–3). The essay's
   table (2) goes to row 4 (tetration). v4 marks row 4 as the one row left to the reader
   (or proves it as a new `simp` lemma if desired) — it must not imply Mathlib has it.
6. **Tone.** v4's own text keeps the essay's existing discipline (no decorative claims).
   Every formalization claim in v4 is either *verified* or *explicitly marked frontier*.

---

## 3. The two-formulation spine (v4's structural decision) — Option B, confirmed by r6

- **(A) Follow Mathlib** (unary+pairing): the Lean layer mirrors `Ackermann.lean`
  lemma-for-lemma. Lowest effort, but the essay's prose (multivariate) and its Lean
  (unary+pairing) *disagree in the details*, which a careful reader will object to.
- **(B) Keep the essay's multivariate proof as the star** and add the unary+pairing
  Mathlib proof as a **parallel development**, with `Nat.Primrec₂`/`Primrec₂.mk` as the
  explicit bridge. More work, but it *resolves* the mismatch into a feature: "here is
  the clean textbook proof (what you read), here is the machine-checked proof (what
  Mathlib checks), and here is the two-line argument that the formulations are the same
  class."

**Decision (r6-confirmed): (B).** The bridge is `Nat.Primrec₂` + `Primrec₂.mk` (one
existing definition + one lemma) plus a short remark; the extra cost is bounded.

Concretely, v4 restructures §5 as:

- §5 (informal, unchanged from v3): multivariate domination, sum bound, `+1` level.
- §5.x "The same theorem, machine-checked": the Mathlib unary+pairing development,
  `Nat.Primrec₂`/`Primrec₂.mk` bridge, the max bound, the `+9` recursion constant, and the
  **verified two-line derivation of the essay's sum bound from the max bound** (Lemma 5.2).

---

## 4. Section-by-section mapping (essay § → Lean), at Mathlib `v4.32.0`

| Essay § | Lean layer (source: `Mathlib/Computability/…` @ v4.32.0) |
|---|---|
| 2 (def, totality) | `#check ack`; note termination checker; `#eval ack 3 4` (small); contrast with Prop 2.1 double induction | `Ackermann.ack` |
| 2.1 (rows) | `ack_one/ack_two/ack_three` as `simp` lemmas; **row 4 = exercise** (not in Mathlib) | `Ackermann` |
| 2.2 (monotonicity) | `ack_strictMono_right` / `ack_strictMono_left`; one-line `#check` of both | `Ackermann` |
| 3 (machine) | present `M_A` (essay's stack machine) as the *conceptual* machine; note Mathlib proves computability via the Partrec code `pappAck` + `computable₂_ack`; `#check computable₂_ack` | `Ackermann` + `PartrecCode` |
| 4 (Thm 4.1) | **state** the theorem; ⇒ half (PR ⇒ PR-clock TM) *informally* as in v3; Partrec⇒TM half via `PartrecToTM2.tr_eval`; **← half (PR-clock ⇒ PR) marked Frontier (B(iii))** | `ToPartrec`, `Computable` |
| 5.1 (each row PR) | induction on `k` as a Lean `induction k` sketch; note Mathlib has no single "each fixed row is PR" lemma — a small gap v4 may fill with a 1-line lemma | — |
| 5.2 (composition bound) | **PROVE the essay's sum bound as named verified Lemma 5.2** (~2 lines from `ack_ack_lt_ack_max_add_two` + `ack_strictMono_left`) — this is B(i), now in the body | `Ackermann` |
| 5.3 (domination) | **mirror** `exists_lt_ack_of_nat_primrec`; show the `induction hf` structure; call out the `+9` recursion constant and the pairing helpers | `Ackermann` |
| 6 (Thm 6.1, diag) | **mirror** `not_primrec₂_ack` / `not_nat_primrec_ack_self`; show the 3-line contradiction | `Ackermann` |
| 7 (proof theory) | no Lean layer (FGH/ε₀ not in Mathlib's Computability); prose-only, as in v3 | — |

---

## 5. Scope (r6: Tier A + B(i); B(ii), B(iii) → Frontier)

**Tier A — verified mirror (the spine; ship first).**
Every in-essay Lean snippet is (i) a reference to an existing Mathlib lemma, or
(ii) a one-to-few-line derivation from one. All compiled, all labelled verified.
Theorem 4.1 is *stated*, its Partrec⇒TM half shown via `tr_eval`, and the ← half
deferred to the Frontier. *Effort: ~1 day including the build (short, because
`v4.32.0` is already built locally). Risk: low. Fully verifiable now.*

**B(i) — sum composition bound (r6: include).**
Promoted from "Tier B" into the verified body: a named lemma
`ack x (ack y z) < ack (x + y + 2) z`, proved in ~2 lines from
`ack_ack_lt_ack_max_add_two` + `ack_strictMono_left`. This makes the essay's *specific*
bound (Lemma 5.2) a verified claim, not just an informal remark.

**Frontier — B(ii), B(iii) (stated, not proven; separate `.lean`, referenced).**

- **B(ii)** the **multivariate** domination theorem in the essay's exact form, via
  `Nat.Primrec'` — *moderate* (port the v3 §5.3 proof; makes the essay's *own* proof the
  formal one, not just Mathlib's pairing version).
- **B(iii)** **Theorem 4.1's ← direction**: "TM computes `f` within a PR time bound `t`
  ⇒ `f` is `Nat.Primrec`," via Gödel-coding of TM configs, PR-ness of the one-step
  transition, and bounded iteration. *Substantial* (the genuine contribution; Mathlib has
  the ingredients — `TM2ComputableInTime`, config encoding — but not this theorem as a
  single statement). Likely several hundred lines; effectively a standalone Mathlib PR.

The Frontier section (a) states each theorem, (b) lists exactly what Mathlib already
provides, (c) gives the essay's informal proof as the argument for the new lemma, and (d)
links the repo file once completed. Only Tier A + B(i) are claimed "verified."

---

## 6. Verification & tooling protocol (pinned, reproducible)

1. **Pin (r6, corrected):** `lakefile.toml` requires `mathlib` `rev = "v4.32.0"`;
   `lean-toolchain` = `leanprover/lean4:v4.32.0` (already installed via elan; already
   built → 8674 oleans at `openai/ten-prrofs/.lake`, reused by the new project's build).
   Do **not** use `master`/`nightly` (master→Lean 4.34.0-rc2, unbuilt, slow).
2. **Fresh `lake` project** `ack-lean/` (do not edit the `openai/ten-prrofs` project).
   `lake build` — short here because the `v4.32.0` mathlib is pre-built.
3. **Every snippet compiles** before it is marked verified. Snippets that are
   illustrative-only (e.g., the §3 `M_A` sketch) are marked `-- sketch, not compiled`.
4. **Alectryon + LeanInk** render the interactive page:
   `alectryon --frontend md --backend webpage ack-essay.md -o ack-essay.html`
   (Lean 4 support **requires** LeanInk installed). **Primary deliverable = static
   `.md`** (r6: durable, reads anywhere); the HTML is the bonus, non-blocking.
5. **CI / reproducibility:** a `justfile` (or `Makefile`) with targets `build` (lake)
   and `render` (alectryon); the Mathlib rev and Lean toolchain are pinned in the repo so
   the "verified (Lean 4.32.0, Mathlib @ v4.32.0, <date>)" banner is reproducible.

---

## 7. Prose changes v4 forces (beyond adding code)

- **§2.2**: add the Lean contrast (human double induction vs checker witness); keep the
  human proof as primary.
- **§3.1**: note Mathlib proves computability via the Partrec *code*, not a raw TM;
  present `M_A` as the conceptual machine. (Pre-empts "your machine isn't the one in
  Mathlib.")
- **§4**: restate the scope of "no PR time bound" (already careful) and *add* the precise
  Frontier note: what `PartrecToTM2` gives vs what B(iii) would add. Drop any
  "groundbreaking" framing.
- **§5.2**: the sum composition bound is now a **verified named lemma** (B(i)); the
  two-line derivation from the max bound is shown inline.
- **New §5.x**: the two-formulation bridge (multivariate ↔ unary+pairing via
  `Nat.Primrec₂`/`Primrec₂.mk`), the max-vs-sum bound, the `+9` constant.
- **§5.4 / §7**: unchanged (prose-only; no FGH/ε₀ in Mathlib).
- **References**: add the Mathlib file paths + rev (`v4.32.0`), `ToPartrec`,
  `Primrec.Basic`, and the Alectryon/LeanInk tools; keep the v3 references.

---

## 8. Decision points — resolved by r6 (no further call needed)

1. **Scope:** Tier A + B(i). B(ii), B(iii) → Frontier. ✅
2. **Delivery:** both — static `.md` first (source of truth), Alectryon/LeanInk HTML
   second (bonus). ✅
3. **Mathlib rev:** pinned to stable **`v4.32.0`** (toolchain 4.32.0) — the closest stable
   tag to 4.33.1 that is *already built locally*; no tag matches 4.33.1 exactly. ✅

---

## 9. First execution steps

1. `lake new ack-lean`; `lakefile.toml` → `mathlib rev = "v4.32.0"`; `lean-toolchain` →
   `leanprover/lean4:v4.32.0`.
2. `lake build` (short: reuses the pre-built `v4.32.0` mathlib).
3. Write `AckEssay.lean` with the Tier A snippets + **named Lemma 5.2 (B(i) sum bound)**;
   compile; iterate until green.
4. Weave snippets into a v4 draft of the markdown (v3 text + §5.x + the §2/§3/§4 prose
   corrections + the verified Lemma 5.2).
5. Render Alectryon HTML (bonus); write the `justfile`; tag the verified banner
   (`Lean 4.32.0, Mathlib @ v4.32.0, <date>`).
6. (Later, if requested) execute Frontier B(ii), then B(iii), each in its own `.lean`.
