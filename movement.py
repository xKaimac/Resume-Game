from enum import Enum

class Movement(Enum):
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3
class Direction(Enum):
    DOWN = 1
    UP = -1
    RIGHT = 1
    LEFT = -1
    STOP = 0
