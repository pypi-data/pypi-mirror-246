from typing import Tuple, Union


def if_not_instance_raise(obj: object, expected_type: Union[type, Tuple[type, ...]]):
    if not isinstance(obj, expected_type):
        raise TypeError(f"Expected `{expected_type}`, but got `{type(obj).__name__}`")
