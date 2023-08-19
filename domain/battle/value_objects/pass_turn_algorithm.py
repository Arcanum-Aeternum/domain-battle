from abc import ABCMeta
from typing import Type

from domain.character import ICharacter

from .interfaces import IBattleAllies, IPassTurnAlgorithm, ITeam, PassTurnAlgorithmEnum

StaticCharacterPosition = dict[int, ICharacter]
StaticTeamPosition = dict[int, StaticCharacterPosition]
StaticBattleAlliesPosition = dict[int, StaticTeamPosition]


class _BasePassTurnAlgorithm(IPassTurnAlgorithm, metaclass=ABCMeta):
    """Base class that implements the main public methods of a PassTurnAlgorithm."""

    def __init__(self, participants_battle_allies: tuple[IBattleAllies, ...]) -> None:
        self._current_turn = (0, 0, 0)
        self._playing_battle_allies = 0
        self._static_turn_positions: StaticBattleAlliesPosition = {
            index: self.__organize_team_positions(battle_allies)
            for index, battle_allies in enumerate(participants_battle_allies)
        }

    @property
    def current_character(self) -> ICharacter:
        return self._static_turn_positions[self._current_turn[0]][self._current_turn[1]][self._current_turn[2]]

    @property
    def enemies(self) -> tuple[ICharacter, ...]:
        enemies_groups = self._static_turn_positions.copy()
        enemies_groups.pop(self._playing_battle_allies)
        return tuple(
            enemy
            for enemy_teams in enemies_groups.values()
            for enemies in enemy_teams.values()
            for enemy in enemies.values()
            if enemy.is_alive
        )

    @property
    def finalists(self) -> tuple[tuple[ICharacter, ...], tuple[ICharacter, ...]] | None:
        alive_battle_allies_indexes = [
            battle_allies_index
            for battle_allies_index, static_battle_allies in self._static_turn_positions.items()
            if self.__is_battle_allies_alive(static_battle_allies)
        ]
        if len(alive_battle_allies_indexes) != 1:
            return None
        losers_battle_allies = self._static_turn_positions.copy()
        alive_battle_allies = losers_battle_allies.pop(alive_battle_allies_indexes[0])
        winners_characters = tuple(character for team in alive_battle_allies.values() for character in team.values())
        losers_characters = tuple(
            character for team in alive_battle_allies.values() for character in team.values() if not character.is_alive
        )
        return (winners_characters, losers_characters)

    def __is_battle_allies_alive(self, static_battle_allies: StaticTeamPosition) -> bool:
        return any(character.is_alive for team in static_battle_allies.values() for character in team.values())

    def __organize_team_positions(self, battle_allies: IBattleAllies) -> StaticTeamPosition:
        static_team_position: StaticTeamPosition = {}
        for team_index, team in enumerate(battle_allies.teams):
            static_team_position[team_index] = self.__organize_character_positions(team)
        return static_team_position

    def __organize_character_positions(self, team: ITeam) -> StaticCharacterPosition:
        static_character_position: StaticCharacterPosition = {}
        for character_index, character in enumerate(team.characters):
            static_character_position[character_index] = character
        return static_character_position


class RegularPassTurn(_BasePassTurnAlgorithm):
    """Class that implements the regular circular queue algorithm"""

    def next_turn(self) -> tuple[ICharacter, tuple[ICharacter, ...]]:
        self._playing_battle_allies = self._current_turn[0]
        character = self.current_character
        next_battle_allies = (self._current_turn[0] + 1) % len(self._static_turn_positions)
        next_team = (
            (self._current_turn[1] + 1) % len(self._static_turn_positions[0])
            if next_battle_allies == 0
            else self._current_turn[1]
        )
        next_character = (
            (self._current_turn[2] + 1) % len(self._static_turn_positions[0][0])
            if next_team == 0 and next_battle_allies == 0
            else self._current_turn[2]
        )
        self._current_turn = (next_battle_allies, next_team, next_character)
        return (character, self.enemies)


