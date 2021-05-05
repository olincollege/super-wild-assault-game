'''
Swag healthbar. Based on: https://youtu.be/pUEZbUAMZYA, https://www.codepile.net/pile/XydlGQy1
'''
import pygame, sys
from math import ceil

class SwagHealthBar(pygame.sprite.Sprite):
    def __init__(self, healthbar_x,healthbar_y,horizontal_flip):
        super().__init__()
        self.healthbar_x = healthbar_x
        self.healthbar_y = healthbar_y
        self.horizontal_flip = horizontal_flip
        self.image = pygame.Surface((40,40))
        self.image.fill((200,30,30))
        self.rect = self.image.get_rect(center = (500,250))
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

    def update(self):
        self.advanced_health()

    def advanced_health(self):
        transition_width = 0
        transition_color = (255,0,0)
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = -ceil((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (255,255,0)
        health_bar_width = int(self.target_health / self.health_ratio)
        # TODO: change
        if self.horizontal_flip:
            health_bar = pygame.Rect(+ self.healthbar_x + self.health_bar_length - health_bar_width,self.healthbar_y,health_bar_width,25)
            transition_bar = pygame.Rect(health_bar.left - transition_width,self.healthbar_y,transition_width,25)
        else:
            health_bar = pygame.Rect(self.healthbar_x,self.healthbar_y,health_bar_width,25)
            transition_bar = pygame.Rect(health_bar.right,45,transition_width,25)
        pygame.draw.rect(screen,(255,0,0),health_bar)
        pygame.draw.rect(screen,transition_color,transition_bar)	
        pygame.draw.rect(screen,(255,255,255),(self.healthbar_x,self.healthbar_y,self.health_bar_length,25),4)	

pygame.init()
screen = pygame.display.set_mode((1000,500))
clock = pygame.time.Clock()
player1 = pygame.sprite.GroupSingle(SwagHealthBar(50,45,True))
player2 = pygame.sprite.GroupSingle(SwagHealthBar(550,45,False))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player1.sprite.get_damage(200)
            if event.key == pygame.K_UP:
                player2.sprite.get_damage(200)

    screen.fill((30,30,30))
    player1.draw(screen)
    player1.update()
    player2.update()
    pygame.display.update()
    clock.tick(60)