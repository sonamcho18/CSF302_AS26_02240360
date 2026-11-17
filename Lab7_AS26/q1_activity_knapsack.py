"""
CSF302 - Lab 7, Q1: Activity Selection and Knapsack
Name: Sonam Choki
Student Number: 02240360

Usage:
    python3 q1_activity_knapsack.py                  # reads activities.txt
    python3 q1_activity_knapsack.py my_file.txt      # your own (start finish) pairs
"""

import os
import random
import sys


# ---------------------------------------------------------------
# Read (start, finish) pairs from a file
# ---------------------------------------------------------------
def read_activities(path):
    acts = []
    with open(path) as f:
        for line in f:
            line = line.split("#")[0].strip()
            if line:
                s, t = map(int, line.replace(",", " ").split())
                acts.append((s, t))
    return acts


# ---------------------------------------------------------------
# 1-2. Greedy activity selection with three different rules
# ---------------------------------------------------------------
def greedy_select(acts, key):
    """Sort by `key`, then take each activity that doesn't overlap
    anything already chosen."""
    chosen = []
    for s, f in sorted(acts, key=key):
        if all(f <= cs or s >= cf for cs, cf in chosen):   # no overlap
            chosen.append((s, f))
    return sorted(chosen, key=lambda a: a[1])


def earliest_finish(acts):
    return greedy_select(acts, key=lambda a: a[1])


def earliest_start(acts):
    return greedy_select(acts, key=lambda a: a[0])


def shortest_duration(acts):
    return greedy_select(acts, key=lambda a: a[1] - a[0])


def part_1(path):
    print("=" * 66)
    print("TASK 1: Greedy activity selection (earliest finish time)")
    print("=" * 66)
    acts = read_activities(path)
    print(f"Read {len(acts)} activities from {os.path.basename(path)}:")
    for i, (s, f) in enumerate(acts, 1):
        print(f"  a{i:<2} start = {s:>2}  finish = {f:>2}  " + " " * s + "#" * (f - s))
    chosen = earliest_finish(acts)
    print(f"\nSelected {len(chosen)} activities: {chosen}")
    print()


def find_counterexample(rule, rng, tries=100_000):
    for _ in range(tries):
        n = rng.randint(2, 5)
        acts = []
        for _ in range(n):
            s = rng.randint(0, 10)
            acts.append((s, s + rng.randint(1, 8)))
        if len(rule(acts)) < len(earliest_finish(acts)):
            return acts
    return None


def part_2():
    print("=" * 66)
    print("TASK 2: Other greedy rules can give a SMALLER answer")
    print("=" * 66)
    rng = random.Random(302)
    for name, rule in [("Earliest start", earliest_start),
                       ("Shortest duration", shortest_duration)]:
        acts = find_counterexample(rule, rng)
        print(f"{name}: counterexample found by random testing")
        print(f"  Input            : {sorted(acts)}")
        print(f"  {name:<17}: {rule(acts)}  -> {len(rule(acts))} activities")
        print(f"  Earliest finish  : {earliest_finish(acts)}  -> "
              f"{len(earliest_finish(acts))} activities")
        print()
    print("Why: earliest START may pick one long activity that blocks many")
    print("short ones. SHORTEST duration may pick a short activity that overlaps")
    print("two others which could both have been chosen. Earliest FINISH always")
    print("leaves the most time free for the rest, so it is always optimal.")
    print()


# ---------------------------------------------------------------
# 3. Fractional knapsack: highest value/weight ratio first
# ---------------------------------------------------------------
def fractional_knapsack(items, capacity):
    """items = list of (value, weight). We may take part of an item."""
    total = 0.0
    taken = []
    for v, w in sorted(items, key=lambda it: it[0] / it[1], reverse=True):
        if capacity <= 0:
            break
        amount = min(w, capacity)
        total += v * amount / w
        taken.append((v, w, amount / w))
        capacity -= amount
    return total, taken


def part_3():
    print("=" * 66)
    print("TASK 3: Fractional knapsack (best value/weight first)")
    print("=" * 66)
    items = [(60, 10), (100, 20), (120, 30)]
    cap = 50
    print(f"Items (value, weight): {items}, capacity = {cap}")
    for v, w in items:
        print(f"  value {v:>3}, weight {w:>2} -> ratio {v / w:.1f}")
    total, taken = fractional_knapsack(items, cap)
    print("Taken:")
    for v, w, frac in taken:
        print(f"  {frac * 100:>5.1f}% of item (value {v}, weight {w}) -> {v * frac:.1f}")
    print(f"Maximum value = {total:.1f}")
    print()


# ---------------------------------------------------------------
# 4. 0/1 knapsack: greedy by ratio vs DP (optimal)
# ---------------------------------------------------------------
def greedy_01(items, capacity):
    total = 0
    for v, w in sorted(items, key=lambda it: it[0] / it[1], reverse=True):
        if w <= capacity:          # whole item or nothing
            total += v
            capacity -= w
    return total


def dp_01(items, capacity):
    best = [0] * (capacity + 1)
    for v, w in items:
        for c in range(capacity, w - 1, -1):
            best[c] = max(best[c], best[c - w] + v)
    return best[capacity]


def part_4():
    print("=" * 66)
    print("TASK 4: 0/1 knapsack - greedy (ratio) vs DP (optimal)")
    print("=" * 66)
    items = [(60, 10), (100, 20), (120, 30)]
    print(f"Same items, capacity 50: greedy = {greedy_01(items, 50)}, "
          f"DP = {dp_01(items, 50)}")
    print("  (greedy takes 60 + 100, then 120 doesn't fit; best is 100 + 120)\n")

    rng = random.Random(302)
    trials = 5000
    worst_ratio, worst_case = 1.0, None
    not_optimal = 0
    for _ in range(trials):
        n = rng.randint(2, 8)
        items = [(rng.randint(1, 100), rng.randint(1, 30)) for _ in range(n)]
        cap = rng.randint(10, 60)
        g, d = greedy_01(items, cap), dp_01(items, cap)
        if d == 0:
            continue
        if g < d:
            not_optimal += 1
        if g / d < worst_ratio:
            worst_ratio, worst_case = g / d, (items, cap, g, d)
    print(f"Random tests            : {trials}")
    print(f"Greedy was NOT optimal  : {not_optimal} times "
          f"({not_optimal / trials * 100:.1f}%)")
    print(f"Worst greedy/optimal    : {worst_ratio:.3f}")
    items, cap, g, d = worst_case
    print(f"  Worst case: items = {items}, capacity = {cap}")
    print(f"  greedy = {g}, optimal = {d}")
    print("Greedy works for FRACTIONAL knapsack but not for 0/1 knapsack,")
    print("because in 0/1 we cannot fill the leftover space with part of an item.")
    print()


if __name__ == "__main__":
    print("CSF302 Lab 7 - Q1 Activity Selection & Knapsack | Sonam Choki | 02240360\n")
    here = os.path.dirname(os.path.abspath(__file__))
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "activities.txt")
    part_1(path)
    part_2()
    part_3()
    part_4()
