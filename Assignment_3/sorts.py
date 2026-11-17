"""
CSF302 - Assignment 3: Fixing a Slow Quicksort
Name:       Sonam Choki
Student No: 02240360

Part A: two in-place quicksorts for lists of integers.

    quicksort_basic(a)              - Lomuto partition, last element as pivot
    quicksort_improved(a, cutoff)   - random pivot + insertion sort for small
                                      parts + recurse on the smaller part and
                                      loop on the larger part (O(log n) depth)

Neither function uses sorted() or list.sort(); those are used only in the
tests and in the benchmark to check answers.

Running this file directly (python3 sorts.py) runs the Part C timing
experiments and prints the tables. If matplotlib is installed it also saves
the graphs as PNG files.
"""

import random
import sys
import time


# ---------------------------------------------------------------------------
# Part A.1 - Basic quicksort (textbook version)
# ---------------------------------------------------------------------------

def _lomuto_partition(a, lo, hi):
    """Partition a[lo..hi] around the pivot a[hi] (Lomuto scheme).

    After the call, every element left of the returned index is <= pivot and
    every element right of it is > pivot. Returns the pivot's final index.
    """
    pivot = a[hi]
    i = lo - 1                      # end of the "<= pivot" region
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1


def _quicksort_basic(a, lo, hi):
    if lo < hi:
        p = _lomuto_partition(a, lo, hi)
        _quicksort_basic(a, lo, p - 1)
        _quicksort_basic(a, p + 1, hi)


def quicksort_basic(a):
    """Sort list a in place using textbook quicksort (last element as pivot).

    Worst case Theta(n^2) time and Theta(n) recursion depth - this happens on
    already-sorted input and on input with many equal values.
    """
    _quicksort_basic(a, 0, len(a) - 1)


# ---------------------------------------------------------------------------
# Part A.2 - Improved quicksort
# ---------------------------------------------------------------------------

def _insertion_sort(a, lo, hi):
    """Sort a[lo..hi] in place with insertion sort."""
    for i in range(lo + 1, hi + 1):
        key = a[i]
        j = i - 1
        while j >= lo and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key


def _three_way_partition(a, lo, hi, rng):
    """Partition a[lo..hi] around a randomly chosen pivot value.

    Uses Dijkstra's three-way ("Dutch national flag") partition so that the
    range ends up as   [ < pivot | == pivot | > pivot ].
    Returns (lt, gt): a[lt..gt] all equal the pivot and are already in their
    final positions, so they are never touched again. This is what stops the
    many-duplicates input (lots of Nu 100 / Nu 500 amounts) from going
    quadratic.
    """
    pivot = a[rng.randint(lo, hi)]  # random pivot value
    lt, i, gt = lo, lo, hi
    while i <= gt:
        x = a[i]
        if x < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif x > pivot:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:
            i += 1
    return lt, gt


def quicksort_improved(a, cutoff=16, rng=None):
    """Sort list a in place using an improved quicksort.

    Improvements over quicksort_basic:
      1. Random pivot - sorted / reverse-sorted input is no longer a bad case;
         expected time is O(n log n) for every input order.
      2. Insertion sort for parts of size <= cutoff - less overhead on the
         many tiny sub-lists near the bottom of the recursion.
      3. Recurse on the smaller part, loop on the larger part - the smaller
         part is at most half the size, so recursion depth is O(log n) and a
         RecursionError cannot happen.
      4. Three-way partition - all elements equal to the pivot are fixed in
         one pass, so many repeated values are handled in linear time.

    rng may be a random.Random instance (useful for repeatable tests).
    """
    if cutoff < 1:
        raise ValueError("cutoff must be at least 1")
    if rng is None:
        rng = random
    _quicksort_improved(a, 0, len(a) - 1, cutoff, rng)


def _quicksort_improved(a, lo, hi, cutoff, rng):
    while hi - lo + 1 > cutoff:
        lt, gt = _three_way_partition(a, lo, hi, rng)
        # left part is a[lo..lt-1], right part is a[gt+1..hi]
        if (lt - lo) < (hi - gt):
            _quicksort_improved(a, lo, lt - 1, cutoff, rng)  # smaller: recurse
            lo = gt + 1                                     # larger: loop
        else:
            _quicksort_improved(a, gt + 1, hi, cutoff, rng)  # smaller: recurse
            hi = lt - 1                                      # larger: loop
    _insertion_sort(a, lo, hi)


# ---------------------------------------------------------------------------
# Part C - Timing experiments (run: python3 sorts.py)
# ---------------------------------------------------------------------------

SIZES = [1000, 2000, 4000, 8000, 16000, 32000, 64000]
CUTOFFS = [1, 4, 8, 16, 32, 64]
TIME_LIMIT = 60.0   # seconds; a run slower than this is not repeated at larger n


