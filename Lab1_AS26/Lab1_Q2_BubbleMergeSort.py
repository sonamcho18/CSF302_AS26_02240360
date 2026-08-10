"""
Lab1_Q2_BubbleMergeSort.py

Student Number: 02240360

Question 2
-----------
1. Implement Bubble Sort.
2. Implement Merge Sort.
3. Generate random arrays.
4. Measure average execution time.

Input sizes tested: 100 / 500 / 1000 / 2000 / 4000 / 8000
"""

import random
import time
import copy


def generate_random_array_360(size, lower=0, upper=1_000_000):
    """
    Generate a list of `size` random integers in the range [lower, upper].
    """
    return [random.randint(lower, upper) for _ in range(size)]


def bubble_sort_360(arr):
    """
    Bubble Sort.
    Repeatedly steps through the list, comparing adjacent elements and
    swapping them if they are in the wrong order. Sorts the list IN PLACE.

    Includes an early-exit optimization: if a full pass makes no swaps,
    the array is already sorted and the algorithm stops early.

    Time Complexity: O(n^2) worst/average case, O(n) best case (already sorted)
    """
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def merge_360(left, right):
    """
    Helper function for Merge Sort.
    Merges two already-sorted lists (`left`, `right`) into a single
    sorted list.
    """
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append any remaining elements (one of these will be empty)
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def merge_sort_360(arr):
    """
    Merge Sort (recursive, divide-and-conquer).
    Splits the array into halves, recursively sorts each half, then
    merges the sorted halves back together. Returns a NEW sorted list.

    Time Complexity: O(n log n) in all cases.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort_360(arr[:mid])
    right_half = merge_sort_360(arr[mid:])

    return merge_360(left_half, right_half)


def measure_average_time_360(func, arr, trials=5):
    """
    Runs `func` on a fresh deep copy of `arr` for `trials` runs and
    returns the average execution time in seconds. A fresh copy is used
    each trial because both sorting algorithms consume/mutate their input.
    """
    total_time = 0.0
    for _ in range(trials):
        arr_copy = copy.deepcopy(arr)
        start = time.perf_counter()
        func(arr_copy)
        end = time.perf_counter()
        total_time += (end - start)
    return total_time / trials


def run_experiment_360():
    """
    Runs Bubble Sort and Merge Sort on random arrays of increasing size,
    times both algorithms (averaged over several trials), and prints a
    comparison table.
    """
    input_sizes = [100, 500, 1000, 2000, 4000, 8000]
    trials = 5

    print("Question 2: Bubble Sort vs Merge Sort")
    print(f"{'Size':>10} | {'Bubble Sort (s)':>20} | {'Merge Sort (s)':>20}")
    print("-" * 56)

    for size in input_sizes:
        # 3. Generate a random array for this size
        arr = generate_random_array_360(size)

        # 4. Measure average execution time for both algorithms
        bubble_time = measure_average_time_360(bubble_sort_360, arr, trials=trials)
        merge_time = measure_average_time_360(merge_sort_360, arr, trials=trials)

        print(f"{size:>10} | {bubble_time:>20.6f} | {merge_time:>20.6f}")


if __name__ == "__main__":
    run_experiment_360()
