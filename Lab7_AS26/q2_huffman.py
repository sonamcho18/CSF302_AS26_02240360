"""
CSF302 - Lab 7, Q2: Huffman Coding
Name: Sonam Choki
Student Number: 02240360

Usage:
    python3 q2_huffman.py                       # text1.txt, text2.txt, text3.txt
    python3 q2_huffman.py a.txt b.txt ...       # your own files
"""

import heapq
import os
import sys
from collections import Counter


class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq, self.char, self.left, self.right = freq, char, left, right


# ---------------------------------------------------------------
# 1. Build the Huffman tree with a priority queue (heapq)
# ---------------------------------------------------------------
def build_tree(text):
    freq = Counter(text)
    heap = []
    for i, (ch, f) in enumerate(freq.items()):
        heapq.heappush(heap, (f, i, Node(f, ch)))   # i breaks ties
    counter = len(heap)
    if len(heap) == 1:                              # only one kind of char
        f, _, only = heap[0]
        return Node(f, left=only), freq
    while len(heap) > 1:
        f1, _, a = heapq.heappop(heap)              # two smallest
        f2, _, b = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, counter, Node(f1 + f2, left=a, right=b)))
        counter += 1
    return heap[0][2], freq


# ---------------------------------------------------------------
# 2. Code table: left = 0, right = 1
# ---------------------------------------------------------------
def make_codes(node, prefix="", codes=None):
    if codes is None:
        codes = {}
    if node.char is not None:
        codes[node.char] = prefix or "0"
    else:
        if node.left:
            make_codes(node.left, prefix + "0", codes)
        if node.right:
            make_codes(node.right, prefix + "1", codes)
    return codes


# ---------------------------------------------------------------
# 3. Encode and decode
# ---------------------------------------------------------------
def encode(text, codes):
    return "".join(codes[ch] for ch in text)


def decode(bits, root):
    out = []
    node = root
    for b in bits:
        node = node.left if b == "0" else node.right
        if node.char is not None:
            out.append(node.char)
            node = root
    return "".join(out)


def show(ch):
    return {" ": "' '", "\n": "\\n", "\t": "\\t"}.get(ch, ch)


def process(path, show_table):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    root, freq = build_tree(text)
    codes = make_codes(root)
    bits = encode(text, codes)
    decoded = decode(bits, root)

    name = os.path.basename(path)
    print("=" * 66)
    print(f"File: {name}  ({len(text)} characters, {len(freq)} different)")
    print("=" * 66)
    if show_table:
        print("TASK 2: Code table (most frequent first)")
        print(f"  {'char':>5} {'freq':>6}  code")
        for ch, f in sorted(freq.items(), key=lambda x: (-x[1], codes[x[0]])):
            print(f"  {show(ch):>5} {f:>6}  {codes[ch]}")
        print()
    print(f"TASK 3: First 60 bits of encoded file: {bits[:60]}...")
    print(f"        Decoded text equals original: {decoded == text}")
    fixed = len(text) * 8
    print(f"TASK 4: Fixed-length (8 bits/char): {fixed:,} bits")
    print(f"        Huffman                   : {len(bits):,} bits")
    print(f"        Compression ratio         : {len(bits) / fixed:.3f} "
          f"(saves {(1 - len(bits) / fixed) * 100:.1f}%)")
    print(f"        Average bits per char     : {len(bits) / len(text):.2f}")
    print()
    return name, len(text), len(freq), fixed, len(bits), decoded == text


if __name__ == "__main__":
    print("CSF302 Lab 7 - Q2 Huffman Coding | Sonam Choki | 02240360\n")
    here = os.path.dirname(os.path.abspath(__file__))
    files = sys.argv[1:] or [os.path.join(here, f)
                             for f in ("text1.txt", "text2.txt", "text3.txt")]
    rows = [process(p, show_table=(i == 0)) for i, p in enumerate(files)]

    print("=" * 66)
    print("Summary: compression compared with 8-bit fixed-length encoding")
    print("=" * 66)
    print(f"{'file':<12} {'chars':>6} {'unique':>6} {'8-bit':>8} {'Huffman':>8} "
          f"{'ratio':>6} {'ok':>4}")
    print("-" * 66)
    for name, n, u, fixed, h, ok in rows:
        print(f"{name:<12} {n:>6} {u:>6} {fixed:>8,} {h:>8,} {h / fixed:>6.3f} "
              f"{'yes' if ok else 'NO':>4}")
    print("-" * 66)
    print("Fewer different characters, or a few very common ones, give")
    print("better compression (smaller ratio).")
