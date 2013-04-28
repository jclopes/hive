from board import HexBoard
from piece import HivePiece


class HiveException(Exception):
    """Base class for exceptions."""
    pass

class Hive(object):
    """
    The Hive Game.
    This class enforces the game rules and keeps the state of the game.
    """

    # Directions
    O = HexBoard.HX_O   # origin/on-top
    W = HexBoard.HX_W   # west
    NW = HexBoard.HX_NW  # north-west
    NE = HexBoard.HX_NE  # north-east
    E = HexBoard.HX_E   # east
    SE = HexBoard.HX_SE  # south-east
    SW = HexBoard.HX_SW  # south-west

    def __init__(self):
        self.turn = 0
        self.players = ['w', 'b']
        self.board = HexBoard()
        self.playedPieces = {}
        self.piecesInCell = {}


    def get_board_boundaries(self):
        """returns the coordinates of the board limits."""
        return self.board.get_boundaries()


    def get_pieces(self, cell):
        """return the pieces that are in the cell (x, y)."""
        return self.piecesInCell.get(cell, [])


    # TODO: rename/remove this function. probably should not be exposed
    def poc2cell(self, refPiece, pointOfContact):
        """
        Translates a relative position (piece, point of contact) into
        a board cell (x, y).
        """
        refCell = self.locate(refPiece)
        return self.board.get_dir_cell(refCell, pointOfContact)


    def locate(self, piece):
        """
        Returns the cell where the piece is positioned.
        piece is a piece identifier (string)
        """
        res = None
        pp = self.playedPieces.get(str(piece))
        if pp is not None:
            res = pp['cell']

        return res


    def move_piece(self, piece, refPiece, refDirection):
        """
        Verifies if a piece can be played from hand into a given cell.
        """
        # the move is valid

        pieceName = str(piece)
        targetCell = self.poc2cell(refPiece, refDirection)
        # TODO: check if the piece was played
        # TODO: check if it's the top piece
        if not self._validate_move_piece(piece, targetCell):
            raise HiveException("Invalid Piece Movement")

        pp = self.playedPieces[pieceName]
        # remove the piece from its current location
        self.piecesInCell[pp['cell']].remove(pieceName)
        # places the piece at the target location
        self.board.resize(targetCell)
        pp['cell'] = targetCell
        pic = self.piecesInCell.setdefault(pp['cell'], [])
        pic.append(piece)

        return pp['cell']


    def place_piece(self, piece, refPieceName=None, refDirection=None):
        """
        Place a piece on the playing board.
        """

        # if it's the first piece we put it at cell (0, 0)
        if refPieceName is None and self.turn == 1:
            targetCell = (0, 0)
        else:
            targetCell = self.poc2cell(refPieceName, refDirection)

        # the placement is valid
        if not self._validate_place_piece(piece, targetCell):
            raise HiveException("Invalid Piece Placement")

        self.board.resize(targetCell)
        pic = self.piecesInCell.setdefault(targetCell, [])
        pic.append(str(piece))
        self.playedPieces[str(piece)] = {'piece': piece, 'cell': targetCell}

        return targetCell


    def _validate_move_piece(self, moving_piece, cell):
        # - check if moving this piece won't break the hive
        #   - check if the piece is touching more then one piece
        #   - check that from one of the touching pieces you can reach all other
        #     pieces that where touching the moving piece


        # - check that end position is accessible
        #   - check if the end position is free unless is a move on top
        #   - if the move is not a jump
        #     - check that the end position is in the periphery of the board
        return True


    def _validate_place_piece(self, piece, cell):
        """
        Verifies if a piece can be played from hand into a given cell.
        The piece must be placed touching at least one piece of the same color
        and can only be touching pieces of the same color.
        """

        # the piece was already played
        if str(piece) in self.playedPieces:
            return False

        # if it's the first turn we don't need to validate
        if self.turn == 1:
            # TODO: turnament rules don't allow playing Queen on first turn
            return True

        # if it's the second turn we put it without validating touching colors
        if self.turn == 2:
            return True

        playedColor = piece.color

        occupiedCells = self._occupied_surroundings(cell)
        visiblePieces = [
            self.piecesInCell[oCell][-1] for oCell in occupiedCells
        ]
        res = True
        for pName in visiblePieces:
            if self.playedPieces[pName]['piece'].color != playedColor:
                res = False
                break

        return res


    def one_hive(self, piece):
        """
        Check if removing a piece doesn't break the one hive rule.
        Returns False if the hive is broken.
        """
        originalPos = self.locate(str(piece))
        # if the piece is not in the board then moving it won't break the hive
        if originalPos is None:
            return True
        # if there is another piece in the same cell then the one hive rule
        # won't be broken
        pic = self.piecesInCell[originalPos]
        if len(pic) > 1:
            return True

        # remove the piece
        del self.piecesInCell[originalPos]

        # Get all pieces that are in contact with the removed one and try to
        # reach all of them from one of them.
        occupied = self._occupied_surroundings(originalPos)
        visited = set()
        toExplore = set([occupied[0]])
        toReach = set(occupied[1:])
        res = False

        while len(toExplore) > 0:
            found = []
            for cell in toExplore:
                found += self._occupied_surroundings(cell)
                visited.add(cell)
            toExplore = set(found) - visited
            if toReach.issubset(visited):
                res = True
                break

        # restore the removed piece
        self.piecesInCell[originalPos] = pic
        return res


    def bee_moves(self, cell):
        """
        Get possible bee_moves from cell.

        A bee can move to a adjacent target position only if:
        - target position is free
        - and there is a piece adjacent to that position
        - and there is a free cell that is adjacent to both the bee and the
          target position.
        """
        available_moves = []
        surroundings = self.board.get_surrounding(cell)
        for i in range(6):
            target = surroundings[i-1]
            # is the target cell free?
            if self._is_cell_free(target):
                # does it have an adjacent fee cell that is also adjacent to the
                # starting cell?
                if (
                    self._is_cell_free(surroundings[i])
                    or self._is_cell_free(surroundings[i-2])
                ):
                    # does it have an adjacent occupied cell other then the
                    # starting cell?
                    if len(self._occupied_surroundings(target)) > 1:
                        available_moves.append(surroundings[i-1])

        return available_moves


    def valid_grasshopper_move(self, startingCell, endCell):
        # TODO: add function to HexBoard that find cells in a straight line

        # is the move in only one direction?
        (sx, sy) = startingCell
        (ex, ey) = endCell
        dx = ex - sx
        dy = ey - sy
        p = sy % 2  # starting from an even or odd line?

        moveDir = None
        # horizontal jump
        if dy == 0:
            # must jump atleast over one piece
            if abs(dx) <= 1:
                return False

            # moving west
            if dx < 0:
                moveDir = 1  # w
            # moving east
            else:
                moveDir = 4  # e

        # diagonal jump (dy != 0)
        else:
            # must jump atleast over one piece
            if abs(dy) == 1:
                return False

            # must move in a diagonal with slope = 2
            nx = (dy + p) / 2
            if abs(dx) != abs(nx):
                return False

            if dx < 0:
                if dy < 0:
                    moveDir = 2  # nw
                else:
                    moveDir = 6  # sw
            else:
                if dy < 0:
                    moveDir = 3  # ne
                else:
                    moveDir = 5  # se

        # are all in-between cells occupied?
        cell = self.board.get_dir_cell(startingCell, moveDir)
        while cell != endCell:
            if self._is_cell_free(cell):
                return False
            cell = self.board.get_dir_cell(cell, moveDir)

        # is the endCell free?
        if not self._is_cell_free(endCell):
            return False

        return True


    def _is_cell_free(self, cell):
        res = True
        if cell in self.piecesInCell:
            res = len(self.piecesInCell) == 0
        return res


    def _occupied_surroundings(self, cell):
        surroundings = self.board.get_surrounding(cell)
        return [c for c in surroundings if not self._is_cell_free(c)]


    def __repr__(self):
        return str(self.board)
