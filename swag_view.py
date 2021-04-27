'''
SWAG game view.
'''
from abc import ABC, abstractmethod
import pygame
from pygame.locals import *
from swag_scene import SwagScene

class SwagView(ABC):
    '''
    Docstring
    '''
    def ___init___(self, scene: SwagScene) -> None:
        self.__scene = scene
    
    @property
    def scene(self):
        '''
        Return the value of private scene attribute.
        '''
        return self.__scene
    
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
    def ___init___(self, PT1, P1, P2):
        # Use to show sprites
        all_sprites = pygame.sprite.Group()
        all_sprites.add(PT1) # platform
        all_sprites.add(P1) # player 1
        all_sprites.add(P2) # player 2
        self.all_sprites = all_sprites
        # Set up game window
        HEIGHT = 500 # Window height
        WIDTH = 500 # Window width
        self.FPS = 60
        self.FramePerSec = pygame.time.Clock()
        self.displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
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
        self.FramePerSec.tick(self.FPS)
        pass
