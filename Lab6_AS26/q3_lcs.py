"""
CSF302 - Lab 6, Q3: Longest Common Subsequence (LCS)
Name: Sonam Choki
Student Number: 02240360

A subsequence keeps the order of characters but may skip some.
LCS = the longest subsequence that appears in BOTH strings.

Usage:
    python3 q3_lcs.py                         # uses file1.txt and file2.txt
    python3 q3_lcs.py old.txt new.txt         # diff your own files
"""

import os
import random
import sys
import time
from itertools import combinations


# ---------------------------------------------------------------
# 1. Fill the LCS table bottom-up. O(m*n)
# ---------------------------------------------------------------
def lcs_table(X, Y):
    m, n = len(X), len(Y)
    c = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1          # match: diagonal + 1
            else:
                c[i][j] = max(c[i - 1][j], c[i][j - 1])  # best of up / left
    return c


def print_table(X, Y, c):
    print("    " + f"{'':>5}" + "".join(f"{ch:>5}" for ch in Y))
    for i in range(len(X) + 1):
        label = X[i - 1] if i > 0 else " "
        print(f"  {label} " + "".join(f"{c[i][j]:>5}" for j in range(len(Y) + 1)))


# ---------------------------------------------------------------
# 2. Reconstruct one LCS by walking back from c[m][n]
# ---------------------------------------------------------------
def lcs_reconstruct(X, Y, c):
    i, j = len(X), len(Y)
    out = []
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            out.append(X[i - 1])
            i -= 1
            j -= 1
        elif c[i - 1][j] >= c[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return out[::-1]


# ---------------------------------------------------------------
# 3. Space-optimised: only two rows, returns the length. O(n) space
# ---------------------------------------------------------------
def lcs_length_two_rows(X, Y):
    prev = [0] * (len(Y) + 1)
    for i in range(1, len(X) + 1):
        curr = [0] * (len(Y) + 1)
        for j in range(1, len(Y) + 1):
            if X[i - 1] == Y[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr
    return prev[-1]


# ---------------------------------------------------------------
# 4. Brute force: try every subsequence of X. O(2^m * n)
# ---------------------------------------------------------------
def is_subsequence(s, Y):
    it = iter(Y)
    return all(ch in it for ch in s)


def lcs_brute_force(X, Y):
    """Try EVERY one of the 2^m subsequences of X and keep the longest
    one that is also a subsequence of Y."""
    best = 0
    for length in range(len(X) + 1):
        for idx in combinations(range(len(X)), length):
            if is_subsequence([X[i] for i in idx], Y):
                best = length
    return best


def part_1_to_3():
    print("=" * 66)
    print("TASKS 1-3: LCS table, reconstruction, two-row version")
    print("=" * 66)
    X, Y = "ABCBDAB", "BDCABA"
    print(f"X = {X}, Y = {Y}\n")
    c = lcs_table(X, Y)
    print_table(X, Y, c)
    lcs = "".join(lcs_reconstruct(X, Y, c))
    print(f"\nLCS length (table)      : {c[-1][-1]}")
    print(f"One LCS (reconstructed) : {lcs}")
    print(f"LCS length (two rows)   : {lcs_length_two_rows(X, Y)}")
    print(f"Check: '{lcs}' is a subsequence of both X and Y -> "
          f"{is_subsequence(lcs, X) and is_subsequence(lcs, Y)}")
    print()


def part_4():
    print("=" * 66)
    print("TASK 4: DP vs brute force, string length 5 to 18")
    print("=" * 66)
    rng = random.Random(302)
    print(f"{'len':>4} | {'LCS':>4} | {'DP (s)':>10} {'brute force (s)':>16} | "
          f"{'subsequences':>12}")
    print("-" * 60)
    for L in range(5, 19):
        X = "".join(rng.choice("ACGT") for _ in range(L))
        Y = "".join(rng.choice("ACGT") for _ in range(L))
        t0 = time.perf_counter()
        d = lcs_length_two_rows(X, Y)
        t1 = time.perf_counter()
        b = lcs_brute_force(X, Y)
        t2 = time.perf_counter()
        assert d == b
        print(f"{L:>4} | {d:>4} | {t1 - t0:>10.6f} {t2 - t1:>16.6f} | {2 ** L:>12,}")
    print("-" * 60)
    print("DP time grows slowly (m*n cells). Brute force tries up to 2^m")
    print("subsequences, so it roughly doubles with each extra character.")
    print()


# ---------------------------------------------------------------
# 5. Line-by-line diff of two text files using LCS of LINES
# ---------------------------------------------------------------
def diff_lines(a, b):
    c = lcs_table(a, b)
    i, j = len(a), len(b)
    out = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            out.append(("  ", a[i - 1]))       # in the LCS -> unchanged
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or c[i][j - 1] >= c[i - 1][j]):
            out.append(("+ ", b[j - 1]))       # only in new file -> added
            j -= 1
        else:
            out.append(("- ", a[i - 1]))       # only in old file -> removed
            i -= 1
    return out[::-1]


def part_5(file1, file2):
    print("=" * 66)
    print(f"TASK 5: Line-by-line diff of {os.path.basename(file1)} -> "
          f"{os.path.basename(file2)}")
    print("=" * 66)
    with open(file1) as f:
        a = f.read().splitlines()
    with open(file2) as f:
        b = f.read().splitlines()
    result = diff_lines(a, b)
    for tag, line in result:
        print(f"{tag}{line}")
    same = sum(1 for t, _ in result if t == "  ")
    print("-" * 66)
    print(f"Unchanged (in LCS): {same}   Added (+): "
          f"{sum(1 for t, _ in result if t == '+ ')}   Removed (-): "
          f"{sum(1 for t, _ in result if t == '- ')}")
    print()


if __name__ == "__main__":
    print("CSF302 Lab 6 - Q3 Longest Common Subsequence | Sonam Choki | 02240360\n")
    here = os.path.dirname(os.path.abspath(__file__))
    f1 = sys.argv[1] if len(sys.argv) > 2 else os.path.join(here, "file1.txt")
    f2 = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "file2.txt")
    part_1_to_3()
    part_4()
    part_5(f1, f2)
