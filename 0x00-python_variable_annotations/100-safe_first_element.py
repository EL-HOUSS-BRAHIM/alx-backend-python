from typing import Sequence, Union, Any, TypeVar

T = TypeVar('T')

def safe_first_element(lst: Sequence[T]) -> Union[T, None]:
    if lst:
        return lst[0]
    else:
        return None