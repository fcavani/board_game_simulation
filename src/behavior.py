from typing import NewType
import random


BehaviorType = NewType('BehaviorType', object)


class Behavior():
    def buy(self, **kwargs):
        pass


class Impulsive(Behavior):
    name = 'impulsive'
    def buy(self, **kwargs) -> bool:
        return True


class Picky(Behavior):
    name = 'picky'
    def buy(self, **kwargs) -> bool:
        if 'rent' not in kwargs:
            raise InvalidBehaviorException('rent value wasn''t given')
        return kwargs['rent'] > 50


class Conservative(Behavior):
    name = 'conservative'
    def buy(self, **kwargs) -> bool:
        if 'balance' not in kwargs:
            raise InvalidBehaviorException('balance value wasn''t given')
        return kwargs['balance'] >= 80


class Random(Behavior):
    name = 'random'
    def buy(self, **kwargs) -> bool:
        return bool(random.randint(0, 1))


class Passive(Behavior):
    name='passive'
    def buy(self, **kwargs) -> bool:
        raise PassiveBehavior()


class InvalidBehaviorException(Exception):
    pass


class PassiveBehavior(Exception):
    pass
