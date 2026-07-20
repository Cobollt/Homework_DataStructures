import argparse
import shutil
from pathlib import Path


def get_unique_path(destination_path: Path) -> Path:

    if not destination_path.exists():
        return destination_path

    counter = 1
    stem = destination_path.stem
    suffix = destination_path.suffix
    parent = destination_path.parent

    while True:
        new_path = parent / f"{stem}_{counter}{suffix}"

        if not new_path.exists():
            return new_path

        counter += 1


def copy_file(file_path: Path, destination_directory: Path) -> None:
    try:
        extension = file_path.suffix.lower().lstrip(".")

        if not extension:
            extension = "no_extension"

        extension_directory = destination_directory / extension
        extension_directory.mkdir(parents=True, exist_ok=True)

        destination_path = extension_directory / file_path.name
        destination_path = get_unique_path(destination_path)

        shutil.copy2(file_path, destination_path)

        print(f"Скопійовано: {file_path} -> {destination_path}")

    except PermissionError:
        print(f"Помилка доступу до файлу: {file_path}")

    except OSError as error:
        print(f"Не вдалося скопіювати файл {file_path}: {error}")


def process_directory(
    source_directory: Path,
    destination_directory: Path
) -> None:
    try:
        for item in source_directory.iterdir():
            try:
                if item.resolve() == destination_directory.resolve():
                    continue

                if item.is_dir():
                    process_directory(item, destination_directory)

                elif item.is_file():
                    copy_file(item, destination_directory)

            except PermissionError:
                print(f"Немає доступу до елемента: {item}")

            except OSError as error:
                print(f"Помилка під час обробки {item}: {error}")

    except FileNotFoundError:
        print(f"Директорію не знайдено: {source_directory}")

    except PermissionError:
        print(f"Немає доступу до директорії: {source_directory}")

    except OSError as error:
        print(f"Помилка читання директорії {source_directory}: {error}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Рекурсивно копіює файли та сортує їх "
            "за розширеннями."
        )
    )

    parser.add_argument(
        "source",
        type=Path,
        help="Шлях до вихідної директорії"
    )

    parser.add_argument(
        "destination",
        type=Path,
        nargs="?",
        default=Path("dist"),
        help="Шлях до директорії призначення. За замовчуванням: dist"
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    source_directory = args.source.resolve()
    destination_directory = args.destination.resolve()

    if not source_directory.exists():
        print(f"Вихідна директорія не існує: {source_directory}")
        return

    if not source_directory.is_dir():
        print(f"Указаний шлях не є директорією: {source_directory}")
        return

    if source_directory == destination_directory:
        print(
            "Вихідна директорія та директорія призначення "
            "не можуть бути однаковими."
        )
        return

    try:
        destination_directory.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(
            "Немає дозволу на створення директорії: "
            f"{destination_directory}"
        )
        return
    except OSError as error:
        print(
            f"Не вдалося створити директорію "
            f"{destination_directory}: {error}"
        )
        return

    print(f"Вихідна директорія: {source_directory}")
    print(f"Директорія призначення: {destination_directory}")
    print("-" * 60)

    process_directory(source_directory, destination_directory)

    print("-" * 60)
    print("Сортування файлів завершено.")


if __name__ == "__main__":
    main()