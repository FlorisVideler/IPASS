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
    pass


class HuntTargetParityTest(unittest.TestCase):
    pass


class ProbabilityDensityTest(unittest.TestCase):
    pass


class RandomTest(unittest.TestCase):
    ships = [5, 4, 3, 3, 2]
    algorithm = Random(ships)

    need_to_guess = []
    for i in range(10):
        for j in range(10):
            need_to_guess.append([i, j])

    def test_unique_turn(self):

        for i in self.need_to_guess:
            with self.subTest(i=i):
                self.assertIn(self.algorithm.turn(), self.need_to_guess)



if __name__ == '__main__':
    unittest.main()
