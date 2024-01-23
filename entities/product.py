class Product:
    def __init__(self, element1, product_sign, element2):
        from .position import Position
        self.element1 = element1
        self.element2 = element2
        self.position1 = Position(x=element1.rect.x, y=element1.rect.y)
        self.position2 = Position(x=element2.rect.x, y=element2.rect.y)
        self.value1 = 0
        self.value2 = 0
        self.product_sign = product_sign

    def draw(self, font_size):
        self.element1.font_size = font_size
        self.element2.font_size = font_size
        self.element1.draw()
        self.product_sign.draw()
        self.element2.draw()

    def calculate(self):
        return self.value1 * self.value2
