from typing import Tuple, NamedTuple, List
import pygame
from pygame import Vector2
import csv
from os import listdir, path
from abc import ABC, abstractmethod
from swag_player import Player

class Animation:
    
    REPEAT_FRAME = 5
    def __init__(self, player: Player, character: str, move: str) -> None:
        self.__character_path = path.join('chars', character)

        self.__sprites_path = path.join(self.__character_path, 'sprites', move)
        sprite_filenames = listdir(self.__sprites_path)
        sprite_filenames = [path.join(self.__sprites_path, name) for name in sprite_filenames
                            if name[-4:] == '.png']
        sprite_filenames.sort()
        self.__sprites_list = [pygame.image.load(frame) for frame in sprite_filenames]

        self.__framedata_path = path.join(self.__character_path, 'animations', f'{move}.anim')

        self.__move = move
        self.__animation_length = len(self.__sprites_list)

        self.__current_frame = 0
        self.__repetition = 0
        
        self.__hurtboxes = []
        self.__hitboxes = []
        self.__cancelable = False
        self.__endlag = 0
        # self.__collisions = self.get_collision_boxes()

    def __repr__(self):
        return f'{self.__move} frame {self.__current_frame}'

    @property
    def move(self) -> str:
        return self.__move

    @property
    def cancelable(self) -> bool:
        return self.__cancelable

    def reset(self) -> None:
        self.__current_frame = 0

    def get_collision_boxes(self) -> None:
        framedata = []
        with open(self.__framedata_path, 'r') as framedata_file:
            reader = csv.reader(framedata_file)
            for row in reader:
                framedata.append(row)
    
    def update_frame(self) -> pygame.Surface:
        self.__repetition += 1
        if self.__repetition >= self.REPEAT_FRAME:
            self.__current_frame += 1
            self.__repetition = 0
        if self.__current_frame > self.__animation_length-1:
            self.__current_frame = 0
            if self.__end_callback:
                self.__end_callback()
                return self.__sprites_list[-1]
        return self.__sprites_list[self.__current_frame]

class CollisionBox(NamedTuple):
    x: int
    y: int
    xoffset: int
    yoffset: int
    width: int
    height: int
    damage: int
    knockback_scale: float
    knockback_x: float
    knockback_y: float
    cancelable: bool
