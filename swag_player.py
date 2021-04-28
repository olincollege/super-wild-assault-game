'''
docstring moment
'''
import os
import pygame
from pygame import Vector2
from swag_animation import Animation
from swag_stage import SwagStage

class Player(pygame.sprite.Sprite):

    def __init__(self, player_number: int, character: str, stage: SwagStage) -> None:
        super().__init__()
        self._stage = stage
        self._character = character
        self._player_number = player_number
        self.surf = pygame.image.load(os.path.join('chars', character, 'sprites', 'idle', f'{character}_idle-1.png'))
        self.rect = self.surf.get_rect(center = (500, 500))
        
        self._walk_accel = .3
        self._walk_speed_cap = 3

        self.pos = Vector2((500,500))
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)
        self._facing_right = True
        
        self._attacking = False
        self._current_animation = None
        # self._animations = {}
        # self.moves = ['block','hit','idle','jab','jump', 'walk']
        # self._generate_anims()

    @property
    def player_number(self):
        return self._player_number

    def _generate_anims(self):
        self._animations = {move: Animation(self._character, move) for move in self.moves}

    def _toggle_facing(self):
            self.surf = pygame.transform.flip(self.surf, True, False)
            self._facing_right = not self._facing_right

    def action(self, action):
        if action == 'left':
            self.acc.x = -self._walk_accel
            if self._facing_right:
                self._toggle_facing()

        if action == 'right':
            self.acc.x = self._walk_accel
            if not self._facing_right:
                self._toggle_facing()

        self.rect.midbottom = self.pos
    
    def update(self):
        self.acc.x += self.vel.x * self._stage.friction
        self.vel += self.acc
        if self.vel.x > self._walk_speed_cap:
            self.vel.x = self._walk_speed_cap
        if abs(self.vel.x) < .09:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        # Animation.update_frame(self)

    def attacked(self, damage, base_knockback, knockback_direction):
        pass
