"""
CSF302 Assignment 2: Closest Camera Traps
Name: Sonam Choki
Student number: 02240360

Finds the two camera traps (points) that are closest to each other.
Two versions:
  closest_pair_brute(points) - checks every pair, Theta(n^2)
  closest_pair(points)       - divide and conquer, O(n log n)

Both return (d, i, j): the smallest distance d and the indices i < j
of the two points in the original list.
"""

import math


def dist(p, q):
    """Straight-line (Euclidean) distance between two points."""
    return math.hypot(p[0] - q[0], p[1] - q[1])


# ---------------------------------------------------------------
# 1. Brute force: compare every pair
# ---------------------------------------------------------------
def closest_pair_brute(points):
    n = len(points)
    best_d, best_i, best_j = math.inf, -1, -1
    for i in range(n):
        for j in range(i + 1, n):
            d = dist(points[i], points[j])
            if d < best_d:
                best_d, best_i, best_j = d, i, j
    return (best_d, best_i, best_j)


# ---------------------------------------------------------------
# 2. Divide and conquer
# ---------------------------------------------------------------
def closest_pair(points):
    # We work with indices so we can report the original positions,
    # and so duplicate points are never confused with each other.
    idx = list(range(len(points)))
    by_x = sorted(idx, key=lambda k: (points[k][0], points[k][1]))
    by_y = sorted(idx, key=lambda k: (points[k][1], points[k][0]))

    d, i, j = _solve(points, by_x, by_y)
    return (d, min(i, j), max(i, j))   # make sure i < j


def _solve(points, by_x, by_y):
    """by_x and by_y hold the SAME indices, sorted by x and by y."""
    n = len(by_x)

    # Base case: 3 or fewer points -> just check every pair.
    if n <= 3:
        best = (math.inf, -1, -1)
        for a in range(n):
            for b in range(a + 1, n):
                i, j = by_x[a], by_x[b]
                d = dist(points[i], points[j])
                if d < best[0]:
                    best = (d, i, j)
        return best

    # DIVIDE: split at the middle of the x-sorted list.
    mid = n // 2
    mid_x = points[by_x[mid]][0]          # x of the dividing line
    left_x, right_x = by_x[:mid], by_x[mid:]

    # Keep the y-order for each half (one pass, O(n)).
    in_left = set(left_x)
    left_y = [k for k in by_y if k in in_left]
    right_y = [k for k in by_y if k not in in_left]

    # CONQUER: solve each half.
    best_left = _solve(points, left_x, left_y)
    best_right = _solve(points, right_x, right_y)
    best = min(best_left, best_right)
    delta = best[0]

    # COMBINE: check the strip of width 2*delta around the line.
    strip = [k for k in by_y if abs(points[k][0] - mid_x) < delta]
    for a in range(len(strip)):
        for b in range(a + 1, len(strip)):
            # Points are in y-order: once the y-gap is >= delta,
            # no later point can be closer. (At most ~7 checks.)
            if points[strip[b]][1] - points[strip[a]][1] >= delta:
                break
            d = dist(points[strip[a]], points[strip[b]])
            if d < delta:
                delta = d
                best = (d, strip[a], strip[b])
    return best


if __name__ == "__main__":
    pts = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    print("Brute force:      ", closest_pair_brute(pts))
    print("Divide & conquer: ", closest_pair(pts))
