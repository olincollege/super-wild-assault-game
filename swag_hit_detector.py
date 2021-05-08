'''
Contains the information about game collision between sprites
'''
from typing import Tuple
from pygame import Vector2
from swag_player import Player
from swag_helpers import CollisionBox, sign


class HitDetector:
    '''
    [summary]
    '''

    def __init__(self, players: Tuple[Player, Player]):
        '''
        [summary]

        Args:
            players (Tuple[Player, Player]): [description]
        '''
        self.__players = players

    def get_collision_boxes(self) -> dict:
        '''
        [summary]

        Returns:
            dict: [description]
        '''
        player_collision_boxes = {}
        for player in self.__players:
            collision_boxes = {
                'hurt': [CollisionBox(*tuple(box))
                         for box in player.current_animation.current_hurtboxes],
                'hit': [CollisionBox(*tuple(box))
                        for box in player.current_animation.current_hitboxes]}
            for box_type in collision_boxes:
                for index in range(len(collision_boxes[box_type])):
                    collision_rect = collision_boxes[box_type][index].rect.move(
                        player.rect.x, player.rect.y)
                    if player.facing_left:
                        collision_rect.move_ip(
                            -2*abs(collision_rect.right-player.pos.x)+collision_rect.w, 0)
                    collision_boxes[box_type][index] = \
                        collision_boxes[box_type][index]._replace(
                            rect=collision_rect)
            player_collision_boxes[player.player_number] = collision_boxes
        return player_collision_boxes

    def player_collision(self):
        '''
        [summary]
        '''
        player_collision_boxes = self.get_collision_boxes()

        for hurt_player in self.__players:
            for hurtbox in player_collision_boxes[hurt_player.player_number]['hurt']:
                hit_player_num = 1
                if hurt_player.player_number == 1:
                    hit_player_num = 2

                hurt_rect = hurtbox.rect
                collision = hurt_rect.collidelist(
                    [hitbox.rect for hitbox in player_collision_boxes[hit_player_num]['hit']])
                if collision != -1:
                    collision_box = player_collision_boxes[hit_player_num]['hit'][collision]
                    self.__players[hurt_player.player_number-1].attacked(
                        collision_box.damage,
                        collision_box.knockback_scale,
                        Vector2(sign(-1*self.__players[hit_player_num-1].facing_left)
                                * abs(collision_box.knockback_x),
                                collision_box.knockback_y))
