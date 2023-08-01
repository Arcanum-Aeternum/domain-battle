from domain.character import ICharacterPublicMethods
from domain.interfaces import ValueObject

from .interfaces import ITeam, ITeamBuilder, ITeamPublicMethods


class Team(ValueObject, ITeam):
    """Value Object that represents the Team"""

    def __init__(self) -> None:
        raise NotImplementedError("This class should not be instantiated directly.")

    def _init(self) -> None:
        self.__characters: tuple[ICharacterPublicMethods, ...]

    def _set_characters(self, characters: tuple[ICharacterPublicMethods, ...]) -> None:
        self.__characters = characters

    @classmethod
    def create_new(cls) -> ITeamBuilder:
        new_team = cls.__new__(cls)
        new_team._init()
        return _TeamBuilder(new_team)

    @property
    def characters(self) -> tuple[ICharacterPublicMethods, ...]:
        return tuple(self.__characters)


class _TeamBuilder(ITeamBuilder):
    """Builder that helps to create a Team"""

    def __init__(self, team: Team) -> None:
        self.__team = team
        self.__characters: list[ICharacterPublicMethods] = []

    def add_character(self, character: ICharacterPublicMethods) -> ITeamBuilder:
        self.__characters.append(character)
        return self

    def build(self) -> ITeamPublicMethods:
        if len(self.__characters) == 0:
            raise ValueError("Team should have at least one Character.")
        self.__team._set_characters(tuple(self.__characters))
        return self.__team
