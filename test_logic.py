#!/usr/bin/python2

import unittest
from gamelogic import letter_to_index, in_bounds, make_move
from gamelogic import peg_destination, INITIAL_BOARD, InvalidMoveExpection
from rpc_messages import GameMessage
from models import Game, User


class TestLogic(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.fakeuser = User(name="fakeuser", email="fakeuser@example.com")

    def setUp(self):
        self.GAME_STATE = Game(user=self.fakeuser.key, board=INITIAL_BOARD)

    def test_letter_to_index(self):
        self.assertEqual(letter_to_index("a"), 0)
        self.assertEqual(letter_to_index("A"), 0)
        self.assertEqual(letter_to_index("g"), 6)

    def test_in_bounds(self):
        self.assertTrue(in_bounds(0, 0))
        self.assertFalse(in_bounds(7, 0))

    def test_origin_peg_in_bounds(self):
        with self.assertRaises(InvalidMoveExpection):
            make_move(self.GAME_STATE, ("h1", "down"))
        with self.assertRaises(InvalidMoveExpection):
            make_move(self.GAME_STATE, ("a8", "up"))
        make_move(self.GAME_STATE, ("d2", "down"))

    def test_dest_peg_in_bounds(self):
        with self.assertRaises(InvalidMoveExpection):
            make_move(self.GAME_STATE, ("f4", "right"))
        with self.assertRaises(InvalidMoveExpection):
            make_move(self.GAME_STATE, ("b4", "left"))
        make_move(self.GAME_STATE, ("d6", "up"))

    def test_wrong_direction(self):
        with self.assertRaises(ValueError):
            make_move(self.GAME_STATE, ("b4", "north"))
        with self.assertRaises(ValueError):
            make_move(self.GAME_STATE, ("d5", "k"))

    def test_peg_destination(self):
        self.assertEqual((3, 3), peg_destination(3, 5, "u"))
        self.assertEqual((3, 3), peg_destination(3, 1, "d"))
        self.assertEqual((3, 3), peg_destination(5, 3, "l"))
        self.assertEqual((3, 3), peg_destination(1, 3, "r"))

    def test_move_sanity(self):
        with self.assertRaises(InvalidMoveExpection):
            # Invalid move since d4(jump) is a hole.
            # A valid move should "jump" over a peg.
            make_move(self.GAME_STATE, ("c4", "left"))
        with self.assertRaises(InvalidMoveExpection):
            # Invalid move since d4(origin) is a hole.
            # A valid move should have a peg as origin.
            make_move(self.GAME_STATE, ("d4", "left"))
        with self.assertRaises(InvalidMoveExpection):
            # Invalid move since c4(destination) is a peg.
            # A valid move should have a hole as destination.
            make_move(self.GAME_STATE, ("a4", "left"))
        with self.assertRaises(InvalidMoveExpection):
            # Invalid move since a2(origin) is an unusable space.
            make_move(self.GAME_STATE, ("a2", "down"))
        with self.assertRaises(InvalidMoveExpection):
            # Invalid move since a2(destination) is an unusable space .
            make_move(self.GAME_STATE, ("a4", "up"))
        # Valid move
        make_move(self.GAME_STATE, ("b4", "right"))

    def test_board_update(self):
        new_state = make_move(self.GAME_STATE, ("b4", "right"))
        expected_board = ['  ***  ',
                          '  ***  ',
                          '*******',
                          '*oo****',
                          '*******',
                          '  ***  ',
                          '  ***  ']
        self.assertEqual(expected_board, new_state.board)
        new_state = make_move(new_state, ("e4", "left"))
        expected_board = ['  ***  ',
                          '  ***  ',
                          '*******',
                          '*o*oo**',
                          '*******',
                          '  ***  ',
                          '  ***  ']
        self.assertEqual(expected_board, new_state.board)

        def test_rest_one(self):
            board = ['  ooo  ',
                     '  ooo  ',
                     'ooooooo',
                     '*oooooo',
                     'ooooooo',
                     '  ooo  ',
                     '  ooo  ']
            assertTrue(rest_one(board))
            board = ['  ooo  ',
                     '  ooo  ',
                     'ooooooo',
                     '**ooooo',
                     'ooooooo',
                     '  ooo  ',
                     '  ooo  ']
            assertFalse(rest_one(board))

    def test_game_solution(self):
        solution = ["b4:r", "c6:u", "a5:r", "a3:d", "c4:d", "c7:u", "d5:l",
                    "a5:r", "f5:l", "c5:r", "d7:u", "d5:r", "e7:u", "f5:l",
                    "f3:d", "g5:l", "g3:d", "d5:r", "g5:l", "d3:r", "e5:u",
                    "f3:l", "e1:d", "d3:r", "b3:r", "c1:d", "c3:r", "d1:d",
                    "d4:u", "f3:l", "d2:d"]
        game = self.GAME_STATE
        self.assertFalse(game.game_over)
        for move in solution:
            origin = move.split(":")[0]
            direction = move.split(":")[1]
            game = make_move(game, (origin, direction))
        self.assertTrue(game.game_over)

if __name__ == '__main__':
    unittest.main()
