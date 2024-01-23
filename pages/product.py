import math

from .page import Page
from components.label import Label


class ProductPage(Page):
    DEFAULT_NB_LINE1 = 3
    DEFAULT_NB_COLUMN_LINE = 2
    DEFAULT_NB_COLUMN2 = 1

    def __init__(self, windows):
        from entities.matrice import Matrice
        from entities.calculating_chain import ProductCalculatingChain
        from components.button import Button
        from components.entry import Entry
        super().__init__(windows)
        self.title = Label(x=windows.get_width() / 2 - windows.get_width() * 0.5 / 2, y=windows.get_height() * 0.05,
                           width=windows.get_width() * 0.5,
                           height=windows.get_height() * 0.1, color=(250, 250, 250), text="Product", windows=windows,
                           text_color=(0, 0, 0))

        divided_width = self.windows.get_width() / 2
        divided_divided_width = divided_width / 2
        divided_divided_divided_width = divided_divided_width / 2
        divided_divided_divided_divided_width = divided_divided_divided_width / 2

        self.matrice1 = Matrice(nb_lines=ProductPage.DEFAULT_NB_LINE1, nb_columns=ProductPage.DEFAULT_NB_COLUMN_LINE,
                                x=divided_divided_width - divided_divided_divided_width,
                                y=0.1 * windows.get_height(), width=divided_divided_width,
                                height=windows.get_height() * 0.3, windows=self.windows, with_entries=True,
                                value="test")
        self.matrice2 = Matrice(nb_lines=ProductPage.DEFAULT_NB_COLUMN_LINE, nb_columns=ProductPage.DEFAULT_NB_COLUMN2,
                                x=divided_width + self.matrice1.x,
                                width=divided_divided_width, y=0.1 * windows.get_height(),
                                height=windows.get_height() * 0.3, windows=self.windows, with_entries=True,
                                value="test")
        self.product_sign = Label(x=divided_width - divided_divided_divided_divided_width, y=0.1 * windows.get_height(),
                                  width=divided_divided_divided_width, height=windows.get_height() * 0.25, text="X",
                                  color=(250, 250, 250), windows=self.windows, text_color=(0, 0, 0), font_size=60)

        self.calculate_button = Button(x=divided_width - self.matrice1.width / 4, y=self.windows.get_height() * 0.8,
                                       width=self.matrice1.width / 2, height=self.matrice1.height / 3, text="calculate",
                                       color=(0, 0, 0), text_color=(250, 250, 250), func=self.turn_calculating_on,
                                       page=self, windows=self.windows)
        self.refresh_button = Button(x=self.calculate_button.rect.x, y=self.windows.get_height() * 0.9,
                                     width=self.calculate_button.rect.width, height=self.calculate_button.rect
                                     .height, text="refresh", color=(0, 0, 0), text_color=(250, 250, 250),
                                     func=self.refresh,
                                     page=self, windows=self.windows)

        self.nb_lines_entry1 = Entry(x=self.matrice1.x + self.matrice1.width * 0.25, y=self.windows.get_height() * 0.4,
                                     width=self.matrice1.width / 4, height=self.matrice1.height / 5, color=(0, 0, 0),
                                     text_color=(250, 250, 250), windows=self.windows, _max=6,
                                     text=str(ProductPage.DEFAULT_NB_LINE1))
        self.nb_columns_entry1 = Entry(x=self.matrice1.x + self.matrice1.width * 0.55,
                                       y=self.windows.get_height() * 0.4,
                                       width=self.matrice1.width / 4, height=self.matrice1.height / 5, color=(0, 0, 0),
                                       text_color=(250, 250, 250), windows=self.windows, _max=6,
                                       text=str(ProductPage.DEFAULT_NB_COLUMN_LINE))

        self.nb_lines_entry2 = Entry(x=self.matrice2.x + self.matrice2.width * 0.25, y=self.windows.get_height() * 0.4,
                                     width=self.matrice1.width / 4, height=self.matrice1.height / 5, color=(0, 0, 0),
                                     text_color=(250, 250, 250), windows=self.windows, _max=6,
                                     text=str(ProductPage.DEFAULT_NB_COLUMN_LINE))
        self.nb_columns_entry2 = Entry(x=self.matrice2.x + self.matrice2.width * 0.55,
                                       y=self.windows.get_height() * 0.4,
                                       width=self.matrice1.width / 4, height=self.matrice1.height / 5, color=(0, 0, 0),
                                       text_color=(250, 250, 250), windows=self.windows, _max=6,
                                       text=str(ProductPage.DEFAULT_NB_COLUMN2))

        self.result_matrice = Matrice(x=self.matrice1.closing_arc.x, y=0.65 * self.windows.get_height(),
                                      width=self.matrice1.width, height=self.matrice1.height,
                                      nb_columns=self.matrice2.nb_columns, nb_lines=self.matrice1.nb_lines,
                                      windows=self.windows, with_entries=False)

        self.calculating_chain = ProductCalculatingChain(page=self)

        self.components.append(self.matrice1)
        self.components.append(self.matrice2)
        self.components.append(self.result_matrice)
        self.components.append(self.product_sign)
        self.components.append(self.calculate_button)
        self.components.append(self.nb_columns_entry1)
        self.components.append(self.nb_columns_entry2)
        self.components.append(self.nb_lines_entry1)
        self.components.append(self.nb_lines_entry2)
        self.components.append(self.title)
        self.components.append(self.calculating_chain)
        self.components.append(self.refresh_button)

        self.calculating = False
        self.moving_back = False
        self.resulting = False

        self.result_matrice.drawable = False
        self.calculating_chain.drawable = False
        self.refresh_button.drawable = False

        self.matrice1_moving_line_index = 0
        self.matrice2_moving_column_index = 0

        self.matrice1.add_components_to_page(self)
        self.matrice2.add_components_to_page(self)
        self.result_matrice.add_components_to_page(self)
        self.result_matrice.make_elements_drawable_false()

    def update(self):
        self.update_matrices()
        if self.calculating:
            self.calculate()

    def turn_calculating_on(self):
        self.calculate_button.drawable = False
        self.update_calculating_chain()

        self.calculating_chain.drawable = True
        self.nb_lines_entry1.drawable = False
        self.nb_columns_entry1.drawable = False
        self.nb_lines_entry2.drawable = False
        self.nb_columns_entry2.drawable = False
        self.result_matrice.drawable = True

        self.result_matrice.make_elements_drawable_true()

        self.calculating = True

    def calculate(self):
        if not self.resulting:
            if self.moving_back:
                self.move_matrice1_elements(back=True)
                self.move_matrice2_elements(back=True)
                if self.are_matrice1_elements_in_position(back=True) and self.are_matrice2_elements_in_position(
                        back=True):
                    self.increment_indexes()
                    self.moving_back = False
            else:
                self.move_matrice1_elements()
                if self.are_matrice1_elements_in_position():
                    self.move_matrice2_elements()
                    if self.are_matrice2_elements_in_position():
                        self.calculate_and_move_result_label()
                        if self.is_result_label_in_position():
                            self.update_calculating_chain_and_target_matrice_element()
                            self.moving_back = True
        else:
            self.result()

    def result(self):
        from entities.position import Position
        self.calculating_chain.drawable = False
        self.matrice1.drawable = False
        self.matrice2.drawable = False
        self.product_sign.drawable = False
        self.matrice1.make_elements_drawable_false()
        self.matrice2.make_elements_drawable_false()
        self.result_matrice.move_matrice_vertically(Position(self.result_matrice.x,
                                                             self.windows.get_height() / 2 - self.result_matrice.height / 2))
        if self.result_matrice.is_in_position(Position(self.result_matrice.x,
                                                       self.windows.get_height() / 2 - self.result_matrice.height / 2)):
            self.refresh_button.drawable = True

    def refresh(self):
        self.calculating = False
        self.resulting = False

        self.result_matrice.drawable = False
        self.matrice1.drawable = True
        self.matrice2.drawable = True
        self.calculate_button.drawable = True
        self.refresh_button.drawable = False

        self.result_matrice.make_elements_drawable_false()
        self.matrice1.make_elements_drawable_true()
        self.matrice2.make_elements_drawable_true()

        self.result_matrice.change_vertical_position(self.windows.get_height() * 0.65, self)
        self.result_matrice.refresh_elements()

        self.matrice1_moving_line_index = 0
        self.matrice2_moving_column_index = 0

        self.nb_lines_entry1.drawable = True
        self.nb_lines_entry2.drawable = True
        self.nb_columns_entry1.drawable = True
        self.nb_columns_entry2.drawable = True

    def move_matrice1_elements(self, back=False):
        i = 0
        for element in self.matrice1.lines[self.matrice1_moving_line_index].elements:
            if not back:
                target_position = self.calculating_chain.products[i].position1
                self.calculating_chain.fit_component(component=element.component)
            else:
                self.matrice1.fit_component(component=element.component)
                target_position = self.matrice1.lines[self.matrice1_moving_line_index].elements[i].position
            element.component.move_to(target_position)
            i += 1

    def move_matrice2_elements(self, back=False):
        j = 0
        for line in self.matrice2.lines:
            element = line.elements[self.matrice2_moving_column_index]
            if not back:
                target_position = self.calculating_chain.products[j].position2
                self.calculating_chain.fit_component(component=element.component)
            else:
                self.matrice2.fit_component(component=element.component)
                target_position = element.position

            element.component.move_to(target_position)
            j += 1

    def are_matrice1_elements_in_position(self, back=False):
        in_position = True
        i = 0
        for element in self.matrice1.lines[self.matrice1_moving_line_index].elements:
            if not back:
                target_position = self.calculating_chain.products[i].position1
            else:
                target_position = self.matrice1.lines[self.matrice1_moving_line_index].elements[i].position
            if not element.component.is_in_position(target_position):
                in_position = False
            else:
                self.calculating_chain.products[i].value1 = element.value
            i += 1
        return in_position

    def are_matrice2_elements_in_position(self, back=False):
        in_position = True
        j = 0
        for line in self.matrice2.lines:
            element = line.elements[self.matrice2_moving_column_index]
            if not back:
                target_position = self.calculating_chain.products[j].position2
            else:
                target_position = element.position
            if not element.component.is_in_position(target_position):
                in_position = False
            else:
                self.calculating_chain.products[j].value2 = element.value
            j += 1
        return in_position

    def calculate_and_move_result_label(self):
        self.calculating_chain.calculate()
        target_matrice_element = self.result_matrice.lines[self.matrice1_moving_line_index].elements[self.matrice2_moving_column_index]
        self.result_matrice.fit_component(component=self.calculating_chain.result_label)
        self.calculating_chain.result_label.move_to(target_matrice_element.position)

    def update_calculating_chain_and_target_matrice_element(self):
        from entities.calculating_chain import ProductCalculatingChain
        target_matrice_element = self.result_matrice.lines[self.matrice1_moving_line_index].elements[
            self.matrice2_moving_column_index]
        target_matrice_element.component.drawable = False
        target_matrice_element.component = self.calculating_chain.result_label
        self.calculating_chain.result_label = ProductCalculatingChain.get_label(page=self)
        self.components.append(target_matrice_element.component)

    def is_result_label_in_position(self):
        target_matrice_element = self.result_matrice.lines[self.matrice1_moving_line_index].elements[
            self.matrice2_moving_column_index]
        if self.calculating_chain.result_label.is_in_position(target_matrice_element.position):
            return True
        return False

    def increment_indexes(self):
        if self.matrice2_moving_column_index != self.matrice2.nb_columns - 1:
            self.matrice2_moving_column_index += 1
        else:
            if self.matrice1_moving_line_index != self.matrice1.nb_lines - 1:
                self.matrice1_moving_line_index += 1
                self.matrice2_moving_column_index = 0
            else:
                self.resulting = True

    def update_calculating_chain(self):
        from entities.product import Product
        from entities.calculating_chain import ProductCalculatingChain
        divided_width = self.windows.get_width() * 0.9 / self.matrice1.nb_columns
        divided_divided_width = divided_width / 3
        self.calculating_chain.products = []
        self.calculating_chain.plus_signs = []
        for i in range(self.matrice1.nb_columns):
            calculating_label1 = Label(x=i * divided_width + 0.3 * divided_divided_width,
                                       y=0.57 * self.windows.get_height(),
                                       width=self.windows.get_width() / (self.matrice1.nb_columns * 6),
                                       height=self.matrice1.height / 5, color=(250, 250, 250), text_color=(0, 0, 0),
                                       windows=self.windows, text="_")
            product_sign = Label(x=i * divided_width + 1 * divided_divided_width, y=0.57 * self.windows.get_height(),
                                 width=self.windows.get_width() / (self.matrice1.nb_columns * 9),
                                 height=self.matrice1.height / 5, color=(250, 250, 250), text_color=(0, 0, 0),
                                 windows=self.windows, text="x")
            calculating_label2 = Label(x=i * divided_width + 1.7 * divided_divided_width,
                                       y=0.57 * self.windows.get_height(),
                                       width=self.windows.get_width() / (self.matrice1.nb_columns * 6),
                                       height=self.matrice1.height / 5, color=(250, 250, 250), text_color=(0, 0, 0),
                                       windows=self.windows, text="_")
            product = Product(element1=calculating_label1, product_sign=product_sign, element2=calculating_label2)
            self.calculating_chain.products.append(product)

            if i + 1 != self.matrice1.nb_columns:
                plus_sign = Label(
                    x=(i + 1) * divided_width - self.windows.get_width() / (6 * self.matrice1.nb_columns),
                    y=0.57 * self.windows.get_height(),
                    width=self.windows.get_width() / (self.matrice1.nb_columns * 9),
                    height=self.matrice1.height / 5, color=(250, 250, 250), text_color=(0, 0, 0),
                    windows=self.windows, text="+")
                self.calculating_chain.plus_signs.append(plus_sign)

        self.calculating_chain.equal_sign = Label(x=0.9 * self.windows.get_width(), y=0.57 * self.windows.get_height(),
                                                  width=self.windows.get_width() / (self.matrice1.nb_columns * 6),
                                                  height=self.matrice1.height / 5, color=(250, 250, 250),
                                                  text_color=(0, 0, 0),
                                                  windows=self.windows, text="=")
        self.calculating_chain.result_label = ProductCalculatingChain.get_label(page=self)

    def update_matrices(self):
        """
        if a change in the columns and lines entries is made
        Here we first update the number of lines in the first matrix and the number of columns in the second matrix, then we make sure that the number of columns and in the first matrix and of lines in the second matrix are always equal
        :return:
        """
        if not self.calculating:
            try:

                self.matrice1.update(new_nb_lines=int(self.nb_lines_entry1.text),
                                     new_nb_columns=self.matrice1.nb_columns,
                                     page=self)
                self.matrice2.update(new_nb_lines=self.matrice2.nb_lines,
                                     new_nb_columns=int(self.nb_columns_entry2.text),
                                     page=self)

                if self.matrice1.nb_columns != int(self.nb_columns_entry1.text):  # we check what was changed first
                    self.matrice1.update(new_nb_lines=self.matrice1.nb_lines,
                                         new_nb_columns=int(self.nb_columns_entry1.text), page=self)
                    self.matrice2.update(new_nb_lines=self.matrice1.nb_columns,
                                         new_nb_columns=self.matrice2.nb_columns,
                                         page=self)
                    self.nb_lines_entry2.text = self.nb_columns_entry1.text

                elif self.matrice2.nb_lines != int(self.nb_lines_entry2.text):
                    self.matrice2.update(new_nb_lines=int(self.nb_lines_entry2.text),
                                         new_nb_columns=self.matrice2.nb_columns, page=self)
                    self.matrice1.update(new_nb_lines=self.matrice1.nb_lines, new_nb_columns=self.matrice2.nb_lines,
                                         page=self)
                    self.nb_columns_entry1.text = self.nb_lines_entry2.text
                self.result_matrice.update(new_nb_lines=self.matrice1.nb_lines, new_nb_columns=self.matrice2.nb_columns,
                                           page=self, new_elements_drawable=False)
            except ValueError:
                pass

            finally:
                self.matrice1.update_values()
                self.matrice2.update_values()


def get_font_size(nb_columns, nb_lines):
    return int(math.sqrt(9 / (nb_columns * nb_lines)) * 24)
