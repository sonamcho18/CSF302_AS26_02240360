"""
CSF303 - Lab 2 - Q1: Prime Number Testing
Student: Sonam Choki (02240360)
Note: Variables are named with suffix "360" (last 3 digits of student number).
"""

import time
import matplotlib.pyplot as plt


# ---------------- Algorithm 1: Naive Method (check 2 to n-1) ----------------
def is_prime_naive_360(n360):
    steps360 = 0
    if n360 < 2:
        return False, steps360
    for i360 in range(2, n360):
        steps360 += 1
        if n360 % i360 == 0:
            return False, steps360
    return True, steps360


# ------------- Algorithm 2: Optimized Method (check up to sqrt(n)) -------------
def is_prime_optimized_360(n360):
    steps360 = 0
    if n360 < 2:
        return False, steps360
    i360 = 2
    while i360 * i360 <= n360:
        steps360 += 1
        if n360 % i360 == 0:
            return False, steps360
        i360 += 1
    return True, steps360


# ---------------- Optional: Sieve of Eratosthenes ----------------
def sieve_of_eratosthenes_360(limit360):
    is_prime_list360 = [True] * (limit360 + 1)
    if limit360 >= 0:
        is_prime_list360[0] = False
    if limit360 >= 1:
        is_prime_list360[1] = False
    steps360 = 0
    p360 = 2
    while p360 * p360 <= limit360:
        steps360 += 1
        if is_prime_list360[p360]:
            for multiple360 in range(p360 * p360, limit360 + 1, p360):
                is_prime_list360[multiple360] = False
                steps360 += 1
        p360 += 1
    primes360 = [num360 for num360, val360 in enumerate(is_prime_list360) if val360]
    return primes360, steps360


def get_numbers_from_user_360():
    numbers360 = []
    print("Enter at least 10 numbers (one per line):")
    while len(numbers360) < 10:
        raw_value360 = input(f"Enter number {len(numbers360) + 1}: ")
        try:
            numbers360.append(int(raw_value360))
        except ValueError:
            print("Invalid input. Please enter an integer.")
    return numbers360


def main():
    print("=== Q1: Prime Number Testing ===")
    numbers360 = get_numbers_from_user_360()

    print("\nNumber | Prime(Naive) | Steps(Naive) | Prime(Optimized) | Steps(Optimized)")
    print("-" * 82)

    naive_steps_list360 = []
    optimized_steps_list360 = []

    for n360 in numbers360:
        result_naive360, steps_naive360 = is_prime_naive_360(n360)
        result_opt360, steps_opt360 = is_prime_optimized_360(n360)
        naive_steps_list360.append(steps_naive360)
        optimized_steps_list360.append(steps_opt360)
        print(f"{n360:6} | {str(result_naive360):13} | {steps_naive360:13} | "
              f"{str(result_opt360):17} | {steps_opt360}")

    # ---- Timing comparison ----
    print("\n--- Timing Comparison (total time for all numbers) ---")
    start_time360 = time.time()
    for n360 in numbers360:
        is_prime_naive_360(n360)
    naive_time360 = time.time() - start_time360

    start_time360 = time.time()
    for n360 in numbers360:
        is_prime_optimized_360(n360)
    optimized_time360 = time.time() - start_time360

    print(f"Naive Method Total Time:     {naive_time360:.6f} seconds")
    print(f"Optimized Method Total Time: {optimized_time360:.6f} seconds")

    # ---- Optional: Sieve of Eratosthenes ----
    limit360 = max(numbers360) if numbers360 else 100
    limit360 = max(limit360, 2)
    primes_list360, sieve_steps360 = sieve_of_eratosthenes_360(limit360)
    print(f"\n--- Optional: Sieve of Eratosthenes (up to {limit360}) ---")
    print(f"Primes found: {primes_list360}")
    print(f"Steps taken: {sieve_steps360}")

    # ---- Plot Graph: Step count comparison ----
    plt.figure(figsize=(8, 5))
    plt.plot(numbers360, naive_steps_list360, marker='o', label='Naive Method')
    plt.plot(numbers360, optimized_steps_list360, marker='s', label='Optimized Method')
    plt.xlabel('Number (n)')
    plt.ylabel('Step Count')
    plt.title('Prime Testing: Naive vs Optimized (Step Count Comparison)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('prime_test_graph_360.png')
    print("\nGraph saved as prime_test_graph_360.png")


if __name__ == "__main__":
    main()
