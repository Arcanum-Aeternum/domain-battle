from abc import ABCMeta, abstractmethod
from typing import Callable

from domain import EventDispatcher, IEntityID

from .value_objects import IBattleAllies, IBattleAlliesBuilder, IMoveBuilder, PassTurnAlgorithmEnum


class IBattle(metaclass=ABCMeta):
    """Interface that define the public methods of Battle"""

    entity_id: IEntityID

    @abstractmethod
    async def play(self, build_playing_move: Callable[[IMoveBuilder], None]) -> None:
        ...


class IBattleInitializer(metaclass=ABCMeta):
    """Interface that define the builder method of Battle"""

    @abstractmethod
    def specify_pass_turn_algorithm(self, pass_turn_algorithm: PassTurnAlgorithmEnum) -> IBattle:
        ...


class IBattleBuilder(IBattleInitializer, metaclass=ABCMeta):
    """Interface that defines an easy way to create a Battle with its Battle Allies"""

    @abstractmethod
    def add_battle_allies_builder(
        self, build_battle_allies: Callable[[IBattleAlliesBuilder], IBattleAllies]
    ) -> "IBattleBuilder":
        ...

    @abstractmethod
    def add_battle_allies(self, battle_allies: IBattleAllies) -> "IBattleBuilder":
        ...


class IBattleFactory(metaclass=ABCMeta):
    """Interface that define the public methods of Battle"""

    @abstractmethod
    def create_new(
        self, *, event_dispatcher: EventDispatcher, entity_id: IEntityID, is_battle_ongoing: bool
    ) -> "IBattleBuilder":
        ...
