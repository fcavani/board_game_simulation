from typing import NewType, NamedTuple
from src.behavior import BehaviorType


PlayerType = NewType('PlayerType', object)


class Player(NamedTuple):
    name: str
    behavior: BehaviorType

    def __str__(self) -> str:
        return self.name
