from abc import ABCMeta, abstractmethod

from domain import IEntityID
from domain.skill import IMagicalAttack


class ISpell(IMagicalAttack, metaclass=ABCMeta):
    """Interface that defines the public methods in Spell"""


class ISpellProfileBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to create a Spell with its SpellProfile"""

    @abstractmethod
    def specify_spell_properties(
        self,
        mana_cost: int,
        damage: int,
        cooldown: int,
        loading_time: int = 0,
    ) -> ISpell:
        ...


class ISpellFactory(metaclass=ABCMeta):
    """Interface that define the public methods of Spell with exception of factory methods"""

    @abstractmethod
    def create_new(self, *, entity_id: IEntityID, name: str) -> ISpellProfileBuilder:
        ...
