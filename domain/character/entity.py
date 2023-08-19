from typing import Generator, Type, TypeVar, cast

from domain import Entity, IEntityID
from domain.skill import IAttackable, ICooldownSkill, IMagicalAttack, IPhysicalAttack, ISkill
from domain.skill.combat_technique import CombatTechnique, ICombatTechnique
from domain.skill.spell import ISpell, Spell

from .exceptions import (
    CantUseThisSkillToAttackException,
    CharacterDoesNotHaveThatSkillException,
    NoCombatTechniqueAvailableException,
    NoSpellAvailableException,
)
from .interfaces import ICharacter, ICharacterFactory, ISkillBuilder, IStatsProfileBuilder
from .value_objects import SkillProfile

T_skill_contra = TypeVar("T_skill_contra", bound=ISkill, contravariant=True)


class Character(Entity, ICharacterFactory, ICharacter):
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

    def _build_skills(self, skills: tuple[ISkill, ...]) -> None:
        self.__skills = skills

    @classmethod
    def create_new(cls, *, entity_id: IEntityID, name: str) -> IStatsProfileBuilder:
        new_character = cls.__new__(cls)
        new_character._init(entity_id, name)
        return _StatsProfileBuilder(new_character)

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
    def available_combat_techniques(self) -> Generator[ICombatTechnique, None, None]:
        try:
            skills_gen = self.__available_skills(CombatTechnique)
            return (cast(CombatTechnique, skill) for skill in skills_gen)
        except StopIteration as error:
            raise NoCombatTechniqueAvailableException() from error

    @property
    def available_spells(self) -> Generator[ISpell, None, None]:
        try:
            skills_gen = self.__available_skills(Spell)
            return (cast(Spell, skill) for skill in skills_gen)
        except StopIteration as error:
            raise NoSpellAvailableException() from error

    def attack(self, skill_id: IEntityID, target_character: ICharacter) -> None:
        try:
            skill = next(skill for skill in self.__skills if skill == skill_id)
            if not isinstance(skill, IAttackable):
                raise CantUseThisSkillToAttackException()
            skill.use()
            if isinstance(skill, IMagicalAttack):
                self.__skill_profile.use_mana(skill.cost)
            if isinstance(skill, IPhysicalAttack):
                self.__skill_profile.use_stamina(skill.cost)
            target_character._receive_attack(skill.damage)
        except StopIteration as error:
            raise CharacterDoesNotHaveThatSkillException() from error

    def rest(self) -> None:
        for skill in self.__skills_on_cooldown():
            skill.rest()

    def _receive_attack(self, damage: int) -> None:
        self.__skill_profile.take_damage(damage)

    def __available_skills(self, skill_type: Type[T_skill_contra]) -> Generator[ISkill, None, None]:
        try:
            return (skill for skill in self.__skills if isinstance(skill, skill_type) and skill.is_ready)
        except StopIteration as error:
            msg = f"No {skill_type.__name__} is available"
            error.add_note(msg)
            raise error

    def __skills_on_cooldown(self) -> Generator[ICooldownSkill, None, None]:
        try:
            return (skill for skill in self.__skills if isinstance(skill, ICooldownSkill) and not skill.is_ready)
        except StopIteration as error:
            error.add_note("All skills are available")
            raise error


class _StatsProfileBuilder(IStatsProfileBuilder):
    def __init__(
        self,
        character_obj: Character,
    ) -> None:
        self.__character_obj = character_obj

    def specify_skill_properties(self, life_points: int, stamina_points: int, mana_points: int) -> ISkillBuilder:
        skill_profile = SkillProfile(life_points=life_points, stamina_points=stamina_points, mana_points=mana_points)
        self.__character_obj._build_skill_profile(skill_profile)
        return _SkillBuilder(self.__character_obj)


class _SkillBuilder(ISkillBuilder):
    def __init__(self, character_obj: Character) -> None:
        self.__character_obj = character_obj
        self.__skills_list: list[ISkill] = []

    def build(self) -> ICharacter:
        self.__character_obj._build_skills(tuple(self.__skills_list))
        return self.__character_obj

    def add_skill(self, skill: ISkill) -> ISkillBuilder:
        self.__skills_list.append(skill)
        return self

    def add_skills(self, *skills: ISkill) -> ICharacter:
        self.__skills_list.extend(skills)
        return self.build()
