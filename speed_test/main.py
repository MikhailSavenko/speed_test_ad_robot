from run import build_parser

import time
import requests
import random


def speed_test(url, rounds):
    all_time = []
    all_size = 0

    success_count = 0
    failed_count = 0

    print(f"Запуск теста: {rounds} запросов последовательно...")

    for i in range(1, rounds + 1):
        bust_url = f"{url}?cache_bust={random.randint(1, 100000)}"

        start_time = time.monotonic()
        try:
            response = requests.get(bust_url, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            status = getattr(e.response, "status_code", "Network Error")
            print(f"Запрос № {i} завершился c ошибкой: {status} ({e})")
            failed_count+= 1
            continue
        end_time = time.monotonic()

        file_size_mb = len(response.content) / (1024*1024)
        duration = end_time - start_time
        all_time.append(duration)
        all_size += file_size_mb

        print(f"Запрос № {i} отработал корректно")
        success_count += 1

    if not all_time:
        print("\n=== Результаты замера ===")
        print(f"Все запросы ({failed_count}) завершились ошибкой. Тест скорости невозможен.")
        return

    average_time = sum(all_time) / len(all_time)
    speed_mbps = all_size / sum(all_time)

    print("\n=== Результаты замера ===")
    print(f"Успешных запросов: {success_count} из {rounds}")
    if failed_count > 0:
        print(f"Запросов с ошибкой: {failed_count}")
    print(f"Размер скачанных данных: {all_size:.2f} МБ")
    print(f"Среднее время запроса: {average_time:.3f} сек.")
    print(f"Скорость скачивания: {speed_mbps:.2f} МБ/c")

    print(f"Скорость интернета: {speed_mbps * 8:.2f} Мбит/c")


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    speed_test(url=args.url, rounds=args.rounds)