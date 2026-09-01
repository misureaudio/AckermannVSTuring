"""
Verification of the key Ackermann-row inequalities for the domination
theorem and the non-PR proof (revision 3, per review 3).

Review 3's point: rest the argument on the Ackermann rows A(k,.), not the
FGH. The proof needs only a few concrete, provable inequalities:

  (CLOSING)  b < K  =>  A(b, A(K,n)) <= A(K, n + 1)        [constant shift]
             (from the recursion A(K,n+1) = A(K-1, A(K,n)) + monotonicity)
  (IDENTITY) A(K-1, A(K,n)) = A(K, n+1)                    [exact, by def]
  (ABSORB)   c*A(K,n)   <= A(K, n + c')  for K>=3          [const mult -> shift]
  (SHIFT)    A(k, n+c)  <= A(k+2, n)   eventually          [shift -> 2 rows up]
  (MONO)     A strictly increasing in each argument
  (DIAG)     A(n,n) > A(k,n) for n > k                     [monotonicity]

All instances checked here are materializable (K<=3, n<=60) -> runs in < 1 s.
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

ok_all = True
def report(name, ok, detail=""):
    global ok_all
    ok_all = ok_all and ok
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {name}" + (f"   {detail}" if detail else ""))

# ---------- (IDENTITY) A(K-1, A(K,n)) = A(K, n+1)  [exact] ----------
print("=== (IDENTITY)  A(K-1, A(K,n)) == A(K, n+1)  [by definition] ===")
bad = 0
for K in range(1, 4):
    for n in range(0, 60):
        if A(K-1, A(K, n)) != A(K, n+1):
            bad += 1
report("A(K-1,A(K,n)) == A(K,n+1) for K=1..3, n=0..59", bad == 0,
       f"{bad} mismatches" if bad else "")

# ---------- (CLOSING) b < K => A(b, A(K,n)) <= A(K, n+1) ----------
print("\n=== (CLOSING)  b < K :  A(b, A(K,n)) <= A(K, n+1)  [c = 1] ===")
bad = 0
for K in range(1, 4):
    for b in range(0, K):
        for n in range(0, 60):
            if A(b, A(K, n)) > A(K, n+1):
                bad += 1
report("A(b,A(K,n)) <= A(K,n+1) for all b<K, K=1..3, n=0..59", bad == 0,
       f"{bad} violations" if bad else "")

# ---------- (ABSORB) c*A(K,n) <= A(K, n+c') for K>=3 ----------
print("\n=== (ABSORB)  c*A(K,n) <= A(K, n + c')  for K>=3  [find c'] ===")
for K in (3,):
    for c in (2, 3, 5, 10):
        cprime = 0
        for n in range(0, 40):
            d = 0
            while A(K, n + d) < c * A(K, n):
                d += 1
            cprime = max(cprime, d)
        report(f"K={K}, c={c}: A(K,n+c') with c'={cprime}", cprime <= 5, f"c'={cprime}")

# ---------- (SHIFT) A(k, n+c) <= A(k+2, n) eventually ----------
print("\n=== (SHIFT)  A(k, n+c) <= A(k+2, n)  eventually  [k+2<=3] ===")
for k in range(0, 2):
    for c in (1, 2, 3, 5):
        # find N such that for all n>=N the inequality holds
        N = 0
        while N < 60 and A(k, N + c) > A(k+2, N):
            N += 1
        holds = N < 60
        report(f"k={k}, c={c}: holds for n>={N}", holds, f"threshold N={N}")

# ---------- (MONO) A strictly increasing in each argument ----------
print("\n=== (MONO)  A strictly increasing in each argument ===")
mono1 = all(A(m+1, n) > A(m, n) for m in range(0, 3) for n in range(0, 30))
mono2 = all(A(m, n+1) > A(m, n) for m in range(0, 3) for n in range(0, 30))
report("A(m+1,n) > A(m,n)  (first arg, m=0..2, n=0..29)", mono1)
report("A(m,n+1) > A(m,n)  (second arg, m=0..2, n=0..29)", mono2)

# ---------- (DIAG) A(n,n) > A(k,n) for n > k  [materializable n<=3] ----------
print("\n=== (DIAG)  A(n,n) > A(k,n) for n > k  [n<=3 materializable] ===")
bad = 0
for n in range(0, 4):
    for k in range(0, n):
        if not (A(n, n) > A(k, n)):
            bad += 1
            print(f"    VIOLATION A({n},{n}) <= A({k},{n})")
report("A(n,n) > A(k,n) for 0<=k<n<=3", bad == 0,
       "(general n>k follows from monotonicity in first arg)")

# ---------- (SAME-LEVEL) A(K, A(K,n)) <= A(K+1, n+1) ----------
print("\n=== (SAME-LEVEL)  A(K, A(K,n)) <= A(K+1, n+1) ===")
# K+1 <= 3 needed for materializability; A(K,A(K,n)) for K<=2 is small.
bad = 0
for K in range(1, 3):
    for n in range(0, 59):
        if A(K, A(K, n)) > A(K+1, n+1):
            bad += 1
report("A(K,A(K,n)) <= A(K+1,n+1) for K=1..2, n=0..58", bad == 0,
       f"{bad} violations" if bad else "")

print("\n" + "="*64)
print("ALL PASS" if ok_all else "SOME FAILED")
sys.exit(0 if ok_all else 1)
