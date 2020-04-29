from enum import Enum


class GameStates(Enum):
    INVALID_STATE = 0
    PLAYER_TURN = 1
    ENEMIES_TURN = 2
    PLAYER_DEAD = 3
    SHOW_INVENTORY = 4
    DROP_INVENTORY = 5
