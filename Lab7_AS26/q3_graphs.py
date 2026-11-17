"""
CSF302 - Lab 7, Q3: Shortest Paths and Minimum Spanning Trees
Name: Sonam Choki
Student Number: 02240360

Usage:
    python3 q3_graphs.py                  # reads graph.txt
    python3 q3_graphs.py my_graph.txt     # lines: "from to weight", optional "SOURCE X"
"""

import heapq
import os
import random
import sys
import time


# ---------------------------------------------------------------
# Read a weighted directed graph from a file
# ---------------------------------------------------------------
def read_graph(path):
    graph = {}
    source = None
    with open(path) as f:
        for line in f:
            line = line.split("#")[0].strip()
            if not line:
                continue
            parts = line.split()
            if parts[0].upper() == "SOURCE":
                source = parts[1]
                continue
            u, v, w = parts[0], parts[1], float(parts[2])
            w = int(w) if w.is_integer() else w
            graph.setdefault(u, []).append((v, w))
            graph.setdefault(v, [])
    if source is None:
        source = next(iter(graph))
    return graph, source


# ---------------------------------------------------------------
# 1. Dijkstra with a binary heap: O((V + E) log V)
# ---------------------------------------------------------------
def dijkstra(graph, source):
    dist = {v: float("inf") for v in graph}
    prev = {v: None for v in graph}
    dist[source] = 0
    heap = [(0, source)]
    done = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)                       # u's distance is now FINAL
        for v, w in graph[u]:
            if v not in done and d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, prev


def path_to(prev, v):
    path = []
    while v is not None:
        path.append(v)
        v = prev[v]
    return path[::-1]


def part_1(path):
    print("=" * 66)
    print(f"TASK 1: Dijkstra (binary heap) on {os.path.basename(path)}")
    print("=" * 66)
    graph, src = read_graph(path)
    print("Edges:")
    for u in graph:
        for v, w in graph[u]:
            print(f"  {u} -> {v}  weight {w}")
    dist, prev = dijkstra(graph, src)
    print(f"\nShortest distances from source {src}:")
    print(f"  {'vertex':>6} {'distance':>9}  path")
    for v in sorted(graph):
        if dist[v] == float("inf"):
            print(f"  {v:>6} {'inf':>9}  (unreachable)")
        else:
            print(f"  {v:>6} {dist[v]:>9}  {' -> '.join(path_to(prev, v))}")
    print()


# ---------------------------------------------------------------
# 2. Kruskal (union-find) and Prim (heap)
# ---------------------------------------------------------------
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path halving
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                                  # would make a cycle
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def kruskal(n, edges):
    """edges = list of (w, u, v). Take cheapest edges that don't make a cycle."""
    uf = UnionFind(n)
    total, chosen = 0, []
    for w, u, v in sorted(edges):
        if uf.union(u, v):
            total += w
            chosen.append((u, v, w))
            if len(chosen) == n - 1:
                break
    return total, chosen


def prim(n, adj, start=0):
    """Grow one tree; always add the cheapest edge leaving it."""
    in_tree = [False] * n
    total, chosen = 0, []
    heap = [(0, start, -1)]
    while heap and len(chosen) < n - 1:
        w, u, frm = heapq.heappop(heap)
        if in_tree[u]:
            continue
        in_tree[u] = True
        if frm != -1:
            total += w
            chosen.append((frm, u, w))
        for v, wv in adj[u]:
            if not in_tree[v]:
                heapq.heappush(heap, (wv, v, u))
    return total, chosen


def random_connected_graph(n, m, rng):
    """Random spanning tree first (so it is connected), then extra edges."""
    edges = set()
    order = list(range(n))
    rng.shuffle(order)
    for i in range(1, n):
        a, b = order[i], order[rng.randrange(i)]
        edges.add((min(a, b), max(a, b)))
    while len(edges) < m:
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b:
            edges.add((min(a, b), max(a, b)))
    wedges = [(rng.randint(1, 1000), a, b) for a, b in edges]
    adj = [[] for _ in range(n)]
    for w, a, b in wedges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    return wedges, adj


