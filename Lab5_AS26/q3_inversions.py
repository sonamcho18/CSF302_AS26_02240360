"""
CSF302 - Lab 5, Q3: Counting Inversions (tasks 1-4)
Name: Sonam Choki
Student Number: 02240360

An inversion is a pair of positions (i, j) with i < j but a[i] > a[j].
"""

import random
import time

TIME_LIMIT = 60.0      # stop brute force once it would exceed 60 seconds


# ---------------------------------------------------------------
# 1. Brute force: check every pair. O(n^2)
# ---------------------------------------------------------------
def count_inversions_brute(a):
    count = 0
    n = len(a)
    for i in range(n):
        ai = a[i]
        for j in range(i + 1, n):
            if ai > a[j]:
                count += 1
    return count


# ---------------------------------------------------------------
# 2. Merge-sort based: O(n log n)
#    While merging, if right[j] < left[i] then right[j] is smaller
#    than ALL the remaining items in left -> add len(left) - i.
# ---------------------------------------------------------------
def sort_and_count(a):
    """Return (sorted list, number of inversions)."""
    n = len(a)
    if n <= 1:
        return list(a), 0
    mid = n // 2
    left, inv_left = sort_and_count(a[:mid])
    right, inv_right = sort_and_count(a[mid:])
    merged = []
    i = j = 0
    split = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            split += len(left) - i      # all of left[i:] are > right[j]
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inv_left + inv_right + split


def count_inversions_merge(a):
    return sort_and_count(a)[1]


# ---------------------------------------------------------------
# 3. Verify both give the same answer
# ---------------------------------------------------------------
def verify():
    print("=" * 66)
    print("TASKS 1-3: Brute force vs merge-sort inversion count")
    print("=" * 66)
    examples = [[2, 4, 1, 3, 5], [5, 4, 3, 2, 1], [1, 2, 3, 4, 5], [3, 3, 1], []]
    for ex in examples:
        print(f"  {str(ex):<18} brute = {count_inversions_brute(ex):>2}   "
              f"merge = {count_inversions_merge(ex):>2}")
    rng = random.Random(302)
    tests = 0
    ok = True
    for n in [0, 1, 2, 10, 100, 500, 1000, 1500, 2000]:
        for _ in range(5):
            data = [rng.randint(0, n) for _ in range(n)]
            ok &= count_inversions_brute(data) == count_inversions_merge(data)
            tests += 1
    print(f"\n{tests} random arrays (size 0 up to 2,000) -> all answers match: {ok}")
    print()


# ---------------------------------------------------------------
# 4. Timing
# ---------------------------------------------------------------
def benchmark():
    print("=" * 66)
    print("TASK 4: Timing, n = 1,000 to 1,000,000")
    print("=" * 66)
    rng = random.Random(302)
    sizes = [1_000, 2_000, 5_000, 10_000, 20_000, 50_000,
             100_000, 200_000, 500_000, 1_000_000]
    print(f"{'n':>10} | {'brute (s)':>12} {'merge (s)':>10} | {'inversions':>16}")
    print("-" * 58)
    brute_stopped = False
    last_n = last_t = None
    for n in sizes:
        data = [rng.randint(0, 10 ** 9) for _ in range(n)]
        start = time.perf_counter()
        inv = count_inversions_merge(data)
        tm = time.perf_counter() - start

        brute_text = "stopped*"
        if not brute_stopped and last_t is not None:
            predicted = last_t * (n / last_n) ** 2       # O(n^2) growth
            if predicted > TIME_LIMIT:
                brute_stopped = True
        if not brute_stopped:
            start = time.perf_counter()
            inv_b = count_inversions_brute(data)
            tb = time.perf_counter() - start
            assert inv_b == inv
            brute_text = f"{tb:.4f}"
            last_n, last_t = n, tb
            if tb > TIME_LIMIT:
                brute_stopped = True
        print(f"{n:>10,} | {brute_text:>12} {tm:>10.4f} | {inv:>16,}")
    print("-" * 58)
    print(f"* stopped: brute force would take more than {TIME_LIMIT:.0f} seconds.")
    print("Brute force: doubling n -> about 4x slower (O(n^2)).")
    print("Merge sort : doubling n -> about 2x slower (O(n log n)).")
    print()


if __name__ == "__main__":
    print("CSF302 Lab 5 - Q3 Counting Inversions | Sonam Choki | 02240360\n")
    verify()
    benchmark()
