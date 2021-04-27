'''
The model for SWAG. Contains the information about the game "scene", which is the environment around the players. 
'''
import pygame
class SwagStage(pygame.sprite.Sprite):
    def __init__(self, player_1, player_2):
        super().__init__()
        
