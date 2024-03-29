import os
import tkinter as tk


class NoGraphic:
    def __init__(self):
        self.restart = False
        self.auto_restart = 0

    def display(self, state):
        pass

    def display_with_q(self, state, action):
        pass

    def end(self, state):
        if self.auto_restart > 0:
            self.restart = True
        self.auto_restart -= 1
        pass


class TerminalGraphic:
    def display(self, state):
        os.system('cls' if os.name == 'nt' else 'clear')
        height = state.height
        width = state.width
        print("-" * width)
        for h in range(height - 1, -1, -1):
            print("|", end="")
            for w in range(width / 2):
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
        self.restart_button = tk.Button(self.window, text="restart", command=self.restart, font="50")
        self.quit_button = tk.Button(self.window, text="quit", command=self.quit, font="30")
        self.restart = False
        self.auto_restart = -1
        self.window.update()

    def quit(self):
        self.window.quit()

    def restart(self):
        self.restart_button.place_forget()
        self.quit_button.place_forget()
        self.restart = True
        self.window.quit()

    def display(self, state):
        self.clear_canvas()
        self.draw_dino(state)
        self.draw_obstacles(state)
        self.draw_score(state.point)

        self.canvas.update()

    def draw_score(self, score):
        self.canvas.create_text(self.width - self.width / 15, self.height / 15, text="Score: " + str(score), font="20")

    def end(self, state):
        self.canvas.create_text(self.width / 2, self.height / 2, text="Game Ended. Your Score: " + str(state.point),
                                font='100')

        if self.auto_restart == -1:

            self.restart_button.place(x=self.width / 2, y=self.height / 2 + self.height / 8, anchor="center")
            self.quit_button.place(x=self.width / 2, y=self.height / 2 + 2 * self.height / 8, anchor="center")

            self.window.mainloop()
        elif self.auto_restart == 0:
            self.restart = False
            return
        else:
            self.auto_restart -= 1
            self.restart = True
            return

    def draw_dino(self, state):
        self.draw_sprite(state, state.dino)

    def draw_obstacles(self, state):
        obstacles = state.obstacles
        for obstacle in obstacles:
            self.draw_sprite(state, obstacle)

    def draw_sprite(self, state, sprite):
        x1, y1 = self.map_coordinate(state, sprite.x, sprite.y)
        x2, y2 = self.map_coordinate(state, sprite.x + sprite.width, sprite.y + sprite.height)
        self.canvas.create_rectangle(x1, self.height - y1, x2, self.height - y2)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="white")

    def map_coordinate(self, state, x, y):
        return x / state.width * self.width, y / state.height * self.height


class TkGraphicQAgent(TkGraphic):
    def draw_q_value(self, state, agent):
        actions = state.possible_actions()
        t = ""
        for action in actions:
            t += f"{action}: {agent.get_q_value(state, action)} "
        self.canvas.create_text(self.width / 2, self.height / 15, text=t, font="20")
        self.canvas.update()

    def display_with_q(self, state, agent):
        self.display(state)
        self.draw_q_value(state, agent)
