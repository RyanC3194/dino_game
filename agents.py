import keyboard
import sys
from game_enums import *


class DinoAgent:
    def get_action(self, state):
        print("Not Defined")
        sys.exit(1)

# always jump
class JumpAgent(DinoAgent):
    def get_action(self, state):
        return DinoActions.Jump


class KeyBoardAgent(DinoAgent):
    def __init__(self):
        pass

    def get_action(self, state):
        # up arrow is pressed
        if keyboard.is_pressed(keyboard.KEY_UP) or keyboard.is_pressed("w"):
            return DinoActions.Jump
        return DinoActions.Nothing
