from abc import ABCMeta

from domain.character import IExpectedCharacterSpell
from domain.interfaces import Entity


class ICharacterSpell(Entity, IExpectedCharacterSpell, metaclass=ABCMeta):
    """Interface that define the public methods of CharacterSpell with exception of factory methods"""
