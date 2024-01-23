class ScalarOperation:
    def __init__(self, line, scalar, page):
        from components.label import Label
        from .calculating_chain import ScalarCalculatingChain
        self.line = line
        self.scalar = scalar
        self.finished = False
        self.label = Label(x=page.windows.get_width() * 0.8, y=page.windows.get_height() * 0.2,
                           text=f"{self.scalar}*L{self.line.index}", color=(250, 250, 250),
                           text_color=(0, 0, 0), windows=page.windows, width=page.windows.get_width() * 0.15,
                           height=page.windows.get_height() * 0.15)
        page.components.append(self.label)
        self.calculating_chain = ScalarCalculatingChain(page=page, scalar=self.scalar)
        page.components.append(self.calculating_chain)
        self.current_index = 0

        self.working = True
        self.moving_back = False

    def do(self):
        if self.working:
            if not self.moving_back:
                self.move_element()
                if self.element_in_position():
                    self.calculate_result()
                    self.moving_back = True
            else:
                self.move_result()

    def move_element(self):
        element = self.line.elements[self.current_index]
        element.component.move_to(position=self.calculating_chain.calculating_position)

    def element_in_position(self):
        element = self.line.elements[self.current_index]
        return element.component.is_in_position(position=self.calculating_chain.calculating_position)

    def calculate_result(self):
        element = self.line.elements[self.current_index]
        self.calculating_chain.value = element.value
        self.calculating_chain.calculate()

    def move_result(self):
        element = self.line.elements[self.current_index]
        self.calculating_chain.result_label.move_to(element.position)


class SwitchOperation:
    def __init__(self, line1, line2, page):
        from components.label import Label
        self.line1 = line1
        self.line2 = line2
        self.label = Label(x=page.windows.get_width() * 0.8, y=page.windows.get_height() * 0.2,
                           text=f"L{self.line1.index}<=>L{self.line2.index}", color=(250, 250, 250),
                           text_color=(0, 0, 0), windows=page.windows, width=page.windows.get_width() * 0.15,
                           height=page.windows.get_height() * 0.15)
        self.label.drawable = False
        self.page = page
        self.page.components.append(self.label)
        self.finished = False

    def do(self):
        self.label.drawable = True
        for i in range(len(self.line1.elements)):
            element1 = self.line1.elements[i]
            element2 = self.line2.elements[i]
            if element1.component.is_in_position(element2.position) and element2.component.is_in_position(
                    element1.position):
                self.label.drawable = False
                self.finished = True
                self.page.matrice.lines[self.line1.index - 1], self.page.matrice.lines[self.line2.index - 1] = \
                    self.page.matrice.lines[self.line2.index - 1], self.page.matrice.lines[self.line1.index - 1]
                self.line1.index, self.line2.index = self.line2.index, self.line1.index

                element1.update_coordinates()
                element2.update_coordinates()
            else:
                element1.component.move_to(element2.position)
                element2.component.move_to(element1.position)


class ReplaceOperation:
    def __init__(self, switching_line, reference_line, scalar, page):
        from components.label import Label
        from .calculating_chain import ReplaceCalculatingChain
        from .position import Position
        self.switching_line = switching_line  # Line
        self.reference_line = reference_line  # Line
        self.scalar = scalar  # int
        self.label = Label(x=page.windows.get_width() * 0.8, y=page.windows.get_height() * 0.2,
                           text=self.get_text(),
                           color=(250, 250, 250),
                           text_color=(0, 0, 0), windows=page.windows, width=page.windows.get_width() * 0.15,
                           height=page.windows.get_height() * 0.15)
        self.finished = False
        page.components.append(self.label)
        self.label.drawable = True
        self.page = page
        self.current_moving_element = 0

        self.calculating_chain = ReplaceCalculatingChain(page=self.page, scalar=self.scalar)
        self.page.components.append(self.calculating_chain)

        self.working = True
        self.moving_back = False

    def get_text(self):
        if self.scalar < 0:
            return f"L{self.switching_line.index}=>L{self.switching_line.index} - {-self.scalar} * L{self.reference_line.index}"
        else:
            return f"L{self.switching_line.index}=>L{self.switching_line.index} + {self.scalar} * L{self.reference_line.index}"

    def get_elements(self):
        switching_element = self.switching_line.elements[self.current_moving_element]
        reference_element = self.reference_line.elements[self.current_moving_element]
        return switching_element, reference_element

    def do(self):
        if self.working:
            if not self.moving_back:
                self.move_elements_to_position()
                if self.elements_are_in_position():
                    self.calculate_result()
                    self.moving_back = True
            else:
                self.move_result_label_and_reference_element()
                if self.result_label_and_reference_element_in_position():
                    self.update_matrice()
                    self.increment_index()

    def move_elements_to_position(self):
        switching_element, reference_element = self.get_elements()
        switching_element.component.move_to(self.calculating_chain.calculating_position1)
        reference_element.component.move_to(self.calculating_chain.calculating_position2)

    def elements_are_in_position(self):
        switching_element, reference_element = self.get_elements()
        if switching_element.component.is_in_position(
                self.calculating_chain.calculating_position1) and reference_element.component.is_in_position(
            self.calculating_chain.calculating_position2):
            return True
        return False

    def calculate_result(self):
        switching_element, reference_element = self.get_elements()
        self.calculating_chain.value1 = switching_element.value
        self.calculating_chain.value2 = reference_element.value
        self.calculating_chain.calculate()

    def move_result_label_and_reference_element(self):
        switching_element, reference_element = self.get_elements()
        reference_element.component.move_to(reference_element.position)
        self.calculating_chain.result_label.move_to(switching_element.position)

    def result_label_and_reference_element_in_position(self):
        switching_element, reference_element = self.get_elements()
        if self.calculating_chain.result_label.is_in_position(
                switching_element.position) and reference_element.component.is_in_position(reference_element.position):
            return True
        return False

    def terminate(self):
        self.working = False
        self.label.drawable = False
        self.calculating_chain.drawable = False
        self.label.drawable = False
        self.finished = True

    def update_matrice(self):
        switching_element, reference_element = self.get_elements()
        switching_element.component.drawable = False
        switching_element.component = self.calculating_chain.result_label
        self.page.components.append(self.calculating_chain.result_label)
        self.page.matrice.update_values()

    def increment_index(self):
        if self.current_moving_element == self.page.matrice.nb_columns - 1:
            self.terminate()
        else:
            self.current_moving_element += 1
            self.moving_back = False
            self.calculating_chain.update_result_label()
