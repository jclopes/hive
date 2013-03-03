#! /usr/bin/env python

import sys
from board import HexBoard


def main():
    board = HexBoard()
    board.set(3, 3, "3,3")
    print board


if __name__ == '__main__':
    sys.exit(main())
