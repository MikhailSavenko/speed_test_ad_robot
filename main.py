import time
import requests
import random

url = "https://samplelib.com/png/sample-photo-3840x2160.png"


def speed_test(url):
    all_time = []
    all_size = 0

    for _ in range(10):
        start_time = time.time()

        response = requests.get(f"{url}?cache_bust={random.randint(1, 100000)}")

        end_time = time.time()

        # считаем
        file_size_mb = len(response.content) / (1024*1024)
        duration = end_time - start_time
        all_time.append(duration)
        all_size += file_size_mb

    speed_mbps = all_size / sum(all_time)
    speed_mbit = speed_mbps * 8

    print(f"Размер: {file_size_mb} МБ")
    print(f"Скорость скачивания: {speed_mbps:.2f} МБ/c")
    print(f"Скорость интернета: {speed_mbit} Мбит/c")

speed_test(url)