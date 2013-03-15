from hive import Hive
from unittest import TestCase

class TestHive(TestCase):
    """Verify the game logic"""

    def setUp(self):
        self.hive = Hive()
        self.hive.board.place((0, 0), "wS1")
        self.hive.board.place((1, 0), "bS1")
        (x, y) = self.hive.board.get_ll_xy((0, 0))
        self.hive.board.place((x, y), "wQ1")
        (x, y) = self.hive.board.get_lr_xy((1, 0))
        self.hive.board.place((x, y), "bA1")
        (x, y) = self.hive.board.get_ul_xy((0, 0))
        self.hive.board.place((x, y), "wS2")
        (x, y) = self.hive.board.get_r_xy((1, 0))
        self.hive.board.place((x, y), "bG1")


    def test_one_hive_rule(self):
        self.assertFalse(self.hive.one_hive("wS1"))
        self.assertTrue(self.hive.one_hive("wS2"))
