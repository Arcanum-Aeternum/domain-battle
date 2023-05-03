from abc import ABCMeta, abstractmethod

from domain.interfaces import IEntityID


class IExpectedCharacterSpell(metaclass=ABCMeta):
    """Interface that defines the public methods that Character expects to find in CharacterSpell"""

    @abstractmethod
    def __init__(self) -> None:
        self.entity_id: IEntityID

    @property
    @abstractmethod
    def get_name(self) -> str:
        ...

    @property
    @abstractmethod
    def get_damage(self) -> int:
        ...

    @property
    @abstractmethod
    def get_mana_cost(self) -> int:
        ...

    @abstractmethod
    def cast_spell(self) -> None:
        ...

    @abstractmethod
    def load_spell(self) -> None:
        ...
