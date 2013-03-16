from board import Board, HexBoard
from unittest import TestCase

class TestHexBoard(TestCase):
    """Verify the HexBoard logic"""

    def setUp(self):
        self.board = HexBoard()


    def test_get_surrounding(self):
        cell = (1, 1)
        expected = [(0, 1), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2)]
        actual = self.board.get_surrounding(cell)
        self.assertEqual(expected.sort(), actual.sort())

        cell = (-1, -1)
        expected = [(0, -1), (1, 0), (2, 0), (2, -1), (2, -2), (-1, -2)]
        actual = self.board.get_surrounding(cell)
        self.assertEqual(expected.sort(), actual.sort())

        cell = (0, 0)
        expected = [(-1, 0), (-1, 1), (0, 1), (1, 0), (0, -1), (-1, -1)]
        actual = self.board.get_surrounding(cell)
        self.assertEqual(expected.sort(), actual.sort())


class TestBoard(TestCase):
    """Verify Board class logic"""

    def setUp(self):
        self.board = Board()


    def test_get(self):
        self.board.place((-1, -1), "p1")
        self.board.place((-1, 1), "p2")
        self.board.get((-1,-2))
        self.assertEqual([], self.board.get((-1,-2)))
