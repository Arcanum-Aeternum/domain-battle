from domain.character import ICharacter
from domain.interfaces import ValueObject

from .interfaces import ITeam, ITeamBuilder, ITeamFactory


class Team(ValueObject, ITeamFactory, ITeam):
    """Value Object that represents the Team"""

    def __init__(self) -> None:
        raise NotImplementedError("This class should not be instantiated directly.")

    def _init(self) -> None:
        self.__characters: tuple[ICharacter, ...]

    def _set_characters(self, characters: tuple[ICharacter, ...]) -> None:
        self.__characters = characters

    @classmethod
    def create_new(cls) -> ITeamBuilder:
        new_team = cls.__new__(cls)
        new_team._init()
        return _TeamBuilder(new_team)

    @property
    def characters(self) -> tuple[ICharacter, ...]:
        return tuple(self.__characters)


class _TeamBuilder(ITeamBuilder):
    """Builder that helps to create a Team"""

    def __init__(self, team: Team) -> None:
        self.__team = team
        self.__characters: list[ICharacter] = []

    def add_character(self, character: ICharacter) -> ITeamBuilder:
        self.__characters.append(character)
        return self

    def build(self) -> ITeam:
        if len(self.__characters) == 0:
            raise ValueError("Team should have at least one Character.")
        self.__team._set_characters(tuple(self.__characters))
        return self.__team
