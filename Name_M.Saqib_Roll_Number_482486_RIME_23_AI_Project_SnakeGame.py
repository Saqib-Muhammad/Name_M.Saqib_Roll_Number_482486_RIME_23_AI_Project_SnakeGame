# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/

import tkinter as tk
import random
import threading
import time

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("400x420")  # Adjusted height for the scorecard
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(self.master, bg="black", width=400, height=400)
        self.canvas.pack()

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.enemy_snake = [(300, 300), (310, 300), (320, 300)]  # Enemy snake initial position
        self.direction = "Right"
        self.enemy_direction = "Left"  # Initial direction for the enemy snake

        self.food = self.create_food()
        self.obstacles = []  # List to store obstacle coordinates
        self.create_obstacles()

        self.score_label = tk.Label(self.master, text="Snake Length: {}".format(len(self.snake)))
        self.score_label.pack()

        self.competition_time_limit = 20  # Specify the competition time limit in seconds

        self.master.bind("<KeyPress>", self.change_direction)

        self.update()

        # Run the competition in a separate thread
        self.competition_thread = threading.Thread(target=self.run_competition)
        self.competition_thread.start()

    def create_food(self):
        x = random.randint(0, 19) * 20
        y = random.randint(0, 19) * 20
        food = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="red")
        return food

    def create_obstacles(self):
        obstacle_coords = [(60, 100), (140, 200), (260, 300)]
        for coord in obstacle_coords:
            obstacle = self.canvas.create_rectangle(coord[0], coord[1], coord[0] + 20, coord[1] + 20, fill="blue")
            self.obstacles.append(obstacle)

    def move_snake(self):
        head = self.snake[0]
        if self.direction == "Right":
            new_head = (head[0] + 20, head[1])
        elif self.direction == "Left":
            new_head = (head[0] - 20, head[1])
        elif self.direction == "Up":
            new_head = (head[0], head[1] - 20)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 20)

        self.snake.insert(0, new_head)
        self.snake = self.snake[:len(self.snake) - 1]  # Remove the last segment to maintain length

    def move_enemy_snake(self):
        # Simple random movement for the enemy snake
        directions = ["Right", "Left", "Up", "Down"]
        new_direction = random.choice(directions)

        head = self.enemy_snake[0]
        if new_direction == "Right":
            new_head = (head[0] + 20, head[1])
        elif new_direction == "Left":
            new_head = (head[0] - 20, head[1])
        elif new_direction == "Up":
            new_head = (head[0], head[1] - 20)
        elif new_direction == "Down":
            new_head = (head[0], head[1] + 20)

        self.enemy_snake.insert(0, new_head)
        self.enemy_snake = self.enemy_snake[:len(self.enemy_snake) - 1]

        self.enemy_direction = new_direction

    def update_score(self):
        self.score_label.config(text="Snake Length: {}".format(len(self.snake)))

    def check_collisions(self):
        head = self.snake[0]

        # Check for boundary collisions
        if head[0] < 0 or head[0] >= 400 or head[1] < 0 or head[1] >= 400:
            self.game_over()

        # Check for self-collision
        if head in self.snake[1:]:
            self.game_over()

        # Check for obstacle collisions
        for obstacle in self.obstacles:
            obstacle_coords = self.canvas.coords(obstacle)
            if head[0] == obstacle_coords[0] and head[1] == obstacle_coords[1]:
                self.game_over()

    def update(self):
        self.move_snake()
        self.check_collisions()

        head = self.snake[0]
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green",
                                         tags="snake")

        self.move_enemy_snake()
        self.canvas.delete("enemy_snake")
        for segment in self.enemy_snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="orange",
                                         tags="enemy_snake")

        self.canvas.delete("food")
        food_coords = self.canvas.coords(self.food)
        if head[0] == food_coords[0] and head[1] == food_coords[1]:
            self.snake.append((0, 0))  # Just to increase the length
            self.canvas.delete("food")
            self.food = self.create_food()
            self.update_score()

        self.master.after(200, self.update)

    def change_direction(self, event):
        if event.keysym == "Right" and not self.direction == "Left":
            self.direction = "Right"
        elif event.keysym == "Left" and not self.direction == "Right":
            self.direction = "Left"
        elif event.keysym == "Up" and not self.direction == "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and not self.direction == "Up":
            self.direction = "Down"

    def game_over(self):
        print("Game Over")
        self.master.destroy()

    def run_competition(self):
        start_time = time.time()
        while time.time() - start_time < self.competition_time_limit:
            time.sleep(1)  # Pause for 1 second
            print("Competition Time Remaining: {} seconds".format(int(self.competition_time_limit - (time.time() - start_time))))
        print("Competition Ended")
        self.game_over()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
