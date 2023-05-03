from copy import copy

from domain.character_spell.exceptions import (
    InvalidCooldownRange,
    InvalidDamageRange,
    InvalidLoadingTimeRange,
    InvalidManaCostRange,
    SpellIsAlreadyReady,
    SpellIsNotReady,
)
from domain.interfaces import ValueObject


class SpellProfile(ValueObject):
    """Class that represents a value object of spell profile to the CharacterSpell"""

    def __init__(self, mana_cost: int, damage: int, cooldown: int, loading_time: int = 0) -> None:
        if mana_cost < 0 or mana_cost > 100:
            raise InvalidManaCostRange()
        if damage < 0 or damage > 100:
            raise InvalidDamageRange()
        if 0 > cooldown > 10:
            raise InvalidCooldownRange()
        if loading_time > cooldown:
            raise InvalidLoadingTimeRange()
        self.__mana_cost = mana_cost
        self.__damage = damage
        self.__cooldown = cooldown
        self.__loading_time = loading_time

    def start_loading_time(self) -> None:
        if self.__loading_time != 0:
            raise SpellIsNotReady()
        self.__loading_time = copy(self.__cooldown)

    def load_spell(self) -> None:
        if self.__loading_time == 0:
            raise SpellIsAlreadyReady()
        self.__loading_time -= 1

    @property
    def get_mana_cost(self) -> int:
        return self.__mana_cost

    @property
    def get_damage(self) -> int:
        return self.__damage

    @property
    def get_cooldown(self) -> int:
        return self.__cooldown

    @property
    def is_ready(self) -> bool:
        return self.__loading_time == 0