def part_2_3():
    print("=" * 66)
    print("TASKS 2-3: Kruskal vs Prim on a small graph and random graphs")
    print("=" * 66)
    names = "ABCDEFG"
    small = [(7, 0, 1), (5, 0, 3), (8, 1, 2), (9, 1, 3), (7, 1, 4), (5, 2, 4),
             (15, 3, 4), (6, 3, 5), (8, 4, 5), (9, 4, 6), (11, 5, 6)]
    adj = [[] for _ in range(7)]
    for w, a, b in small:
        adj[a].append((b, w))
        adj[b].append((a, w))
    tk, ek = kruskal(7, small)
    tp, ep = prim(7, adj)
    print("Small undirected graph (7 vertices, 11 edges)")
    print("  Kruskal MST edges:", ", ".join(f"{names[u]}-{names[v]}({w})" for u, v, w in ek))
    print("  Prim    MST edges:", ", ".join(f"{names[u]}-{names[v]}({w})" for u, v, w in ep))
    print(f"  Total weight: Kruskal = {tk}, Prim = {tp}\n")

    rng = random.Random(302)
    print(f"{'test':>5} {'V':>5} {'E':>6} | {'Kruskal':>9} {'Prim':>9} | same?")
    print("-" * 48)
    ok = True
    for t in range(1, 11):
        n = rng.randint(5, 300)
        m = rng.randint(n - 1, min(n * (n - 1) // 2, 4 * n))
        edges, adj = random_connected_graph(n, m, rng)
        a, _ = kruskal(n, edges)
        b, _ = prim(n, adj)
        ok &= a == b
        print(f"{t:>5} {n:>5} {m:>6} | {a:>9} {b:>9} | {'YES' if a == b else 'NO'}")
    print("-" * 48)
    print("Both MST algorithms give the same total weight on every graph:", ok)
    print()


def part_4():
    print("=" * 66)
    print("TASK 4: Timing Kruskal vs Prim, V = 1,000")
    print("=" * 66)
    rng = random.Random(302)
    n = 1000
    print(f"{'graph':>8} {'E':>9} | {'Kruskal (s)':>12} {'Prim (s)':>10} | {'faster':>8} | same weight")
    print("-" * 70)
    winners = {}
    for name, m in [("sparse", 3 * n), ("dense", n * n // 4)]:
        edges, adj = random_connected_graph(n, m, rng)
        t0 = time.perf_counter()
        a, _ = kruskal(n, edges)
        t1 = time.perf_counter()
        b, _ = prim(n, adj)
        t2 = time.perf_counter()
        win = "Kruskal" if t1 - t0 < t2 - t1 else "Prim"
        winners[name] = win
        print(f"{name:>8} {m:>9,} | {t1 - t0:>12.4f} {t2 - t1:>10.4f} | {win:>8} | {a == b}")
    print("-" * 70)
    print("Theory:")
    print("  Kruskal = O(E log E): sort all edges, then union-find (almost O(1)).")
    print("  Prim    = O(E log V) with a heap, or O(V^2) with a simple array.")
    print("  On SPARSE graphs both are about the same (E is small).")
    print("  On DENSE graphs (E ~ V^2) Prim with an array, O(V^2), is the best")
    print("  choice in theory, because Kruskal must sort ~V^2 edges.")
    print("What I measured in Python:")
    print(f"  Sparse winner: {winners['sparse']},  dense winner: {winners['dense']}.")
    if winners["dense"] == "Kruskal":
        print("  Kruskal won on the dense graph because Python's sort is written")
        print("  in C and is extremely fast, while Prim does ~250,000 heap pushes")
        print("  and pops in slower Python code. So the constant factors of the")
        print("  language matter as much as the big-O here.")
    else:
        print("  Prim won on the dense graph: it avoids sorting all the edges.")
    print()


# ---------------------------------------------------------------
# 5. A negative edge breaks Dijkstra
# ---------------------------------------------------------------
def bellman_ford(graph, source):
    dist = {v: float("inf") for v in graph}
    prev = {v: None for v in graph}
    dist[source] = 0
    for _ in range(len(graph) - 1):
        for u in graph:
            for v, w in graph[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
    return dist, prev


def part_5():
    print("=" * 66)
    print("TASK 5: One negative edge makes Dijkstra WRONG")
    print("=" * 66)
    graph = {
        "A": [("B", 2), ("C", 5)],
        "B": [("D", 1)],
        "C": [("B", -4)],            # the negative edge
        "D": [],
    }
    print("Edges: A->B 2, A->C 5, B->D 1, C->B -4  (negative!)\n")
    dd, dp = dijkstra(graph, "A")
    bd, bp = bellman_ford(graph, "A")
    print(f"  {'vertex':>6} | {'Dijkstra':>8} {'path':<14} | {'correct':>7} {'path':<14}")
    print("  " + "-" * 60)
    for v in "ABCD":
        flag = "" if dd[v] == bd[v] else "  <-- WRONG"
        print(f"  {v:>6} | {dd[v]:>8} {'->'.join(path_to(dp, v)):<14} | "
              f"{bd[v]:>7} {'->'.join(path_to(bp, v)):<14}{flag}")
    print("\n(The 'correct' answers come from the Bellman-Ford algorithm.)")
    print("Why: Dijkstra takes B out of the heap first (distance 2) and marks it")
    print("FINAL. Later it finds A->C->B = 5 + (-4) = 1, which is shorter, but B")
    print("is already finished, so B and D keep their wrong distances.")
    print("Dijkstra assumes adding an edge can never make a path shorter, which")
    print("is only true when every weight is >= 0.")
    print()


if __name__ == "__main__":
    print("CSF302 Lab 7 - Q3 Shortest Paths & MST | Sonam Choki | 02240360\n")
    here = os.path.dirname(os.path.abspath(__file__))
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "graph.txt")
    part_1(path)
    part_2_3()
    part_4()
    part_5()
