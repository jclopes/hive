from hive import Hive
from unittest import TestCase
from piece import HivePiece


class TestHive(TestCase):
    """Verify the game logic"""

    # Pieces used for testing
    piece = {
        'wS1': HivePiece('w', 'S', 1),
        'wQ1': HivePiece('w', 'Q', 1),
        'wS2': HivePiece('w', 'S', 2),
        'bS1': HivePiece('b', 'S', 1),
        'bA1': HivePiece('b', 'A', 1),
        'bG1': HivePiece('b', 'G', 1),
    }

    def setUp(self):
        self.hive = Hive()
        self.hive.board.place((0, 0), self.piece['wS1'])
        self.hive.board.place((1, 0), self.piece['bS1'])
        (x, y) = self.hive.board.get_sw_xy((0, 0))
        self.hive.board.place((x, y), self.piece['wQ1'])
        (x, y) = self.hive.board.get_se_xy((1, 0))
        self.hive.board.place((x, y), self.piece['bA1'])
        (x, y) = self.hive.board.get_nw_xy((0, 0))
        self.hive.board.place((x, y), self.piece['wS2'])
        (x, y) = self.hive.board.get_e_xy((1, 0))
        self.hive.board.place((x, y), self.piece['bG1'])
        (x, y) = self.hive.board.get_w_xy((0, 0))
        self.hive.board.place((x, y), self.piece['wB1'])


    def test_one_hive(self):
        self.assertFalse(self.hive.one_hive(self.piece['wS1']))
        self.assertTrue(self.hive.one_hive(self.piece['wS2']))


    def test_bee_moves(self):
        beePos = self.hive.board.locate(self.piece['wQ1'])
        expected = [(-1, 0), (0, 1)]
        self.assertEquals(expected, self.hive.bee_moves(beePos))

        beePos = self.hive.board.locate(self.piece['wS1'])
        expected = []
        self.assertEquals(expected, self.hive.bee_moves(beePos))

        beePos = self.hive.board.locate(self.piece['wS2'])
        expected = [(-1, 0), (0, -1)]
        self.assertEquals(expected, self.hive.bee_moves(beePos))


    def test_validate_place_piece(self):
        wA1 = HivePiece('w', 'A', 1)
        bQ1 = HivePiece('b', 'Q', 1)

        self.assertTrue(
            self.hive.validate_place_piece(wA1, self.piece['wS1'], 1)
        )
        self.assertFalse(
            self.hive.validate_place_piece(bQ1, self.piece['wS1'], 1)
        )
