"""
Contains the core of hintwith: hintwith(), hintwithmethod(), etc.

NOTE: this module is private. All functions and objects are available in the main
`hintwith` namespace - use that instead.

"""
from typing import Any, Callable, Literal, TypeVar, overload

from typing_extensions import Concatenate, ParamSpec

P = ParamSpec("P")
Q = ParamSpec("Q")
S = TypeVar("S")
T = TypeVar("T")

__all__ = ["hintwith", "hintwithmethod"]


@overload
def hintwith(
    __func: Callable[P, Any], __is_method: Literal[False] = False
) -> Callable[[Callable[..., T]], Callable[P, T]]:
    ...


@overload
def hintwith(
    __func: Callable[P, Any], __is_method: Literal[True] = True
) -> Callable[[Callable[Concatenate[S, Q], T]], Callable[Concatenate[S, P], T]]:
    ...


def hintwith(__func: Callable, __is_method: bool = False) -> Callable:
    """
    This decorator does literally NOTHING to the decorated function except change
    its type hints with the annotations of an existing function. This means that
    nothing inside the decorated function (including attributes like `__doc__` and
    `__annotations__`) are modified, but the type hints may SEEM to be changed in
    language tools like Pylance.

    Parameters
    ----------
    __func : Callable
        An existing function.

    __is_method : bool, optional
        Determines whether the decorated function is a method, by default False.

    Returns
    -------
    Callable
        A decorator which does nothing to the function.

    """

    def decorator(a: Any) -> Any:
        return a  # See? We do nothing to the function

    return decorator


@overload
def hintwithmethod(
    __method: Callable[Concatenate[Any, P], Any], __is_method: Literal[False] = False
) -> Callable[[Callable[..., T]], Callable[P, T]]:
    ...


@overload
def hintwithmethod(
    __method: Callable[Concatenate[Any, P], Any], __is_method: Literal[True] = True
) -> Callable[[Callable[Concatenate[S, Q], T]], Callable[Concatenate[S, P], T]]:
    ...


def hintwithmethod(__method: Callable, __is_method: bool = False) -> Callable:
    """
    Behaves like `hintwith()` except that it hints the decorated function with a
    method rather than a direct callable.

    Parameters
    ----------
    __method : Callable
        An existing method.

    __is_method : bool, optional
        Determines whether the decorated function is a method, by default False.

    Returns
    -------
    Callable
        A decorator which does nothing to the function.

    """

    def decorator(a: Any) -> Any:
        return a  # See? We do nothing to the function

    return decorator
