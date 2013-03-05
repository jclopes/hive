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
    All positions of the board are initialized with "[]" value.
    """
    def __init__(self):
        # the board starts with one row and a column without pieces
        self.board = [[[]]]
        self.ref0x = 0
        self.ref0y = 0
        self.pieceIndex = {}


    def _add_row(self, before=False):
        newRow = []
        rowSize = len(self.board[0])
        for i in range(rowSize):
            newRow.append([])
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
                row.append([])
            else:
                row.insert(0, [])


    def place(self, (x, y), piece):
        "Place a piece in the board position (x, y)"
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

        self.board[yy][xx].append(piece)
        self.pieceIndex[piece] = (x, y)


    def locate(self, piece):
        return self.pieceIndex[piece]


    def remove(self, piece):
        (x, y) = self.pieceIndex.pop(piece)
        cell = self.get((x, y))
        cell.remove(piece)
        return (x, y)


    def get(self, (x, y)):
        xx = self.ref0x + x
        yy = self.ref0y + y
        res = []
        try:
            res = self.board[yy][xx]
        except IndexError, e:
            # TODO: add logging
            pass

        return res


    def get_surrounding(self, (x, y)):
        """
        returns a list with the surrounding positions
        """
        return [(x-1, y), (x+1, y), (x, y-1), (x,y+1)]


class HexBoard(Board):
    """Hexagonal Tile Board"""
    def __init__(self):
        super(HexBoard, self).__init__()


    def get_surrounding(self, (x, y)):
        """
        returns a list with the surrounding positions
        """
        res = super(HexBoard, self).get_surrounding((x, y))
        p = y % 2
        if p == 0:
            res.extend([(x-1, y-1), (x-1, y+1)])
        else:
            res.extend([(x+1, y-1), (x+1, y+1)])
        return res


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
        firstCol = -self.ref0x
        firstRow = -self.ref0y
        numCols = len(self.board[0]) + firstCol
        numRows = len(self.board) + firstRow
        for i in range(firstRow, numRows):
            p = i % 2
            if i > firstRow and p == 1:
                res += " \\"
            else:
                res += "  " * p
            for j in range(firstCol, numCols):
                res += " / \\"
            if i > firstRow and p == 0:
                res += " /"
            res += "\n"
            res += "  " * p
            for j in range(firstCol, numCols):
                value = self.get((j, i))
                if len(value) != 0:
                    value = value[0][:3]
                else:
                    value = "   "
                res += "|" + value
            res += "|\n"
        p = (numRows - 1) % 2
        res += "  " * p
        for j in range(firstCol, numCols):
            res += " \\ /"
        res += "\n"

        return res


class Piece(object):
    """Representation of Playing Piece"""
    def __init__(self, color, kind, number):
        super(Cell, self).__init__()
        self.color = color
        self.kind = kind
        self.number = number

