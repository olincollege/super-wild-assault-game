from typing import Tuple, NamedTuple, List
import pygame
from pygame import Vector2
import csv
from os import listdir, path
from abc import ABC, abstractmethod
from swag_helpers import sign, CollisionBox

class Animation:
    REPEAT_FRAME = 5
    def __init__(self, character: str, move: str, allowed_states: list, cancelable_start: int, endlag: int) -> None:
        self.__character_path = path.join('chars', character)

        self.__sprites_path = path.join(self.__character_path, 'sprites', move)
        sprite_filenames = listdir(self.__sprites_path)
        sprite_filenames = [path.join(self.__sprites_path, name) for name in sprite_filenames
                            if name[-4:] == '.png']
        sprite_filenames.sort()
        self.__sprites_list = [pygame.image.load(frame) for frame in sprite_filenames]

        self.__framedata_path = path.join(self.__character_path, 'animations', f'{move}.anim')

        self.__move = move
        self.__endlag = endlag
        self.__animation_length = len(self.__sprites_list)

        self.__current_frame_index = 0
        self.__current_lag_frame = 0
        self.__repetition = 0
        self.__done = False

        self.__allowed_states = allowed_states
        self.__hurtboxes = {}
        self.__hitboxes = {}
        self.get_collision_boxes()
        self.__cancelable_start = cancelable_start

    def __repr__(self):
        return f'{self.__move} frame {self.__current_frame_index}'

    @property
    def move(self) -> str:
        return self.__move

    @property
    def cancelable(self) -> bool:
        if self.__done:
            return True
        return self.__cancelable_start > 0 and self.__current_frame_index >= self.__cancelable_start

    @property
    def done(self) -> bool:
        return self.__done

    def get_current_frame(self) -> pygame.Surface:
        if self.__current_lag_frame > 0:
            return self.__sprites_list[-1]
        return self.__sprites_list[self.__current_frame_index]

    def allowed_to_start(self, state: str) -> bool:
        return state in self.__allowed_states

    def reset(self) -> None:
        self.__current_frame_index = 0
        self.__current_lag_frame = 0
        self.__done = False

    def get_collision_boxes(self) -> None:
        if path.isfile(self.__framedata_path):
            with open(self.__framedata_path, newline='') as framedata_file:
                reader = csv.reader(framedata_file, skipinitialspace=True)
                for row in reader:
                    if row[1] == 'hurt':
                        self.__hurtboxes[row[0]] = CollisionBox(*row[2:])
                    elif row[1] == 'hit':
                        self.__hitboxes[row[0]] = CollisionBox(*row[2:])

    def update_frame(self) -> pygame.Surface:
        self.__repetition += 1
        if self.__repetition >= self.REPEAT_FRAME:
            self.__current_frame_index += 1
            self.__repetition = 0
        if self.__current_frame_index >= self.__animation_length:
            self.__current_frame_index = self.__animation_length-1
            self.__current_lag_frame += 1
            self.__done = self.__current_lag_frame > self.__endlag
