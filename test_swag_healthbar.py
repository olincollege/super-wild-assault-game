"""
Test helper functions to aid with the game.
"""
import pytest
from swag_healthbar import SwagHealthBar


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
    assert test_player1.target_health == max_health
    assert test_player1.current_health == max_health
    assert test_player1.health_ratio == max_health/400

def test_healthbar_init_rect():
    """
    Check that initial configuration sets up the correct position and scale.
    """
    test_player1 = SwagHealthBar(1,100)
    test_player2 = SwagHealthBar(2,100)
    assert test_player1.rect.x == 550
    assert test_player1.rect.y == 45
    assert test_player2.rect.x == 50
    assert test_player2.rect.y == 45
    assert test_player1.rect.width == test_player1.health_bar_length
    assert test_player2.rect.width == test_player2.health_bar_length
    assert test_player1.rect.height == 25 # constant state

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
    assert  test_player1.target_health == max_health - damage

def test_healthbar_update_bar():
    """
    Check healthbar is changed by other functions.
    """
    test_player1 = SwagHealthBar(1,100)
    test_player2 = SwagHealthBar(2,100)
    assert test_player1.target_health == 100 #not doing this
