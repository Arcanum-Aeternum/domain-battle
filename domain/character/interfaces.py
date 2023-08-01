from abc import ABCMeta, abstractmethod
from typing import Generator

from domain.character_combat_technique import ICharacterCombatTechniquePublicMethods
from domain.character_spell import ICharacterSpellPublicMethods
from domain.interfaces import IEntityID


class ICharacterPublicMethods(metaclass=ABCMeta):
    """Interface that defines the public methods in Character"""

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
    def available_combat_techniques(self) -> Generator[ICharacterCombatTechniquePublicMethods, None, None]:
        ...

    @property
    @abstractmethod
    def available_spells(self) -> Generator[ICharacterSpellPublicMethods, None, None]:
        ...

    @abstractmethod
    def apply_combat_technique(
        self, combat_technique_id: IEntityID, target_character: "ICharacterPublicMethods"
    ) -> None:
        ...

    @abstractmethod
    def cast_spell(self, spell_id: IEntityID, target_character: "ICharacterPublicMethods") -> None:
        ...

    @abstractmethod
    async def rest(self) -> None:
        ...

    @abstractmethod
    def _receive_attack(self, damage: int) -> None:
        ...


class ISpellsBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to add spells to the Character"""

    @abstractmethod
    def build(self) -> ICharacterPublicMethods:
        ...

    @abstractmethod
    def add_spells(self, *spells: ICharacterSpellPublicMethods) -> ICharacterPublicMethods:
        ...

    @abstractmethod
    def add_spell(self, spell: ICharacterSpellPublicMethods) -> "ISpellsBuilder":
        ...


class ICombatTechniquesBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to add combat techniques to the Character"""

    @abstractmethod
    def build(self) -> ISpellsBuilder:
        ...

    @abstractmethod
    def add_combat_techniques(self, *combat_techniques: ICharacterCombatTechniquePublicMethods) -> ISpellsBuilder:
        ...

    @abstractmethod
    def add_combat_technique(
        self, combat_technique: ICharacterCombatTechniquePublicMethods
    ) -> "ICombatTechniquesBuilder":
        ...


class ISkillProfileBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to create a Character with its SkillProfile"""

    @abstractmethod
    def specify_skill_properties(
        self, life_points: int, stamina_points: int, mana_points: int
    ) -> ICombatTechniquesBuilder:
        ...


class ICharacter(metaclass=ABCMeta):
    """Interface that define the public methods of Character with exception of factory methods"""

    entity_id: IEntityID

    @classmethod
    @abstractmethod
    def create_new(cls, *, entity_id: IEntityID, name: str) -> ISkillProfileBuilder:
        ...
