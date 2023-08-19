from abc import ABCMeta, abstractmethod

from domain import IEntityID
from domain.skill import IPhysicalAttack


class ICombatTechnique(IPhysicalAttack, metaclass=ABCMeta):
    """Interface that defines the public methods in CombatTechnique"""


class ICombatTechniqueProfileBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to create a CombatTechnique with its CombatTechniqueProfile"""

    @abstractmethod
    def specify_combat_technique_properties(
        self,
        stamina_cost: int,
        damage: int,
        cooldown: int,
        loading_time: int = 0,
    ) -> ICombatTechnique:
        ...


class ICombatTechniqueFactory(metaclass=ABCMeta):
    """Interface that define the factory methods of CombatTechnique"""

    @abstractmethod
    def create_new(self, *, entity_id: IEntityID, name: str) -> ICombatTechniqueProfileBuilder:
        ...
