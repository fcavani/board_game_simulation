from typing import List, NewType
from src.player import PlayerType, Player
from src.property import PropertyType
from src.behavior import (
    Impulsive,
    Picky,
    Conservative,
    Random,
    Passive
)


BankType = NewType('BankType', object)


class Bank():
    def __init__(self, customers: List[PlayerType], properties: List[PropertyType], open_balance: int):
        self._property_owners: Dict[PropertyType, PlayerType] = {
            prop: None
            for prop in properties
        }
        self._owners: Dict[PlayerType, List[PropertyType]] = {
            customer: list()
            for customer in customers
        }
        self._balance: Dict[PlayerType, int] = {
            customer: open_balance
            for customer in customers
        }
        self._bank = Player('bank', Passive())
        self._balance[self._bank] = 0

    def buy_property(self, player: PlayerType, prop: PropertyType):
        buy = player.behavior.buy(
            rent=prop.rent,
            balance=self._balance[player]
        )
        if buy:
            self._buy_property(player, prop)

    def pay_rent(self, player: PlayerType, prop: PropertyType):
        landlord = self._property_owners[prop]
        self._transfer(player, landlord, prop.rent)

    def declare_bankruptcy(self, player: PlayerType):
        properties = self._owners[player]
        for prop in properties:
            self._property_owners[prop] = None
        self._owners[player] = list()

    def make_money(self, to: PlayerType, amount: int):
        self._balance[to] += amount

    def richer(self) -> PlayerType:
        richer = {
            customer: balance
            for customer, balance in sorted(
                self._balance.items(),
                key=lambda x: x[1],
                reverse=True
            ) if customer.name != self._bank.name
        }
        player = next(iter(richer.items()))
        return player

    def owner(self, prop: PropertyType) -> PlayerType:
        return self._property_owners[prop]

    def balance(self, player: PlayerType) -> int:
        return self._balance[player] 
    
    def _buy_property(self, player: PlayerType, prop: PropertyType):
        balance = self._balance[player]
        if balance < 0:
            raise NegativeBalance('balance is less than zero')
        owner = self._property_owners[prop]
        if not owner:
            if balance >= prop.value:
                self._transfer(player, self._bank, prop.value)
                self._property_owners[prop] = player
                self._owners[player].append(prop)
            else:
                raise InsufficientBalance('insufficient balance')
        elif owner and owner.name != player.name:
            raise PropertyHaveOwner(f'property already have an owner: "{owner.name}"')
        elif owner and owner.name == player.name:
            raise PlayerAlreadyOwnIt(f'player is the owner of this property')

    def _transfer(self, source: PlayerType, destiny: PlayerType, amount: int):
        self._balance[source] -= amount
        self._balance[destiny] += amount


class NegativeBalance(Exception):
    pass


class InsufficientBalance(Exception):
    pass


class PropertyHaveOwner(Exception):
    pass


class PlayerAlreadyOwnIt(Exception):
    pass
