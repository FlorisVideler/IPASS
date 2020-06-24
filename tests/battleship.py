import unittest
from battleship import *


class TestShip(unittest.TestCase):
    board = Board([3])
    ship = Ship(3, board)

    def test_lenght_to_coordinates(self):
        expected_output = [[0, 0], [1, 0], [2, 0]]
        self.assertEqual(self.ship.cords, expected_output)

    def test_rotate(self):
        expected_output = [[0, 0], [0, 1], [0, 2]]
        self.ship.rotate()
        self.assertEqual(self.ship.cords, expected_output)

    def test_update_position(self):
        expected_ouput = [[5, 5], [5, 6], [5, 7]]
        self.ship.update_position(expected_ouput)
        self.assertEqual(self.ship.cords, expected_ouput)

class TestBoard(unittest.TestCase):
    board = Board([3])

    def test_out_of_bounds(self):
        out_of_bounds = [[8, 8], [8, 9], [8, 10]]
        not_out_of_bounds = [[5, 4], [5, 5], [5, 6]]

        self.assertTrue(self.board.out_of_bounds(out_of_bounds))
        self.assertFalse(self.board.out_of_bounds(not_out_of_bounds))

class TestPlayerBoard(unittest.TestCase):
    ship_sizes = [5, 4, 3, 3, 2]
    display = Display()
    player_board = PlayerBoard(ship_sizes, display)
    # display.show()


    def test_mouse_to_tile(self):
        position_not_on_map = (100, 390)

        self.assertEqual([0], self.player_board.selector_click(position_not_on_map))


class TestAIBoard(unittest.TestCase):
    ship_sizes = [5, 4, 3, 3, 2]
    ai_board = AIBoard(ship_sizes)

    def test_ship_placing(self):
        self.ai_board.place_ships()
        self.assertEqual(len(self.ship_sizes), len(self.ai_board.ships))

if __name__ == '__main__':
    unittest.main()
