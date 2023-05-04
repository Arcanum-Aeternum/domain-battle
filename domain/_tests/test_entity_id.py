import uuid

from domain.value_objects import EntityID


def test_entity_id_creation() -> None:
    assert isinstance(EntityID(), uuid.UUID), "Generated ID is not UUID"
    assert isinstance(EntityID(unique_font="UNIQUE FONT"), uuid.UUID), "Generated ID is not UUID"
    assert EntityID(unique_font="UNIQUE FONT") == EntityID(unique_font="UNIQUE FONT")
    assert EntityID() != EntityID()
    assert len(EntityID() * 3) == 3
    assert len(5 * EntityID()) == 5
    try:
        hash(EntityID())
    except TypeError:
        assert False, "Can not use <hash> built in function"
