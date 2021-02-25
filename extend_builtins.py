from __future__ import annotations

import inspect
from functools import wraps
from typing import Iterable, Callable, Any, List, TypeVar, Generic, Optional

__all__ = (
    'Function',
    'Consumer',
    'T',
    'Filter',
    'Compute',
    'NoneValueException',
    'NoSuchElementException',
    'PyOptional'
)

Function = Callable[..., Any]  # (item) -> result
Consumer = Callable[..., None]  # (item) -> {} (Return nothing)

T = TypeVar('T')


# class map(object):
#     def __init__(func: Function, *iterables: Iterable):   ...


class Filter(filter):
    """Extend filter object to support several utility methods"""

    def find_first(self) -> Optional[Any]:
        """Find first element in filter object."""
        try:
            return tuple(self)[0]
        except IndexError:
            return None

    def length(self) -> int:
        """Macro function of len(tuple(self)). Maybe find some implementation in CPython implementation of 'filter'"""
        return len(tuple(self))

    def toList(self) -> list:
        """Macro function of list(self)."""
        return list(self)

    def toTuple(self) -> tuple:
        return tuple(self)


# Optional<T> port

class _PyOptionalException(Exception):
    def __init__(self) -> None:
        super(_PyOptionalException, self).__init__()

    def __repr__(self) -> str:
        return 'PyOptional[T].{}'.format(self.__class__.__name__)

    def __str__(self) -> str:
        return 'PyOptional[T] raised exception!'


class NoneValueException(_PyOptionalException):
    """Exception class used in PyOptional. Indicates PyOptional[T].of(value) got None value."""

    def __str__(self) -> str:
        return 'PyOptional[T].of(value) should accept not-None value!'


class NoSuchElementException(_PyOptionalException):
    """Exception class used in PyOptional. Indicates PyOptional[T] contains None value."""

    def __str__(self) -> str:
        return 'PyOptional[T] contains None value!'


class PyOptional(Generic[T]):
    """Optional<T> implementation in Python."""

    @classmethod
    def empty(cls) -> PyOptional[T]:
        """None 을 담고 있는, 한 마디로 비어있는 PyOptional[T] 객체를 가져옵니다. 이 비어있는 객체는 내부적으로 미리 생성해둔 싱글톤 객체입니다."""
        try:
            return getattr(cls, 'pyopt_instance')
        except AttributeError:
            instance = cls(None)
            setattr(cls, 'pyopt_instance', instance)
            return instance

    @classmethod
    def of(cls, value: T) -> PyOptional[T]:
        """None 이 아닌 객체를 담고 있는 Optional 객체를 생성합니다. None 객체에 대해서는 TypeError를 발생시킵니다."""
        if value is None:
            raise TypeError(
                'PyOptional[T].of(value) must called with non-null value. Use PyOptional[T].empty() for null values.'
            )
        return cls(value)

    @classmethod
    def ofNullable(cls, value: Optional[T]) -> PyOptional[T]:
        """None 인지 아닌지 확신할 수 없는 객체를 담고 있는 Optional 객체를 생성합니다."""
        return cls(value)

    def __init__(self, item: Optional[T]) -> None:
        self._item: Optional[T] = item
        try:
            attrsToPatch = {
                key: attr
                for key, attr
                in item.__dict__.items()
                if not key.startswith('__')
            }
            attrsToPatch.update({
                attr: getattr(item, attr)
                for attr
                in item.__slots__
                if not attr.startswith('__')
            })
        except AttributeError:
            attrsToPatch = {attrName: getattr(item, attrName) for attrName in dir(item) if not attrName.startswith('__')}
        for attrName, attr in attrsToPatch.items():
            if inspect.ismethod(attr):
                setattr(self, attrName, self._WrapOptionalObjectMethod(attr))
            else:
                setattr(self, attrName, attr)

    # Access to value in PyOptional

    def get(self) -> T:
        if self.isNone:
            raise NoSuchElementException()
        return self._item

    def orElse(self, other: T) -> T:
        return self._item if self._item is not None else other

    def orElseGet(self, other: Callable[..., T]) -> T:
        if self.isNone:
            return other()
        return self._item

    def orElseThrow(self, exceptionSupplier: Callable[..., Exception]) -> T:
        if self.isNone:
            raise exceptionSupplier()
        return self._item

    @property
    def isNone(self) -> bool:
        return self._item is None

    isNull = isNone  # Alias

    # Extend item's methods in PyOptional[T] : Experimental feature.
    def _WrapOptionalObjectMethod(self, method: Function) -> Function:
        @wraps(method)
        def wrapper(*args, **kwargs):
            if self.isNone:
                raise NoneValueException()
            else:
                return method()

        return wrapper

    def _WrapOptionalObjectMethodWithName(self, methodName: str) -> Function:
        try:
            method = self._item.__dict__[methodName]

            @wraps(method)
            def wrapper(*args, **kwargs):
                if self.isNone:
                    raise NoneValueException()
                else:
                    return method()     # Since method already has bound 'self' attribute, we can use it by simply calling it.

            return wrapper
        except KeyError:
            raise KeyError("PyOptional[T] cannot patch method in given object with name '{}'".format(methodName))

    # TODO : Java의 Optional<T>를 구현. (Nullable한 값에 대한 functional한 처리)
