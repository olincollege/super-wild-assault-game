'''
docstring moment
'''

class Player:
    def __init__(self, player_number: int, character: str) -> None:
        self.__player_number = player_number

    def attack(self, action):
        pass

    def attacked(self, damage, base_knockback, knockback_direction):
        pass
