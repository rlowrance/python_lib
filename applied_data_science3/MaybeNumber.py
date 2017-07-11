'''
Copyright 2017 Roy E. Lowrance

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on as "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing premission and
limitation under the license.
'''
from __future__ import division

import math
import numbers
import numpy as np
import pdb
import unittest


class MaybeNumber(object):
    'monad for float values that are numbers or None'
    def __init__(self, value):
        if value is None:
            self.value = None
        elif isinstance(value, MaybeNumber):
            self.value = value.value
        elif isinstance(value, float) and np.isnan(value):
            self.value = None
        else:
            assert isinstance(value, numbers.Number), value
            self.value = value

    def __repr__(self):
        return 'MaybeNumber(%s)' % self.value

    def __eq__(self, other):
        if self.value is None:
            return other.value is None
        if other.value is None:
            return self.value is None
        return self.value == other.value

    def __abs__(self):
        if self.value is None:
            return MaybeNumber(None)
        else:
            return MaybeNumber(abs(self.value))

    def __add__(self, other):
        if isinstance(other, numbers.Number):
            return self + MaybeNumber(other)
        if self.value is None or other.value is None:
            return MaybeNumber(None)
        else:
            return MaybeNumber(self.value + other.value)

    def __radd__(self, other):
        return self + other

    def ge(self, other):
        if isinstance(other, numbers.Number):
            return self.ge(MaybeNumber(other))
        if self.value is None or other.value is None:
            return MaybeNumber(None)
        else:
            return MaybeNumber(self.value >= other.value)

    def le(self, other):
        if isinstance(other, numbers.Number):
            return self.le(MaybeNumber(other))
        if self.value is None or other.value is None:
            return MaybeNumber(None)
        else:
            return MaybeNumber(self.value <= other.value)

    def lt(self, other):
        if isinstance(other, numbers.Number):
            return self.lt(MaybeNumber(other))
        if self.value is None or other.value is None:
            return MaybeNumber(None)
        else:
            return MaybeNumber(self.value < other.value)

    def __sub__(self, other):
        if isinstance(other, numbers.Number):
            return self - MaybeNumber(other)
        if self.value is None or other.value is None:
            return MaybeNumber(None)
        else:
            return MaybeNumber(self.value - other.value)

    def __rsub__(self, other):
        return MaybeNumber(other) - self

    def __truediv__(self, other):
        if isinstance(other, numbers.Number):
            return self / MaybeNumber(other)
        if self.value is None or other.value is None:
            return MaybeNumber(None)
        elif other.value == 0:
            return MaybeNumber(None)
        else:
            return MaybeNumber(self.value / other.value)

    def __rtruediv__(self, other):
        return MaybeNumber(other) / self

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return self * MaybeNumber(other)
        if self.value is None or other.value is None:
            return MaybeNumber(None)
        else:
            return MaybeNumber(self.value * other.value)

    def __rmul__(self, other):
        return self * other

    def mean(self, other):
        sum = self + other
        if sum.value is None:
            return MaybeNumber(None)
        else:
            return (self + other) / MaybeNumber(2.0)

    def sqrt(self):
        if self.value is None:
            return MaybeNumber(None)
        else:
            return MaybeNumber(math.sqrt(self.value))


class TestMaybeNumber(unittest.TestCase):
    def setUp(self):
        pass

    def test_plain_number(self):
        verbose = False
        a = MaybeNumber(10)
        b = 2
        tests = (
            (a + b, MaybeNumber(12)),
            (b + a, MaybeNumber(12)),
            (a - b, MaybeNumber(8)),
            (b - a, MaybeNumber(-8)),
            (a * b, MaybeNumber(20)),
            (b * a, MaybeNumber(20)),
            (a / b, MaybeNumber(5)),
            (b / a, MaybeNumber(0.2)),
        )
        for test in tests:
            actual, expected = test
            if verbose:
                print actual, expected
            self.assertEqual(expected, actual)

    def test_construction(self):
        verbose = False
        tests = (
            (10.0, 10.0),
            (None, None),
            (np.nan, None),
            (MaybeNumber(10.), 10.0),
        )
        for test in tests:
            if verbose:
                print test
            value, expected = test
            x = MaybeNumber(value)
            self.assertEqual(x.value, expected)

    def test_abs(self):
        tests = (
            (0, 0),
            (1, 1),
            (-1, 1),
            (None, None),
        )
        for test in tests:
            a, expected_value = test
            self.assertEqual(abs(MaybeNumber(a)), MaybeNumber(expected_value))

    def test_add(self):
        tests = (
            (1, 2, 3),
            (1, None, None),
            (None, 2, None),
            (None, None, None),
        )
        for test in tests:
            a, b, c = test
            self.assertEqual(MaybeNumber(a) + MaybeNumber(b), MaybeNumber(c))

    def test_ge(self):
        tests = (
            (100, 101, False),
            (100, 100, True),
            (100, 99, True),
            (100, None, None),
            (None, 101, None),
            (None, None, None),
        )
        for test in tests:
            a, b, c = test
            self.assertEqual(MaybeNumber(c), MaybeNumber(a).ge(MaybeNumber(b)))

    def test_sub(self):
        tests = (
            (1, 2, -1),
            (1, None, None),
            (None, 2, None),
            (None, None, None),
        )
        for test in tests:
            a, b, c = test
            self.assertEqual(MaybeNumber(a) - MaybeNumber(b), MaybeNumber(c))

    def test_le(self):
        tests = {
            (100, 101, True),
            (101, 100, False),
            (100, None, None),
            (None, 101, None),
        }
        for test in tests:
            a, b, c = test
            self.assertEqual(MaybeNumber(c), MaybeNumber(a).le(MaybeNumber(b)))

    def test_lt(self):
        tests = (
            (1, 2, True),
            (2, 1, False),
            (None, 2, None),
            (1, None, None),
        )
        for test in tests:
            a, b, c = test
            self.assertEqual(MaybeNumber(c), MaybeNumber(a).le(MaybeNumber(b)))

    def test_div(self):
        tests = (
            (1, 2, 0.5),
            (1, None, None),
            (None, 2, None),
            (None, None, None),
            (1, 0, None),
        )
        for test in tests:
            a, b, c = test
            self.assertEqual(MaybeNumber(a) / MaybeNumber(b), MaybeNumber(c))

    def test_mean(self):
        tests = (
            (1, 2, 1.5),
            (None, 2, None),
            (1, None, None),
        )
        for test in tests:
            a, b, c = test
            self.assertAlmostEqual(MaybeNumber(c), MaybeNumber(a).mean(MaybeNumber(b)))

    def test_mul(self):
        tests = (
            (2, 3, 6),
            (1, None, None),
            (None, 2, None),
            (None, None, None),
        )
        for test in tests:
            a, b, c = test
            self.assertEqual(MaybeNumber(a) * MaybeNumber(b), MaybeNumber(c))

    def test_sqrt(self):
        tests = (
            (4, 2),
            (None, None),
        )
        for test in tests:
            a, b = test
            if a is None:
                self.assertIsNone(MaybeNumber(a).sqrt().value)
            else:
                self.assertAlmostEqual(MaybeNumber(b), MaybeNumber(a).sqrt())


if __name__ == '__main__':
    unittest.main()
    if False:
        pdb  # avoid pyflake8 warning
