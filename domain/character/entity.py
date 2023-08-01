from typing import Generator

from trio import open_nursery, to_thread

from domain.character_combat_technique import ICharacterCombatTechniquePublicMethods
from domain.character_spell import ICharacterSpellPublicMethods
from domain.interfaces import Entity, IEntityID

from .exceptions import (
    CombatTechniqueNotAvailable,
    SpellNotAvailable,
    ThisCharacterDoesNotHaveThatCombatTechnique,
    ThisCharacterDoesNotHaveThatSpell,
)
from .interfaces import (
    ICharacter,
    ICharacterPublicMethods,
    ICombatTechniquesBuilder,
    ISkillProfileBuilder,
    ISpellsBuilder,
)
from .value_objects import SkillProfile


class Character(Entity, ICharacter, ICharacterPublicMethods):
    """Class that represents a Character entity"""

    def __init__(self) -> None:
        raise RuntimeError("Cannot instantiate directly")

    def _init(
        self,
        entity_id: IEntityID,
        name: str,
    ) -> None:
        super().__init__(entity_id)
        self.__name = name

    def _build_skill_profile(self, skill_profile: SkillProfile) -> None:
        self.__skill_profile = skill_profile

    def _build_combat_techniques(self, combat_techniques: tuple[ICharacterCombatTechniquePublicMethods, ...]) -> None:
        self.__combat_techniques = combat_techniques

    def _build_spells(self, spells: tuple[ICharacterSpellPublicMethods, ...] = tuple()) -> None:
        self.__spells = spells

    @classmethod
    def create_new(cls, *, entity_id: IEntityID, name: str) -> ISkillProfileBuilder:
        new_character = cls.__new__(cls)
        new_character._init(entity_id, name)
        return _BuildSkillProfile(new_character)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def is_alive(self) -> bool:
        return self.__skill_profile.current_life_points > 0

    @property
    def current_life_points(self) -> int:
        return self.__skill_profile.current_life_points

    @property
    def current_stamina_points(self) -> int:
        return self.__skill_profile.current_stamina_points

    @property
    def current_mana_points(self) -> int:
        return self.__skill_profile.current_mana_points

    @property
    def available_combat_techniques(self) -> Generator[ICharacterCombatTechniquePublicMethods, None, None]:
        try:
            return (combat_technique for combat_technique in self.__combat_techniques if combat_technique.is_ready)
        except StopIteration as error:
            msg = "No combat technique is available"
            raise CombatTechniqueNotAvailable(msg) from error

    @property
    def available_spells(self) -> Generator[ICharacterSpellPublicMethods, None, None]:
        try:
            return (spell for spell in self.__spells if spell.is_ready)
        except StopIteration as error:
            msg = "No spell is available"
            raise SpellNotAvailable(msg) from error

    def apply_combat_technique(self, combat_technique_id: IEntityID, target_character: ICharacterPublicMethods) -> None:
        try:
            combat_technique = next(
                combat_technique
                for combat_technique in self.__combat_techniques
                if combat_technique.entity_id == combat_technique_id and combat_technique.is_ready
            )
            combat_technique.apply_combat_technique()
            self.__skill_profile.decrement_stamina_points(combat_technique.stamina_cost)
            target_character._receive_attack(combat_technique.damage)
        except StopIteration:
            raise ThisCharacterDoesNotHaveThatCombatTechnique()

    def cast_spell(self, spell_id: IEntityID, target_character: ICharacterPublicMethods) -> None:
        try:
            spell = next(spell for spell in self.__spells if spell.entity_id == spell_id and spell.is_ready)
            spell.cast_spell()
            self.__skill_profile.decrement_mana_points(spell.mana_cost)
            target_character._receive_attack(spell.damage)
        except StopIteration:
            raise ThisCharacterDoesNotHaveThatSpell()

    async def rest(self) -> None:
        def _rest_combat_technique() -> None:
            for combat_technique in self.__combat_techniques:
                combat_technique.rest_and_prepare()

        def _load_spell() -> None:
            for spell in self.__spells:
                spell.load_spell()

        async with open_nursery() as nursery:
            nursery.start_soon(to_thread.run_sync, _rest_combat_technique)
            nursery.start_soon(to_thread.run_sync, _load_spell)

    def _receive_attack(self, damage: int) -> None:
        self.__skill_profile.decrement_life_points(damage)


class _BuildSkillProfile(ISkillProfileBuilder):
    def __init__(
        self,
        character_obj: Character,
    ) -> None:
        self.__character_obj = character_obj

    def specify_skill_properties(
        self, life_points: int, stamina_points: int, mana_points: int
    ) -> ICombatTechniquesBuilder:
        skill_profile = SkillProfile(life_points=life_points, stamina_points=stamina_points, mana_points=mana_points)
        self.__character_obj._build_skill_profile(skill_profile)
        return _BuildCombatTechniques(self.__character_obj)


class _BuildCombatTechniques(ICombatTechniquesBuilder):
    def __init__(self, character_obj: Character) -> None:
        self.__character_obj = character_obj
        self.__combat_techniques_list: list[ICharacterCombatTechniquePublicMethods] = []

    def build(self) -> ISpellsBuilder:
        self.__character_obj._build_combat_techniques(tuple(self.__combat_techniques_list))
        return _BuildSpells(self.__character_obj)

    def add_combat_technique(
        self, combat_technique: ICharacterCombatTechniquePublicMethods
    ) -> ICombatTechniquesBuilder:
        self.__combat_techniques_list.append(combat_technique)
        return self

    def add_combat_techniques(self, *combat_technique: ICharacterCombatTechniquePublicMethods) -> ISpellsBuilder:
        self.__combat_techniques_list.extend(combat_technique)
        return self.build()


class _BuildSpells(ISpellsBuilder):
    def __init__(self, character_obj: Character) -> None:
        self.__character_obj = character_obj
        self.__spell_list: list[ICharacterSpellPublicMethods] = []

    def build(self) -> Character:
        self.__character_obj._build_spells(tuple(self.__spell_list))
        return self.__character_obj

    def add_spell(self, spell: ICharacterSpellPublicMethods) -> ISpellsBuilder:
        self.__spell_list.append(spell)
        return self

    def add_spells(self, *spells: ICharacterSpellPublicMethods) -> Character:
        self.__spell_list.extend(spells)
        return self.build()
