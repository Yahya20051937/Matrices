import pygame

from .label import Label


class Button(Label):
    def __init__(self, x, y, width, height, color, func, text_color, windows, text,  page, args=()):
        super().__init__(x=x, y=y, width=width, height=height, color=color, text_color=text_color, windows=windows, text=text)
        self.func = func
        self.args = args
        self.page = page

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.func(*self.args)
