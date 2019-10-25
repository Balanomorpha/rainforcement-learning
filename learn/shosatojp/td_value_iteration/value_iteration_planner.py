from pprint import pprint
from grid_environment import GridEnvironment, State, Action


class ValueIterationPlanner():
    def __init__(self, env: GridEnvironment):
        self.env = env
        self.log = []

    def initialize(self):
        self.env.reset()

    def transitions_at(self, state: State, action: Action):
        '''
        価値を付加してるだけ
        この関数の存在価値？
        '''
        transition_probabilities = self.env.get_transition_probabilities(state, action)
        for _state, probability in transition_probabilities.items():
            reward, _ = self.env.get_reward_of(_state)
            yield probability, _state, reward

    def plan(self, gamma: float = 0.9, threshold: float = 0.0001):
        '''
        # 動的計画法で価値関数V(state)を更新する
        float: 減衰
        threshold: 更新を停止するときの更新量
        '''
        self.initialize()
        V = {state: 0 for state in self.env.STATES}

        while True:
            delta = 0

            for state in V:
                if not self.env.is_normal_state(state):
                    continue

                expected_rewards = []
                for action in self.env.ACTIONS:
                    expected_rewards.append(sum([probability*(reward+gamma*V[_state])
                                                 for (probability, _state, reward) in self.transitions_at(state, action)]))
                max_reward = max(expected_rewards)

                # すべてのStateに対して、最大のdeltaを求める
                delta = max(delta, max_reward-V[state])
                V[state] = max_reward

            if delta < threshold:
                break

        return self.env.dict_to_grid(V)


planner = ValueIterationPlanner(env=GridEnvironment())
pprint(planner.plan())
