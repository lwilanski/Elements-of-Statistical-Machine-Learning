import tkinter as tk
import numpy as np


class DrawingApp:
    def __init__(self, root, canvas_size=420, pixel_size=15):
        self.root = root
        self.canvas_size = canvas_size
        self.pixel_size = pixel_size
        self.array_size = self.canvas_size // self.pixel_size
        self.array = np.zeros((self.array_size, self.array_size), dtype=np.uint8)
        self.colors = {'#000000': 0, '#666666': 102, '#CCCCCC': 204, '#FFFFFF': 255}

        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg='#FFFFFF')
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.save_to_array)

        self.rectangles = []

        for x in range(self.array_size):
            row = []
            for y in range(self.array_size):
                rect = self.canvas.create_rectangle(y * self.pixel_size, x * self.pixel_size,
                                                    (y + 1) * self.pixel_size, (x + 1) * self.pixel_size,
                                                    fill='#000000')
                row.append(rect)
            self.rectangles.append(row)

    def validate_move(self, current_position, move):
        x, y = current_position[0], current_position[1]
        dx, dy = move[0], move[1]
        if 0 <= x + dx < self.array_size and 0 <= y + dy < self.array_size:
            return True

        return False

    def paint(self, event):
        x, y = event.x // self.pixel_size, event.y // self.pixel_size
        neighbors = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1), (2, 0), (-2, 0), (0, 2), (0, -2)]

        for neighbor in neighbors:
            if self.validate_move((x, y), neighbor):
                if abs(neighbor[0]) + abs(neighbor[1]) == 0:
                    self.canvas.itemconfig(self.rectangles[y + neighbor[1]][x + neighbor[0]], fill='#FFFFFF')

                elif abs(neighbor[0]) + abs(neighbor[1]) == 1 and self.colors['#CCCCCC'] > self.colors[
                    self.canvas.itemcget(self.rectangles[y + neighbor[1]][x + neighbor[0]], 'fill')]:
                    self.canvas.itemconfig(self.rectangles[y + neighbor[1]][x + neighbor[0]], fill='#CCCCCC')

                else:
                    if self.colors['#666666'] > self.colors[self.canvas.itemcget(self.rectangles[y + neighbor[1]][x + neighbor[0]], 'fill')]:
                        self.canvas.itemconfig(self.rectangles[y + neighbor[1]][x + neighbor[0]], fill='#666666')

    def save_to_array(self, event):
        for y in range(self.array_size):
            for x in range(self.array_size):
                color = self.canvas.itemcget(self.rectangles[y][x], 'fill')
                self.array[y, x] = self.colors[color]

    def get_array(self):
        return self.array
