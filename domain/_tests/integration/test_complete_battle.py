from typing import Callable

import pytest

from domain.battle.entity import Battle
from domain.battle.exceptions import BattleIsNotHappeningException
from domain.character.entity import Character
from domain.character.exceptions import ThisCharacterDoesNotHaveThatCombatTechnique, ThisCharacterDoesNotHaveThatSpell
from domain.character.interfaces import ICharacter
from domain.character_combat_technique.entity import CharacterCombatTechnique
from domain.character_combat_technique.interfaces import ICharacterCombatTechnique
from domain.character_spell.entity import CharacterSpell
from domain.character_spell.interfaces import ICharacterSpell
from domain.interfaces import IEntityID
from domain.value_objects import EntityID

MAXIMUS_POINTS = 100


def create_fake_character_combat_techniques(*, name: str, seed: int) -> ICharacterCombatTechnique:
    return CharacterCombatTechnique.create_new(
        entity_id=EntityID(),
        name=name,
    ).specify_combat_technique_properties(
        stamina_cost=seed,
        damage=seed,
        cooldown=seed,
    )


def create_fake_character_spell(*, name: str, seed: int) -> ICharacterSpell:
    return CharacterSpell.create_new(
        entity_id=EntityID(),
        name=name,
    ).specify_spell_properties(
        mana_cost=seed,
        damage=seed,
        cooldown=seed,
    )


def create_fake_character(
    *,
    name: str,
    combat_techniques: tuple[ICharacterCombatTechnique, ...] = tuple(),
    spells: tuple[ICharacterSpell, ...] = tuple(),
) -> ICharacter:
    return (
        Character.create_new(entity_id=EntityID(), name=name)
        .specify_skill_properties(life_points=MAXIMUS_POINTS, stamina_points=MAXIMUS_POINTS, mana_points=MAXIMUS_POINTS)
        .add_combat_techniques(*combat_techniques)
        .add_spells(*spells)
    )


def test_complete_battle() -> None:
    with pytest.raises(RuntimeError, match="Cannot instantiate directly"):
        CharacterSpell()

    with pytest.raises(RuntimeError, match="Cannot instantiate directly"):
        Character()

    combat_technique_seed = 15
    neryo_tchagui = create_fake_character_combat_techniques(name="Neryo Tchagui", seed=combat_technique_seed)
    mondolio_tchagui = create_fake_character_combat_techniques(name="Mondolio Tchagui", seed=combat_technique_seed)
    jab_punch = create_fake_character_combat_techniques(name="Jab Punch", seed=combat_technique_seed)
    direct_punch = create_fake_character_combat_techniques(name="Direct Punch", seed=combat_technique_seed)
    cross_punch = create_fake_character_combat_techniques(name="Cross Punch", seed=combat_technique_seed)
    spell_seed = 15
    hadouken = create_fake_character_spell(name="Hadouken", seed=spell_seed)
    shoryuken = create_fake_character_spell(name="Shoryuken", seed=spell_seed)
    shoot_spider_web = create_fake_character_spell(name="Shoot Spider Web", seed=spell_seed)

    character1 = create_fake_character(
        name="John Wick",
        combat_techniques=(neryo_tchagui, mondolio_tchagui),
        spells=(hadouken, shoryuken),
    )
    character2 = create_fake_character(
        name="Spider Man",
        combat_techniques=(neryo_tchagui,),
        spells=(hadouken,),
    )
    character3 = create_fake_character(
        name="Spider Man",
        spells=(shoot_spider_web,),
    )
    character4 = create_fake_character(
        name="Rocky Balboa",
        combat_techniques=(jab_punch, direct_punch, cross_punch),
    )

    with pytest.raises(ThisCharacterDoesNotHaveThatSpell):
        character3.cast_spell(spell_id=hadouken.entity_id, target_character=character2)

    with pytest.raises(ThisCharacterDoesNotHaveThatCombatTechnique):
        character3.apply_combat_technique(combat_technique_id=neryo_tchagui.entity_id, target_character=character2)

    team1 = Team(characters=(character1, character2))
    team2 = Team(characters=(character3, character4))
    battle = (
        Battle(entity_id=EntityID())
        .pass_turn_algorithm(PassTurnAlgorithm.REGULAR_CIRCULAR_QUEUE)
        .add_battle_allies(teams=(team1,))
        .add_battle_allies(teams=(team2,))
        .init_battle()
    )
    assert battle.is_current_player(player=character1)

    def simulate_playing(
        combat_technique_id: IEntityID, spell_id: IEntityID
    ) -> Callable[[ICharacter, ICharacter], None]:
        def playing(player: ICharacter, target_character: ICharacter) -> None:
            player.cast_spell(spell_id=spell_id, target_character=target_character)
            player.apply_combat_technique(combat_technique_id=combat_technique_id, target_character=target_character)

        return playing

    battle.play(playing=simulate_playing(neryo_tchagui.entity_id, hadouken.entity_id))
    assert battle.is_current_player(player=character2)
    assert character1.get_current_stamina_points == MAXIMUS_POINTS - combat_technique_seed
    assert character1.get_current_mana_points == MAXIMUS_POINTS - spell_seed
    assert character1.get_current_life_points == MAXIMUS_POINTS - (spell_seed + combat_technique_seed)
