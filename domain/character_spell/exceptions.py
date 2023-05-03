class SpellIsNotReady(RuntimeError):
    """Error indicates that someone tried to cast a spell that was not ready"""


class InvalidCooldownRange(RuntimeError):
    """Error indicates past cooldown is too high, none or negative"""


class InvalidLoadingTimeRange(RuntimeError):
    """Error indicates loading time is greater than cooldown or negative"""


class SpellIsAlreadyReady(RuntimeError):
    """Error indicates that someone tried to load a ready-made spell"""


class InvalidManaCostRange(RuntimeError):
    """Error indicates that the mana cost range is invalid (less than zero or greater than 100)"""


class InvalidDamageRange(RuntimeError):
    """Error indicates that the damage range is invalid (less than zero or greater than 100)"""
