def safely_get_value(dct: dict, key: str, default: str = None) -> str:
    """
    Given a dictionary and a key, safely get the value of the key
    """
    if key in dct:
        return dct[key]
    else:
        return default