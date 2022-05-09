from game_enums import *


class Sprite:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def pos(self):
        return self.x, self.y

    def is_inside(self, pos):
        x, y = pos
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height

    def collide(self, sprite):
        print("collide method not implemented")
        raise


class Dino(Sprite):
    def __init__(self, x=10, y=0.0, width=15, height=10, alive=True, acceleration=-1.5, jump_speed=17,
                 dino_state=DinoState.GROUND):
        super().__init__(x, y, width, height)
        self.state = dino_state
        self.acceleration = acceleration
        self.alive = alive
        self.jump_speed = jump_speed
        self.speed = 0

    def collide(self, sprite):
        for x in range(self.x, self.x + self.width):
            if sprite.is_inside((x, self.y)):
                return True
        return False

    def move(self, input=DinoActions.Nothing):
        if input == DinoActions.Jump:
            if self.state == DinoState.GROUND:
                self.speed = self.jump_speed
            elif self.state == DinoState.AIR_UP and self.y <= self.jump_speed:
                self.speed = self.jump_speed
            elif self.state == DinoState.AIR_DOWN:
                self.speed += self.acceleration / 3
            else:
                self.speed += self.acceleration
        else:
            self.speed += self.acceleration

        self.y += self.speed * 0.1
        if self.y < 0:
            self.speed = 0
            self.y = 0
        self.update_state()

    def update_state(self):
        if self.y == 0:
            self.state = DinoState.GROUND
        else:
            if self.speed > 0:
                self.state = DinoState.AIR_UP
            else:
                self.state = DinoState.AIR_DOWN

    def is_alive(self):
        return self.alive


class Obstacle(Sprite):
    def __init__(self, x=0, y=0, width=5, height=15, speed=-15):
        super().__init__(x, y, width, height)
        self.speed = speed

    # should only be able to move left
    def move(self):
        self.x += self.speed * 0.1

    def __repr__(self):
        return f"Obstacle at: {self.x}"