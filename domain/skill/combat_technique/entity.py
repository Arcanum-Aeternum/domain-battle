"""Module describes the Spell entity and its direct dependencies"""
from typing import Callable

from domain import Entity, IEntityID

from .interfaces import ICombatTechnique, ICombatTechniqueFactory, ICombatTechniqueProfileBuilder
from .value_objects import CombatTechniqueProfile


class CombatTechnique(Entity, ICombatTechniqueFactory, ICombatTechnique):
    """Class that represents a CombatTechnique entity"""

    def __init__(self) -> None:
        raise RuntimeError("Cannot instantiate directly")

    def _init(self, entity_id: IEntityID, name: str) -> None:
        super().__init__(entity_id)
        self.__name = name

    def _set_combat_technique_profile(self, combat_technique_profile: CombatTechniqueProfile) -> None:
        self.__combat_technique_profile = combat_technique_profile

    @classmethod
    def create_new(cls, *, entity_id: IEntityID, name: str) -> ICombatTechniqueProfileBuilder:
        new_spell = cls.__new__(cls)
        new_spell._init(entity_id, name)
        return _SpellProfileBuilder(new_spell, new_spell._set_combat_technique_profile)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def is_ready(self) -> bool:
        return self.__combat_technique_profile.is_ready

    @property
    def damage(self) -> int:
        return self.__combat_technique_profile.damage

    @property
    def cost(self) -> int:
        return self.__combat_technique_profile.stamina_cost

    def use(self) -> None:
        self.__combat_technique_profile.start_loading_time()

    def rest(self) -> None:
        self.__combat_technique_profile.rest()


class _SpellProfileBuilder(ICombatTechniqueProfileBuilder):
    def __init__(
        self,
        spell_obj: CombatTechnique,
        func_set_spell_profile: Callable[[CombatTechniqueProfile], None],
    ) -> None:
        self.__func_set_spell_profile = func_set_spell_profile
        self.__spell_obj = spell_obj

    def specify_combat_technique_properties(
        self,
        stamina_cost: int,
        damage: int,
        cooldown: int,
        loading_time: int = 0,
    ) -> ICombatTechnique:
        spell_profile = CombatTechniqueProfile(
            stamina_cost=stamina_cost,
            damage=damage,
            cooldown=cooldown,
            loading_time=loading_time,
        )
        self.__func_set_spell_profile(spell_profile)
        return self.__spell_obj
