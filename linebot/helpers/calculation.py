from math import ceil
from random import randint


def calc_need_exp(level: int) -> int:
    return ceil(100 * level + 0.25 * level**2)


def random_exp() -> int:
    return randint(30, 100)
