'''
Handles all character animations for SWAG.
'''
import csv
from os import listdir, path
import pygame
from swag_helpers import CollisionBox, MoveInfo


class Animation:
    '''
    Stores information about a single character animation.

    Attributes:
        __move (MoveInfo): Information about the animation's associated move.
        __sprites_list (list): A list of Surfaces for each frame of the
            animation.
        __collision_boxes (dict): A list of information about the hitboxes and
            hurtboxes.
        __current_frame_index (int): The current frame of animation.
        __current_lag_frame (int): The current endlag frame.
        __repetition (int): The current frame repetition, used to slow down the
            speed of animations without decreasing the game's framerate.
        __done (bool): Stores whether or not the animation is done playing.

    '''
    REPEAT_FRAME = 5

    def __init__(self, character: str, move: MoveInfo) -> None:
        '''
        Creates an Animation object.
        Args:
            character (str): Representing the character being controlled
            move (MoveInfo): Info about the associated move
        '''
        character_path = path.join('chars', character)
        self.__move = move

        sprites_path = path.join(character_path, 'sprites', self.__move.name)
        sprite_filenames = listdir(sprites_path)
        sprite_filenames = [path.join(sprites_path, name) for name in
                            sprite_filenames
                            if name[-4:] == '.png']
        sprite_filenames.sort()
        self.__sprites_list = [pygame.image.load(
            frame) for frame in sprite_filenames]

        self.__collision_boxes = {'hit': {}, 'hurt': {}}
        self.get_collision_boxes(path.join(character_path,
                                           'animations', f'{self.__move.name}.anim'))

        self.__current_frame_index = 0
        self.__current_lag_frame = 0

        self.__repetition = 0
        self.__done = False

    def __repr__(self):
        '''
        Returns the move name and current frame as a string
        '''
        return f'{self.__move.name} frame {self.__current_frame_index}'

    @property
    def move(self) -> str:
        '''
        Returns the string name of the current move
        '''
        return self.__move.name

    @property
    def cancelable(self) -> bool:
        '''
        Returns whether the move is cancelable in it's current state
        '''
        if self.__done:
            return True
        return self.__move.cancelable_start > 0 and  \
            self.__current_frame_index >= self.__move.cancelable_start

    @property
    def done(self) -> bool:
        '''
        Returns whether the animation is done or not
        '''
        return self.__done

    @property
    def current_hitboxes(self) -> list:
        '''
        Returns the current hitboxes for the current sprite.

        Returns:
            list: Collision boxes representing all the current hitboxes
                of the sprite
        '''
        try:
            return self.__collision_boxes['hit'][self.__current_frame_index+1]
        except KeyError:
            return [CollisionBox(0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 pygame.Rect(0, 0, 0, 0))]

    @property
    def current_hurtboxes(self) -> list:
        '''
        Returns the current hurtboxes for the current sprite.

        Returns:
            list: Collision boxes representing all the current hurtboxes
                of the sprite
        '''
        try:
            return self.__collision_boxes['hurt'][self.__current_frame_index+1]
        except KeyError:
            return [CollisionBox(0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 pygame.Rect(0, 0, 0, 0))]

    def get_current_frame(self) -> pygame.Surface:
        '''
        Gets the current frame of the currently running animation.

        Returns:
            pygame.Surface: [description]
        '''
        if self.__current_lag_frame > 0:
            return self.__sprites_list[-1]
        return self.__sprites_list[self.__current_frame_index]

    def allowed_to_start(self, state: str) -> bool:
        '''
        Return whether or not the animation is allowed to start depending on a
        character's state.

        Args:
            state (str): next state of the character (ground or air)

        Returns:
            bool: whether or not the current move allows this state
        '''
        return state in self.__move.allowed_states

    def reset(self) -> None:
        '''
        Resets the frame index for the current animation.
        '''
        self.__current_frame_index = 0
        self.__current_lag_frame = 0
        self.__done = False

    def get_collision_boxes(self, framedata_path: str) -> None:
        '''
        Imports the animations collision boxes from it's .anim file.

        Args:
            framedata_path (str): The file path of the .anim file
        '''
        if path.isfile(framedata_path):
            with open(framedata_path, newline='') as framedata_file:
                reader = csv.reader(framedata_file, skipinitialspace=True)
                for row in reader:
                    if row[0] != 'frame':
                        row_ints = [int(element) for element in row[2:]]
                        coords = (row_ints[0], row_ints[1],
                                  row_ints[4], row_ints[5])
                        box = CollisionBox(*row_ints, pygame.Rect(coords))
                        if row[1] == 'hurt':
                            try:
                                self.__collision_boxes['hurt'][int(
                                    row[0])].append(box)
                            except KeyError:
                                self.__collision_boxes['hurt'][int(row[0])] = [
                                    box]
                        elif row[1] == 'hit':
                            try:
                                self.__collision_boxes['hit'][int(
                                    row[0])].append(box)
                            except KeyError:
                                self.__collision_boxes['hit'][int(row[0])] = [
                                    box]

    def update_frame(self):
        '''
        Updates the animation to the next frame, or changes its state to done.
        '''
        animation_length = len(self.__sprites_list)
        self.__repetition += 1
        if self.__repetition >= self.REPEAT_FRAME:
            self.__current_frame_index += 1
            self.__repetition = 0
        if self.__current_frame_index >= animation_length:
            self.__current_frame_index = animation_length-1
            self.__current_lag_frame += 1
            self.__done = self.__current_lag_frame > self.__move.endlag
