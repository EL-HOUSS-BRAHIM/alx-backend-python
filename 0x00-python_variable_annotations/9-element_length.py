#!/usr/bin/env python3
from typing import List, Tuple, Sequence
def element_length(lst: List[Sequence]) -> List[Tuple[Sequence, int]]:
    return [(i, len(i)) for i in lst]