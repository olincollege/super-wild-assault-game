'''
SWAG game view - displays sprites.
'''
from abc import ABC, abstractmethod
from typing import Tuple
import pygame
from swag_player import Player
from swag_stage import SwagStage, SwagStageBackground, SwagBarriers


class SwagView(ABC):
    '''
    An abstract base class representing the view of the game. The abstract
    still utilizes pygame sprite groups because the other view implementation
    planned to still use a pygame surface to render the sprites, but draw the
    actual results elsewhere.
    Attribute:
        _background (SwagStageBackground): Current instance of the background
        _stage (SwagStage):  Current instance of the stage
        _left_barrier (SwagBarriers): The left barrier of the pygame window
        _right_barrier (SwagBarriers): The right barrier of the pygame window
        all_sprites: All of the sprites for the game to display
        _fps (integer): Frames per second
        clock: Advances the frames of the game
    '''

    def __init__(self, background: SwagStageBackground, stage: SwagStage,
                 barriers: Tuple[SwagBarriers, SwagBarriers],
                 players: Tuple[Player, Player]) -> None:
        '''
        Creates a SwagView instance.
        Args:
            background (SwagStageBackground): Current instance of the background
            stage (SwagStage): Current instance of the stage
            barriers (tuple): A tuple of the barriers to display (in case images
                are added later)
            player (tuple): A tuple of the players to display.
        '''
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
    A view implementation based on pygame.
    Attributes:
        displaysurface: Surface representing the game window
        _background (SwagStageBackground): Current instance of the background
        all_sprites: All of the sprites for the game to display
        _clock: Advances the frames of the game
    '''

    def __init__(self, background: SwagStageBackground, stage: SwagStage,
                 barriers: Tuple[SwagBarriers, SwagBarriers], players: Tuple[
                     Player, Player]):
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
