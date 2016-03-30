#!/usr/bin/python2

import unittest
from gamelogic import letter_to_index, in_bounds, move, InvalidMoveExpection
from gamelogic import peg_destination, INITIAL_BOARD
from rpc_messages import GameMessage

# Initial game state
GAME_STATE = GameMessage(user="fakeuser",
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
        move(GAME_STATE, ("d2", "down"))

    def test_dest_peg_in_bounds(self):
        with self.assertRaises(InvalidMoveExpection):
            move(GAME_STATE, ("f4", "right"))
        with self.assertRaises(InvalidMoveExpection):
            move(GAME_STATE, ("b4", "left"))
        move(GAME_STATE, ("d6", "up"))

    def test_wrong_direction(self):
        with self.assertRaises(ValueError):
            move(GAME_STATE, ("b4", "north"))
        with self.assertRaises(ValueError):
            move(GAME_STATE, ("d5", "k"))

    def test_peg_destination(self):
        self.assertEqual((3, 3), peg_destination(3, 5, "u"))
        self.assertEqual((3, 3), peg_destination(3, 1, "d"))
        self.assertEqual((3, 3), peg_destination(5, 3, "l"))
        self.assertEqual((3, 3), peg_destination(1, 3, "r"))

    def test_move_sanity(self):
        with self.assertRaises(InvalidMoveExpection):
            # Invalid move since d4(jump) is a hole.
            # A valid move should "jump" over a peg.
            move(GAME_STATE, ("c4", "left"))
        with self.assertRaises(InvalidMoveExpection):
            # Invalid move since d4(origin) is a hole.
            # A valid move should have a peg as origin.
            move(GAME_STATE, ("d4", "left"))
        with self.assertRaises(InvalidMoveExpection):
            # Invalid move since c4(destination) is a peg.
            # A valid move should have a hole as destination.
            move(GAME_STATE, ("a4", "left"))
        with self.assertRaises(InvalidMoveExpection):
            # Invalid move since a2(origin) is an unusable space.
            move(GAME_STATE, ("a2", "down"))
        with self.assertRaises(InvalidMoveExpection):
            # Invalid move since a2(destination) is an unusable space .
            move(GAME_STATE, ("a4", "up"))
        # Valid move
        move(GAME_STATE, ("b4", "right"))

    def test_board_update(self):
        new_state = move(GAME_STATE, ("b4", "right"))
        expected_board = ['  ***  ',
                          '  ***  ',
                          '*******',
                          '*oo****',
                          '*******',
                          '  ***  ',
                          '  ***  ']
        self.assertEqual(expected_board, new_state.board)

if __name__ == '__main__':
    unittest.main()
