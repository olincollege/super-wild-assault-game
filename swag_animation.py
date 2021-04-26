from typing import Tuple, NamedTuple, List
import pygame
from pygame import Vector2
import csv
from os import listdir, path
from abc import ABC, abstractmethod

class Animation:
    def __init__(self, character: str, move: str) -> None:
        self.__character_path = path.join('chars', character)
        self.__sprites_path = path.join(self.__character_path, 'sprites', move)
        self.__sprites_list = [pygame.image.load(frame) for frame in listdir(self.__sprites_path)]
        self.__framedata_path = path.join(self.__character_path, 'animations', f'{move}.anim')
        self.__move = move
        self.__animation_length = len(self.__sprites_list)
        self.__current_frame = 0
        self.__hurtboxes = []
        self.__hitboxes = []
        self.__collisions = self.get_collision_boxes()

    def get_collision_boxes(self) -> None:
        framedata = []
        with open(self.__framedata_path, 'r') as framedata_file:
            reader = csv.reader(framedata_file)
            for row in reader:
                framedata.append(row)


class Point2D(NamedTuple):
    x: int
    y: int


class CollisionBox(NamedTuple):
    topleft: Point2D
    bottomright: Point2D
    damage: int
    knockback_scale: float
    knockback_direction: Vector2
