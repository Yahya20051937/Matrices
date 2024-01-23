import pygame
from .label import Label


class Entry(Label):
    def __init__(self, x, y, width, height, color, text_color, windows, font_size=24, text="", _max=99):
        super().__init__(x=x, y=y, width=width, height=height, color=color, text_color=text_color, windows=windows,
                         text=text, font_size=font_size)
        self.max = _max

    def handle_event(self, event, page):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if page.active_entry == self:
                    page.active_entry = None
                else:
                    page.active_entry = self
        elif event.type == pygame.KEYDOWN and page.active_entry == self:
            if event.key == pygame.K_BACKSPACE:
                if len(str(self.text)) > 0:
                    if len(self.text) > 1:
                        self.text = self.text[:-1]
                    else:
                        self.text = "_"
            else:
                if event.unicode in [str(i) for i in range(10)]:
                    value = int(event.unicode)
                    if self.text == "_" or self.text == "0":
                        if value < self.max:
                            self.text = str(int(event.unicode))
                    else:
                        if self.text != "-":
                            if "/" in self.text:
                                if self.text[-1] == "/":
                                    if value != 0:
                                        self.text += str(value)
                            else:
                                if int(self.text) + value < self.max:
                                    self.text += str(value)
                        else:
                            if -value < self.max:
                                self.text = f'-{value}'

                elif event.unicode == "-":
                    if self.text == "_":
                        self.text = "-"

                elif event.unicode == "/":
                    if self.text != "_":
                        self.text += "/"

