# Ackermann - Turing review 2

The essay’s central characterization is good, but in its present form I would **not call it acceptably accurate as a mathematical essay**, because several important statements are false or materially overstated. The errors are fixable without changing the core story. The strongest parts are §§2–4 and the diagonal idea in §6; the weakest are §5’s formal domination proof and almost all of the proof-theoretic interpretation in §7. 

The central statement you want is indeed standard:

$$
\mathrm{PR}\subsetneq\{\text{total computable functions}\},
$$

and an Ackermann function is the canonical textbook witness: it is total and computable by a Turing machine, while not primitive recursive. Moreover, there is a legitimate machine-theoretic characterization behind your “PR clock” idea: a function is primitive recursive iff it can be computed by an appropriately encoded Turing machine with a primitive-recursive running-time bound. A recent paper gives exactly this characterization, although the result is older folklore/textbook material. ([arXiv][1])

There are, however, five substantial corrections I would make.

1. **Lemma 1 in §5.1 is false.** You write:

> “The function \(\Phi(m,n)=F_m(n)\) is primitive recursive.”

It cannot be. Each **fixed** finite-level function \(F_m(\cdot)\) is primitive recursive, but the *uniform two-variable function* \((m,n)\mapsto F_m(n)\) is not primitive recursive. Indeed, its diagonal \(n\mapsto F_n(n)\) is essentially Ackermannian and dominates every primitive-recursive function. This distinction—“every fixed row is PR, but the family uniformly indexed by its row number is not”—is precisely the phenomenon the essay is trying to explain. Standard descriptions identify \(F_\omega(n)\), obtained by diagonalizing the finite levels, with an Ackermann-type growth rate. ([Biblio][2])

The purported proof of Lemma 1 hides this mistake. An induction saying “for each numeral \(m\), \(F_m\) is PR” establishes a **metatheoretic family of separate PR definitions**. It does not produce one PR function \(\Phi(m,n)\) with \(m\) as an input. So this needs to become something like:

> For every fixed \(m\in\mathbb N\), \(F_m:\mathbb N\to\mathbb N\) is primitive recursive.

That correction actually makes your overall narrative cleaner.

2. **The proof of Lemma 2 is not currently valid.** The theorem itself—every PR function is eventually dominated by a fixed Ackermann row—is standard and exactly the right theorem to use. But the primitive-recursion case in your proof mishandles the parameter in the iteration bound.

You have

$$
T_{x,t}(z)\le A(b,z+(\langle x\rangle+t)),
$$

and then invoke an iteration lemma requiring an additive constant \(C\) independent of the iteration variables. Here \(C=\langle x\rangle+t\) is not a constant: it varies with the input and, crucially, with \(t\). The next displayed bound also appears to lose the potentially much larger initial value \(g(x)\le A(a,\langle x\rangle)\).

This is repairable, but I would not improvise the proof in this form. Either cite the standard majorization theorem for primitive-recursive functions by the finite fast-growing/Grzegorczyk hierarchy, or give a carefully formulated simultaneous induction with sufficiently generous shifts and levels. The diagonal proof in §6 then becomes only a few lines.

3. **The resource interpretation is basically correct, but you overstate what “no PR time bound” means.** The valid consequence is:

$$
A\notin\mathrm{PR}
\quad\Longrightarrow\quad
\text{there is no PR function }t\text{ which upper-bounds the running time of a TM computing }A.
$$

That does **not**, merely by logic, mean that the runtime of every such machine “runs for more than any PR function” in the usual eventual-domination sense. “Not bounded above by any PR function” and “eventually dominates every PR function” are different assertions. Your Corollary 1 supports the former. So passages such as

> “every Turing machine computing \(A\) runs for more than any PR function of its input”

should instead say:

> “no Turing machine computing \(A\) has a primitive-recursive upper bound on its running time.”

That is both exact and sufficiently striking.

There is also an encoding subtlety in Theorem 1: \(t(|x|)\) makes the complexity bound a function of *representation length*, while primitive-recursive functions are conventionally functions of numerical arguments. This can be made consistent, but you should specify the coding convention carefully. The theorem is safest when stated as a PR bound in the encoded numerical inputs or with an explicit representation model.

4. **The PA discussion badly mislocates Ackermann in the fast-growing hierarchy.** Ackermann is not near the \(\varepsilon_0\) boundary of PA. An Ackermann diagonal is roughly the **\(F_\omega\)** level (depending on normalization), whereas PA proves the totality of \(F_\alpha\) for every fixed \(\alpha<\varepsilon_0\), and every PA-provably total recursive function is eventually dominated by some such \(F_\alpha\). Thus there is an enormous ordinal gap

$$
\omega \ll \varepsilon_0.
$$

Sources on the standard hierarchy explicitly identify Ackermannian growth with \(F_\omega\), while the characterization of PA extends all the way through the ordinals below \(\varepsilon_0\). ([Biblio][2])

