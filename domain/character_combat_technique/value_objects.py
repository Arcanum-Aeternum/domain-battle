from copy import copy

from domain.interfaces import ValueObject

from .exceptions import (
    CombatTechniqueIsAlreadyReady,
    CombatTechniqueIsNotReady,
    InvalidCooldownRange,
    InvalidDamageRange,
    InvalidLoadingTimeRange,
    InvalidManaCostRange,
)


class CombatTechniqueProfile(ValueObject):
    """Class that represents a value object of spell profile to the CharacterSpell"""

    def __init__(self, stamina_cost: int, damage: int, cooldown: int, loading_time: int = 0) -> None:
        if stamina_cost < 0 or stamina_cost > 100:
            raise InvalidManaCostRange()
        if damage < 0 or damage > 100:
            raise InvalidDamageRange()
        if 0 > cooldown > 10:
            raise InvalidCooldownRange()
        if loading_time > cooldown:
            raise InvalidLoadingTimeRange()
        self.__stamina_cost = stamina_cost
        self.__damage = damage
        self.__cooldown = cooldown
        self.__loading_time = loading_time
        self.__just_used = False

    def start_loading_time(self) -> None:
        if self.__loading_time != 0:
            raise CombatTechniqueIsNotReady()
        self.__loading_time = copy(self.__cooldown)
        self.__just_used = True

    def rest_and_prepare(self) -> None:
        if self.__loading_time == 0:
            raise CombatTechniqueIsAlreadyReady()
        if not self.__just_used:
            self.__loading_time -= 1
        else:
            self.__just_used = False

    @property
    def stamina_cost(self) -> int:
        return self.__stamina_cost

    @property
    def damage(self) -> int:
        return self.__damage

    @property
    def cooldown(self) -> int:
        return self.__cooldown

    @property
    def is_ready(self) -> bool:
        return self.__loading_time == 0
