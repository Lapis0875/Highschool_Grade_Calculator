from typing import Iterable, Callable, Any, List, TypeVar, Generic, Optional

Function = Callable[..., Any]       # (item) -> result
Consumer = Callable[..., None]      # (item) -> {} (Return nothing)

T = TypeVar('T')

def extend_filter():
    """Extend filter object for utility."""
    if not getattr(filter, 'find_first', False):
        filter.find_first = lambda self: next(self, default=None)

# class map(object):
#     def __init__(func: Function, *iterables: Iterable):   ...


class compute(map):
    """Specialized version of `map`"""

    def __init__(self, func: Consumer, *iterables: Iterable):
        super(compute, self).__init__(func, *iterables)

    def run(self):
        """Run function"""
        tuple(self)     # Loop all iterables in map(parent class).


class PyOptional(Generic[T]):
    def __init__(self, item: Optional[T]) -> None:
        self._item = item

    @property
    def isNone(self) -> bool:
        return self._item is None

    # TODO : Java의 Optional<T>를 구현. (Nullable한 값에 대한 functional한 처리)


def init():
    extend_filter()


if __name__ != "__name__":
    # Run when imported as module
    init()
