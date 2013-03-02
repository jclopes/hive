# board.py
# classes that represent the game rules

# Board layout:
#
#  / \ / \ / \ / \
# |0,0|1,0|2,0|3,0|
#  \ / \ / \ / \ / \
#   |0,1|1,1|2,1|3,1|
#  / \ / \ / \ / \ /
# |0,2|1,2|2,2|3,2|
#  \ / \ / \ / \ / \
#   |0,3|1,3|2,3|3,3|
#    \ / \ / \ / \ /


class Board(object):
    """
    Representation of the virtual playing Board.
    Dynamic board that will extend to the required size when values are set.
    All positions of the board are initialized with "None" value.
    """
    def __init__(self):
        # the board starts with one row and a column without pices
        self.board = [[None]]
        self.ref0x = 0
        self.ref0y = 0


    def _add_row(self, before=False):
        newRow = []
        rowSize = len(self.board[0])
        for i in range(rowSize):
            newRow.append(None)
        if not before:
            self.board.append(newRow)
        else:
            self.ref0y += 1
            self.board.insert(0, newRow)


    def _add_column(self, before=False):
        if before:
            self.ref0x += 1
        for row in self.board:
            if not before:
                row.append(None)
            else:
                row.insert(0, None)


    def set(self, x, y, value):
        xx = self.ref0x+x
        yy = self.ref0y+y

        while xx < 0:
            self._add_column(before=True)
            xx += 1
        while xx >= len(self.board[0]):
            self._add_column()
        while yy < 0:
            self._add_row(before=True)
            yy += 1
        while yy >= len(self.board):
            self._add_row()

        self.board[yy][xx] = value


    def get(self, x, y):
        xx = self.ref0x+x
        yy = self.ref0y+y
        res = None
        try:
            res = self.board[yy][xx]
        except IndexError, e:
            # TODO: add logging
            pass

        return res


class HexBoard(Board):
    """Hexagonal Tile Board"""
    def __init__(self):
        super(HexBoard, self).__init__()


    def get_ul_xy(self, x, y):
        """
        Get X;Y coordinates for the uper-left Cell
        """
        p = y % 2
        nx = x - 1 + p
        ny = y - 1
        return (nx, ny)


    def get_ur_xy(self, x, y):
        """
        Get X;Y coordinates for the uper-right Cell
        """
        p = y % 2
        nx = x + p
        ny = y - 1
        return (nx, ny)


    def get_ll_xy(self, x, y):
        """
        Get X;Y coordinates for the lower-left Cell
        """
        p = y % 2
        nx = x - 1 + p
        ny = y + 1
        return (nx, ny)


    def get_lr_xy(self, x, y):
        """
        Get X;Y coordinates for the lower-right Cell
        """
        p = y % 2
        nx = x + p
        ny = y + 1
        return (nx, ny)


    def get_l_xy(self, x, y):
        """
        Get X;Y coordinates for the left Cell
        """
        return (x-1, y)


    def get_r_xy(self, x, y):
        """
        Get X;Y coordinates for the right Cell
        """
        return (x+1, y)


    def __repr__(self):
        res = ""
        num_columns = len(self.board[0])
        num_rows = len(self.board)
        for i in range(num_rows):
            p = i % 2
            res += " \\" * p
            for j in range(num_columns):
                res += " / \\"
            res += "\n"
            res += "  " * p
            for j in range(num_columns):
                res += "|   "
            res += "|\n"
        p = (num_rows - 1) % 2
        res += "  " * p
        for j in range(num_columns):
            res += " \\ /"
        res += "\n"

        return res


class Pice(object):
    """Representation of Playing Pice"""
    def __init__(self, color, kind, number):
        super(Cell, self).__init__()
        self.color = color
        self.kind = kind
        self.number = number

