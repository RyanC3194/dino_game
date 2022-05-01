import copy

from sprites import *

class State:
    def __init__(self, dino=Dino(), speed=1, width=500, height=50):
        self.point = 0
        self.speed = speed
        self.height = height
        self.width = width
        self.dino = dino
        self.obstacles = list()

    def next(self, action):
        self.dino.move(action)
        for obstacle in self.obstacles:
            obstacle.move()
        self.point += self.speed

    def get_next(self, action):
        new_state = copy.deepcopy(self)
        new_state.next(action)
        return new_state

    def create_obstacle(self, width = 5, height=15):
        self.obstacles.append(Obstacle(self.width, 0, width, height))
