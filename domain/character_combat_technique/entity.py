"""Module describes the CharacterSpell entity and its direct dependencies"""
from abc import ABCMeta, abstractmethod
from functools import partial
from typing import Callable

from domain.value_objects import EntityID

from .interfaces import ICharacterCombatTechnique
from .value_objects import CombatTechniqueProfile


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


class CharacterCombatTechnique(ICharacterCombatTechnique):
    """Class that represents a CharacterCombatTechnique entity"""

    def __init__(self) -> None:
        raise RuntimeError("Cannot instantiate directly")

    def _init(self, entity_id: EntityID, name: str, combat_technique_profile: CombatTechniqueProfile) -> None:
        super().__init__(entity_id)
        self.__name = name
        self.__combat_technique_profile = combat_technique_profile

    @classmethod
    def create_new(cls, *, entity_id: EntityID, name: str) -> ICombatTechniqueProfileBuilder:
        new_character_spell = cls.__new__(cls)
        set_spell_profile = partial(new_character_spell._init, entity_id, name)
        return _SpellProfileBuilder(new_character_spell, set_spell_profile)

    @property
    def get_name(self) -> str:
        return self.__name

    @property
    def get_damage(self) -> int:
        return self.__combat_technique_profile.get_damage

    @property
    def get_stamina_cost(self) -> int:
        return self.__combat_technique_profile.get_stamina_cost

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
        *,
        stamina_cost: int,
        damage: int,
        cooldown: int,
        loading_time: int = 0,
    ) -> CharacterCombatTechnique:
        spell_profile = CombatTechniqueProfile(
            stamina_cost=stamina_cost,
            damage=damage,
            cooldown=cooldown,
            loading_time=loading_time,
        )
        self.__func_set_spell_profile(spell_profile)
        return self.__character_spell_obj
