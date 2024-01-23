import pygame.time

from components.button import Button
from components.entry import Entry


class Page:

    @staticmethod
    def switch(name, windows):
        from .sum import SumPage
        from .product import ProductPage
        from .inverse import InversePage
        from .el import ElPage
        from .home import HomePage
        pages = {"sum": SumPage, "product": ProductPage, "inverse": InversePage, "el": ElPage, "home": HomePage}
        new_page = pages[name](windows)
        new_page.run()

    FPS = 60

    def __init__(self, windows):
        self.windows = windows
        self.clock = pygame.time.Clock()
        self.components = []
        self.running = False
        self.active_entry = None

    def update(self):
        pass

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(Page.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                for component in self.components:
                    if component.__class__ == Button:
                        component.handle_event(event=event)
                    elif component.__class__ == Entry:
                        component.handle_event(event=event, page=self)

            self.windows.fill((250, 250, 250))
            for component in self.components:
                component.draw()
            self.update()
            pygame.display.update()

