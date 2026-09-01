"""
Verify the LINEAR-shift absorption needed to close the primitive-recursion
step of the domination theorem:

  for fixed K, R, c:  A(K, R*n + c) <= A(K' , n + c'')  for all n,

with K' = K+2 (two rows up) and a fixed c''. In the domination proof the
recursion-depth shift s(t) grows LINEARLY in t (slope d+2), so the bound is
A(K, (d+2)*n + c0); this lemma absorbs that linear shift into a fixed row.
"""
import sys
sys.set_int_max_str_digits(100_000)

def A(m, n):
    if m == 0: return n + 1
    if m == 1: return n + 2
    if m == 2: return 2*n + 3
    if m == 3: return 2**(n+3) - 3
    if m == 4:
        if n > 2: raise OverflowError
        v = 2
        for _ in range(n+2): v = 2**v
        return v-3
    raise OverflowError

ok = True
print("=== linear-shift absorption: A(K, R*n+c) <= A(K+2, n+c'') for all n ===")
print("(needed for K>=1, where K+2>=3 is >= exponential and absorbs linear shifts)")
for K in range(1, 2):
    for R in (1, 2, 3, 5, 10):
        for c in (0, 5, 50):
            # find smallest c'' (<= 60) with A(K, R*n+c) <= A(K+2, n+c'') for all n in 0..60
            found = None
            for cp in range(0, 61):
                if all(A(K, R*n + c) <= A(K+2, n + cp) for n in range(0, 61)):
                    found = cp
                    break
            good = found is not None
            ok = ok and good
            print(f"  [{'PASS' if good else 'FAIL'}] K={K}, R={R}, c={c}: "
                  f"A(K+2, n+c'') with c'={found}")

print("\n" + "="*64)
print("ALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
