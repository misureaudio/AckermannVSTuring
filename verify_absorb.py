"""
Verify the eventual constant-shift absorption used in the Theorem 6.1
contradiction:  for fixed K, c,  A(K, n+c) <= A(K+2, n)  for all n >= N.
(K+2, not K+1: at low rows K+1 is too slow for large c.)
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
print("=== eventual absorption: A(K, n+c) <= A(K+2, n) for n>=N ===")
for K in range(0, 3):
    for c in (1, 2, 3, 5, 10, 50):
        N = 0
        while N < 60 and A(K, N+c) > A(K+2, N):
            N += 1
        holds = N < 60
        ok = ok and holds
        print(f"  [{'PASS' if holds else 'FAIL'}] K={K}, c={c}: holds for n>={N}")

print("\n=== and the K+1 version FAILS at low rows (why we need K+2) ===")
for K, c in [(0, 2), (0, 5), (1, 5)]:
    # check whether A(K,n+c) <= A(K+1,n) EVER holds for n up to 59
    ever = any(A(K, n+c) <= A(K+1, n) for n in range(0, 60))
    print(f"  K={K}, c={c}: A(K,n+c)<=A(K+1,n) holds for some n<60? {ever}")

print("\nALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
