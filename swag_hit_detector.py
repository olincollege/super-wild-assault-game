'''
Contains the information about game collision between sprites
'''
from typing import Tuple
from pygame import Vector2
from swag_player import Player
from swag_helpers import CollisionBox, sign


class HitDetector:
    '''
    Used to calculate collisions between players.
    '''

    def __init__(self, players: Tuple[Player, Player]):
        '''
        Creates a HitDetector.

        Args:
            players (Tuple[Player, Player]): A tuple of both players in the
                game.
        '''
        self.__players = players

    def get_collision_boxes(self) -> dict:
        '''
        Gets the collision boxes for the current frame of both players'
        animations.

        Returns:
            player_collision_boxes (dict): The collision hit and hurt boxes
                shifted to the proper positions based on the player locations.
        '''
        player_collision_boxes = {}
        for player in self.__players:
            # initialize boxes at un-shifted locations
            collision_boxes = {
                'hurt': [CollisionBox(*tuple(box))
                         for box in player.current_animation.current_hurtboxes],
                'hit': [CollisionBox(*tuple(box))
                        for box in player.current_animation.current_hitboxes]}
            for box_type in collision_boxes:
                # move the boxes to their proper locations relative to players
                for index in range(len(collision_boxes[box_type])):
                    collision_rect = collision_boxes[box_type][index].rect.move(
                        player.rect.x, player.rect.y)
                    if player.facing_left:
                        collision_rect.move_ip(
                            -2*abs(collision_rect.right-player.pos.x) +
                            collision_rect.w, 0)
                    collision_boxes[box_type][index] = collision_boxes\
                        [box_type][index]._replace(rect=collision_rect)
            # store the updated collision boxes
            player_collision_boxes[player.player_number] = collision_boxes
        return player_collision_boxes

    def player_collision(self):
        '''
        Calculates the collisions between players
        '''
        # Get all the collision hit and hurt boxes in game
        player_collision_boxes = self.get_collision_boxes()

        for hurt_player in self.__players:
            for hurtbox in player_collision_boxes[hurt_player.player_number][
                    'hurt']:
                # Set up which hitbox that that connect to character hurtbox
                hit_player_num = 1
                if hurt_player.player_number == 1:
                    hit_player_num = 2
                hurt_rect = hurtbox.rect
                # check if a collision happened
                collision = hurt_rect.collidelist(
                    [hitbox.rect for hitbox in player_collision_boxes[
                        hit_player_num]['hit']])
                # apply damage and knockback to a player if they got hit
                if collision != -1:
                    collision_box = player_collision_boxes[hit_player_num][
                        'hit'][collision]
                    self.__players[hurt_player.player_number-1].attacked(
                        collision_box.damage,
                        collision_box.knockback_scale,
                        Vector2(sign(-1*self.__players[hit_player_num-1].
                                     facing_left)
                                * abs(collision_box.knockback_x),
                                collision_box.knockback_y))
