"""
CSF303 - Lab 2 - Q3 (Extension): Strassen's Matrix Multiplication
Student: Sonam Choki (02240360)
Note: Variables are named with suffix "360" (last 3 digits of student number).
Compares standard multiplication vs Strassen's algorithm using
step/frequency counts and running time, for matrix sizes that are
powers of 2 (2, 4, 8, 16 ...).
"""

import random
import time
import matplotlib.pyplot as plt

operations360 = 0  # global step/frequency counter


def generate_random_matrix_360(n360):
    return [[random.randint(1, 10) for _ in range(n360)] for _ in range(n360)]


def add_matrix_360(a360, b360):
    global operations360
    n360 = len(a360)
    result360 = [[0] * n360 for _ in range(n360)]
    for i360 in range(n360):
        for j360 in range(n360):
            result360[i360][j360] = a360[i360][j360] + b360[i360][j360]
            operations360 += 1
    return result360


def sub_matrix_360(a360, b360):
    global operations360
    n360 = len(a360)
    result360 = [[0] * n360 for _ in range(n360)]
    for i360 in range(n360):
        for j360 in range(n360):
            result360[i360][j360] = a360[i360][j360] - b360[i360][j360]
            operations360 += 1
    return result360


def split_matrix_360(matrix360):
    n360 = len(matrix360)
    mid360 = n360 // 2
    a11360 = [row360[:mid360] for row360 in matrix360[:mid360]]
    a12360 = [row360[mid360:] for row360 in matrix360[:mid360]]
    a21360 = [row360[:mid360] for row360 in matrix360[mid360:]]
    a22360 = [row360[mid360:] for row360 in matrix360[mid360:]]
    return a11360, a12360, a21360, a22360


def combine_matrix_360(c11360, c12360, c21360, c22360):
    top360 = [r1360 + r2360 for r1360, r2360 in zip(c11360, c12360)]
    bottom360 = [r1360 + r2360 for r1360, r2360 in zip(c21360, c22360)]
    return top360 + bottom360


def standard_multiply_360(a360, b360):
    global operations360
    n360 = len(a360)
    result360 = [[0] * n360 for _ in range(n360)]
    for i360 in range(n360):
        for j360 in range(n360):
            for k360 in range(n360):
                result360[i360][j360] += a360[i360][k360] * b360[k360][j360]
                operations360 += 1
    return result360


def strassen_multiply_360(a360, b360):
    global operations360
    n360 = len(a360)
    if n360 == 1:
        operations360 += 1
        return [[a360[0][0] * b360[0][0]]]

    a11360, a12360, a21360, a22360 = split_matrix_360(a360)
    b11360, b12360, b21360, b22360 = split_matrix_360(b360)

    m1360 = strassen_multiply_360(add_matrix_360(a11360, a22360), add_matrix_360(b11360, b22360))
    m2360 = strassen_multiply_360(add_matrix_360(a21360, a22360), b11360)
    m3360 = strassen_multiply_360(a11360, sub_matrix_360(b12360, b22360))
    m4360 = strassen_multiply_360(a22360, sub_matrix_360(b21360, b11360))
    m5360 = strassen_multiply_360(add_matrix_360(a11360, a12360), b22360)
    m6360 = strassen_multiply_360(sub_matrix_360(a21360, a11360), add_matrix_360(b11360, b12360))
    m7360 = strassen_multiply_360(sub_matrix_360(a12360, a22360), add_matrix_360(b21360, b22360))

    c11360 = add_matrix_360(sub_matrix_360(add_matrix_360(m1360, m4360), m5360), m7360)
    c12360 = add_matrix_360(m3360, m5360)
    c21360 = add_matrix_360(m2360, m4360)
    c22360 = add_matrix_360(sub_matrix_360(add_matrix_360(m1360, m3360), m2360), m6360)

    return combine_matrix_360(c11360, c12360, c21360, c22360)


def main():
    global operations360
    print("=== Strassen's vs Standard Matrix Multiplication ===")
    sizes360 = [2, 4, 8, 16]
    standard_ops360 = []
    strassen_ops360 = []
    standard_times360 = []
    strassen_times360 = []

    for n360 in sizes360:
        a360 = generate_random_matrix_360(n360)
        b360 = generate_random_matrix_360(n360)

        operations360 = 0
        start_time360 = time.time()
        standard_multiply_360(a360, b360)
        standard_times360.append(time.time() - start_time360)
        standard_ops360.append(operations360)

        operations360 = 0
        start_time360 = time.time()
        strassen_multiply_360(a360, b360)
        strassen_times360.append(time.time() - start_time360)
        strassen_ops360.append(operations360)

    print("\nSize | Standard Ops | Strassen Ops | Standard Time | Strassen Time")
    for n360, so360, sto360, st360, stt360 in zip(
            sizes360, standard_ops360, strassen_ops360, standard_times360, strassen_times360):
        print(f"{n360:4} | {so360:13} | {sto360:13} | {st360:.6f}      | {stt360:.6f}")

    plt.figure(figsize=(8, 5))
    plt.plot(sizes360, standard_ops360, marker='o', label='Standard Multiplication')
    plt.plot(sizes360, strassen_ops360, marker='s', label="Strassen's Algorithm")
    plt.xlabel('Matrix Size (n)')
    plt.ylabel('Operation Count')
    plt.title('Standard vs Strassen Matrix Multiplication')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('strassen_comparison_360.png')
    print("\nGraph saved as strassen_comparison_360.png")


if __name__ == "__main__":
    main()
