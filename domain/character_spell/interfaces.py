from abc import ABCMeta, abstractmethod

from domain.character import IExpectedCharacterSpell
from domain.interfaces import IEntityID


class ICharacterSpell(IExpectedCharacterSpell, metaclass=ABCMeta):
    """Interface that define the public methods of CharacterSpell with exception of factory methods"""

    @abstractmethod
    def create_new(self, *, entity_id: IEntityID, name: str) -> "ISpellProfileBuilder":
        ...


class ISpellProfileBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to create a CharacterSpell with its SpellProfile"""

    @abstractmethod
    def specify_spell_properties(
        self,
        *,
        mana_cost: int,
        damage: int,
        cooldown: int,
        loading_time: int = 0,
    ) -> ICharacterSpell:
        ...
