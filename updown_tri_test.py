from updown_tri import *
import unittest

class TestUpDownTri(unittest.TestCase):

    def test_line(self):
        x1, y1 = tri_center(0, 1, 0)
        x2, y2 = tri_center(1, 1, 0)
        self.assertListEqual(list(tri_line(x1, y1, x2, y2)), [
            (0, 1, 0),
            (1, 1, 0),
        ])

        x1, y1 = tri_center(0, 1, 0)
        x2, y2 = tri_center(2, -1, 1)
        self.assertListEqual(list(tri_line(x1, y1, x2, y2)), [
            (0, 1, 0),
            (1, 1, 0),
            (1, 0, 0),
            (1, 0, 1),
            (1, -1, 1),
            (2, -1, 1),
        ])

        x1, y1 = tri_center(0, 1, 0)
        x2, y2 = tri_center(2, 0, -1)
        self.assertListEqual(list(tri_line(x1, y1, x2, y2)), [
            (0, 1, 0),
            (1, 1, 0),
            (1, 1, -1),
            (2, 1, -1),
            (2, 0, -1)
        ])

if __name__ == '__main__':
    unittest.main()
