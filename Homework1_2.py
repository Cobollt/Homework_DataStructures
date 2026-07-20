from collections import deque


def is_palindrome(text):
    normalized_text = text.replace(" ", "").lower()
    characters = deque(normalized_text)

    while len(characters) > 1:
        first_character = characters.popleft()
        last_character = characters.pop()

        if first_character != last_character:
            return False

    return True


def main():
    text = input("Введіть рядок: ")

    if is_palindrome(text):
        print("Рядок є паліндромом.")
    else:
        print("Рядок не є паліндромом.")


if __name__ == "__main__":
    main()