import pygame

from components.label import Label
from .page import Page


class InversePage(Page):
    def __init__(self, windows):
        super().__init__(windows)
        self.title = Label(x=windows.get_width() / 2 - windows.get_width() * 0.5 / 2, y=windows.get_height() * 0.05,
                           width=windows.get_width() * 0.5,
                           height=windows.get_height() * 0.1, color=(250, 250, 250), text="Inverse", windows=windows,
                           text_color=(0, 0, 0))
        self.components.append(self.title)


