#!/usr/bin/env python3
# This script defines a function to_kv that takes a string and a number as input
# and returns a tuple containing the string and the square of the number.
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Converts a string and a number to a tuple containing the string and the square of the number.

    Args:
        k (str): The string value.
        v (Union[int, float]): The number value.

    Returns:
        Tuple[str, float]: A tuple containing the string and the square of the number.
    """
    return (k, float(v ** 2))
