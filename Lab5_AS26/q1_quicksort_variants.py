"""
CSF302 - Lab 5, Q1: Quicksort Variants
Name: Sonam Choki
Student Number: 02240360

Every variant:
  * sorts the list in place and returns the number of comparisons made
  * recurses on the SMALLER part and loops on the LARGER part (task 7),
    so the recursion depth is at most about log2(n), even on sorted input.
"""

import random
import sys
import time

# If a quadratic case is predicted to take longer than this (seconds),
# it is skipped. Raise it to run everything (it may take a few minutes).
SKIP_IF_PREDICTED_OVER = 25.0


# ---------------------------------------------------------------
# 1. Lomuto partition (last element as pivot)
# ---------------------------------------------------------------
def quicksort_lomuto(a):
    comps = 0

    def sort(lo, hi):
        nonlocal comps
        while lo < hi:
            pivot = a[hi]
            i = lo - 1
            for j in range(lo, hi):
                comps += 1
                if a[j] <= pivot:
                    i += 1
                    a[i], a[j] = a[j], a[i]
            p = i + 1
            a[p], a[hi] = a[hi], a[p]
            # recurse on smaller side, loop on larger side
            if p - lo < hi - p:
                sort(lo, p - 1)
                lo = p + 1
            else:
                sort(p + 1, hi)
                hi = p - 1

    sort(0, len(a) - 1)
    return comps


# ---------------------------------------------------------------
# 2. Hoare partition (first element as pivot, classic version)
# ---------------------------------------------------------------
def quicksort_hoare(a):
    comps = 0

    def sort(lo, hi):
        nonlocal comps
        while lo < hi:
            pivot = a[lo]
            i, j = lo - 1, hi + 1
            while True:
                j -= 1
                comps += 1
                while a[j] > pivot:
                    j -= 1
                    comps += 1
                i += 1
                comps += 1
                while a[i] < pivot:
                    i += 1
                    comps += 1
                if i < j:
                    a[i], a[j] = a[j], a[i]
                else:
                    p = j
                    break
            # parts are [lo, p] and [p+1, hi]
            if p - lo < hi - p:
                sort(lo, p)
                lo = p + 1
            else:
                sort(p + 1, hi)
                hi = p

    sort(0, len(a) - 1)
    return comps


# ---------------------------------------------------------------
# 3. Randomised quicksort (random pivot + Lomuto partition)
# ---------------------------------------------------------------
def quicksort_randomised(a):
    comps = 0
    rand = random.randint

    def sort(lo, hi):
        nonlocal comps
        while lo < hi:
            r = rand(lo, hi)
            a[r], a[hi] = a[hi], a[r]          # move random pivot to the end
            pivot = a[hi]
            i = lo - 1
            for j in range(lo, hi):
                comps += 1
                if a[j] <= pivot:
                    i += 1
                    a[i], a[j] = a[j], a[i]
            p = i + 1
            a[p], a[hi] = a[hi], a[p]
            if p - lo < hi - p:
                sort(lo, p - 1)
                lo = p + 1
            else:
                sort(p + 1, hi)
                hi = p - 1

    sort(0, len(a) - 1)
    return comps


# ---------------------------------------------------------------
# 4. Three-way (Dutch national flag) quicksort, random pivot
#    Splits into  < pivot | == pivot | > pivot
# ---------------------------------------------------------------
def quicksort_three_way(a):
    comps = 0
    rand = random.randint

    def sort(lo, hi):
        nonlocal comps
        while lo < hi:
            pivot = a[rand(lo, hi)]
            lt, i, gt = lo, lo, hi
            while i <= gt:
                comps += 1
                if a[i] < pivot:
                    a[lt], a[i] = a[i], a[lt]
                    lt += 1
                    i += 1
                else:
                    comps += 1
                    if a[i] > pivot:
                        a[i], a[gt] = a[gt], a[i]
                        gt -= 1
                    else:
                        i += 1
            # a[lt..gt] all equal pivot -> already in place
            if lt - lo < hi - gt:
                sort(lo, lt - 1)
                lo = gt + 1
            else:
                sort(gt + 1, hi)
                hi = lt - 1

    sort(0, len(a) - 1)
    return comps


VARIANTS = [
    ("Lomuto", quicksort_lomuto),
    ("Hoare", quicksort_hoare),
    ("Randomised", quicksort_randomised),
    ("Three-way", quicksort_three_way),
]


