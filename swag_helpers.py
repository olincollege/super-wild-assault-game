'''
A list of helper functions and classes to be used by core scripts.
'''
from math import copysign
from typing import NamedTuple
from pygame import Rect


def sign(number) -> float:
    '''
    Returns 1 with the sign of a number.

    Args:
        number: A number to get the sign of

    Returns:
        float: 1 * the sign of the input
    '''
    return copysign(1, number)


class PlayerPhysics(NamedTuple):
    '''
    A named tuple storing information about character physics.
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
    A named tuple storing information about a hit or hurt box.
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
    A named tuple storing information about character move info.
    '''
    name: str
    allowed_states: list
    cancelable_start: int
    endlag: int
    can_move: int
