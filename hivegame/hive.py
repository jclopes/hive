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
    O = HexBoard.HX_O    # origin/on-top
    W = HexBoard.HX_W    # west
    NW = HexBoard.HX_NW  # north-west
    NE = HexBoard.HX_NE  # north-east
    E = HexBoard.HX_E    # east
    SE = HexBoard.HX_SE  # south-east
    SW = HexBoard.HX_SW  # south-west

    # End game status
    UNFINISHED = 0
    WHITE_WIN = 1
    BLACK_WIN = 2
    DRAW = 3


    def __init__(self):
        self.turn = 0
        self.players = ['w', 'b']
        self.board = HexBoard()
        self.playedPieces = {}
        self.piecesInCell = {}
        self.unplayedPieces = {}

    def setup(self):
        """
        Prepare the game to be played
        """
        # Add pieces to the players hands
        self.unplayedPieces['w'] = self._piece_set('w')
        self.unplayedPieces['b'] = self._piece_set('b')
        self.turn = 1


    def action(self, actPiece, refPiece=None, direction=None):
        """Perform the player action.
        return True or ExceptionType
        TODO: elaborate on the exceptions
        """
        player = self.get_active_player()

        piece = self.unplayedPieces[player].get(actPiece, None)
        if piece is not None:
            self.place_piece(piece, refPiece, direction)
            # Remove piece from the unplayed set
            del self.unplayedPieces[player][actPiece]
        else:
            ppiece = self.playedPieces.get(actPiece, None)
            if ppiece is None:
                raise HiveException
            else:
                self.move_piece(ppiece['piece'], refPiece, direction)

        # perform turn increment - TODO:if succesful
        self.turn += 1
        return True

    def get_unplayed_pieces(self, player):
        return self.unplayedPieces[player]


    def get_active_player(self):
        if self.turn <= 0:
            return None

        ap = 1 - (self.turn % 2)
        return self.players[ap]

    def get_board_boundaries(self):
        """returns the coordinates of the board limits."""
        return self.board.get_boundaries()


    def get_pieces(self, cell):
        """return the pieces that are in the cell (x, y)."""
        return self.piecesInCell.get(cell, [])


    def locate(self, pieceName):
        """
        Returns the cell where the piece is positioned.
        pieceName is a piece identifier (string)
        """
        res = None
        pp = self.playedPieces.get(pieceName)
        if pp is not None:
            res = pp['cell']

        return res


    def move_piece(self, piece, refPiece, refDirection):
        """
        Moves a piece on the playing board.
        """

        pieceName = str(piece)
        targetCell = self._poc2cell(refPiece, refDirection)

        # is the move valid
        if not self._validate_turn(piece, 'move'):
            raise HiveException("Invalid Piece Placement")

        if not self._validate_move_piece(piece, targetCell):
            raise HiveException("Invalid Piece Movement")

        pp = self.playedPieces[pieceName]
        startingCell = pp['cell']

        # remove the piece from its current location
        self.piecesInCell[startingCell].remove(pieceName)

        # places the piece at the target location
        self.board.resize(targetCell)
        pp['cell'] = targetCell
        pic = self.piecesInCell.setdefault(targetCell, [])
        pic.append(str(piece))

        return targetCell


    def place_piece(self, piece, refPieceName=None, refDirection=None):
        """
        Place a piece on the playing board.
        """

        # if it's the first piece we put it at cell (0, 0)
        if refPieceName is None and self.turn == 1:
            targetCell = (0, 0)
        else:
            targetCell = self._poc2cell(refPieceName, refDirection)

        # is the placement valid
        if not self._validate_turn(piece, 'place'):
            raise HiveException("Invalid Piece Placement")

        if not self._validate_place_piece(piece, targetCell):
            raise HiveException("Invalid Piece Placement")

        # places the piece at the target location
        self.board.resize(targetCell)
        self.playedPieces[str(piece)] = {'piece': piece, 'cell': targetCell}
        pic = self.piecesInCell.setdefault(targetCell, [])
        pic.append(str(piece))

        return targetCell


    def check_victory(self):
        """
        Check if white wins or black wins or draw or not finished
        """
        white = False
        black = False
        res = self.UNFINISHED

        # if white queen is surrounded => black wins
        queen = self.playedPieces.get('wQ1')
        if(
            queen is not None and
            len(self._occupied_surroundings(queen['cell'])) == 6
        ):
            black = True
            res = self.BLACK_WIN

        # if black queen is surrounded => white wins
        queen = self.playedPieces.get('wB1')
        if(
            queen is not None and
            len(self._occupied_surroundings(queen['cell'])) == 6
        ):
            white = True
            res = self.WHITE_WIN

        # if both queens are surrounded
        if white and black:
            res = self.DRAW

        return res


    def _validate_turn(self, piece, action):
        """
        Verifies if the action is valid on this turn.
        """
        is_even_turn = (self.turn % 2) == 0

        # White player plays on the odd turns
        if (not is_even_turn) and piece.color != 'w':
            return False

        # Black player plays on the even turns
        if is_even_turn and piece.color != 'b':
            return False

        # Tournament rule: no queen in the first move
        if (self.turn == 1 or self.turn == 2) and piece.kind == 'Q':
            return False

        # Move actions are only allowed after the queen is on the board
        if action == 'move':
            if is_even_turn and ('bQ1' not in self.playedPieces):
                return False
            if (not is_even_turn) and ('wQ1' not in self.playedPieces):
                return False

        # White Queen must be placed by turn 7 (4th white action)
        if self.turn == 7:
            if 'wQ1' not in self.playedPieces:
                if str(piece) != 'wQ1' or action != 'place':
                    return False

        # Black Queen must be placed by turn 8 (4th black action)
        if self.turn == 8:
            if 'bQ1' not in self.playedPieces:
                if str(piece) != 'bQ1' or action != 'place':
                    return False

        return True


    def _validate_move_piece(self, moving_piece, targetCell):
        # check if the piece has been placed
        pp = self.playedPieces.get(str(moving_piece))
        if pp is None:
            print "piece was not played yet"
            return False

        # check if the move it's to a different targetCell
        if str(moving_piece) in self.piecesInCell.get(targetCell, []):
            print "moving to the same place"
            return False

        # check if moving this piece won't break the hive
        if not self._one_hive(moving_piece):
            print "break _one_hive rule"
            return False

        validate_fun_map = {
            'A': self._valid_ant_move,
            'B': self._valid_beetle_move,
            'G': self._valid_grasshopper_move,
            'Q': self._valid_queen_move,
            'S': self._valid_spider_move
        }

        return validate_fun_map[moving_piece.kind](
            pp['piece'], pp['cell'], targetCell
        )


    def _validate_place_piece(self, piece, targetCell):
        """
        Verifies if a piece can be played from hand into a given targetCell.
        The piece must be placed touching at least one piece of the same color
        and can only be touching pieces of the same color.
        """

        # targetCell must be free
        if not self._is_cell_free(targetCell):
            return False

        # the piece was already played
        if str(piece) in self.playedPieces:
            return False

        # if it's the first turn we don't need to validate
        if self.turn == 1:
            return True

        # if it's the second turn we put it without validating touching colors
        if self.turn == 2:
            return True

        playedColor = piece.color

        occupiedCells = self._occupied_surroundings(targetCell)
        visiblePieces = [
            self.piecesInCell[oCell][-1] for oCell in occupiedCells
        ]
        res = True
        for pName in visiblePieces:
            if self.playedPieces[pName]['piece'].color != playedColor:
                res = False
                break

        return res


    def _is_cell_free(self, cell):
        pic = self.piecesInCell.get(cell, [])
        return len(pic) == 0


    def _occupied_surroundings(self, cell):
        """
        Returns a list of surrounding cells that contain a piece.
        """
        surroundings = self.board.get_surrounding(cell)
        return [c for c in surroundings if not self._is_cell_free(c)]


    # TODO: rename/remove this function.
    def _poc2cell(self, refPiece, pointOfContact):
        """
        Translates a relative position (piece, point of contact) into
        a board cell (x, y).
        """
        refCell = self.locate(refPiece)
        return self.board.get_dir_cell(refCell, pointOfContact)


    def _bee_moves(self, cell):
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
            if not self._is_cell_free(target):
                continue
            # does it have an adjacent fee cell that is also adjacent to the
            # starting cell?
            if (
                self._is_cell_free(surroundings[i])
                or self._is_cell_free(surroundings[i-2])
            ):
                # does it have an adjacent occupied cell other then the
                # starting cell?
                tOSurroundings = self._occupied_surroundings(target)
                if cell in tOSurroundings:
                    tOSurroundings.remove(cell)
                if len(tOSurroundings) > 0:
                    available_moves.append(target)

        return available_moves


    def _piece_set(self, color):
        """
        Return a full set of hive pieces
        """
        pieceSet = {}
        for i in xrange(3):
            ant = HivePiece(color, 'A', i+1)
            pieceSet[str(ant)] = ant
            grasshopper = HivePiece(color, 'G', i+1)
            pieceSet[str(grasshopper)] = grasshopper
        for i in xrange(2):
            spider = HivePiece(color, 'S', i+1)
            pieceSet[str(spider)] = spider
            beetle = HivePiece(color, 'B', i+1)
            pieceSet[str(beetle)] = beetle
        queen = HivePiece(color, 'Q', 1)
        pieceSet[str(queen)] = queen
        return pieceSet


