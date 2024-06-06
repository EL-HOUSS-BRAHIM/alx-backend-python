#!/usr/bin/env python3
from typing import Sequence, Union, Any, TypeVar
# Define a generic type variable T
T = TypeVar('T')

# Define a function safe_first_element that takes a sequence lst of type T and returns a Union of type T and None


def safe_first_element(lst: Sequence[T]) -> Union[T, None]:
    # Check if the list is not empty
    if lst:
        # Return the first element of the list
        return lst[0]
    else:
        # Return None if the list is empty
        return None
