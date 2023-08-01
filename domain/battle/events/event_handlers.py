from trio import sleep

from domain import EventHandler


class NotifyEvolutionEventHandler(EventHandler):
    """Event Handler that notifies the Evolution when a Character win the Battle"""

    async def handle(self) -> None:
        """Handle the event"""
        await sleep(1)
        print(f"Evolution Context notified: {self.event.event_name}")


class NotifyQuestEventHandler(EventHandler):
    """Event Handler that notifies the Quest when a Character win the Battle"""

    async def handle(self) -> None:
        """Handle the event"""
        await sleep(1)
        print(f"Quest Context notified: {self.event.event_name}")
