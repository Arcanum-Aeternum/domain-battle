from domain import DomainEvent


class CharacterWonBattleEvent(DomainEvent):
    """Event that notifies that a Character won the Battle"""

    def __init__(self, character_name: str) -> None:
        super().__init__(character_name=character_name)


class CharacterLostBattleEvent(DomainEvent):
    """Event that notifies that a Character won the Battle"""

    def __init__(self, character_name: str) -> None:
        super().__init__(character_name=character_name)
