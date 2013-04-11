#! /usr/bin/env python

import time
import sys
from board import HexBoard
from hive import Hive


class HiveShellClient(object):
    """docstring for HiveShellClient"""

    def __init__(self):
        super(HiveShellClient, self).__init__()
        self.hive = Hive()
        self.input = sys.stdin


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


    def pocp_to_cell(self, pointOfContact, refPiece):
        if pointOfContact == '|*':
            return self.hive.board.poc2cell(refPiece, 1)
        if pointOfContact == '/*':
            return self.hive.board.poc2cell(refPiece, 2)
        if pointOfContact == '*\\':
            return self.hive.board.poc2cell(refPiece, 3)
        if pointOfContact == '*|':
            return self.hive.board.poc2cell(refPiece, 4)
        if pointOfContact == '*/':
            return self.hive.board.poc2cell(refPiece, 5)
        if pointOfContact == '\\*':
            return self.hive.board.poc2cell(refPiece, 6)
        if pointOfContact == '=*':
            return self.hive.board.poc2cell(refPiece, 0)


    def exec_cmd(self, cmd):
        (movingPiece, pointOfContact, refPiece) = self.parse_cmd(cmd)
        if pointOfContact is None:
            if self.hive.turn == 1:
                self.hive.board.place((0, 0), movingPiece)
        else:
            # if the piece is on the board
            # first remove the pice from it's current location
            startCell = self.hive.board.locate(movingPiece)
            targetCell = self.pocp_to_cell(pointOfContact, refPiece)
            if not startCell is None:
                self.hive.board.remove(movingPiece)
            self.hive.board.place(targetCell, movingPiece)


    def run(self):
        while True:
            self.hive.turn += 1
            print self.hive
            print "player %s play: " % (2 - (self.hive.turn % 2)),
            try:
                cmd = self.input.readline()
            except KeyboardInterrupt, e:
                break
            self.exec_cmd(cmd.strip())

        print "\nThanks for playing. Have a nice day!"


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
    (x, y) = board.get_ll_xy((0, 0))
    board.place((x, y), "wQ1")
    print board
    time.sleep(1)
    (x, y) = board.get_lr_xy((1, 0))
    board.place((x, y), "bA1")
    print board
    time.sleep(1)
    (x, y) = board.get_ul_xy((0, 0))
    board.place((x, y), "wS2")
    print board
    time.sleep(1)
    (x, y) = board.get_r_xy((1, 0))
    board.place((x, y), "bG1")
    print board
    time.sleep(1)
    board.remove("bG1")
    print board
    time.sleep(1)
    (x, y) = board.get_ur_xy((1, 0))
    board.place((x, y), "bG1")
    print board
    time.sleep(1)


if __name__ == '__main__':
    sys.exit(main())
