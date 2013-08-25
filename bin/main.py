#! /usr/bin/env python

import time
import sys
from hivegame.board import HexBoard
from hivegame.hive import Hive, HiveException
from hivegame.piece import HivePiece
from hivegame.view import HiveView


class HiveShellClient(object):
    """HiveShellClient is a command line client to the Hive game."""

    def __init__(self):
        super(HiveShellClient, self).__init__()
        self.hive = Hive()
        self.view = HiveView(self.hive)
        self.input = sys.stdin
        self.player = {1: None, 2: None}
        self.logger = None


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
        self.logger.write(cmd+'\n')

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
        try:
            p = self.player[actPlayer][actPiece]
        except Exception, e:
            return False

        direction = None
        if pointOfContact is not None:
            direction = self.poc2direction(pointOfContact)

        self.hive.action(actPiece, refPiece, direction)
        return True


    def run(self):
        self.logger = open('game.log', 'w')
        self.player[1] = self.piece_set('w')
        self.player[2] = self.piece_set('b')
        self.hive.turn += 1 # white player start
        self.hive.setup()

        while self.hive.check_victory() == self.hive.UNFINISHED:
            print "Turn: %s" % self.hive.turn
            active_player = (2 - (self.hive.turn % 2))
            print self.view
            print "pieces available: %s" % sorted(
                self.player[active_player].keys()
            )
            print "player %s play: " % active_player,
            try:
                cmd = self.input.readline()
            except KeyboardInterrupt, e:
                break
            if self.exec_cmd(cmd.strip(), self.hive.turn):
                print
                print "=" * 79
                print
            else:
                print "invalid play!"

        print "\nThanks for playing Hive. Have a nice day!"


def main():

    game = HiveShellClient()
    game.run()


if __name__ == '__main__':
    sys.exit(main())
