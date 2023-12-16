from typing import Any, Callable, Protocol, reveal_type


# class MyCallable(Protocol):
#     def __call__(self, *args, **kwargs) -> Any: ...
#
#
#

# def print_name(f: Callable[..., Any]) -> None:
#     reveal_type(f)
#     print(f.__name__)


def print_name(f: Callable[..., Any]) -> None:
    print(f.__name__)

def foo() -> None:
    pass

print_name(foo)

print_name(lambda x: x)
