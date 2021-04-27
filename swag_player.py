'''
docstring moment
'''
import os
import pygame
from pygame import Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, player_number: int, character: str) -> None:
        super().__init__()
        self.__player_number = player_number
        self.surf = pygame.image.load(os.path.join('chars', character, 'sprites', 'idle', f'{character}_idle-1.png'))
        self.rect = self.surf.get_rect(center = (500, 500))
        self.pos = Vector2((500,500))
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)

    @property
    def player_number(self):
        return self.__player_number

    def action(self, action):
        if action == 'left':
            self.pos.x -= 1
        if action == 'right':
            self.pos.x += 1
        self.rect.midbottom = self.pos

    def attacked(self, damage, base_knockback, knockback_direction):
        pass
