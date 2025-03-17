from enum import Enum


class SIPrefix(Enum):
    """
    NONE - no prefix
    n - nano (10^-9)\n
    mc - micro (10^-6)\n
    m - milli (10^-3)\n
    c - centi (10^-2)\n
    k - kilo (10^3)\n
    M - Mega (10^6)\n
    G - Giga (10^9)\n
    """
    NONE = 1.0
    n = 10.0 ** (-9)
    mc = 10.0 ** (-6)
    m = 10.0 ** (-3)
    c = 10.0 ** (-2)
    k = 10.0 ** 3
    M = 10.0 ** 6
    G = 10.0 ** 9

def metrics(func):
    def wrapper(*args, **kwargs):
        num = func(*args)
        if kwargs and isinstance(kwargs['metrics'], str): return num/SIPrefix[kwargs['metrics']].value
        return num
    return wrapper

