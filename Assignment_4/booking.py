"""
CSF302 - Assignment 4: Booking the Hall
Name:       Sonam Choki
Student No: 02240360

Weighted interval scheduling for a community hall in Paro.

Each request is a tuple (start, finish, fee). Two requests fit together if
one finishes no later than the other starts (an event ending at 12 and one
starting at 12 both fit). Every function returns (total_fee, chosen) where
`chosen` is a sorted list of indices into the ORIGINAL request list.

Run this file directly to print the worked example, the Part C
counterexamples and the Part C revenue-ratio table:

    python3 booking.py
"""

from bisect import bisect_right
from itertools import combinations
import random


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def _fits(a, b):
    """True if requests a and b do not overlap (touching ends are allowed)."""
    return a[1] <= b[0] or b[1] <= a[0]


def _greedy(requests, order):
    """Accept requests in the given index order whenever they fit with
    everything accepted so far. Shared by both greedy rules."""
    accepted = []
    for i in order:
        if all(_fits(requests[i], requests[j]) for j in accepted):
            accepted.append(i)
    accepted.sort()
    return sum(requests[i][2] for i in accepted), accepted


# ---------------------------------------------------------------------------
# Part A.1 - Greedy: earliest finish time first
# ---------------------------------------------------------------------------
def greedy_earliest_finish(requests):
    """Sort by finish time; accept each request that starts no earlier than
    the finish of the last accepted request.  O(n log n)."""
    order = sorted(range(len(requests)), key=lambda i: requests[i][1])
    accepted = []
    last_finish = float("-inf")
    for i in order:
        start, finish, _ = requests[i]
        if start >= last_finish:
            accepted.append(i)
            last_finish = finish
    accepted.sort()
    return sum(requests[i][2] for i in accepted), accepted


# ---------------------------------------------------------------------------
# Part A.2 - Greedy: highest fee first
# ---------------------------------------------------------------------------
def greedy_highest_fee(requests):
    """Sort by fee (highest first); accept each request that fits with all
    requests accepted so far.  O(n^2) because of the overlap check."""
    order = sorted(range(len(requests)), key=lambda i: -requests[i][2])
    return _greedy(requests, order)


# ---------------------------------------------------------------------------
# Part A.3 - Dynamic programming (weighted interval scheduling)
# ---------------------------------------------------------------------------
def best_schedule(requests):
    """Optimal schedule by dynamic programming.

    Sort by finish time (1-based positions 1..n).  p(j) = the last request
    (in sorted order) that finishes no later than request j starts.
        OPT(0) = 0
        OPT(j) = max(OPT(j-1), fee_j + OPT(p(j)))
    p(j) is found with binary search, so the whole thing is O(n log n).
    """
    n = len(requests)
    if n == 0:
        return 0, []

    order = sorted(range(n), key=lambda i: requests[i][1])
    finishes = [requests[i][1] for i in order]

    # p[j] for j = 1..n (p[0] unused). bisect_right counts finishes <= start,
    # which is exactly the 1-based position of the last compatible request.
    p = [0] * (n + 1)
    for j in range(1, n + 1):
        start = requests[order[j - 1]][0]
        p[j] = bisect_right(finishes, start, 0, j - 1)

    opt = [0] * (n + 1)
    for j in range(1, n + 1):
        fee = requests[order[j - 1]][2]
        opt[j] = max(opt[j - 1], fee + opt[p[j]])

    # Reconstruct: walk back from n, taking j whenever it was the better choice.
    chosen = []
    j = n
    while j > 0:
        fee = requests[order[j - 1]][2]
        if fee + opt[p[j]] >= opt[j - 1]:
            chosen.append(order[j - 1])
            j = p[j]
        else:
            j -= 1
    chosen.sort()
    return opt[n], chosen


# ---------------------------------------------------------------------------
# Part A.4 - Brute force (for checking only)
# ---------------------------------------------------------------------------
def brute_force(requests):
    """Try every subset and keep the best compatible one.  O(2^n * n^2);
    only use for n <= 15."""
    n = len(requests)
    best_total, best_set = 0, []
    for size in range(1, n + 1):
        for subset in combinations(range(n), size):
            ok = all(_fits(requests[a], requests[b])
                     for a, b in combinations(subset, 2))
            if ok:
                total = sum(requests[i][2] for i in subset)
                if total > best_total:
                    best_total, best_set = total, list(subset)
    return best_total, best_set


# ---------------------------------------------------------------------------
# Utilities shared with the tests / Part C experiment
# ---------------------------------------------------------------------------
def is_valid_schedule(requests, chosen):
    """True if no two chosen requests overlap."""
    return all(_fits(requests[a], requests[b]) for a, b in combinations(chosen, 2))


def random_requests(n, rng, max_time=100, max_len=20, max_fee=10000):
    """Generate n random requests (start, finish, fee) with integer times."""
    reqs = []
    for _ in range(n):
        start = rng.randint(0, max_time - 1)
        finish = start + rng.randint(1, max_len)
        fee = rng.randint(1, max_fee)
        reqs.append((start, finish, fee))
    return reqs


def ratio_experiment(trials=1000, n=50, seed=302):
    """Part C.3: average and worst ratio of greedy revenue to optimal."""
    rng = random.Random(seed)
    results = {"greedy_earliest_finish": [], "greedy_highest_fee": []}
    for _ in range(trials):
        reqs = random_requests(n, rng)
        opt, _ = best_schedule(reqs)
        results["greedy_earliest_finish"].append(greedy_earliest_finish(reqs)[0] / opt)
        results["greedy_highest_fee"].append(greedy_highest_fee(reqs)[0] / opt)
    summary = {}
    for name, ratios in results.items():
        summary[name] = {
            "average": sum(ratios) / len(ratios),
            "worst": min(ratios),
            "optimal_runs": sum(1 for r in ratios if r == 1.0),
        }
    return summary


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    example = [(9, 12, 3000), (10, 16, 8000), (13, 17, 4000),
               (12, 14, 2500), (17, 20, 2000)]
    print("Worked example:", example)
    print("  greedy_earliest_finish ->", greedy_earliest_finish(example))
    print("  greedy_highest_fee     ->", greedy_highest_fee(example))
    print("  best_schedule          ->", best_schedule(example))
    print("  brute_force            ->", brute_force(example))

    print("\nPart C.1 counterexamples")
    cx_finish = [(0, 2, 1), (1, 5, 10)]
    cx_fee = [(0, 10, 10), (0, 5, 6), (5, 10, 6)]
    for name, reqs, fn in [("earliest finish", cx_finish, greedy_earliest_finish),
                           ("highest fee", cx_fee, greedy_highest_fee)]:
        print(f"  {name}: {reqs}")
        print(f"    greedy  -> {fn(reqs)}")
        print(f"    optimal -> {best_schedule(reqs)}")

    print("\nPart C.3 ratio table (1,000 random inputs of 50 requests, seed 302)")
    summary = ratio_experiment()
    print(f"  {'Rule':<24}{'Average':>10}{'Worst':>10}{'Optimal runs':>15}")
    for name, s in summary.items():
        print(f"  {name:<24}{s['average']:>10.4f}{s['worst']:>10.4f}"
              f"{s['optimal_runs']:>11}/1000")
