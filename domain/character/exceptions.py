class ThisCharacterDoesNotHaveThatSpell(RuntimeError):
    """Error that indicates that the character does not have the magic he tried to use"""


class ThisCharacterDoesNotHaveThatCombatTechnique(RuntimeError):
    """Error that indicates that the character does not have the combat technique he tried to use"""


class CombatTechniqueNotAvailable(RuntimeError):
    """Error that indicates that the requested combat technique is on cooldown"""


class SpellNotAvailable(RuntimeError):
    """Error that indicates that the requested spell is on cooldown"""
