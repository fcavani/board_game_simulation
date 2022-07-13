from typing import List, Dict, NewType
from src.player import PlayerType
from src.property import PropertyType


BoardType = NewType('BoardType', object)


class Board():
    def __init__(self, players: List[PlayerType], properties: List[PropertyType]):
        self._length = len(properties)
        self._properties = properties
        self._player_position: Dict[PlayerType, int] = {
            player: -1
            for player in players
        }

    def move(self, player: PlayerType, places: int):
        if places <= 0:
            raise InvalidPosition()
        position = self._player_position[player]
        new_position = (position + places) % self._length
        self._player_position[player] = new_position

    def position(self, player: PlayerType) -> PropertyType:
        position = self._player_position[player]
        if position < 0:
            raise InvalidPosition()
        return self._properties[position]


class InvalidPosition(Exception):
    pass
