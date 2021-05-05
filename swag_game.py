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
from swag_collision import CollisionHandler
#from swag_healthbar import SwagHealthBar


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
    # create player healthbars
    #P1HEALTHBAR = pygame.sprite.GroupSingle(SwagHealthBar(50,45,True))
    #P2HEALTHBAR = pygame.sprite.GroupSingle(SwagHealthBar(1000-450,45,False))

    # create view
    VIEW = PygameView(BACKGROUND,STAGE,LEFT_BARRIER,RIGHT_BARRIER, P1, P2)
    collision_handler = CollisionHandler(STAGE, BARRIER_SPRITES, (P1, P2))

    CONTROLLERS = [PygameInput(P1), PygameInput(P2)]

    VIEW.draw()
    while True:
        for event in pygame.event.get():
            # Will run when the close window button is clicked    
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # TODO: actually implement damage
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_DOWN:
            #         P1HEALTHBAR.sprite.get_damage(200)
            #     if event.key == pygame.K_UP:
            #         P2HEALTHBAR.sprite.get_damage(200)

        for controller in CONTROLLERS:
            controller.poll_input()
        # check collisions then update p1 and p2
        collision_handler.player_collision()
        P1.update()
        P2.update()
        VIEW.draw()
        # healthbars
        # P1HEALTHBAR.update()
        # P2HEALTHBAR.update()
