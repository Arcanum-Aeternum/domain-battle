from abc import ABCMeta, abstractmethod

from domain.interfaces import IEntityID


class ICharacterCombatTechniquePublicMethods(metaclass=ABCMeta):
    """Interface that defines the public methods in CharacterCombatTechnique"""

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
    def stamina_cost(self) -> int:
        ...

    @abstractmethod
    def apply_combat_technique(self) -> None:
        ...

    @abstractmethod
    def rest_and_prepare(self) -> None:
        ...


class ICombatTechniqueProfileBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to create a CharacterCombatTechnique with its CombatTechniqueProfile"""

    @abstractmethod
    def specify_combat_technique_properties(
        self,
        stamina_cost: int,
        damage: int,
        cooldown: int,
        loading_time: int = 0,
    ) -> ICharacterCombatTechniquePublicMethods:
        ...


class ICharacterCombatTechnique(metaclass=ABCMeta):
    """Interface that define the factory methods of CharacterCombatTechnique"""

    @abstractmethod
    def create_new(self, *, entity_id: IEntityID, name: str) -> ICombatTechniqueProfileBuilder:
        ...
