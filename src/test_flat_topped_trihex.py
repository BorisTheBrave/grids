from flat_topped_trihex import *
from updown_tri import tri_center
import unittest

class TestFlatToppedTriHex(unittest.TestCase):

    def test_pick(self):
        for (a, b, c) in [(0, 0, 0), (0, 1, 0), (5, -2, -3), (-3, 0, 2)]:
            self.assertEqual(pick_trihex(*trihex_center(a, b,c)), (a, b, c))

    def test_tri_convert(self):
        for (a, b, c) in [(0, 0, 0), (0, 1, 0), (5, -2, -3), (-3, 0, 2)]:
            for tri in trihex_to_tris(a, b, c):
                self.assertEqual(tri_to_trihex(*tri), (a, b, c))


if __name__ == '__main__':
    unittest.main()
