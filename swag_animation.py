'''
[summary]
'''
import csv
from os import listdir, path
import pygame
from swag_helpers import CollisionBox, MoveInfo


class Animation:
    '''
    [summary]
    '''
    REPEAT_FRAME = 5

    def __init__(self, character: str, move: MoveInfo) -> None:
        character_path = path.join('chars', character)
        self.__move = move

        sprites_path = path.join(character_path, 'sprites', self.__move.name)
        sprite_filenames = listdir(sprites_path)
        sprite_filenames = [path.join(sprites_path, name) for name in sprite_filenames
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
        return f'{self.__move.name} frame {self.__current_frame_index}'

    @property
    def move(self) -> str:
        '''
        [summary]
        '''
        return self.__move.name

    @property
    def cancelable(self) -> bool:
        '''
        [summary]

        Returns:
            bool: [description]
        '''
        if self.__done:
            return True
        return self.__move.cancelable_start > 0 and  \
            self.__current_frame_index >= self.__move.cancelable_start

    @property
    def done(self) -> bool:
        '''
        [summary]

        Returns:
            bool: [description]
        '''
        return self.__done

    @property
    def current_hitboxes(self) -> list:
        '''
        [summary]

        Returns:
            list: [description]
        '''
        try:
            return self.__collision_boxes['hit'][self.__current_frame_index+1]
        except KeyError:
            return [CollisionBox(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, pygame.Rect(0, 0, 0, 0))]

    @property
    def current_hurtboxes(self) -> list:
        '''
        [summary]

        Returns:
            list: [description]
        '''
        try:
            return self.__collision_boxes['hurt'][self.__current_frame_index+1]
        except KeyError:
            return [CollisionBox(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, pygame.Rect(0, 0, 0, 0))]

    def get_current_frame(self) -> pygame.Surface:
        '''
        [summary]

        Returns:
            pygame.Surface: [description]
        '''
        if self.__current_lag_frame > 0:
            return self.__sprites_list[-1]
        return self.__sprites_list[self.__current_frame_index]

    def allowed_to_start(self, state: str) -> bool:
        '''
        [summary]

        Args:
            state (str): [description]

        Returns:
            bool: [description]
        '''
        return state in self.__move.allowed_states

    def reset(self) -> None:
        '''
        [summary]
        '''
        self.__current_frame_index = 0
        self.__current_lag_frame = 0
        self.__done = False

    def get_collision_boxes(self, framedata_path: str) -> None:
        '''
        [summary]

        Args:
            framedata_path (str): [description]
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

    def update_frame(self) -> pygame.Surface:
        '''
        [summary]

        Returns:
            pygame.Surface: [description]
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
