from run import build_parser

import time
import requests
import random


def speed_test(url: str, rounds: int):
    """Генератор, который выполняет замеры и возвращает результаты каждого раунда."""
    for i in range(1, rounds + 1):
        bust_url = f"{url}?cache_bust={random.randint(1, 100000)}"
        start_time = time.monotonic()

        try:
            response = requests.get(bust_url, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            status = e.response.status_code if e.response is not None else "Network Error"
            yield {"round": i, "success": False, "error": f"{status} ({e})"}
            continue

        end_time = time.monotonic()

        yield {
            "round": i,
            "success": True,
            "duration": end_time - start_time,
            "size_mb": len(response.content) / (1024 * 1024)
        }


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    all_time = []
    all_size = 0
    
    success_count = 0
    failed_count = 0

    print(f"Запуск теста: {args.rounds} запросов последовательно...")

    for result in speed_test(url=args.url, rounds=args.rounds):
        i = result["round"]
        if not result["success"]:
            print(f"Запрос № {i} завершился c ошибкой: {result['error']}")
            failed_count += 1
        else:
            print(f"Запрос № {i} отработал корректно")
            success_count += 1
            all_time.append(result["duration"])
            all_size += result["size_mb"]

    if not all_time:
        print("\n=== Результаты замера ===")
        print(f"Все запросы ({failed_count}) завершились ошибкой. Тест скорости невозможен.")
        exit(1)

    average_time = sum(all_time) / len(all_time)
    speed_mbps = all_size / sum(all_time)

    print("\n=== Результаты замера ===")
    print(f"Успешных запросов: {success_count} из {args.rounds}")
    if failed_count > 0:
        print(f"Запросов с ошибкой: {failed_count}")
    print(f"Размер скачанных данных: {all_size:.2f} МБ")
    print(f"Среднее время запроса: {average_time:.3f} сек.")
    print(f"Скорость скачивания: {speed_mbps:.2f} МБ/c")
    print(f"Скорость интернета: {speed_mbps * 8:.2f} Мбит/c")