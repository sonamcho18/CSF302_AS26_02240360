"""
Lab 3 - Q1: Matrix Multiplication - Strassen's vs Traditional
================================================================
Student Number: 02240360

Multiplies two n x n matrices (n a power of 2) using:
  1. Traditional method (triple nested loop, O(n^3))
  2. Strassen's algorithm (divide and conquer, 7 multiplications per split)

Verifies both results match, and benchmarks performance across
increasing matrix sizes: 2, 4, 8, 16, 32, 64, 128.
"""

import random
import time
import copy


# ---------------------------------------------------------------------------
# 1. Traditional matrix multiplication  O(n^3)
# ---------------------------------------------------------------------------
def traditional_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            total = 0
            for k in range(n):
                total += A[i][k] * B[k][j]
            C[i][j] = total
    return C


# ---------------------------------------------------------------------------
# 2. Strassen's algorithm  O(n^log2(7)) ~= O(n^2.807)
# ---------------------------------------------------------------------------
def add_matrix(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def sub_matrix(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def split_matrix(M):
    """Split M into 4 quadrants: top-left, top-right, bottom-left, bottom-right."""
    n = len(M)
    mid = n // 2
    a11 = [row[:mid] for row in M[:mid]]
    a12 = [row[mid:] for row in M[:mid]]
    a21 = [row[:mid] for row in M[mid:]]
    a22 = [row[mid:] for row in M[mid:]]
    return a11, a12, a21, a22


def join_matrix(c11, c12, c21, c22):
    """Join 4 quadrants back into a single matrix."""
    top = [c11[i] + c12[i] for i in range(len(c11))]
    bottom = [c21[i] + c22[i] for i in range(len(c21))]
    return top + bottom


def strassen_multiply(A, B):
    n = len(A)

    # Base case: 1x1 matrix -> plain scalar multiply
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    a11, a12, a21, a22 = split_matrix(A)
    b11, b12, b21, b22 = split_matrix(B)

    # 7 recursive multiplications (Strassen's formulas)
    m1 = strassen_multiply(add_matrix(a11, a22), add_matrix(b11, b22))
    m2 = strassen_multiply(add_matrix(a21, a22), b11)
    m3 = strassen_multiply(a11, sub_matrix(b12, b22))
    m4 = strassen_multiply(a22, sub_matrix(b21, b11))
    m5 = strassen_multiply(add_matrix(a11, a12), b22)
    m6 = strassen_multiply(sub_matrix(a21, a11), add_matrix(b11, b12))
    m7 = strassen_multiply(sub_matrix(a12, a22), add_matrix(b21, b22))

    c11 = add_matrix(sub_matrix(add_matrix(m1, m4), m5), m7)
    c12 = add_matrix(m3, m5)
    c21 = add_matrix(m2, m4)
    c22 = add_matrix(sub_matrix(add_matrix(m1, m3), m2), m6)

    return join_matrix(c11, c12, c21, c22)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def generate_random_matrix(n, low=0, high=9):
    return [[random.randint(low, high) for _ in range(n)] for _ in range(n)]


def print_matrix(M, label=""):
    if label:
        print(label)
    for row in M:
        print(row)
    print()


def matrices_equal(A, B):
    n = len(A)
    return all(A[i][j] == B[i][j] for i in range(n) for j in range(n))


def get_manual_matrix(n, name):
    print(f"Enter matrix {name} row by row ({n} values per row, space-separated):")
    M = []
    for i in range(n):
        while True:
            try:
                row = list(map(int, input(f"  Row {i}: ").split()))
                if len(row) != n:
                    print(f"  Expected {n} values, got {len(row)}. Try again.")
                    continue
                M.append(row)
                break
            except ValueError:
                print("  Invalid input, enter integers only.")
    return M


# ---------------------------------------------------------------------------
# Demo / verification for a single size (interactive-friendly)
# ---------------------------------------------------------------------------
def run_demo(n=4, manual=False, seed=None):
    if seed is not None:
        random.seed(seed)

    if manual:
        A = get_manual_matrix(n, "A")
        B = get_manual_matrix(n, "B")
    else:
        A = generate_random_matrix(n)
        B = generate_random_matrix(n)

    print_matrix(A, "Matrix A:")
    print_matrix(B, "Matrix B:")

    t0 = time.perf_counter()
    C_trad = traditional_multiply(A, B)
    t1 = time.perf_counter()
    C_strassen = strassen_multiply(A, B)
    t2 = time.perf_counter()

    print_matrix(C_trad, "Result - Traditional Method:")
    print_matrix(C_strassen, "Result - Strassen's Algorithm:")

    match = matrices_equal(C_trad, C_strassen)
    print(f"Results match: {match}")
    print(f"Traditional time: {(t1 - t0) * 1000:.4f} ms")
    print(f"Strassen time:    {(t2 - t1) * 1000:.4f} ms")
    return match


# ---------------------------------------------------------------------------
# Benchmark across increasing sizes (used to produce the report's table/graph)
# ---------------------------------------------------------------------------
def benchmark(sizes=(2, 4, 8, 16, 32, 64, 128), trials=3, seed=42):
    random.seed(seed)
    results = []
    print(f"{'n':>5} | {'Traditional (s)':>16} | {'Strassen (s)':>14} | {'Match':>6}")
    print("-" * 52)
    for n in sizes:
        trad_times = []
        strassen_times = []
        match = True
        for _ in range(trials):
            A = generate_random_matrix(n)
            B = generate_random_matrix(n)

            t0 = time.perf_counter()
            C1 = traditional_multiply(A, B)
            t1 = time.perf_counter()
            C2 = strassen_multiply(A, B)
            t2 = time.perf_counter()

            trad_times.append(t1 - t0)
            strassen_times.append(t2 - t1)
            match = match and matrices_equal(C1, C2)

        avg_trad = sum(trad_times) / trials
        avg_strassen = sum(strassen_times) / trials
        results.append((n, avg_trad, avg_strassen, match))
        print(f"{n:>5} | {avg_trad:>16.6f} | {avg_strassen:>14.6f} | {str(match):>6}")

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("DEMO: 4x4 matrix multiplication (random values)")
    print("=" * 60)
    run_demo(n=4, seed=1)

    print("\n" + "=" * 60)
    print("BENCHMARK: sizes 2 through 128 (powers of 2)")
    print("=" * 60)
    benchmark()
