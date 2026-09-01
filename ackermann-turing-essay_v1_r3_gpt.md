# Ackermann - Turing review 3

You’re right to be skeptical. That script does **not** provide an alternative to the fast-growing hierarchy argument, and it does not establish the central mathematical claims of the essay. It is mainly a **sanity-checking script for small numerical instances and closed forms**.

Its useful role is narrower: it can catch arithmetic mistakes such as \(F_2(n)=2^n n\), confirm \(A(4,1)=65533\), check the digit count of \(A(4,2)\), and test a proposed inequality on a few small arguments. Those are worthwhile checks, especially because these functions become too large for intuitive arithmetic very quickly.

But several lines in the script sound much stronger than what the computation establishes. For example:

```python
print("=== (7) Uniform Phi(m,n)=F_m(n) is NOT PR:
       diagonal F_n(n) dominates every fixed level ===")
```

followed by checking only \(m=0,1\) and \(n\le2\), obviously does **not prove** that \(n\mapsto F_n(n)\) dominates every fixed \(F_m\), nor that the uniform \(\Phi(m,n)\) is non-PR. Those are mathematical theorems requiring an argument about the hierarchy. The numerical check merely confirms that the theorem is not immediately contradicted by tiny cases.

The same applies to the key inequality

$$
F_b\bigl(u+F_{b+1}(v)\bigr)\le F_{b+1}(v+1).
$$

The script checks essentially one level, \(b=1\), for \(v\le6\). If that inequality is meant to close a structural-induction proof for **arbitrary** primitive-recursive functions, what matters is a proof valid for every relevant \(b,u,v\), not six numerical examples.

So I would separate two quite different jobs.

The **FGH/Ackermann-row argument supplies the theorem**:

$$
\text{every PR function is dominated by some fixed level},
$$

while

$$
n\mapsto F_n(n)
\quad\text{or}\quad
n\mapsto A(n,n)
$$

escapes every fixed level. Therefore the diagonal is not primitive recursive.

The Python script merely says, approximately:

> “Here are some low-level numerical checks showing that the formulas and inequalities used in that theoretical argument behave as claimed on small examples.”

That is supporting material, not an alternative proof.

Indeed, there is a slightly ironic point here: **you cannot computationally demonstrate the key phenomenon in any convincing numerical range**, because the hierarchy becomes infeasible almost immediately. The script itself admits this when it avoids \(F_3(3)\) and higher values. The whole reason one introduces a hierarchy such as \(F_m\) is precisely to reason symbolically about growth that cannot be explored numerically.

For your essay, I think the cleanest route is actually to **avoid making the FGH do too much**. The Ackermann rows themselves already give you the important characterization:

$$
A_0,\ A_1,\ A_2,\ldots
$$

are each primitive recursive when the first argument is fixed, while a standard domination theorem says that for every primitive-recursive \(f\), there is some fixed \(k\) such that, up to harmless argument shifts,

$$
f(n)\le A(k,n).
$$

Then the diagonal immediately escapes:

$$
A(n,n)>A(k,n)\qquad(n>k).
$$

That is the essential proof. The FGH can then appear afterward as a conceptual comparison:

> The finite levels of the fast-growing hierarchy provide another standard exhaustion scale for the primitive-recursive functions; diagonalization through the finite levels produces Ackermannian growth.

This is substantially clearer than trying to prove a collection of fairly technical FGH inequalities and then supplementing them with Python checks.

There is also an important distinction that the script itself now gets right, and that should be prominent in the essay:

$$
\boxed{\text{For every fixed }m,\quad F_m(\cdot)\text{ is PR}}
$$

but

$$
\boxed{(m,n)\mapsto F_m(n)\text{ is not PR}.}
$$

That distinction is almost the entire Ackermann phenomenon in miniature. If the uniform function were PR, its diagonal \(n\mapsto F_n(n)\) would also be PR; but the diagonal escapes every fixed level.

So I would not ask the reader to run this script as part of the argument. At most, put a sentence or footnote saying that low-level formulas and numerical examples were machine-checked. The mathematical exposition should stand entirely without it.

A compact structure for the essay could therefore be:

1. Define primitive recursion and Ackermann.
2. Show each fixed row \(A(k,\cdot)\) is PR.
3. State/prove the domination theorem: every PR function is bounded by a fixed Ackermann row.
4. Diagonalize: \(A(n,n)\) escapes every fixed row, hence is not PR.
5. Note that Ackermann is nevertheless total recursive/Turing-computable.
6. Derive the TM consequence: **no TM computing it can have a primitive-recursive uniform running-time bound.**
7. Mention the FGH only to locate this phenomenon conceptually: finite levels correspond to the PR exhaustion; Ackermannian diagonalization sits around \(F_\omega\).

That would make the relationship with Turing machines much more visible than the long verification script does.
