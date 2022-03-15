from functools import wraps
from time import time


def add(a: int, b: int) -> int:
    """
    Adds a and b together
    :param a:
    :param b:
    :return: Sum of a and b
    """
    return a + b


def sub(a: int, b: int) -> int:
    """
    Subtracts a and b
    :param a:
    :param b:
    :return: Result of a - b
    """
    return a - b


def mul(a: int, b: int) -> int:
    """
    Multiplies a and b together
    :param a:
    :param b:
    :return: Product of a and b
    """
    return a * b


def div(a: int, b: int) -> int:
    """
    Divides a and b
    :param a:
    :param b:
    :return: Quotient of a and b
    """
    return a / b


add(100, 2)
sub(100, 2)
mul(100, 2)
div(100, 2)
