from board import HexBoard
from piece import HivePiece


class Hive(object):
    """
    The Hive Game.
    This class enforces the game rules and keeps the state of the game.
    """

    def __init__(self):
        self.turn = 0
        self.players = ['w', 'b']
        self.board = HexBoard()
        self.playedPieces = {}


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
        try:
            res = self.playedPieces[str(piece)]['cell']
        except KeyError:
            pass

        return res


    def move_piece(self, piece, refPiece, refDirection):
        """
        Verifies if a piece can be played from hand into a given cell.
        """
        # the piece is on the board
        # the piece can be moved
        # the move is valid
        raise NotImplemented


    def place_piece(self, piece, refPieceName=None, refDirection=None):
        """
        Verifies if a piece can be played from hand into a given cell.
        """
        # the piece was already played
        if str(piece) in self.playedPieces:
            return False

        # if it's the first piece we put it at cell (0, 0)
        if refPieceName is None and self.turn == 1:
            cell = (0, 0)
            self.board.place(cell, str(piece))
            self.playedPieces[str(piece)] = {'piece': piece, 'cell': cell}
            return cell

        # the placement is valid
        cell = self.poc2cell(refPieceName, refDirection)
        if self._validate_place_piece(piece, cell):
            self.board.place(cell, str(piece))
            self.playedPieces[str(piece)] = {'piece': piece, 'cell': cell}

        return cell


    def _validate_move_piece(self, moving_piece, cell):
        # - check if moving this piece won't break the hive
        #   - check if the piece is touching more then one piece
        #   - check that from one of the touching pieces you can reach all other
        #     pieces that where touching the moving piece


        # - check that end position is accessible
        #   - check if the end position is free unless is a move on top
        #   - if the move is not a jump
        #     - check that the end position is in the periphery of the board
        raise NotImplemented


    def _validate_place_piece(self, piece, cell):
        """
        Verifies if a piece can be played from hand into a given cell.
        The piece must be placed touching at least one piece of the same color
        and can only be touching pieces of the same color.
        """
        # if it's the second piece we put it without validating touching colors
        if self.turn == 2:
            self.board.place(cell, str(piece))
            self.playedPieces[str(piece)] = {'piece': piece, 'cell': cell}
            return True

        playedColor = piece.color

        occupiedCells = self._occupied_surroundings(cell)
        visiblePieces = [
            self.board.get(oCell)[-1] for oCell in occupiedCells
        ]
        res = True
        for pName in visiblePieces:
            if self.playedPieces[pName]['piece'].color != playedColor:
                res = False
                break

        return res


    def one_hive(self, piece):
        """Check if removing a piece doesn't break the one hive rule."""
        originalPos = self.board.remove(str(piece))
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

        self.board.place(originalPos, str(piece))
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
            target =  surroundings[i-1]
            # is the target cell free?
            if self.board.is_cell_free(target):
                # does it have an adjacent fee cell that is also adjacent to the
                # starting cell?
                if (
                    self.board.is_cell_free(surroundings[i])
                    or self.board.is_cell_free(surroundings[i-2])
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
            if self.board.is_cell_free(cell):
                return False
            cell = self.board.get_dir_cell(cell, moveDir)

        # is the endCell free?
        if not self.board.is_cell_free(endCell):
            return False

        return True


    def _occupied_surroundings(self, cell):
        surroundings = self.board.get_surrounding(cell)
        return [c for c in surroundings if len(self.board.get(c)) > 0]


    def __repr__(self):
        return str(self.board)
