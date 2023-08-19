from domain._tests.fakes import fake_character_gen
from domain.battle.value_objects.interfaces import IMoveBuilder
from domain.battle.value_objects.move import Move


def test_player_move_behavior() -> None:
    seed = 10

    playing_character = next(fake_character_gen(seed, 1))
    enemy_characters = tuple(fake_character_gen(seed, 2))
    character_skill = next(playing_character.available_spells)

    target_enemy_id = enemy_characters[0].entity_id

    def move(move: IMoveBuilder) -> None:
        move.attack(target_enemy_id, character_skill).rest()

    move_builder = Move.create_new(playing_character, enemy_characters)
    move(move_builder)
