'''
Test the controller / input handler for S.W.A.G.
'''
import pytest
import pygame
from swag_input_handler import PygameInput

# Create mock player class to test inputs with


class PlayerMock:  # pylint: disable=too-few-public-methods
    '''
    Mock Player class to return inputs needed
    Attributes:
            player_number: integer representing the player
            action_list: list representing the recent action due to input
    '''

    def __init__(self, player_number):
        '''
        Create a mock player
        '''
        self.player_number = player_number
        self.action_list = []

    def reset(self):
        '''
        Resets the action list
        '''
        self.action_list = []

    def action(self, action):
        '''
        Returns the current action
        '''
        self.action_list.append(action)

# Helper function for key inputs


def mock_key_input(key_input):
    '''
    Takes a key input and posts it as a pygame KEYDOWN event.
    '''
    newevent = pygame.event.Event(
        pygame.KEYDOWN, key=key_input)  # create the event
    pygame.event.post(newevent)  # add the event to the queue


# All possible key inputs
KEY_DICT = {'UP': pygame.K_UP, 'W': pygame.K_w,
            'LEFT': pygame.K_LEFT, 'A': pygame.K_a,
            'RIGHT': pygame.K_RIGHT, 'S': pygame.K_s,
            'PERIOD': pygame.K_PERIOD, 'C': pygame.K_c,
            'COMMA': pygame.K_COMMA, 'V': pygame.K_v,
            'SPACE': pygame.K_SPACE}

# For testing expected actions
KEYBIND_TO_ACTION_CASES = [(KEY_DICT['UP'],     KEY_DICT['W'], 'jump'),
                           (KEY_DICT['LEFT'],   KEY_DICT['A'], 'left'),
                           (KEY_DICT['RIGHT'],  KEY_DICT['S'], 'right'),
                           (KEY_DICT['PERIOD'], KEY_DICT['C'], 'jab'),
                           (KEY_DICT['COMMA'],  KEY_DICT['V'], 'block')]

# Skip explanation below
@pytest.mark.skip(
    reason='''No way of currently testing this. We attempted using Pynput, but
    it didn't work because the game didn't have keyboard focus. We also tested
    using pygame.Events, however, it's not detected by 
    pygame.keys.get_pressed.''')
@pytest.mark.parametrize("player1_key, player2_key, expected_action",
                         KEYBIND_TO_ACTION_CASES)
def test_poll_input(player1_key, player2_key, expected_action):
    '''
    Tests for whether or not inputs lead to expected action from the player.
    Args:
        player1_key: pygame key input for player 1 leading to expected action
        player2_key: pygame key input for player 2 leading to expected action
        expected_action: the move following the input, such as jump or left
    '''
    pygame.init()
    # Create mock players
    player_1 = PlayerMock(1)
    player_2 = PlayerMock(2)
    # Create mock controllers
    controller_1 = PygameInput(player_1)
    controller_2 = PygameInput(player_2)
    # Test for only Player 1 inputs
    pygame.event.clear()
    mock_key_input(player1_key)
    mock_key_input(player2_key)
    controller_1.poll_input()
    controller_2.poll_input()
    assert player_1.action_list == [expected_action]
    assert player_2.action_list == ['idle']
