#! /usr/bin/env python

import time
import sys
from board import HexBoard
from hive import Hive
from piece import HivePiece

class HiveShellClient(object):
    """docstring for HiveShellClient"""

    def __init__(self):
        super(HiveShellClient, self).__init__()
        self.hive = Hive()
        self.input = sys.stdin
        self.player = {1: None, 2: None}


    def piece_set(self, color):
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

    def parse_cmd(self, cmd):
        if len(cmd) == 3:
            movingPiece = cmd
            pointOfContact = None
            refPiece = None
        else:
            movingPiece = cmd[:3]
            pointOfContact = cmd[3:5]
            refPiece = cmd[5:]
        return (movingPiece, pointOfContact, refPiece)


    def ppoc2cell(self, pointOfContact, refPiece):
        direction = self.poc2direction(pointOfContact)
        return self.hive.poc2cell(refPiece, direction)


    def poc2direction(self, pointOfContact):
        "Parse point of contact to a Hive.direction"
        if pointOfContact == '|*':
            return Hive.W
        if pointOfContact == '/*':
            return Hive.NW
        if pointOfContact == '*\\':
            return Hive.NE
        if pointOfContact == '*|':
            return Hive.E
        if pointOfContact == '*/':
            return Hive.SE
        if pointOfContact == '\\*':
            return Hive.SW
        if pointOfContact == '=*':
            return Hive.O
        return None


    def exec_cmd(self, cmd, turn):
        (actPiece, pointOfContact, refPiece) = self.parse_cmd(cmd)
        actPlayer = (2 - (turn % 2))
        # if the piece is on the board
        # first remove the pice from it's current location
        if refPiece is not None:
            targetCell = self.ppoc2cell(pointOfContact, refPiece)
        startCell = self.hive.locate(actPiece)
        if startCell is None:
            p = self.player[actPlayer][actPiece]
            if not self.hive.place_piece(
                p, refPiece, self.poc2direction(pointOfContact)
            ):
                return False
        else:
            # TODO: change this to self.hive.move(actPiece, target)
            self.hive.board.remove(actPiece)
            self.hive.board.place(targetCell, actPiece)
        return True


    def run(self):
        self.player[1] = self.piece_set('w')
        self.player[2] = self.piece_set('b')
        self.hive.turn += 1
        while True:
            print self.hive
            print "player %s play: " % (2 - (self.hive.turn % 2)),
            try:
                cmd = self.input.readline()
            except KeyboardInterrupt, e:
                break
            if self.exec_cmd(cmd.strip(), self.hive.turn):
                self.hive.turn += 1
            else:
                print "invalid play!"

        print "\nThanks for playing Hive. Have a nice day!"


def main():

    game = HiveShellClient()
    game.run()

    board = HexBoard()
    board.place((0, 0), "wS1")
    print board
    time.sleep(1)
    board.place((1, 0), "bS1")
    print board
    time.sleep(1)
    (x, y) = board.get_sw_xy((0, 0))
    board.place((x, y), "wQ1")
    print board
    time.sleep(1)
    (x, y) = board.get_se_xy((1, 0))
    board.place((x, y), "bA1")
    print board
    time.sleep(1)
    (x, y) = board.get_nw_xy((0, 0))
    board.place((x, y), "wS2")
    print board
    time.sleep(1)
    (x, y) = board.get_e_xy((1, 0))
    board.place((x, y), "bG1")
    print board
    time.sleep(1)
    board.remove("bG1")
    print board
    time.sleep(1)
    (x, y) = board.get_ne_xy((1, 0))
    board.place((x, y), "bG1")
    print board
    time.sleep(1)


if __name__ == '__main__':
    sys.exit(main())
