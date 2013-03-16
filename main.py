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


    def run(self):
        while True:
            print self.hive
            print "play: ",
            try:
                cmd = self.input.readline()
            except KeyboardInterrupt, e:
                break

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
