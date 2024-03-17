from math import ceil


def calc_need_exp(level: int) -> int:
    return ceil(100 * level + 0.25 * level**2)
