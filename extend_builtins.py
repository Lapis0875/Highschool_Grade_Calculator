from typing import Iterable, Callable, Any, List

Function = Callable[..., Any]       # (item) -> result
Consumer = Callable[..., None]      # (item) -> {} (Return nothing)


def extend_filter():
    """Extend filter object for utility."""
    if not getattr(filter, 'find_first', False):
        filter.find_first = lambda self: next(self)

# class map(object):
#     def __init__(func: Function, *iterables: Iterable):   ...


class compute(map):
    """Specialized version of `map`"""

    def __init__(self, func: Consumer, *iterables: Iterable):
        super(compute, self).__init__(func, *iterables)

    def run(self):
        """Run function"""
        tuple(self)     # Loop all iterables in map(parent class).


def init():
    extend_filter()


if __name__ != "__name__":
    # Run when imported as module
    init()
