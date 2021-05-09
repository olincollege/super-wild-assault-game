"""
Test helper functions to aid with the game.
"""
import pytest
from swag_healthbar import SwagHealthBar

BLANK_BLACK_SOLID_COLOR = (0, 0, 0, 255)
WHITE_SOLID_COLOR = (255, 255, 255, 255)
RED_SOLID_COLOR = (255, 0, 0, 255)
YELLOW_SOLID_TRANSITION_COLOR = (255, 255, 0, 255)
BACKGROUND_COLOR = (44, 38, 69, 255)

test_init_health_cases = [(3),(200),(-100),(0),(0.1),(150)]
test_damage_cases = [(1), (150), (0),(0),(-1),(125)]
test_health_to_damage_cases = [(test_init_health_cases[index],\
    test_damage_cases[index]) for index in range(len(test_damage_cases))]

@pytest.mark.parametrize("max_health",test_init_health_cases)
def test_healthbar_init_health(max_health):
    """
    Check that initial configuration sets up the correct values for health.
    Args:
        max_health: maximum amount of health for character
    """
    test_player1 = SwagHealthBar(1,max_health)
    # Check that the player target health is set correctly
    assert test_player1.target_health == max_health
    # Check that the player current health is set correctly
    assert test_player1.current_health == max_health
    # Check that the player health ratio for the healthbar is correct
    assert test_player1.health_ratio == max_health/400

def test_healthbar_init_rect():
    """
    Check that initial configuration sets up the correct position and scale.
    """
    test_player1 = SwagHealthBar(1,100)
    test_player2 = SwagHealthBar(2,100)
    # Test that the player 1 healthbox left x position is correct
    assert test_player1.rect.x == 550
    # Test that the player 1 healthbox top y position is correct
    assert test_player1.rect.y == 45
    # Test that the player 1 healthbox left x position is correct
    assert test_player2.rect.x == 50
    # Test that the player 2 healthbox top y position is correct
    assert test_player2.rect.y == 45
    # Check that the player 1 healthbar width is correct
    assert test_player1.rect.width == test_player1.health_bar_length
    # Check that the player 2 healthbar width is correct
    assert test_player2.rect.width == test_player2.health_bar_length
    # Check that the player healthbar height is correct
    assert test_player1.rect.height == 25 # constant state
    # Check that the healthbar colors at specific locations are correct
    # Non-drawn healthbar
    assert test_player1.surf.get_at((200,15)) == BLANK_BLACK_SOLID_COLOR
    assert test_player2.surf.get_at((200,15)) == BLANK_BLACK_SOLID_COLOR

@pytest.mark.parametrize("max_health, damage",test_health_to_damage_cases)
def test_healthbar_damage(max_health, damage):
    """
    Check that damage function works correctly with target health.
    Args:
        max_health: integer of the maximum amount of health
        damage: integer of the total amount of damage taken
    """
    test_player1 = SwagHealthBar(1,max_health)
    test_player1.damage(damage)
    # Test that the damage function changed the target health correctly
    assert  test_player1.target_health == max_health - damage

def test_healthbar_update_bar():
    """
    Check healthbar is changed by other functions.
    """
    test_player1 = SwagHealthBar(1,100)
    test_player2 = SwagHealthBar(2,100)
    test_player1.update_bar()
    test_player2.update_bar()
    # Test that the current health is the same as target health, no damage
    assert test_player1.current_health == test_player1.target_health
    # Check that the healthbar colors are still correct
    # Player healthbar borders:
    assert test_player1.surf.get_at((0,0)) == WHITE_SOLID_COLOR
    assert test_player2.surf.get_at((0,0)) == WHITE_SOLID_COLOR
    # Player healthbar health:
    assert test_player1.surf.get_at((200,15)) == RED_SOLID_COLOR
    assert test_player2.surf.get_at((200,15)) == RED_SOLID_COLOR
    # Damage players
    test_player1.damage(50) # half health
    test_player2.damage(99) # near-zero health
    test_player1.update_bar() # one tick
    test_player2.update_bar()
    # Check transition bar works correctly
    assert test_player1.surf.get_at((395,5)) == YELLOW_SOLID_TRANSITION_COLOR
    assert test_player2.surf.get_at((5,5)) == YELLOW_SOLID_TRANSITION_COLOR
    # Check that current health (real health) is still less than target health
    assert test_player1.current_health > test_player1.target_health
    assert test_player2.current_health > test_player2.target_health
    # go through 45 more ticks for near-half point
    for _ in range(45):
        test_player1.update_bar()
        test_player2.update_bar()
    # Check empty healthbar is background color
    assert test_player1.surf.get_at((220,5)) == BACKGROUND_COLOR
    assert test_player2.surf.get_at((180,5)) == BACKGROUND_COLOR
    # Check that bar is still changing in transition color
    assert test_player1.surf.get_at((200,5)) == YELLOW_SOLID_TRANSITION_COLOR
    assert test_player2.surf.get_at((395,5)) == YELLOW_SOLID_TRANSITION_COLOR
    # Check that bar has correct red health
    assert test_player1.surf.get_at((195,5)) == RED_SOLID_COLOR # Half health
    assert test_player2.surf.get_at((396,5)) == RED_SOLID_COLOR # Low health
    # go through complete amount needed ticks for 99 damage
    for _ in range(53):
        test_player1.update_bar()
        test_player2.update_bar()
    # Check that former transition area is now background color
    assert test_player1.surf.get_at((200,5)) == BACKGROUND_COLOR
    assert test_player2.surf.get_at((395,5)) == BACKGROUND_COLOR
    # Check that red health is correct
    assert test_player1.surf.get_at((195,5)) == RED_SOLID_COLOR # Half health
    assert test_player2.surf.get_at((396,5)) == RED_SOLID_COLOR # Low health
    # Check that current health and target health are now the same after loop
    assert test_player1.current_health == test_player1.target_health
    assert test_player2.current_health == test_player2.target_health


