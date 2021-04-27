'''
The model for SWAG. Contains the information about the game "scene", which is the environment around the players. 
'''
import pygame
class SwagStage(pygame.sprite.Sprite):
    def __init__(self, player_1, player_2):
        super().__init__()
        self.surf = pygame.Surface([1000, 50])
        self.surf.fill((255,255,255))
        self.rect = self.image.get_rect(center = (1000/2, 1000-50))
