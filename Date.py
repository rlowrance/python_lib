'manipulation of dates'
from __future__ import division

import datetime
import pdb
import unittest


class Date(object):
    def __init__(self, from_float=None):
        if from_float is not None:
            if isinstance(from_float, float):
                self._value = Date._from_float(from_float)  # a datetime.date
            else:
                print 'arg from_float %s is of type %s, not float' % (from_float, type(from_float))
                assert False, 'construction error'
        else:
            print 'bad construction of Date'
            assert False, 'construct via Data(from_float=<float value>)'

    def as_datetime_date(self):
        'return value as a datetime.date'
        return self._value  # for now, the value is stored as a datetime.date

    @staticmethod
    def _from_float(x):
        'return a datetime.date'
        assert isinstance(x, float), x
        assert 0 < x <= 99999999, x
        year = int(x / 10000)
        month_day = x - year * 10000
        month = int(month_day / 100)
        day = int(month_day - month * 100)
        result = datetime.date(year, month, day)
        return result


class TestDate(unittest.TestCase):
    def test_from_float_ok(self):
        tests = (
            (20030826, 2003, 8, 26),
            (10101, 1, 1, 1),
            (19500830, 1950, 8, 30),
            (19520512, 1952, 5, 12),
        )
        for test in tests:
            x, year, month, day = test
            d = Date(from_float=float(x))
            self.assertTrue(isinstance(d, Date))
            self.assertTrue(isinstance(d._value, datetime.date))
            dt = d.as_datetime_date()
            self.assertEqual(year, dt.year)
            self.assertEqual(month, dt.month)
            self.assertEqual(day, dt.day)

    def test_from_float_bad(self):
        tests = (
            00000101,
            20170001,
            20171301,
            20171200,
            20171232,
        )

        def f(x):
            return Date(from_float=float(x))

        for test in tests:
            self.assertRaises(ValueError, f, test)


if __name__ == '__main__':
    unittest.main()
    if False:
        pdb