def make_input(kind, n, rng):
    if kind == "random":
        return [rng.randint(-1_000_000, 1_000_000) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "duplicates":
        return [rng.randint(0, 9) for _ in range(n)]
    raise ValueError(kind)


def time_sort(sort_fn, data, repeats=3):
    """Return (best_seconds, None) or (None, error_name) if the sort crashed."""
    best = None
    for _ in range(repeats):
        a = list(data)
        t0 = time.perf_counter()
        try:
            sort_fn(a)
        except RecursionError:
            return None, "RecursionError"
        elapsed = time.perf_counter() - t0
        assert a == sorted(data), "sort gave a wrong answer"
        best = elapsed if best is None else min(best, elapsed)
        if elapsed > 5:          # slow case: one run is enough
            break
    return best, None


def fmt(t, err):
    if err:
        return "CRASH (" + err + ")"
    if t is None:
        return "skipped (too slow)"
    return f"{t * 1000:.1f} ms"


def experiment_sizes(rng):
    print("\nC.1  Time vs n (best of 3 runs)")
    print(f"     Python recursion limit = {sys.getrecursionlimit()}")
    sorts = [("quicksort_basic", quicksort_basic),
             ("quicksort_improved", lambda a: quicksort_improved(a, 16))]
    results = {}
    for kind in ["random", "sorted", "duplicates"]:
        print(f"\n  Input: {kind}")
        print(f"  {'n':>7} | {'quicksort_basic':>22} | {'quicksort_improved':>22}")
        print("  " + "-" * 58)
        too_slow = {name: False for name, _ in sorts}
        for n in SIZES:
            data = make_input(kind, n, rng)
            row = []
            for name, fn in sorts:
                if too_slow[name]:
                    t, err = None, None
                else:
                    t, err = time_sort(fn, data)
                    if t is not None and t > TIME_LIMIT:
                        too_slow[name] = True
                results[(kind, name, n)] = (t, err)
                row.append(fmt(t, err))
            print(f"  {n:>7} | {row[0]:>22} | {row[1]:>22}")
    return results


def experiment_quadratic():
    """C.2 support: quicksort_basic on sorted input small enough not to crash.

    Doubling n should roughly quadruple the time if T(n) = T(n-1) + Theta(n).
    """
    print("\nC.2  quicksort_basic on SORTED input below the recursion limit")
    print(f"  {'n':>5} | {'time':>10} | ratio to previous n")
    prev = None
    out = {}
    for n in [100, 200, 400, 800]:
        t, _ = time_sort(quicksort_basic, list(range(n)), repeats=7)
        out[n] = t
        ratio = f"{t / prev:.2f}x" if prev else "-"
        print(f"  {n:>5} | {t * 1000:7.2f} ms | {ratio}")
        prev = t
    return out


def experiment_cutoff(rng):
    print("\nC.3  quicksort_improved on n = 100,000 random values (best of 5)")
    data = make_input("random", 100_000, rng)
    out = {}
    for c in CUTOFFS:
        t, _ = time_sort(lambda a: quicksort_improved(a, c), data, repeats=5)
        out[c] = t
        print(f"  cutoff = {c:>3}: {t * 1000:8.1f} ms")
    best = min(out, key=out.get)
    print(f"  Best cutoff: {best}")
    return out, best, data


def experiment_builtin(data, best_cutoff):
    print("\nC.4  Best version vs Python's sorted(), n = 100,000 random (best of 5)")
    t_mine, _ = time_sort(lambda a: quicksort_improved(a, best_cutoff), data, 5)
    best_builtin = None
    for _ in range(5):
        t0 = time.perf_counter()
        sorted(data)
        e = time.perf_counter() - t0
        best_builtin = e if best_builtin is None else min(best_builtin, e)
    print(f"  quicksort_improved (cutoff={best_cutoff}): {t_mine * 1000:8.1f} ms")
    print(f"  sorted():                         {best_builtin * 1000:8.1f} ms")
    print(f"  sorted() is {t_mine / best_builtin:.0f}x faster")
    return t_mine, best_builtin


def make_graphs(results, cutoff_times):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n(matplotlib not installed - skipping graphs. "
              "Install with: pip3 install matplotlib)")
        return

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    for ax, kind in zip(axes, ["random", "sorted", "duplicates"]):
        for name, colour in [("quicksort_basic", "tab:red"),
                             ("quicksort_improved", "tab:blue")]:
            xs, ys, crash = [], [], []
            for n in SIZES:
                t, err = results[(kind, name, n)]
                if t is not None:
                    xs.append(n)
                    ys.append(t * 1000)
                elif err:
                    crash.append(n)
            if xs:
                ax.plot(xs, ys, "o-", color=colour, label=name)
            if crash:
                ax.plot([], [], "x", color=colour,
                        label=f"{name}: crashed for n >= {crash[0]}")
        ax.set_title(f"Input: {kind}")
        ax.set_xlabel("n (list size)")
        ax.set_ylabel("time (ms)")
        ax.set_xscale("log", base=2)
        ax.set_yscale("log")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig("graph_time_vs_n.png", dpi=150)

    fig, ax = plt.subplots(figsize=(6, 4))
    cs = list(cutoff_times)
    ax.plot(cs, [cutoff_times[c] * 1000 for c in cs], "o-", color="tab:blue")
    ax.set_xscale("log", base=2)
    ax.set_xticks(cs)
    ax.set_xticklabels([str(c) for c in cs])
    ax.set_xlabel("cutoff")
    ax.set_ylabel("time (ms)")
    ax.set_title("quicksort_improved, n = 100,000 random")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig("graph_cutoff.png", dpi=150)
    print("\nSaved graph_time_vs_n.png and graph_cutoff.png")


def main():
    rng = random.Random(2024)
    results = experiment_sizes(rng)
    experiment_quadratic()
    cutoff_times, best, data = experiment_cutoff(rng)
    experiment_builtin(data, best)
    make_graphs(results, cutoff_times)


if __name__ == "__main__":
    main()
