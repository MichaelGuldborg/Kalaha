import random

from kalaha.kalaha_env import KalahaEnv

INFINITY = 1.0e400  # constant


class KalahaAgent(object):
    def __init__(self, index, n_pits, n_balls, name="KalahaAgent", strategy="max_balls", enemy=None):
        self.index = index
        self.n_pits = n_pits
        self.n_balls = n_balls  # per pit
        self.name = name
        self.strategy = strategy
        self.enemy = enemy

    def __repr__(self):
        """Returns a string representation of the Agent."""
        return "{}) {} with strategy: {}".format(self.index, self.name, self.strategy)

    def act(self, state, strategy=None):
        strategy = self.strategy if strategy is None else "random"

        if strategy == "playbook":
            action = self.act_with_playbook(state)
            return action

        if strategy == "max_score":
            action, value = self.act_with_max_score(state)
            print("player: {}, action: {}, value: {}".format(self.index, action, value))
            return action

        return self.act_with_simple_strategy(state, strategy=strategy)

    def act_with_playbook(self, state):
        index_start, index_end = self.index_range()
        for i in range(index_start, index_end):
            if state[i] == i:  # if action gives extra turn
                return self.index_to_action(i)

        # else use max_balls strategy
        return self.act_with_simple_strategy(state, strategy="max_balls")

    def act_with_max_score(self, state):
        initial_score = state[KalahaEnv.target_index(self.index, self.n_pits)]
        final_action = 1
        final_score = 0

        index_start, index_end = self.index_range()
        for i in range(index_start, index_end):
            action = self.index_to_action(i)
            # for each action in player pit range

            next_state, next_player = KalahaEnv.eval_action(state, self.index, action)
            score = next_state[KalahaEnv.target_index(self.index, self.n_pits)]
            if next_player == self.index:
                next_action, next_score = self.act_with_max_score(next_state)
                score = next_score

            if score > final_score:
                final_action = action
                final_score = score

        if final_score == initial_score:
            return self.act_with_simple_strategy(state, "front"), final_score

        # return the best score and move so far
        return final_action, final_score

    def act_with_simple_strategy(self, state, strategy="random"):
        if strategy == "random":
            return random.randint(1, 6)
        if strategy == "human":
            return int(input("It's your turn {}\nPlease enter a number from 1 to 6\n".format(self.name)))

        index_start, index_end = self.index_range()
        if strategy == "max_balls":
            action_index = -1
            for i in range(index_start, index_end):
                if action_index == -1 or state[i] >= state[action_index]:
                    action_index = i
            return self.index_to_action(action_index)

        if strategy == "front":
            action_index = -1
            for i in range(index_start, index_end):
                if action_index == -1 or state[action_index] == 0:
                    action_index = i
            return self.index_to_action(action_index)

        if strategy == "back":
            action_index = -1
            for i in range(index_start, index_end):
                if action_index == -1 or state[i] != 0:
                    action_index = i
            return self.index_to_action(action_index)

    def index_range(self):
        index_start = 1 + self.index + self.index * self.n_pits
        index_end = index_start + self.n_pits
        # print("state_index_start:", state_index_start)
        # print("state_index_end:", state_index_end)
        return index_start, index_end

    def index_to_action(self, action_index):
        # print("action_index:", action_index)
        return action_index - self.index * self.n_pits - self.index
