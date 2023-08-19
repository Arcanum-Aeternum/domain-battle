from abc import ABCMeta, abstractmethod
from typing import Generator

from domain import IEntityID
from domain.skill import ISkill
from domain.skill.combat_technique import ICombatTechnique
from domain.skill.spell import ISpell


class ICharacter(metaclass=ABCMeta):
    """Interface that defines the public methods in Character"""

    entity_id: IEntityID

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def is_alive(self) -> bool:
        ...

    @property
    @abstractmethod
    def current_stamina_points(self) -> int:
        ...

    @property
    @abstractmethod
    def current_mana_points(self) -> int:
        ...

    @property
    @abstractmethod
    def current_life_points(self) -> int:
        ...

    @property
    @abstractmethod
    def available_combat_techniques(self) -> Generator[ICombatTechnique, None, None]:
        ...

    @property
    @abstractmethod
    def available_spells(self) -> Generator[ISpell, None, None]:
        ...

    @abstractmethod
    def attack(self, skill_id: IEntityID, target_character: "ICharacter") -> None:
        ...

    @abstractmethod
    def rest(self) -> None:
        ...

    @abstractmethod
    def _receive_attack(self, damage: int) -> None:
        ...


class ISkillBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to add skills to the Character"""

    @abstractmethod
    def build(self) -> ICharacter:
        ...

    @abstractmethod
    def add_skills(self, *skills: ISkill) -> ICharacter:
        ...

    @abstractmethod
    def add_skill(self, skill: ISkill) -> "ISkillBuilder":
        ...


class IStatsProfileBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to create a Character with its SkillProfile"""

    @abstractmethod
    def specify_skill_properties(self, life_points: int, stamina_points: int, mana_points: int) -> ISkillBuilder:
        ...


class ICharacterFactory(metaclass=ABCMeta):
    """Interface that define the public methods of Character with exception of factory methods"""

    @classmethod
    @abstractmethod
    def create_new(cls, *, entity_id: IEntityID, name: str) -> IStatsProfileBuilder:
        ...
