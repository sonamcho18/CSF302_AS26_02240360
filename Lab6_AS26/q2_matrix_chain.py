"""
CSF302 - Lab 6, Q2: Matrix Chain Multiplication
Name: Sonam Choki
Student Number: 02240360

Matrix Ai has size dims[i-1] x dims[i]. Multiplying a (p x q) by a (q x r)
matrix costs p*q*r scalar multiplications. We choose where to put the
brackets so the total cost is as small as possible.
"""

import random
from functools import lru_cache


# ---------------------------------------------------------------
# 1. Bottom-up DP: O(n^3)
# ---------------------------------------------------------------
def matrix_chain_order(dims):
    n = len(dims) - 1                      # number of matrices
    m = [[0] * (n + 1) for _ in range(n + 1)]   # m[i][j] = min cost Ai..Aj
    s = [[0] * (n + 1) for _ in range(n + 1)]   # s[i][j] = best split k
    for length in range(2, n + 1):         # chain length
        for i in range(1, n - length + 2):
            j = i + length - 1
            m[i][j] = float("inf")
            for k in range(i, j):
                cost = m[i][k] + m[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k
    return m, s


# ---------------------------------------------------------------
# 2. Optimal parenthesisation
# ---------------------------------------------------------------
def parens(s, i, j):
    if i == j:
        return f"A{i}"
    k = s[i][j]
    return "(" + parens(s, i, k) + parens(s, k + 1, j) + ")"


# ---------------------------------------------------------------
# 3. Brute force: try EVERY way of splitting (no memo). Exponential.
# ---------------------------------------------------------------
def brute_force(dims):
    def best(i, j):
        if i == j:
            return 0
        return min(best(i, k) + best(k + 1, j) + dims[i - 1] * dims[k] * dims[j]
                   for k in range(i, j))
    return best(1, len(dims) - 1)


def left_to_right_cost(dims):
    """Cost of ((((A1A2)A3)A4)...): no clever bracketing."""
    cost = 0
    rows = dims[0]
    for k in range(1, len(dims) - 1):
        cost += rows * dims[k] * dims[k + 1]
    return cost


def left_to_right_parens(n):
    s = "A1"
    for i in range(2, n + 1):
        s = f"({s}A{i})"
    return s


def show_table(m, n):
    print("  m[i][j] table (minimum cost for Ai..Aj):")
    print("       " + "".join(f"{j:>8}" for j in range(1, n + 1)))
    for i in range(1, n + 1):
        row = "".join(f"{m[i][j]:>8}" if j >= i else f"{'':>8}" for j in range(1, n + 1))
        print(f"   i={i:<2}" + row)


def solve(name, dims, show=False):
    n = len(dims) - 1
    m, s = matrix_chain_order(dims)
    dp = m[1][n]
    bf = brute_force(dims) if n <= 8 else None
    ltr = left_to_right_cost(dims)
    print(f"{name}: dims = <{', '.join(map(str, dims))}>  ({n} matrices)")
    if show:
        show_table(m, n)
    print(f"  Optimal order      : {parens(s, 1, n)}")
    print(f"  Minimum cost (DP)  : {dp:,}")
    print(f"  Brute force check  : {bf:,}  -> {'MATCH' if bf == dp else 'DIFFERENT'}")
    print(f"  Left-to-right order: {left_to_right_parens(n)}")
    print(f"  Left-to-right cost : {ltr:,}  ({ltr / dp:.2f}x the optimal)")
    print()
    return dp, bf, ltr


if __name__ == "__main__":
    print("CSF302 Lab 6 - Q2 Matrix Chain Multiplication | Sonam Choki | 02240360\n")
    print("=" * 72)
    print("Required test chains")
    print("=" * 72)
    dp, _, _ = solve("Chain 1", [30, 35, 15, 5, 10, 20, 25], show=True)
    print(f"  Expected minimum 15,125 -> {'CORRECT' if dp == 15125 else 'WRONG'}\n")
    solve("Chain 2", [5, 4, 6, 2, 7], show=True)

    print("=" * 72)
    print("5 random chains (3 to 8 matrices, sizes 2..50)")
    print("=" * 72)
    rng = random.Random(302)
    rows = []
    for t in range(1, 6):
        n = rng.randint(3, 8)
        dims = [rng.randint(2, 50) for _ in range(n + 1)]
        rows.append((t, n, *solve(f"Random {t}", dims)))

    print("=" * 72)
    print("Summary table")
    print("=" * 72)
    print(f"{'chain':>7} {'n':>3} | {'optimal (DP)':>13} {'brute force':>12} | "
          f"{'left-to-right':>14} {'ratio':>6}")
    print("-" * 72)
    for t, n, dp, bf, ltr in rows:
        print(f"{'R' + str(t):>7} {n:>3} | {dp:>13,} {bf:>12,} | {ltr:>14,} {ltr / dp:>5.2f}x")
    print("-" * 72)
    print("DP always equals brute force, and is often much cheaper than")
    print("just multiplying left to right.")
