"""
CSF302 - Lab 4, Part B: Efficient Matrix Modular Exponentiation
Name: Sonam Choki
Student Number: 02240360
"""

import random
import time

# Naive benchmark runs with d^3 * n above this number are skipped
# Set lower (e.g. 20_000_000) if your laptop is slow.
NAIVE_WORK_LIMIT = 200_000_000


# ---------------------------------------------------------------
# Task 1: Multiply two square matrices mod m
# ---------------------------------------------------------------
def mat_mult(A, B, m):
    """Return (A x B) mod m for two d x d matrices. O(d^3)."""
    d = len(A)
    Bt = list(zip(*B))                      # columns of B (faster access)
    return [[sum(A[i][k] * Bt[j][k] for k in range(d)) % m
             for j in range(d)]
            for i in range(d)]


# ---------------------------------------------------------------
# Task 2: Identity matrix
# ---------------------------------------------------------------
def identity(d, m=None):
    """d x d identity matrix (1 on the diagonal, 0 elsewhere)."""
    one = 1 if m is None else 1 % m        # if m = 1 everything is 0
    return [[one if i == j else 0 for j in range(d)] for i in range(d)]


def validate(A, n, m):
    if m < 1:
        raise ValueError(f"Invalid modulus m = {m}. Modulus must be >= 1.")
    if n < 0:
        raise ValueError(f"Negative exponent n = {n} is not supported.")
    if any(len(row) != len(A) for row in A):
        raise ValueError("Matrix must be square.")
    return [[x % m for x in row] for row in A]


# ---------------------------------------------------------------
# Task 3: Naive matrix exponentiation
# ---------------------------------------------------------------
def naive_mat_exp(A, n, m):
    """A^n mod m by multiplying A, n times. O(d^3 * n)."""
    A = validate(A, n, m)
    result = identity(len(A), m)
    for _ in range(n):
        result = mat_mult(result, A, m)
    return result


# ---------------------------------------------------------------
# Task 4: Binary matrix exponentiation (repeated squaring)
# ---------------------------------------------------------------
def binary_mat_exp(A, n, m):
    """A^n mod m by repeated squaring. O(d^3 * log n)."""
    A = validate(A, n, m)
    result = identity(len(A), m)
    while n > 0:
        if n & 1:
            result = mat_mult(result, A, m)
        A = mat_mult(A, A, m)
        n >>= 1
    return result


def show(M, indent="    "):
    for row in M:
        print(indent + " ".join(f"{x:>6}" for x in row))


# ---------------------------------------------------------------
# Task 5: Compare naive and binary results
# ---------------------------------------------------------------
def compare_outputs():
    print("=" * 72)
    print("TASKS 1-5: Matrix multiply, identity, naive vs binary exponentiation")
    print("=" * 72)
    print("Identity matrix I(3):")
    show(identity(3))
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    print("\n[[1,2],[3,4]] x [[5,6],[7,8]] mod 10:")
    show(mat_mult(A, B, 10))
    print()

    random.seed(302)
    cases = [
        ([[1, 1], [1, 0]], 10, 1000),
        ([[2, 0], [0, 3]], 5, 100),
        ([[1, 2], [3, 4]], 0, 7),            # zero exponent -> identity
        ([[-1, 2], [3, -4]], 7, 13),         # negative entries
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 20, 97),
    ]
    for _ in range(3):
        d = random.randint(2, 5)
        M = [[random.randint(0, 50) for _ in range(d)] for _ in range(d)]
        cases.append((M, random.randint(1, 200), random.randint(2, 10_000)))

    print(f"{'#':>2} {'d':>2} {'n':>5} {'m':>6} | match | binary result (first row)")
    print("-" * 72)
    all_ok = True
    for i, (M, n, m) in enumerate(cases, 1):
        r1 = naive_mat_exp(M, n, m)
        r2 = binary_mat_exp(M, n, m)
        ok = r1 == r2
        all_ok &= ok
        print(f"{i:>2} {len(M):>2} {n:>5} {m:>6} | {'YES' if ok else 'NO ':>5} | {r2[0]}")
    print("-" * 72)
    print("All results match:", all_ok)
    print()


# ---------------------------------------------------------------
# Tasks 6 & 7: Fibonacci with matrix exponentiation
# ---------------------------------------------------------------
def fibonacci_mod(n, m):
    """F(n) mod m using [[1,1],[1,0]]^n = [[F(n+1),F(n)],[F(n),F(n-1)]]."""
    if n < 0:
        raise ValueError("n must be >= 0")
    return binary_mat_exp([[1, 1], [1, 0]], n, m)[0][1]


