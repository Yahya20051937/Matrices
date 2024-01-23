import math
import time

import pygame


class Label:
    VEL = 3

    def __init__(self, x, y, width, height, color, text_color, windows, font_size=24, text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        if text is None:
            self.text = "0"
        else:
            self.text = str(text)
        self.text_color = text_color
        self.windows = windows
        self.font_size = font_size
        self.drawable = True

    def draw(self):
        if self.drawable:
            pygame.draw.rect(self.windows, self.color, self.rect)
            font = pygame.font.Font(None, self.font_size)
            text_surface = font.render(str(self.text), True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            self.windows.blit(text_surface, text_rect)

    def move_to(self, position):
        if self.rect.x != _round(position.x):
            self.move_horizontally_to(position)
            return

        if self.rect.y != _round(position.y):
            self.move_vertically_to(position)

    def move_horizontally_to(self, position):
        if self.rect.x > position.x:
            difference = self.rect.x - position.x
            if difference > Label.VEL:
                self.rect.x -= Label.VEL
            else:
                self.rect.x = _round(position.x)
        else:
            difference = position.x - self.rect.x
            if difference > Label.VEL:
                self.rect.x += Label.VEL
            else:
                self.rect.x = _round(position.x)

    def move_vertically_to(self, position):
        if self.rect.y > position.y:
            if self.rect.y - Label.VEL > position.y:
                self.rect.y -= Label.VEL
            else:
                self.rect.y = _round(position.y)

        elif self.rect.y < position.y:
            if self.rect.y + Label.VEL < position.y:
                self.rect.y += Label.VEL
            else:
                self.rect.y = _round(position.y)

    def is_in_position(self, position):
        if self.rect.x == _round(position.x) and self.rect.y == _round(position.y):
            return True
        return False


def _round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)
