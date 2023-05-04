"""Modulo describes each of the value objects used within the Duel aggregate"""
import uuid
from typing import Tuple

from domain import IEntityID


class EntityID(IEntityID, uuid.UUID):
    """Represents a value object specialized in working with entity IDs.

    It is capable of generating unique IDs, whether or not based on the namespace.
    : unique_font = None
        Uses the uuid4 algorithm to generate a pseudorandom ID
    : unique_font = <str>
        Uses the uuid5 (SHA-1) algorithm to generate a retrievable pseudo-random ID.
        In this case the ID can be retrieved using its source (unique_source)

    When instantiating this class with a namespace parameter, be sure to
    use a single_source, that is, only in cases that you are working on
    with entities that have unique attributes, such as cell phone number, or ID, in this way,
    the SHA-1 algorithm will always deliver hashes with an infamous collision probability!
    """

    def __init__(self, *, unique_font: str | None = None):
        if unique_font is not None:
            super().__init__(str(uuid.uuid5(uuid.NAMESPACE_DNS, unique_font)), version=5)
        else:
            super().__init__(str(uuid.uuid4()), version=4)

    def __eq__(self, entity_id: object) -> bool:
        if not isinstance(entity_id, EntityID):
            return False
        return self.hex == entity_id.hex

    def __mul__(self, quantidade_de_instancias: int) -> Tuple["EntityID", ...]:
        return tuple(EntityID() for _ in range(quantidade_de_instancias))

    def __rmul__(self, quantidade_de_instancias: int) -> Tuple["EntityID", ...]:
        return tuple(EntityID() for _ in range(quantidade_de_instancias))

    def __hash__(self) -> int:
        return hash(str(self))
