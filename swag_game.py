'''
Swag Game 👍
'''

from swag_stage import SwagStage
from swag_stage import SwagStageBackground
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

    # create players
    P1 = Player(1, 'olinman', STAGE)
    P2 = Player(2, 'catboy', STAGE)

    VIEW = PygameView(BACKGROUND,STAGE, P1, P2)

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