Consequently these claims should go:

> “\(A\) is thus the threshold object [for PA].”

and

> “proving its totality requires induction over the whole finite initial segment of the hierarchy up to \(\varepsilon_0\)—the full strength of PA's provable totality.”

Ackermann is a natural threshold for the **primitive-recursive functions**, not for the provably total functions of PA. A more precise proof-theoretic observation is that Ackermann totality is provable in PA but is not provable in theories whose provably total functions are exactly the primitive-recursive ones; for example, \(I\Sigma_1\) has exactly the primitive-recursive provably recursive functions. ([Biblio][2])

Relatedly, §7.1 says that all PR functions are provably total “already in fragments with only \(\Delta_0\) or \(\Sigma_1\) induction.” That lumps together theories of very different strength. In the usual first-order language, \(I\Delta_0\) does **not** prove totality of all primitive-recursive functions—for example, exponentiation creates the standard difficulty. \(I\Sigma_1\), on the other hand, has the relevant primitive-recursive provably-total characterization. That sentence needs substantial qualification.

5. **The hydra section reverses the Kirby–Paris theorem.** This is the most conspicuous factual error. You state:

> “the statement ‘the hydra game always terminates’ is provable in PA but not in the weaker \(\Delta_0\)-induction fragment.”

The famous Kirby–Paris result is precisely that the appropriate hydra termination theorem is **not provable in PA**. A stronger metatheory can prove termination using well-foundedness up to \(\varepsilon_0\). Modern summaries and the proof-theoretic literature state the independence from PA explicitly. ([ScienceDirect][3])

Likewise, the hydra battle-length function is vastly faster than ordinary Ackermann \(A(n,n)\). Suitable hydra length functions eventually dominate **all PA-provably total recursive functions**, whereas Ackermann sits around \(F_\omega\) and is itself PA-provably total. ([Wikipedia][4]) So the sentence saying the number of hydra moves grows “hence like \(A(n,n)\)” should be removed.

A few smaller issues are worth cleaning up as well. The statement in §3.2 that Ackermann’s recursion is “general rather than primitive” is directionally fine, but primitive recursion versus general/\(\mu\)-recursion is not best characterized simply by “data-dependent recursion depth”; nested recursion is a more precise description of the displayed Ackermann definition. Also, the proof sketch after the low-row table says “by induction on \(m\)” but then assumes the specific formula \(A(m,n)=2n+3\), so it is really demonstrating the \(m=2\to3\) case, not giving an induction over arbitrary \(m\). And the conclusion calls \(A\) a “canonical, minimal witness,” contradicting your earlier and correct warning that it is not minimal. I would delete “minimal.”

I would therefore recast the conceptual backbone as follows:

$$
\boxed{
\begin{array}{c}
\text{each fixed Ackermann row }A_k(n)\text{ is primitive recursive},\\[2mm]
\text{every primitive-recursive function is eventually dominated by some fixed row},\\[2mm]
A(n,n)\text{ diagonalizes through those rows and is therefore not PR},\\[2mm]
A(n,n)\text{ nevertheless is total computable, hence Turing-computable}.
\end{array}}
$$

Machine-theoretically, this gives the very nice secondary characterization that although some TM computes Ackermann and halts on every input, **there is no primitive-recursive function serving as a uniform upper bound on the running time of any such TM**. Proof-theoretically, the appropriate statement is that Ackermannian growth corresponds roughly to the first limit \(F_\omega\), well above all finite levels governing PR growth but **far below** the \(\varepsilon_0\) frontier associated with PA. ([Biblio][2])

So I would rate the current essay as **conceptually strong but mathematically not yet reliable enough to circulate without revision**. §§1–4 contain a good exposition with some qualifications needed; the diagonal strategy in §6 is exactly the right one once the domination theorem is repaired; §5.1’s uniform-\(F_m\) lemma must be corrected; and §7.2 should essentially be rewritten because Ackermann and Kirby–Paris hydras occupy very different proof-theoretic scales. 

If your aim is specifically a crisp “characterisation of the relationship between Ackermann and Turing machines,” I’d also recommend **shortening rather than expanding** the proof-theoretic material: the PR/TM-time-bound equivalence plus the fixed-level-versus-diagonal distinction gives you the strongest and cleanest answer to that question.

[1]: https://arxiv.org/abs/2510.18283?utm_source=chatgpt.com "A Characterization of Turing Machines that Compute Primitive Recursive Functions"
[2]: https://backoffice.biblio.ugent.be/download/1230584/4335572?utm_source=chatgpt.com "Faculty of Sciences"
[3]: https://www.sciencedirect.com/science/article/pii/S0304397502003328?utm_source=chatgpt.com "A new proof-theoretic proof of the independence of Kirby–Paris’ Hydra Theorem - ScienceDirect"
[4]: https://en.wikipedia.org/wiki/Hydra_game?utm_source=chatgpt.com "Hydra game"
