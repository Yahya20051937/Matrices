import pygame
from pages.home import HomePage

WIDTH = 800
HEIGHT = 500
FPS = 60
BACKGROUND = (250, 250 , 250)

WINDOWS = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matrices")
page = HomePage(windows=WINDOWS)
page.run()


