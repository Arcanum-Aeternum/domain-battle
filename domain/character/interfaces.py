from abc import ABCMeta, abstractmethod

from domain.interfaces import IEntityID

from .ext_interfaces import IExpectedCharacterCombatTechnique, IExpectedCharacterSpell


class ICharacter(metaclass=ABCMeta):
    """Interface that define the public methods of Character with exception of factory methods"""

    entity_id: IEntityID

    @abstractmethod
    def create_new(self, *, entity_id: IEntityID, name: str) -> "ISkillProfileBuilder":
        ...

    @property
    @abstractmethod
    def get_name(self) -> str:
        ...

    @property
    @abstractmethod
    def get_current_stamina_points(self) -> int:
        ...

    @property
    @abstractmethod
    def get_current_mana_points(self) -> int:
        ...

    @property
    @abstractmethod
    def get_current_life_points(self) -> int:
        ...

    @abstractmethod
    def apply_combat_technique(self, *, combat_technique_id: IEntityID, target_character: "ICharacter") -> None:
        ...

    @abstractmethod
    def cast_spell(self, *, spell_id: IEntityID, target_character: "ICharacter") -> None:
        ...

    @abstractmethod
    def receive_attack(self, damage: int) -> None:
        ...


class ISpellsBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to add spells to the Character"""

    @abstractmethod
    def build(self) -> ICharacter:
        ...

    @abstractmethod
    def add_spells(self, *spells: IExpectedCharacterSpell) -> ICharacter:
        ...

    @abstractmethod
    def add_spell(self, spell: IExpectedCharacterSpell) -> "ISpellsBuilder":
        ...


class ICombatTechniquesBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to add combat techniques to the Character"""

    @abstractmethod
    def build(self) -> ISpellsBuilder:
        ...

    @abstractmethod
    def add_combat_techniques(self, *combat_techniques: IExpectedCharacterCombatTechnique) -> ISpellsBuilder:
        ...

    @abstractmethod
    def add_combat_technique(self, combat_technique: IExpectedCharacterCombatTechnique) -> "ICombatTechniquesBuilder":
        ...


class ISkillProfileBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to create a Character with its SkillProfile"""

    @abstractmethod
    def specify_skill_properties(
        self, *, life_points: int, stamina_points: int, mana_points: int
    ) -> ICombatTechniquesBuilder:
        ...
