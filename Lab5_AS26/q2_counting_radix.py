"""
CSF302 - Lab 5, Q2: Counting Sort and Radix Sort
Name: Sonam Choki
Student Number: 02240360
"""

import random
import time

from merge_sort import merge_sort

try:
    import matplotlib
    matplotlib.use("Agg")           # save to file, no window needed
    import matplotlib.pyplot as plt
    HAVE_PLOT = True
except ImportError:
    HAVE_PLOT = False


# ---------------------------------------------------------------
# 1. Stable counting sort for integers in the range 0..k
# ---------------------------------------------------------------
def counting_sort(a, k, key=None):
    """
    Stable counting sort. O(n + k) time and O(n + k) extra space.
    key: optional function giving the integer key (0..k) of each item.
    """
    if key is None:
        key = lambda x: x
    keys = [key(x) for x in a]
    count = [0] * (k + 1)
    for kk in keys:                      # 1) count each key
        count[kk] += 1
    total = 0
    for v in range(k + 1):               # 2) prefix sums -> end positions
        total += count[v]
        count[v] = total
    out = [None] * len(a)
    for i in range(len(a) - 1, -1, -1):  # 3) go BACKWARDS -> stable
        kk = keys[i]
        count[kk] -= 1
        out[count[kk]] = a[i]
    return out


