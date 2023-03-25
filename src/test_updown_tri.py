from updown_tri import *
import unittest

class TestUpDownTri(unittest.TestCase):

    def test_line_intersect(self):
        x1, y1 = tri_center(0, 1, 0)
        x2, y2 = tri_center(1, 1, 0)
        self.assertListEqual(list(tri_line_intersect(x1, y1, x2, y2)), [
            (0, 1, 0),
            (1, 1, 0),
        ])

        x1, y1 = tri_center(0, 1, 0)
        x2, y2 = tri_center(2, -1, 1)
        self.assertListEqual(list(tri_line_intersect(x1, y1, x2, y2)), [
            (0, 1, 0),
            (1, 1, 0),
            (1, 0, 0),
            (1, 0, 1),
            (1, -1, 1),
            (2, -1, 1),
        ])

        x1, y1 = tri_center(0, 1, 0)
        x2, y2 = tri_center(2, 0, -1)
        self.assertListEqual(list(tri_line_intersect(x1, y1, x2, y2)), [
            (0, 1, 0),
            (1, 1, 0),
            (1, 0, 0),
            (2, 0, 0),
            (2, 0, -1)
        ])

    def test_line(self):
        self.assertListEqual(list(tri_line(1, 0, 1, 2, 0, 0)), [
            (1, 0, 1),
            (1, 0, 0),
            (2, 0, 0),
        ])

    def test_rect_intersect(self):
        x1, y1 = tri_center(0, 1, 0)
        self.assertListEqual(list(tri_rect_intersect(x1, y1, 0, 0)), [
            (0, 1, 0)
        ])
        self.assertListEqual(list(tri_rect_intersect(x1, y1, 0, 0.3)), [
            (0, 1, 0),
            (0, 2, 0),
        ])
        self.assertListEqual(list(tri_rect_intersect(x1, y1, 0.6, 0.3)), [
            (0, 1, 0),
            (1, 1, 0),
            (1, 1, -1),
            (0, 2, 0),
            (0, 2, -1),
            (1, 2, -1),
        ])
        self.assertListEqual(list(tri_rect_intersect(x1, y1, 0, sqrt(3) / 2 * 10)), [
            (0, 1, 0),
            (0, 2, 0),
            (-1, 3, -1),
            (-1, 4, -1),
            (-2, 5, -2),
            (-2, 6, -2),
            (-3, 7, -3),
            (-3, 8, -3),
            (-4, 9, -4),
            (-4, 10, -4),
            (-5, 11, -5),
        ])

    def test_reflect(self):
        self.assertEqual(tri_reflect_x(1, 1, 0), (0, 1, 1))
        self.assertEqual(tri_reflect_y(1, 1, 0), (1, 0, 0))
        self.assertEqual(tri_reflect_by(1, 1, 0, 1), (1, 1, 0))
        self.assertEqual(tri_reflect_by(1, 1, 0, -1), (1, 0, 1))

    def test_precision(self):
        # https://github.com/BorisTheBrave/grids/issues/2
        l = list(tri_line(2,-8,7, 23,-27,6))
        self.assertEqual((23, -27, 6), l[-1])

if __name__ == '__main__':
    unittest.main()
