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


    def move_piece(self, piece, cell):
        """
        Verifies if a piece can be played from hand into a given cell.
        """
        raise NotImplemented


    def place_piece(self, piece, cell):
        """
        Verifies if a piece can be played from hand into a given cell.
        """
        raise NotImplemented


    def validate_move_piece(self, moving_piece, ref_piece, ref_position):
        # - check if moving this piece won't break the hive
        #   - check if the piece is touching more then one piece
        #   - check that from one of the touching pieces you can reach all other
        #     pieces that where touching the moving piece


        # - check that end position is accessible
        #   - check if the end position is free unless is a move on top
        #   - if the move is not a jump
        #     - check that the end position is in the periphery of the board
        raise NotImplemented


    def validate_place_piece(self, piece, cell):
        """
        Verifies if a piece can be played from hand into a given cell.
        The piece must be placed touching at least one piece of the same color
        and can only be touching pieces of the same color.
        """
        playedColor = piece.color
        occupiedCells = self._occupied_surroundings(cell)
        visiblePiecesColor = [pieces[-1].color for pieces in occupied]
        res = True
        for c in visiblePiecesColor:
            if c != playedColor:
                res = False
                break

        return res


    def one_hive(self, piece):
        """Check if removing a piece doesn't break the one hive rule."""
        originalPos = self.board.remove(piece)
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

        self.board.place(originalPos, piece)
        return res


    def bee_moves(self, cell):
        """
        Get possible bee_moves.

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


    def _occupied_surroundings(self, cell):
        surroundings = self.board.get_surrounding(cell)
        return [c for c in surroundings if len(self.board.get(c)) > 0]


    def __repr__(self):
        return str(self.board)
