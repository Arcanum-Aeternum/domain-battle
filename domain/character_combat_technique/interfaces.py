from abc import ABCMeta

from domain.character import IExpectedCharacterCombatTechnique
from domain.interfaces import Entity


class ICharacterCombatTechnique(Entity, IExpectedCharacterCombatTechnique, metaclass=ABCMeta):
    """Interface that define the public methods of CharacterCombatTechnique with exception of factory methods"""
