from flat_topped_hex import *
import unittest

class TestFlatToppedHex(unittest.TestCase):

    def test_rect1(self):
        rect = (0, 0, 0, 3, 3, False, False)
        self.assertListEqual(list(hex_rect(*rect)), [
            (0, 0, 0),
            (0, 1, -1),
            (0, 2, -2),
            (1, 0, -1),
            (1, 1, -2),
            (2, -1, -1),
            (2, 0, -2),
            (2, 1, -3),
        ])

        i = 0
        for hex in hex_rect(*rect):
            self.assertEqual(hex_rect_index(*hex, *rect), i)
            self.assertEqual(hex_rect_deindex(i, *rect), hex)
            i += 1

        self.assertEqual(len(list(hex_rect(*rect))), hex_rect_size(*rect))

    def test_rect2(self):
        rect = (0, 0, 0, 3, 3, True, True)
        self.assertListEqual(list(hex_rect(*rect)), [
            (0, 0, 0),
            (0, 1, -1),
            (0, 2, -2),
            (1, -1, 0),
            (1, 0, -1),
            (1, 1, -2),
            (1, 2, -3),
            (2, -1, -1),
            (2, 0, -2),
            (2, 1, -3),
        ])

        i = 0
        for hex in hex_rect(*rect):
            self.assertEqual(hex_rect_index(*hex, *rect), i)
            self.assertEqual(hex_rect_deindex(i, *rect), hex)
            i += 1

        self.assertEqual(len(list(hex_rect(*rect))), hex_rect_size(*rect))

    def test_hex_line(self):
        self.assertListEqual(list(hex_line(0, 0, 0, 4, -3, -1)), [
            (0, 0, 0),
            (1, -1, 0),
            (2, -1, -1), # (2, -2, 0) would be an equally valid choice
            (3, -2, -1),
            (4, -3, -1)
        ])

    def test_hex_to_tris(self):
        self.assertListEqual(hex_to_tris(1, 0, -1), [
            (2, 1, -2),
            (2, 2, -2),
            (1, 2, -2),
            (1, 2, -1),
            (1, 1, -1),
            (2, 1, -1),
        ])
        for tri in hex_to_tris(1, 0, -1):
            self.assertEqual(tri_to_hex(*tri), (1, 0, -1))

if __name__ == '__main__':
    unittest.main()
