'''
The model for SWAG. Contains the information about the game "scene", which is the environment around the players. 
'''
import pygame
class SwagStage(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface([1000, 50])
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (1000/2, 1000-50))
        self.__FRICTION = -0.1
        self.__GRAVITY = .02

    @property
    def friction(self):
        return self.__FRICTION

    @property
    def gravity(self):
        return self.__GRAVITY
