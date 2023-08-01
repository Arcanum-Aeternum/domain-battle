from abc import ABCMeta, abstractmethod
from typing import Callable

from domain.character import ICharacterPublicMethods
from domain.interfaces import EventDispatcher, IEntityID

from .value_objects import IBattleAlliesBuilder, IBattleAlliesPublicMethods, PassTurnAlgorithmEnum


class IBattlePublicMethods(metaclass=ABCMeta):
    """Interface that define the public methods of Battle"""

    @abstractmethod
    async def play(
        self, playing: Callable[[ICharacterPublicMethods, tuple[ICharacterPublicMethods, ...]], None]
    ) -> None:
        ...


class IBattleInitializer(metaclass=ABCMeta):
    """Interface that define the builder method of Battle"""

    @abstractmethod
    def specify_pass_turn_algorithm(self, pass_turn_algorithm: PassTurnAlgorithmEnum) -> IBattlePublicMethods:
        ...


class IBattleBuilder(IBattleInitializer, metaclass=ABCMeta):
    """Interface that defines an easy way to create a Battle with its Battle Allies"""

    @abstractmethod
    def add_battle_allies_builder(
        self, build_battle_allies: Callable[[IBattleAlliesBuilder], IBattleAlliesPublicMethods]
    ) -> "IBattleBuilder":
        ...

    @abstractmethod
    def add_battle_allies(self, battle_allies: IBattleAlliesPublicMethods) -> "IBattleBuilder":
        ...


class IBattle(IBattlePublicMethods, metaclass=ABCMeta):
    """Interface that define the public methods of Battle"""

    @abstractmethod
    def create_new(
        self, *, event_dispatcher: EventDispatcher, entity_id: IEntityID, is_battle_ongoing: bool
    ) -> "IBattleBuilder":
        ...