# +++               +++
# +++ One Hive rule +++
# +++               +++
    def _one_hive(self, piece):
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

        # temporarily remove the piece
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

# --- ---

# +++                +++
# +++ Movement rules +++
# +++                +++
    def _valid_ant_move(self, ant, startCell, endCell):
        # check if ant has no piece on top blocking the move
        if self.piecesInCell[startCell][-1] != str(ant):
            return False
        # temporarily remove ant
        self.piecesInCell[startCell].remove(str(ant))

        toExplore = set([startCell])
        visited = set([startCell])
        res = False

        while len(toExplore) > 0:
            found = set()
            for c in toExplore:
                found.update(self._bee_moves(c))
            found.difference_update(visited)
            # have we found the endCell?
            if endCell in found:
                res = True
                break

            visited.update(found)
            toExplore = found

        # restore ant to it's original position
        self.piecesInCell[startCell].append(str(ant))

        return res


    def _valid_beetle_move(self, beetle, startCell, endCell):
        # check if beetle has no piece on top blocking the move
        if not self.piecesInCell[startCell][-1] == str(beetle):
            return False
        # temporarily remove beetle
        self.piecesInCell[startCell].remove(str(beetle))

        res = False
        # are we on top of the hive?
        if len(self.piecesInCell[startCell]) > 0:
            res = endCell in self.board.get_surrounding(startCell)
        else:
            res = endCell in (
                self._bee_moves(startCell) +
                self._occupied_surroundings(startCell)
            )

        # restore beetle to it's original position
        self.piecesInCell[startCell].append(str(beetle))

        return res


    def _valid_grasshopper_move(self, grasshopper, startCell, endCell):
        # TODO: add function to HexBoard that find cells in a straight line

        # is the move in only one direction?
        (sx, sy) = startCell
        (ex, ey) = endCell
        dx = ex - sx
        dy = ey - sy
        p = sy % 2  # starting from an even or odd line?

        # horizontal jump
        if dy == 0:
            # must jump at least over one piece
            if abs(dx) <= 1:
                return False
        # diagonal jump (dy != 0)
        else:
            # must jump at least over one piece
            if abs(dy) <= 1:
                return False

        moveDir = self.board.get_line_dir(startCell, endCell)
        # must move in a straight line
        if moveDir is None or moveDir == 0:
            return False

        # are all in-between cells occupied?
        c = self.board.get_dir_cell(startCell, moveDir)
        while c != endCell:
            if self._is_cell_free(c):
                return False
            c = self.board.get_dir_cell(c, moveDir)

        # is the endCell free?
        if not self._is_cell_free(endCell):
            return False

        return True


    def _valid_queen_move(self, queen, startCell, endCell):
        return endCell in self._bee_moves(startCell)


    def _valid_spider_move(self, spider, startCell, endCell):
        # check if spider has no piece on top blocking the move
        if not self.piecesInCell[startCell][-1] == str(spider):
            return False
        # temporarily remove spider
        self.piecesInCell[startCell].remove(str(spider))


        visited = set()
        firstStep = set()
        secondStep = set()
        thirdStep = set()

        visited.add(startCell)

        firstStep.update(set(self._bee_moves(startCell)))
        visited.update(firstStep)

        for c in firstStep:
            secondStep.update(set(self._bee_moves(c)))
        secondStep.difference_update(visited)
        visited.update(secondStep)

        for c in secondStep:
            thirdStep.update(set(self._bee_moves(c)))
        thirdStep.difference_update(visited)

        # restore spider to it's original position
        self.piecesInCell[startCell].append(str(spider))

        return endCell in thirdStep

# --- ---
