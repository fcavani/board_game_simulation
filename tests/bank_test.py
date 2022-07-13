import pytest
from src.player import Player
from src.behavior import Impulsive
from src.property import Property
from src.bank import (
    Bank,
    NegativeBalance,
    PropertyHaveOwner,
    PlayerAlreadyOwnIt,
    InsufficientBalance
)


def test_balance():
    player = Player('player 1', Impulsive())
    prop = Property('property 0', 10, 1)
    bank = Bank([player], [prop], open_balance=300)
    assert bank.balance(player) == 300


def test_make_money():
    player = Player('player 1', Impulsive())
    prop = Property('property 0', 10, 1)
    bank = Bank([player], [prop], open_balance=0)
    bank.make_money(player, 1e100)
    assert bank.balance(player) == 1e100


def test_declare_bankruptcy():
    player = Player('player 1', Impulsive())
    prop = Property('property 0', 10, 1)
    bank = Bank([player], [prop], open_balance=0)
    bank.declare_bankruptcy(player)
    owner = bank.owner(prop)
    assert owner is None


def test_buy_property_negative_balance():
    player = Player('player 1', Impulsive())
    prop = Property('property 0', 10, 1)
    bank = Bank([player], [prop], open_balance=-10)
    with pytest.raises(NegativeBalance) as exec_info:
        bank.buy_property(player, prop)


def test_buy_property_have_owner():
    player_1 = Player('player 1', Impulsive())
    player_2 = Player('player 2', Impulsive())
    prop = Property('property 0', 10, 1)
    bank = Bank([player_1, player_2], [prop], open_balance=300)
    bank.buy_property(player_1, prop)
    with pytest.raises(PropertyHaveOwner) as exec_info:
        bank.buy_property(player_2, prop)


def test_buy_property_buy_twice():
    player = Player('player 1', Impulsive())
    prop = Property('property 0', 10, 1)
    bank = Bank([player], [prop], open_balance=300)
    bank.buy_property(player, prop)
    with pytest.raises(PlayerAlreadyOwnIt) as exec_info:
        bank.buy_property(player, prop)


def test_buy_property_insufficient_balance():
    player = Player('player 1', Impulsive())
    prop = Property('property 0', 10, 1)
    bank = Bank([player], [prop], open_balance=1)
    with pytest.raises(InsufficientBalance) as exec_info:
        bank.buy_property(player, prop)


def test_owner():
    player = Player('player 1', Impulsive())
    prop = Property('property 0', 10, 1)
    bank = Bank([player], [prop], open_balance=300)
    bank.buy_property(player, prop)
    owner = bank.owner(prop)
    assert owner == player


def test_pay_rent():
    player_1 = Player('player 1', Impulsive())
    player_2 = Player('player 2', Impulsive())
    prop = Property('property 0', 10, 5)
    bank = Bank([player_1, player_2], [prop], open_balance=300)
    bank.buy_property(player_1, prop)
    bank.pay_rent(player_2, prop)
    assert bank.balance(player_2) < 300
