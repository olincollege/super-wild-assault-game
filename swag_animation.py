from typing import Tuple, NamedTuple, List
import pygame
from pygame import Vector2
import csv
from os import listdir, path
from abc import ABC, abstractmethod
from swag_helpers import sign, CollisionBox, MoveInfo

class Animation:
    REPEAT_FRAME = 5
    def __init__(self, character: str, move: MoveInfo) -> None:
        self.__character_path = path.join('chars', character)
        self.__move = move

        self.__sprites_path = path.join(self.__character_path, 'sprites', self.__move.name)
        sprite_filenames = listdir(self.__sprites_path)
        sprite_filenames = [path.join(self.__sprites_path, name) for name in sprite_filenames
                            if name[-4:] == '.png']
        sprite_filenames.sort()
        self.__sprites_list = [pygame.image.load(frame) for frame in sprite_filenames]

        self.__framedata_path = path.join(self.__character_path, 'animations', f'{self.__move.name}.anim')

        
        self.__animation_length = len(self.__sprites_list)

        self.__current_frame_index = 0
        self.__current_lag_frame = 0
        self.__repetition = 0
        self.__done = False

        self.__hurtboxes = {}
        self.__hitboxes = {}
        self.get_collision_boxes()

    def __repr__(self):
        return f'{self.__move.name} frame {self.__current_frame_index}'

    @property
    def move(self) -> str:
        return self.__move.name

    @property
    def cancelable(self) -> bool:
        if self.__done:
            return True
        return self.__move.cancelable_start > 0 and self.__current_frame_index >= self.__move.cancelable_start

    @property
    def done(self) -> bool:
        return self.__done

    @property
    def current_hitboxes(self) -> list:
        try:
            return self.__hitboxes[self.__current_frame_index+1]
        except KeyError:
            return [CollisionBox(0,0,0,0,0,0,0,0,0,0,pygame.Rect(0,0,0,0))]

    @property
    def current_hurtboxes(self) -> list:
        try:
            return self.__hurtboxes[self.__current_frame_index+1]
        except KeyError:
            return [CollisionBox(0,0,0,0,0,0,0,0,0,0,pygame.Rect(0,0,0,0))]

    def get_current_frame(self) -> pygame.Surface:
        if self.__current_lag_frame > 0:
            return self.__sprites_list[-1]
        return self.__sprites_list[self.__current_frame_index]

    def allowed_to_start(self, state: str) -> bool:
        return state in self.__move.allowed_states

    def reset(self) -> None:
        self.__current_frame_index = 0
        self.__current_lag_frame = 0
        self.__done = False

    def get_collision_boxes(self) -> None:
        if path.isfile(self.__framedata_path):
            with open(self.__framedata_path, newline='') as framedata_file:
                reader = csv.reader(framedata_file, skipinitialspace=True)
                for row in reader:
                    if row[0] != 'frame':
                        row_ints = [int(element) for element in row[2:]]
                        coords = (row_ints[0], row_ints[1], row_ints[4], row_ints[5])
                        box = CollisionBox(*row_ints, pygame.Rect(coords))
                        if row[1] == 'hurt':
                            try:
                                self.__hurtboxes[int(row[0])].append(box)
                            except KeyError:
                                self.__hurtboxes[int(row[0])] = [box]
                        elif row[1] == 'hit':
                            try:
                                self.__hitboxes[int(row[0])].append(box)
                            except KeyError:
                                self.__hitboxes[int(row[0])] = [box]

    def update_frame(self) -> pygame.Surface:
        self.__repetition += 1
        if self.__repetition >= self.REPEAT_FRAME:
            self.__current_frame_index += 1
            self.__repetition = 0
        if self.__current_frame_index >= self.__animation_length:
            self.__current_frame_index = self.__animation_length-1
            self.__current_lag_frame += 1
            self.__done = self.__current_lag_frame > self.__move.endlag
