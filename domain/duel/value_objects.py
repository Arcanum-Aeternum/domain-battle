from abc import ABCMeta, abstractmethod
from queue import Queue
from typing import Callable, Dict

from domain import ValueObject
from domain.value_objects import EntityID


class TurnQueueBuilder(metaclass=ABCMeta):
    """Interface that define an easy way to consume some Turn Queue"""

    @abstractmethod
    def __init__(self, turn_queue_instance: "TurnQueue") -> None:
        ...

    @abstractmethod
    def add_player(self, player: EntityID) -> "TurnQueueBuilder":
        ...


class TurnQueue(metaclass=ABCMeta):
    """Interface that represents the minimum that a turn queue needs to have"""

    @abstractmethod
    def __init__(self, players_quantity: int) -> None:
        ...

    @abstractmethod
    def add_player(self, player: EntityID) -> TurnQueueBuilder:
        """Factory method that offers an easy way to mount the Turn Queue from an Turn Queue Builder"""

    @abstractmethod
    def advance_turn(self) -> EntityID:
        """Advances to the next turn, takes the first placed in the queue,
        puts it at the end and returns it
        """

    @abstractmethod
    def show_players_order(self) -> tuple[EntityID, ...]:
        """Shows the order in which dueling players can play"""

    @property
    @abstractmethod
    def is_all_players_in_queue(self) -> bool:
        """Return True if the Turn Queue has all players (queue is full) else False"""


class TurnCircularQueue(TurnQueue):
    """Circular Queue that can be used to represent the order of players in duel"""

    __builder_cache: Dict["TurnCircularQueue", TurnQueueBuilder] = {}

    def __init__(self, *, players_quantity: int) -> None:
        self.__queue: Queue = Queue(maxsize=players_quantity)

    def add_player(self, player: EntityID) -> TurnQueueBuilder:
        if self.is_all_players_in_queue:
            raise TypeError()
        if self not in self.__builder_cache:
            new_builder = self.__BuildTurnQueue(turn_queue_instance=self, put_method=self.__queue.put)
            self.__builder_cache[self] = new_builder
        builder = self.__builder_cache[self]
        builder.add_player(player=player)
        return builder

    class __BuildTurnQueue(TurnQueueBuilder):
        """Builder that provides an easy way to put players in the queue"""

        def __init__(self, *, turn_queue_instance: "TurnCircularQueue", put_method: Callable[[EntityID], None]) -> None:
            self.__turn_queue_instance = turn_queue_instance
            self.__put_to_queue = put_method

        def add_player(self, player: EntityID) -> TurnQueueBuilder:
            """Enqueue player on next available position of turn queue"""
            if self.__turn_queue_instance.is_all_players_in_queue:
                raise TypeError()
            self.__put_to_queue(player)
            return self

    @property
    def is_all_players_in_queue(self) -> bool:
        return self.__queue.full()

    def advance_turn(self) -> EntityID:
        if not self.is_all_players_in_queue:
            raise TypeError()
        player = self.__queue.get()
        self.__queue.put(player)
        return player

    def show_players_order(self) -> tuple[EntityID, ...]:
        if not self.is_all_players_in_queue:
            raise TypeError()
        players_in_order: list[EntityID] = list(self.__queue.queue)
        return tuple(players_in_order)


class TurnControl(ValueObject, metaclass=ABCMeta):
    """Class that represents a value object of players in duel"""

    @abstractmethod
    def advance_turn(self) -> None:
        """Pass turn to the next player"""

    @abstractmethod
    def show_players_order(self) -> tuple[EntityID, ...]:
        """Shows the order in which dueling players can play"""

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...


class TurnControlFor1x1Duel(TurnControl):
    """Class that represents a value object of players in a 1x1 duel"""

    def __init__(self, *, turn_queue: TurnQueue) -> None:
        if len(turn_queue.show_players_order()) != 2 or not turn_queue.is_all_players_in_queue:
            raise TypeError("Either the <class of TurnQueue> has invalid number of players or it's not ready")
        self._turn_queue = turn_queue

    def advance_turn(self) -> None:
        self._turn_queue.advance_turn()

    def show_players_order(self) -> tuple[EntityID, ...]:
        return self._turn_queue.show_players_order()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return all(
            self_entity_id == other_entity_id
            for self_entity_id, other_entity_id in zip(
                self.show_players_order(),
                other.show_players_order(),
            )
        )
