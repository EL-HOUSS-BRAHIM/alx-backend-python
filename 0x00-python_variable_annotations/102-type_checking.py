#!/usr/bin/env python3
from typing import List, Tuple
def zoom_array(lst: Tuple, factor: int = 2) -> List:
    '''Creates multiple copies of items in a tuple.
    '''
    zoomed_in: List = [
        item for item in lst
        for i in range(int(factor))
    ]
    return zoomed_in

array = (12, 72, 91)

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)  # Changed from 3.0 to 3
