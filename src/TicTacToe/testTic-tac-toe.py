import unittest
import numpy as np
from tic_tac_toe import checkWin


class TestTTT(unittest.TestCase):

    def testWin(self):
        field = np.array([['X', 'X', 'X'], [' ', ' ', 'O'], ['O', ' ', ' ']])
        self.assertTrue(checkWin(field, 'X', 3, 3, 3))

        field = np.array([['X', 'O', 'X'], [' ', 'O', 'O'], ['O', 'O', ' ']])
        self.assertTrue(checkWin(field, 'O', 3, 3, 3))

        field = np.array([[' ', ' ', 'O'], [' ', 'O', ' '], ['O', ' ', ' ']])
        self.assertTrue(checkWin(field, 'O', 3, 3, 3))

        field = np.array([['X', ' ', 'X', 'O', ' '], ['X', 'X', ' ', 'O', 'X'],
                          [' ', 'O', 'O', 'O', 'X'], ['O', 'X', 'O', 'O', 'X']])
        self.assertTrue(checkWin(field, 'O', 5, 4, 4))

        field = np.array([['X', ' ', ' ', ' '], ['X', ' ', ' ', ' '], ['X', ' ', ' ', ' '], ['X', ' ', ' ', ' ']])
        self.assertTrue(checkWin(field, 'X', 4, 4, 4))


if __name__ == '__main__':
    unittest.main()
