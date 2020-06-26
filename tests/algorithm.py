import unittest
from algortims import *


class AlgorithmTest(unittest.TestCase):
    ships = [5, 4, 3, 3, 2]
    algorithm = Algorithm(ships)

    def test_make_grid(self):
        expected = []
        for i in range(10):
            for j in range(10):
                expected.append([i, j])
        self.assertEqual(self.algorithm.possible_targets, expected)

    def test_get_surrounding(self):
        cord = [3, 4]
        expected = [[3, 3], [4, 4], [3, 5], [2, 4]]
        self.assertEqual(self.algorithm.get_surrounding(cord), expected)


class HuntTargetTest(unittest.TestCase):
    ships = [5, 4, 3, 3, 2]
    algorithm = HuntTarget(ships)

    def test_potential_targets(self):
        """
        [4, 4] gets removed (kind of like it was a miss)
        After that, when we hit [4, 5], [4, 4] should not be in te potential targets list
        """
        self.algorithm.possible_targets.remove([4, 4])
        self.algorithm.last_guess = [4, 5]
        self.algorithm.turn()
        self.assertNotIn([4, 4], self.algorithm.potential_targets)

    pass


class HuntTargetParityTest(unittest.TestCase):
    ships = [5, 4, 3, 3, 2]
    algorithm = HuntTargetParity(ships)

    def test_parity_grid(self):
        self.assertNotIn([0, 0], self.algorithm.parity_grid)


class ProbabilityDensityTest(unittest.TestCase):
    ships = [5, 4, 3, 3, 2]
    algorithm = ProbabilityDensity(ships)

    def test_probability(self):
        """
        Should return either [4, 4], [5, 4], [4, 5] or [5, 5] because the middle ones are most likey to contain a
        ship at the start of the game
        """
        self.assertIn(self.algorithm.turn(), [[4, 4], [5, 4], [4, 5], [5, 5]])


class RandomTest(unittest.TestCase):
    ships = [5, 4, 3, 3, 2]
    algorithm = Random(ships)

    need_to_guess = []
    for i in range(10):
        for j in range(10):
            need_to_guess.append([i, j])

    def test_unique_turn(self):
        """
        Make sure that all the random guesses are possible.
        """
        for i in self.need_to_guess:
            with self.subTest(i=i):
                self.assertIn(self.algorithm.turn(), self.need_to_guess)


if __name__ == '__main__':
    unittest.main()
