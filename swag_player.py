'''
The Player class stores and modifies information about the player-controlled
character.
'''
import os
import json
import pygame
from pygame import Vector2
from swag_animation import Animation
from swag_stage import SwagStage
from swag_helpers import sign, PlayerPhysics, MoveInfo
from swag_healthbar import SwagHealthBar


class Player(pygame.sprite.Sprite):  # pylint: disable=too-many-instance-attributes
    '''
    The Player class stores and modifies information about the
    player-controlled character.

    Attributes:
        _player_number (int): 1 or 2, mostly accessed from other classes to
             determine interactions
        _surf (pygame.surface.Surface): The pygame surface occupied by the
            player sprite
        rect (pygame.Rect): Defines the location and boundaries of the player
            sprite
        _stage_group (pygame.sprite.Group): Contains the stage sprite object
            for collision detection
        _barrier_group (pygame.sprite.Group): Contains the barrier objects for
            collision detection
        _name (str): Name of the character being controlled
        _health (int): Current health of the character being controlled
        _physics (PlayerPhysics): A NamedTuple storing physics properties of
        the character to interact with movement in environment
            determine how they move around
        _moves (dict): Stores information about moves (when they can start,
            how much endlag, etc.)
        _animations (dict): Contains animation objects for all of a characters
            animations, bound to the move or action that activates them
        _facing_left (bool): Whether or not the player is currently facing left
            (to control if the sprite flips)
        healthbar (SwagHealthBar): The character's healthbar
        pos (pygame.Vector2): Position (x,y) of where the character is on the
            pygame screen.
        vel (pygame.Vector2): Velocity (x,y) of the character
        acc (pygame.Vector2): Acceleration (x,y) of the character
        controlled_acc (pygame.Vector2): Contains the x and y components of a
            character's "controlled" acceleration, such as from jumping and
            walking
        knockback_acc (pygame.Vector2): Contains the x and y components of a
            character's "non-controller" acceleration, such as from being
            attacked
        _state (str): 'air' or 'ground', the location of the character
        _current_animation (Animation): The animation object representing the
            current animation state of the character
    '''

    def __init__(self, player_number: int, character: str,
                 stage: SwagStage, barriers: list) -> None:
        '''
        Initializes a Player instance.
        Args:
            player_number (int): 1 or 2, representing which character is being
                controlled
            character (string): The name of the character being controlled, use
                to call sprite information
            stage (SwagStage): The stage the player is on.
            barriers (list): The barriers of the screen.
        '''

        super().__init__()

        self._player_number = player_number
        self.surf = pygame.image.load(os.path.join('chars', character, 'sprites', 'idle',
                                                   f'{character}_idle-1.png'))

        # stage collisions
        self._stage_group = pygame.sprite.Group()
        self._stage_group.add(stage)
        # barrier collisions
        self._barrier_group = pygame.sprite.Group()
        for barrier_sprite in barriers:
            self._barrier_group.add(barrier_sprite)

        # import character properties from file
        with open(os.path.join('chars', character, f'{character}.info'), 'r') as info_file:
            prop_dict = json.load(info_file)
            self._name = prop_dict['name']
            self._health = prop_dict['health']
            self._physics = PlayerPhysics(**(prop_dict['physics']))
            self._moves = prop_dict['moves']

        self._animations = {move: Animation(character, MoveInfo(move, **move_info))
                            for move, move_info in self._moves.items()}

        # set up starting location
        if self._player_number == 1:
            self.rect = self.surf.get_rect(center=(750, 250))
            self.pos = Vector2((750, 250))
            self._facing_left = True
        elif self._player_number == 2:
            self.rect = self.surf.get_rect(center=(250, 250))
            self.pos = Vector2((250, 250))
            self._facing_left = False

        # set up healthbar
        self.healthbar = SwagHealthBar(self._player_number, self._health)

        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.knockback_acc = Vector2(0, 0)
        self.controlled_acc = Vector2(0, 0)

        self._state = 'air'

        self._current_animation = self._animations['idle']  # type: Animation

    @property
    def collision(self) -> pygame.Rect:
        '''
        Returns the collision box (rect) of the player.
        '''
        return self.rect

    @property
    def player_number(self) -> int:
        '''
        Returns the player number (1 or 2)
        '''
        return self._player_number

    @property
    def character_name(self) -> str:
        '''
        Returns the character name.
        '''
        return self._name

    @property
    def facing_left(self) -> bool:
        '''
        Returns a boolean representing whether the player is
        facing left or right.
        '''
        return self._facing_left

    @property
    def health(self) -> int:
        '''
        Returns an int value representing the player's current health.
        '''
        return self._health

    @property
    def current_animation(self) -> Animation:
        '''
        Returns an Animation representing the player's current animation.
        '''
        return self._current_animation

    @property
    def lost(self) -> bool:
        '''
        Returns a boolean representing if the player has lost or not.

        |   |  ||
        ----------
        ||  |  |_
        '''
        if self._health <= 0:
            return True
        return False

    def switch_animation(self, animation_name: str) -> None:
        '''
        Changes the player's current animation after resetting it.

        Args:
            animation_name (str): Next animation for the character to switch
                into
        '''
        self._current_animation.reset()
        self._current_animation = self._animations[animation_name]

    def action(self, action: str) -> None:
        '''
        Receives an action from the input handler and changes the player state
        depending on a number of factors.

        Args:
            action (str): The current input action move for the player
        '''
        # determine which animation is being asked for
        new_animation = action
        if action in ('left', 'right'):
            if self._state == 'air':
                new_animation = 'air_idle'
            else:
                new_animation = 'walk'
        if action == 'idle' and self._state == 'air':
            new_animation = 'air_idle'
        # if prior move not the same and animation is ok to switch, reset animation frame then
        # change current animation
        if self._current_animation.done or \
            (self._current_animation.cancelable and
                self._current_animation.move != new_animation) and \
                self._animations[new_animation].allowed_to_start(self._state):
            self.switch_animation(new_animation)

        # set facing
        if action == 'left':
            self._facing_left = True
        elif action == 'right':
            self._facing_left = False

        # special cases for when the player should be moving around
        # left/right:
        if (action in ('left', 'right')) and self._moves[self._current_animation.move]['can_move']:
            if self._state == 'air':
                self.controlled_acc.x = sign(-1*self._facing_left) * \
                    self._physics.air_accel
            else:
                self.controlled_acc.x = sign(-1*self._facing_left) * \
                    self._physics.ground_accel

        # jumping:
        if self._current_animation.move == 'jump' and self._state == 'ground':
            self.controlled_acc.y = self._physics.jump_accel

    def update(self) -> None:
        '''
        Changes the prior state of the player's character to the next state
        for physics, movement, and animation
        '''
        # Add appropriate resistive force depending on whether or not the
        # player is on the ground
        friction_acc = 0
        if not self.controlled_acc.x:
            if self._state == 'ground':
                friction_acc = self._physics.traction * - \
                    sign(self.vel.x) * (abs(self.vel.x) > 0)
            else:
                friction_acc = self._physics.air_accel * - \
                    sign(self.vel.x) * (abs(self.vel.x) > 0)

        self.acc.x += friction_acc

        # if in hitstun, make controlled acceleration much smaller
        if self._current_animation.move == 'hit':
            self.controlled_acc.x *= .2
            self.controlled_acc.y *= .2
        self.acc.y += self.controlled_acc.y     # jump accel, DI
        self.acc.y += self._physics.gravity  # fall acceleration
        self.acc += self.knockback_acc          # knockback
        self.acc.x += self.controlled_acc.x     # walk accel, DI

        self.vel += self.acc    # update velocity

        # apply ground and air speed cap
        if abs(self.vel.x) > self._physics.ground_speed and self._state == 'ground':
            self.vel.x = self._physics.ground_speed * sign(self.vel.x)
        if abs(self.vel.x) > self._physics.air_speed and self._state == 'air':
            self.vel.x = self._physics.air_speed * sign(self.vel.x)

        # stop the player if their speed is below a threshold
        if abs(self.vel.x) < .3:
            self.vel.x = 0

        # update the sprite and bounding box for the current animation
        self._current_animation.update_frame()
        self.surf = self._current_animation.get_current_frame()
        self.rect = self.surf.get_rect(center=(self.pos.x, self.pos.y))
        # mirror the sprite horizontally if the player is facing left
        if self._facing_left:
            self.surf = pygame.transform.flip(self.surf, True, False)

        # if player is on the ground, don't let them fall through
        self._stage_collision_check()
        self._barrier_collision_check()  # if the player is crossing over a window barrier

        # update position based on current vel and accel
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

        if self._stage_collision():
            self._state = 'ground'
        else:
            self._state = 'air'

        # reset accelerations so things don't fly out of control
        self.controlled_acc.x = 0
        self.controlled_acc.y = 0
        self.knockback_acc.x = 0
        self.knockback_acc.x = 0
        self.acc.x = 0
        self.acc.y = 0

        # control health bar
        self.healthbar.update_bar()

    def _stage_collision(self) -> list:
        '''
        Checks if the player is in contact with the stage.

        Returns:
            list: A list of collisions, should be empty if the player isn't
                touching the stage.
        '''
        return pygame.sprite.spritecollide(self, self._stage_group,
                                           False, collided=hitbox_collision)

    def _stage_collision_check(self) -> None:
        '''
        Checks whether or not the player's character is on the stage, and
        stops it from going below it.
        '''
        stage_collisions = self._stage_collision()
        if self.vel.y > 0:
            if stage_collisions:
                lowest = stage_collisions[0]
                # Don't let players drop below lowest point
                if self.pos.y < lowest.collision.bottom:
                    self.pos.y = lowest.collision.top + 1
                    self.vel.y = 0
                    self.acc.y = 0
                    if self._state == 'air' and self.current_animation.move != 'hit':
                        self.switch_animation('land')
                    self._state = 'ground'

    def _barrier_collision(self) -> list:
        '''
        Checks if the player is in contact with the barriers.

        Returns:
            list: A list of collisions, should be empty if the player isn't
                touching either barrier.
        '''
        return pygame.sprite.spritecollide(self, self._barrier_group,
                                           False, collided=hitbox_collision)

    def _barrier_collision_check(self) -> None:
        '''
        Checks whether or not the player's touching one of two barriers, and
        stops it from going past these barriers.
        '''
        barrier_collisions = self._barrier_collision()
        if barrier_collisions:
            first_collision = barrier_collisions[0]
            collision_location = first_collision.collision.left
            if self.pos.x < 0 and self.vel.x < 0:
                self.pos.x = collision_location + 1
                self.vel.x = 0
                self.acc.x = 0
            if collision_location != 0:
                max_collision = collision_location
                if self.pos.x > max_collision and self.vel.x > 0:
                    self.pos.x = collision_location - 1
                    self.vel.x = 0
                    self.acc.x = 0

    def attacked(self, damage: int, base_knockback: float, knockback_direction: Vector2) -> None:
        '''
        Called when a the character has been hit. Applied the appropriate
        damage and knockback.

        Args:
            damage (int): The amount of damage taken by the character
            base_knockback (float): The base knockback amount of the move
            knockback_direction (Vector2): The x and y components representing
                the directional knockback of the move
        '''
        if self.current_animation.move != 'hit':
            self.switch_animation('hit')
            self.acc.y += base_knockback * knockback_direction.y
            self.acc.x += base_knockback * knockback_direction.x
            if self._health > 0:
                self._health -= damage
                self.healthbar.damage(damage)
            if self._health <= 0:
                self._health = 0


def hitbox_collision(sprite1: pygame.sprite.Sprite, sprite2: pygame.sprite.Sprite) -> bool:
    '''
    Check if two hitboxes collide.
    Args:
        sprite1 (pygame.sprite.Sprite): First sprite being checked
        sprite2 (pygame.sprite.Sprite): Second sprite being checked
    Returns:
        Boolean of whether or not the sprites have collided
    '''
    return sprite1.collision.colliderect(sprite2.collision)
