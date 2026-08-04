import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi


def f(x):
    """Функція, інтеграл якої потрібно обчислити."""
    return x ** 2


def monte_carlo_integral(
    function,
    a: float,
    b: float,
    number_of_points: int = 100_000,
    seed: int = 42,
):
    """
    Обчислює площу під графіком методом Монте-Карло.

    Метод працює для невід'ємної функції на заданому проміжку.
    """

    if number_of_points <= 0:
        raise ValueError("Кількість точок повинна бути більшою за нуль.")

    if a >= b:
        raise ValueError("Нижня межа повинна бути меншою за верхню.")

    rng = np.random.default_rng(seed)

    # Для функції x^2 на проміжку [0, 2]
    # найбільше значення дорівнює f(2) = 4.
    x_for_max = np.linspace(a, b, 10_000)
    function_maximum = np.max(function(x_for_max))

    # Генеруємо випадкові координати точок.
    random_x = rng.uniform(a, b, number_of_points)
    random_y = rng.uniform(0, function_maximum, number_of_points)

    # Визначаємо точки, які потрапили під графік.
    points_under_graph = random_y <= function(random_x)

    rectangle_area = (b - a) * function_maximum
    probability = np.mean(points_under_graph)

    integral = rectangle_area * probability

    return integral, random_x, random_y, points_under_graph


def show_graph(
    function,
    a,
    b,
    random_x,
    random_y,
    points_under_graph,
    points_to_show=5_000,
):
    """Будує графік функції та показує випадкові точки."""

    x = np.linspace(a - 0.5, b + 0.5, 400)
    y = function(x)

    visible_points = min(points_to_show, len(random_x))

    fig, ax = plt.subplots(figsize=(10, 6))

    # Графік функції.
    ax.plot(
        x,
        y,
        color="red",
        linewidth=2,
        label=r"$f(x)=x^2$",
    )

    # Область інтегрування.
    integral_x = np.linspace(a, b, 400)
    integral_y = function(integral_x)

    ax.fill_between(
        integral_x,
        integral_y,
        color="gray",
        alpha=0.3,
        label="Площа під графіком",
    )

    # Точки, що потрапили під графік.
    ax.scatter(
        random_x[:visible_points][points_under_graph[:visible_points]],
        random_y[:visible_points][points_under_graph[:visible_points]],
        color="green",
        s=5,
        alpha=0.4,
        label="Точки під графіком",
    )

    # Точки, що не потрапили під графік.
    ax.scatter(
        random_x[:visible_points][~points_under_graph[:visible_points]],
        random_y[:visible_points][~points_under_graph[:visible_points]],
        color="blue",
        s=5,
        alpha=0.3,
        label="Точки поза графіком",
    )

    ax.axvline(x=a, color="gray", linestyle="--")
    ax.axvline(x=b, color="gray", linestyle="--")

    ax.set_xlim(a - 0.5, b + 0.5)
    ax.set_ylim(0, function(b) + 0.5)

    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")

    ax.set_title(
        "Обчислення інтеграла функції "
        r"$f(x)=x^2$ методом Монте-Карло"
    )

    ax.grid()
    ax.legend()

    plt.show()


def main():
    a = 0
    b = 2
    number_of_points = 100_000

    monte_carlo_result, random_x, random_y, points_under_graph = (
        monte_carlo_integral(
            function=f,
            a=a,
            b=b,
            number_of_points=number_of_points,
        )
    )

    # Перевірка за допомогою scipy.integrate.quad.
    quad_result, quad_error = spi.quad(f, a, b)

    # Аналітичне обчислення:
    # integral(x^2 dx) = x^3 / 3
    analytical_result = (b ** 3 - a ** 3) / 3

    absolute_error = abs(monte_carlo_result - analytical_result)

    relative_error = (
        absolute_error / abs(analytical_result) * 100
    )

    print(f"Кількість випадкових точок: {number_of_points}")
    print(
        "Кількість точок під графіком:",
        np.sum(points_under_graph),
    )

    print(
        f"\nРезультат методу Монте-Карло: "
        f"{monte_carlo_result:.6f}"
    )

    print(
        f"Аналітичний результат: "
        f"{analytical_result:.6f}"
    )

    print(
        f"Результат scipy.integrate.quad: "
        f"{quad_result:.6f}"
    )

    print(
        f"Оцінка помилки quad: "
        f"{quad_error:.16e}"
    )

    print(
        f"\nАбсолютна похибка Монте-Карло: "
        f"{absolute_error:.6f}"
    )

    print(
        f"Відносна похибка Монте-Карло: "
        f"{relative_error:.4f}%"
    )

    show_graph(
        function=f,
        a=a,
        b=b,
        random_x=random_x,
        random_y=random_y,
        points_under_graph=points_under_graph,
    )


if __name__ == "__main__":
    main()