class Line:
    def __init__(self, y, index):
        self.index = index
        self.y = y
        self.elements = []

    def get_number_of_starting_null_elements(self):
        n = 0
        for element in self.elements:
            if element.value == 0:
                n += 1
            else:
                return n

    def get_elements_indexes_to_nullify_for_el_matrix(self):
        indexes = []
        index = 0
        for element in self.elements[:self.index]:
            if element.value != 0:
                indexes.append(index)
            index += 1

    def find_divider(self):
        smallest_value = min([e.value for e in self.elements])
        if smallest_value == 1 or smallest_value == 0:
            return None
        for element in self.elements:
            if element.value % smallest_value != 0:
                return None
        return smallest_value


