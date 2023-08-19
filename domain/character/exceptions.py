class CharacterDoesNotHaveThatSkillException(RuntimeError):
    """Error that indicates that the character does not have the skill he tried to use"""


class SkillNotAvailableException(RuntimeError):
    """Error that indicates that the requested skill is on cooldown"""


class CantUseThisSkillToAttackException(RuntimeError):
    """Error that indicates that the character can't use this skill to attack"""


class NoCombatTechniqueAvailableException(RuntimeError):
    """Error indicates that someone tried to use a combat technique that was not available"""


class NoSpellAvailableException(RuntimeError):
    """Error indicates that someone tried to use a spell that was not available"""
