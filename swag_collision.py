'''
Contains the information about game collision between sprites
'''
import pygame

class SwagCollisionSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    @property
    def collision(self):
        if hasattr(self, 'hitbox'):
            return self.hitbox
        else:
            return self.rect

