from typing import Callable

from domain.interfaces import ValueObject

from .interfaces import IBattleAllies, IBattleAlliesBuilder, IBattleAlliesFactory, ITeam, ITeamBuilder
from .team import Team


class BattleAllies(ValueObject, IBattleAlliesFactory, IBattleAllies):
    """Value Object that represents the Battle Allies"""

    def __init__(self) -> None:
        raise NotImplementedError("This class should not be instantiated directly.")

    def _init(self) -> None:
        self.__teams: tuple[ITeam, ...]

    def _set_teams(self, teams: tuple[ITeam, ...]) -> None:
        self.__teams = teams

    @classmethod
    def create_new(cls) -> IBattleAlliesBuilder:
        new_battle_allies = cls.__new__(cls)
        new_battle_allies._init()
        return _BattleAlliesBuilder(new_battle_allies)

    @property
    def teams(self) -> tuple[ITeam, ...]:
        return tuple(self.__teams)


class _BattleAlliesBuilder(IBattleAlliesBuilder):
    def __init__(self, battle_allies: BattleAllies) -> None:
        self.__battle_allies = battle_allies
        self.__teams: list[ITeam] = []

    def add_team_builder(self, build_team: Callable[[ITeamBuilder], ITeam]) -> IBattleAlliesBuilder:
        team_builder = Team.create_new()
        team = build_team(team_builder)
        self.__teams.append(team)
        return self

    def add_team(self, team: ITeam) -> IBattleAlliesBuilder:
        self.__teams.append(team)
        return self

    def build(self) -> IBattleAllies:
        if len(self.__teams) == 0:
            raise ValueError("Battle Allies should have at least one Team.")
        self.__battle_allies._set_teams(tuple(self.__teams))
        return self.__battle_allies
