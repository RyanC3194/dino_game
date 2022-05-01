import os
import tkinter as tk


class NoGraphic:
    def display(self, state):
        pass

    def end(self, state):
        pass


class TerminalGraphic:
    def display(self, state):
        os.system('cls' if os.name == 'nt' else 'clear')
        height = state.height
        width = state.width
        print("-" * width)
        for h in range(height - 1, -1, -1):
            print("|", end="")
            for w in range(width):
                c = "*" if state.dino.is_inside((w, h)) else " "
                for obstacle in state.obstacles:
                    c = "!" if obstacle.is_inside((w, h)) else c
                print(c, end="")
            print("|")
        print("-" * width)

    def end(self, state):
        print("Your score: " + str(state.point))


class TkGraphic:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = tk.Tk()
        self.window.title("Dino")
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.pack()
        self.clear_canvas()
        self.window.update()

    def display(self, state):
        self.clear_canvas()
        self.draw_dino(state)
        self.draw_obstacles(state)

        self.canvas.update()

    def draw_dino(self, state):
        self.draw_sprite(state, state.dino)

    def draw_obstacles(self, state):
        obstacles = state.obstacles
        for obstacle in obstacles:
            self.draw_sprite(state, obstacle)

    def end(self, state):
        self.clear_canvas()
        self.canvas.create_text(self.width / 2, self.height / 2, text="Game Ended. Your Score: " + str(state.point),
                                font='100')
        self.canvas.create_text(self.width / 2, self.height / 2 + self.height / 8, text="Restart", font="50")
        self.window.mainloop()

    def draw_sprite(self, state, sprite):
        x1, y1 = self.map_coordinate(state, sprite.x, sprite.y)
        x2, y2 = self.map_coordinate(state, sprite.x + sprite.width, sprite.y + sprite.height)
        self.canvas.create_rectangle(x1, self.height - y1, x2, self.height - y2)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="white")

    def map_coordinate(self, state, x, y):
        return x / state.width * self.width, y / state.height * self.height
