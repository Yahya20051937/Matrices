import math

from .page import Page
from components.label import Label


class SumPage(Page):
    DEFAULT_NB_LINES = 2
    DEFAULT_NB_COLUMNS = 2

    def __init__(self, windows):
        from entities.matrice import Matrice
        from components.label import Label
        from components.button import Button
        from components.entry import Entry
        from entities.position import Position
        super().__init__(windows)
        self.title = Label(x=windows.get_width() / 2 - windows.get_width() * 0.5 / 2, y=windows.get_height() * 0.05,
                           width=windows.get_width() * 0.5,
                           height=windows.get_height() * 0.05, color=(250, 250, 250), text="Sum", windows=windows,
                           text_color=(0, 0, 0))

        divided_width = self.windows.get_width() / 2
        divided_divided_width = divided_width / 2
        divided_divided_divided_width = divided_divided_width / 2
        divided_divided_divided_divided_width = divided_divided_divided_width / 2

        self.matrice1 = Matrice(nb_lines=SumPage.DEFAULT_NB_LINES, nb_columns=SumPage.DEFAULT_NB_COLUMNS,
                                x=divided_divided_width - divided_divided_divided_width,
                                y=0.1 * windows.get_height(), width=divided_divided_width,
                                height=windows.get_height() * 0.3, windows=self.windows, with_entries=True,
                                value="test")
        self.matrice2 = Matrice(nb_lines=SumPage.DEFAULT_NB_LINES, nb_columns=SumPage.DEFAULT_NB_COLUMNS,
                                x=divided_width + self.matrice1.x,
                                width=divided_divided_width, y=0.1 * windows.get_height(),
                                height=windows.get_height() * 0.3, windows=self.windows, with_entries=True,
                                value="test")
        self.plus_sign = Label(x=divided_width - divided_divided_divided_divided_width, y=0.1 * windows.get_height(),
                               width=divided_divided_divided_width, height=windows.get_height() * 0.25, text="+",
                               color=(250, 250, 250), windows=self.windows, text_color=(0, 0, 0), font_size=60)

        self.calculate_button = Button(x=divided_width - self.matrice1.width / 4, y=self.windows.get_height() * 0.7,
                                       width=self.matrice1.width / 2, height=self.matrice1.height / 3, text="calculate",
                                       color=(0, 0, 0), text_color=(250, 250, 250), func=self.turn_calculating_on,
                                       page=self, windows=self.windows)

        self.refresh_button = Button(x=self.calculate_button.rect.x, y=self.windows.get_height() * 0.85,
                                     width=self.calculate_button.rect.width, height=self.calculate_button.rect
                                     .height, text="refresh", color=(0, 0, 0), text_color=(250, 250, 250),
                                     func=self.refresh,
                                     page=self, windows=self.windows)

        self.calculating_position1 = Position(x=self.matrice1.closing_arc.x, y=0.45 * self.windows.get_height())

        self.calculating_position2 = Position(x=self.matrice2.opening_arc.x - self.matrice1.lines[0].elements[0].width,
                                              y=0.45 * self.windows.get_height())

        self.result_matrice = Matrice(x=self.matrice1.closing_arc.x, y=0.65 * self.windows.get_height(),
                                      width=self.matrice1.width, height=self.matrice1.height,
                                      nb_columns=self.matrice1.nb_columns, nb_lines=self.matrice1.nb_lines,
                                      windows=self.windows, with_entries=False)

        self.equal_sign = Label(x=self.matrice2.opening_arc.x,
                                y=self.calculating_position2.y - self.plus_sign.rect.height * 0.3,
                                width=divided_divided_divided_width, height=windows.get_height() * 0.25, text="=",
                                color=(250, 250, 250), windows=self.windows, text_color=(0, 0, 0), font_size=60)
        self.result_label_position = Position(x=self.equal_sign.rect.x + self.equal_sign.rect.width,
                                              y=0.45 * self.windows.get_height())

        self.result_label = Label(x=self.result_label_position.x,
                                  y=self.result_label_position.y,
                                  width=self.matrice1.lines[0].elements[0].width,
                                  height=self.matrice1.lines[0].elements[0].height, text="_",
                                  color=(250, 250, 250), text_color=(0, 0, 0), windows=self.windows,
                                  font_size=get_font_size(self.matrice1.nb_columns, self.matrice1.nb_lines))

        self.nbLines_entry = Entry(x=self.plus_sign.rect.x - self.plus_sign.rect.width / 4,
                                   y=0.35 * self.windows.get_height(), width=self.matrice1.width / 4,
                                   height=self.matrice1.height / 5, color=(0, 0, 0), text_color=(250, 250, 250),
                                   windows=self.windows, text=str(self.matrice1.nb_lines))
        self.nbColumns_entry = Entry(
            x=self.plus_sign.rect.x + self.plus_sign.rect.width / 4 + self.nbLines_entry.rect.width,
            y=self.nbLines_entry.rect.y, width=self.nbLines_entry.rect.width,
            height=self.nbLines_entry.rect.height, color=(0, 0, 0), text_color=(250, 250, 250),
            windows=self.windows, text=str(self.matrice2.nb_columns))

        self.components.append(self.nbLines_entry)
        self.components.append(self.nbColumns_entry)
        self.components.append(self.refresh_button)
        self.components.append(self.result_matrice)
        self.components.append(self.result_label)
        self.components.append(self.equal_sign)
        self.components.append(self.matrice1)
        self.components.append(self.matrice2)
        self.components.append(self.plus_sign)
        self.components.append(self.calculate_button)
        self.components.append(self.title)

        self.result_matrice.make_elements_drawable_false()

        self.result_label.drawable = False
        self.equal_sign.drawable = False
        self.result_matrice.drawable = False
        self.refresh_button.drawable = False

        self.matrice1.add_components_to_page(self)
        self.matrice2.add_components_to_page(self)
        self.result_matrice.add_components_to_page(self)

        self.moving_line_index = 0
        self.moving_column_index = 0

        self.calculating = False
        self.moving_back = False
        self.resulting = False
        self.refreshing = False

    def update(self):
        """
        if calculating is true, if refreshing is false then we are moving the elements to the calculating position, if refreshing is true, we are moving back the elements
        :return:
        """
        # print(self.result_matrice.lines[0].elements[0].position.x, self.result_matrice.lines[0].elements[0].position.y)
        if self.calculating is True:
            self.calculate()

        else:
            try:
                if 0 < int(self.nbLines_entry.text) < 10 and 0 < int(self.nbColumns_entry.text) < 10:
                    if int(self.nbLines_entry.text) != self.matrice1.nb_lines or int(
                            self.nbColumns_entry.text) != self.matrice1.nb_columns:
                        self.matrice1.update(new_nb_lines=int(self.nbLines_entry.text),
                                             new_nb_columns=int(self.nbColumns_entry.text), page=self)
                        self.matrice2.update(new_nb_lines=int(self.nbLines_entry.text),
                                             new_nb_columns=int(self.nbColumns_entry.text), page=self)
                        self.result_matrice.update(new_nb_lines=int(self.nbLines_entry.text),
                                                   new_nb_columns=int(self.nbColumns_entry.text), page=self,
                                                   add_components=False)
                        self.result_label.font_size = get_font_size(int(self.nbLines_entry.text),
                                                                    int(self.nbColumns_entry.text))
            except ValueError:
                pass

        self.matrice1.update_values()
        self.matrice2.update_values()

    def calculate(self):
        if not self.resulting:
            self.move_plus_sign()
            if self.is_plus_sign_in_position():
                self.sum()
        else:
            self.result()

    def move_back(self, element1, element2):
        element1.component.move_to(position=element1.position)  # move the elements to the default position
        element2.component.move_to(position=element2.position)
        if element1.component.is_in_position(element1.position) and element2.component.is_in_position(
                element2.position):  # if the elements are both back in position, we set increment the index to move the next elements, and set refreshing too false to move the new elements to the calculating positions
            self.moving_back = False
            self.increment_index()

    def calculate_and_move_result(self, element1, element2):
        self.result_label.text = str(
            element1.value + element2.value)  # here the elements are both in the calculating positions, so we calculate the sum and move the result label to the result matrice position
        result_matrice_column = self.result_matrice.lines[self.moving_line_index].elements[
            self.moving_column_index]
        self.result_label.move_to(result_matrice_column.position)
        if self.result_label.is_in_position(result_matrice_column.position):
            # here we change the component of the column to the result label
            self.result_matrice.lines[self.moving_line_index].elements[
                self.moving_column_index].component.drawable = False
            self.result_matrice.lines[self.moving_line_index].elements[
                self.moving_column_index].component = self.result_label

            self.moving_back = True
            self.result_label = Label(x=self.result_label_position.x,
                                      y=self.result_label_position.y,
                                      width=self.matrice1.lines[0].elements[0].width,
                                      height=self.matrice1.lines[0].elements[0].height, text="_",
                                      color=(250, 250, 250), text_color=(0, 0, 0),
                                      windows=self.windows,
                                      font_size=get_font_size(self.matrice1.nb_columns,
                                                              self.matrice1.nb_lines))  # here we create a new result label
            self.components.append(self.result_label)

    def sum(self):
        element1 = self.matrice1.lines[self.moving_line_index].elements[self.moving_column_index]
        element2 = self.matrice2.lines[self.moving_line_index].elements[self.moving_column_index]

        if not self.moving_back:
            element1.component.move_to(
                position=self.calculating_position1)  # move the elements to the calculating position
            element2.component.move_to(position=self.calculating_position2)
        else:
            self.move_back(element1, element2)
        if element1.component.is_in_position(self.calculating_position1) and element2.component.is_in_position(
                self.calculating_position2):
            self.calculate_and_move_result(element1, element2)

    def result(self):
        from entities.position import Position
        self.matrice1.drawable = False
        self.matrice2.drawable = False
        self.equal_sign.drawable = False
        self.plus_sign.drawable = False
        self.result_label.drawable = False

        self.matrice1.make_elements_drawable_false()
        self.matrice2.make_elements_drawable_false()

        result_matrice_target_position = Position(self.result_matrice.x,
                                                  self.windows.get_height() / 2 - self.result_matrice.height / 2)
        self.result_matrice.move_matrice_vertically(result_matrice_target_position)
        if self.result_matrice.is_in_position(result_matrice_target_position):
            self.refresh_button.drawable = True

    def increment_index(self):
        if self.moving_column_index == self.matrice1.nb_columns - 1:
            if self.moving_line_index == self.matrice1.nb_lines - 1:
                self.resulting = True
            else:
                self.moving_line_index += 1
                self.moving_column_index = 0
        else:
            self.moving_column_index += 1

    def turn_calculating_on(self):
        self.calculate_button.drawable = False

        self.result_matrice.make_elements_drawable_true()
        self.result_matrice.drawable = True
        self.result_label.drawable = True
        self.equal_sign.drawable = True

        self.nbLines_entry.drawable = False
        self.nbColumns_entry.drawable = False
        self.calculating = True

    def refresh(self):
        self.calculating = False
        self.resulting = False

        self.moving_line_index = 0
        self.moving_column_index = 0

        self.result_matrice.drawable = False
        self.result_matrice.refresh_elements()
        self.result_matrice.make_elements_drawable_false()
        self.result_matrice.change_vertical_position(self.windows.get_height() * 0.65, self)

        self.matrice1.drawable = True
        self.matrice1.refresh_elements()
        self.matrice1.make_elements_drawable_true()

        self.matrice2.drawable = True
        self.matrice2.refresh_elements()
        self.matrice2.make_elements_drawable_true()

        self.calculate_button.drawable = True
        self.nbLines_entry.drawable = True
        self.nbColumns_entry.drawable = True

        self.refresh_button.drawable = False

    def move_plus_sign(self):
        from entities.position import Position
        position = Position(x=self.plus_sign.rect.x, y=self.calculating_position1.y - self.plus_sign.rect.height * 0.3)
        self.plus_sign.move_to(position)

    def is_plus_sign_in_position(self):
        from entities.position import Position
        position = Position(x=self.plus_sign.rect.x, y=self.calculating_position1.y - self.plus_sign.rect.height * 0.3)
        if self.plus_sign.is_in_position(position):
            return True
        return False


def get_font_size(nb_columns, nb_lines):
    return int(math.sqrt(9 / (nb_columns * nb_lines)) * 24)
