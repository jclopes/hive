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
        'wG1': HivePiece('w', 'G', 1),
        'bS1': HivePiece('b', 'S', 1),
        'bQ1': HivePiece('b', 'Q', 1),
        'bB1': HivePiece('b', 'B', 1),
        'bA1': HivePiece('b', 'A', 1),
        'bG1': HivePiece('b', 'G', 1),
    }

    def setUp(self):
        #    / \ / \ / \ / \ / \
        #   |wB1|wS2|   |bB1|   |
        #  / \ / \ / \ / \ / \ /
        # |wG1|   |wS1|bS1|bG1|
        #  \ / \ / \ / \ / \ / \
        #   |   |wQ1|   |bQ1|   |
        #  / \ / \ / \ / \ / \ /
        # |   |   |   |bA1|   |
        #  \ / \ / \ / \ / \ /
        self.hive = Hive()
        self.hive.turn += 1
        self.hive.place_piece(self.piece['wS1'])
        self.hive.turn += 1
        self.hive.place_piece(self.piece['bS1'], 'wS1', self.hive.E)
        self.hive.turn += 1
        self.hive.place_piece(self.piece['wQ1'], 'wS1', self.hive.SW)
        self.hive.turn += 1
        self.hive.place_piece(self.piece['bQ1'], 'bS1', self.hive.SE)
        self.hive.turn += 1
        self.hive.place_piece(self.piece['wS2'], 'wS1', self.hive.NW)
        self.hive.turn += 1
        self.hive.place_piece(self.piece['bG1'], 'bS1', self.hive.E)
        self.hive.turn += 1
        self.hive.place_piece(self.piece['wB1'], 'wS2', self.hive.W)
        self.hive.turn += 1
        self.hive.place_piece(self.piece['bA1'], 'bQ1', self.hive.SW)
        self.hive.turn += 1
        self.hive.place_piece(self.piece['wG1'], 'wB1', self.hive.SW)
        self.hive.turn += 1
        self.hive.place_piece(self.piece['bB1'], 'bS1', self.hive.NE)


    def test_one_hive(self):
        self.assertFalse(self.hive._one_hive(self.piece['wS1']))
        self.assertTrue(self.hive._one_hive(self.piece['wQ1']))


    def test_bee_moves(self):
        beePos = self.hive.locate('wQ1')
        expected = [(-2, 1), (-1, 0), (0, 1), (0, 2)]
        self.assertEquals(expected, self.hive._bee_moves(beePos))

        beePos = self.hive.locate('wS1')
        expected = []
        self.assertEquals(expected, self.hive._bee_moves(beePos))

        beePos = self.hive.locate('wS2')
        expected = [(-1, -2), (0, -1)]
        self.assertEquals(expected, self.hive._bee_moves(beePos))


    def test_ant_moves(self):
        startCell = self.hive.locate('bA1')
        endCell = self.hive._poc2cell('wS1', self.hive.W)
        self.assertFalse(
            self.hive._valid_ant_move(startCell, end_cell)
        )

        end_cell = self.hive._poc2cell('bS1', self.hive.SW)
        self.assertTrue(
            self.hive._valid_ant_move(startCell, end_cell)
        )

        end_cell = self.hive._poc2cell('wS1', self.hive.NE)
        self.assertTrue(
            self.hive._valid_ant_move(startCell, end_cell)
        )

        end_cell = self.hive._poc2cell('wQ1', self.hive.W)
        self.assertTrue(
            self.hive._valid_ant_move(startCell, end_cell)
        )


    def test_beetle_moves(self):
        pass


    def test_grasshopper_moves(self):
        starting_cell = self.hive.locate('bG1')
        endCell = self.hive._poc2cell('wS1', self.hive.W)
        self.assertTrue(
            self.hive._valid_grasshopper_move(starting_cell, end_cell)
        )

        end_cell = self.hive._poc2cell('bA1', self.hive.SW)
        self.assertTrue(
            self.hive._valid_grasshopper_move(starting_cell, end_cell)
        )

        end_cell = self.hive._poc2cell('wG1', self.hive.W)
        self.assertFalse(
            self.hive._valid_grasshopper_move(starting_cell, end_cell)
        )

        starting_cell = self.hive.locate('wG1')
        endCell = self.hive._poc2cell('wB1', self.hive.NE)
        self.assertTrue(
            self.hive._valid_grasshopper_move(starting_cell, end_cell)
        )


    def test_validate_place_piece(self):
        wA1 = HivePiece('w', 'A', 1)
        bB2 = HivePiece('b', 'B', 2)

        # place over another piece
        cell = self.hive._poc2cell('wS1', self.hive.SW)
        self.assertFalse(
            self.hive._validate_place_piece(wA1, cell)
        )

        # valid placement
        cell = self.hive._poc2cell('bG1', self.hive.E)
        self.assertTrue(
            self.hive._validate_place_piece(bB2, cell)
        )

        # wrong color
        cell = self.hive._poc2cell('wQ1', self.hive.E)
        self.assertFalse(
            self.hive._validate_place_piece(wA1, cell)
        )


    def test_move_piece(self):
        bB1 = self.piece['bB1']
        bS1 = self.piece['bS1']
        cell = self.hive.locate('bS1')
        self.hive.move_piece(bB1, 'bS1', 0)
        pieces = self.hive.get_pieces(cell)

        self.assertEquals(cell, self.hive.locate('bB1'))
        self.assertEquals(2, len(pieces))
        self.assertTrue(str(bB1) in pieces)
        self.assertTrue(str(bS1) in pieces)
