"""
Lab1_Q1_BinarySearch.py

CSF302 - Algorithm Analysis - Assignment 26
Student Number: 02240360

Question 1
-----------
1. Implement Linear Search.
2. Implement Binary Search.
3. Generate random datasets of different sizes.
4. Sort the dataset before applying Binary Search.
5. Measure the average execution time for both algorithms.

Input sizes tested: 1,000 / 5,000 / 10,000 / 50,000 / 100,000 / 500,000 / 1,000,000
"""

import random
import time


def generate_random_dataset_360(size, lower=0, upper=10_000_000):
    """
    Generate a list of `size` random integers in the range [lower, upper].
    """
    return [random.randint(lower, upper) for _ in range(size)]


def linear_search_360(data, target):
    """
    Linear Search.
    Scans the list sequentially from the start until the target is found
    (or the list is exhausted).

    Parameters:
        data   -- list to search (unsorted or sorted, doesn't matter)
        target -- value being searched for

    Returns:
        Index of `target` if found, else -1.

    Time Complexity: O(n)
    """
    for index in range(len(data)):
        if data[index] == target:
            return index
    return -1


def binary_search_360(sorted_data, target):
    """
    Binary Search (iterative).
    Repeatedly halves the search interval on a SORTED list until the
    target is found.

    Parameters:
        sorted_data -- list sorted in ascending order
        target      -- value being searched for

    Returns:
        Index of `target` if found, else -1.

    Time Complexity: O(log n)
    """
    low = 0
    high = len(sorted_data) - 1

    while low <= high:
        mid = (low + high) // 2
        if sorted_data[mid] == target:
            return mid
        elif sorted_data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def measure_average_time_360(func, args, trials=5):
    """
    Runs `func(*args)` `trials` times and returns the average execution
    time in seconds, measured using a high-resolution performance counter.
    """
    total_time = 0.0
    for _ in range(trials):
        start = time.perf_counter()
        func(*args)
        end = time.perf_counter()
        total_time += (end - start)
    return total_time / trials


def run_experiment_360():
    """
    Runs Linear Search and Binary Search on random datasets of increasing
    size, times both algorithms (averaged over several trials), and
    prints a comparison table.
    """
    input_sizes = [1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
    trials = 5

    print("Question 1: Linear Search vs Binary Search")
    print(f"{'Size':>10} | {'Linear Search (s)':>20} | {'Binary Search (s)':>20}")
    print("-" * 58)

    for size in input_sizes:
        # 3. Generate a random dataset for this size
        dataset = generate_random_dataset_360(size)

        # Search for the last element -> guarantees the element exists
        # and represents a fair (near worst-case) test for Linear Search.
        target = dataset[-1]

        # 4. Sort a copy of the dataset before running Binary Search
        sorted_dataset = sorted(dataset)

        # 5. Measure average execution time for both algorithms
        linear_time = measure_average_time_360(
            linear_search_360, (dataset, target), trials=trials
        )
        binary_time = measure_average_time_360(
            binary_search_360, (sorted_dataset, target), trials=trials
        )

        print(f"{size:>10} | {linear_time:>20.6f} | {binary_time:>20.6f}")


if __name__ == "__main__":
    run_experiment_360()
