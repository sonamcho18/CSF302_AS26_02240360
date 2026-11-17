"""
CSF302 - Assignment 4: Booking the Hall  (Part B tests)
Name:       Sonam Choki
Student No: 02240360

Run with either:
    python3 -m unittest -v test_booking.py
    python3 -m pytest -v test_booking.py      (if pytest is installed)
"""

import random
import unittest

from booking import (
    greedy_earliest_finish,
    greedy_highest_fee,
    best_schedule,
    brute_force,
    is_valid_schedule,
    random_requests,
)

ALL_FUNCS = [greedy_earliest_finish, greedy_highest_fee, best_schedule, brute_force]


class TestWorkedExample(unittest.TestCase):
    def test_assignment_example(self):
        reqs = [(9, 12, 3000), (10, 16, 8000), (13, 17, 4000),
                (12, 14, 2500), (17, 20, 2000)]
        self.assertEqual(greedy_earliest_finish(reqs), (7500, [0, 3, 4]))
        self.assertEqual(best_schedule(reqs), (10000, [1, 4]))
        self.assertEqual(brute_force(reqs)[0], 10000)


class TestRandomAgainstBruteForce(unittest.TestCase):
    """Part B.1: best_schedule vs brute_force on 500+ random inputs (0-10)."""

    def test_dp_matches_brute_force(self):
        rng = random.Random(2024)
        for trial in range(600):
            n = rng.randint(0, 10)
            reqs = random_requests(n, rng, max_time=30, max_len=10, max_fee=50)
            dp_total, dp_chosen = best_schedule(reqs)
            bf_total, _ = brute_force(reqs)
            with self.subTest(trial=trial, requests=reqs):
                self.assertEqual(dp_total, bf_total)
                # The chosen list must be a real, valid schedule worth dp_total.
                self.assertTrue(is_valid_schedule(reqs, dp_chosen))
                self.assertEqual(sum(reqs[i][2] for i in dp_chosen), dp_total)

    def test_greedy_never_beats_optimal_and_is_valid(self):
        rng = random.Random(7)
        for _ in range(500):
            reqs = random_requests(rng.randint(0, 10), rng, max_time=30, max_len=10)
            opt = brute_force(reqs)[0]
            for fn in (greedy_earliest_finish, greedy_highest_fee):
                total, chosen = fn(reqs)
                self.assertLessEqual(total, opt)
                self.assertTrue(is_valid_schedule(reqs, chosen))
                self.assertEqual(sum(reqs[i][2] for i in chosen), total)


class TestEdgeCases(unittest.TestCase):
    """Part B.2: the required special cases, checked on every function."""

    def test_no_requests(self):
        for fn in ALL_FUNCS:
            self.assertEqual(fn([]), (0, []), fn.__name__)

    def test_one_request(self):
        for fn in ALL_FUNCS:
            self.assertEqual(fn([(8, 10, 500)]), (500, [0]), fn.__name__)

    def test_all_overlapping(self):
        # Every request contains the time 10-11, so only one can be chosen.
        reqs = [(9, 12, 300), (10, 11, 900), (8, 15, 400), (10, 13, 200)]
        self.assertEqual(best_schedule(reqs), (900, [1]))
        self.assertEqual(brute_force(reqs), (900, [1]))
        self.assertEqual(greedy_highest_fee(reqs), (900, [1]))
        total, chosen = greedy_earliest_finish(reqs)
        self.assertEqual(len(chosen), 1)

    def test_none_overlapping(self):
        reqs = [(1, 2, 10), (5, 7, 20), (3, 4, 30), (8, 9, 40)]
        for fn in ALL_FUNCS:
            self.assertEqual(fn(reqs), (100, [0, 1, 2, 3]), fn.__name__)

    def test_back_to_back(self):
        # One event ends exactly when the next begins: they all fit.
        reqs = [(12, 14, 50), (9, 12, 60), (14, 18, 70)]
        for fn in ALL_FUNCS:
            self.assertEqual(fn(reqs), (180, [0, 1, 2]), fn.__name__)


class TestEqualFees(unittest.TestCase):
    """Part B.3: with equal fees, earliest-finish greedy is always optimal."""

    def test_earliest_finish_optimal_when_fees_equal(self):
        rng = random.Random(99)
        for _ in range(500):
            n = rng.randint(0, 12)
            reqs = [(s, s + rng.randint(1, 10), 1000)
                    for s in (rng.randint(0, 30) for _ in range(n))]
            self.assertEqual(greedy_earliest_finish(reqs)[0], best_schedule(reqs)[0])
            self.assertEqual(greedy_earliest_finish(reqs)[0], brute_force(reqs)[0])


class TestCounterexamples(unittest.TestCase):
    """Part C.1: each greedy rule is beaten on a small input."""

    def test_earliest_finish_counterexample(self):
        reqs = [(0, 2, 1), (1, 5, 10)]
        self.assertEqual(greedy_earliest_finish(reqs), (1, [0]))
        self.assertEqual(best_schedule(reqs), (10, [1]))

    def test_highest_fee_counterexample(self):
        reqs = [(0, 10, 10), (0, 5, 6), (5, 10, 6)]
        self.assertEqual(greedy_highest_fee(reqs), (10, [0]))
        self.assertEqual(best_schedule(reqs), (12, [1, 2]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
