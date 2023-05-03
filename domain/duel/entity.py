"""Module describes the Duel root entity and its direct dependencies"""
from typing import Callable

from domain.character.interfaces import ICharacter
from domain.interfaces import AggregateRoot
from domain.value_objects import EntityID

from .exceptions import DuelIsAlreadyHappeningException, DuelIsNotHappeningException


class Duel(AggregateRoot):
    """Class that represents a Duel entity, which is the aggregate root"""

    def __init__(
        self,
        *,
        entity_id: EntityID,
        players: tuple[ICharacter, ...],
        is_happening: bool = False,
    ) -> None:
        super().__init__(entity_id)
        self.__players = players
        self.__current_player = 0
        self.__is_happening = is_happening
        self.__reason_for_ending = ""

    def is_current_player(self, *, player: ICharacter) -> bool:
        return self.__players[self.__current_player] == player

    def init_duel(self) -> None:
        """Changes attribute if it has not yet been started, indicating the start of the duel"""
        if self.__is_happening:
            raise DuelIsAlreadyHappeningException()
        self.__is_happening = True

    def play(self, *, playing: Callable[[ICharacter, ICharacter], None]) -> None:
        """Pass the turn to the other player"""
        if not self.__is_happening:
            raise DuelIsNotHappeningException()
        current_player = self.__players[self.__current_player]
        next_player = self.__players[(self.__current_player + 1) % 2]
        playing(current_player, next_player)
        self.__current_player = (self.__current_player + 1) % 2

    def finish_duel(self, *, reason_for_ending: str) -> None:
        """Ends the duel if the same is happening, indicating its end"""
        if not self.__is_happening:
            raise DuelIsNotHappeningException()
        self.__is_happening = False
        self.__reason_for_ending = reason_for_ending

    def __str__(self) -> str:
        if self.__is_happening:
            return f"""<Duel(
                id={self.entity_id},
                players={str(self.__players)},
                current_player={self.__players[self.__current_player]}
            )>
            """
        return f"<Duel(id={self.entity_id}, reason_for_ending={self.__reason_for_ending})>"
