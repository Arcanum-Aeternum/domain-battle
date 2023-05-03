class DuelIsAlreadyHappeningException(RuntimeError):
    """Error indicates that someone tried to start a duel that was already running"""


class DuelIsNotHappeningException(RuntimeError):
    """Error indicates that someone tried to end a duel that had not been started yet"""


class OnlyTwoPlayerDuelAllowedException(RuntimeError):
    """Error indicates that someone tried to start a duel with more or less than 2 players"""
