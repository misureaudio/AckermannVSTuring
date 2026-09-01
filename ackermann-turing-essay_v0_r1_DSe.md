# Ackermann - Turing review 1

##

This is a highly accurate, beautifully structured, and pedagogically valuable expository essay. It correctly synthesizes the classic recursion-theoretic, computational, and proof-theoretic facets of the Ackermann function into a cohesive narrative. 

If I were grading or reviewing this for a journal or advanced textbook, I would give it high marks. Below is a breakdown of its accuracy, followed by my critical evaluation and minor corrections.

### 1. Accuracy Check (The Nitty-Gritty)

- **Definitions and Totality (§2)**: The Péter definition, the closed forms for rows 0–4, and the double-induction proof of totality are completely correct. The decimal digit count for \(A(4,2)\) (19,729 digits) is accurate.
- **Turing Computability (§3)**: The stack-based Turing machine description is valid. It correctly implements the nested recursion using a push-down stack, which a single-tape machine can simulate. 
- **Theorem 1 (PR = PR-bounded time)**: This is the critical bridge, and the logic is fundamentally sound. *Technical caveat*: The essay states "the map \( \text{cfg} \mapsto \text{cfg}' \) is PR, and therefore its \(s\)-fold iterate is PR in \( (\text{cfg}_0, s) \)." This is true, but only if you explicitly define the iterate via primitive recursion: \( g(y,0)=y \), \( g(y, s+1)=T(g(y,s)) \). Since the essay implies this rather than spelling out the formal definition, it is rigorous enough for an expository piece.
- **Fast-Growing Hierarchy (§5)** – **Contains a factual error**: 
  - The essay states \( F_2(n) \approx 2n^2 \) and \( F_3(n) \approx 2^{n} n^{2^{n}} \). 
  - **This is mathematically incorrect.** Given \( F_0(n)=n+1 \), \( F_1(n)=2n \), and \( F_2(n) = F_1^n(n) \), the exact value is \( F_2(n) = n \cdot 2^n \) (not \( 2n^2 \)). Consequently, \( F_3(n) = F_2^n(n) \) grows like a **power tower of 2's of height \( n \)** (i.e., tetration), not the comparatively tiny \( 2^{n} n^{2^{n}} \). 
  - *Why this matters*: The proof of Theorem 2 does not rely on these exact approximations; it only relies on the hierarchy strictly increasing and exhausting PR functions. So the *theorem* remains perfectly proven, but the illustrative "first levels" are objectively wrong and should be corrected in any revision.
- **Lemma 2 (Domination)**: The structural induction proof is standard and valid. The "level-additivity" \( F_p(F_q(n)) \le F_{p+q+1}(n) \) is a well-known property.
- **Lemma 3 and Theorem 2**: The proof that \( A \) is not PR via the diagonal \( A(n,n) \) outrunning \( F_{n-1}(n) \) is the classic, airtight proof. 
- **Proof Theory (§7)**: The statements regarding PA, \( \varepsilon_0 \), and the Kirby–Paris hydra are completely accurate. The provably-total functions of PA are indeed exactly those bounded by \( F_\alpha \) for \( \alpha < \varepsilon_0 \), placing \( A \) safely inside PA but outside the PR fragment.

---

### 2. My Critical Evaluation (The "Idea" about it)

The essay's greatest strength is its **tripartite thesis** (Function / Resource / Proof-theory). By framing \( A \) not just as a fast-growing function, but as the **canonical witness to the failure of PR-bounded time**, the author answers the titular question ("relation to the Turing machine") in the most substantive way possible. Many expositions stop at "it is computable but not primitive recursive"; this one correctly emphasizes that the *resource* characterization (Corollary 2) is the operational, machine-centric meaning of the divide.

**Strengths**:

- The prose is precise without being turgid. 
- The "stack machine" description is refreshingly explicit; many authors wave their hands at this step.
- The connection to the hydra game provides an intuitive, combinatorial anchor for why the growth is tied to ordinal \( \varepsilon_0 \).

**Potential Weaknesses / Points of Debate**:

1. **"The Exact Boundary" (Title)**: The essay claims \( A \) is the *exact* boundary. While it is the *canonical* boundary, mathematically speaking, there is a vast, dense zoo of total recursive functions between the PR functions and \( A \) (e.g., the sub-Ackermannian functions like the inverse Ackermann, or the Sudan function). In terms of *time complexity*, \( A \) is the first *natural* function to break the PR barrier, but it is not the immediate successor in a well-ordered sense. The title is rhetorically strong but slightly informal.
2. **Theorem 1 nuance**: The proof of the reverse direction (\( \Leftarrow \)) assumes that the Turing machine's configuration can be encoded as a fixed-length tuple of natural numbers, and that the transition function is primitive recursive. This is true for a one-tape machine with a fixed alphabet, but it requires a bit more formal coding than the essay provides. Given the target audience (logic/computability readers), this is an acceptable shorthand, but a purist might ask for an explicit Gödel encoding.

---

### 3. Suggested Corrections for a Revision

If this were to be published or used as lecture notes, I would strongly suggest the following changes:

1. **Fix the FGH approximations**:
   Change:
   \[
   F_2(n)\approx 2n^2, \quad F_3(n)\approx 2^{n} n^{2^{n}}
   \]
   To:
   \[
   F_2(n) = n \cdot 2^n, \quad F_3(n) \approx \text{a power tower of 2's of height } n.
   \]
   (Actually, proving the exact closed form for \( F_3 \) is tricky, so simply stating "approximately tetration" is safest.)

2. **Clarify the \( \mu \)-recursive reading (§3.2)**: The statement "the number of 'steps' is not bounded by a PR function" is the *conclusion* of the essay, not a premise of the \( \mu \)-recursive definition. Reword this to avoid circularity: say that the recursion is *general* because the depth of recursion depends on the computed value, but it is still *well-founded* (proved by the double induction).

3. **Minor citation**: The Goodstein reference (1947) is fine, but the hydra paper by Kirby and Paris is actually from 1982 (published in the *Logic Colloquium '81* proceedings, not exactly as cited, but close enough).

### Final Verdict

**Accuracy**: 98% (minus the \( F_2/F_3 \) numerical slip).  
**Quality**: Excellent. It is a model of clear, rigorous mathematical exposition. It successfully bridges the syntactic, operational, and proof-theoretic worlds, making it a perfect capstone reading for a graduate course in Computability Theory or Logic. The author clearly knows the material inside out.