def fibonacci_loop(n, m):
    """Simple loop version, only used to check small answers."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, (a + b) % m
    return a


def fibonacci_demo():
    print("=" * 72)
    print("TASK 6: nth Fibonacci number mod m using matrix exponentiation")
    print("=" * 72)
    m = 1000
    print(f"{'n':>4} | {'matrix':>8} {'loop':>8} | match   (m = {m})")
    print("-" * 40)
    for n in [0, 1, 2, 5, 10, 20, 50, 90, 100]:
        a, b = fibonacci_mod(n, m), fibonacci_loop(n, m)
        print(f"{n:>4} | {a:>8} {b:>8} | {'YES' if a == b else 'NO'}")
    print()

    print("=" * 72)
    print("TASK 7: F(10^18) mod (10^9 + 7)")
    print("=" * 72)
    MOD = 10 ** 9 + 7
    start = time.perf_counter()
    ans = fibonacci_mod(10 ** 18, MOD)
    t = time.perf_counter() - start
    print(f"F(10^18) mod (10^9 + 7) = {ans}")
    print(f"Time taken: {t:.6f} s  (only ~{(10 ** 18).bit_length()} squarings needed)")
    print()


# ---------------------------------------------------------------
# Task 8: Count walks of exactly k edges in a directed graph
# ---------------------------------------------------------------
def count_walks(adj, u, v, k, m):
    """Number of walks with exactly k edges from u to v = (adj^k)[u][v] mod m."""
    return binary_mat_exp(adj, k, m)[u][v]


def brute_force_walks(adj, u, v, k):
    """Check by trying every path (only for tiny k)."""
    if k == 0:
        return 1 if u == v else 0
    return sum(brute_force_walks(adj, w, v, k - 1)
               for w in range(len(adj)) if adj[u][w])


def walks_demo():
    print("=" * 72)
    print("TASK 8: Counting walks of exactly k edges")
    print("=" * 72)
    # Directed graph:  0->1, 0->2, 1->2, 2->0, 2->3, 3->1
    adj = [[0, 1, 1, 0],
           [0, 0, 1, 0],
           [1, 0, 0, 1],
           [0, 1, 0, 0]]
    print("Edges: 0->1, 0->2, 1->2, 2->0, 2->3, 3->1")
    print("Adjacency matrix:")
    show(adj)
    m = 10 ** 9 + 7
    print(f"\n{'u':>2} {'v':>2} {'k':>4} | {'matrix':>8} {'brute force':>12} | match")
    print("-" * 46)
    for u, v, k in [(0, 2, 1), (0, 0, 3), (0, 3, 4), (1, 1, 5), (2, 2, 6), (0, 1, 8)]:
        a = count_walks(adj, u, v, k, m)
        b = brute_force_walks(adj, u, v, k)
        print(f"{u:>2} {v:>2} {k:>4} | {a:>8} {b:>12} | {'YES' if a == b else 'NO'}")
    print(f"\nWalks 0 -> 3 with k = 10^6 edges (mod 10^9+7): "
          f"{count_walks(adj, 0, 3, 10 ** 6, m)}")
    print()


# ---------------------------------------------------------------
# Task 9: Benchmark
# ---------------------------------------------------------------
def benchmark():
    print("=" * 72)
    print("TASK 9: Benchmark naive vs binary matrix exponentiation (m = 10^9+7)")
    print("=" * 72)
    m = 10 ** 9 + 7
    random.seed(302)
    skipped_any = False
    print(f"{'d':>3} {'n':>6} | {'naive (s)':>12} {'binary (s)':>12} | {'speed-up':>9}")
    print("-" * 52)
    for d in [2, 4, 8, 16, 32]:
        M = [[random.randint(0, m - 1) for _ in range(d)] for _ in range(d)]
        for p in range(4, 13):
            n = 2 ** p
            start = time.perf_counter()
            rb = binary_mat_exp(M, n, m)
            t_bin = time.perf_counter() - start
            if d ** 3 * n <= NAIVE_WORK_LIMIT:
                start = time.perf_counter()
                rn = naive_mat_exp(M, n, m)
                t_naive = time.perf_counter() - start
                assert rn == rb
                print(f"{d:>3} {n:>6} | {t_naive:>12.5f} {t_bin:>12.5f} | "
                      f"{t_naive / t_bin:>8.0f}x")
            else:
                skipped_any = True
                print(f"{d:>3} {n:>6} | {'skipped*':>12} {t_bin:>12.5f} | {'-':>9}")
        print("-" * 52)
    if skipped_any:
        print("* naive skipped: it would take too long (work d^3 * n is too big).")
    print("Naive time doubles when n doubles (O(d^3 n));")
    print("binary time only grows by a little (O(d^3 log n)).")
    print()


if __name__ == "__main__":
    print("CSF302 Lab 4 - Part B | Sonam Choki | 02240360\n")
    compare_outputs()
    fibonacci_demo()
    walks_demo()
    benchmark()
