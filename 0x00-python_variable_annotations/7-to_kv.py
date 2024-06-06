#!/usr/bin/env python3
"""This script defines a function to_kv that takes a string and a number as input.."""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Converts a string and a number to a tuple containing the string and the square of the number."""
    return (k, float(v ** 2))
