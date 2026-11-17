"""
CSF302 - Lab 4, Part A: Efficient Modular Exponentiation
Name: Sonam Choki
Student Number: 02240360
"""

import random
import time


# ---------------------------------------------------------------
# Task 5: Input validation (shared by both algorithms)
# ---------------------------------------------------------------
def validate(a, b, m):
    """Check the inputs and return the base reduced mod m."""
    if m < 1:
        raise ValueError(f"Invalid modulus m = {m}. Modulus must be >= 1.")
    if b < 0:
        raise ValueError(f"Negative exponent b = {b} is not supported.")
    # Negative base: reduce a mod m first (Python's % always gives 0..m-1)
    return a % m


# ---------------------------------------------------------------
# Task 1: Naive modular exponentiation (repeated multiplication)
# ---------------------------------------------------------------
def naive_mod_exp(a, b, m):
    """Compute a^b mod m by multiplying a, b times. O(b) time."""
    a = validate(a, b, m)
    result = 1 % m              # zero exponent -> 1 mod m
    for _ in range(b):
        result = (result * a) % m
    return result


# ---------------------------------------------------------------
# Task 2: Binary exponentiation (square-and-multiply)
# ---------------------------------------------------------------
def binary_mod_exp(a, b, m):
    """Square-and-multiply using % 2 and // 2. O(log b) time."""
    a = validate(a, b, m)
    result = 1 % m
    while b > 0:
        if b % 2 == 1:          # exponent is odd
            result = (result * a) % m
        a = (a * a) % m         # square the base
        b = b // 2              # halve the exponent
    return result


# ---------------------------------------------------------------
# Task 4: Binary exponentiation with bitwise operations
# ---------------------------------------------------------------
def binary_mod_exp_bitwise(a, b, m):
    """Same as above but uses b & 1 and b >>= 1."""
    a = validate(a, b, m)
    result = 1 % m
    while b > 0:
        if b & 1:               # lowest bit set -> odd exponent
            result = (result * a) % m
        a = (a * a) % m
        b >>= 1                 # shift right = halve
    return result


# ---------------------------------------------------------------
# Task 3: Compare outputs
# ---------------------------------------------------------------
def compare_outputs():
    print("=" * 78)
    print("TASK 3: Comparing naive vs binary vs bitwise outputs")
    print("=" * 78)
    test_cases = [
        (2, 10, 1000),
        (3, 13, 7),
        (5, 0, 13),       # zero exponent
        (7, 1, 1),        # modulus 1 -> always 0
        (-3, 5, 11),      # negative base
        (10, 100, 17),
        (123, 456, 789),
        (2, 1000, 1_000_000_007),
    ]
    random.seed(302)
    for _ in range(4):
        test_cases.append((random.randint(-1000, 1000),
                           random.randint(0, 2000),
                           random.randint(1, 10_000)))

    print(f"{'a':>7} {'b':>6} {'m':>12} | {'naive':>10} {'binary':>10} "
          f"{'bitwise':>10} {'pow()':>10} | match")
    print("-" * 78)
    all_ok = True
    for a, b, m in test_cases:
        n = naive_mod_exp(a, b, m)
        bi = binary_mod_exp(a, b, m)
        bw = binary_mod_exp_bitwise(a, b, m)
        ref = pow(a, b, m)          # Python built-in, used as a check
        ok = n == bi == bw == ref
        all_ok &= ok
        print(f"{a:>7} {b:>6} {m:>12} | {n:>10} {bi:>10} {bw:>10} "
              f"{ref:>10} | {'YES' if ok else 'NO'}")
    print("-" * 78)
    print("All results match:", all_ok)
    print()


# ---------------------------------------------------------------
# Task 5: Show input validation working
# ---------------------------------------------------------------
def demo_validation():
    print("=" * 78)
    print("TASK 5: Input validation")
    print("=" * 78)
    print("Zero exponent    5^0 mod 13   =", binary_mod_exp_bitwise(5, 0, 13))
    print("Zero exp, m = 1  5^0 mod 1    =", binary_mod_exp_bitwise(5, 0, 1))
    print("Negative base   (-3)^5 mod 11 =", binary_mod_exp_bitwise(-3, 5, 11),
          " (same as 8^5 mod 11 =", binary_mod_exp_bitwise(8, 5, 11), ")")
    for args, label in [((2, -3, 7), "Negative exponent 2^-3 mod 7"),
                        ((2, 3, 0), "Invalid modulus   2^3 mod 0"),
                        ((2, 3, -5), "Invalid modulus   2^3 mod -5")]:
        try:
            binary_mod_exp_bitwise(*args)
        except ValueError as e:
            print(f"{label:<30} -> ValueError: {e}")
    print()


# ---------------------------------------------------------------
# Task 6: Timing comparison
# ---------------------------------------------------------------
def time_it(func, *args, repeats=1):
    start = time.perf_counter()
    for _ in range(repeats):
        result = func(*args)
    return (time.perf_counter() - start) / repeats, result


def benchmark():
    print("=" * 78)
    print("TASK 6: Execution time, naive vs binary (a = 7, m = 10^9 + 7)")
    print("=" * 78)
    a, m = 7, 1_000_000_007
    print(f"{'b':>10} | {'naive (s)':>12} {'binary (s)':>12} "
          f"{'bitwise (s)':>12} | {'speed-up':>10}")
    print("-" * 70)
    for k in range(1, 7):
        b = 10 ** k
        t_naive, r1 = time_it(naive_mod_exp, a, b, m)
        t_bin, r2 = time_it(binary_mod_exp, a, b, m, repeats=1000)
        t_bit, r3 = time_it(binary_mod_exp_bitwise, a, b, m, repeats=1000)
        assert r1 == r2 == r3
        print(f"{b:>10} | {t_naive:>12.6f} {t_bin:>12.8f} {t_bit:>12.8f} | "
              f"{t_naive / t_bit:>9.0f}x")
    print("-" * 70)
    print("Naive time grows ~10x each row (O(b)); binary barely changes (O(log b)).")
    print()


if __name__ == "__main__":
    print("CSF302 Lab 4 - Part A | Sonam Choki | 02240360\n")
    compare_outputs()
    demo_validation()
    benchmark()
