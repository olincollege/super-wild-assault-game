'''
Controllers for each player in the game (P1 and P2).
'''
from abc import ABC, abstractmethod
import pygame
from swag_player import Player


class SwagInputHandler(ABC):  # pylint: disable=too-few-public-methods
    '''
    Docstring lol
    '''

    def __init__(self, player: Player) -> None:
        '''
        [summary]

        Args:
            player (Player): [description]
        '''
        self._player = player

    @abstractmethod
    def poll_input(self):
        '''
        [summary]
        '''


class PygameInput(SwagInputHandler):  # pylint: disable=too-few-public-methods
    '''
    Docstring lol
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
        [summary]

        Args:
            player (Player): [description]
        '''
        super().__init__(player)
        self._keybinds = self.keybinds[player.player_number]

    def poll_input(self):
        '''
        [summary]
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
