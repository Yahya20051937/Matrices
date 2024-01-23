class Position:
    def __init__(self, x, y):
        self.x = round(x)
        self.y = round(y)

    def __repr__(self):
        return f"position : {self.x}, {self.y}"
