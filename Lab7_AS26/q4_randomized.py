"""
CSF302 - Lab 7, Q4: Randomized Algorithms
Name: Sonam Choki
Student Number: 02240360
"""

import math
import random
import time


# ---------------------------------------------------------------
# 1. Randomized quickselect: k-th smallest in expected O(n)
# ---------------------------------------------------------------
def quickselect(a, k):
    """Return the k-th smallest element (k = 1 is the minimum)."""
    a = list(a)
    while True:
        pivot = random.choice(a)
        less = [x for x in a if x < pivot]
        equal_count = 0
        greater = []
        for x in a:
            if x > pivot:
                greater.append(x)
            elif x == pivot:
                equal_count += 1
        if k <= len(less):
            a = less                                  # answer is on the left
        elif k <= len(less) + equal_count:
            return pivot                              # answer is the pivot
        else:
            k -= len(less) + equal_count              # answer is on the right
            a = greater


def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def part_1():
    print("=" * 74)
    print("TASK 1: Randomized quickselect vs sorting + indexing (k = n/2, median)")
    print("=" * 74)
    rng = random.Random(302)
    random.seed(302)
    print(f"{'n':>10} | {'quickselect (s)':>15} {'merge sort (s)':>15} "
          f"{'sorted() (s)':>13} | same answer")
    print("-" * 74)
    for n in [10 ** 4, 10 ** 5, 10 ** 6]:
        data = [rng.randint(0, 10 ** 9) for _ in range(n)]
        k = n // 2
        t0 = time.perf_counter()
        q = quickselect(data, k)
        t1 = time.perf_counter()
        m = merge_sort(data)[k - 1]
        t2 = time.perf_counter()
        s = sorted(data)[k - 1]
        t3 = time.perf_counter()
        print(f"{n:>10,} | {t1 - t0:>15.4f} {t2 - t1:>15.4f} {t3 - t2:>13.4f} | "
              f"{q == m == s}")
    print("-" * 74)
    print("Quickselect only keeps ONE side after each split, so its expected")
    print("work is n + n/2 + n/4 + ... = about 2n = O(n). Sorting is O(n log n).")
    print("Python's built-in sorted() is written in C, so it is very fast even")
    print("though it does more work. Against a sort written in Python (merge")
    print("sort), quickselect wins easily.")
    print()


# ---------------------------------------------------------------
# 2. Miller-Rabin primality test vs trial division
# ---------------------------------------------------------------
def miller_rabin(n, rounds=20, rng=random):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:              # write n - 1 = d * 2^r with d odd
        d //= 2
        r += 1
    for _ in range(rounds):
        a = rng.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False           # a proves n is composite
    return True                    # probably prime


def miller_rabin_one_round(n, rng):
    """One round, without the small-prime shortcut (used for 561)."""
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    a = rng.randint(2, n - 2)
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(r - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
    return False


def trial_division(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    if n % 3 == 0:
        return n == 3
    i = 5
    limit = math.isqrt(n)
    while i <= limit:              # only test up to sqrt(n)
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def part_2():
    print("=" * 74)
    print("TASK 2: Miller-Rabin vs trial division on 20 random 12-digit numbers")
    print("=" * 74)
    rng = random.Random(302)
    numbers = []
    for i in range(20):
        n = rng.randint(10 ** 11, 10 ** 12 - 1)
        if i % 2 == 1:             # every second number: move up to a prime,
            n |= 1                 # so both "prime" and "composite" appear
            while not trial_division(n):
                n += 2
        numbers.append(n)
    print(f"{'#':>3} {'number':>14} | {'Miller-Rabin':>12} {'time (s)':>10} | "
          f"{'trial div':>9} {'time (s)':>9} | agree")
    print("-" * 74)
    tot_mr = tot_td = 0.0
    agree = 0
    for i, n in enumerate(numbers, 1):
        t0 = time.perf_counter()
        a = miller_rabin(n, rng=rng)
        t1 = time.perf_counter()
        b = trial_division(n)
        t2 = time.perf_counter()
        tot_mr += t1 - t0
        tot_td += t2 - t1
        agree += a == b
        print(f"{i:>3} {n:>14} | {'prime' if a else 'composite':>12} {t1 - t0:>10.6f} | "
              f"{'prime' if b else 'composite':>9} {t2 - t1:>9.6f} | {'YES' if a == b else 'NO'}")
    print("-" * 74)
    print(f"Both agree on {agree}/20 numbers.")
    print(f"Total time: Miller-Rabin = {tot_mr:.4f} s, trial division = {tot_td:.4f} s")
    print("Trial division may need about sqrt(10^12)/3 = 333,000 divisions for a")
    print("prime. Miller-Rabin does one fast modular power (about 40 squarings)")
    print("per round, so 20 rounds take only about a thousand multiplications.")
    print()


# ---------------------------------------------------------------
# 3. Carmichael number 561 = 3 x 11 x 17, one round, 1000 times
# ---------------------------------------------------------------
def part_3():
    print("=" * 74)
    print("TASK 3: Miller-Rabin with 1 round on Carmichael number 561, 1000 times")
    print("=" * 74)
    rng = random.Random(302)
    n = 561
    print(f"561 = 3 x 11 x 17, so it is NOT prime. Trial division says: "
          f"{'prime' if trial_division(n) else 'composite'}")
    fermat_liars = sum(1 for a in range(2, n - 1)
                       if math.gcd(a, n) == 1 and pow(a, n - 1, n) == 1)
    strong_liars = [a for a in range(2, n - 1)
                    if miller_rabin_one_round_fixed(n, a)]
    runs = 1000
    said_prime = sum(miller_rabin_one_round(n, rng) for _ in range(runs))
    print(f"Times Miller-Rabin (1 round) answered 'prime': {said_prime} / {runs}"
          f"  = {said_prime / runs * 100:.1f}%")
    print(f"Times it correctly answered 'composite'      : {runs - said_prime} / {runs}")
    print()
    print(f"Bases a in 2..559 that FOOL Miller-Rabin ('strong liars'): "
          f"{len(strong_liars)} -> {strong_liars}")
    print(f"Expected error rate = {len(strong_liars)}/558 = "
          f"{len(strong_liars) / 558 * 100:.1f}%  (theory says at most 25%)")
    print(f"Compare: the simpler Fermat test is fooled by {fermat_liars} bases "
          f"({fermat_liars / 558 * 100:.0f}%),")
    print("because 561 is a Carmichael number. Miller-Rabin's extra square-root")
    print("check catches it almost every time, and with 20 rounds the chance of")
    print("a wrong answer is below (1/4)^20, which is less than one in a trillion.")
    print()


def miller_rabin_one_round_fixed(n, a):
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(r - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
    return False


if __name__ == "__main__":
    print("CSF302 Lab 7 - Q4 Randomized Algorithms | Sonam Choki | 02240360\n")
    part_1()
    part_2()
    part_3()
