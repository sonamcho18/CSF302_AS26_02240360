"""
CSF302 Assignment 2: tests for closest.py
Name: Sonam Choki   Student number: 02240360

Run with:  python -m pytest test_closest.py -v
      or:  python test_closest.py
"""

import math
import random

from closest import closest_pair, closest_pair_brute, dist


def check_answer(points, result):
    """The answer must be valid: i < j, and d must be the real distance."""
    d, i, j = result
    assert 0 <= i < j < len(points)
    assert math.isclose(d, dist(points[i], points[j]))


# ---------- 1. Random tests against brute force ----------
def test_random_against_brute():
    random.seed(360)
    for _ in range(1000):                      # at least 500 required
        n = random.randint(2, 50)
        pts = [(random.randint(-100, 100), random.randint(-100, 100))
               for _ in range(n)]
        fast = closest_pair(pts)
        slow = closest_pair_brute(pts)
        check_answer(pts, fast)
        # Two pairs can tie, so compare the distance, not the indices.
        assert math.isclose(fast[0], slow[0]), (pts, fast, slow)


def test_random_floats_against_brute():
    random.seed(2240360)
    for _ in range(500):
        n = random.randint(2, 50)
        pts = [(random.uniform(0, 1000), random.uniform(0, 1000))
               for _ in range(n)]
        assert math.isclose(closest_pair(pts)[0], closest_pair_brute(pts)[0])


# ---------- 2. Special cases ----------
def test_example_from_assignment():
    pts = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    d, i, j = closest_pair(pts)
    assert (i, j) == (0, 5)
    assert math.isclose(d, math.sqrt(2))


def test_exactly_two_points():
    pts = [(0, 0), (3, 4)]
    assert closest_pair(pts) == (5.0, 0, 1)


def test_duplicate_points():
    pts = [(5, 5), (1, 9), (7, 2), (1, 9), (8, 8)]
    d, i, j = closest_pair(pts)
    assert d == 0
    assert (i, j) == (1, 3)


def test_many_duplicates():
    pts = [(4, 4)] * 10
    d, i, j = closest_pair(pts)
    assert d == 0 and i < j


def test_all_on_one_vertical_line():
    # Every point has the same x, so the split cannot use x alone.
    pts = [(7, y) for y in [0, 10, 25, 26, 40, 60, 90]]
    d, i, j = closest_pair(pts)
    assert d == 1
    assert (i, j) == (2, 3)


def test_closest_pair_crosses_dividing_line():
    # 8 points: the first 4 go to the left half, the last 4 to the right.
    # Inside each half the points are far apart, but (4.9, 50) is the
    # last point on the left and (5.1, 50) is the first on the right,
    # so the closest pair (0.2 apart) is only found in the strip.
    pts = [(0, 0), (1, 100), (2, 200), (4.9, 50),
           (5.1, 50), (8, 0), (9, 100), (10, 200)]
    d, i, j = closest_pair(pts)
    assert math.isclose(d, 0.2)
    assert (i, j) == (3, 4)


if __name__ == "__main__":
    tests = [f for name, f in list(globals().items()) if name.startswith("test_")]
    for t in tests:
        t()
        print("PASS", t.__name__)
    print(f"All {len(tests)} tests passed.")
