"""Module describes the Spell entity and its direct dependencies"""
from typing import Callable

from domain import Entity, IEntityID

from .interfaces import ISpell, ISpellFactory, ISpellProfileBuilder
from .value_objects import SpellProfile


class Spell(Entity, ISpellFactory, ISpell):
    """Class that represents a Spell entity"""

    def __init__(self) -> None:
        raise RuntimeError("Cannot instantiate directly")

    def _init(self, entity_id: IEntityID, name: str) -> None:
        super().__init__(entity_id)
        self.__name = name

    def _set_spell_profile(self, spell_profile: SpellProfile) -> None:
        self.__spell_profile = spell_profile

    @classmethod
    def create_new(cls, *, entity_id: IEntityID, name: str) -> ISpellProfileBuilder:
        new_spell = cls.__new__(cls)
        new_spell._init(entity_id, name)
        return _SpellProfileBuilder(new_spell, new_spell._set_spell_profile)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def is_ready(self) -> bool:
        return self.__spell_profile.is_ready

    @property
    def damage(self) -> int:
        return self.__spell_profile.get_damage

    @property
    def cost(self) -> int:
        return self.__spell_profile.get_mana_cost

    def use(self) -> None:
        self.__spell_profile.start_loading_time()

    def rest(self) -> None:
        self.__spell_profile.load_spell()


class _SpellProfileBuilder(ISpellProfileBuilder):
    def __init__(
        self,
        spell_obj: Spell,
        func_set_spell_profile: Callable[[SpellProfile], None],
    ) -> None:
        self.__func_set_spell_profile = func_set_spell_profile
        self.__spell_obj = spell_obj

    def specify_spell_properties(
        self,
        mana_cost: int,
        damage: int,
        cooldown: int,
        loading_time: int = 0,
    ) -> Spell:
        spell_profile = SpellProfile(
            mana_cost=mana_cost,
            damage=damage,
            cooldown=cooldown,
            loading_time=loading_time,
        )
        self.__func_set_spell_profile(spell_profile)
        return self.__spell_obj
