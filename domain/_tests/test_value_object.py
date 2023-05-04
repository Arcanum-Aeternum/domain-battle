from domain.interfaces import ValueObject


def test_value_object() -> None:
    class ExampleValueObject(ValueObject):
        """Example of ValueObject abstraction usage"""

        def __init__(self, a: str, b: str, c: int) -> None:
            self._a = a
            self._b = b
            self._c = c

    assert ExampleValueObject("a", "b", 1) == ExampleValueObject("a", "b", 1)
    assert ExampleValueObject("a", "b", 1) != ExampleValueObject("aa", "bb", 11)
