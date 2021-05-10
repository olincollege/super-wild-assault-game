'''
Swag healthbar, based on Dark Souls: https://youtu.be/pUEZbUAMZYA (video),
https://www.codepile.net/pile/XydlGQy1 (code).
'''
from math import ceil
import pygame
from pygame import Vector2


class SwagHealthBar(pygame.sprite.Sprite):
    '''
    A healthbar class to control the visual change in health for each player.
    Attributes:
        target_health: The player's health - what the healthbar moves to
        current_health: The current health shown on the bar
    '''

    def __init__(self, player_number: int, max_health: int):
        '''
        Creates the instance for the healthbar for each player.

        Args:
            player_number (int): 1 or 2, based on keyboard input selection
            max_health (int): the maximum amount of health the character has
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
        Gets the amount of damage taken and removes it from the player
        character's target health.

        Args:
            amount (integer): amount of damage taken by the player's character.
        '''
        self.target_health -= amount

    def update_bar(self):
        '''
        Changes the length of the health bar and the transitional bar (from
        current state to next state of health) to match the current health
        of the player's character to be rendered as a sprite.
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
