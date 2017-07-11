from abc import ABCMeta
import collections
import pdb
from pprint import pprint
import unittest


class Doit(object):
    'create items self.in_*, self.inout_*, self.out_*, self.actions, self.file_dep, self.targets'
    __metaclass__ = ABCMeta

    def __str__(self):
        for k in sorted(self.__dict__.keys()):
            v = self.__dict__[k]
            if isinstance(v, collections.Iterable):
                print 'doit.%s =' % k
                pprint(v)
            else:
                print 'doit.%s = %s' % (k, v)
        return self.__repr__()


class Test(unittest.TestCase):
    def test_construction(self):
        verbose = False

        class X(Doit):
            def __init__(self, a, b):
                self.a = a
                self.b = b

        x = X('a', [1, 2, 3])
        if verbose:
            print x
        self.assertEqual('a', x.a)
        self.assertEqual([1, 2, 3], x.b)


if __name__ == '__main__':
    unittest.main()
    if False:
        pdb
