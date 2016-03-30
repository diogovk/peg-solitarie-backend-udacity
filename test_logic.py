#!/usr/bin/python2

import unittest
from gamelogic import letter_to_index, in_bounds, move, InvalidMoveExpection
from gamelogic import peg_destination, INITIAL_BOARD
from rpc_messages import GameMessage

# Initial game state
GAME_STATE=GameMessage(user="fakeuser",
                       board=INITIAL_BOARD,
                       game_over=False,
                       urlsafe_key="fake_key")


class TestLogic(unittest.TestCase):

    def test_letter_to_index(self):
        self.assertEqual(letter_to_index("a"), 0)
        self.assertEqual(letter_to_index("A"), 0)
        self.assertEqual(letter_to_index("g"), 6)

    def test_in_bounds(self):
        self.assertTrue(in_bounds(0, 0))
        self.assertFalse(in_bounds(7, 0))

    def test_origin_peg_in_bounds(self):
        with self.assertRaises(InvalidMoveExpection):
            move(GAME_STATE, ("h1", "down"))
        with self.assertRaises(InvalidMoveExpection):
            move(GAME_STATE, ("a8", "up"))
        move(GAME_STATE, ("c3", "down"))

    def test_dest_peg_in_bounds(self):
        with self.assertRaises(InvalidMoveExpection):
            move(GAME_STATE, ("f4", "right"))
        with self.assertRaises(InvalidMoveExpection):
            move(GAME_STATE, ("b4", "left"))
        move(GAME_STATE, ("d6", "up"))

    def test_wrong_direction(self):
        with self.assertRaises(ValueError):
            move(GAME_STATE, ("a1", "north"))
        with self.assertRaises(ValueError):
            move(GAME_STATE, ("a1", "k"))

    def test_peg_destination(self):
        self.assertEqual((3, 3), peg_destination(3, 5, "u"))
        self.assertEqual((3, 3), peg_destination(3, 1, "d"))
        self.assertEqual((3, 3), peg_destination(5, 3, "l"))
        self.assertEqual((3, 3), peg_destination(1, 3, "r"))


if __name__ == '__main__':
    unittest.main()
