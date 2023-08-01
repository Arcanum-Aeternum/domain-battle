from abc import ABCMeta, abstractmethod

from domain.interfaces import IEntityID


class ICharacterSpellPublicMethods(metaclass=ABCMeta):
    """Interface that defines the public methods in CharacterSpell"""

    entity_id: IEntityID

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        ...

    @property
    @abstractmethod
    def damage(self) -> int:
        ...

    @property
    @abstractmethod
    def mana_cost(self) -> int:
        ...

    @abstractmethod
    def cast_spell(self) -> None:
        ...

    @abstractmethod
    def load_spell(self) -> None:
        ...


class ISpellProfileBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to create a CharacterSpell with its SpellProfile"""

    @abstractmethod
    def specify_spell_properties(
        self,
        mana_cost: int,
        damage: int,
        cooldown: int,
        loading_time: int = 0,
    ) -> ICharacterSpellPublicMethods:
        ...


class ICharacterSpell(metaclass=ABCMeta):
    """Interface that define the public methods of CharacterSpell with exception of factory methods"""

    @abstractmethod
    def create_new(self, *, entity_id: IEntityID, name: str) -> ISpellProfileBuilder:
        ...
