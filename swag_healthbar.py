'''
Swag healthbar. Based on: https://youtu.be/pUEZbUAMZYA, https://www.codepile.net/pile/XydlGQy1
'''
import pygame, sys
import time
from math import ceil

clock = pygame.time.Clock()
class SwagHealthBar(pygame.sprite.Sprite):
    def __init__(self, player_number: int, health: int):
        super().__init__()
        if player_number == 1:
            self.healthbar_x = 550
            self.healthbar_y = 45
            self.horizontal_flip = False
        if player_number == 2:
            self.healthbar_x = 50
            self.healthbar_y = 45
            self.horizontal_flip = True
        self.max_health = health
        self.target_health = health # player health
        self.current_health = health
        self.health_bar_length = 400
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 1
        self.surf = pygame.Surface((self.health_bar_length, 25))
        self.rect = self.surf.get_rect(topleft=(self.healthbar_x, self.healthbar_y))
    
    def damage(self, amount):
        self.target_health -= amount

    def update_bar(self):
        transition_width = 0
        transition_color = (255,255,0)
        transition_bar = pygame.Rect(0,0,0,0)
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = ceil((self.current_health - self.target_health)/self.health_ratio)
        health_bar_width = int(self.target_health / self.health_ratio)
        if self.horizontal_flip:
            health_bar = pygame.Rect(self.health_bar_length - health_bar_width,0,
                health_bar_width,25)
            transition_bar = pygame.Rect(health_bar.left - transition_width,\
                0,transition_width,25)
        else:
            health_bar = pygame.Rect(0,0,health_bar_width,25)
            transition_bar = pygame.Rect(health_bar.right,0,transition_width,25)
        self.surf.fill((44, 38, 69))     # background color for empty health
        self.surf.fill((255,0,0),health_bar)            # filled health color
        self.surf.fill(transition_color,transition_bar) # transition health color
        pygame.draw.rect(self.surf,(255,255,255),(0,0,self.health_bar_length,25),4) # outline
