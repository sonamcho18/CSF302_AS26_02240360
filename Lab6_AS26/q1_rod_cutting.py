"""
CSF302 - Lab 6, Q1: Rod Cutting
Name: Sonam Choki
Student Number: 02240360

Problem: a rod of length n can be cut into pieces. A piece of length i sells
for p[i]. Find the cuts that give the most money (maximum revenue).
"""

import sys
import time

sys.setrecursionlimit(10_000)

BASE_PRICES = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]   # lengths 1..10


def price_table(n):
    """p[0..n]; p[i] = 3*i for i > 10 (task 5)."""
    p = [0] + BASE_PRICES[:]
    for i in range(11, n + 1):
        p.append(3 * i)
    return p


# ---------------------------------------------------------------
# 1. Naive recursive solution: O(2^n)
# ---------------------------------------------------------------
def cut_rod_naive(p, n):
    calls = 0

    def solve(n):
        nonlocal calls
        calls += 1
        if n == 0:
            return 0
        best = -1
        for i in range(1, n + 1):          # first piece has length i
            best = max(best, p[i] + solve(n - i))
        return best

    return solve(n), calls


# ---------------------------------------------------------------
# 2. Top-down memoized solution: O(n^2)
# ---------------------------------------------------------------
def cut_rod_memo(p, n):
    calls = 0
    memo = {}

    def solve(n):
        nonlocal calls
        calls += 1
        if n in memo:                      # already solved -> reuse
            return memo[n]
        if n == 0:
            result = 0
        else:
            result = max(p[i] + solve(n - i) for i in range(1, n + 1))
        memo[n] = result
        return result

    return solve(n), calls


# ---------------------------------------------------------------
# 3. Bottom-up tabulated solution: O(n^2), no recursion
#    Also records the first cut so we can rebuild the pieces.
# ---------------------------------------------------------------
def cut_rod_bottom_up(p, n):
    r = [0] * (n + 1)          # r[j] = best revenue for length j
    first = [0] * (n + 1)      # first[j] = best first piece for length j
    steps = 0
    for j in range(1, n + 1):
        best = -1
        for i in range(1, j + 1):
            steps += 1
            if p[i] + r[j - i] > best:
                best = p[i] + r[j - i]
                first[j] = i
        r[j] = best
    return r, first, steps


def pieces(first, n):
    out = []
    while n > 0:
        out.append(first[n])
        n -= first[n]
    return out


# ---------------------------------------------------------------
# 4. Revenue and pieces for n = 1..10
# ---------------------------------------------------------------
def table_1_to_10():
    print("=" * 68)
    print("TASKS 1-4: Maximum revenue and pieces for n = 1 to 10")
    print("=" * 68)
    p = price_table(10)
    print("Prices:", ", ".join(f"p[{i}]={p[i]}" for i in range(1, 11)))
    print()
    r, first, _ = cut_rod_bottom_up(p, 10)
    print(f"{'n':>3} | {'naive':>6} {'memo':>6} {'bottom-up':>10} | pieces")
    print("-" * 68)
    ok = True
    for n in range(1, 11):
        a, _ = cut_rod_naive(p, n)
        b, _ = cut_rod_memo(p, n)
        c = r[n]
        ok &= a == b == c
        cuts = pieces(first, n)
        check = " + ".join(f"p[{x}]" for x in cuts)
        print(f"{n:>3} | {a:>6} {b:>6} {c:>10} | {cuts}  ({check} = {sum(p[x] for x in cuts)})")
    print("-" * 68)
    print("All three versions agree:", ok)
    print()


# ---------------------------------------------------------------
# 5-6. Count calls and time for n = 5, 10, 15, 20, 25
# ---------------------------------------------------------------
def benchmark():
    print("=" * 78)
    print("TASKS 5-6: Number of calls and execution time (p[i] = 3i for i > 10)")
    print("=" * 78)
    print(f"{'n':>3} {'revenue':>8} | {'naive calls':>12} {'naive (s)':>10} | "
          f"{'memo calls':>10} {'memo (s)':>9} | {'bottom-up steps':>15} {'(s)':>8}")
    print("-" * 78)
    for n in [5, 10, 15, 20, 25]:
        p = price_table(n)
        t0 = time.perf_counter()
        a, naive_calls = cut_rod_naive(p, n)
        t1 = time.perf_counter()
        b, memo_calls = cut_rod_memo(p, n)
        t2 = time.perf_counter()
        r, _, steps = cut_rod_bottom_up(p, n)
        t3 = time.perf_counter()
        assert a == b == r[n]
        print(f"{n:>3} {a:>8} | {naive_calls:>12,} {t1 - t0:>10.4f} | "
              f"{memo_calls:>10,} {t2 - t1:>9.6f} | {steps:>15,} {t3 - t2:>8.6f}")
    print("-" * 78)
    print("Naive calls = 2^n          -> doubles every time n grows by 1.")
    print("Memo calls  = n(n+1)/2 + 1 -> each length is solved only ONCE.")
    print("Bottom-up   = n(n+1)/2 loop steps and 0 recursive calls.")
    print()
    print("Why: the naive version solves the same smaller rods again and again")
    print("(length 1 is solved 2^(n-2) times!). Memoization and tabulation save")
    print("each answer the first time, so the work drops from O(2^n) to O(n^2).")
    print()


if __name__ == "__main__":
    print("CSF302 Lab 6 - Q1 Rod Cutting | Sonam Choki | 02240360\n")
    table_1_to_10()
    benchmark()
