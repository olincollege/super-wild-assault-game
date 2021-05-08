'''
SWAG game view.
'''
from abc import ABC, abstractmethod
from typing import Tuple
import pygame
from swag_player import Player
from swag_stage import SwagStage, SwagStageBackground, SwagBarriers


class SwagView(ABC):
    '''
    Docstring
    '''

    def __init__(self, background: SwagStageBackground, stage: SwagStage,
                 barriers: Tuple[SwagBarriers, SwagBarriers], players: Tuple[Player, Player]) -> None:
        # Set up sprites
        self._background = background
        self._stage = stage
        self._left_barrier = barriers[0]
        self._right_barrier = barriers[1]
        # Use to show sprites
        all_sprites = pygame.sprite.Group()
        all_sprites.add(background)  # background
        all_sprites.add(stage)  # platform
        all_sprites.add(self._left_barrier)  # barrier 1
        all_sprites.add(self._right_barrier)  # barrier 2
        all_sprites.add(players[0])  # player 1
        all_sprites.add(players[1])  # player 2
        all_sprites.add(players[0].healthbar)
        all_sprites.add(players[1].healthbar)
        self.all_sprites = all_sprites
        self._fps = 60
        self._clock = pygame.time.Clock()

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
        return self._fps

    @abstractmethod
    def draw(self):
        '''
        An abstract method that passes the subclass draw function.
        '''


class PygameView(SwagView):
    '''
    ABC according to an instance of the SWAG game.

    Attributes:
        scene: class representing current instance of game
    '''

    def __init__(self, background: SwagStageBackground, stage: SwagStage,
                 barriers: Tuple[SwagBarriers, SwagBarriers], players: Tuple[Player, Player]):
        # Set up window display
        super().__init__(background, stage, barriers, players)
        self.displaysurface = pygame.display.set_mode(
            (self._background.width, self._background.height))
        pygame.display.set_caption("S.W.A.G.: Super Wild Assault Game")

    def draw(self):
        '''
        Outputs pygame view of SWAG game.
        '''
        # Render game
        for entity in self.all_sprites:
            self.displaysurface.blit(entity.surf, entity.rect)

        pygame.display.update()
        self._clock.tick(self._fps)
