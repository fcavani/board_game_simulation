import pytest
from unittest import mock
from src.behavior import (
    Impulsive,
    Picky,
    Conservative,
    Random,
    Passive,
    InvalidBehaviorException,
    PassiveBehavior
)


def test_impulsive():
    behavior = Impulsive()
    assert behavior.buy() is True


def test_picky_no_rent_value():
    behavior = Picky()
    with pytest.raises(InvalidBehaviorException) as exec_info:
        behavior.buy()
    assert exec_info.value.args[0] == 'rent value wasn''t given'


def test_picky_must_not_buy():
    behavior = Picky()
    assert behavior.buy(rent=10) is False


def test_picky_must_buy():
    behavior = Picky()
    assert behavior.buy(rent=51) is True


def test_conservative_no_property_value():
    behavior = Conservative()
    with pytest.raises(InvalidBehaviorException) as exec_info:
        behavior.buy()
    assert exec_info.value.args[0] == 'balance value wasn''t given'


def test_conservative_must_not_buy():
    behavior = Conservative()
    assert behavior.buy(balance=79) is False


def test_conservative_must_buy():
    behavior = Conservative()
    assert behavior.buy(balance=80) is True


def test_random_must_not_buy():
    with mock.patch('random.randint', return_value=0):
        behavior = Random()
        assert behavior.buy() is False


def test_random_must_buy():
    with mock.patch('random.randint', return_value=1):
        behavior = Random()
        assert behavior.buy() is True


def test_passive():
    behavior = Passive()
    with pytest.raises(PassiveBehavior) as exec_info:
        behavior.buy()
