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
        #   - check if the pice is touching more then one pice
        #   - check that from one of the touching pices you can reach all other
        #     pices that where touching the moving piece


        # - check that end position is accessible
        #   - check if the end position is free unless is a move on top
        #   - if the move is not a jump
        #     - check that the end position is in the periphery of the board


    def one_hive(self, piece):
        """Check if removing a piece doesn't break the one hive rule."""
        originalPos = self.board.remove(piece)
        occupied = self.occupied_surroundings(originalPos)
        visited = set()
        toExplore = set([occupied[0]])
        toReach = set(occupied[1:])
        res = False

        while len(toExplore) > 0:
            found = []
            for cell in toExplore:
                found += self.occupied_surroundings(cell)
                visited.add(cell)
            toExplore = set(found) - visited
            if toReach.issubset(visited):
                res = True
                break

        self.board.place(originalPos, piece)
        return res


    def occupied_surroundings(self, cell):
        surroundings = self.board.get_surrounding(cell)
        return [c for c in surroundings if len(self.board.get(c)) > 0]
