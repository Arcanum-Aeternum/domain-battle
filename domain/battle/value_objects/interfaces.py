from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Callable

from domain.character import ICharacterPublicMethods


class ITeamPublicMethods(metaclass=ABCMeta):
    """Interface that defines the public methods that Battle expects to find in Team"""

    @property
    @abstractmethod
    def characters(self) -> tuple[ICharacterPublicMethods, ...]:
        ...


class ITeamBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to add characters to the Team"""

    @abstractmethod
    def build(self) -> ITeamPublicMethods:
        ...

    @abstractmethod
    def add_character(self, character: ICharacterPublicMethods) -> "ITeamBuilder":
        ...


class ITeam(ITeamPublicMethods, metaclass=ABCMeta):
    """Interface that defines the public methods that Battle expects to find in Team"""

    @classmethod
    @abstractmethod
    def create_new(cls) -> ITeamBuilder:
        ...


class IBattleAlliesPublicMethods(metaclass=ABCMeta):
    """Interface that defines the public methods that Battle expects to find in BattleAllies"""

    @property
    @abstractmethod
    def teams(self) -> tuple[ITeamPublicMethods, ...]:
        ...


class IBattleAlliesBuilder(metaclass=ABCMeta):
    """Interface that defines an easy way to create a Battle with its Battle Allies"""

    @abstractmethod
    def add_team_builder(self, build_team: Callable[[ITeamBuilder], ITeamPublicMethods]) -> "IBattleAlliesBuilder":
        ...

    @abstractmethod
    def add_team(self, team: ITeamPublicMethods) -> "IBattleAlliesBuilder":
        ...

    @abstractmethod
    def build(self) -> IBattleAlliesPublicMethods:
        ...


class IBattleAllies(IBattleAlliesPublicMethods, metaclass=ABCMeta):
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
    def current_character(self) -> ICharacterPublicMethods:
        """Returns the current character"""

    @property
    @abstractmethod
    def enemies(self) -> tuple[ICharacterPublicMethods, ...]:
        """Returns the enemies of the current character""" ""

    @property
    @abstractmethod
    def finalists(self) -> tuple[tuple[ICharacterPublicMethods, ...], tuple[ICharacterPublicMethods, ...]] | None:
        """Returns the winner of the Battle"""

    @abstractmethod
    def next_turn(self) -> tuple[ICharacterPublicMethods, tuple[ICharacterPublicMethods, ...]]:
        """Returns the next turn based on the current turn and the participants"""
