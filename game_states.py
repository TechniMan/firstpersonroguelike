from enum import Enum


class GameStates(Enum):
    INVALID_STATE = 0
    PLAYER_TURN = 1
    ENEMIES_TURN = 2
