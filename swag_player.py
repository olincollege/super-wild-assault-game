'''
docstring moment
'''
import os
import pygame
from pygame import Vector2
from swag_animation import Animation
from swag_stage import SwagStage

def hitbox_collision(sprite1, sprite2):
    """
    Check if two hitboxes collide
    """
    if hasattr(sprite1, 'hitbox'):
        hitbox1 = sprite1.hitbox
    else:
        hitbox1 = sprite1.rect

    if hasattr(sprite2, 'hitbox'):
        hitbox2 = sprite2.hitbox
    else:
        hitbox2 = sprite2.rect
    return hitbox1.colliderect(hitbox2)

class Player(pygame.sprite.Sprite):

    def __init__(self, player_number: int, character: str, stage: SwagStage) -> None:
        super().__init__()
        self._stage = stage
        self._character = character
        self._player_number = player_number
        self.surf = pygame.image.load(os.path.join('chars', character, 'sprites', 'idle',
            f'{character}_idle-1.png'))
        self.rect = self.surf.get_rect(center = (500, 250))
        
        self._walk_accel = .3
        self._walk_speed_cap = 3
        self._weight = 1

        self.pos = Vector2((500,500))
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)
        self._facing_left = False
        self._flip = False

        self._locked_animation = False
        self._is_walking = False

        self._stage_group = pygame.sprite.Group()
        self._stage_group.add(self._stage)

        self.moves = ['block','hit','idle','jab','jump', 'walk']
        self._animations = {move: Animation(self._character, move) for move in self.moves}
        self._current_animation = self._animations['idle']  # type: Animation

    @property
    def player_number(self):
        return self._player_number

    def action(self, action):
        # determine which animation is being asked for
        new_animation = action
        if action == 'left' or action == 'right':
            new_animation = 'walk'

        # if prior move not the same and animation is ok to switch, reset animation frame then
        # change current animation
        if self._current_animation.move != new_animation and not self._locked_animation:
            self._current_animation.reset()
            self._current_animation = self._animations[new_animation]

        # special cases for when the player should be moving around
        # walking:
        if self._current_animation.move == 'walk':
            self._is_walking = True
            if action == 'left':
                self.acc.x = -self._walk_accel
                if not self._facing_left:
                    self._facing_left = True
            if action == 'right':
                self.acc.x = self._walk_accel
                if self._facing_left:
                    self._facing_left = False
        else:
            self._is_walking = False
        
        # jumping:
        if self._current_animation.move == 'jump':
            self._jumping = True
            self.vel.y = -10
        
        # If the action is idle and knockback etc. not applied
        if action == 'idle' and not self._locked_animation:
            self.vel.x = 0
            self.acc.x = 0

    def update(self):
        self.acc.y += self._stage.gravity * self._weight
        self.acc.x += self.vel.x * self._stage.friction
        self.vel += self.acc

        if self.vel.x > self._walk_speed_cap and self._is_walking:
            self.vel.x = self._walk_speed_cap

        self.surf = self._current_animation.update_frame()
        self.rect = self.surf.get_rect(center = (self.pos.x, self.pos.y))
        if self._facing_left:
            self.surf = pygame.transform.flip(self.surf, True, False)

        self._stage_collision_check()

        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

    def _stage_collision_check(self):
        collisions = pygame.sprite.spritecollide(self, self._stage_group, False, collided=hitbox_collision)
        if self.vel.y > 0:
            if collisions:
                lowest = collisions[0]
                if hasattr(lowest, 'hitbox'):
                    hitbox_ground = lowest.hitbox
                else:
                    hitbox_ground = lowest.rect
                # Don't let players drop below lowest point
                if self.pos.y < hitbox_ground.bottom:
                    self.pos.y = hitbox_ground.top + 1
                    self.vel.y = 0
                    self.acc.y = 0
                    self._jumping = False
                    self._locked_animation = False # fix later

    def attacked(self, damage, base_knockback, knockback_direction):
        pass
