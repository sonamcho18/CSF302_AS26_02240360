"""
CSF302 - Lab 6, Q4 (Optional): Optimal Binary Search Tree
Name: Sonam Choki
Student Number: 02240360

p[i] = probability of searching for key ki (successful search)
q[i] = probability of searching for a value between keys (dummy key di)
Goal: build the BST with the smallest expected search cost.
"""

P = [0, 0.15, 0.10, 0.05, 0.10, 0.20]       # p[1..5] (p[0] unused)
Q = [0.05, 0.10, 0.05, 0.05, 0.05, 0.10]    # q[0..5]


def optimal_bst(p, q, n):
    # e[i][j] = expected cost of keys ki..kj, w[i][j] = sum of probabilities
    e = [[0.0] * (n + 1) for _ in range(n + 2)]
    w = [[0.0] * (n + 1) for _ in range(n + 2)]
    root = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 2):
        e[i][i - 1] = q[i - 1]          # empty tree: just a dummy key
        w[i][i - 1] = q[i - 1]
    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            e[i][j] = float("inf")
            w[i][j] = w[i][j - 1] + p[j] + q[j]
            for r in range(i, j + 1):   # try every key as the root
                t = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if t < e[i][j]:
                    e[i][j] = t
                    root[i][j] = r
    return e, w, root


def print_structure(root, i, j, parent=None, side=None):
    """Same style as the textbook: 'k2 is the root', 'k1 is the left child of k2'."""
    if j < i:
        d = f"d{j}"
        print(f"  {d} is the {side} child of k{parent}")
        return
    r = root[i][j]
    if parent is None:
        print(f"  k{r} is the root")
    else:
        print(f"  k{r} is the {side} child of k{parent}")
    print_structure(root, i, r - 1, r, "left")
    print_structure(root, r + 1, j, r, "right")


def draw_tree(root, i, j, prefix="", is_left=None):
    """Sideways picture of the tree."""
    if j < i:
        label = f"d{j}"
        left = right = None
    else:
        r = root[i][j]
        label = f"k{r}"
        left, right = (i, r - 1), (r + 1, j)
    if is_left is None:
        print("  " + label)
        child_prefix = "  "
    else:
        print("  " + prefix + ("├── L: " if is_left else "└── R: ") + label)
        child_prefix = prefix + ("│      " if is_left else "       ")
    if left is not None:
        draw_tree(root, left[0], left[1], child_prefix if is_left is not None else "", True)
        draw_tree(root, right[0], right[1], child_prefix if is_left is not None else "", False)


if __name__ == "__main__":
    print("CSF302 Lab 6 - Q4 Optimal Binary Search Tree | Sonam Choki | 02240360\n")
    n = 5
    print("i    :", "  ".join(f"{i:>4}" for i in range(n + 1)))
    print("p[i] :", "  ".join(f"{'':>4}" if i == 0 else f"{P[i]:>4.2f}" for i in range(n + 1)))
    print("q[i] :", "  ".join(f"{Q[i]:>4.2f}" for i in range(n + 1)))
    print(f"Sum of all probabilities = {sum(P) + sum(Q):.2f}\n")

    e, w, root = optimal_bst(P, Q, n)

    print("e[i][j] table (expected cost):")
    print("       " + "".join(f"{j:>7}" for j in range(0, n + 1)))
    for i in range(1, n + 2):
        print(f"  i={i:<2} " + "".join(
            f"{e[i][j]:>7.2f}" if j >= i - 1 else f"{'':>7}" for j in range(0, n + 1)))
    print("\nroot[i][j] table:")
    print("       " + "".join(f"{j:>5}" for j in range(1, n + 1)))
    for i in range(1, n + 1):
        print(f"  i={i:<2} " + "".join(
            f"{'k' + str(root[i][j]):>5}" if j >= i else f"{'':>5}" for j in range(1, n + 1)))

    cost = e[1][n]
    print(f"\nExpected search cost = {cost:.2f}   "
          f"(expected 2.75 -> {'CORRECT' if abs(cost - 2.75) < 1e-9 else 'WRONG'})")
    print("\nStructure of the optimal tree:")
    print_structure(root, 1, n)
    print("\nPicture (L = left child, R = right child):")
    draw_tree(root, 1, n)
