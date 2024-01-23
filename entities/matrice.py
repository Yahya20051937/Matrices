import math

from .line import Line
from .element import Element


class Matrice:
    def __init__(self, nb_lines, nb_columns, x, y, width, height, windows, with_entries=False, value=None,
                 ):
        from components.arc import Arc
        self.lines = []

        self.nb_lines = nb_lines
        self.nb_columns = nb_columns
        self.width = width
        self.height = height
        self.x = x  # the x of the top of the first arc
        self.y = y  # the y of the top of the first arc
        self.opening_arc = Arc(x=self.x, y=self.y, height=self.height)
        self.closing_arc = Arc(x=self.x + self.width, y=self.y, height=self.height)
        self.windows = windows
        self.drawable = True
        self.create(with_entries=with_entries, value=value)

    def create(self, with_entries, value=None):
        divided_width = self.width / self.nb_columns
        divided_height = self.height / self.nb_lines

        for i in range(self.nb_lines):
            line = Line(y=self.y + divided_height * i + divided_height / 2 - (
                    divided_height * 0.8) / 2, index=i + 1)
            for j in range(self.nb_columns):
                element = Element(x=self.x + divided_width * j + divided_width / 2 - 0.8 *
                                  divided_width / 2, index=j + 1,
                                  width=0.8 * divided_width,
                                  height=divided_height * 0.8, y=line.y, windows=self.windows,
                                  with_entries=with_entries, value=value,
                                  font_size=self.get_font_size())
                line.elements.append(element)

            self.lines.append(line)

    def update_existing_elements(self, divided_width, divided_height, new_nb_columns, new_nb_lines):
        # here, we adjust the width and height, x and y of each of the elements to fit the new number of columns and lines
        i = 0
        for line in self.lines:
            line.y = self.y + divided_height * i + divided_height / 2 - (
                    divided_height * 0.8) / 2
            i += 1
            j = 0
            for element in line.elements:
                element.x = self.x + divided_width * j + divided_width / 2 - 0.8 * divided_width / 2
                element.width = 0.8 * divided_width
                element.height = 0.8 * divided_height
                element.y = line.y
                j += 1
                element.update()
                element.component.font_size = get_font_size(new_nb_columns, new_nb_lines)

    def create_new_lines(self, divided_width, divided_height, new_nb_lines, add_components, page, new_nb_columns,
                         new_elements_drawable):
        """
        in the range between the new number of lines and the existing lines, we create a new line, with existing number of columns
        :param new_nb_columns:
        :param new_elements_drawable:
        :param divided_width:
        :param divided_height:
        :param new_nb_lines:
        :param add_components:
        :param page:
        :return:
        """
        for i in range(self.nb_lines, new_nb_lines):
            line = Line(y=self.y + divided_height * i + divided_height / 2 - (
                    divided_height * 0.8) / 2, index=i + 1)
            for j in range(self.nb_columns):
                element = Element(x=self.x + divided_width * j + divided_width / 2 - 0.8 *
                                    divided_width / 2, index=j + 1,
                                  width=0.8 * divided_width,
                                  height=divided_height * 0.8, y=line.y, windows=self.windows,
                                  with_entries=True, value=None,
                                  font_size=self.get_font_size())
                element.component.drawable = new_elements_drawable
                line.elements.append(element)
                if add_components:  # this to avoid adding the components and thus drawing them in the page
                    page.components.append(element.component)

            self.lines.append(line)

    def remove_lines(self, new_nb_lines):
        for line in self.lines[
                    new_nb_lines:]:  # in the lines that we want to remove, we make their elements drawable attribute too false to stop drawing them, and then we delete the lines
            for element in line.elements:
                element.component.drawable = False
        self.lines = self.lines[:new_nb_lines]

    def remove_columns(self, new_nb_columns):
        for line in self.lines:  # here we make the element of each column in each line drawable to false, then we delete the elements
            for element in line.elements[new_nb_columns:]:
                element.component.drawable = False
            line.elements = line.elements[:new_nb_columns]

    def create_new_columns(self, divided_width, divided_height, new_nb_columns, new_nb_lines, add_components, page,
                           new_elements_drawable):
        # here we just create new elements in each line
        for line in self.lines:
            for i in range(self.nb_columns, new_nb_columns):
                element = Element(x=self.x + divided_width * i + divided_width / 2 - 0.8 *
                                    divided_width / 2, index=i + 1,
                                  width=0.8 * divided_width,
                                  height=divided_height * 0.8, y=line.y, windows=self.windows,
                                  with_entries=True, value=None,
                                  font_size=self.get_font_size())
                element.component.drawable = new_elements_drawable
                line.elements.append(element)
                if add_components:
                    page.components.append(element.component)

    def update(self, new_nb_columns, new_nb_lines, page, add_components=True, new_elements_drawable=True):
        """
        When updating the number of lines and/or columns of a matrix, we first update the existing elements, then we add or remove lines or columns
        :param new_elements_drawable:
        :param new_nb_lines:
        :param new_nb_columns:
        :param page:
        :param add_components:
        :return:
        """

        divided_width = self.width / new_nb_columns
        divided_height = self.height / new_nb_lines

        self.update_existing_elements(divided_width=divided_width, divided_height=divided_height,
                                      new_nb_columns=new_nb_columns, new_nb_lines=new_nb_lines)
        if new_nb_lines > self.nb_lines:
            self.create_new_lines(divided_width, divided_height, new_nb_lines, add_components, page, new_nb_columns,
                                  new_elements_drawable)
        else:
            self.remove_lines(new_nb_lines)

        if new_nb_columns > self.nb_columns:
            self.create_new_columns(divided_width, divided_height, new_nb_columns, new_nb_lines, add_components, page,
                                    new_elements_drawable)
        else:
            self.remove_columns(new_nb_columns)

        self.nb_lines = new_nb_lines
        self.nb_columns = new_nb_columns

        for line in self.lines:
            for element in line.elements:
                element.update()

    def update_arcs(self):
        self.opening_arc.y = self.y
        self.closing_arc.y = self.y
        self.opening_arc.get_elements()
        self.closing_arc.get_elements()

    def addLine(self, line):
        self.lines.append(line)

    def draw(self):
        if self.drawable:
            self.opening_arc.draw(self.windows)
            self.closing_arc.draw(self.windows)

    def add_components_to_page(self, page):
        for line in self.lines:
            for element in line.elements:
                page.components.append(element.component)

    def make_elements_drawable_false(self):
        for line in self.lines:
            for element in line.elements:
                element.component.drawable = False

    def make_elements_drawable_true(self):
        for line in self.lines:
            for element in line.elements:
                element.component.drawable = True

    def update_values(self):
        for line in self.lines:
            for element in line.elements:
                if element.component.text == "-":
                    element.value = -1
                elif element.component.text[-1] == "/":
                    element.value = int(element.component.text[:-1])
                elif "/" in element.component.text:
                    index = element.component.text.index("/")
                    element.value = int(element.component.text[:index]) / int(element.component.text[index + 1])
                else:
                    try:
                        element.value = int(element.component.text)
                    except ValueError:
                        pass

    def move_matrice_vertically(self, position):
        from .position import Position
        self.opening_arc.move_vertically(position)
        self.closing_arc.move_vertically(position)
        divided_height = self.height / self.nb_lines
        i = 0
        for line in self.lines:
            line.y = position.y + divided_height * i + divided_height / 2 - (
                    divided_height * 0.8) / 2
            for element in line.elements:
                element.y = line.y
                element.component.move_to(Position(x=element.x, y=line.y))
            i += 1
        self.y = position.y

    def is_in_position(self, position):
        divided_height = self.height / self.nb_lines
        if self.opening_arc.elements[0].y == position.y and self.lines[0].elements[
            0].y == position.y + divided_height / 2 - (
                divided_height * 0.8) / 2:
            return True
        return False

    def refresh_elements(self):
        for line in self.lines:
            for element in line.elements:
                element.value = None
                element.component.text = "_"

    def change_vertical_position(self, y, page):
        self.y = y
        self.update_arcs()
        self.lines = []
        self.create(with_entries=False, value=None)
        self.add_components_to_page(page)
        self.make_elements_drawable_false()

    def get_elements_width(self):
        return (self.width / self.nb_columns) * 0.8

    def get_elements_height(self):
        return (self.height / self.nb_lines) * 0.8

    def get_font_size(self):
        return int(math.sqrt(9 / (self.nb_columns * self.nb_lines)) * 24)

    def fit_component(self, component):
        component.font_size = self.get_font_size()
        component.rect.width = self.get_elements_width()
        component.rect.height = self.get_elements_height()

    def get_a_line_that_starts_with_1_other_that_first(self):
        for line in self.lines[1:]:
            if line.elements[0].value == 1:
                return line
        return None

    def does_line_1_starts_with_1(self):
        if self.lines[0].elements[0].value == 1:
            return True
        return False

    def are_elements_at_index_fixed(self, index):
        return False

    def simplify(self):
        for line in self.lines:
            line.simplify()

    



def get_font_size(nb_columns, nb_lines):
    return int(math.sqrt(9 / (nb_columns * nb_lines)) * 24)
