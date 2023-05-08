class BattleIsAlreadyHappeningException(RuntimeError):
    """Error indicates that someone tried to start a duel that was already running"""


class BattleIsNotHappeningException(RuntimeError):
    """Error indicates that someone tried to end a duel that had not been started yet"""
