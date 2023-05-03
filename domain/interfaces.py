from abc import ABCMeta


class ValueObject(metaclass=ABCMeta):
    """Abstraction used as a marker for value objects"""

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ValueObject):
            return False
        self_attributes = vars(self)
        other_attributes = vars(other)
        return self_attributes == other_attributes

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, ValueObject):
            return False
        return not self == other


class IEntityID(ValueObject, metaclass=ABCMeta):
    """Abstraction that defines mandatory methods for concretes of EntityID"""


class Entity(metaclass=ABCMeta):
    """Abstraction used as a marker for entities"""

    def __init__(self, entity_id: IEntityID) -> None:
        self.entity_id = entity_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.entity_id == other.entity_id

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False
        return self == other


class AggregateRoot(Entity, metaclass=ABCMeta):
    """Interface used as a marker for entities that are the root of the aggregate"""


class DomainService(metaclass=ABCMeta):
    """Interface used as a marker for domain services"""
