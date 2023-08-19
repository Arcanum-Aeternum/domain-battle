"""Module describes the Battle root entity and its direct dependencies"""
from typing import Callable

from trio import open_nursery
from trio.to_thread import run_sync

from domain.battle.value_objects import IMoveBuilder, Move
from domain.character import ICharacter
from domain.interfaces import AggregateRoot, EventDispatcher, IEntityID
from domain.skill.combat_technique.exceptions import CombatTechniqueIsAlreadyReady
from domain.skill.spell.exceptions import SpellIsAlreadyReady

from .events import EventFactory
from .exceptions import BattleIsAlreadyHappeningException, BattleIsNotHappeningException
from .interfaces import IBattle, IBattleBuilder, IBattleFactory
from .value_objects import (
    BattleAllies,
    IBattleAllies,
    IBattleAlliesBuilder,
    PassTurnAlgorithmEnum,
    PassTurnAlgorithmStrategy,
)


class Battle(AggregateRoot, IBattleFactory, IBattle):
    """Class that represents a Battle entity, which is the aggregate root"""

    def __init__(self) -> None:
        raise NotImplementedError("Cannot instantiate directly")

    def _init(self, event_dispatcher: EventDispatcher, entity_id: IEntityID, is_battle_ongoing: bool) -> None:
        super().__init__(event_dispatcher, entity_id)
        self.__is_battle_ongoing = is_battle_ongoing
        self.__reason_for_ending = ""

    def _init_battle(self) -> None:
        """Changes attribute if it has not yet been started, indicating the start of the Battle"""
        if self.__is_battle_ongoing:
            raise BattleIsAlreadyHappeningException()
        self.__is_battle_ongoing = True

    def _finish_battle(self, reason_for_ending: str) -> None:
        """Ends the Battle if the same is happening, indicating its end"""
        if not self.__is_battle_ongoing:
            raise BattleIsNotHappeningException()
        self.__is_battle_ongoing = False
        self.__reason_for_ending = reason_for_ending

    def _set_specifications(
        self,
        pass_turn_algorithm: PassTurnAlgorithmEnum,
        participants_battle_allies: tuple[IBattleAllies, ...],
    ) -> None:
        self.__pass_turn_algorithm = PassTurnAlgorithmStrategy(pass_turn_algorithm, participants_battle_allies)

    @classmethod
    def create_new(
        cls, *, event_dispatcher: EventDispatcher, entity_id: IEntityID, is_battle_ongoing: bool
    ) -> IBattleBuilder:
        new_battle = cls.__new__(cls)
        new_battle._init(event_dispatcher, entity_id, is_battle_ongoing)
        if not is_battle_ongoing:
            new_battle._init_battle()
        return _BattleSpecificationsBuilder(new_battle)

    async def play(self, build_playing_move: Callable[[IMoveBuilder], None]) -> None:
        """Pass the turn to the other player"""
        if not self.__is_battle_ongoing:
            raise BattleIsNotHappeningException()
        current_character, enemies = self.__pass_turn_algorithm.next_turn()
        move_builder = Move.create_new(current_character, enemies)
        build_playing_move(move_builder)
        async with open_nursery() as nursery:
            nursery.start_soon(self._rest_characters, [current_character, *enemies])
            nursery.start_soon(self._notify)

    async def _rest_characters(self, characters: list[ICharacter]) -> None:
        try:
            async with open_nursery() as nursery:
                for character in characters:
                    nursery.start_soon(run_sync, character.rest)
        except (ExceptionGroup, CombatTechniqueIsAlreadyReady, SpellIsAlreadyReady):
            ...

    async def _notify(self) -> None:
        if finalists := self.__pass_turn_algorithm.finalists:
            self._finish_battle("Winner is found")
            winners_characters = finalists[0]
            losers_characters = finalists[1]
            async with open_nursery() as nursery:
                nursery.start_soon(self.__notify_winning_characters, winners_characters)
                nursery.start_soon(self.__notify_losing_characters, losers_characters)

    async def __notify_winning_characters(self, winning_characters: tuple[ICharacter, ...]) -> None:
        """Notifies the winning characters of the Battle"""
        if self.__is_battle_ongoing:
            raise BattleIsAlreadyHappeningException("Cannot notify winning characters if the battle is ongoing")
        async with EventFactory(self._event_dispatcher) as event_factory:
            for character in winning_characters:
                event_factory.character_won_battle(character.name)

    async def __notify_losing_characters(self, losing_characters: tuple[ICharacter, ...]) -> None:
        """Notifies the losing characters of the Battle"""
        if self.__is_battle_ongoing:
            raise BattleIsAlreadyHappeningException("Cannot notify losing characters if the battle is ongoing")
        async with EventFactory(self._event_dispatcher) as event_factory:
            for character in losing_characters:
                event_factory.character_lost_battle(character.name)

    def __str__(self) -> str:
        if self.__is_battle_ongoing:
            return f"""<{self.__class__.__name__}(id={self.entity_id})> """
        return f"<{self.__class__.__name__}(id={self.entity_id}, reason_for_ending={self.__reason_for_ending})>"


class _BattleSpecificationsBuilder(IBattleBuilder):
    """Class that implements the Builder Pattern to create a Battle with its Ally"""

    def __init__(self, battle: Battle) -> None:
        self.__battle = battle
        self.__participants_battle_allies: list[IBattleAllies] = []

    def add_battle_allies_builder(
        self, build_battle_allies: Callable[[IBattleAlliesBuilder], IBattleAllies]
    ) -> IBattleBuilder:
        new_battle_allies = BattleAllies.create_new()
        builded_battle_allies = build_battle_allies(new_battle_allies)
        self.__participants_battle_allies.append(builded_battle_allies)
        return self

    def add_battle_allies(self, battle_allies: IBattleAllies) -> IBattleBuilder:
        self.__participants_battle_allies.append(battle_allies)
        return self

    def specify_pass_turn_algorithm(self, pass_turn_algorithm: PassTurnAlgorithmEnum) -> IBattle:
        self.__battle._set_specifications(
            pass_turn_algorithm=pass_turn_algorithm,
            participants_battle_allies=tuple(self.__participants_battle_allies),
        )
        return self.__battle
