import math
import random

import pygame


class Element:
    def __init__(self, x, y, width, height, index, windows, with_entries, font_size, value="test"):
        from components.entry import Entry
        from components.label import Label
        from .fraction import Fraction
        from .position import Position
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.index = index
        self.position = Position(x=self.x, y=self.y)
        self.x_velocity = 0
        self.y_velocity = 0
        if value is None:
            self.value = 0
            self.text = "_"
        else:
            self.value = random.randint(1, 9)
            self.text = str(self.value)

        if with_entries:
            self.component = Entry(x=self.x, y=self.y, width=self.width, height=self.height, color=(250, 250, 250),
                                   text_color=(0, 0, 0), text=self.text, windows=windows, font_size=font_size)
        else:
            self.component = Label(x=self.x, y=self.y, width=self.width, height=self.height, color=(250, 250, 250),
                                   text_color=(0, 0, 0), text=self.text, windows=windows, font_size=font_size)

    def update(self):
        self.component.rect.x = self.x
        self.component.rect.y = self.y
        self.component.rect.width = self.width
        self.component.rect.height = self.height
        self.position.x = self.x
        self.position.y = self.y

    def update_coordinates(self):
        self.x = self.component.rect.x
        self.y = self.component.rect.y
        self.position.x = self.x
        self.position.y = self.y

    def draw(self):
        self.component.draw()



