from queue import Queue
import random
import time

request_queue = Queue()
request_id = 1


def generate_request():
    """Створює нову заявку та додає її до черги."""
    global request_id

    request = {
        "id": request_id,
        "client": f"Client_{random.randint(1000, 9999)}"
    }

    request_queue.put(request)
    print(f"Створено заявку №{request['id']} ({request['client']})")

    request_id += 1


def process_request():
    """Обробляє першу заявку з черги."""
    if not request_queue.empty():
        request = request_queue.get()
        print(f"Обробляється заявка №{request['id']} ({request['client']})")
    else:
        print("Черга порожня.")


def main():
    print("Система обробки заявок запущена.")
    print("Для завершення натисніть Ctrl + C.\n")

    try:
        while True:
            for _ in range(random.randint(1, 3)):
                generate_request()

            time.sleep(1)

            process_request()

            print(f"Заявок у черзі: {request_queue.qsize()}")
            print("-" * 40)

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nПрограму завершено.")


if __name__ == "__main__":
    main()