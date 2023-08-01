import pytest

from domain.interfaces import IEntityID
from domain.value_objects import EntityID


@pytest.fixture
def entity_id() -> IEntityID:
    return EntityID()
