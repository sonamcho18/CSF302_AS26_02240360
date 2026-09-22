"""
CSF303 - Lab 2 - Q3: Square Matrix Multiplication
Student: Sonam Choki (02240360)
Note: Variables are named with suffix "360" (last 3 digits of student number).
"""

import random


def input_matrix_360(n360, name360):
    print(f"\nEnter matrix {name360} ({n360}x{n360}) row by row, values separated by space:")
    matrix360 = []
    for i360 in range(n360):
        row360 = list(map(int, input(f"Row {i360 + 1}: ").split()))
        matrix360.append(row360)
    return matrix360


def generate_random_matrix_360(n360):
    return [[random.randint(1, 10) for _ in range(n360)] for _ in range(n360)]


def print_matrix_360(matrix360):
    for row360 in matrix360:
        print(row360)


def multiply_matrices_360(a360, b360, n360):
    result360 = [[0] * n360 for _ in range(n360)]
    steps360 = 0
    for i360 in range(n360):
        for j360 in range(n360):
            for k360 in range(n360):
                result360[i360][j360] += a360[i360][k360] * b360[k360][j360]
                steps360 += 1
    return result360, steps360


def main():
    print("=== Q3: Square Matrix Multiplication ===")
    n360 = int(input("Enter size of square matrix (power of 2, e.g. 2, 4, 8): "))

    mode360 = input("Input matrices (M)anually or (R)andomly? ").strip().upper()

    if mode360 == 'M':
        matrix_a360 = input_matrix_360(n360, "A")
        matrix_b360 = input_matrix_360(n360, "B")
    else:
        matrix_a360 = generate_random_matrix_360(n360)
        matrix_b360 = generate_random_matrix_360(n360)
        print("\nMatrix A:")
        print_matrix_360(matrix_a360)
        print("\nMatrix B:")
        print_matrix_360(matrix_b360)

    result360, steps360 = multiply_matrices_360(matrix_a360, matrix_b360, n360)

    print("\nResultant Matrix (A x B):")
    print_matrix_360(result360)

    print(f"\nTotal basic operations (multiplications + additions, step/frequency count): {steps360}")


if __name__ == "__main__":
    main()
