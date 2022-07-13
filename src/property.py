import random
from typing import NewType, NamedTuple


PropertyType = NewType('PropertyType', object)


class Property(NamedTuple):
    name: str
    value: int
    rent: int

    def __str__(self) -> str:
        return self.name


def create_property(name: str,
                    mu_value: float,
                    sigma_value: float,
                    mu_rent: float,
                    sigma_rent: float) -> PropertyType:
    value = abs(random.gauss(mu_value, sigma_value))
    rent = abs(value * random.gauss(mu_rent, sigma_rent))
    value = int(round(value, 0))
    rent = int(round(rent, 0))
    return Property(name, value, rent)
