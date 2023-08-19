from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Type

BASIC_TYPES = int | str | bool | float


class DomainEvent(metaclass=ABCMeta):
    """Interface used as a marker for domain events"""

    @dataclass
    class Payload:
        """Payload of the event"""

    event_name: str
    payload: Payload

    def __init_subclass__(cls) -> None:
        cls.event_name = cls.__name__

    def __init__(self, **payload: BASIC_TYPES | dict[str, BASIC_TYPES]) -> None:
        self.payload = self.Payload()
        self.include_payload(**payload)
        self.set_timestamp()

    def include_payload(self, **payload: BASIC_TYPES | dict[str, BASIC_TYPES]) -> None:
        """Set the payload of the event"""
        for key, value in payload.items():
            setattr(self.payload, key, value)

    def set_timestamp(self) -> None:
        """Set the timestamp of the event"""
        self.timestamp = datetime.now().timestamp()


class EventHandler(metaclass=ABCMeta):
    """Interface used as a marker for event handlers"""

    def __init__(self, event: DomainEvent) -> None:
        self.__event = event

    @property
    def event(self) -> DomainEvent:
        return self.__event

    @abstractmethod
    async def handle(self) -> None:
        """Handle the event"""


class EventMediator(EventHandler, metaclass=ABCMeta):
    """Interface used as a marker for event mediators"""

    event_name: str

    def __init__(self, event: DomainEvent) -> None:
        super().__init__(event)
        self.event_name = event.event_name

    @abstractmethod
    def unregister(self, event_handler: Type[EventHandler]) -> None:
        """Unregister an Event Handler to the Event"""

    @abstractmethod
    def unregister_all(self) -> None:
        """Unregister all Event Handlers"""


class EventDispatcher(metaclass=ABCMeta):
    """Interface used as a marker for event dispatchers"""

    events: list[EventMediator]

    @abstractmethod
    def has(self, event: Type[DomainEvent]) -> bool:
        """Check if an Event is registered"""

    @abstractmethod
    def was_dispatched(self, event: Type[DomainEvent]) -> bool:
        """Return the list of dispatched events"""

    @abstractmethod
    def register(self, event_mediator: EventMediator) -> None:
        """Register an Event Handler to an Event"""

    @abstractmethod
    def unregister(self, event: DomainEvent, event_handler: Type[EventHandler]) -> None:
        """Unregister an Event Handler to an Event"""

    @abstractmethod
    def unregister_all(self) -> None:
        """Unregister all Events"""

    @abstractmethod
    async def notify(self, event: DomainEvent) -> None:
        """Notify Event Handlers bounded to the Event"""

    @abstractmethod
    async def notify_all(self) -> None:
        """Notify all Event Handlers not matter the triggered Event"""

    @abstractmethod
    def _pop_event(self, event_index: int) -> EventMediator:
        """Unregister an entire Event"""


class ValueObject(metaclass=ABCMeta):
    """Abstraction used as a marker for value objects"""

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ValueObject):
            return False
        self_attributes = vars(self)
        other_attributes = vars(other)
        return self_attributes == other_attributes

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, ValueObject):
            return False
        return not self == other


class IEntityID(ValueObject, metaclass=ABCMeta):
    """Abstraction that defines mandatory methods for concretes of EntityID"""


class Entity(metaclass=ABCMeta):
    """Abstraction used as a marker for entities"""

    def __init__(self, entity_id: IEntityID) -> None:
        self.entity_id = entity_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity) and not isinstance(other, IEntityID):
            return False
        if isinstance(other, IEntityID):
            return self.entity_id == other
        return self.entity_id == other.entity_id

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False
        return not self == other


class AggregateRoot(Entity, metaclass=ABCMeta):
    """Interface used as a marker for entities that are the root of the aggregate"""

    def __init__(self, event_dispatcher: EventDispatcher, entity_id: IEntityID) -> None:
        super().__init__(entity_id)
        self._event_dispatcher = event_dispatcher


class DomainService(metaclass=ABCMeta):
    """Interface used as a marker for domain services"""
