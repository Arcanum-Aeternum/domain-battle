from typing import Generator

from domain import EventDispatcher
from domain.battle import Battle, IBattle
from domain.battle.value_objects import BattleAllies, IBattleAllies, ITeam, PassTurnAlgorithmEnum, Team
from domain.character import Character, ICharacter
from domain.skill.combat_technique import CombatTechnique, ICombatTechnique
from domain.skill.spell import ISpell, Spell
from domain.value_objects import EntityID

MAXIMUS_POINTS = 100


def fake_combat_technique(seed: int) -> ICombatTechnique:
    return CombatTechnique.create_new(
        entity_id=EntityID(),
        name=str(seed),
    ).specify_combat_technique_properties(
        stamina_cost=seed,
        damage=seed,
        cooldown=seed,
    )


def fake_spell(seed: int) -> ISpell:
    return Spell.create_new(
        entity_id=EntityID(),
        name=str(seed),
    ).specify_spell_properties(
        mana_cost=seed,
        damage=seed,
        cooldown=seed,
    )


def fake_character(
    name: str,
    seed: int,
    combat_technique_quantity: int,
    spell_quantity: int,
) -> ICharacter:
    skill_builder = Character.create_new(
        entity_id=EntityID(),
        name=name,
    ).specify_skill_properties(
        life_points=MAXIMUS_POINTS,
        stamina_points=MAXIMUS_POINTS,
        mana_points=MAXIMUS_POINTS,
    )
    combat_techniques = [fake_combat_technique(seed) for _ in range(combat_technique_quantity)]
    spells = [fake_spell(seed) for _ in range(spell_quantity)]
    return skill_builder.add_skills(*combat_techniques, *spells)


def fake_character_gen(seed: int, character_quantity: int) -> Generator[ICharacter, None, None]:
    yield from (fake_character(str(seed), seed, seed, seed) for _ in range(character_quantity))


def fake_team(*characters: ICharacter) -> ITeam:
    team_builder = Team.create_new()
    for character in characters:
        team_builder = team_builder.add_character(character)
    return team_builder.build()


def fake_team_gen(seed: int, team_quantity: int, character_quantity: int) -> Generator[ITeam, None, None]:
    yield from (
        fake_team(*list(character for character in fake_character_gen(seed, character_quantity)))
        for _ in range(team_quantity)
    )


def fake_battle_allies(*teams: ITeam) -> IBattleAllies:
    battle_allies_builder = BattleAllies.create_new()
    for team in teams:
        battle_allies_builder = battle_allies_builder.add_team(team)
    return battle_allies_builder.build()


def fake_battle_allies_gen(
    seed: int,
    battle_allies_quantity: int,
    team_quantity: int,
    character_quantity: int,
) -> Generator[IBattleAllies, None, None]:
    yield from (
        fake_battle_allies(*list(team for team in fake_team_gen(seed, team_quantity, character_quantity)))
        for _ in range(battle_allies_quantity)
    )


def fake_battle(
    event_dispatcher: EventDispatcher,
    pass_turn_algorithm_enum: PassTurnAlgorithmEnum,
    *battle_allies_tuple: IBattleAllies
) -> IBattle:
    battle_builder = Battle.create_new(event_dispatcher=event_dispatcher, entity_id=EntityID(), is_battle_ongoing=False)
    for battle_allies in battle_allies_tuple:
        battle_builder = battle_builder.add_battle_allies(battle_allies)
    return battle_builder.specify_pass_turn_algorithm(pass_turn_algorithm_enum)
