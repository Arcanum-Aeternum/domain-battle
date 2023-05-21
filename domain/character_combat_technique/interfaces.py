from abc import ABCMeta, abstractmethod

from domain.character import IExpectedCharacterCombatTechnique
from domain.interfaces import IEntityID


class ICharacterCombatTechnique(IExpectedCharacterCombatTechnique, metaclass=ABCMeta):
    """Interface that define the public methods of CharacterCombatTechnique with exception of factory methods"""

    @abstractmethod
    def create_new(self, *, entity_id: IEntityID, name: str) -> "ICombatTechniqueProfileBuilder":
        ...


class ICombatTechniqueProfileBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to create a CharacterCombatTechnique with its CombatTechniqueProfile"""

    @abstractmethod
    def specify_combat_technique_properties(
        self,
        *,
        stamina_cost: int,
        damage: int,
        cooldown: int,
        loading_time: int = 0,
    ) -> ICharacterCombatTechnique:
        ...
