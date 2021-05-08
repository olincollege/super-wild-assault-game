'''
SWAG game view.
'''
from abc import ABC, abstractmethod
from swag_player import Player
import pygame
from swag_stage import SwagStage, SwagStageBackground, SwagBarriers
from swag_healthbar import SwagHealthBar

class SwagView(ABC):
    '''
    Docstring
    '''
    def __init__(self, background: SwagStageBackground, stage: SwagStage, \
        left_barrier : SwagBarriers, right_barrier : SwagBarriers, P1: Player, P2: Player) -> None:
        # Set up sprites
        self._background = background
        self._stage = stage
        self._left_barrier = left_barrier
        self._right_barrier = right_barrier
        self._P1 = P1
        self._P2 = P2
        # Use to show sprites
        all_sprites = pygame.sprite.Group()
        all_sprites.add(background) # background
        all_sprites.add(stage) # platform
        all_sprites.add(left_barrier) # barrier 1
        all_sprites.add(right_barrier) # barrier 2
        all_sprites.add(P1) # player 1
        all_sprites.add(P2) # player 2
        all_sprites.add(P1.healthbar)
        all_sprites.add(P2.healthbar)
        self.all_sprites = all_sprites
        # Set up game window
        self._HEIGHT = self._background.WIDTH # Window height
        self._WIDTH = self._background.HEIGHT # Window width
        self._FPS = 60
        self._FramePerSec = pygame.time.Clock()
    
    @property
    def stage(self):
        '''
        Return the value of private stage attribute.
        '''
        return self._stage
    
    @property
    def fps(self):
        '''
        Return the FPS of the game.
        '''
        return self._FPS

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
    def __init__(self, background: SwagStageBackground, stage: SwagStage, \
        left_barrier : SwagBarriers, right_barrier : SwagBarriers, P1: Player, P2: Player):
        # Set up window display
        super().__init__(background, stage, left_barrier, right_barrier, P1, P2)
        self.displaysurface = pygame.display.set_mode((self._HEIGHT,self._WIDTH))
        pygame.display.set_caption("S.W.A.G.: Super Wild Assault Game")

    def draw(self):
        '''
        Outputs pygame view of SWAG game.
        '''
        # Render game
        for entity in self.all_sprites:
            self.displaysurface.blit(entity.surf, entity.rect)
            
        pygame.display.update()
        self._FramePerSec.tick(self._FPS)
