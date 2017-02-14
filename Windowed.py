import collections
import unittest

from MaybeNumber import MaybeNumber


class Windowed(object):
    'computation on the most recent window of items'
    def __init__(self, window_size):
        self.window_size = window_size
        self.items = collections.deque([], window_size)

    def append(self, item):
        self.items.append(item)

    def sum(self):
        if len(self.items) < self.window_size:
            return MaybeNumber(None)
        else:
            sum = 0
            for item in self.items:
                sum += item
            return MaybeNumber(sum)


class TestWindowed(unittest.TestCase):
    def test_window_size_1(self):
        w = Windowed(1)
        tests = (
            (None, None),
            (1, 1),
            (2, 2),
        )
        for test in tests:
            item, expected_sum = test
            if item is not None:
                w.append(item)
            self.assertEqual(MaybeNumber(expected_sum), w.sum())

    def test_window_size_2(self):
        w = Windowed(2)
        tests = (
            (None, None),
            (1, None),
            (2, 3),
            (3, 5),
        )
        for test in tests:
            item, expected_sum = test
            if item is not None:
                w.append(item)
            self.assertEqual(MaybeNumber(expected_sum), w.sum())


if __name__ == '__main__':
    unittest.main()
