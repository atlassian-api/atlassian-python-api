from typing import Union, TypeVar, Callable, Any

from typing_extensions import TypeAlias

T_id: TypeAlias = Union[str, int]
_Data: TypeAlias = Union[dict, str]
T_resp_json: TypeAlias = Union[dict, None]

_T = TypeVar("T")

def copy_type(_:_T) -> Callable[[Any], _T]:
    """Decorator to inherit typing from parent."""
    return lambda x: x
