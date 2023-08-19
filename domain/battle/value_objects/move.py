from domain import IEntityID, ValueObject
from domain.character import ICharacter
from domain.skill import IAttackable

from .interfaces import IMove, IMoveBuilder, IRestBuilder


class Move(ValueObject, IMove):
    """Class that represents a value object of move to the Character"""

    def __init__(self) -> None:
        raise NotImplementedError("Cannot instantiate directly")

    def _init(
        self,
        playing_character: ICharacter,
        enemy_characters: tuple[ICharacter, ...],
    ) -> None:
        self.__playing_character = playing_character
        self.__enemy_characters = enemy_characters

    @classmethod
    def create_new(cls, playing_character: ICharacter, enemy_characters: tuple[ICharacter, ...]) -> IMoveBuilder:
        new_move = cls.__new__(cls)
        new_move._init(playing_character, enemy_characters)
        return _MoveBuilder(new_move)

    def _attack(self, target_enemy_id: IEntityID, attack_skill: IAttackable) -> None:
        target_enemy = self.__specific_enemy(target_enemy_id)
        self.__playing_character.attack(attack_skill.entity_id, target_enemy)

    def _rest(self) -> None:
        self.__playing_character.rest()

    def __specific_enemy(self, character_id: IEntityID) -> ICharacter:
        def _is_enemy(character: ICharacter) -> bool:
            return character.entity_id == character_id

        return next(filter(_is_enemy, self.__enemy_characters))


class _RestBuilder(IRestBuilder):
    def __init__(self, move_obj: Move) -> None:
        self.__move_obj = move_obj

    def rest(self) -> Move:
        self.__move_obj._rest()
        return self.__move_obj


class _MoveBuilder(IMoveBuilder, _RestBuilder):
    def __init__(self, move_obj: Move) -> None:
        self.__move_obj = move_obj

    def attack(self, target_enemy_id: IEntityID, attack_skill: IAttackable) -> IRestBuilder:
        self.__move_obj._attack(target_enemy_id, attack_skill)
        rest_builder = _RestBuilder(self.__move_obj)
        return rest_builder
