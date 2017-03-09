'''Collect a bunch of named items (like a C struct)

ref: Python Cookbook "Collecting a Bunch of Named Items"

usage
  point = Bunch(datum=y, squared=y*y)
  if point.squared > threshold:
      point.is_ok = True
  b = Bunch(namespace)
'''
import argparse
import pdb
import unittest


class Bunch(object):
    @staticmethod
    def from_namespace(namespace):
        b = Bunch()
        for attr, value in namespace.__dict__.iteritems():
            b.__dict__[attr] = value
        return b

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def values(self, d, basename):
        # return list of values basename.key = value
        result = []
        for k in sorted(d):
            v = d[k]
            if isinstance(v, Bunch):
                vs = self.values(v.__dict__, k)
                for v in vs:
                    result.append(v)
            elif isinstance(v, argparse.Namespace):
                for k2, v2 in v.__dict__.items():
                    result.append('%s.%s = %s' % (str(k), str(k2), str(v2)))
            elif basename == '':
                result.append('%s = %s' % (k, v))
            else:
                result.append('%s.%s = %s' % (basename, k, v))
        return result

    def __str__(self, base_name=''):
        values = self.values(self.__dict__, '')
        s = ''
        for value in values:
            s += '%s' % value
            if len(values) > 1:
                s += '\n'
        return s

    def __repr__(self):
        s = 'Bunch('
        first = True
        for k, v in self.__dict__.iteritems():
            if first:
                first = False
            else:
                s += ', '
            s += '%s=%s' % (k, v)
        s += ')'
        return s


class Test(unittest.TestCase):
    def setUp(self):
        self.verbose = False

    def test_construction(self):
        struct = Bunch(x=10, y=20)
        struct.total = struct.x + struct.y
        self.assertEqual(struct.x, 10)
        self.assertEqual(struct.total, 30)

    def test_construction_from_namespace(self):
        ns = argparse.Namespace(x=10, y=20)
        b = Bunch.from_namespace(ns)
        if self.verbose:
            pdb.set_trace()
            print b

    def test_print(self):
        inner = Bunch(a=10, b=20)
        outer = Bunch(x='abc', inner=inner)
        if self.verbose:
            print outer


if __name__ == '__main__':
    if False:
        pdb.set_trace()
    unittest.main()
