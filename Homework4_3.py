import heapq


def minimum_connection_cost(cables):
    if any(length < 0 for length in cables):
        raise ValueError("Довжина кабелю не може бути від’ємною")

    # Створюємо копію, щоб не змінювати початковий список
    heap = cables.copy()
    heapq.heapify(heap)

    total_cost = 0
    connection_order = []

    while len(heap) > 1:
        # Беремо два найкоротші кабелі
        first = heapq.heappop(heap)
        second = heapq.heappop(heap)

        # З’єднуємо їх
        combined = first + second
        total_cost += combined

        connection_order.append((first, second, combined))

        # Повертаємо новий кабель у купу
        heapq.heappush(heap, combined)

    return total_cost, connection_order


cables = [4, 3, 2, 6]

total_cost, order = minimum_connection_cost(cables)

for first, second, combined in order:
    print(f"{first} + {second} = {combined}")

print("Мінімальні загальні витрати:", total_cost)