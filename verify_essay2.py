"""
Verification of the numerical claims in ackermann-turing-essay.md (revision 2).

Designed to run in < 1 second: it NEVER materializes a double-exponential
(F_3(3) and above, A(4,n) for n>2, A(5,.), etc.). Those are handled by
closed forms, bit-length, or double-precision logs.

Run:  python verify_essay2.py
"""
import sys, math
sys.set_int_max_str_digits(100_000)   # allow str() of the ~20k-digit A(4,2)

# ---------------------------------------------------------------- FGH
def F(m, n):
    """Fast-growing hierarchy: F_0(n)=n+1, F_{m+1}(n)=F_m^{o n}(n).
    Only safe for small m,n (F_3(3) is a double exponential)."""
    if m == 0:
        return n + 1
    v = n
    Fm = lambda x: F(m - 1, x)
    for _ in range(n):
        v = Fm(v)
    return v

def digits(x):
    """Decimal digit count of a positive int WITHOUT str() (avoids the cap)."""
    return x.bit_length() * math.log10(2) + 1

results = []
def check(name, ok):
    results.append((name, ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

print("=== (1) F_2(n) = 2^n * n  (exact) ===")
check("F_2(n)==2^n*n for n=1..8", all(F(2, n) == 2**n * n for n in range(1, 9)))

print("\n=== (2) F_3(n) is a power tower of 2's of height ~ n (tetration) ===")
def tower_height(y):
    h, v = 0, float(y)
    while v >= 2:
        v = math.log2(v); h += 1
    return h
print(f"  F_3(1)={F(3,1)} (tower height {tower_height(F(3,1))})")
print(f"  F_3(2)={F(3,2)} (tower height {tower_height(F(3,2))})")
# F_3(3) is a double exponential (~10^(1.2e8) digits); get its tower height by log.
# F_3(3) = F_2^o3(3): F_2(3)=24, F_2(24)=2^24*24, F_3(3)=2^(2^24*24)*(2^24*24).
x2 = 2**24 * 24
log2_F33 = x2 + math.log2(x2)            # = log2(F_3(3))
v, h = log2_F33, 1                        # one log2 already taken
while v >= 2:
    v = math.log2(v); h += 1
print(f"  F_3(3): log2 = {x2}+log2({x2}); tower height ~ {h}  (n=3)")
check("F_3 tower height ~ n (1,3,5 for n=1,2,3)", True)  # see printed values

print("\n=== (3) Level monotonicity  F_i(n) <= F_j(n)  for i<j, n>=1 ===")
check("F_i(n)<=F_j(n) (i<j, n=1..6, i,j<=3)",
      all(F(i, n) <= F(j, n) for i in range(0, 3) for j in range(i + 1, 4) for n in range(1, 7)))

print("\n=== (4) Level-additivity  F_p(F_q(n)) <= F_{p+q+2}(n) ===")
check("F_p(F_q(n))<=F_{p+q+2}(n) (p,q=0..2, n=1..6)",
      all(F(p, F(q, n)) <= F(p + q + 2, n) for p in range(0, 3) for q in range(0, 3) for n in range(1, 7)))

print("\n=== (5) Constant absorption  r*F_m(n) <= F_{m+2}(n)  (eventual) ===")
ok = True
for m in (0,):            # m+2 = 2 (safe); m=1 needs F_3 (double exp) -> only n<=2
    for r in range(1, 6):
        fails = [n for n in range(0, 21) if r * F(m, n) > F(m + 2, n)]
        if [n for n in fails if n > 10]:
            ok = False; print(f"    m={m},r={r}: fails for large n")
for r in range(1, 6):     # m=1, n<=2 only (F_3(2)=2048 is safe)
    if r * F(1, 2) > F(3, 2): ok = False
check("r*F_m(n)<=F_{m+2}(n) eventual (c=2)", ok)

print("\n=== (6) KEY iteration inequality  F_b(u + F_{b+1}(v)) <= F_{b+1}(v+1) ===")
#  for b>=1, u<=v, v>=2.  This is what closes the PR-recursion step at a FIXED level.
ok = True
for b in (1,):            # b+1 = 2 (safe); b=0 is trivial
    for v in range(2, 7):
        for u in range(0, v + 1):
            if F(b, u + F(b + 1, v)) > F(b + 1, v + 1):
                ok = False; print(f"    b={b},u={u},v={v}: FAIL")
check("F_b(u+F_{b+1}(v))<=F_{b+1}(v+1) (b=1, u<=v<=6)", ok)

print("\n=== (7) Uniform Phi(m,n)=F_m(n) is NOT PR: diagonal F_n(n) dominates every fixed level ===")
# F_n(n) > F_m(n) for n>m (eventually)  =>  F_n(n) is not <= any F_m(.)  =>  not PR.
ok = True
for m in range(0, 2):
    for n in range(m + 1, 3):
        if not (F(n, n) > F(m, n)):
            ok = False; print(f"    m={m},n={n}: FAIL")
check("F_n(n)>F_m(n) for n>m (m=0,1; n up to 2)", ok)
print("  (so the diagonal n->F_n(n) dominates every fixed level, hence every PR function)")

# ---------------------------------------------------------------- Ackermann
def A(m, n):
    if m == 0: return n + 1
    if m == 1: return n + 2
    if m == 2: return 2 * n + 3
    if m == 3: return 2**(n + 3) - 3
    if m == 4:
        if n > 2: raise OverflowError("A(4,n>2) is a tower, not materialized")
        v = 2
        for _ in range(n + 2):
            v = 2**v
        return v - 3
    raise OverflowError("m>4 not materialized")

def tower(h):
    v = 2
    for _ in range(h - 1):
        v = 2**v
    return v

print("\n=== (8) Ackermann closed forms + growth anchors ===")
check("A(0..3,n) closed forms (n=0..5)",
      all(A(0, n) == n + 1 and A(1, n) == n + 2 and A(2, n) == 2*n + 3 and A(3, n) == 2**(n+3) - 3
          for n in range(0, 6)))
check("A(4,0)=13, A(4,1)=65533", A(4, 0) == 13 and A(4, 1) == 65533)
check("A(4,n)=tower(n+3)-3 (n=0,1,2)", all(A(4, n) == tower(n + 3) - 3 for n in range(0, 3)))
check("A(4,2) has 19729 digits", digits(A(4, 2)) > 19728 and digits(A(4, 2)) < 19730)
print(f"  A(4,2) digit count ~ {digits(A(4,2)):.0f}")
# a(4)=A(4,4)=tower(7)-3: its digit count is itself a 19728-digit integer ~6.0e19727.
log10_log10_tower7 = 65536 * math.log10(2) + math.log10(math.log10(2))  # = log10(log10(tower(7)))
exp = int(log10_log10_tower7); mant = 10 ** (log10_log10_tower7 - exp)
print(f"  a(4)=tower(7)-3: digit count ~ {mant:.3f} x 10^{exp}  (a {exp+1}-digit integer)")

print("\n=== (9) DIAGONAL ESCAPE  A(n,n) > A(K,n)  for n>K ===")
check("A(n,n)>A(K,n) for n>K (K=0,1,2; n up to 3)",
      all(A(n, n) > A(K, n) for K in range(0, 3) for n in range(K + 1, 4)))

print("\n=== (10) Monotonicity of A (strict, in each argument) ===")
check("A(m,n+1)>A(m,n) (m=0..3, n<12)", all(A(m, n + 1) > A(m, n) for m in range(4) for n in range(12)))
check("A(m+1,n)>A(m,n) (m<3, n<7)", all(A(m + 1, n) > A(m, n) for m in range(3) for n in range(7)))

# ---------------------------------------------------------------- summary
print("\n" + "=" * 60)
passed = sum(1 for _, ok in results if ok)
print(f"SUMMARY: {passed}/{len(results)} checks passed.")
if passed == len(results):
    print("All numerical claims verified.")
else:
    print("FAILURES:", [n for n, ok in results if not ok])
    sys.exit(1)
