'''
Controllers for each player in the game (P1 and P2).
'''
from abc import ABC, abstractmethod
from swag_player import Player
import pygame
from pygame.locals import *     # type: ignore  pylint: disable=wildcard-import
from swag_stage import SwagStage

class SwagInputHandler(ABC):
    '''
    Docstring lol
    '''

    def __init__(self, player: Player) -> None:
        self.__player = player

    @abstractmethod
    def poll_input(self):
        pass


class PygameInput(SwagInputHandler):
    '''
    Docstring lol
    '''

    keybinds = {
        1: {
            pygame.K_UP: 'jump',
            pygame.K_LEFT: 'left',
            pygame.K_RIGHT: 'right',
            pygame.K_v: 'attack'
        },
        2: {
            pygame.K_w: 'jump',
            pygame.K_a: 'left',
            pygame.K_d: 'right',
            pygame.K_PERIOD: 'attack'
        }
    }

    def __init__(self, player: Player) -> None:
        super().__init__(player)
        self.__keybinds = self.keybinds[player]

    def poll_input(self):
        keys_pressed = pygame.key.get_pressed()
        for key in self.__keybinds:
            if keys_pressed[key]:
                self.__player.action(self.__keybinds[key])
