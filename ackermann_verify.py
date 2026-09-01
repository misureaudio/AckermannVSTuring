import sys
sys.set_int_max_str_digits(100_000)  # allow printing huge exact integers

# Closed-form check for A(4,y) and diagonal growth (no deep recursion).

def A(x, y):
    if x == 0:
        return y + 1
    if y == 0:
        return A(x - 1, 1)
    return A(x - 1, A(x, y - 1))

def tower(h):
    v = 2
    for _ in range(h - 1):
        v = 2 ** v
    return v

# A(4,y) = tower(y+3) - 3. Explicit only up to y=2 (tower(5)=2^65536,
# 19729 digits); tower(6) and tower(7) are unmaterializable (2^65536-bit
# and 2^(2^65536)-bit numbers), so their sizes are reported by magnitude.
for y in range(3):
    v = tower(y + 3) - 3
    if v < 10**6:
        print(f"A(4,{y}) = {v}")
    else:
        print(f"A(4,{y}) = tower({y+3})-3, exactly {len(str(v))} digits")
import math
# y=3: tower(6) = 2^(2^65536). bit-length = 2^65536.
# y=4: tower(7) = 2^(2^(2^65536)). bit-length = 2^(2^65536).
# Report log10(bit-length); for y=4 that itself overflows, so report its log10.
for y in (3, 4):
    if y == 3:
        log10_bits = 65536 * math.log10(2)          # ~1.97e4  (a plain float)
        print(f"A(4,{y}) = tower({y+3})-3, bit-length ~ 10^{log10_bits:.1f} "
              f"(unwritable)")
    else:
        # log10(bit-length) = 2^65536 * log10(2); report log10 of that:
        log10_log10_bits = 65536 * math.log10(2) + math.log10(math.log10(2))
        print(f"A(4,{y}) = tower({y+3})-3, bit-length ~ 10^(10^{log10_log10_bits:.1f}) "
              f"(unwritable)")

# Diagonal a(n) = A(n,n) for n<=4 via closed forms
print("\nDiagonal a(n)=A(n,n):")
for n in range(5):
    if n == 0:
        print("  a(0) = 1")
    elif n == 1:
        print("  a(1) = 3")
    elif n == 2:
        print("  a(2) = 7")
    elif n == 3:
        print(f"  a(3) = {2**6 - 3}")
    else:
        # a(4) = A(4,4) = tower(7) - 3, a power tower of 2's, height 7:
        #   tower(7) = 2^(2^(2^65536)).
        # Its decimal digit count is D = floor(tower(6)*log10(2)) + 1
        # = floor(2^(2^65536)*log10(2)) + 1, itself a ~19728-digit number.
        # Compute log10(D) directly (single float op, no huge powers):
        #   log10(D) = 2^65536*log10(2) + log10(log10(2))
        #            => log10(log10(D)) = 65536*log10(2) + log10(log10(2))
        import math
        L = 65536 * math.log10(2) + math.log10(math.log10(2))
        exp = int(L)
        mant = 10 ** (L - exp)
        print(f"  a(4) = A(4,4) = tower(7)-3  [2-tower of height 7]")
        print(f"      decimal-digit count D ~ {mant:.4f} x 10^{exp}")
        print(f"      (D itself is a {exp+1}-digit integer)")

# Cross-check A(3,13)=65533 (feeds A(4,1)) using closed form, not recursion.
print("\nA(3,13) =", 2 ** (13 + 3) - 3, "(closed form 2^(y+3)-3; should be 65533)")

# FGH: F_0(n)=n+1, F_{m+1}(n)=F_m^n(n)
def F(m, n):
    if m == 0:
        return n + 1
    v = n
    Fm = lambda x: F(m - 1, x)
    for _ in range(n):
        v = Fm(v)
    return v

# FGH: F_0(n)=n+1, F_{m+1}(n)=F_m^n(n).  F_m at small n stays small;
# the Ackermann diagonal sits near the F_m sequence (F_m ~ A(m, .)).
# Stop at m=2: F_3(3)=F_2^3(3) already has ~10^50 digits.
print("\nFGH F_m(n) at n=3 (m=0,1,2):")
for m in range(3):
    print(f"  F_{m}(3) = {F(m, 3)}")
print("F_1(3)=6?", F(1, 3), " F_2(3)=2^3*3=24?", F(2, 3))

# Knuth up-arrows (corrected): a ↑^1 b = a^b; a ↑^k 1 = a;
# a ↑^k b = a ↑^(k-1) (a ↑^k (b-1)).
def uparrow(a, b, k):
    if k == 1:
        return a ** b
    if b == 1:
        return a
    return uparrow(a, uparrow(a, b - 1, k), k - 1)
print("\nKnuth double-arrow: 2^^2 =", uparrow(2, 2, 2),
      " 2^^3 =", uparrow(2, 3, 2), " 2^^4 =", uparrow(2, 4, 2))
print("  2^^5 = 2^65536, has", len(str(uparrow(2, 5, 2))),
      "digits [should be 19729]")
# A(4,y) = 2 ^^ (y+3) - 3 : compare up-arrow values against the
# independently verified closed forms (no recursive A).
print("  A(4,0) == 2^^3-3 :", uparrow(2, 3, 2) - 3 == 13)
print("  A(4,1) == 2^^4-3 :", uparrow(2, 4, 2) - 3 == 65533)
print("  A(4,2) == 2^^5-3 :", len(str(uparrow(2, 5, 2) - 3)) == 19729)
