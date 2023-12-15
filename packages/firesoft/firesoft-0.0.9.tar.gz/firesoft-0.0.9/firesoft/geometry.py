import enum


class AlignCorner(enum.Enum):
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4

    @staticmethod
    def get_from_value(value: int):
        if value == 1:
            return AlignCorner.TOP_LEFT
        elif value == 2:
            return AlignCorner.TOP_RIGHT
        elif value == 3:
            return AlignCorner.BOTTOM_LEFT
        elif value == 4:
            return AlignCorner.BOTTOM_RIGHT
        else:
            raise Exception("Unknown AlignCorner value: {}".format(value))

    def get_opposite(self):
        if self == AlignCorner.TOP_LEFT:
            return AlignCorner.BOTTOM_RIGHT
        elif self == AlignCorner.TOP_RIGHT:
            return AlignCorner.BOTTOM_LEFT
        elif self == AlignCorner.BOTTOM_LEFT:
            return AlignCorner.TOP_RIGHT
        elif self == AlignCorner.BOTTOM_RIGHT:
            return AlignCorner.TOP_LEFT
        else:
            raise Exception("Unknown AlignCorner value: {}".format(self))


class Margin:
    def __init__(self, top: int = 0, right: int = 0, bottom: int = 0, left: int = 0):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left