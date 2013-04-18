# board.py
# classes that represent generic boards

# Board layout:
#
#  --- --- ---
# |0,0|1,0|2,0|
#  --- --- ---
# |0,1|1,1|2,1|
#  --- --- ---
# |0,2|1,2|2,2|
#  --- --- ---

# HexBoard layout:
#
#  / \ / \ / \ / \ / \
# |0,0|1,0|2,0|3,0|4,0|
#  \ / \ / \ / \ / \ / \
#   |0,1|1,1|2,1|3,1|4,1|
#  / \ / \ / \ / \ / \ /
# |0,2|1,2|2,2|3,2|4,2|
#  \ / \ / \ / \ / \ / \
#   |0,3|1,3|2,3|3,3|4,3|
#  / \ / \ / \ / \ / \ /
# |0,4|1,4|2,4|3,4|4,4|
#  \ / \ / \ / \ / \ /
#
# Point of Contact / Direction:
#
#    2/ \3
#   1|   |4
#    6\ /5
#
# 1 => w (west)
# 2 => nw (north-west)
# 3 => ne (north-east)
# 4 => e (east)
# 5 => se (south-east)
# 6 => sw (south-west)
# 7 => o (origin/on-top)

# A 'cell' is a coordinate representation of a board position (x, y)
# A 'piece' is an unique identifier of a playing piece (string)


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


    def place(self, cell, piece):
        """
        Extends the board to contain the target cell and stores the piece in
        that cell.
        """
        (xx, yy) = self.resize()
        self.board[yy][xx].append(piece)
        self.pieceIndex[piece] = (x, y)


    def remove(self, piece):
        cell = self.pieceIndex.pop(piece)
        cellPieces = self.get(cell)
        cellPieces.remove(piece)
        return cell


    def resize(self, (x, y)):
        """
        Resizes the board to include the position (x, y)
        returns the normalized (x, y)
        """
        xx = self.ref0x + x
        yy = self.ref0y + y

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
        return (xx, yy)


    def get(self, (x, y)):
        """
        Returns pieces contained in the cell (x,y) in the same order as they
        were placed into the cell.
        """

        xx = self.ref0x + x
        yy = self.ref0y + y

        if xx < 0 or yy < 0:
            return []

        res = []
        try:
            res = self.board[yy][xx]
        except IndexError, e:
            # TODO: add logging
            pass

        return res


    def is_cell_free(self, cell):
        return self.get(cell) == []


    def get_surrounding(self, (x, y)):
        """
        Returns a list with the surrounding positions sorted clockwise starting
        from the left
        """
        return [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]


    def get_w_xy(self, (x, y)):
        """
        Get X;Y coordinates for the west/left Cell
        """
        return (x-1, y)


    def get_e_xy(self, (x, y)):
        """
        Get X;Y coordinates for the east/right Cell
        """
        return (x+1, y)


class HexBoard(Board):
    """Hexagonal Tile Board"""

    def __init__(self):
        super(HexBoard, self).__init__()


    def get_surrounding(self, (x, y)):
        """
        Returns a list with the surrounding positions sorted clockwise starting
        from the left
        """
        res = super(HexBoard, self).get_surrounding((x, y))
        p = y % 2
        if p == 0:
            res.insert(1, (x-1, y-1))
            res.insert(5, (x-1, y+1))
        else:
            res.insert(2, (x+1, y-1))
            res.insert(4, (x+1, y+1))
        return res


    def get_dir_cell(self, cell, direction):
        """
        Translates a relative position (cell, direction) to the refered
        cell (x, y).

        direction in [0, 1, 2, 3, 4, 5, 6] and translates to:
        0 => o (origin/on-top)
        1 => w (west)
        2 => nw (north-west)
        3 => ne (north-east)
        4 => e (east)
        5 => se (south-east)
        6 => sw (south-west)
        """
        dir2func = {
            0: lambda x: x,
            1: self.get_w_xy,
            2: self.get_nw_xy,
            3: self.get_ne_xy,
            4: self.get_e_xy,
            5: self.get_se_xy,
            6: self.get_sw_xy
        }
        return dir2func[direction](cell)


    def get_nw_xy(self, (x, y)):
        """
        Get X;Y coordinates for the uper-left Cell
        """
        p = y % 2
        nx = x - 1 + p
        ny = y - 1
        return (nx, ny)


    def get_ne_xy(self, (x, y)):
        """
        Get X;Y coordinates for the uper-right Cell
        """
        p = y % 2
        nx = x + p
        ny = y - 1
        return (nx, ny)


    def get_sw_xy(self, (x, y)):
        """
        Get X;Y coordinates for the lower-left Cell
        """
        p = y % 2
        nx = x - 1 + p
        ny = y + 1
        return (nx, ny)


    def get_se_xy(self, (x, y)):
        """
        Get X;Y coordinates for the lower-right Cell
        """
        p = y % 2
        nx = x + p
        ny = y + 1
        return (nx, ny)


    def get_w_xy(self, (x, y)):
        """
        Get X;Y coordinates for the left Cell
        """
        return (x-1, y)


    def get_e_xy(self, (x, y)):
        """
        Get X;Y coordinates for the right Cell
        """
        return (x+1, y)


    def __repr__(self):
        res = "\n"
        firstCol = -self.ref0x
        firstRow = -self.ref0y
        lastCol = len(self.board[0]) + firstCol
        lastRow = len(self.board) + firstRow
        for i in range(firstRow, lastRow):
            p = i % 2
            # Top of the cells is also the bottom of the cells
            # for the previous row.
            if i > firstRow:
                res += " \\" * p
            else:
                res += "  " * p
            for j in range(firstCol, lastCol):
                res += " / \\"
            if i > firstRow and p == 0:
                res += " /"
            res += "\n"
            # Center of the cells
            res += "  " * p
            for j in range(firstCol, lastCol):
                pieces = self.get((j, i))
                if len(pieces) != 0:
                    pieceName = pieces[-1][:3]
                else:
                    pieceName = "   "
                res += "|" + pieceName
            res += "|\n"
        p = (lastRow - 1) % 2
        res += "  " * p
        for j in range(firstCol, lastCol):
            res += " \\ /"
        res += "\n"

        return res
