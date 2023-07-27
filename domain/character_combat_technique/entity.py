"""Module describes the CharacterSpell entity and its direct dependencies"""
from typing import Callable

from domain.interfaces import Entity, IEntityID

from .interfaces import (
    ICharacterCombatTechnique,
    ICharacterCombatTechniquePublicMethods,
    ICombatTechniqueProfileBuilder,
)
from .value_objects import CombatTechniqueProfile


class CharacterCombatTechnique(Entity, ICharacterCombatTechnique, ICharacterCombatTechniquePublicMethods):
    """Class that represents a CharacterCombatTechnique entity"""

    def __init__(self) -> None:
        raise RuntimeError("Cannot instantiate directly")

    def _init(self, entity_id: IEntityID, name: str) -> None:
        super().__init__(entity_id)
        self.__name = name

    def _set_combat_technique_profile(self, combat_technique_profile: CombatTechniqueProfile) -> None:
        self.__combat_technique_profile = combat_technique_profile

    @classmethod
    def create_new(cls, *, entity_id: IEntityID, name: str) -> ICombatTechniqueProfileBuilder:
        new_character_spell = cls.__new__(cls)
        new_character_spell._init(entity_id, name)
        return _SpellProfileBuilder(new_character_spell, new_character_spell._set_combat_technique_profile)

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
    def stamina_cost(self) -> int:
        return self.__combat_technique_profile.stamina_cost

    def apply_combat_technique(self) -> None:
        self.__combat_technique_profile.start_loading_time()

    def rest_and_prepare(self) -> None:
        self.__combat_technique_profile.rest_and_prepare()


class _SpellProfileBuilder(ICombatTechniqueProfileBuilder):
    def __init__(
        self,
        character_spell_obj: CharacterCombatTechnique,
        func_set_spell_profile: Callable[[CombatTechniqueProfile], None],
    ) -> None:
        self.__func_set_spell_profile = func_set_spell_profile
        self.__character_spell_obj = character_spell_obj

    def specify_combat_technique_properties(
        self,
        stamina_cost: int,
        damage: int,
        cooldown: int,
        loading_time: int = 0,
    ) -> ICharacterCombatTechniquePublicMethods:
        spell_profile = CombatTechniqueProfile(
            stamina_cost=stamina_cost,
            damage=damage,
            cooldown=cooldown,
            loading_time=loading_time,
        )
        self.__func_set_spell_profile(spell_profile)
        return self.__character_spell_obj
