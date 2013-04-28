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


    def test_get_boundaries(self):
        self.assertEqual((0, 0, 0, 0), self.board.get_boundaries())


    def test_resize(self):
        self.board.resize((-2, 2))
        self.board.resize((3, -3))
        self.assertEqual((-2, -3, 3, 2), self.board.get_boundaries())
        self.board.resize((1, -1))
        self.assertEqual((-2, -3, 3, 2), self.board.get_boundaries())
