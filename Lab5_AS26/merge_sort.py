"""
Merge sort (from Lab 1), shared by Q2 and Q3.
Name: Sonam Choki | Student Number: 02240360
"""


def merge_sort(a):
    """Return a new sorted list. O(n log n) time, stable."""
    if len(a) <= 1:
        return list(a)
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    return merge(left, right)


def merge(left, right):
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


if __name__ == "__main__":
    print(merge_sort([5, 2, 9, 1, 5, 6, 0, 3]))
