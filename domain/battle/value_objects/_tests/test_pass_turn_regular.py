import pytest

from domain._tests.fakes import fake_battle_allies_gen
from domain.battle.value_objects.interfaces import IBattleAllies

from ..pass_turn_algorithm import RegularPassTurn


def many_battle_allies(
    seed: int,
    battle_allies_quantity: int,
    team_quantity: int,
    character_quantity: int,
) -> tuple[IBattleAllies, ...]:
    return tuple(
        battle_allies
        for battle_allies in fake_battle_allies_gen(
            seed,
            battle_allies_quantity,
            team_quantity,
            character_quantity,
        )
    )


@pytest.mark.parametrize(
    "seed, battle_allies_quantity, team_quantity, character_quantity",
    [
        (10, 2, 1, 1),
        (15, 3, 1, 2),
        (20, 4, 2, 3),
        (25, 5, 2, 4),
    ],
)
def test_data_structure_creation(
    seed: int, battle_allies_quantity: int, team_quantity: int, character_quantity: int
) -> None:
    battle_allies_groups = many_battle_allies(
        seed,
        battle_allies_quantity,
        team_quantity,
        character_quantity,
    )

    pass_turn_algorithmn = RegularPassTurn(battle_allies_groups)
    current_character = pass_turn_algorithmn.current_character
    assert current_character == battle_allies_groups[0].teams[0].characters[0]
    playing_character, _ = pass_turn_algorithmn.next_turn()
    assert playing_character == current_character
