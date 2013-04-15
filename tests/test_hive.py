from hive import Hive
from unittest import TestCase
from piece import HivePiece


class TestHive(TestCase):
    """Verify the game logic"""

    # Pieces used for testing
    piece = {
        'wQ1': HivePiece('w', 'Q', 1),
        'wS1': HivePiece('w', 'S', 1),
        'wS2': HivePiece('w', 'S', 2),
        'wB1': HivePiece('w', 'B', 1),
        'bS1': HivePiece('b', 'S', 1),
        'bA1': HivePiece('b', 'A', 1),
        'bG1': HivePiece('b', 'G', 1),
    }

    def setUp(self):
        self.hive = Hive()
        self.hive.turn += 1
        self.hive.place_piece(self.piece['wS1'])
        self.hive.turn += 1
        self.hive.place_piece(self.piece['bS1'], 'wS1', 4)
        self.hive.turn += 1
        self.hive.place_piece(self.piece['wQ1'], 'wS1', 6)
        self.hive.turn += 1
        self.hive.place_piece(self.piece['bA1'], 'bS1', 5)
        self.hive.turn += 1
        self.hive.place_piece(self.piece['wS2'], 'wS1', 2)
        self.hive.turn += 1
        self.hive.place_piece(self.piece['bG1'], 'bS1', 4)
        self.hive.turn += 1
        self.hive.place_piece(self.piece['wB1'], 'wS1', 1)


    def test_one_hive(self):
        self.assertFalse(self.hive.one_hive(self.piece['wS1']))
        self.assertTrue(self.hive.one_hive(self.piece['wS2']))


    def test_bee_moves(self):
        beePos = self.hive.locate('wQ1')
        expected = [(-2, 1), (0, 1)]
        self.assertEquals(expected, self.hive.bee_moves(beePos))

        beePos = self.hive.locate('wS1')
        expected = []
        self.assertEquals(expected, self.hive.bee_moves(beePos))

        beePos = self.hive.locate('wS2')
        expected = [(-2, -1), (0, -1)]
        self.assertEquals(expected, self.hive.bee_moves(beePos))


    def test_ant_moves(self):
        pass


    def test_beetle_moves(self):
        pass


    def test_grasshopper_moves(self):
        starting_cell = (2, 0)
        end_cell = (-2, 0)
        self.assertTrue(
            self.hive.valid_grasshopper_move(starting_cell, end_cell)
        )

        starting_cell = (2, 0)
        end_cell = (1, 2)
        self.assertTrue(
            self.hive.valid_grasshopper_move(starting_cell, end_cell)
        )

        starting_cell = (2, 0)
        end_cell = (-3, 0)
        self.assertFalse(
            self.hive.valid_grasshopper_move(starting_cell, end_cell)
        )


    def test_validate_place_piece(self):
        wA1 = HivePiece('w', 'A', 1)
        bQ1 = HivePiece('b', 'Q', 1)

        cell = self.hive.poc2cell(self.piece['wS1'], 1)
        self.assertTrue(
            self.hive._validate_place_piece(wA1, cell)
        )
        self.assertFalse(
            self.hive._validate_place_piece(bQ1, cell)
        )
