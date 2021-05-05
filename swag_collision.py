'''
Contains the information about game collision between sprites
'''
import pygame
from typing import Tuple
from swag_stage import SwagStage, SwagBarriers
from swag_player import Player
from pygame import Rect, Vector2
from swag_collisionsprite import SwagCollisionSprite

class CollisionHandler:
    def __init__(self, stage: SwagStage, barriers: list, players: Tuple[Player, Player]):
        self.__stage = stage
        self.__barriers = barriers
        self.__players = players

        self._stage_group = pygame.sprite.Group()
        self._stage_group.add(self.__stage)

        self._barrier_group = pygame.sprite.Group()
        for barrier_sprite in self.__barriers:
            self._barrier_group.add(barrier_sprite)

    def player_collision(self):

        player_hurtboxes = {player.player_number: player.current_animation.current_hurtboxes
                            for player in self.__players}
        player_hitboxes = {player.player_number: player.current_animation.current_hitboxes
                            for player in self.__players}
        # print(player_hurtboxes)
        # print(player_hitboxes)
        # tuple(Rect(hurtbox.x, hurtbox.y, hurtbox.width, hurtbox.height))

        # check if player 2 hit player 1 
        for hurtbox in player_hurtboxes[1]:
            # print(hurtbox)
            collision = hurtbox.rect.collidelist([hitbox.rect for hitbox in player_hitboxes[2]])
            if collision != -1:
                collision_box = player_hitboxes[2][collision]
                self.__players[0].attacked(collision_box.damage, collision_box.knockback_scale, Vector2(collision_box.knockback_x, collision_box.knockback_y))

        # iterate through player's hurtboxes
        #   if hurtbox collides with other player's hitbox, apply knockback and damage corresponding to hitbox


    def _hitbox_collision(self, sprite1: SwagCollisionSprite, sprite2: SwagCollisionSprite) -> bool:
        '''
        Check if two hitboxes collide
        '''
        return sprite1.collision.colliderect(sprite2.collision)