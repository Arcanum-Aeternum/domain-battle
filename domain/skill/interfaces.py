from abc import ABCMeta, abstractmethod

from domain import IEntityID


class ISkill(metaclass=ABCMeta):
    """Interface that defines the public methods for skills"""

    entity_id: IEntityID

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        ...


class ICooldownSkill(ISkill, metaclass=ABCMeta):
    """Interface that defines the public methods for Cooldown skills"""

    @abstractmethod
    def rest(self) -> None:
        ...


class IPassive(ISkill, metaclass=ABCMeta):
    """Interface that defines the public methods for Passive skills"""

    @property
    @abstractmethod
    def is_active(self) -> bool:
        ...

    @property
    @abstractmethod
    def is_always_active(self) -> bool:
        ...

    @abstractmethod
    def activate(self) -> None:
        ...

    @abstractmethod
    def deactivate(self) -> None:
        ...


class IPassiveCooldown(IPassive, ICooldownSkill, metaclass=ABCMeta):
    """Interface that defines the public methods for PassiveCooldown skills"""


class IActive(ICooldownSkill, metaclass=ABCMeta):
    """Interface that defines the public methods for Active skills"""

    @property
    @abstractmethod
    def cost(self) -> int:
        ...

    @abstractmethod
    def use(self) -> None:
        ...


class IAttackable(IActive, metaclass=ABCMeta):
    """Interface that defines the public methods for Attackable skills"""

    @property
    @abstractmethod
    def damage(self) -> int:
        ...


class IPhysicalAttack(IAttackable, metaclass=ABCMeta):
    """Interface that defines the public methods for PhysicalAttack skills"""


class IMagicalAttack(IAttackable, metaclass=ABCMeta):
    """Interface that defines the public methods for MagicalAttack skills"""
