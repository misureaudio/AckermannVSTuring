# Ackermann - Turing review 4

##

Yes. The script is an improvement over the version implied by the earlier essay criticism, because it now explicitly acknowledges one of the key points:

```text
Uniform Phi(m,n)=F_m(n) is NOT PR
```

and it treats the diagonal \(n \mapsto F_n(n)\) as the source of non-primitive-recursiveness rather than claiming \(\Phi\) itself is primitive recursive.

However, I would still regard it as **evidence for the intended argument, not the argument itself**.

A few observations:

### What is better

The script now reflects the correct conceptual structure:

* Each fixed level \(F_m\) is primitive recursive.
* Levels are monotone.
* Composition of lower levels remains bounded by a higher level.
* The diagonal \(F_n(n)\) escapes every fixed level.

That is much closer to the standard fast-growing-hierarchy proof strategy.

In particular, item (7)

```python
F_n(n) > F_m(n) for n>m
```

is at least pointing at the right theorem, whereas the earlier essay version effectively confused fixed levels with the uniform family.

---

### What it still does not prove

The script repeatedly verifies statements such as

```python
for v in range(2,7):
```

or

```python
n in range(1,7)
```

and then reports "PASS".

Mathematically, that establishes only

$$
\text{the claim holds for a handful of small cases.}
$$

But the proof requires

$$
\forall n,\forall m,\forall p,\forall q,\dots
$$

which is a completely different statement.

For example:

```python
F_p(F_q(n)) <= F_{p+q+2}(n)
```

checked for \(p,q\le2\) and \(n\le6\)

does not establish the theorem for arbitrary \(p,q,n\).

Likewise:

```python
F_b(u + F_{b+1}(v)) <= F_{b+1}(v+1)
```

checked only for \(b=1\)

does not justify its use in a general induction over primitive-recursive definitions.

---

### The deepest issue

The script cannot replace the domination theorem because the domination theorem is inherently symbolic.

The theorem you need is something like:

> Every primitive-recursive function is eventually bounded by some finite level of the hierarchy.

No finite computation can verify that statement. There are infinitely many primitive-recursive functions.

The script can only test whether your proposed lemmas are *consistent with small examples*.

---

### How I would use it

If I were revising the essay, I would move the script to an appendix and describe it as:

> "A collection of computational checks of low-level formulas and sample instances of the hierarchy inequalities used in the proof."

I would not present it as verification of the theorem itself.

The mathematical proof should still be:

1. Every fixed row \(A(k,\cdot)\) (or \(F_k\)) is primitive recursive.
2. Every primitive-recursive function is eventually dominated by some fixed row.
3. The diagonal \(A(n,n)\) (or \(F_n(n)\)) exceeds every fixed row.
4. Therefore the diagonal is not primitive recursive.
5. Yet it is computable by a Turing machine.

That argument stands on its own. The script is then a nice consistency check, not a substitute for the hierarchy.

So my verdict would be: **yes, it is an improvement, and it no longer contains the glaring "uniform \(\Phi\) is PR" mistake—but it still cannot carry the proof burden that the essay needs.**
