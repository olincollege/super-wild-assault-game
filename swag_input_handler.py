'''
Controllers for each player in the game (P1 and P2).
'''
from abc import ABC, abstractmethod
import pygame
from swag_player import Player


class SwagInputHandler(ABC):  # pylint: disable=too-few-public-methods
    '''
    An abstract base class for the input handler.
    Attributes:
        _player (Player): The player controlled by the input handler
    '''

    def __init__(self, player: Player) -> None:
        '''
        Creates the input handler
        '''
        self._player = player

    @abstractmethod
    def poll_input(self):
        '''
        Grabs input from whatever input source is being used.
        Should call Player.action().
        '''


class PygameInput(SwagInputHandler):  # pylint: disable=too-few-public-methods
    '''
    An input handler utilizing pygame events.
    Attributes:
        _keybinds (dict): A dict representing each player of a dict connecting
        the possible inputs to a specific move.
    '''

    keybinds = {
        1: {
            pygame.K_UP: 'jump',
            pygame.K_LEFT: 'left',
            pygame.K_RIGHT: 'right',
            pygame.K_PERIOD: 'jab',
            pygame.K_COMMA: 'block'
        },
        2: {
            pygame.K_w: 'jump',
            pygame.K_a: 'left',
            pygame.K_d: 'right',
            pygame.K_c: 'jab',
            pygame.K_v: 'block'
        }
    }

    def __init__(self, player: Player) -> None:
        '''
        Creates an input handler.

        Args:
            player (Player): The player controlled by the input handler
        '''
        super().__init__(player)
        self._keybinds = self.keybinds[player.player_number]

    def poll_input(self):
        '''
        Set the current action according to the current inputs on the keyboard
        and the keybinds as defined above
        '''
        keys_pressed = pygame.key.get_pressed()
        player_keys_pressed = {}
        for key in self._keybinds:
            player_keys_pressed[key] = keys_pressed[key]
        for key in self._keybinds:
            if keys_pressed[key]:
                self._player.action(self._keybinds[key])
        if not any(player_keys_pressed.values()):
            self._player.action('idle')
