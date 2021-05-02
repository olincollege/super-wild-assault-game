'''
The model for SWAG. Contains the information about the game "scene", which is the environment around the players. 
'''
import pygame
from swag_collision import SwagCollisionSprite

class SwagStage(SwagCollisionSprite):
    def __init__(self, bkg_width, bkg_height):
        super().__init__()
        self.surf = pygame.image.load("./background_data/stage.png")
        self.rect = self.surf.get_rect(center = (bkg_width/2, bkg_height-100))
        self.hitbox = self.surf.get_rect(center = (bkg_width/2, bkg_height-53))
        self.__FRICTION = 0.1
        self.__AIR_RESIST = 0.1
        self.__GRAVITY = .2

    @property
    def friction(self):
        return self.__FRICTION

    @property
    def air_resist(self):
        return self.__AIR_RESIST

    @property
    def gravity(self):
        return self.__GRAVITY

class SwagStageBackground(SwagCollisionSprite):
    def __init__(self):
        super().__init__()
        self.WIDTH = 1000 # Window width
        self.HEIGHT = 600 # Window height
        # Import background image
        self.surf = pygame.image.load("./background_data/olin_backdrop_1.png")
        # Scale background image to fit window
        width, height = self.surf.get_size()
        width_ratio = self.WIDTH/width
        height_ratio = self.HEIGHT/height
        value_ratio = max(width_ratio,height_ratio)
        width = int(width * value_ratio)
        height = int(height * value_ratio)
        # Set background image sprite
        self.surf = pygame.transform.scale(self.surf, (width, self.HEIGHT))
        self.rect = pygame.Rect(0,0,self.WIDTH,self.HEIGHT)
        self.hitbox = pygame.Rect(0,0,0,0)