def make_input(kind, n, rng):
    if kind == "random":
        return [rng.randint(0, 10 * n) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "reverse":
        return list(range(n, 0, -1))
    if kind == "duplicates":
        return [rng.randint(0, 9) for _ in range(n)]
    raise ValueError(kind)


INPUT_TYPES = ["random", "sorted", "reverse", "duplicates"]
SIZES = [1000, 2000, 4000, 8000, 16000]


def correctness_check():
    print("=" * 74)
    print("CORRECTNESS CHECK: every variant vs Python's sorted()")
    print("=" * 74)
    rng = random.Random(1)
    ok = True
    for name, fn in VARIANTS:
        for trial in range(200):
            n = rng.randint(0, 60)
            data = [rng.randint(-20, 20) for _ in range(n)]
            b = data[:]
            fn(b)
            ok &= (b == sorted(data))
        print(f"  {name:<11} 200 random tests passed: {ok}")
    print(f"All variants correct: {ok}\n")


def benchmark():
    print("=" * 74)
    print("TASKS 5-6: Comparisons and time for each variant and input type")
    print("=" * 74)
    print(f"Recursion limit = {sys.getrecursionlimit()} (we never get near it, "
          "thanks to task 7)\n")
    rng = random.Random(302)
    results = {}  # (variant, kind, n) -> (comps, time)

    for kind in INPUT_TYPES:
        print(f"--- Input type: {kind.upper()} ---")
        print(f"{'n':>7} | " + " | ".join(f"{name:^22}" for name, _ in VARIANTS))
        print(f"{'':>7} | " + " | ".join(f"{'comparisons':>12} {'time(s)':>9}"
                                       for _ in VARIANTS))
        print("-" * 106)
        last_time = {}
        for n in SIZES:
            base = make_input(kind, n, rng)
            cells = []
            for name, fn in VARIANTS:
                prev = last_time.get(name)
                # quadratic growth: doubling n -> about 4x the time
                if prev is not None and prev * 4 > SKIP_IF_PREDICTED_OVER:
                    cells.append(f"{'skipped*':>12} {'-':>9}")
                    last_time[name] = prev * 4
                    continue
                arr = base[:]
                random.seed(n)
                start = time.perf_counter()
                comps = fn(arr)
                t = time.perf_counter() - start
                assert arr == sorted(base), f"{name} failed"
                last_time[name] = t
                results[(name, kind, n)] = (comps, t)
                cells.append(f"{comps:>12,} {t:>9.4f}")
            print(f"{n:>7} | " + " | ".join(cells))
        print()

    if len(results) < len(VARIANTS) * len(INPUT_TYPES) * len(SIZES):
        print(f"* skipped: predicted time > {SKIP_IF_PREDICTED_OVER:.0f} s "
              "(quadratic case). Change SKIP_IF_PREDICTED_OVER to run it.\n")
    return results


def growth_summary(results):
    print("=" * 74)
    print("TASK 8: Which variant degrades to Theta(n^2)?")
    print("=" * 74)
    print("Ratio = comparisons(n=16000) / comparisons(n=8000).")
    print("  about 2   -> n log n (good)")
    print("  about 4   -> n^2     (bad, quadratic)\n")
    print(f"{'variant':<11} | " + " | ".join(f"{k:>10}" for k in INPUT_TYPES))
    print("-" * 62)
    for name, _ in VARIANTS:
        cells = []
        for kind in INPUT_TYPES:
            a = results.get((name, kind, 8000))
            b = results.get((name, kind, 16000))
            if a and b:
                r = b[0] / a[0]
                tag = "n^2" if r > 3.2 else "nlogn"
                cells.append(f"{r:>4.2f} {tag:>5}")
            else:
                cells.append(f"{'n/a':>10}")
        print(f"{name:<11} | " + " | ".join(cells))
    print()
    print("Explanation:")
    print(" - Lomuto (last pivot): sorted & reverse input -> pivot is always the")
    print("   largest/smallest, so one side is empty each time -> n^2.")
    print("   Duplicates -> all keys equal to the pivot go to ONE side -> n^2.")
    print(" - Hoare (first pivot): sorted & reverse input -> bad pivot -> n^2.")
    print("   Duplicates are fine: equal keys are swapped to BOTH sides.")
    print(" - Randomised: random pivot fixes sorted/reverse input, but it still")
    print("   uses Lomuto, so many duplicates still give n^2.")
    print(" - Three-way: random pivot AND equal keys are grouped in the middle")
    print("   and never touched again -> fast on every input type.")
    print()


if __name__ == "__main__":
    print("CSF302 Lab 5 - Q1 Quicksort Variants | Sonam Choki | 02240360\n")
    correctness_check()
    res = benchmark()
    growth_summary(res)
