from typing import Callable

from domain.battle.value_objects.interfaces import IBattleAlliesBuilder, ITeamPublicMethods
from domain.interfaces import ValueObject

from .interfaces import (
    IBattleAllies,
    IBattleAlliesBuilder,
    IBattleAlliesPublicMethods,
    ITeamBuilder,
    ITeamPublicMethods,
)
from .team import Team


class BattleAllies(ValueObject, IBattleAllies):
    """Value Object that represents the Battle Allies"""

    def __init__(self) -> None:
        raise NotImplementedError("This class should not be instantiated directly.")

    def _init(self) -> None:
        self.__teams: tuple[ITeamPublicMethods, ...]

    def _set_teams(self, teams: tuple[ITeamPublicMethods, ...]) -> None:
        self.__teams = teams

    @classmethod
    def create_new(cls) -> IBattleAlliesBuilder:
        new_battle_allies = cls.__new__(cls)
        new_battle_allies._init()
        return _BattleAlliesBuilder(new_battle_allies)

    @property
    def teams(self) -> tuple[ITeamPublicMethods, ...]:
        return tuple(self.__teams)


class _BattleAlliesBuilder(IBattleAlliesBuilder):
    def __init__(self, battle_allies: BattleAllies) -> None:
        self.__battle_allies = battle_allies
        self.__teams: list[ITeamPublicMethods] = []

    def add_team_builder(self, build_team: Callable[[ITeamBuilder], ITeamPublicMethods]) -> IBattleAlliesBuilder:
        team_builder = Team.create_new()
        team = build_team(team_builder)
        self.__teams.append(team)
        return self

    def add_team(self, team: ITeamPublicMethods) -> IBattleAlliesBuilder:
        self.__teams.append(team)
        return self

    def build(self) -> IBattleAlliesPublicMethods:
        if len(self.__teams) == 0:
            raise ValueError("Battle Allies should have at least one Team.")
        self.__battle_allies._set_teams(tuple(self.__teams))
        return self.__battle_allies
