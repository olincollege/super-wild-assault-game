'''
[summary]
'''
from math import copysign
from typing import NamedTuple
from pygame import Rect


def sign(number) -> float:
    '''
    [summary]

    Args:
        number ([type]): [description]

    Returns:
        float: [description]
    '''
    return copysign(1, number)


class PlayerPhysics(NamedTuple):
    '''
    [summary]
    '''
    ground_accel: float
    ground_speed: float
    air_accel: float
    air_speed: float
    weight: float
    gravity: float
    fall_speed: float
    jump_accel: float
    traction: float


class CollisionBox(NamedTuple):
    '''
    [summary]
    '''
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
    rect: Rect


class MoveInfo(NamedTuple):
    '''
    [summary]
    '''
    name: str
    allowed_states: list
    cancelable_start: int
    endlag: int
    can_move: int
