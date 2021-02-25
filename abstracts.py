from __future__ import annotations

from enum import Enum
from typing import Any, Union

from abc import abstractmethod, ABC
from constants import JSON


class JsonObject(ABC):
    @abstractmethod
    def toJson(self) -> JSON:
        """Parse python object(JsojObject's subclasses) into json data"""

    @classmethod
    @abstractmethod
    def fromJson(cls, data: JSON) -> JsonObject:
        """Parse json data into python object"""


class ParsableEnum(Enum):
    @classmethod
    @abstractmethod
    def parse(cls, value: Any) -> ParsableEnum:
        """
        Parse raw value into ParsableEnum instance.

        Args:
            value (Any): value to parse into ParsableEnum object.
        """
        ...


class ComparableEnum(Enum):
    @abstractmethod
    def __eq__(self, other: Union[ComparableEnum, Any]) -> bool:
        """
        Override '=' operator. Compare with either ComparableEnum instance or raw value

        Args:
            other : other object to compare with this object.
        """
        pass

    def __ne__(self, other: Union[ComparableEnum, Any]) -> bool:
        """
        Override '!=' operator.
        Subclasses are not forced to override this method.

        Args:
            other : other object to compare with this object.
        """
        return not self.__eq__(other)

    def __lt__(self, other: Union[ComparableEnum, Any]) -> bool:
        """
        Override '<' operator.
        Subclasses are not forced to override this method.

        Args:
            other : other object to compare with this object.
        """
        return super(ComparableEnum, self).__lt__(other)

    def __le__(self, other: Union[ComparableEnum, Any]) -> bool:
        """
        Override '<=' operator.
        Subclasses are not forced to override this method.

        Args:
            other : other object to compare with this object.
        """
        return super(ComparableEnum, self).__le__(other)

    def __gt__(self, other: Union[ComparableEnum, Any]) -> bool:
        """
        Override '>' operator.
        Subclasses are not forced to override this method.

        Args:
            other : other object to compare with this object.
        """
        return super(ComparableEnum, self).__gt__(other)

    def __ge__(self, other: Union[ComparableEnum, Any]) -> bool:
        """
        Override '>=' operator.
        Subclasses are not forced to override this method.

        Args:
            other : other object to compare with this object.
        """
        return super(ComparableEnum, self).__ge__(other)