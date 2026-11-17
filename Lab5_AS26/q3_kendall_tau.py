"""
CSF302 - Lab 5, Q3 task 5: Kendall tau distance between two users' rankings
Name: Sonam Choki
Student Number: 02240360

Kendall tau distance = number of movie pairs the two users order differently.
Trick: write user 2's ranking using user 1's positions. Then every pair the
users disagree on becomes an inversion, so we reuse the merge-sort counter.
"""

from q3_inversions import count_inversions_merge

MOVIES = [
    "Inception", "Titanic", "Avatar", "The Matrix", "Interstellar",
    "Frozen", "Joker", "Parasite", "Coco", "Up",
]
N = len(MOVIES)

EXAMPLE_USER1 = [5, 1, 4, 8, 2, 3, 7, 6, 9, 10]
EXAMPLE_USER2 = [1, 5, 4, 2, 8, 3, 6, 7, 10, 9]


def read_ranking(user):
    """Read 10 movie numbers (best to worst) from the keyboard."""
    while True:
        text = input(f"\nUser {user} ranking (10 numbers, best first; "
                     f"press Enter for the example): ").strip()
        if text == "":
            ranking = EXAMPLE_USER1 if user == 1 else EXAMPLE_USER2
            print("  using example:", " ".join(map(str, ranking)))
            return ranking
        try:
            ranking = [int(x) for x in text.replace(",", " ").split()]
        except ValueError:
            print("  Please type numbers only, e.g. 3 1 2 5 4 6 8 7 10 9")
            continue
        if sorted(ranking) != list(range(1, N + 1)):
            print(f"  Please type each number 1 to {N} exactly once.")
            continue
        return ranking


def kendall_tau_distance(r1, r2):
    position_in_r1 = {movie: pos for pos, movie in enumerate(r1)}
    sequence = [position_in_r1[movie] for movie in r2]
    return count_inversions_merge(sequence)


def disagreeing_pairs(r1, r2):
    p1 = {m: i for i, m in enumerate(r1)}
    p2 = {m: i for i, m in enumerate(r2)}
    pairs = []
    for a in range(1, N + 1):
        for b in range(a + 1, N + 1):
            if (p1[a] < p1[b]) != (p2[a] < p2[b]):
                pairs.append((a, b))
    return pairs


def main():
    print("CSF302 Lab 5 - Q3 Kendall Tau Distance | Sonam Choki | 02240360\n")
    print("Movies:")
    for i, m in enumerate(MOVIES, 1):
        print(f"  {i:>2}. {m}")

    r1 = read_ranking(1)
    r2 = read_ranking(2)

    print("\n" + "=" * 60)
    print(f"{'Rank':>4} | {'User 1':<16} | {'User 2':<16}")
    print("-" * 60)
    for i in range(N):
        print(f"{i + 1:>4} | {MOVIES[r1[i] - 1]:<16} | {MOVIES[r2[i] - 1]:<16}")
    print("=" * 60)

    d = kendall_tau_distance(r1, r2)
    max_pairs = N * (N - 1) // 2
    pairs = disagreeing_pairs(r1, r2)
    assert d == len(pairs)

    print(f"\nKendall tau distance (merge-sort inversions): {d}")
    print(f"Check by brute force (pairs they disagree on): {len(pairs)}")
    if pairs:
        print("Disagreeing pairs:")
        for a, b in pairs[:10]:
            print(f"   {MOVIES[a - 1]} vs {MOVIES[b - 1]}")
        if len(pairs) > 10:
            print(f"   ... and {len(pairs) - 10} more")
    print(f"\nMaximum possible distance = {N}*{N - 1}/2 = {max_pairs}")
    print(f"Normalised distance = {d}/{max_pairs} = {d / max_pairs:.3f}")
    print(f"Similarity          = 1 - {d}/{max_pairs} = {1 - d / max_pairs:.3f}"
          f"  ({(1 - d / max_pairs) * 100:.1f}% of pairs agree)")
    print(f"Kendall tau coefficient = 1 - 2*{d}/{max_pairs} = "
          f"{1 - 2 * d / max_pairs:.3f}   (+1 = identical, -1 = opposite)")


if __name__ == "__main__":
    main()
