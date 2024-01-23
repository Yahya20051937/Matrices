from .page import Page
from components.label import Label


class ElPage(Page):
    DEFAULT_NB_LINES_COLUMNS = 3

    def __init__(self, windows):
        from entities.matrice import Matrice
        from components.entry import Entry
        from entities.position import Position
        from components.button import Button
        super().__init__(windows)
        self.title = Label(x=windows.get_width() / 2 - windows.get_width() * 0.5 / 2, y=windows.get_height() * 0.05,
                           width=windows.get_width() * 0.5,
                           height=windows.get_height() * 0.1, color=(250, 250, 250), text="EL", windows=windows,
                           text_color=(0, 0, 0))
        self.components.append(self.title)
        divided_width = self.windows.get_width() / 2
        divided_divided_width = divided_width / 2
        divided_divided_divided_width = divided_divided_width / 2

        self.matrice = Matrice(nb_lines=ElPage.DEFAULT_NB_LINES_COLUMNS, nb_columns=ElPage.DEFAULT_NB_LINES_COLUMNS,
                               x=divided_divided_width - divided_divided_divided_width,
                               y=0.1 * windows.get_height(), width=divided_divided_width,
                               height=windows.get_height() * 0.3, windows=self.windows, with_entries=True,
                               value="test")
        self.nb_lines_columns_entry = Entry(x=self.matrice.x + self.matrice.width * 0.5 - self.matrice.width / 8,
                                            y=self.windows.get_height() * 0.45,
                                            width=self.matrice.width / 4, height=self.matrice.height / 5,
                                            color=(0, 0, 0),
                                            text_color=(250, 250, 250), windows=self.windows, _max=6,
                                            text=str(ElPage.DEFAULT_NB_LINES_COLUMNS))
        self.start_button = Button(x=divided_width - self.matrice.width / 4, y=self.windows.get_height() * 0.8,
                                   width=self.matrice.width / 2, height=self.matrice.height / 3, text="start",
                                   color=(0, 0, 0), text_color=(250, 250, 250), func=self.start,
                                   page=self, windows=self.windows)

        self.components.append(self.matrice)
        self.components.append(self.nb_lines_columns_entry)
        self.components.append(self.start_button)

        self.matrice.add_components_to_page(page=self)

        self.working = False

        self.current_operation = None
        self.current_fixing_index = 0

    def start(self):
        self.working = True

    def work(self):  # for now, we assume that the matrix is not el
        from entities.operation import SwitchOperation, ReplaceOperation, ScalarOperation
        if self.current_operation is None:
            """for line in self.matrice.lines:
                divider = line.find_divider()
                if divider is not None:
                    self.current_operation = ScalarOperation(line=line, scalar=1 / divider)
                    return"""

            if not self.matrice.does_line_1_starts_with_1():
                other_line_that_start_with_one = self.matrice.get_a_line_that_starts_with_1_other_that_first()
                if other_line_that_start_with_one is not None:
                    self.current_operation = SwitchOperation(line1=self.matrice.lines[0],
                                                             line2=other_line_that_start_with_one, page=self)
            else:
                for line in self.matrice.lines[self.current_fixing_index + 1:]:
                    element_at_current_index = line.elements[self.current_fixing_index]
                    if element_at_current_index.value != 0:
                        self.current_operation = ReplaceOperation(switching_line=line,
                                                                  reference_line=self.matrice.lines[0],
                                                                  scalar=element_at_current_index.value * -1, page=self)
                        break
        else:
            self.current_operation.do()
            if self.current_operation.finished:
                self.current_operation = None

    def update(self):
        if not self.working:
            try:
                self.matrice.update(new_nb_lines=int(self.nb_lines_columns_entry.text),
                                    new_nb_columns=int(self.nb_lines_columns_entry.text), page=self)
            except ValueError:
                pass
            finally:
                self.matrice.update_values()
        else:
            self.work()
