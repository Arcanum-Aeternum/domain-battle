from domain import EventDispatcher

from .events import CharacterLostBattleEvent, CharacterWonBattleEvent
from .mediator import CharacterLostBattleMediator, CharacterWonBattleMediator


class EventFactory:
    """Factory that creates Event Mediators"""

    def __init__(self, event_dispatcher: EventDispatcher) -> None:
        self.event_dispatcher = event_dispatcher

    async def __aenter__(self) -> "EventFactory":
        return self

    async def __aexit__(self, *_: Exception) -> None:
        await self.event_dispatcher.notify_all()

    def __enter__(self) -> "EventFactory":
        return self

    def __exit__(self, *_: Exception) -> None:
        ...

    def character_won_battle(self, character_name: str) -> None:
        """Create an Event Handler"""
        event = CharacterWonBattleEvent(character_name)
        self.event_dispatcher.register(CharacterWonBattleMediator(event))

    def character_lost_battle(self, character_name: str) -> None:
        """Create an Event Handler"""
        event = CharacterLostBattleEvent(character_name)
        self.event_dispatcher.register(CharacterLostBattleMediator(event))
