'''
The model for SWAG. Contains the information about the game "scene", which is the environment
around the players.
'''
from math import ceil
import pygame


class SwagStage(pygame.sprite.Sprite):
    '''
    [summary]

    Args:
        SwagCollisionSprite ([type]): [description]
    '''

    def __init__(self, bkg_width, bkg_height):
        super().__init__()
        self.surf = pygame.image.load("./background_data/stage.png")
        self.rect = self.surf.get_rect(center=(bkg_width/2, bkg_height-100))
        self.hitbox = self.surf.get_rect(center=(bkg_width/2, bkg_height-53))

    @property
    def collision(self):
        '''
        [summary]

        Returns:
            [type]: [description]
        '''
        return self.hitbox

    def swap_image(self, image_name: str) -> None:
        '''
        [summary]

        Args:
            image_name (str): [description]
        '''
        self.surf = pygame.image.load('./background_data/'+image_name)


class SwagStageBackground(pygame.sprite.Sprite):
    '''
    [summary]

    Args:
        SwagCollisionSprite ([type]): [description]
    '''

    def __init__(self):
        super().__init__()
        self.width = 1000  # Window width
        self.height = 600  # Window height
        # Import background image
        self.surf = pygame.image.load('./background_data/olin_backdrop_1.png')
        # Scale background image to fit window
        width, height = self.surf.get_size()
        width_ratio = self.width/width
        height_ratio = self.height/height
        value_ratio = max(width_ratio, height_ratio)
        # Fix rounding error for int, size up
        width = ceil(width * value_ratio) + 1
        # Fix rounding error for int, size up
        height = ceil(height * value_ratio)
        # Set background image sprite
        self.surf = pygame.transform.scale(self.surf, (width, self.height))
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.hitbox = pygame.Rect(0, 0, 0, 0)

    @property
    def collision(self):
        '''
        [summary]

        Returns:
            [type]: [description]
        '''
        return self.hitbox

    def swap_backdrop(self, name: str) -> None:
        '''
        [summary]

        Args:
            name (str): [description]
        '''
        self.surf = pygame.image.load('./background_data/'+name)


class SwagBarriers(pygame.sprite.Sprite):
    '''
    [summary]

    Args:
        SwagCollisionSprite ([type]): [description]
    '''

    def __init__(self, bkg_height, left_x):
        '''
        [summary]

        Args:
            bkg_height ([type]): [description]
            left_x ([type]): [description]
        '''
        super().__init__()
        self.surf = pygame.Surface((0, 0), flags=0)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.hitbox = pygame.Rect(left_x, 0, 1, bkg_height)

    @property
    def collision(self):
        '''
        [summary]

        Returns:
            [type]: [description]
        '''
        return self.hitbox

    def resize(self, width, height):
        '''
        [summary]

        Args:
            width ([type]): [description]
            height ([type]): [description]
        '''
        self.hitbox.w = width
        self.hitbox.h = height
