"""
Lab 3 - Q3: Binary Search vs Ternary Search (Menu-Driven Program)
====================================================================
Student Number: 02240360

Searches for a key in a sorted array of n integers using Binary Search
and Ternary Search, and analyzes step/frequency (comparison) counts.

Menu:
  1. Generate n sorted random numbers -> Array
  2. Display Array
  3. Search for a key using Binary Search
  4. Search for a key using Ternary Search
  5. Step/frequency count for best case (key present, minimum comparisons)
  6. Step/frequency count for worst case (key absent / last comparison)
  7. Step/frequency count comparison table across increasing n
"""

import random


# ---------------------------------------------------------------------------
# 1. Binary Search  ->  T(n) = T(n/2) + O(1)
# ---------------------------------------------------------------------------
def binary_search(arr, key):
    """Returns (index_or_-1, comparison_count)."""
    lo, hi = 0, len(arr) - 1
    comparisons = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        comparisons += 1
        if arr[mid] == key:
            return mid, comparisons
        comparisons += 1
        if arr[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, comparisons


# ---------------------------------------------------------------------------
# 2. Ternary Search  ->  T(n) = T(n/3) + O(1)
# ---------------------------------------------------------------------------
def ternary_search(arr, key):
    """Returns (index_or_-1, comparison_count)."""
    lo, hi = 0, len(arr) - 1
    comparisons = 0
    while lo <= hi:
        mid1 = lo + (hi - lo) // 3
        mid2 = hi - (hi - lo) // 3

        comparisons += 1
        if arr[mid1] == key:
            return mid1, comparisons
        comparisons += 1
        if arr[mid2] == key:
            return mid2, comparisons

        comparisons += 1
        if key < arr[mid1]:
            hi = mid1 - 1
        else:
            comparisons += 1
            if key > arr[mid2]:
                lo = mid2 + 1
            else:
                lo, hi = mid1 + 1, mid2 - 1
    return -1, comparisons


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def generate_sorted_array(n, low=1, high=None):
    if high is None:
        high = max(n * 10, 100)
    values = random.sample(range(low, high), min(n, high - low))
    values.sort()
    return values


def best_case_binary(arr):
    """Key at the first-checked mid index -> 2 comparisons (found on first probe)."""
    mid = (0 + (len(arr) - 1)) // 2
    return arr[mid]


def best_case_ternary(arr):
    """Key at the first mid1 probe -> found in fewest comparisons."""
    lo, hi = 0, len(arr) - 1
    mid1 = lo + (hi - lo) // 3
    return arr[mid1]


def worst_case_key(arr):
    """A value guaranteed not to be in the array -> forces full search to exhaustion."""
    return arr[-1] + 1 if arr else 1


# ---------------------------------------------------------------------------
# Menu-driven interactive program
# ---------------------------------------------------------------------------
def comparison_table(sizes=(10, 50, 100, 500, 1000, 5000, 10000), seed=42):
    random.seed(seed)
    rows = []
    print(f"{'n':>7} | {'Binary (best)':>13} | {'Binary (worst)':>14} | "
          f"{'Ternary (best)':>14} | {'Ternary (worst)':>15}")
    print("-" * 76)
    for n in sizes:
        arr = generate_sorted_array(n)
        b_best_key = best_case_binary(arr)
        t_best_key = best_case_ternary(arr)
        w_key = worst_case_key(arr)

        _, b_best_c = binary_search(arr, b_best_key)
        _, b_worst_c = binary_search(arr, w_key)
        _, t_best_c = ternary_search(arr, t_best_key)
        _, t_worst_c = ternary_search(arr, w_key)

        rows.append((n, b_best_c, b_worst_c, t_best_c, t_worst_c))
        print(f"{n:>7} | {b_best_c:>13} | {b_worst_c:>14} | {t_best_c:>14} | {t_worst_c:>15}")
    return rows


def menu():
    arr = []
    while True:
        print("\n" + "=" * 55)
        print("MENU")
        print("1. Generate n sorted random numbers -> Array")
        print("2. Display Array")
        print("3. Search for a key using Binary Search")
        print("4. Search for a key using Ternary Search")
        print("5. Step/frequency count for best case")
        print("6. Step/frequency count for worst case")
        print("7. Step/frequency count comparison table across increasing n")
        print("0. Exit")
        print("=" * 55)
        choice = input("Enter choice: ").strip()

        if choice == "1":
            n = int(input("Enter n: "))
            arr = generate_sorted_array(n)
            print(f"Generated {len(arr)} sorted values.")
        elif choice == "2":
            print(arr)
        elif choice == "3":
            if not arr:
                print("Generate the array first (option 1).")
                continue
            key = int(input("Enter key to search: "))
            idx, c = binary_search(arr, key)
            print(f"Binary Search -> index: {idx}, comparisons: {c}")
        elif choice == "4":
            if not arr:
                print("Generate the array first (option 1).")
                continue
            key = int(input("Enter key to search: "))
            idx, c = ternary_search(arr, key)
            print(f"Ternary Search -> index: {idx}, comparisons: {c}")
        elif choice == "5":
            if not arr:
                print("Generate the array first (option 1).")
                continue
            bkey = best_case_binary(arr)
            tkey = best_case_ternary(arr)
            _, bc = binary_search(arr, bkey)
            _, tc = ternary_search(arr, tkey)
            print(f"Best case  -> Binary: key={bkey}, comparisons={bc} | "
                  f"Ternary: key={tkey}, comparisons={tc}")
        elif choice == "6":
            if not arr:
                print("Generate the array first (option 1).")
                continue
            wkey = worst_case_key(arr)
            _, bc = binary_search(arr, wkey)
            _, tc = ternary_search(arr, wkey)
            print(f"Worst case -> key={wkey} (absent) | "
                  f"Binary comparisons={bc} | Ternary comparisons={tc}")
        elif choice == "7":
            comparison_table()
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        # Non-interactive run: demonstrates every menu option automatically,
        # producing the same output the report's tables/graphs are built from.
        random.seed(1)
        arr = generate_sorted_array(20)
        print("1) Generated array (n=20):")
        print(arr)

        print("\n2) Display array:")
        print(arr)

        key_present = arr[7]
        print(f"\n3) Binary search for key={key_present} (present):")
        idx, c = binary_search(arr, key_present)
        print(f"   index={idx}, comparisons={c}")

        print(f"\n4) Ternary search for key={key_present} (present):")
        idx, c = ternary_search(arr, key_present)
        print(f"   index={idx}, comparisons={c}")

        print("\n5) Best case:")
        bkey, tkey = best_case_binary(arr), best_case_ternary(arr)
        _, bc = binary_search(arr, bkey)
        _, tc = ternary_search(arr, tkey)
        print(f"   Binary:  key={bkey}, comparisons={bc}")
        print(f"   Ternary: key={tkey}, comparisons={tc}")

        print("\n6) Worst case:")
        wkey = worst_case_key(arr)
        _, bc = binary_search(arr, wkey)
        _, tc = ternary_search(arr, wkey)
        print(f"   key={wkey} (absent)")
        print(f"   Binary comparisons={bc}, Ternary comparisons={tc}")

        print("\n7) Comparison table across increasing n:")
        comparison_table()
    else:
        menu()
