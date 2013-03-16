# piece.py
# Classes representing playing pieces

class HivePiece(object):
    """Representation of Playing Piece"""

    def __init__(self, color, kind, number):
        super(Cell, self).__init__()
        self.color = color      # can be 'b' or 'w'
        self.kind = kind        # one of ['A', 'B', 'G', 'Q', 'S']
        self.number = number    # can be [1, 2, 3]


    def __repr__(self):
        return "%s%s%s" % (self.color, self.kind, self.number)
