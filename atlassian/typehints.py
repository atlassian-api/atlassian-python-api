from typing import Callable, TypeVar, Union, cast

from typing_extensions import ParamSpec, TypeAlias

T_id: TypeAlias = Union[str, int]
_Data: TypeAlias = Union[dict, str]
T_resp_json: TypeAlias = Union[dict, None]

P = ParamSpec("P")
T = TypeVar("T")


def copy_type(_: Callable[P, T]) -> Callable[[Callable[..., T]], Callable[P, T]]:
    """Decorator to inherit typing from parent."""

    def decorator(function: Callable[..., T]) -> Callable[P, T]:
        return cast(Callable[P, T], function)

    return decorator
