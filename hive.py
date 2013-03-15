from board import HexBoard

class Hive(object):
    """
    The Hive Game.
    This class enforces the game rules and keeps the state of the game.
    """

    def __init__(self):
        self.turn = 0
        self.players = ['w', 'b']
        self.board = HexBoard()

    def vlidate_move(self, moving_piece, ref_pieace, ref_position):
        # - check if moving this pieace won't break the hive
        #   - check if the piece is touching more then one piece
        #   - check that from one of the touching pieces you can reach all other
        #     pieces that where touching the moving piece


        # - check that end position is accessible
        #   - check if the end position is free unless is a move on top
        #   - if the move is not a jump
        #     - check that the end position is in the periphery of the board
        pass

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
