from typing import Tuple, NamedTuple, List
from pygame import Vector2
from os import listdir, path
from abc import ABC, abstractmethod

class Animation(ABC):
    def __init__(self, animation_path: str) -> None:
        self.__animation_path = animation_path
        self.__sprites_list = [pygame.image.load(frame) for frame in listdir(path.join(animation_path,'sprites')]
        self.__animation_length = len(self.__sprites_list)
        self.__current_frame = 0

    @abstractmethod
    def get_collision_boxes(self) -> None:
        pass


class AttackAnimation(Animation):
    def __init__(self, animation_path: str) -> None:
        super().__init__(animation_path)
        # import hitboxes from file


class PassiveAnimation(Animation):
    def __init__(self, animation_path: str) -> None:
        super().__init__(animation_path)
        # import hurtboxes from file


class Point2D(NamedTuple):
    x: int
    y: int


class Hurtbox(NamedTuple):
    origin: Point2D
    radius: int


class Hitbox(NamedTuple):
    origin: Point2D
    radius: int
    damage: int
    knockback_scale: float
    knockback_direction: Vector2
