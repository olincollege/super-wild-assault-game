'''
Swag healthbar. Based on: https://youtu.be/pUEZbUAMZYA.
'''
import pygame, sys
from math import ceil
from swag_player import Player

class SwagHealthBar(pygame.sprite.Sprite):
    def __init__(self, player: Player):
        super().__init__()
        self.image = pygame.Surface((40,40))
        self.image.fill((200,30,30))
        self.rect = self.image.get_rect(center = (400,400))
        self.max_health = 1000
        self.target_health = self.max_health
        self.current_health = self.max_health
        self.health_bar_length = 400
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 5

    def get_damage(self,amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def get_health(self,amount):
        if self.target_health < self.max_health:
            self.target_health += amount
        if self.target_health > self.max_health:
            self.target_health = self.max_health

    def update(self):
        self.advanced_health()

    def advanced_health(self):
        transition_width = 0
        transition_color = (255,0,0)
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = -ceil((self.target_health - self.current_health) / self.health_ratio)
            print(transition_width)
            transition_color = (255,255,0)

        health_bar_width = int(self.target_health / self.health_ratio)
        health_bar = pygame.Rect(10,45,health_bar_width,25)
        transition_bar = pygame.Rect(health_bar.right,45,transition_width,25)
        
        pygame.draw.rect(screen,(255,0,0),health_bar)
        pygame.draw.rect(screen,transition_color,transition_bar)	
        pygame.draw.rect(screen,(255,255,255),(10,45,self.health_bar_length,25),4)	



pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
SwagHealthBar = pygame.sprite.GroupSingle(SwagHealthBar())

SwagHealthBar.sprite.get_damage(200)

screen.fill((30,30,30))
SwagHealthBar.draw(screen)
SwagHealthBar.update()
pygame.display.update()
clock.tick(60)