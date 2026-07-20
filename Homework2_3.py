import random
import timeit


def insertion_sort(arr):
    arr = arr.copy()

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr


def merge(left, right):
    result = []

    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def merge_sort(arr):
    if len(arr) <= 1:
        return arr.copy()

    middle = len(arr) // 2

    left = merge_sort(arr[:middle])
    right = merge_sort(arr[middle:])

    return merge(left, right)


def timsort(arr):
    return sorted(arr)


def measure(sort_function, data):
    return timeit.timeit(lambda: sort_function(data), number=5) / 5


sizes = [100, 500, 1000, 5000]

print(f"{'Size':<10}{'Insertion':<15}{'Merge':<15}{'Timsort':<15}")
print("-" * 55)

for size in sizes:
    data = [random.randint(0, 100000) for _ in range(size)]

    insertion_time = measure(insertion_sort, data)
    merge_time = measure(merge_sort, data)
    timsort_time = measure(timsort, data)

    print(
        f"{size:<10}"
        f"{insertion_time:<15.6f}"
        f"{merge_time:<15.6f}"
        f"{timsort_time:<15.6f}"
    )