from pathlib import Path
from statistics import mean
from timeit import repeat


def read_text(file_path: str) -> str:
    """Читає текстовий файл, підтримуючи UTF-8 та Windows-1251."""
    raw_data = Path(file_path).read_bytes()

    for encoding in ("utf-8", "utf-8-sig", "cp1251"):
        try:
            return raw_data.decode(encoding)
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Не вдалося визначити кодування файлу: {file_path}")


def boyer_moore_search(text: str, pattern: str) -> int:
    """Пошук підрядка алгоритмом Боєра—Мура (правило поганого символу)."""
    if pattern == "":
        return 0

    text_length = len(text)
    pattern_length = len(pattern)

    if pattern_length > text_length:
        return -1

    bad_character = {
        character: index for index, character in enumerate(pattern)
    }

    shift = 0

    while shift <= text_length - pattern_length:
        pattern_index = pattern_length - 1

        while (
            pattern_index >= 0
            and pattern[pattern_index] == text[shift + pattern_index]
        ):
            pattern_index -= 1

        if pattern_index < 0:
            return shift

        mismatched_character = text[shift + pattern_index]
        shift += max(
            1,
            pattern_index - bad_character.get(mismatched_character, -1),
        )

    return -1


def build_lps(pattern: str) -> list[int]:
    """Створює таблицю найдовших префіксів і суфіксів для КМП."""
    lps = [0] * len(pattern)
    prefix_length = 0
    index = 1

    while index < len(pattern):
        if pattern[index] == pattern[prefix_length]:
            prefix_length += 1
            lps[index] = prefix_length
            index += 1
        elif prefix_length:
            prefix_length = lps[prefix_length - 1]
        else:
            lps[index] = 0
            index += 1

    return lps


def kmp_search(text: str, pattern: str) -> int:
    """Пошук підрядка алгоритмом Кнута—Морріса—Пратта."""
    if pattern == "":
        return 0

    lps = build_lps(pattern)
    text_index = 0
    pattern_index = 0

    while text_index < len(text):
        if text[text_index] == pattern[pattern_index]:
            text_index += 1
            pattern_index += 1

            if pattern_index == len(pattern):
                return text_index - pattern_index

        elif pattern_index:
            pattern_index = lps[pattern_index - 1]
        else:
            text_index += 1

    return -1


def rabin_karp_search(text: str, pattern: str) -> int:
    """Пошук підрядка алгоритмом Рабіна—Карпа."""
    if pattern == "":
        return 0

    text_length = len(text)
    pattern_length = len(pattern)

    if pattern_length > text_length:
        return -1

    base = 256
    modulus = 1_000_000_007
    pattern_hash = 0
    window_hash = 0
    highest_power = pow(base, pattern_length - 1, modulus)

    for index in range(pattern_length):
        pattern_hash = (
            pattern_hash * base + ord(pattern[index])
        ) % modulus
        window_hash = (
            window_hash * base + ord(text[index])
        ) % modulus

    for start in range(text_length - pattern_length + 1):
        if (
            pattern_hash == window_hash
            and text[start:start + pattern_length] == pattern
        ):
            return start

        if start < text_length - pattern_length:
            window_hash = (
                window_hash
                - ord(text[start]) * highest_power
            ) % modulus
            window_hash = (
                window_hash * base
                + ord(text[start + pattern_length])
            ) % modulus

    return -1


def measure_search(
    function,
    text: str,
    pattern: str,
    number: int = 100,
    repeat_count: int = 5,
) -> float:
    """
    Повертає середній час одного запуску алгоритму в секундах.
    """
    measurements = repeat(
        lambda: function(text, pattern),
        number=number,
        repeat=repeat_count,
    )

    return mean(measurements) / number


def print_table(results: list[dict]) -> None:
    header = (
        f"{'Текст':<10}"
        f"{'Підрядок':<14}"
        f"{'Алгоритм':<28}"
        f"{'Час, мс':>12}"
    )

    print("\n" + header)
    print("-" * len(header))

    for result in results:
        print(
            f"{result['text']:<10}"
            f"{result['pattern_type']:<14}"
            f"{result['algorithm']:<28}"
            f"{result['time'] * 1000:>12.6f}"
        )


def print_conclusions(results: list[dict]) -> None:
    print("\nНайшвидші алгоритми:")

    text_names = sorted({result["text"] for result in results})

    for text_name in text_names:
        text_results = [
            result for result in results
            if result["text"] == text_name
        ]

        for pattern_type in ("існуючий", "вигаданий"):
            filtered = [
                result for result in text_results
                if result["pattern_type"] == pattern_type
            ]
            winner = min(filtered, key=lambda result: result["time"])

            print(
                f"- {text_name}, {pattern_type} підрядок: "
                f"{winner['algorithm']} "
                f"({winner['time'] * 1000:.6f} мс)"
            )

        overall_text_winner = min(
            (
                {
                    "algorithm": algorithm,
                    "average": mean(
                        result["time"]
                        for result in text_results
                        if result["algorithm"] == algorithm
                    ),
                }
                for algorithm in {
                    result["algorithm"] for result in text_results
                }
            ),
            key=lambda item: item["average"],
        )

        print(
            f"- {text_name}, у середньому: "
            f"{overall_text_winner['algorithm']} "
            f"({overall_text_winner['average'] * 1000:.6f} мс)"
        )

    all_algorithms = {result["algorithm"] for result in results}
    overall_winner = min(
        (
            {
                "algorithm": algorithm,
                "average": mean(
                    result["time"]
                    for result in results
                    if result["algorithm"] == algorithm
                ),
            }
            for algorithm in all_algorithms
        ),
        key=lambda item: item["average"],
    )

    print(
        f"- Загалом: {overall_winner['algorithm']} "
        f"({overall_winner['average'] * 1000:.6f} мс)"
    )


def main() -> None:
    articles = [
        {
            "name": "Стаття 1",
            "file": "стаття 1.txt",
            "existing_pattern": "алгоритми та структури даних",
        },
        {
            "name": "Стаття 2",
            "file": "стаття 2.txt",
            "existing_pattern": "рекомендаційної системи",
        },
    ]

    missing_pattern = "вигаданий_підрядок_12345"

    algorithms = {
        "Боєра—Мура": boyer_moore_search,
        "Кнута—Морріса—Пратта": kmp_search,
        "Рабіна—Карпа": rabin_karp_search,
    }

    results = []

    for article in articles:
        text = read_text(article["file"])

        patterns = {
            "існуючий": article["existing_pattern"],
            "вигаданий": missing_pattern,
        }

        print(f"\n{article['name']}: {len(text)} символів")

        for pattern_type, pattern in patterns.items():
            expected_index = text.find(pattern)

            print(
                f"{pattern_type.capitalize()} підрядок "
                f"{pattern!r}: індекс {expected_index}"
            )

            for algorithm_name, algorithm in algorithms.items():
                actual_index = algorithm(text, pattern)

                if actual_index != expected_index:
                    raise AssertionError(
                        f"{algorithm_name} повернув {actual_index}, "
                        f"очікувалося {expected_index}"
                    )

                average_time = measure_search(
                    algorithm,
                    text,
                    pattern,
                )

                results.append(
                    {
                        "text": article["name"],
                        "pattern_type": pattern_type,
                        "algorithm": algorithm_name,
                        "time": average_time,
                    }
                )

    print_table(results)
    print_conclusions(results)


if __name__ == "__main__":
    main()
