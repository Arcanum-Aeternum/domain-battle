from contextlib import suppress
from typing import Type

from trio import open_nursery

from domain import DomainEvent, EventDispatcher, EventHandler, EventMediator


class BattleEventDispatcher(EventDispatcher):
    """Battle Event Dispatcher"""

    def __init__(self) -> None:
        self.events_mediators: list[EventMediator] = []
        self.__dispatched_events: list[EventMediator] = []

    def has(self, event: Type[DomainEvent]) -> bool:
        """Check if an Event is registered"""
        return event.event_name in [event_mediator.event_name for event_mediator in self.events_mediators]

    def was_dispatched(self, event: Type[DomainEvent]) -> bool:
        return event.event_name in [event_mediator.event_name for event_mediator in self.__dispatched_events]

    def dispatched_events(self) -> list[EventMediator]:
        """Return the list of dispatched events"""
        return self.__dispatched_events

    def register(self, event_mediator: EventMediator) -> None:
        """Register an Event Handler to an Event"""
        if event_mediator.event_name not in [event.event_name for event in self.events_mediators]:
            self.events_mediators.append(event_mediator)

    def unregister(self, event: DomainEvent, event_handler: Type[EventHandler]) -> None:
        """Unregister an Event Handler to an Event"""
        with suppress(StopIteration):
            event_mediator = next(
                event_mediator
                for event_mediator in self.events_mediators
                if event_mediator.event_name == event.event_name
            )
            event_mediator.unregister(event_handler)

    def unregister_all(self) -> None:
        """Unregister all Events"""
        self.events_mediators.clear()

    async def notify(self, event: DomainEvent) -> None:
        """Notify all Event Handlers of an Event"""
        with suppress(StopIteration):
            event_data = next(
                (event_index, event_mediator)
                for event_index, event_mediator in enumerate(self.events_mediators)
                if event_mediator.event_name == event.event_name
            )
            event_mediator = event_data[1]
            await event_mediator.handle()
            event_index = event_data[0]
            self.__unqueue_event(event_index)

    async def notify_all(self) -> None:
        """Notify all Event Handlers of a list of Events"""
        async with open_nursery() as nursery:
            for event_index, event_mediator in enumerate(self.events_mediators):
                nursery.start_soon(event_mediator.handle)
                self.__unqueue_event(event_index)

    def _pop_event(self, event_index: int) -> EventMediator:
        """Unregister an entire Event"""
        return self.events_mediators.pop(event_index)

    def __unqueue_event(self, event_index: int) -> None:
        self.__dispatched_events.append(self._pop_event(event_index))
