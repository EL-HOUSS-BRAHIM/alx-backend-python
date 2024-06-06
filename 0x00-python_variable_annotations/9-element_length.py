#!/usr/bin/env python3
# This script defines a function element_length that takes a list of sequences as input
# and returns a list of tuples, where each tuple contains a sequence and its length.
from typing import List, Tuple, Sequence


def element_length(lst: List[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Calculate the length of each sequence in the input list and return a list of tuples
    where each tuple contains a sequence and its length.

    Args:
        lst: A list of sequences.

    Returns:
        A list of tuples, where each tuple contains a sequence and its length.
    """
    return [(i, len(i)) for i in lst]
