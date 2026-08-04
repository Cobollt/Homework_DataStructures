from timeit import timeit


COINS = [50, 25, 10, 5, 2, 1]


def validate_amount(amount: int) -> None:
    """Перевіряє коректність суми."""

    if not isinstance(amount, int):
        raise TypeError("Сума повинна бути цілим числом.")

    if amount < 0:
        raise ValueError("Сума не може бути від'ємною.")


def find_coins_greedy(amount: int) -> dict[int, int]:
    """
    Формує решту за допомогою жадібного алгоритму.

    Алгоритм послідовно вибирає найбільший номінал монети,
    який не перевищує залишок суми.
    """

    validate_amount(amount)

    result = {}
    remainder = amount

    for coin in COINS:
        count, remainder = divmod(remainder, coin)

        if count > 0:
            result[coin] = count

        if remainder == 0:
            break

    return result


def find_min_coins(amount: int) -> dict[int, int]:
    """
    Формує решту за допомогою динамічного програмування.

    Функція знаходить мінімальну кількість монет,
    необхідних для формування заданої суми.
    """

    validate_amount(amount)

    if amount == 0:
        return {}

    # min_coins[current_sum] — мінімальна кількість монет,
    # необхідна для формування current_sum.
    min_coins = [float("inf")] * (amount + 1)

    # used_coin[current_sum] — остання монета,
    # використана для формування current_sum.
    used_coin = [0] * (amount + 1)

    min_coins[0] = 0

    for current_sum in range(1, amount + 1):
        for coin in COINS:
            if coin <= current_sum:
                previous_sum = current_sum - coin

                if min_coins[previous_sum] + 1 < min_coins[current_sum]:
                    min_coins[current_sum] = min_coins[previous_sum] + 1
                    used_coin[current_sum] = coin

    result = {}
    current_sum = amount

    # Відновлюємо набір монет.
    while current_sum > 0:
        coin = used_coin[current_sum]

        if coin == 0:
            raise ValueError(
                f"Неможливо сформувати суму {amount} "
                f"за допомогою доступних монет."
            )

        result[coin] = result.get(coin, 0) + 1
        current_sum -= coin

    return dict(sorted(result.items()))


def count_coins(result: dict[int, int]) -> int:
    """Повертає загальну кількість використаних монет."""

    return sum(result.values())


def calculate_sum(result: dict[int, int]) -> int:
    """Повертає суму, сформовану набором монет."""

    return sum(coin * count for coin, count in result.items())


def compare_algorithms(amount: int, repetitions: int = 1000) -> None:
    """Порівнює час виконання двох алгоритмів."""

    greedy_time = timeit(
        lambda: find_coins_greedy(amount),
        number=repetitions,
    )

    dynamic_time = timeit(
        lambda: find_min_coins(amount),
        number=repetitions,
    )

    print(f"\nПорівняння для суми {amount}")
    print(f"Кількість повторень: {repetitions}")
    print(f"Жадібний алгоритм: {greedy_time:.6f} секунд")
    print(f"Динамічне програмування: {dynamic_time:.6f} секунд")


def main() -> None:
    amount = 113

    greedy_result = find_coins_greedy(amount)
    dynamic_result = find_min_coins(amount)

    print(f"Сума решти: {amount}")

    print("\nЖадібний алгоритм:")
    print(greedy_result)
    print("Кількість монет:", count_coins(greedy_result))
    print("Перевірка суми:", calculate_sum(greedy_result))

    print("\nДинамічне програмування:")
    print(dynamic_result)
    print("Кількість монет:", count_coins(dynamic_result))
    print("Перевірка суми:", calculate_sum(dynamic_result))

    compare_algorithms(amount=113, repetitions=1000)
    compare_algorithms(amount=10_000, repetitions=10)


if __name__ == "__main__":
    main()