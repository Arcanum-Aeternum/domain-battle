from contextlib import suppress
from functools import partial

import pytest

from domain._tests.fakes import (
    fake_battle,
    fake_battle_allies,
    fake_character,
    fake_character_combat_technique,
    fake_character_spell,
    fake_team,
)
from domain.battle.events.events import CharacterLostBattleEvent, CharacterWonBattleEvent
from domain.battle.exceptions import BattleIsNotHappeningException
from domain.battle.value_objects import PassTurnAlgorithmEnum
from domain.battle_event_dispatcher import BattleEventDispatcher
from domain.character import Character, ICharacterPublicMethods
from domain.character.exceptions import ThisCharacterDoesNotHaveThatCombatTechnique, ThisCharacterDoesNotHaveThatSpell
from domain.character_combat_technique import CharacterCombatTechnique
from domain.character_spell import CharacterSpell


async def test_complete_battle() -> None:
    with pytest.raises(RuntimeError, match="Cannot instantiate directly"):
        CharacterCombatTechnique()

    with pytest.raises(RuntimeError, match="Cannot instantiate directly"):
        CharacterSpell()

    with pytest.raises(RuntimeError, match="Cannot instantiate directly"):
        Character()

    seed = 15
    neryo_tchagui = fake_character_combat_technique(seed)
    shoot_spider_web = fake_character_spell(seed)

    characters_names = ("Itadori", "Makima", "Tsubasa", "Aizen")
    character1 = fake_character(characters_names[0], seed, combat_technique_quantity=3, spell_quantity=0)
    character2 = fake_character(characters_names[1], seed, combat_technique_quantity=2, spell_quantity=1)
    character3 = fake_character(characters_names[2], seed, combat_technique_quantity=1, spell_quantity=2)
    character4 = fake_character(characters_names[3], seed, combat_technique_quantity=0, spell_quantity=3)

    with pytest.raises(ThisCharacterDoesNotHaveThatSpell):
        character1.cast_spell(shoot_spider_web.entity_id, character2)

    with pytest.raises(ThisCharacterDoesNotHaveThatCombatTechnique):
        character1.apply_combat_technique(neryo_tchagui.entity_id, character2)

    team_a = fake_team(character1, character2)
    team_b = fake_team(character3, character4)
    battle_allies_a = fake_battle_allies(team_a)
    battle_allies_b = fake_battle_allies(team_b)
    event_dispatcher = BattleEventDispatcher()
    battle = fake_battle(event_dispatcher, PassTurnAlgorithmEnum.REGULAR_PASS_TURN, battle_allies_a, battle_allies_b)

    def playing_move(
        character_name: str,
        character: ICharacterPublicMethods,
        his_enemies: tuple[ICharacterPublicMethods, ...],
    ) -> None:
        assert character.name == character_name
        chosen_enemy = his_enemies[0]
        combat_technique = next(character.available_combat_techniques, None)
        spell = next(character.available_spells, None)
        character_current_stamina_points = character.current_stamina_points
        character_current_mana_points = character.current_mana_points
        if combat_technique:
            enemy_current_life_points = chosen_enemy.current_life_points
            character.apply_combat_technique(combat_technique.entity_id, chosen_enemy)
            assert chosen_enemy.current_life_points == max(enemy_current_life_points - combat_technique.damage, 0)
            assert character.current_stamina_points == max(
                character_current_stamina_points - combat_technique.stamina_cost, 0
            )
        if spell:
            enemy_current_life_points = chosen_enemy.current_life_points
            character.cast_spell(spell.entity_id, chosen_enemy)
            assert chosen_enemy.current_life_points == max(enemy_current_life_points - spell.damage, 0)
            assert character.current_mana_points == max(character_current_mana_points - spell.mana_cost, 0)

    async def battle_round() -> None:
        characters_order = (characters_names[0], characters_names[2], characters_names[1], characters_names[3])
        for character_name in characters_order:
            with suppress(BattleIsNotHappeningException):
                await battle.play(partial(playing_move, character_name))

    for _ in range(14):
        await battle_round()

    assert event_dispatcher.was_dispatched(CharacterWonBattleEvent)
    assert event_dispatcher.was_dispatched(CharacterLostBattleEvent)
    assert not event_dispatcher.has(CharacterWonBattleEvent)
    assert not event_dispatcher.has(CharacterLostBattleEvent)
    with pytest.raises(BattleIsNotHappeningException):
        await battle.play(partial(playing_move, characters_names[0]))
