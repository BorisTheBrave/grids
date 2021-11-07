from flat_topped_hex import *
from square import square_line
import unittest

class TestSquare(unittest.TestCase):

    def test_line(self):
        self.assertListEqual(list(square_line(0, 0, 0, 5)), [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
        ])

if __name__ == '__main__':
    unittest.main()
