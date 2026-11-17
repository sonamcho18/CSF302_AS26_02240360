"""
CSF302 Assignment 2: timing experiment (Part C)
Name: Sonam Choki   Student number: 02240360

Times both functions for n = 1000, 2000, ..., 64000.
Brute force is stopped once a run takes more than 60 seconds.
Also finds the smallest n where divide and conquer beats brute force.
"""

import random
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from closest import closest_pair, closest_pair_brute


def random_points(n, seed):
    rng = random.Random(seed)
    return [(rng.uniform(0, 1_000_000), rng.uniform(0, 1_000_000))
            for _ in range(n)]


def time_it(func, pts, repeats=1):
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        func(pts)
        best = min(best, time.perf_counter() - start)
    return best


# ---------- timing table ----------
sizes = [1000 * 2 ** k for k in range(7)]      # 1000 ... 64000
rows = []
brute_stopped = False
for n in sizes:
    pts = random_points(n, seed=n)
    t_dc = time_it(closest_pair, pts, repeats=3)
    if brute_stopped:
        t_bf = None
    else:
        t_bf = time_it(closest_pair_brute, pts)
        if t_bf > 60:
            brute_stopped = True               # skip larger n
    rows.append((n, t_bf, t_dc))
    bf_txt = f"{t_bf:10.3f}" if t_bf is not None else "   skipped"
    print(f"n={n:6d}  brute={bf_txt} s   d&c={t_dc:8.4f} s", flush=True)

# ---------- crossover point ----------
crossover = None
for n in range(2, 301):
    pts_list = [random_points(n, seed=s) for s in range(30)]
    t_bf = sum(time_it(closest_pair_brute, p, 5) for p in pts_list)
    t_dc = sum(time_it(closest_pair, p, 5) for p in pts_list)
    if t_dc < t_bf:
        # make sure it stays faster for the next few n too
        ok = True
        for m in range(n + 1, n + 6):
            ps = [random_points(m, seed=s) for s in range(30)]
            if (sum(time_it(closest_pair, p, 5) for p in ps) >=
                    sum(time_it(closest_pair_brute, p, 5) for p in ps)):
                ok = False
                break
        if ok:
            crossover = n
            break
print("Crossover n =", crossover)

# ---------- log-log graph ----------
plt.figure(figsize=(7, 4.5))
bf = [(n, t) for n, t, _ in rows if t is not None]
plt.loglog([n for n, _ in bf], [t for _, t in bf], "o-",
           color="#c0392b", label="Brute force  Θ(n²)")
plt.loglog([n for n, _, _ in rows], [t for _, _, t in rows], "s-",
           color="#2471a3", label="Divide & conquer  O(n log n)")
plt.xlabel("Number of points n (log scale)")
plt.ylabel("Time in seconds (log scale)")
plt.title("Closest pair: running time vs n")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("timing_graph.png", dpi=150)
print("Saved timing_graph.png")
