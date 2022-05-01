import time
import random

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
        self.state.create_obstacle()

    def restart(self):
        self.__init__(State(), self.agent, self.graphic, self.tick_speed)
        self.loop()

    def loop(self):
        while self.state.dino.is_alive():
            self.next()
            self.display()
            if not self.state.dino.is_alive():
                break
            time.sleep(self.tick_speed)

        self.graphic.end(self.state)

    def next(self):
        self.state.next(self.agent.get_action(self.state))
        self.tick += 1
        if random.random() < (self.tick - self.last_obstacle_tick ) / 30:
            self.create_obstacle()
        self.state.dino.alive = not self.check_collision()

    # return true if a dino is partially inside a obstacle
    def check_collision(self):
        # check collision
        # only checking the bottom right of the dino is sufficient
        for obstacle in self.state.obstacles:
            if self.state.dino.collide(obstacle):
                return True
        return False

    def create_obstacle(self):
        self.state.create_obstacle(height=random.randint(1,3) * 5)
        self.last_obstacle_tick = self.tick

    def display(self):
        self.graphic.display(self.state)


if __name__ == "__main__":
    print("hello")
    game = Game(State(), KeyBoardAgent(), TkGraphic(width=750, height = 300), 0.1)
    game.loop()
