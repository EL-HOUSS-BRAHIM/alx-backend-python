#!/usr/bin/env python3
"""Returns a function that multiplies a float by multiplier"""


def make_multiplier(multiplier: float) -> callable:
    """Returns a function that multiplies a float by multiplier"""
    def multiply(n: float) -> float:
        return n * multiplier
    return multiply
