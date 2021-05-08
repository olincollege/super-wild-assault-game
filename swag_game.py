'''
Swag Game 👍
'''

import sys
import pygame
from pygame.locals import QUIT
from swag_player import Player
from swag_stage import SwagStage, SwagStageBackground, SwagBarriers
from swag_view import PygameView
from swag_input_handler import PygameInput
from swag_hit_detector import HitDetector


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
    HIT_DETECTOR = HitDetector((P1, P2))
    CONTROLLERS = [PygameInput(P1), PygameInput(P2)]

    # used to close the game when someone wins
    GAME_END = False

    VIEW.draw()

    # game loop 
    while True:
        for event in pygame.event.get():
            # Will run when the close window button is clicked
            if event.type == QUIT or GAME_END:
                pygame.quit()
                sys.exit()
        if not P1.lost and not P2.lost:
            for controller in CONTROLLERS:
                controller.poll_input()
        elif not GAME_END:
            print(f'{P2.character_name * P1.lost}{P1.character_name * P2.lost}' + \
                    ' wins! Restart the game to play again.')
            GAME_END = True

        # check collisions then update p1 and p2
        HIT_DETECTOR.player_collision()
        P1.update()
        P2.update()
        VIEW.draw()
