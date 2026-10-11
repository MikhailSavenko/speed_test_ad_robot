from constants import TEST_URL_DEFAULT, DEFAULT_ROUNDS

import argparse

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Cкрипт-замерятель скорости интернета со своего компьютера.")
    
    p.add_argument("--url", type=str, help="Ссылка на тяжелую картинку", default=TEST_URL_DEFAULT)
    p.add_argument("--rounds", type=int, help="Количество запросов к адресу картинки", default=DEFAULT_ROUNDS)

    return p