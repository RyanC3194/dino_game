import time

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

    def restart(self):
        self.__init__(State(), self.agent, self.graphic, self.tick_speed)
        self.tick = 0
        self.graphic.restart = False
        self.loop()

    def loop(self):
        while not self.state.ended():
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


def train(agent, times):
    for i in range(times):
        game = Game(State(), agent, NoGraphic)
        game.loop()


if __name__ == "__main__":
    print("hello")
    game = Game(State(), KeyBoardAgent(), TkGraphic(width=1000, height = 350), 0.01)
    game.loop()
