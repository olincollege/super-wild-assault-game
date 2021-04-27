'''
SWAG game view.
'''
from abc import ABC, abstractmethod
from swag_player import Player
import pygame
from pygame.locals import *     # type: ignore  pylint: disable=wildcard-import
from swag_stage import SwagStage

class SwagView(ABC):
    '''
    Docstring
    '''
    def __init__(self, stage: SwagStage, P1: Player, P2: Player) -> None:
        self.__stage = stage
        self.__P1 = P1
        self.__P2 = P2
        # Use to show sprites
        all_sprites = pygame.sprite.Group()
        all_sprites.add(stage) # platform
        all_sprites.add(P1) # player 1
        all_sprites.add(P2) # player 2
        self.all_sprites = all_sprites
        # Set up game window
        self.__HEIGHT = 1000 # Window height
        self.__WIDTH = 1000 # Window width
        self.__FPS = 60
        self.__FramePerSec = pygame.time.Clock()
    
    @property
    def stage(self):
        '''
        Return the value of private stage attribute.
        '''
        return self.__stage
    
    @property
    def fps(self):
        '''
        Return the FPS of the game.
        '''
        return self.__FPS

    @abstractmethod
    def draw(self):
        '''
        An abstract method that passes the subclass draw function.
        '''
        pass

class PygameView(SwagView):
    '''
    ABC according to an instance of the SWAG game.

    Attributes:
        scene: class representing current instance of game
    '''
    def __init__(self, stage: SwagStage, P1: Player, P2: Player):
        super().__init__(stage, P1, P2)
        self.displaysurface = pygame.display.set_mode((self.__WIDTH, self.__HEIGHT))
        pygame.display.set_caption("S.W.A.G.: Super Wild Assault Game")

    def draw(self):
        '''
        Outputs pygame view of SWAG game.
        '''
        # Default Blank Background
        self.displaysurface.fill((0,0,0))
        # Render game
        for entity in self.all_sprites:
            self.displaysurface.blit(entity.surf, entity.rect)
        pygame.display.update()
        self.__FramePerSec.tick(self.__FPS)
