from functools import partial
from typing import Any, Callable

from domain.interfaces import IEntityID
from domain.value_objects import EntityID

from .exceptions import ThisCharacterDoesNotHaveThatSpell
from .ext_interfaces import IExpectedCharacterSpell
from .interfaces import ICharacter, ISkillProfileBuilder, ISpellsBuilder
from .value_objects import SkillProfile


class Character(ICharacter):
    """Class that represents a Character entity"""

    def __init__(self) -> None:
        raise RuntimeError("Cannot instantiate directly")

    def _init(
        self,
        entity_id: EntityID,
        name: str,
        skill_profile: SkillProfile,
        *spells: IExpectedCharacterSpell,
    ) -> None:
        super().__init__(entity_id)
        self.__name = name
        self.__skill_profile = skill_profile
        self.__spells = spells

    @classmethod
    def create_new(cls, *, entity_id: EntityID, name: str) -> ISkillProfileBuilder:
        new_character = cls.__new__(cls)
        set_skill_profile_and_spells = partial(new_character._init, entity_id, name)
        return _BuildSkillProfile(new_character, set_skill_profile_and_spells)

    @property
    def get_name(self) -> str:
        return self.__name

    @property
    def get_current_life_points(self) -> int:
        return self.__skill_profile.get_current_life_points

    @property
    def get_current_mana_points(self) -> int:
        return self.__skill_profile.get_current_mana_points

    def cast_spell(self, *, spell_id: IEntityID, target_character: ICharacter) -> None:
        try:
            spell = next(spell for spell in self.__spells if spell.entity_id == spell_id)
            spell.cast_spell()
            self.__skill_profile.decrement_mana_points(spell.get_mana_cost)
            target_character.receive_attack(spell.get_damage)
        except StopIteration:
            raise ThisCharacterDoesNotHaveThatSpell()

    def receive_attack(self, damage: int) -> None:
        self.__skill_profile.decrement_life_points(damage)


class _BuildSkillProfile(ISkillProfileBuilder):
    def __init__(
        self,
        character_obj: Character,
        cb_set_func: Callable[[SkillProfile, Any], None],
    ) -> None:
        self.__character_obj = character_obj
        self.__cb_set_func = cb_set_func

    def specify_skill_properties(self, *, life_points: int, mana_points: int) -> ISpellsBuilder:
        skill_profile = SkillProfile(life_points=life_points, mana_points=mana_points)
        func_set_character_spells = partial(self.__cb_set_func, skill_profile)
        return _BuildSpells(self.__character_obj, func_set_character_spells)


class _BuildSpells(ISpellsBuilder):
    def __init__(self, character_obj: Character, cb_set_func: Callable[..., None]) -> None:
        self.__character_obj = character_obj
        self.__cb_set_func = cb_set_func
        self.__spell_list: list[IExpectedCharacterSpell] = []

    def build(self) -> Character:
        self.__cb_set_func(*self.__spell_list)
        return self.__character_obj

    def add_spell(self, spell: IExpectedCharacterSpell) -> ISpellsBuilder:
        self.__spell_list.append(spell)
        return _BuildSpells(self.__character_obj, self.__cb_set_func)

    def add_spells(self, *spells: IExpectedCharacterSpell) -> Character:
        self.__spell_list.extend(spells)
        return self.build()
