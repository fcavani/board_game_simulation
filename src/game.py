from typing import List
import random
from src.player import PlayerType
from src.bank import (
    InsufficientBalance,
    PropertyHaveOwner,
    PlayerAlreadyOwnIt,
    NegativeBalance
)
from src.board import BoardType


class Game():
    def __init__(self,
                 players: List[PlayerType],
                 bank,
                 board: BoardType,
                 timeout: int = 1000,
                 reward: int = 100):
        self._bank = bank
        self._board = board
        self._timeout = timeout
        self._reward = reward
        random.shuffle(players)
        self._players = players

    @staticmethod
    def _roll_dice() -> int:
        return random.randint(1, 6)

    def _round(self):
        remove: List[PlayerType] = list()
        for player in self._players:
            places = self._roll_dice()
            self._board.move(player, places)
            prop = self._board.position(player)
            try:
                self._bank.buy_property(player, prop)
            except NegativeBalance:
                self._bank.declare_bankruptcy(player)
                remove.append(player)
                if len(self._players) - 1 == len(remove): 
                    break
                continue
            except PropertyHaveOwner:
                self._bank.pay_rent(player, prop)
            except (PlayerAlreadyOwnIt, InsufficientBalance):
                pass
            self._reward_survivor(player)
        for player in remove:
            self._players.remove(player)

    def _reward_survivor(self, player: PlayerType):
        if self._bank.balance(player) >= 0:
            self._bank.make_money(to=player, amount=self._reward)

    def play(self) -> PlayerType:
        for round_number in range(self._timeout):
            self._round()
            if len(self._players) == 1:
                return self._players[0], round_number + 1
        customer = self._bank.richer()
        return customer[0], self._timeout