# ---------------------------------------------------------------
# 2. LSD radix sort, using counting sort on each digit
# ---------------------------------------------------------------
def radix_sort(a, base=10):
    """
    Least-significant-digit radix sort for non-negative integers.
    Each pass is a stable counting sort on one digit (0..base-1).
    O(d * (n + base)) time where d = number of digits.
    """
    n = len(a)
    if n == 0:
        return []
    out = list(a)
    biggest = max(out)
    exp = 1
    while biggest // exp > 0:
        digits = [(x // exp) % base for x in out]
        count = [0] * base
        for d in digits:
            count[d] += 1
        total = 0
        for v in range(base):
            total += count[v]
            count[v] = total
        res = [0] * n
        for i in range(n - 1, -1, -1):
            d = digits[i]
            count[d] -= 1
            res[count[d]] = out[i]
        out = res
        exp *= base
    return out


def timed(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    return time.perf_counter() - start, result


# ---------------------------------------------------------------
# Correctness
# ---------------------------------------------------------------
def correctness_check():
    print("=" * 72)
    print("TASKS 1-2: Correctness of counting sort and radix sort")
    print("=" * 72)
    sample = [170, 45, 75, 90, 802, 24, 2, 66]
    print("Input:                 ", sample)
    print("Counting sort (k=802): ", counting_sort(sample, 802))
    print("Radix sort base 10:    ", radix_sort(sample, 10))
    print("Radix sort base 256:   ", radix_sort(sample, 256))
    rng = random.Random(5)
    ok = True
    for _ in range(300):
        n = rng.randint(0, 200)
        k = rng.choice([1, 9, 100, 10 ** 6])
        data = [rng.randint(0, k) for _ in range(n)]
        ok &= counting_sort(data, k) == sorted(data)
        ok &= radix_sort(data, 10) == sorted(data)
        ok &= radix_sort(data, 256) == sorted(data)
    print("300 random tests (counting, radix-10, radix-256) all correct:", ok)
    print()


# ---------------------------------------------------------------
# 7. Stability demo
# ---------------------------------------------------------------
def stability_demo():
    print("=" * 72)
    print("TASK 7: Counting sort is STABLE - sorting (key, original index) pairs")
    print("=" * 72)
    keys = [3, 1, 2, 3, 1, 0, 2, 3, 1, 2]
    pairs = [(k, i) for i, k in enumerate(keys)]
    print("Input pairs (key, index):")
    print("  ", pairs)
    out = counting_sort(pairs, 3, key=lambda p: p[0])
    print("Sorted by key only:")
    print("  ", out)
    stable = all(out[i][1] < out[i + 1][1]
                 for i in range(len(out) - 1) if out[i][0] == out[i + 1][0])
    print("Within each equal key, the original indexes stay in increasing order.")
    print("Stable:", stable)
    big = [(random.randint(0, 50), i) for i in range(20000)]
    out = counting_sort(big, 50, key=lambda p: p[0])
    print("Same check on 20,000 random pairs -> stable:",
          out == sorted(big, key=lambda p: p[0]))
    print()


# ---------------------------------------------------------------
# 4. Fix n = 100,000, vary k for counting sort
# ---------------------------------------------------------------
def vary_k():
    print("=" * 72)
    print("TASKS 3-4: n = 100,000, vary k (largest value)")
    print("=" * 72)
    n = 100_000
    rng = random.Random(302)
    ks = [10, 10 ** 3, 10 ** 5, 10 ** 7]
    rows = []
    print(f"{'k':>12} | {'counting (s)':>12} {'radix10 (s)':>12} "
          f"{'radix256 (s)':>12} {'merge (s)':>10}")
    print("-" * 66)
    for k in ks:
        data = [rng.randint(0, k) for _ in range(n)]
        ref = sorted(data)
        tc, r1 = timed(counting_sort, data, k)
        tr10, r2 = timed(radix_sort, data, 10)
        tr256, r3 = timed(radix_sort, data, 256)
        tm, r4 = timed(merge_sort, data)
        assert r1 == r2 == r3 == r4 == ref
        rows.append((k, tc, tr10, tr256, tm))
        print(f"{k:>12,} | {tc:>12.4f} {tr10:>12.4f} {tr256:>12.4f} {tm:>10.4f}")
    print("-" * 66)
    print("Counting sort is fastest when k is small, but when k >> n it must")
    print("create and scan a count array of size k, so it becomes the slowest.")
    print("(k = 10^9 would need a 10^9-size array: about 8 GB, so it is impossible.)")
    print()
    return rows


# ---------------------------------------------------------------
# 5. Fix k = 10^9, vary n for radix sort and merge sort
# ---------------------------------------------------------------
def vary_n():
    print("=" * 72)
    print("TASK 5: k = 10^9, vary n (radix sort vs merge sort)")
    print("=" * 72)
    k = 10 ** 9
    rng = random.Random(302)
    sizes = [10_000, 50_000, 100_000, 250_000, 500_000, 1_000_000]
    rows = []
    print(f"{'n':>10} | {'radix10 (s)':>12} {'radix256 (s)':>13} {'merge (s)':>10}")
    print("-" * 52)
    for n in sizes:
        data = [rng.randint(0, k) for _ in range(n)]
        t10, r1 = timed(radix_sort, data, 10)
        t256, r2 = timed(radix_sort, data, 256)
        tm, r3 = timed(merge_sort, data)
        assert r1 == r2 == r3
        rows.append((n, t10, t256, tm))
        print(f"{n:>10,} | {t10:>12.4f} {t256:>13.4f} {tm:>10.4f}")
    print("-" * 52)
    print("Base 10 needs 10 passes for numbers up to 10^9; base 256 needs only 4.")
    print("So radix-256 is clearly fastest, while radix-10 does so many passes")
    print("that it is only about as fast as merge sort.")
    print()
    return rows


# ---------------------------------------------------------------
# 6. Plots
# ---------------------------------------------------------------
def make_plots(k_rows, n_rows):
    print("=" * 72)
    print("TASK 6: Plots")
    print("=" * 72)
    if not HAVE_PLOT:
        print("matplotlib is not installed, so no plots were made.")
        print("Install it with:  python3 -m pip install --user matplotlib")
        print()
        return

    ks = [r[0] for r in k_rows]
    plt.figure(figsize=(7, 4.5))
    plt.plot(ks, [r[1] for r in k_rows], "o-", label="Counting sort")
    plt.plot(ks, [r[2] for r in k_rows], "s-", label="Radix sort (base 10)")
    plt.plot(ks, [r[3] for r in k_rows], "^-", label="Radix sort (base 256)")
    plt.plot(ks, [r[4] for r in k_rows], "d-", label="Merge sort")
    plt.xscale("log")
    plt.xlabel("k (largest value)  [log scale]")
    plt.ylabel("time (seconds)")
    plt.title("n = 100,000, varying k  -  Sonam Choki 02240360")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("plot_vary_k.png", dpi=130)
    plt.close()

    ns = [r[0] for r in n_rows]
    plt.figure(figsize=(7, 4.5))
    plt.plot(ns, [r[1] for r in n_rows], "s-", label="Radix sort (base 10)")
    plt.plot(ns, [r[2] for r in n_rows], "^-", label="Radix sort (base 256)")
    plt.plot(ns, [r[3] for r in n_rows], "d-", label="Merge sort")
    plt.xlabel("n (number of elements)")
    plt.ylabel("time (seconds)")
    plt.title("k = 10^9, varying n  -  Sonam Choki 02240360")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("plot_vary_n.png", dpi=130)
    plt.close()
    print("Saved plot_vary_k.png and plot_vary_n.png in this folder.")
    print()


def explanation():
    print("=" * 72)
    print("When do the linear-time sorts WIN and when do they LOSE?")
    print("=" * 72)
    print(" WIN : counting sort when k is small (k <= n): O(n + k) ~ O(n).")
    print(" WIN : radix sort with a big base (256): few passes, beats n log n.")
    print(" LOSE: counting sort when k is huge (k >> n): the O(k) array dominates.")
    print(" LOSE: radix sort with a small base (10) on big numbers: 10 passes,")
    print("       so its big constant factor cancels the O(n) advantage.")
    print(" Also: they only work on integer keys; merge sort works on anything")
    print("       that can be compared.")
    print()


if __name__ == "__main__":
    print("CSF302 Lab 5 - Q2 Counting & Radix Sort | Sonam Choki | 02240360\n")
    random.seed(302)
    correctness_check()
    stability_demo()
    k_rows = vary_k()
    n_rows = vary_n()
    make_plots(k_rows, n_rows)
    explanation()
