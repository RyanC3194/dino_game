import keyboard
import random

from game_enums import *
from feature_extractor import *


class DinoAgent:
    def get_action(self, state):
        print("Not Defined")
        raise Exception("Not implemented")


# always jump
class JumpAgent(DinoAgent):
    def get_action(self, state):
        return DinoActions.Jump


class KeyBoardAgent(DinoAgent):
    def get_action(self, state):
        # up arrow is pressed
        if keyboard.is_pressed(keyboard.KEY_UP) or keyboard.is_pressed("w") or keyboard.is_pressed(" "):
            return DinoActions.Jump
        return DinoActions.Nothing


class QLearningAgent(DinoAgent):
    def __init__(self, extractor=FirstObstacleExtractor(), alpha=0.1, gamma=1, epsilon=0.1):
        self.q = dict()
        self.extractor = extractor
        self.gamma = gamma
        self.alpha = alpha
        self.epsilon = epsilon

    def compute_action(self, state):
        actions = state.possible_actions()
        max_q = self.get_max_q_value(state)
        best_actions = []
        for action in actions:
            if self.get_q_value(state, action) == max_q:
                best_actions.append(action)
        return random.choice(best_actions)

    def get_q_value(self, state, action):
        simple_state = self.extractor.get_features(state, action)
        q = 0
        if (simple_state, action) in self.q:
            q += self.q[(simple_state, action)]
        else:
            q += 1 if action == DinoActions.Nothing else 0
        return q

    def get_max_q_value(self, state):
        actions = state.possible_actions()
        max_q = float('-inf')
        for action in actions:
            q = self.get_q_value(state, action)
            if q > max_q:
                max_q = q
        return max_q

    def update(self, state, action, new_state):
        simple_state = self.extractor.get_features(state, action)
        if (simple_state, action) in self.q:
            self.q[(simple_state, action)] = (1 - self.alpha) * self.q[(simple_state, action)] + self.alpha * (
                        state.get_reward(action) + self.get_max_q_value(new_state) * self.gamma)
        else:
            self.q[(simple_state, action)] = self.alpha * (
                        state.get_reward(action) + self.get_max_q_value(new_state) * self.gamma)

    def get_action(self, state):
        # update the q value weights
        if random.random() < self.epsilon:
            action = random.choice(state.possible_actions())
        else:
            action = self.compute_action(state)
        new_state = state.get_next(action)
        self.update(state, action, new_state)
        return action
