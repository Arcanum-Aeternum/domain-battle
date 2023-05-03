"""Module describes the CharacterSpell entity and its direct dependencies"""
from abc import ABCMeta, abstractmethod
from functools import partial
from typing import Callable

from domain.value_objects import EntityID

from .interfaces import ICharacterSpell
from .value_objects import SpellProfile


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


class CharacterSpell(ICharacterSpell):
    """Class that represents a CharacterSpell entity"""

    def __init__(self) -> None:
        raise RuntimeError("Cannot instantiate directly")

    def _init(self, entity_id: EntityID, name: str, spell_profile: SpellProfile) -> None:
        super().__init__(entity_id)
        self.__name = name
        self.__spell_profile = spell_profile

    @classmethod
    def create_new(cls, *, entity_id: EntityID, name: str) -> ISpellProfileBuilder:
        new_character_spell = cls.__new__(cls)
        set_spell_profile = partial(new_character_spell._init, entity_id, name)
        return _SpellProfileBuilder(new_character_spell, set_spell_profile)

    @property
    def get_name(self) -> str:
        return self.__name

    @property
    def get_damage(self) -> int:
        return self.__spell_profile.get_damage

    @property
    def get_mana_cost(self) -> int:
        return self.__spell_profile.get_mana_cost

    def cast_spell(self) -> None:
        self.__spell_profile.start_loading_time()

    def load_spell(self) -> None:
        self.__spell_profile.load_spell()


class _SpellProfileBuilder(ISpellProfileBuilder):
    def __init__(
        self,
        character_spell_obj: CharacterSpell,
        func_set_spell_profile: Callable[[SpellProfile], None],
    ) -> None:
        self.__func_set_spell_profile = func_set_spell_profile
        self.__character_spell_obj = character_spell_obj

    def specify_spell_properties(
        self,
        *,
        mana_cost: int,
        damage: int,
        cooldown: int,
        loading_time: int = 0,
    ) -> CharacterSpell:
        spell_profile = SpellProfile(
            mana_cost=mana_cost,
            damage=damage,
            cooldown=cooldown,
            loading_time=loading_time,
        )
        self.__func_set_spell_profile(spell_profile)
        return self.__character_spell_obj
