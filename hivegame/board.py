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
# 0 => o (origin/on-top)
# 1 => w (west)
# 2 => nw (north-west)
# 3 => ne (north-east)
# 4 => e (east)
# 5 => se (south-east)
# 6 => sw (south-west)

# A 'cell' is a coordinate representation of a board position (x, y)


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


    def get_boundaries(self):
        """returns the coordinates of the board limits."""
        firstCol = -self.ref0x
        firstRow = -self.ref0y
        lastCol = len(self.board[0]) + firstCol - 1
        lastRow = len(self.board) + firstRow - 1
        return firstCol, firstRow, lastCol, lastRow


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

    # Directions
    HX_O = 0   # origin/on-top
    HX_W = 1   # west
    HX_NW = 2  # north-west
    HX_NE = 3  # north-east
    HX_E = 4   # east
    HX_SE = 5  # south-east
    HX_SW = 6  # south-west


    def __init__(self):
        super(HexBoard, self).__init__()
        self.dir2func = {
            0: lambda x: x,
            1: self.get_w_xy,
            2: self.get_nw_xy,
            3: self.get_ne_xy,
            4: self.get_e_xy,
            5: self.get_se_xy,
            6: self.get_sw_xy
        }


    def get_surrounding(self, (x, y)):
        """
        Returns a list with the surrounding positions sorted clockwise starting
        from the left
        """
        res = super(HexBoard, self).get_surrounding((x, y))
        # if in a even row we insert NW into position 1 and SW into position 5
        p = y % 2
        if p == 0:
            res.insert(1, (x-1, y-1))
            res.insert(5, (x-1, y+1))
        # if in a odd row we insert NE into position 2 and SE into position 4
        else:
            res.insert(2, (x+1, y-1))
            res.insert(4, (x+1, y+1))
        return res


    def get_dir_cell(self, cell, direction):
        """
        Translates a relative position (cell, direction) to the referred
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
        return self.dir2func[direction](cell)


    def get_nw_xy(self, (x, y)):
        """
        Get X;Y coordinates for the upper-left Cell
        """
        p = y % 2
        nx = x - 1 + p
        ny = y - 1
        return (nx, ny)


    def get_ne_xy(self, (x, y)):
        """
        Get X;Y coordinates for the upper-right Cell
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


    def get_line_dir(self, cell0, cell1):
        """
        Returns the direction to take to go from cell0 to cell1 or None if it's
        not possible to go in a straight line.
        """

        (sx, sy) = cell0
        (ex, ey) = cell1
        dx = ex - sx
        dy = ey - sy
        p = sy % 2  # starting from an even or odd line?

        # is the same cell
        if dx == dy == 0:
            return self.HX_O

        moveDir = None
        # horizontal jump
        if dy == 0:
            # moving west
            if dx < 0:
                moveDir = self.HX_W
            # moving east
            else:
                moveDir = self.HX_E

        # diagonal jump (dy != 0)
        else:
            # must move in a diagonal with slope = 2
            nx = (abs(dy) + (1 - p)) / 2
            if abs(dx) != abs(nx):
                return None

            if dx < 0:
                if dy < 0:
                    moveDir = self.HX_NW
                else:
                    moveDir = self.HX_SW
            else:
                if dy < 0:
                    moveDir = self.HX_NE
                else:
                    moveDir = self.HX_SE

        return moveDir
