"""
CSF303 - Lab 2 - Q2: Merge Sort Analysis (Menu-Driven Program)
Student: Sonam Choki (02240360)
Note: Variables are named with suffix "360" (last 3 digits of student number).
"""

import random
import time
import matplotlib.pyplot as plt

comparisons360 = 0  # global counter for merge sort comparisons (step/frequency count)


# ---------------- Merge Sort (Ascending) ----------------
def merge_sort_360(arr360):
    global comparisons360
    if len(arr360) > 1:
        mid360 = len(arr360) // 2
        left360 = arr360[:mid360]
        right360 = arr360[mid360:]

        merge_sort_360(left360)
        merge_sort_360(right360)

        i360 = j360 = k360 = 0
        while i360 < len(left360) and j360 < len(right360):
            comparisons360 += 1
            if left360[i360] <= right360[j360]:
                arr360[k360] = left360[i360]
                i360 += 1
            else:
                arr360[k360] = right360[j360]
                j360 += 1
            k360 += 1

        while i360 < len(left360):
            arr360[k360] = left360[i360]
            i360 += 1
            k360 += 1

        while j360 < len(right360):
            arr360[k360] = right360[j360]
            j360 += 1
            k360 += 1
    return arr360


# ---------------- Descending Sort (Bubble Sort, any algorithm allowed) ----------------
def bubble_sort_descending_360(arr360):
    steps360 = 0
    n360 = len(arr360)
    for i360 in range(n360):
        for j360 in range(0, n360 - i360 - 1):
            steps360 += 1
            if arr360[j360] < arr360[j360 + 1]:
                arr360[j360], arr360[j360 + 1] = arr360[j360 + 1], arr360[j360]
    return arr360, steps360


def get_array_from_user_360():
    size360 = int(input("How many numbers? "))
    arr360 = []
    for i360 in range(size360):
        val360 = int(input(f"Enter number {i360 + 1}: "))
        arr360.append(val360)
    return arr360


def generate_random_array_360(size360):
    return [random.randint(1, 1000) for _ in range(size360)]


def run_complexity_test_360(data_type360):
    global comparisons360
    sizes360 = [100, 200, 400, 800, 1600]
    steps_list360 = []
    time_list360 = []

    for size360 in sizes360:
        if data_type360 == "random":
            arr360 = generate_random_array_360(size360)
        elif data_type360 == "sorted":
            arr360 = list(range(size360))
        else:  # descending
            arr360 = list(range(size360, 0, -1))

        comparisons360 = 0
        start_time360 = time.time()
        merge_sort_360(arr360)
        end_time360 = time.time()

        steps_list360.append(comparisons360)
        time_list360.append(end_time360 - start_time360)

    print(f"\n--- Time Complexity Results ({data_type360} data) ---")
    print("Size  | Comparisons | Time (s)")
    for size360, steps360, t360 in zip(sizes360, steps_list360, time_list360):
        print(f"{size360:5} | {steps360:11} | {t360:.6f}")

    plt.figure(figsize=(8, 5))
    plt.plot(sizes360, steps_list360, marker='o')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Comparison Count')
    plt.title(f'Merge Sort Complexity - {data_type360.capitalize()} Data')
    plt.grid(True)
    plt.tight_layout()
    filename360 = f'merge_sort_{data_type360}_360.png'
    plt.savefig(filename360)
    print(f"Graph saved as {filename360}")


def print_menu_360():
    print("\n===== Q2: Merge Sort Analysis Menu =====")
    print("1. Enter array manually")
    print("2. Generate random array")
    print("3. Sort in Ascending Order using Merge Sort")
    print("4. Sort in Descending Order (any sorting algorithm)")
    print("5. Time Complexity for ascending random data")
    print("6. Time Complexity for ascending already sorted data")
    print("7. Time Complexity for ascending descending-sorted data")
    print("8. Exit")


def main():
    global comparisons360
    current_array360 = []

    while True:
        print_menu_360()
        choice360 = input("Enter your choice: ").strip()

        if choice360 == '1':
            current_array360 = get_array_from_user_360()
            print("Array entered:", current_array360)

        elif choice360 == '2':
            size360 = int(input("Enter size of random array: "))
            current_array360 = generate_random_array_360(size360)
            print("Random array generated:", current_array360)

        elif choice360 == '3':
            if not current_array360:
                print("Please enter or generate an array first (option 1 or 2).")
                continue
            comparisons360 = 0
            sorted_array360 = merge_sort_360(current_array360.copy())
            print("Sorted (Ascending):", sorted_array360)
            print("Total comparisons (steps):", comparisons360)

        elif choice360 == '4':
            if not current_array360:
                print("Please enter or generate an array first (option 1 or 2).")
                continue
            sorted_desc360, steps360 = bubble_sort_descending_360(current_array360.copy())
            print("Sorted (Descending):", sorted_desc360)
            print("Total steps:", steps360)

        elif choice360 == '5':
            run_complexity_test_360("random")

        elif choice360 == '6':
            run_complexity_test_360("sorted")

        elif choice360 == '7':
            run_complexity_test_360("descending")

        elif choice360 == '8':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
