"""
CSF302 - Assignment 1 - Question 5
MINMAX: Divide-and-Conquer Minimum/Maximum Algorithm with comparison counter
Student: Sonam Choki | Student ID: 02240360
Variable naming uses the last 3 digits of the student ID: 360
"""

import random

comparisons_360 = 0  # global comparison counter (named using last 3 digits of student ID: 360)


def minmax_360(A, lo, hi):
    """
    Divide-and-conquer algorithm that returns (min, max) of A[lo..hi]
    using at most ceil(3n/2) - 2 comparisons.
    """
    global comparisons_360

    # Base case 1: single element
    if hi == lo:
        return A[lo], A[lo]

    # Base case 2: two elements -> exactly one comparison
    if hi == lo + 1:
        comparisons_360 += 1
        if A[lo] <= A[hi]:
            return A[lo], A[hi]
        else:
            return A[hi], A[lo]

    # Divide
    mid_360 = (lo + hi) // 2
    min1_360, max1_360 = minmax_360(A, lo, mid_360)
    min2_360, max2_360 = minmax_360(A, mid_360 + 1, hi)

    # Combine: exactly two comparisons
    comparisons_360 += 1
    result_min_360 = min1_360 if min1_360 <= min2_360 else min2_360

    comparisons_360 += 1
    result_max_360 = max1_360 if max1_360 >= max2_360 else max2_360

    return result_min_360, result_max_360


def run_trial_360(n_360):
    """Generate a random array of size n_360, run MINMAX, return comparisons used."""
    global comparisons_360
    comparisons_360 = 0
    array_360 = [random.randint(-100000, 100000) for _ in range(n_360)]
    found_min_360, found_max_360 = minmax_360(array_360, 0, n_360 - 1)

    # sanity check against built-in min/max
    assert found_min_360 == min(array_360)
    assert found_max_360 == max(array_360)

    return comparisons_360


def predicted_closed_form_360(n_360):
    """Closed form derived in Q5c: C(n) = 3n/2 - 2"""
    return (3 * n_360) // 2 - 2


def two_scan_360(n_360):
    """Naive two separate scans: 2n - 2 comparisons"""
    return 2 * n_360 - 2


if __name__ == "__main__":
    random.seed(360)  # reproducible results
    sizes_360 = [8, 64, 512, 4096]

    print(f"{'n':>6} | {'Measured':>10} | {'Predicted (3n/2 - 2)':>22} | {'2n - 2 (two-scan)':>18}")
    print("-" * 66)
    for n_360 in sizes_360:
        measured_360 = run_trial_360(n_360)
        predicted_360 = predicted_closed_form_360(n_360)
        two_scan_val_360 = two_scan_360(n_360)
        print(f"{n_360:>6} | {measured_360:>10} | {predicted_360:>22} | {two_scan_val_360:>18}")