class JumpNextPassTurn(_BasePassTurnAlgorithm):
    """Class that implements the jump next pass turn algorithm"""

    def next_turn(self) -> tuple[ICharacter, tuple[ICharacter, ...]]:
        next_battle_allies = self._current_turn[0] + 2 % len(self._static_turn_positions)
        next_team = self._current_turn[1] + 1 % len(self._static_turn_positions[0])
        next_character = self._current_turn[2] + 1 % len(self._static_turn_positions[0][0])
        character = self.current_character
        self._current_turn = (next_battle_allies, next_team, next_character)
        return (character, self.enemies)


class PassTurnAlgorithmStrategy(IPassTurnAlgorithm):
    """Class that implements the Strategy Pattern to define the algorithm of a PassTurnAlgorithm"""

    __pass_turn_algorithm_cache: dict[PassTurnAlgorithmEnum, IPassTurnAlgorithm] = {}
    __available_algorithms: dict[PassTurnAlgorithmEnum, Type[_BasePassTurnAlgorithm]] = {
        PassTurnAlgorithmEnum.REGULAR_PASS_TURN: RegularPassTurn,
        PassTurnAlgorithmEnum.JUMP_TO_THE_NEXT_PASS_TURN_ALGORITHM: JumpNextPassTurn,
    }

    def __init__(
        self,
        pass_turn_algorithm_enum: PassTurnAlgorithmEnum,
        participants_battle_allies: tuple[IBattleAllies, ...],
    ) -> None:
        self.__pass_turn_algorithm_enum = pass_turn_algorithm_enum
        self.__participants_battle_allies = participants_battle_allies

    @property
    def current_character(self) -> ICharacter:
        try:
            self.__singleton_cache(self.__pass_turn_algorithm_enum)
            return self.__pass_turn_algorithm_cache[self.__pass_turn_algorithm_enum].current_character
        except KeyError as error:
            msg = f"Algorithm <{self.__pass_turn_algorithm_enum.value}> is not available"
            raise NotImplementedError(msg) from error

    @property
    def enemies(self) -> tuple[ICharacter, ...]:
        try:
            self.__singleton_cache(self.__pass_turn_algorithm_enum)
            return self.__pass_turn_algorithm_cache[self.__pass_turn_algorithm_enum].enemies
        except KeyError as error:
            msg = f"Algorithm <{self.__pass_turn_algorithm_enum.value}> is not available"
            raise NotImplementedError(msg) from error

    @property
    def finalists(self) -> tuple[tuple[ICharacter, ...], tuple[ICharacter, ...]] | None:
        try:
            self.__singleton_cache(self.__pass_turn_algorithm_enum)
            return self.__pass_turn_algorithm_cache[self.__pass_turn_algorithm_enum].finalists
        except KeyError as error:
            msg = f"Algorithm <{self.__pass_turn_algorithm_enum.value}> is not available"
            raise NotImplementedError(msg) from error

    def next_turn(self) -> tuple[ICharacter, tuple[ICharacter, ...]]:
        try:
            self.__singleton_cache(self.__pass_turn_algorithm_enum)
            return self.__pass_turn_algorithm_cache[self.__pass_turn_algorithm_enum].next_turn()
        except KeyError as error:
            msg = f"Algorithm <{self.__pass_turn_algorithm_enum.value}> is not available"
            raise NotImplementedError(msg) from error

    def __singleton_cache(self, pass_turn_algorithm_enum: PassTurnAlgorithmEnum) -> None:
        if pass_turn_algorithm_enum in self.__pass_turn_algorithm_cache:
            return None
        pass_turn_algorithm_class = self.__available_algorithms[pass_turn_algorithm_enum]
        self.__pass_turn_algorithm_cache[pass_turn_algorithm_enum] = pass_turn_algorithm_class(
            self.__participants_battle_allies
        )
