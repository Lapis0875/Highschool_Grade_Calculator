from datetime import datetime
from typing import NoReturn, Optional, List

from extend_builtins import PyOptional


def thrower() -> NoReturn:
    raise TypeError('object is empty!')


# myList: list = [1, 2, 3, 4, 5]
# myNotNullList: PyOptional[list] = PyOptional[list].ofNullable(myList)
# print('myNotNullList.get() > ', myNotNullList.get())
# print('myNotNullList.orElse() > ', myNotNullList.orElse([]))
# print('myNotNullList.orElseGet() > ', myNotNullList.orElseGet(lambda: []))
# print('myNotNullList.orElseThrow() > ', myNotNullList.orElseThrow(thrower))
# myNullList: PyOptional[list] = PyOptional[list].empty()
# # print('myNullList.get() > ', myNullList.get())
# print('myNullList.orElse() > ', myNullList.orElse([]))
# print('myNullList.orElseGet() > ', myNullList.orElseGet(lambda: []))
# print('myNullList.orElseThrow() > ', myNullList.orElseThrow(thrower))


class Member:
    def __init__(self, id: int, name: str):
        self.id = id,
        self.name = name

    def __str__(self) -> str:
        return "Member '{}', with id: {}".format(self.name, self.id)


class Order:
    def __init__(self, when: datetime, who: Member, cost: int):
        self.when = when
        self.who = who
        self.cost = cost


def getMemberFromOptionalOrder(order: Optional[Order]) -> Member:
    return PyOptional[Order].ofNullable(order).orElseThrow(thrower).who


member = Member(id=1030407, name='James')
order = Order(when=datetime.now(), who=member, cost=5000)
print(getMemberFromOptionalOrder(order))
print(getMemberFromOptionalOrder(None))
