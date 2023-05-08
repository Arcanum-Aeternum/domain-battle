from domain.interfaces import ValueObject


class SkillProfile(ValueObject):
    """Class that represents a value object of skill profile to the Character"""

    def __init__(self, *, life_points: int, stamina_points: int, mana_points: int) -> None:
        self.__life_points = life_points
        self.__stamina_points = stamina_points
        self.__mana_points = mana_points

    @property
    def get_current_life_points(self) -> int:
        return self.__life_points

    @property
    def get_current_stamina_points(self) -> int:
        return self.__stamina_points

    @property
    def get_current_mana_points(self) -> int:
        return self.__mana_points

    def decrement_life_points(self, damage: int) -> None:
        if self.__life_points < damage:
            damage = self.__life_points
        self.__life_points -= damage

    def decrement_stamina_points(self, stamina_spent: int) -> None:
        if self.__stamina_points < stamina_spent:
            stamina_spent = self.__stamina_points
        self.__stamina_points -= stamina_spent

    def decrement_mana_points(self, mana_spent: int) -> None:
        if self.__mana_points < mana_spent:
            mana_spent = self.__mana_points
        self.__mana_points -= mana_spent
