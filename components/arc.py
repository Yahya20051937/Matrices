import pygame


class Arc:
    VEL = 15

    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height
        self.elements = []
        self.get_elements()

    def get_elements(self):
        self.elements = []
        for i in range(int(self.height)):
            self.elements.append(pygame.Rect(self.x, self.y + i, 5, 1))

    def draw(self, windows):
        for element in self.elements:
            pygame.draw.rect(windows, (0, 0, 0), element)

    def move_vertically(self, position):
        # the first element of the list should be in the new position x and y
        first_element = self.elements[0]
        if first_element.y > position.y:
            difference = first_element.y - position.y
            if difference > Arc.VEL:
                for point in self.elements:
                    point.y -= Arc.VEL
            else:
                for point in self.elements:
                    point.y -= difference
        elif first_element.y < position.y:
            difference = position.y - first_element.y
            if difference > Arc.VEL:
                for point in self.elements:
                    point.y += Arc.VEL
            else:
                for point in self.elements:
                    point.y += difference
