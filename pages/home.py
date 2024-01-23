import pygame
from components.label import Label
from components.button import Button
from .page import Page
from .sum import SumPage
from .product import ProductPage
from .el import ElPage
from .inverse import InversePage

pygame.font.init()


class HomePage(Page):
    def __init__(self, windows):
        super().__init__(windows)
        self.title = Label(x=windows.get_width() / 2 - windows.get_width() * 0.5 / 2, y=windows.get_height() * 0.05,
                           width=windows.get_width() * 0.5,
                           height=windows.get_height() * 0.1, color=(250, 250, 250), text="Matrices", windows=windows,
                           text_color=(0, 0, 0))
        self.sum_page = Button(x=self.title.rect.x, y=windows.get_height() * 0.15, width=self.title.rect.width,
                               height=self.title.rect.height, color=(0, 0, 0), text="Sum", func=SumPage.switch,
                               windows=windows, text_color=(250, 250, 250), page=self, args=("sum", windows))
        self.product_page = Button(x=self.title.rect.x, y=windows.get_height() * 0.3, width=self.title.rect.width,
                                   height=self.title.rect.height, color=(0, 0, 0), text="Product",
                                   func=ProductPage.switch, windows=windows, text_color=(250, 250, 250), page=self,
                                   args=("product", windows))
        self.el_page = Button(x=self.title.rect.x, y=windows.get_height() * 0.45, width=self.title.rect.width,
                              height=self.title.rect.height, color=(0, 0, 0), text="EL",
                              func=ElPage.switch, windows=windows, text_color=(250, 250, 250), page=self,
                              args=("el", windows))
        self.inverse_page = Button(x=self.title.rect.x, y=windows.get_height() * 0.6, width=self.title.rect.width,
                                   height=self.title.rect.height, color=(0, 0, 0), text="Inverse",
                                   func=InversePage.switch, windows=windows, text_color=(250, 250, 250), page=self,
                                   args=("inverse", windows))

        self.components = [self.title, self.sum_page, self.product_page, self.el_page, self.inverse_page]


