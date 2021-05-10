'''
Contains the information about the game's stage, barriers, and background,
which compose the environment around the players.
'''
from math import ceil
import pygame


class SwagStage(pygame.sprite.Sprite):
    '''
    The stage the players beat eachother up on
    Attributes:
        surf (pygame.surface.Surface): The pygame surface occupied by the
            stage sprite
        rect (pygame.Rect): Defines the location and boundaries of the stage
            sprite
        hitbox (pygame.Rect): The area where the stage can collide
    '''

    def __init__(self, bkg_width, bkg_height):
        '''
        Initializes the SwagStage instance.
        Args:
            bkg_width [int]: The background width according to the width
                of the window
            bkg_height [int]: The background height according to the height
                of the window
        '''
        super().__init__()
        self.surf = pygame.image.load("./background_data/stage.png")
        self.rect = self.surf.get_rect(center=(bkg_width/2, bkg_height-100))
        self.hitbox = self.surf.get_rect(center=(bkg_width/2, bkg_height-53))

    @property
    def collision(self):
        '''
        Returns a rect representing the collision box of the stage.
        '''
        return self.hitbox

    def swap_image(self, image_name: str) -> None:
        '''
        Swaps the stage image.

        Args:
            image_name [str]: The file name of the image to swap in.
        '''
        self.surf = pygame.image.load('./background_data/'+image_name)


class SwagStageBackground(pygame.sprite.Sprite):
    '''
    A sprite representing the background of the stage.
    Attributes:
        width [int]: The background width according to the width
            of the window
        height [int]: The background height according to the height
            of the window
        surf (pygame.surface.Surface): The pygame surface occupied by the
            Background sprite
        rect (pygame.Rect): Defines the location and boundaries of the
            Background
        hitbox (pygame.Rect): The none area where the Background can collide
    '''

    def __init__(self):
        '''
        Creates the background.
        '''
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
        Returns the Rect representing the hitbox of the background
        '''
        return self.hitbox

    def swap_backdrop(self, name: str) -> None:
        '''
        Swaps the background image.

        Args:
            name [str]: The file name of the image to swap in.
        '''
        self.surf = pygame.image.load('./background_data/'+name)


class SwagBarriers(pygame.sprite.Sprite):
    '''
    The barriers on the left and right edges of the screen.
    Attributes:
        surf (pygame.surface.Surface): The pygame surface occupied by the
            Barrier sprites
        rect (pygame.Rect): Defines the location and boundaries of the
            Barriers
        hitbox (pygame.Rect): The area where the Barriers can collide
    '''

    def __init__(self, bkg_height, left_x):
        '''
        Initializes the instance for the barriers.

        Args:
            bkg_height (int): Height of the window and background
            left_x (int): Left x position of the barrier
        '''
        super().__init__()
        self.surf = pygame.Surface((0, 0), flags=0)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.hitbox = pygame.Rect(left_x, 0, 1, bkg_height)

    @property
    def collision(self):
        '''
        Property representing whether or not a barrier is colliding
        with another sprite.

        Returns:
            hitbox (pygame.Rect): The area where the Barrier can collide
        '''
        return self.hitbox

    def resize(self, width, height):
        '''
        Resizes the hitbox of the barriers.

        Args:
            width (int): New width for the hitbox
            height (int): New height for the hitbox
        '''
        self.hitbox.w = width
        self.hitbox.h = height
