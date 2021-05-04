'''
docstring moment
'''
import os
from math import copysign
import pygame
import json
from typing import NamedTuple
from pygame import Vector2
from swag_animation import Animation
from swag_stage import SwagStage
from swag_collision import SwagCollisionSprite

def hitbox_collision(sprite1, sprite2):
    '''
    Check if two hitboxes collide
    '''
    return sprite1.collision.colliderect(sprite2.collision)

class Player(SwagCollisionSprite):

    def __init__(self, player_number: int, character: str, stage: SwagStage, barriers: list) -> None:
        super().__init__()
        self._stage = stage
        self._barriers = barriers

        self._character = character
        self._player_number = player_number
        self.surf = pygame.image.load(os.path.join('chars', character, 'sprites', 'idle',
            f'{character}_idle-1.png'))
        self.rect = self.surf.get_rect(center = (500, 250))

        # import physics properties from file
        with open(os.path.join('chars', character, f'{character}.info'), 'r') as info_file:
            self._properties = PlayerProperties(**(json.load(info_file)))

        self.pos = Vector2((500,500))
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)
        self.knockback_acc = Vector2(0,0)
        self.controlled_acc = Vector2(0,0)
        self._facing_left = False
        self._flip = False

        self._hitstun = False
        self._locked_animation = False
        self._is_walking = False

        # stage collisions
        self._stage_group = pygame.sprite.Group()
        self._stage_group.add(self._stage)
        # barrier collisions
        self._barrier_group = pygame.sprite.Group()
        for barrier_sprite in self._barriers:
            self._barrier_group.add(barrier_sprite)

        self.moves = ['block','hit','idle','jab','jump','land', 'walk']
        self._animations = {move: Animation(self._character, move) for move in self.moves}
        self._current_animation = self._animations['idle']  # type: Animation

    @property
    def player_number(self):
        return self._player_number

    def start_idle(self):
        self._current_animation.reset()
        self._current_animation = self._animations['idle']

    def action(self, action):
        # determine which animation is being asked for
        new_animation = action
        if action == 'left' or action == 'right':
            new_animation = 'walk'

        # TODO: add "state" to animations: list of air or ground to show where the animation is
        # allowed to play, and modify the block below to use that.

        # if prior move not the same and animation is ok to switch, reset animation frame then
        # change current animation
        if self._current_animation.move != new_animation and not self._locked_animation:
            if not (new_animation == 'jump' and self._jumping): # make sure you can't double jump
                self._current_animation.reset()
                self._current_animation = self._animations[new_animation]

        # TODO: add aerial drift separate from walk animation

        # special cases for when the player should be moving around
        # walking:
        if self._current_animation.move == 'walk':
            self._is_walking = True
            if action == 'left':
                self.controlled_acc.x = -self._properties.ground_accel
                if not self._facing_left:
                    self._facing_left = True
            if action == 'right':
                self.controlled_acc.x = self._properties.ground_accel
                if self._facing_left:
                    self._facing_left = False
        else:
            self._is_walking = False
        
        # jumping:
        if self._current_animation.move == 'jump' and not self._jumping:
            self._jumping = True
            self.controlled_acc.y = self._properties.jump_accel

    def update(self):
        sign = lambda x : copysign(1, x)

        # add appropriate resistive force depending on whether or not the player is on the ground
        friction_acc = 0
        if not self.controlled_acc.x:
            if self._stage_collision():
                friction_acc = self._properties.traction * -sign(self.vel.x) * (abs(self.vel.x) > 0)
            else:
                friction_acc = self._properties.air_accel * -sign(self.vel.x) * (abs(self.vel.x) > 0)

        self.acc.x += friction_acc

        # if in hitstun, make controlled acceleration much smaller
        if self._hitstun:
            self.controlled_acc.x *= .2
            self.controlled_acc.y *= .2
        self.acc.y += self.controlled_acc.y     # jump accel, DI
        self.acc.y += self._properties.gravity  # fall acceleration
        self.acc += self.knockback_acc          # knockback
        self.acc.x += self.controlled_acc.x     # walk accel, DI

        self.vel += self.acc    # update velocity

        # apply ground speed cap
        if abs(self.vel.x) > self._properties.ground_speed and self._is_walking:
            self.vel.x = self._properties.ground_speed * sign(self.vel.x)

        # stop the player if their speed is below a threshold
        if abs(self.vel.x) < .3:
            self.vel.x = 0

        # update the sprite and bounding box for the current animation
        self.surf = self._current_animation.update_frame()
        self.rect = self.surf.get_rect(center = (self.pos.x, self.pos.y))
        # mirror the sprite horizontally if the player is facing left
        if self._facing_left:
            self.surf = pygame.transform.flip(self.surf, True, False)

        self._stage_collision_check()   # if player is on the ground, don't let them fall through
        self._barrier_collision_check() # if the player is crossing over a window barrier

        self.pos += self.vel + 0.5 * self.acc   # update position based on current vel and accel
        self.rect.midbottom = self.pos

        # reset accelerations so things don't fly out of control
        self.controlled_acc.x = 0
        self.controlled_acc.y = 0
        self.knockback_acc.x = 0
        self.knockback_acc.x = 0
        self.acc.x = 0
        self.acc.y = 0

    def _stage_collision(self):
        return pygame.sprite.spritecollide(self, self._stage_group, False, collided=hitbox_collision)

    def _stage_collision_check(self):
        stage_collisions = self._stage_collision()
        if self.vel.y > 0:
            if stage_collisions:
                lowest = stage_collisions[0]
                # Don't let players drop below lowest point
                if self.pos.y < lowest.collision.bottom:
                    self.pos.y = lowest.collision.top + 1
                    self.vel.y = 0
                    self.acc.y = 0
                    self._jumping = False
                    self._locked_animation = False # fix later

    def _barrier_collision(self):
        return pygame.sprite.spritecollide(self, self._barrier_group, False, collided=hitbox_collision)

    
    def _barrier_collision_check(self):
        barrier_collisions = self._barrier_collision()
        if barrier_collisions:
            first_collision = barrier_collisions[0]
            collision_location = first_collision.collision.left
            if self.pos.x < 0 and self.vel.x < 0:
                self.pos.x = collision_location + 1
                self.vel.x = 0
                self.acc.x = 0
            if collision_location != 0:
                max_collision = collision_location
                if self.pos.x > max_collision and self.vel.x > 0:
                    self.pos.x = collision_location - 1
                    self.vel.x = 0
                    self.acc.x = 0
            # Stop movement
            print(first_collision.collision.left)


    def attacked(self, damage, base_knockback, knockback_direction):
        pass


class PlayerProperties(NamedTuple):
    name: str
    health: int
    ground_accel: float
    ground_speed: float
    air_accel: float
    air_speed: float
    weight: float
    gravity: float
    fall_speed: float
    jump_accel: float
    traction: float
