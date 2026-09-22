"""
Lab 3 - Q2: Karatsuba's Algorithm for Large Integer Multiplication
====================================================================
Student Number: 02240360

Multiplies two large integers (represented as digit strings, so they
can exceed native integer limits) using:
  1. Traditional grade-school method  O(n^2)
  2. Karatsuba's algorithm (divide and conquer, 3 multiplications per split)  O(n^1.585)

Integers are padded to equal length and to the next power of 2 as
required by the recursive split, then verified against each other.
"""

import random
import time


# ---------------------------------------------------------------------------
# 1. Traditional grade-school multiplication  O(n^2)
#    Operates on digit strings to avoid relying on Python's built-in
#    big-int multiply (which is itself sub-quadratic / Karatsuba-based).
# ---------------------------------------------------------------------------
def traditional_multiply(x_str, y_str):
    x_digits = [int(d) for d in x_str[::-1]]  # little-endian digits
    y_digits = [int(d) for d in y_str[::-1]]
    n, m = len(x_digits), len(y_digits)
    result = [0] * (n + m)

    for i in range(n):
        carry = 0
        for j in range(m):
            result[i + j] += x_digits[i] * y_digits[j] + carry
            carry = result[i + j] // 10
            result[i + j] %= 10
        result[i + m] += carry

    # strip leading zeros (result is little-endian, so trailing entries)
    while len(result) > 1 and result[-1] == 0:
        result.pop()

    return int("".join(map(str, result[::-1])))


# ---------------------------------------------------------------------------
# 2. Karatsuba's algorithm  O(n^log2(3)) ~= O(n^1.585)
# ---------------------------------------------------------------------------
def karatsuba(x, y):
    """x, y are non-negative Python ints. Returns x * y using Karatsuba."""
    # Base case: single-digit multiplication
    if x < 10 or y < 10:
        return x * y

    n = max(len(str(x)), len(str(y)))
    m = n // 2

    high1, low1 = divmod(x, 10 ** m)
    high2, low2 = divmod(y, 10 ** m)

    # 3 recursive multiplications (instead of 4 in the naive divide & conquer)
    z0 = karatsuba(low1, low2)
    z2 = karatsuba(high1, high2)
    z1 = karatsuba(low1 + high1, low2 + high2) - z2 - z0

    return z2 * 10 ** (2 * m) + z1 * 10 ** m + z0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def generate_random_number(num_digits):
    """Generate a random integer string with exactly num_digits digits."""
    first = random.randint(1, 9)
    rest = "".join(str(random.randint(0, 9)) for _ in range(num_digits - 1))
    return str(first) + rest


def next_power_of_2(n):
    p = 1
    while p < n:
        p *= 2
    return p


def pad_to_length(num_str, length):
    """Pad a digit string with leading zeros to the given length."""
    return num_str.zfill(length)


def get_manual_number(label):
    while True:
        s = input(f"Enter integer {label}: ").strip()
        if s.isdigit():
            return s
        print("  Invalid input, digits only.")


# ---------------------------------------------------------------------------
# Demo / verification for a single pair (interactive-friendly)
# ---------------------------------------------------------------------------
def run_demo(num_digits=16, manual=False, seed=None):
    if seed is not None:
        random.seed(seed)

    if manual:
        x_str = get_manual_number("X")
        y_str = get_manual_number("Y")
    else:
        x_str = generate_random_number(num_digits)
        y_str = generate_random_number(num_digits)

    # Pad both operands to the same length, then to the next power of 2,
    # as required by the recursive split (padding does not change the value).
    common_len = max(len(x_str), len(y_str))
    padded_len = next_power_of_2(common_len)
    x_padded = pad_to_length(x_str, padded_len)
    y_padded = pad_to_length(y_str, padded_len)

    print(f"X = {x_str}  ({len(x_str)} digits)")
    print(f"Y = {y_str}  ({len(y_str)} digits)")
    print(f"Padded length (next power of 2): {padded_len}")

    x_int, y_int = int(x_padded), int(y_padded)

    t0 = time.perf_counter()
    result_trad = traditional_multiply(x_padded, y_padded)
    t1 = time.perf_counter()
    result_karatsuba = karatsuba(x_int, y_int)
    t2 = time.perf_counter()

    print(f"\nTraditional result:  {result_trad}")
    print(f"Karatsuba result:    {result_karatsuba}")

    match = result_trad == result_karatsuba
    print(f"\nResults match: {match}")
    print(f"Traditional time: {(t1 - t0) * 1000:.4f} ms")
    print(f"Karatsuba time:   {(t2 - t1) * 1000:.4f} ms")
    return match


# ---------------------------------------------------------------------------
# Benchmark across increasing digit counts
# ---------------------------------------------------------------------------
def benchmark(digit_sizes=(8, 16, 32, 64, 128, 256, 512, 1024), trials=3, seed=42):
    random.seed(seed)
    results = []
    print(f"{'digits':>7} | {'Traditional (s)':>16} | {'Karatsuba (s)':>14} | {'Match':>6}")
    print("-" * 54)
    for d in digit_sizes:
        trad_times = []
        karat_times = []
        match = True
        for _ in range(trials):
            x_str = generate_random_number(d)
            y_str = generate_random_number(d)
            padded_len = next_power_of_2(max(len(x_str), len(y_str)))
            x_padded = pad_to_length(x_str, padded_len)
            y_padded = pad_to_length(y_str, padded_len)
            x_int, y_int = int(x_padded), int(y_padded)

            t0 = time.perf_counter()
            r1 = traditional_multiply(x_padded, y_padded)
            t1 = time.perf_counter()
            r2 = karatsuba(x_int, y_int)
            t2 = time.perf_counter()

            trad_times.append(t1 - t0)
            karat_times.append(t2 - t1)
            match = match and (r1 == r2)

        avg_trad = sum(trad_times) / trials
        avg_karat = sum(karat_times) / trials
        results.append((d, avg_trad, avg_karat, match))
        print(f"{d:>7} | {avg_trad:>16.6f} | {avg_karat:>14.6f} | {str(match):>6}")

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("DEMO: 16-digit integer multiplication (random values)")
    print("=" * 60)
    run_demo(num_digits=16, seed=1)

    print("\n" + "=" * 60)
    print("BENCHMARK: digit sizes 8 through 1024 (powers of 2)")
    print("=" * 60)
    benchmark()
