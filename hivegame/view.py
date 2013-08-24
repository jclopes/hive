class HiveView(object):
    """Visual representation of the Hive game state."""

    def __init__(self, game):
        """game is an instance of the Hive class."""
        self.game = game


    def __repr__(self):
        """text representation of the board + pieces."""
        firstCol, firstRow, lastCol, lastRow = self.game.get_board_boundaries()
        res = "\n"
        for i in range(firstRow, lastRow + 1):
            p = i % 2
            # Top of the cells is also the bottom of the cells
            # for the previous row.
            if i > firstRow:
                res += " \\" * p
            else:
                res += "  " * p
            for j in range(firstCol, lastCol + 1):
                res += " / \\"
            if i > firstRow and p == 0:
                res += " /"
            res += "\n"
            # Center of the cells
            res += "  " * p
            for j in range(firstCol, lastCol + 1):
                pieces = self.game.get_pieces((j, i))
                if len(pieces) != 0:
                    pieceName = str(pieces[-1])[:3]
                else:
                    pieceName = "   "
                res += "|" + pieceName
            res += "|\n"
        p = (lastRow) % 2
        res += "  " * p
        for j in range(firstCol, lastCol + 1):
            res += " \\ /"
        res += "\n"

        return res
