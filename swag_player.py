'''
docstring moment
'''
import os
import pygame
import json
from pygame import Vector2
from swag_animation import Animation
from swag_stage import SwagStage
from swag_collisionsprite import SwagCollisionSprite
from swag_helpers import sign, PlayerPhysics, MoveInfo
from swag_healthbar import SwagHealthBar


class Player(SwagCollisionSprite):
    def __init__(self, player_number: int, character: str, stage: SwagStage, barriers: list) -> None:
        super().__init__()
        self._stage = stage
        self._barriers = barriers

        self._character = character
        self._player_number = player_number
        self.surf = pygame.image.load(os.path.join('chars', character, 'sprites', 'idle',
            f'{character}_idle-1.png'))
        
        # set up starting location
        if self._player_number == 1:
            self.rect = self.surf.get_rect(center = (750, 250))
            self.pos = Vector2((750,250))
            self._facing_left = True
        elif self._player_number == 2:
            self.rect = self.surf.get_rect(center = (250, 250))
            self.pos = Vector2((250,250))
            self._facing_left = False

        # import character properties from file
        with open(os.path.join('chars', character, f'{character}.info'), 'r') as info_file:
            prop_dict = json.load(info_file)
            self._name = prop_dict['name']
            self._health = prop_dict['health']
            self._physics = PlayerPhysics(**(prop_dict['physics']))
            self._moves = prop_dict['moves']
        
        # set up win/loss condition
        self._loss = False
        
        # set up healthbar
        self.healthbar = SwagHealthBar(self._player_number,self._health)


        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)
        self.knockback_acc = Vector2(0,0)
        self.controlled_acc = Vector2(0,0)
        self._flip = False

        self._hitstun = False
        self._in_air = True

        # stage collisions
        self._stage_group = pygame.sprite.Group()
        self._stage_group.add(self._stage)
        # barrier collisions
        self._barrier_group = pygame.sprite.Group()
        for barrier_sprite in self._barriers:
            self._barrier_group.add(barrier_sprite)

        self._animations = {move: Animation(self._character, MoveInfo(move, **move_info))
                                            for move, move_info in self._moves.items()}

        self._current_animation = self._animations['idle']  # type: Animation

    @property
    def player_number(self) -> int:
        return self._player_number

    @property
    def character_name(self) -> str:
        return self._name

    @property
    def facing_left(self) -> bool:
        return self._facing_left

    @property
    def health(self) -> int:
        return self._health

    @property
    def current_animation(self) -> Animation:
        return self._current_animation
    
    @property
    def lost(self) -> bool:
        return self._loss

    def switch_animation(self, animation_name: str) -> None:
        self._current_animation.reset()
        self._current_animation = self._animations[animation_name]

    def action(self, action: str) -> None:
        # determine which animation is being asked for
        new_animation = action
        if action == 'left' or action == 'right':
            if self._in_air:
                new_animation = 'air_idle'
            else:
                new_animation = 'walk'
        if action == 'idle' and self._in_air:
            new_animation = 'air_idle'
        # if prior move not the same and animation is ok to switch, reset animation frame then
        # change current animation
        if self._current_animation.done or (self._current_animation.cancelable and self._current_animation.move != new_animation):
            state = 'ground'
            if self._in_air:
                state = 'air'
            if self._animations[new_animation].allowed_to_start(state):
                self.switch_animation(new_animation)

        # set facing
        if action == 'left':
            self._facing_left = True
        elif action == 'right':
            self._facing_left = False

        # special cases for when the player should be moving around
        # left/right:
        if (action == 'left' or action == 'right') and self._moves[self._current_animation.move]['can_move']:
            if self._in_air:
                self.controlled_acc.x = sign(-1*self._facing_left) * self._physics.air_accel
            else:
                self.controlled_acc.x = sign(-1*self._facing_left) * self._physics.ground_accel

        # jumping:
        if self._current_animation.move == 'jump' and not self._in_air:
            self.controlled_acc.y = self._physics.jump_accel

    def update(self) -> None:
        # add appropriate resistive force depending on whether or not the player is on the ground
        friction_acc = 0
        if not self.controlled_acc.x:
            if not self._in_air:
                friction_acc = self._physics.traction * -sign(self.vel.x) * (abs(self.vel.x) > 0)
            else:
                friction_acc = self._physics.air_accel * -sign(self.vel.x) * (abs(self.vel.x) > 0)

        self.acc.x += friction_acc

        # if in hitstun, make controlled acceleration much smaller
        if self._hitstun:
            self.controlled_acc.x *= .2
            self.controlled_acc.y *= .2
        self.acc.y += self.controlled_acc.y     # jump accel, DI
        self.acc.y += self._physics.gravity  # fall acceleration
        self.acc += self.knockback_acc          # knockback
        self.acc.x += self.controlled_acc.x     # walk accel, DI

        self.vel += self.acc    # update velocity

        # apply ground and air speed cap
        if abs(self.vel.x) > self._physics.ground_speed and not self._in_air:
            self.vel.x = self._physics.ground_speed * sign(self.vel.x)
        if abs(self.vel.x) > self._physics.air_speed and self._in_air:
            self.vel.x = self._physics.air_speed * sign(self.vel.x)

        # stop the player if their speed is below a threshold
        if abs(self.vel.x) < .3:
            self.vel.x = 0

        # update the sprite and bounding box for the current animation
        self._current_animation.update_frame()
        self.surf = self._current_animation.get_current_frame()
        self.rect = self.surf.get_rect(center = (self.pos.x, self.pos.y))
        # mirror the sprite horizontally if the player is facing left
        if self._facing_left:
            self.surf = pygame.transform.flip(self.surf, True, False)

        self._stage_collision_check()   # if player is on the ground, don't let them fall through
        self._barrier_collision_check() # if the player is crossing over a window barrier

        self.pos += self.vel + 0.5 * self.acc   # update position based on current vel and accel
        self.rect.midbottom = self.pos

        if self._stage_collision():
            self._in_air = False
        else:
            self._in_air = True

        # reset accelerations so things don't fly out of control
        self.controlled_acc.x = 0
        self.controlled_acc.y = 0
        self.knockback_acc.x = 0
        self.knockback_acc.x = 0
        self.acc.x = 0
        self.acc.y = 0

        # control health bar
        self.healthbar.update_bar()

    def _stage_collision(self) -> list:
        return pygame.sprite.spritecollide(self, self._stage_group, False, collided=hitbox_collision)

    def _stage_collision_check(self) -> None:
        stage_collisions = self._stage_collision()
        if self.vel.y > 0:
            if stage_collisions:
                lowest = stage_collisions[0]
                # Don't let players drop below lowest point
                if self.pos.y < lowest.collision.bottom:
                    self.pos.y = lowest.collision.top + 1
                    self.vel.y = 0
                    self.acc.y = 0
                    if self._in_air and self.current_animation.move != 'hit':
                        self.switch_animation('land')
                    self._in_air = False

    def _barrier_collision(self) -> list:
        return pygame.sprite.spritecollide(self, self._barrier_group, False, collided=hitbox_collision)
    
    def _barrier_collision_check(self) -> None:
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

    def attacked(self, damage: int, base_knockback: float, knockback_direction: Vector2) -> None:
        if self.current_animation.move != 'hit':
            self.switch_animation('hit')
            self.acc.y += base_knockback * knockback_direction.y
            self.acc.x += base_knockback * knockback_direction.x
            if self._health > 0:
                self._health -= damage
                self.healthbar.damage(damage)
            if self._health <= 0:
                self._health = 0
                self._loss = True
            


def hitbox_collision(sprite1: SwagCollisionSprite, sprite2: SwagCollisionSprite) -> bool:
    '''
    Check if two hitboxes collide
    '''
    return sprite1.collision.colliderect(sprite2.collision)