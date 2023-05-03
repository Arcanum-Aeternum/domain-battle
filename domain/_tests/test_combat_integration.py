from typing import Callable

import pytest

from domain.character.entity import Character
from domain.character.interfaces import ICharacter
from domain.character.exceptions import ThisCharacterDoesNotHaveThatSpell
from domain.character_spell.entity import CharacterSpell
from domain.character_spell.interfaces import ICharacterSpell
from domain.duel.entity import Duel
from domain.duel.exceptions import DuelIsNotHappeningException
from domain.interfaces import IEntityID
from domain.value_objects import EntityID

MAXIMUS_POINTS = 100


def create_fake_character_spell(name: str, seed: int) -> ICharacterSpell:
    return CharacterSpell.create_new(
        entity_id=EntityID(),
        name=name,
    ).specify_spell_properties(
        mana_cost=seed,
        damage=seed,
        cooldown=seed,
    )


def create_fake_character(name: str, *spells: ICharacterSpell) -> ICharacter:
    return (
        Character.create_new(entity_id=EntityID(), name=name)
        .specify_skill_properties(life_points=MAXIMUS_POINTS, mana_points=MAXIMUS_POINTS)
        .add_spells(*spells)
    )


def test_complete_combat() -> None:
    with pytest.raises(RuntimeError, match="Cannot instantiate directly"):
        CharacterSpell()

    with pytest.raises(RuntimeError, match="Cannot instantiate directly"):
        Character()

    spell_seed = 15
    hadouken = create_fake_character_spell("Hadouken", spell_seed)
    rasengan = create_fake_character_spell("Rasengan", spell_seed)
    chidori = create_fake_character_spell("Chidori", spell_seed)

    player1 = create_fake_character("John Wick", hadouken, rasengan)
    player2 = create_fake_character("Spider Man", chidori)
    player3 = create_fake_character("Spider Man")

    with pytest.raises(ThisCharacterDoesNotHaveThatSpell):
        player3.cast_spell(spell_id=rasengan.entity_id, target_character=player2)

    duel = Duel(entity_id=EntityID(), players=(player1, player2))
    assert duel.is_current_player(player=player1)

    def simulate_playing(spell_id: IEntityID) -> Callable[[ICharacter, ICharacter], None]:
        def playing(player: ICharacter, target_player: ICharacter) -> None:
            player.cast_spell(spell_id=spell_id, target_character=target_player)

        return playing

    with pytest.raises(DuelIsNotHappeningException):
        duel.play(playing=simulate_playing(hadouken.entity_id))

    duel.init_duel()
    duel.play(playing=simulate_playing(hadouken.entity_id))
    assert duel.is_current_player(player=player2)
    assert player1.get_current_mana_points == MAXIMUS_POINTS - spell_seed
    assert player2.get_current_life_points == MAXIMUS_POINTS - spell_seed
