import decimal
import math


class ReplaceCalculatingChain:
    def __init__(self, page, scalar):
        from .position import Position
        from components.label import Label
        self.page = page
        self.calculating_position1 = Position(x=self.page.windows.get_width() * 0.5,
                                              y=self.page.windows.get_height() * 0.4)
        self.plus_sign = Label(
            x=self.calculating_position1.x + self.page.matrice.lines[0].elements[0].width,
            y=self.page.windows.get_height() * 0.4,
            width=self.page.matrice.lines[0].elements[0].width,
            height=self.page.matrice.lines[0].elements[0].width,
            color=(250, 250, 250),
            text_color=(0, 0, 0), windows=self.page.windows, text="+")
        self.calculating_position2 = Position(x=self.plus_sign.rect.x + self.plus_sign.rect.width,
                                              y=self.page.windows.get_height() * 0.4)
        self.product_sign = Label(
            x=self.calculating_position2.x + self.page.matrice.lines[0].elements[0].width,
            y=self.page.windows.get_height() * 0.4,
            width=self.page.matrice.lines[0].elements[0].width,
            height=self.page.matrice.lines[0].elements[0].width,
            color=(250, 250, 250),
            text_color=(0, 0, 0), windows=self.page.windows, text="*")

        self.scalar_label = Label(
            x=self.product_sign.rect.x + self.page.matrice.lines[0].elements[0].width,
            y=self.page.windows.get_height() * 0.4,
            width=self.page.matrice.lines[0].elements[0].width,
            height=self.page.matrice.lines[0].elements[0].width,
            color=(250, 250, 250),
            text_color=(0, 0, 0), windows=self.page.windows, text=str(scalar))
        self.equal_sign = Label(
            x=self.scalar_label.rect.x + self.page.matrice.lines[0].elements[0].width,
            y=self.page.windows.get_height() * 0.4,
            width=self.page.matrice.lines[0].elements[0].width,
            height=self.page.matrice.lines[0].elements[0].width,
            color=(250, 250, 250),
            text_color=(0, 0, 0), windows=self.page.windows, text="=")
        self.result_label = Label(x=self.equal_sign.rect.x + self.equal_sign.rect.width,
                                  y=self.page.windows.get_height() * 0.4,
                                  width=self.page.matrice.lines[0].elements[0].width,
                                  height=self.page.matrice.lines[0].elements[0].width,
                                  color=(250, 250, 250),
                                  text_color=(0, 0, 0), windows=self.page.windows, text="_")

        self.value1 = None
        self.value2 = None
        self.scalar = scalar
        self.drawable = True

    def draw(self):
        if self.drawable:
            self.plus_sign.draw()
            self.product_sign.draw()
            self.scalar_label.draw()
            self.equal_sign.draw()
            self.result_label.draw()

    def calculate(self):
        try:
            result = self.value1 + self.scalar * self.value2
            self.result_label.text = str(result)
        except TypeError:
            print(TypeError)

    def update_result_label(self):
        from components.label import Label
        self.result_label = Label(x=self.equal_sign.rect.x + self.equal_sign.rect.width,
                                  y=self.page.windows.get_height() * 0.4,
                                  width=self.page.matrice.lines[0].elements[0].width,
                                  height=self.page.matrice.lines[0].elements[0].width,
                                  color=(250, 250, 250),
                                  text_color=(0, 0, 0), windows=self.page.windows, text="_")


class ScalarCalculatingChain:
    def __init__(self, page, scalar):
        from .position import Position
        from components.label import Label

        self.page = page
        self.scalar = scalar
        self.calculating_position = Position(x=0.5 * self.page.windows.get_width(),
                                             y=self.page.windows.get_height() * 0.4)
        self.product_sign = Label(
            x=self.calculating_position.x + self.page.matrice.lines[0].elements[0].width,
            y=self.page.windows.get_height() * 0.4,
            width=self.page.matrice.lines[0].elements[0].width,
            height=self.page.matrice.lines[0].elements[0].width,
            color=(250, 250, 250),
            text_color=(0, 0, 0), windows=self.page.windows, text="*")

        self.scalar_label = Label(
            x=self.product_sign.rect.x + self.page.matrice.lines[0].elements[0].width,
            y=self.page.windows.get_height() * 0.4,
            width=self.page.matrice.lines[0].elements[0].width,
            height=self.page.matrice.lines[0].elements[0].width,
            color=(250, 250, 250),
            text_color=(0, 0, 0), windows=self.page.windows, text=str(scalar))
        self.equal_sign = Label(
            x=self.scalar_label.rect.x + self.page.matrice.lines[0].elements[0].width,
            y=self.page.windows.get_height() * 0.4,
            width=self.page.matrice.lines[0].elements[0].width,
            height=self.page.matrice.lines[0].elements[0].width,
            color=(250, 250, 250),
            text_color=(0, 0, 0), windows=self.page.windows, text="=")
        self.result_label = Label(x=self.equal_sign.rect.x + self.equal_sign.rect.width,
                                  y=self.page.windows.get_height() * 0.4,
                                  width=self.page.matrice.lines[0].elements[0].width,
                                  height=self.page.matrice.lines[0].elements[0].width,
                                  color=(250, 250, 250),
                                  text_color=(0, 0, 0), windows=self.page.windows, text="_")
        self.value = None
        self.scalar = scalar

    def update_result_label(self):
        from components.label import Label
        self.result_label = Label(x=self.equal_sign.rect.x + self.equal_sign.rect.width,
                                  y=self.page.windows.get_height() * 0.4,
                                  width=self.page.matrice.lines[0].elements[0].width,
                                  height=self.page.matrice.lines[0].elements[0].width,
                                  color=(250, 250, 250),
                                  text_color=(0, 0, 0), windows=self.page.windows, text="_")

    def calculate(self):
        try:
            result = self.value * self.scalar
            self.result_label.text = str(result)
        except TypeError:
            print('type error')


class ProductCalculatingChain:
    @staticmethod
    def get_label(page):
        from components.label import Label
        return Label(x=0.95 * page.windows.get_width(),
                     y=0.57 * page.windows.get_height(),
                     width=page.windows.get_width() / (page.matrice1.nb_columns * 6),
                     height=page.matrice1.height / 5, color=(250, 250, 250),
                     text_color=(0, 0, 0),
                     windows=page.windows, text="_")

    def __init__(self, page):
        self.products = []
        self.plus_signs = []
        self.drawable = True
        self.equal_sign = None
        self.result_label = None
        self.elements_width = page.windows.get_width() / (page.matrice1.nb_columns * 6)
        self.elements_height = page.matrice1.height / 5

    def draw(self):
        if self.drawable and len(self.products) != 0:
            font_size = self.get_font_size()
            for product in self.products:
                product.draw(font_size=font_size)
            for plus_sign in self.plus_signs:
                plus_sign.draw()

            self.equal_sign.draw()
            self.result_label.draw()

    def calculate(self):
        result = 0
        for product in self.products:
            result += product.calculate()
        self.result_label.text = str(round(result, 2))

    def get_font_size(self):
        return int(math.sqrt(3 / len(self.products)) * 24)

    def fit_component(self, component):
        component.font_size = self.get_font_size()
        component.rect.width = self.elements_width
        component.rect.height = self.elements_height
