'manipulation of dates'
from __future__ import division

import datetime
import pdb
import unittest


class Date(object):
    def __init__(self, from_float=None, from_yyyy_mm_dd=None):
        if from_float is not None:
            if isinstance(from_float, float):
                self._value = Date._from_float(from_float)  # a datetime.date
            else:
                print 'arg from_float %s is of type %s, not float' % (from_float, type(from_float))
                assert False, 'construction error'
        elif from_yyyy_mm_dd is not None:
            self._value = Date._from_yyyy_mm_dd(from_yyyy_mm_dd)
        else:
            print 'bad construction of Date'
            assert False, 'construct via Data(from_float=<float value>)'
        self.value = self._value  # guaranteed to be a date.datetime

    def as_datetime_date(self):
        'return value as a datetime.date'
        return self._value  # for now, the value is stored as a datetime.date

    def __str__(self):
        print '%s' % self.value

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

    @staticmethod
    def _from_yyyy_mm_dd(s):
        try:
            year, month, day = s.split('-')
            return datetime.date(int(year), int(month), int(day))
        except:
            raise ValueError('%s is not a str of the form YYYY-MM-DD' % s)


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

    def test_from_yyyy_mm_dd(self):
        tests = (
            ('2006-03-15', 2006, 3, 15),
        )
        for test in tests:
            s, expected_year, expected_month, expected_day = test
            d = Date(from_yyyy_mm_dd=s)
            self.assertEqual(
                d.value,
                datetime.date(expected_year, expected_month, expected_day)
            )


if __name__ == '__main__':
    unittest.main()
    if False:
        pdb
