from domain.interfaces import Entity, IEntityID
from domain.value_objects import EntityID


def test_entity_with_real_id() -> None:
    class ExampleEntity(Entity):
        """Example of Entity abstraction usage"""

        def __init__(self, entity_id: IEntityID, a: str, b: str) -> None:
            super().__init__(entity_id)
            self._a = a
            self._b = b

    entity_id = EntityID()
    entity = ExampleEntity(entity_id, "a", "b")
    assert hasattr(entity, "entity_id")
    assert ExampleEntity(entity_id, "a", "b") == ExampleEntity(entity_id, "aa", "bb")
    assert ExampleEntity(EntityID(), "a", "b") != ExampleEntity(EntityID(), "a", "b")
