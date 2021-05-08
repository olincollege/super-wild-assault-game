'''
Swag healthbar. Based on: https://youtu.be/pUEZbUAMZYA, https://www.codepile.net/pile/XydlGQy1
'''
from math import ceil
import pygame
from pygame import Vector2


class SwagHealthBar(pygame.sprite.Sprite):
    '''
    [summary]
    '''

    def __init__(self, player_number: int, max_health: int):
        '''
        [summary]

        Args:
            player_number (int): [description]
            max_health (int): [description]
        '''
        super().__init__()
        pos = Vector2(0, 0)
        pos.x = 550
        pos.y = 45
        if player_number == 2:
            pos.x = 50
            pos.y = 45
        self.target_health = max_health  # player health
        self.current_health = max_health
        self.health_bar_length = 400
        self.health_ratio = max_health / self.health_bar_length
        self.health_change_speed = 1
        self.surf = pygame.Surface((self.health_bar_length, 25))
        self.rect = self.surf.get_rect(topleft=(pos.x, pos.y))

    def damage(self, amount):
        '''
        [summary]

        Args:
            amount ([type]): [description]
        '''
        self.target_health -= amount

    def update_bar(self):
        '''
        [summary]
        '''
        horizontal_flip = self.rect.left == 50
        transition_width = 0
        transition_color = (255, 255, 0)
        transition_bar = pygame.Rect(0, 0, 0, 0)
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = ceil(
                (self.current_health - self.target_health)/self.health_ratio)
        health_bar_width = int(self.target_health / self.health_ratio)
        if horizontal_flip:
            health_bar = pygame.Rect(self.health_bar_length - health_bar_width, 0,
                                     health_bar_width, 25)
            transition_bar = pygame.Rect(health_bar.left - transition_width,
                                         0, transition_width, 25)
        else:
            health_bar = pygame.Rect(0, 0, health_bar_width, 25)
            transition_bar = pygame.Rect(
                health_bar.right, 0, transition_width, 25)
        self.surf.fill((44, 38, 69))     # background color for empty health
        # filled health color
        self.surf.fill((255, 0, 0), health_bar)
        # transition health color
        self.surf.fill(transition_color, transition_bar)
        pygame.draw.rect(self.surf, (255, 255, 255),
                         (0, 0, self.health_bar_length, 25), 4)  # outline
