#!/usr/bin/python2

import unittest
from gamelogic import letter_to_index, in_bounds, move, InvalidMoveExpection

class TestLogic(unittest.TestCase):

    def test_letter_to_index(self):
        self.assertEqual(letter_to_index("a"), 0)
        self.assertEqual(letter_to_index("A"), 0)
        self.assertEqual(letter_to_index("g"), 6)

    def test_in_bounds(self):
        self.assertTrue(in_bounds(0,0))
        self.assertFalse(in_bounds(7,0))

    def test_origin_peg_in_bounds(self):
        with self.assertRaises(InvalidMoveExpection):
            move(None, ("h1", "down"))
        with self.assertRaises(InvalidMoveExpection):
            move(None, ("a8", "up"))
        move(None, ("c3", "down"))

    def test_wrong_direction(self):
        with self.assertRaises(ValueError):
            move(None, ("a1", "north"))
        with self.assertRaises(ValueError):
            move(None, ("a1", "k"))


if __name__ == '__main__':
    unittest.main()
