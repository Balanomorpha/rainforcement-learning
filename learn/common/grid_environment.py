class GridEnvironment():
    def __init__(self):
        grid = [
            [0, 0, 0, 1],
            [0, 9, 0, -1],
            [0, 0, 0, 0, ],
        ]
        self.grid = grid
        self.INITIAL_GRID = grid

        self.DEFAULT_REWARD = -0.04
        self.MOVE_PENALTY = 0.8

    def reset(self):
        pass
    
    def get_actions(self):
        return [Actions.UP,Actions.DOWN,Actions.LEFT,Actions.RIGHT]

from enum import Enum

class Actions(Enum):
    UP = 1
    DOWN = -1
    RIGHT = -2
    LEFT = 2


class State():
    def __init__(self, row=-1, column=-1):
        self.row = row
        self.column = column

    def __eq__(self, value: State):
        return self.row == value.row and self.column == value.column
