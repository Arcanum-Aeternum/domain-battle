from functools import partial

import pytest

from domain._tests.fakes import (
    fake_battle,
    fake_battle_allies,
    fake_character,
    fake_combat_technique,
    fake_spell,
    fake_team,
)
from domain.battle.events.events import CharacterLostBattleEvent, CharacterWonBattleEvent
from domain.battle.exceptions import BattleIsNotHappeningException
from domain.battle.value_objects import IMoveBuilder, PassTurnAlgorithmEnum
from domain.battle_event_dispatcher import BattleEventDispatcher
from domain.character import Character, ICharacter
from domain.character.exceptions import CharacterDoesNotHaveThatSkillException
from domain.skill.combat_technique import CombatTechnique
from domain.skill.spell import Spell


async def test_complete_battle() -> None:
    with pytest.raises(RuntimeError, match="Cannot instantiate directly"):
        CombatTechnique()

    with pytest.raises(RuntimeError, match="Cannot instantiate directly"):
        Spell()

    with pytest.raises(RuntimeError, match="Cannot instantiate directly"):
        Character()

    seed = 15
    neryo_tchagui = fake_combat_technique(seed)
    shoot_spider_web = fake_spell(seed)

    characters_names = ("Itadori", "Makima", "Tsubasa", "Aizen")
    character1 = fake_character(characters_names[0], seed, combat_technique_quantity=3, spell_quantity=0)
    character2 = fake_character(characters_names[1], seed, combat_technique_quantity=2, spell_quantity=1)
    character3 = fake_character(characters_names[2], seed, combat_technique_quantity=1, spell_quantity=2)
    character4 = fake_character(characters_names[3], seed, combat_technique_quantity=0, spell_quantity=3)

    with pytest.raises(CharacterDoesNotHaveThatSkillException):
        character1.attack(shoot_spider_web.entity_id, character2)
        character1.attack(neryo_tchagui.entity_id, character2)

    team_a = fake_team(character1, character2)
    team_b = fake_team(character3, character4)
    battle_allies_a = fake_battle_allies(team_a)
    battle_allies_b = fake_battle_allies(team_b)
    event_dispatcher = BattleEventDispatcher()
    battle = fake_battle(event_dispatcher, PassTurnAlgorithmEnum.REGULAR_PASS_TURN, battle_allies_a, battle_allies_b)

    def playing_move(
        playing_character: ICharacter,
        enemy_character: ICharacter,
        build_playing_move: IMoveBuilder,
    ) -> None:
        combat_technique = next(playing_character.available_combat_techniques, None)
        spell = next(playing_character.available_spells, None)
        character_current_stamina_points = playing_character.current_stamina_points
        character_current_mana_points = playing_character.current_mana_points
        if combat_technique:
            enemy_current_life_points = enemy_character.current_life_points
            build_playing_move.attack(enemy_character.entity_id, combat_technique)
            assert enemy_character.current_life_points == max(enemy_current_life_points - combat_technique.damage, 0)
            assert playing_character.current_stamina_points == max(
                character_current_stamina_points - combat_technique.cost, 0
            )
        if spell:
            enemy_current_life_points = enemy_character.current_life_points
            playing_character.attack(spell.entity_id, enemy_character)
            assert enemy_character.current_life_points == max(enemy_current_life_points - spell.damage, 0)
            assert playing_character.current_mana_points == max(character_current_mana_points - spell.cost, 0)

    async def battle_round() -> None:
        playing_characters_order = (character1, character3, character2, character4)
        enemy_characters_order = (character3, character1, character4, character2)
        for playing_character, enemy_character in zip(playing_characters_order, enemy_characters_order):
            try:
                await battle.play(partial(playing_move, playing_character, enemy_character))
            except BattleIsNotHappeningException:
                break

    rounds_until_battle_ends = 13
    for _ in range(rounds_until_battle_ends):
        await battle_round()

    assert event_dispatcher.was_dispatched(CharacterWonBattleEvent)
    assert event_dispatcher.was_dispatched(CharacterLostBattleEvent)
    assert not event_dispatcher.has(CharacterWonBattleEvent)
    assert not event_dispatcher.has(CharacterLostBattleEvent)

    with pytest.raises(BattleIsNotHappeningException):
        await battle.play(partial(playing_move, characters_names[0]))
