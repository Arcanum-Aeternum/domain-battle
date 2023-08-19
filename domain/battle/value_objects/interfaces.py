from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Callable

from domain import IEntityID
from domain.character import ICharacter
from domain.skill import IAttackable


class IMove(metaclass=ABCMeta):
    """Interface that defines the public methods in Move"""

    @classmethod
    @abstractmethod
    def create_new(cls, playing_character: ICharacter, enemy_characters: tuple[ICharacter, ...]) -> "IMoveBuilder":
        ...


class IRestBuilder(metaclass=ABCMeta):
    """Interface that defines the public methods in RestBuilder"""

    @abstractmethod
    def rest(self) -> IMove:
        ...


class IMoveBuilder(IRestBuilder, metaclass=ABCMeta):
    """Interface that defines the public methods in MoveBuilder"""

    @abstractmethod
    def attack(self, target_enemy_id: IEntityID, attack_skill: IAttackable) -> IRestBuilder:
        ...


class ITeam(metaclass=ABCMeta):
    """Interface that defines the public methods that Battle expects to find in Team"""

    @property
    @abstractmethod
    def characters(self) -> tuple[ICharacter, ...]:
        ...


class ITeamBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to add characters to the Team"""

    @abstractmethod
    def build(self) -> ITeam:
        ...

    @abstractmethod
    def add_character(self, character: ICharacter) -> "ITeamBuilder":
        ...


class ITeamFactory(metaclass=ABCMeta):
    """Interface that defines the public methods that Battle expects to find in Team"""

    @classmethod
    @abstractmethod
    def create_new(cls) -> ITeamBuilder:
        ...


class IBattleAllies(metaclass=ABCMeta):
    """Interface that defines the public methods that Battle expects to find in BattleAllies"""

    @property
    @abstractmethod
    def teams(self) -> tuple[ITeam, ...]:
        ...


class IBattleAlliesBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to create a Battle with its Battle Allies"""

    @abstractmethod
    def add_team_builder(self, build_team: Callable[[ITeamBuilder], ITeam]) -> "IBattleAlliesBuilder":
        ...

    @abstractmethod
    def add_team(self, team: ITeam) -> "IBattleAlliesBuilder":
        ...

    @abstractmethod
    def build(self) -> IBattleAllies:
        ...


class IBattleAlliesFactory(metaclass=ABCMeta):
    """Interface that defines the public methods that Battle expects to find in BattleAllies"""

    @classmethod
    @abstractmethod
    def create_new(cls) -> IBattleAlliesBuilder:
        ...


class PassTurnAlgorithmEnum(str, Enum):
    """Enum that defines the possible PassTurnAlgorithm that a Battle can have"""

    REGULAR_PASS_TURN = "RegularPassTurn"
    JUMP_TO_THE_NEXT_PASS_TURN_ALGORITHM = "JumpToTheNextPassTurnAlgorithm"


class IPassTurnAlgorithm(metaclass=ABCMeta):
    """Interface that defines the public methods that Battle expects to find in PassTurnAlgorithm"""

    @property
    @abstractmethod
    def current_character(self) -> ICharacter:
        """Returns the current character"""

    @property
    @abstractmethod
    def enemies(self) -> tuple[ICharacter, ...]:
        """Returns the enemies of the current character""" ""

    @property
    @abstractmethod
    def finalists(self) -> tuple[tuple[ICharacter, ...], tuple[ICharacter, ...]] | None:
        """Returns the winner of the Battle"""

    @abstractmethod
    def next_turn(self) -> tuple[ICharacter, tuple[ICharacter, ...]]:
        """Returns the next turn based on the current turn and the participants"""
