from enum import Enum
import itertools


class Action(Enum):
    UP = 1
    DOWN = -1
    RIGHT = -2
    LEFT = 2

    def get_opposit(self):
        '''
        逆の向きを返す
        UP <-> DOWN
        RIGHT <-> LEFT
        '''
        return self.value*-1


class State():
    def __init__(self, row=-1, column=-1):
        self.row = row
        self.column = column

    def __eq__(self, value):
        return self.row == value.row and self.column == value.column

    def __repr__(self):
        return f'<State({self.row}, {self.column})>'

    def __hash__(self):
        return hash((self.row, self.column))

    def clone(self):
        return State(self.row, self.column)


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

        self.CORRECT_ACTION_PROBABILITY = 0.8  # move_prob
        self.INCORRECT_ACTION_PROBABILITY = (1-self.CORRECT_ACTION_PROBABILITY)/2
        # 反対側に行く可能性はゼロ、横にそれる可能性は正しい方向に行く可能性の残りの半々

        self.ROW_LENGTH = len(grid)
        self.COLUMN_LENGTH = len(grid[0])
        self.ACTIONS = self._get_actions()
        self.STATES = self._get_states()

    def reset(self):
        pass

    def _get_actions(self):
        '''
        動ける向きを返す
        この情報は静的に決まる
        '''
        return [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]

    def _get_states(self):
        '''
        状態のすべての組み合わせを返す
        '''
        return [State(r, c)
                for r in range(self.ROW_LENGTH)
                for c in range(self.COLUMN_LENGTH)]

    def is_normal_state(self, state: State) -> bool:  # can_action_at
        '''
        stateの場所に動けるか
        障害物・ゴール・罠以外の場所
        '''
        return self.INITIAL_GRID[state.row][state.column] == 0

    def get_reward_of(self, state: State) -> (float, bool):
        '''
        # 報酬関数
        return (stateでの報酬, そこで終了かどうか)
        '''
        cell_value = self.grid[state.row][state.column]
        if cell_value == 1:            # ゴール
            return 1, True  # ここの1とcell_valueの1には関連性はない
        elif cell_value == -1:  # 罠
            return -1, True
        else:  # 普通の場所
            return self.DEFAULT_REWARD, False

    def get_transition_probabilities(self, state: State, action: Action):  # transit_func
        '''
        # 遷移関数
        stateから上下右左に行く確率
        '''
        transition_probabilities = {}
        if not self.is_normal_state(state):
            return transition_probabilities

        opposit_action = action.get_opposit()
        for candidate_action in self.ACTIONS:
            if candidate_action == action:
                probability_of_candidate_action = self.CORRECT_ACTION_PROBABILITY
            elif candidate_action == opposit_action:
                probability_of_candidate_action = 0
            else:
                probability_of_candidate_action = self.INCORRECT_ACTION_PROBABILITY

            next_state = self.move(state, candidate_action)

            if next_state in transition_probabilities:
                transition_probabilities[next_state] += probability_of_candidate_action
            else:
                transition_probabilities[next_state] = probability_of_candidate_action
        return transition_probabilities

    def move(self, state: State, action: Action):
        _state = state.clone()
        if action == Action.UP:
            _state.row -= 1
        elif action == Action.DOWN:
            _state.row += 1
        elif action == Action.RIGHT:
            _state.column += 1
        elif action == Action.LEFT:
            _state.column -= 1

        # はみ出してたり、障害物だったらもとのまま
        if _state.row < 0 or self.ROW_LENGTH-1 < _state.row or\
                _state.column < 0 or self.COLUMN_LENGTH-1 < _state.column or\
                self.INITIAL_GRID[_state.row][_state.column] == 9:
            return state
        else:
            return _state

    def dict_to_grid(self, d: dict):
        grid = [[0 for _ in range(self.COLUMN_LENGTH)] for _ in range(self.ROW_LENGTH)]
        for state, value in d.items():
            grid[state.row][state.column] = value
        return grid
