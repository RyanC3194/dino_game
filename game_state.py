import copy

from sprites import *

class State:
    def __init__(self, dino=Dino(), obstacles=list(), point=0, speed=1, difficulty=1, width=250, height=50):
        self.point = point
        self.speed = speed
        self.difficulty = difficulty
        self.height = height
        self.width = width
        self.dino = dino
        self.obstacles = obstacles

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
