'''
Swag Game 👍
'''

from swag_stage import SwagStage, SwagStageBackground, SwagBarriers
import sys
import pygame
from pygame.locals import *     # type: ignore  pylint: disable=wildcard-import
from swag_player import Player
from swag_view import PygameView
from swag_input_handler import PygameInput


if __name__ == '__main__':
    # Initialize pygame
    pygame.init()

    # create stage
    BACKGROUND = SwagStageBackground()
    STAGE = SwagStage(BACKGROUND.WIDTH, BACKGROUND.HEIGHT)
    LEFT_BARRIER = SwagBarriers(BACKGROUND.WIDTH, BACKGROUND.HEIGHT, 0)
    RIGHT_BARRIER = SwagBarriers(BACKGROUND.WIDTH, BACKGROUND.HEIGHT, BACKGROUND.WIDTH)
    BARRIER_SPRITES = [LEFT_BARRIER, RIGHT_BARRIER]
    # create players
    P1 = Player(1, 'olinman', STAGE, BARRIER_SPRITES)
    P2 = Player(2, 'catboy', STAGE, BARRIER_SPRITES)

    VIEW = PygameView(BACKGROUND,STAGE,LEFT_BARRIER,RIGHT_BARRIER, P1, P2)

    CONTROLLERS = [PygameInput(P1), PygameInput(P2)]

    VIEW.draw()
    while True:
        for event in pygame.event.get():
            # Will run when the close window button is clicked    
            if event.type == QUIT:
                pygame.quit()
                sys.exit() 

        for controller in CONTROLLERS:
            controller.poll_input()
        P1.update()
        P2.update()
        VIEW.draw()
