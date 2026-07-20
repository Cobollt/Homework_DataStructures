import turtle


def draw_koch_curve(turtle_object, length, recursion_level):
    if recursion_level == 0:
        turtle_object.forward(length)
        return

    segment_length = length / 3

    draw_koch_curve(turtle_object, segment_length, recursion_level - 1)
    turtle_object.left(60)

    draw_koch_curve(turtle_object, segment_length, recursion_level - 1)
    turtle_object.right(120)

    draw_koch_curve(turtle_object, segment_length, recursion_level - 1)
    turtle_object.left(60)

    draw_koch_curve(turtle_object, segment_length, recursion_level - 1)


def draw_koch_snowflake(turtle_object, length, recursion_level):
    for _ in range(3):
        draw_koch_curve(turtle_object, length, recursion_level)
        turtle_object.right(120)


def get_recursion_level():
    while True:
        try:
            level = int(input("Введіть рівень рекурсії від 0 до 6: "))

            if 0 <= level <= 6:
                return level

            print("Рівень рекурсії повинен бути від 0 до 6.")

        except ValueError:
            print("Помилка: потрібно ввести ціле число.")


def main():
    recursion_level = get_recursion_level()

    screen = turtle.Screen()
    screen.title("Сніжинка Коха")
    screen.setup(width=900, height=700)

    drawing_turtle = turtle.Turtle()
    drawing_turtle.speed(0)
    drawing_turtle.hideturtle()

    side_length = 450

    drawing_turtle.penup()
    drawing_turtle.goto(-side_length / 2, side_length / 3)
    drawing_turtle.pendown()

    draw_koch_snowflake(
        drawing_turtle,
        side_length,
        recursion_level
    )

    screen.mainloop()


if __name__ == "__main__":
    main()