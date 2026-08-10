"""
Lab1_Q3_PrimeGeneration.py

CSF302 - Algorithm Analysis - Assignment 26
Student Number: 02240360

Question 3
-----------
Compare different methods of generating prime numbers and analyze their
empirical performance.

Tasks:
1. Naive Prime Checking using Trial Division.
2. Optimized Trial Division (checking up to sqrt(n)).
3. Sieve of Eratosthenes.

Measure the execution time required to generate all prime numbers up to N.
Input sizes tested: 10,000 / 50,000 / 100,000 / 500,000 / 1,000,000
"""

import time
import math


def is_prime_naive_360(n):
    """
    Naive primality test.
    Checks divisibility of `n` by every integer from 2 up to n - 1.

    Time Complexity: O(n) per number checked.
    """
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def generate_primes_naive_360(limit):
    """
    Generates all primes in the range [2, limit] using the naive
    (unoptimized) trial division check for every candidate number.

    Time Complexity: O(n^2) overall (O(n) work per number, n numbers).
    """
    primes = []
    for num in range(2, limit + 1):
        if is_prime_naive_360(num):
            primes.append(num)
    return primes


def is_prime_optimized_360(n):
    """
    Optimized primality test.
    Only checks divisors up to sqrt(n), since any composite number must
    have at least one factor <= sqrt(n). Also skips even numbers after
    checking 2, cutting the work roughly in half again.

    Time Complexity: O(sqrt(n)) per number checked.
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    for i in range(3, math.isqrt(n) + 1, 2):
        if n % i == 0:
            return False
    return True


def generate_primes_optimized_360(limit):
    """
    Generates all primes in the range [2, limit] using the optimized
    (sqrt-bounded) trial division check for every candidate number.

    Time Complexity: O(n * sqrt(n)) overall.
    """
    primes = []
    for num in range(2, limit + 1):
        if is_prime_optimized_360(num):
            primes.append(num)
    return primes


def sieve_of_eratosthenes_360(limit):
    """
    Sieve of Eratosthenes.
    Builds a boolean array marking every index as "prime" initially, then
    iteratively marks the multiples of each found prime as composite,
    starting from i*i (smaller multiples are already marked by smaller
    primes).

    Time Complexity: O(n log log n) overall.
    """
    if limit < 2:
        return []

    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, math.isqrt(limit) + 1):
        if is_prime[i]:
            for multiple in range(i * i, limit + 1, i):
                is_prime[multiple] = False

    return [num for num, flag in enumerate(is_prime) if flag]


def measure_time_360(func, *args):
    """
    Runs `func(*args)` a single time and returns the execution time in
    seconds. A single run is sufficient here since these algorithms are
    fully deterministic (no randomness involved), unlike Q1/Q2.
    """
    start = time.perf_counter()
    func(*args)
    end = time.perf_counter()
    return end - start


def run_experiment_360():
    """
    Runs all three prime-generation methods for each value of N in
    `input_sizes`, times them, and prints a comparison table.

    Note: The Naive Trial Division method (O(n^2) overall) becomes
    extremely slow for large N. To keep the experiment runnable in a
    reasonable amount of time, it is skipped for N > naive_cutoff and
    marked as "skipped" in the output table -- this is itself useful
    empirical evidence of how poorly the naive approach scales.
    """
    input_sizes = [10_000, 50_000, 100_000, 500_000, 1_000_000]
    naive_cutoff = 100_000  # beyond this, naive method is skipped (too slow)

    print("Question 3: Naive vs Optimized Trial Division vs Sieve of Eratosthenes")
    print(f"{'N':>10} | {'Naive (s)':>15} | {'Optimized (s)':>15} | {'Sieve (s)':>15}")
    print("-" * 65)

    for limit in input_sizes:
        optimized_time = measure_time_360(generate_primes_optimized_360, limit)
        sieve_time = measure_time_360(sieve_of_eratosthenes_360, limit)

        if limit <= naive_cutoff:
            naive_time = measure_time_360(generate_primes_naive_360, limit)
            naive_str = f"{naive_time:>15.6f}"
        else:
            naive_str = f"{'skipped':>15}"

        print(f"{limit:>10} | {naive_str} | {optimized_time:>15.6f} | {sieve_time:>15.6f}")

    print("\nNote: Naive method skipped for N > 100,000 due to O(n^2) runtime "
          "becoming impractically slow for demonstration purposes.")


if __name__ == "__main__":
    run_experiment_360()
