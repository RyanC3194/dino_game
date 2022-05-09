import time
import argparse

# custom imports
from game_state import *
from agents import *
from graphic import *


class Game:
    def __init__(self, state, agent, graphic, tick_speed):
        self.state = state
        self.agent = agent
        self.graphic = graphic
        self.tick = 0
        self.last_obstacle_tick = 0
        self.tick_speed = tick_speed
        self.max_points = 10000

    def restart(self):
        self.__init__(State(), self.agent, self.graphic, self.tick_speed)
        self.tick = 0
        self.graphic.restart = False
        self.loop()

    def loop(self):
        while self.state.point < self.max_points and not self.state.ended():
            time.sleep(self.tick_speed)
            self.next()
            self.display()

        self.graphic.end(self.state)
        if self.graphic.restart:
            self.restart()

    def next(self):
        self.state.next(self.agent.get_action(self.state))
        self.tick += 1

    def display(self):
        self.graphic.display(self.state)


class QGame(Game):
    def display(self):
        self.graphic.display_with_q(self.state, self.agent)


def train(agent, times):
    for i in range(times):
        graphic = NoGraphic()
        graphic.auto_restart = 0
        Game(State(), agent, graphic, 0).loop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--agent", default="KeyBoard", help="Type of agent")
    parser.add_argument("-i", "--iterations", default=100, type=int, help="Training Iterations")
    args = parser.parse_args()
    if args.agent.lower() == "keyboard":
        Game(State(), KeyBoardAgent(), TkGraphic(width=1000, height=350), 0.01).loop()
    elif args.agent.lower() == "q":
        agent = QLearningAgent()
        train(agent, args.iterations)
        agent.epsolon = 0
        QGame(State(), agent, TkGraphicQAgent(width=1000, height=350), 0.00).loop()
    else:
        print("Invalid agent")
