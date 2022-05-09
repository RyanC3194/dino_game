import copy
import random

from sprites import *


class State:
    def __init__(self, speed=1, width=300, height=50):
        self.point = 0
        self.speed = speed
        self.height = height
        self.width = width
        self.dino = Dino()
        self.obstacles = list()
        self.create_obstacle()
        self.obstacle_tick = 0

    def ended(self):
        return not self.dino.is_alive()

    def next(self, action):
        self.dino.move(action)
        self.dino.alive = not self.check_collision()
        for obstacle in self.obstacles:
            obstacle.move()

        if self.obstacles[0].x < 0:
            self.obstacles.pop(0)

        self.point += self.speed
        self.obstacle_tick += 1

        if self.obstacle_tick > random.normalvariate(100, 20):
            self.create_obstacle(height = random.randint(5, 13))

    def get_next(self, action):
        new_state = copy.deepcopy(self)
        new_state.next(action)
        return new_state

    def create_obstacle(self, width=5, height=12):
        self.obstacles.append(Obstacle(self.width, 0, width, height))
        self.obstacle_tick = 0

    # return true if a dino is partially inside a obstacle
    def check_collision(self):
        # check collision
        # only checking the bottom right of the dino is sufficient
        for obstacle in self.obstacles:
            if self.dino.collide(obstacle):
                return True
        return False

    def possible_actions(self):
        return [DinoActions.Nothing, DinoActions.Jump]

    def get_reward(self, action):
        new_state = self.get_next(action)
        return 1 if not new_state.ended() else -500
