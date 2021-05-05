from flat_topped_hex import *
import unittest

class TestFlatToppedHex(unittest.TestCase):

    def test_rect(self):
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

if __name__ == '__main__':
    unittest.main()
