from domain.interfaces import Entity, IEntityID

from .exceptions import ThisCharacterDoesNotHaveThatCombatTechnique, ThisCharacterDoesNotHaveThatSpell
from .ext_interfaces import IExpectedCharacterCombatTechnique, IExpectedCharacterSpell
from .interfaces import ICharacter, ICombatTechniquesBuilder, ISkillProfileBuilder, ISpellsBuilder
from .value_objects import SkillProfile


class Character(Entity, ICharacter):
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

    def _build_combat_techniques(self, combat_techniques: tuple[IExpectedCharacterCombatTechnique, ...]) -> None:
        self.__combat_techniques = combat_techniques

    def _build_spells(self, spells: tuple[IExpectedCharacterSpell, ...] = tuple()) -> None:
        self.__spells = spells

    @classmethod
    def create_new(cls, *, entity_id: IEntityID, name: str) -> ISkillProfileBuilder:
        new_character = cls.__new__(cls)
        new_character._init(entity_id, name)
        return _BuildSkillProfile(new_character)

    @property
    def get_name(self) -> str:
        return self.__name

    @property
    def get_current_life_points(self) -> int:
        return self.__skill_profile.get_current_life_points

    @property
    def get_current_stamina_points(self) -> int:
        return self.__skill_profile.get_current_stamina_points

    @property
    def get_current_mana_points(self) -> int:
        return self.__skill_profile.get_current_mana_points

    def apply_combat_technique(self, *, combat_technique_id: IEntityID, target_character: ICharacter) -> None:
        try:
            combat_technique = next(
                combat_technique
                for combat_technique in self.__combat_techniques
                if combat_technique.entity_id == combat_technique_id
            )
            combat_technique.apply_combat_technique()
            self.__skill_profile.decrement_stamina_points(combat_technique.get_stamina_cost)
            target_character.receive_attack(combat_technique.get_damage)
        except StopIteration:
            raise ThisCharacterDoesNotHaveThatCombatTechnique()

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
    ) -> None:
        self.__character_obj = character_obj

    def specify_skill_properties(
        self, *, life_points: int, stamina_points: int, mana_points: int
    ) -> ICombatTechniquesBuilder:
        skill_profile = SkillProfile(life_points=life_points, stamina_points=stamina_points, mana_points=mana_points)
        self.__character_obj._build_skill_profile(skill_profile)
        return _BuildCombatTechniques(self.__character_obj)


class _BuildCombatTechniques(ICombatTechniquesBuilder):
    def __init__(self, character_obj: Character) -> None:
        self.__character_obj = character_obj
        self.__combat_techniques_list: list[IExpectedCharacterCombatTechnique] = []

    def build(self) -> ISpellsBuilder:
        self.__character_obj._build_combat_techniques(tuple(self.__combat_techniques_list))
        return _BuildSpells(self.__character_obj)

    def add_combat_technique(self, combat_technique: IExpectedCharacterCombatTechnique) -> ICombatTechniquesBuilder:
        self.__combat_techniques_list.append(combat_technique)
        return _BuildCombatTechniques(self.__character_obj)

    def add_combat_techniques(self, *combat_technique: IExpectedCharacterCombatTechnique) -> ISpellsBuilder:
        self.__combat_techniques_list.extend(combat_technique)
        return self.build()


class _BuildSpells(ISpellsBuilder):
    def __init__(self, character_obj: Character) -> None:
        self.__character_obj = character_obj
        self.__spell_list: list[IExpectedCharacterSpell] = []

    def build(self) -> Character:
        self.__character_obj._build_spells(tuple(self.__spell_list))
        return self.__character_obj

    def add_spell(self, spell: IExpectedCharacterSpell) -> ISpellsBuilder:
        self.__spell_list.append(spell)
        return _BuildSpells(self.__character_obj)

    def add_spells(self, *spells: IExpectedCharacterSpell) -> Character:
        self.__spell_list.extend(spells)
        return self.build()
