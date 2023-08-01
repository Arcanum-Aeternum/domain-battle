from typing import Type

from trio import open_nursery

from domain.interfaces import EventHandler, EventMediator

from .event_handlers import NotifyEvolutionEventHandler, NotifyQuestEventHandler
from .events import CharacterLostBattleEvent, CharacterWonBattleEvent


class CharacterWonBattleMediator(EventMediator):
    """Mediator for character won battle event."""

    def __init__(self, event: CharacterWonBattleEvent) -> None:
        super().__init__(event)
        self.__event = event
        self.__event_handlers: list[Type[EventHandler]] = [NotifyEvolutionEventHandler, NotifyQuestEventHandler]

    async def handle(self) -> None:
        """Handle the event."""
        async with open_nursery() as nursery:
            for handler in self.__event_handlers:
                nursery.start_soon(handler(self.__event).handle)
        self.unregister_all()

    def unregister(self, event_handler: Type[EventHandler]) -> None:
        """Unregister an Event Handler to an Event."""
        self.__event_handlers.remove(event_handler)

    def unregister_all(self) -> None:
        """Unregister all Event Handlers."""
        self.__event_handlers.clear()


class CharacterLostBattleMediator(EventMediator):
    """Mediator for character won battle event."""

    def __init__(self, event: CharacterLostBattleEvent) -> None:
        super().__init__(event)
        self.__event = event
        self.__event_handlers: list[Type[EventHandler]] = [NotifyQuestEventHandler]

    async def handle(self) -> None:
        """Handle the event."""
        async with open_nursery() as nursery:
            for handler in self.__event_handlers:
                nursery.start_soon(handler(self.__event).handle)
        self.unregister_all()

    def unregister(self, event_handler: Type[EventHandler]) -> None:
        """Unregister an Event Handler to an Event."""
        self.__event_handlers.remove(event_handler)

    def unregister_all(self) -> None:
        """Unregister all Event Handlers."""
        self.__event_handlers.clear()
