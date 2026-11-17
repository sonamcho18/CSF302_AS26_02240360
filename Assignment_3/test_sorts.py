"""
CSF302 - Assignment 3: Part B tests
Name:       Sonam Choki
Student No: 02240360

Run with:   python3 -m unittest -v test_sorts.py
   (or)     python3 test_sorts.py

Both sorts are checked against Python's sorted() (the brute-force check)
on 500+ random lists and on the required edge cases.
"""

import random
import unittest

from sorts import quicksort_basic, quicksort_improved


def run(sort_fn, data):
    """Sort a copy of data with sort_fn; return the result (sort is in place)."""
    a = list(data)
    result = sort_fn(a)
    assert result is None, "sort should work in place and return None"
    return a


SORTS = {
    "quicksort_basic": quicksort_basic,
    "quicksort_improved": quicksort_improved,
    "quicksort_improved(cutoff=1)": lambda a: quicksort_improved(a, cutoff=1),
    "quicksort_improved(cutoff=4)": lambda a: quicksort_improved(a, cutoff=4),
    "quicksort_improved(cutoff=64)": lambda a: quicksort_improved(a, cutoff=64),
}


class TestRandomLists(unittest.TestCase):
    """B.1 - compare against sorted() on at least 500 random lists."""

    NUM_LISTS = 600

    def test_random_lists(self):
        rng = random.Random(42)
        for name, fn in SORTS.items():
            for trial in range(self.NUM_LISTS):
                n = rng.randint(0, 200)
                lo = rng.choice([-1000, -10, 0])
                hi = rng.choice([10, 1000])
                data = [rng.randint(lo, hi) for _ in range(n)]
                with self.subTest(sort=name, trial=trial, n=n):
                    self.assertEqual(run(fn, data), sorted(data))

    def test_larger_random_lists(self):
        rng = random.Random(7)
        for name, fn in SORTS.items():
            for trial in range(20):
                data = [rng.randint(-10**6, 10**6) for _ in range(2000)]
                with self.subTest(sort=name, trial=trial):
                    self.assertEqual(run(fn, data), sorted(data))


class TestEdgeCases(unittest.TestCase):
    """B.2 - empty, one element, all equal, sorted, reverse sorted, negatives."""

    CASES = {
        "empty": [],
        "one element": [5],
        "two elements": [2, 1],
        "all equal": [7] * 50,
        "already sorted": list(range(100)),
        "reverse sorted": list(range(100, 0, -1)),
        "negative numbers": [-3, -1, -7, 0, -2, 5, -100, 4],
        "all negative": [-5, -50, -1, -20, -3],
        "many duplicates": [random.Random(1).randint(0, 9) for _ in range(300)],
        "Nu 100 and Nu 500 top-ups": [500, 100, 100, 500, 100, 500, 500, 100],
    }

    def test_edge_cases(self):
        for name, fn in SORTS.items():
            for case, data in self.CASES.items():
                with self.subTest(sort=name, case=case):
                    self.assertEqual(run(fn, data), sorted(data))

    def test_sorts_in_place(self):
        for name, fn in SORTS.items():
            a = [3, 1, 2]
            same_list = a
            fn(a)
            with self.subTest(sort=name):
                self.assertIs(a, same_list)
                self.assertEqual(a, [1, 2, 3])


class TestImprovedOnBadInputs(unittest.TestCase):
    """The improved sort must handle the inputs that break the basic one."""

    N = 50_000

    def test_large_sorted_input(self):
        data = list(range(self.N))
        self.assertEqual(run(quicksort_improved, data), data)

    def test_large_reverse_sorted_input(self):
        data = list(range(self.N, 0, -1))
        self.assertEqual(run(quicksort_improved, data), sorted(data))

    def test_large_many_duplicates(self):
        rng = random.Random(3)
        data = [rng.randint(0, 9) for _ in range(self.N)]
        self.assertEqual(run(quicksort_improved, data), sorted(data))

    def test_large_all_equal(self):
        data = [100] * self.N
        self.assertEqual(run(quicksort_improved, data), data)

    def test_basic_crashes_on_large_sorted_input(self):
        # Documents the bug we are fixing: Theta(n) recursion depth.
        with self.assertRaises(RecursionError):
            quicksort_basic(list(range(5000)))

    def test_invalid_cutoff(self):
        with self.assertRaises(ValueError):
            quicksort_improved([3, 2, 1], cutoff=0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
