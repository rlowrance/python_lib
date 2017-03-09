from abc import ABCMeta, abstractmethod
import unittest


class HpChoices(object):
    'iterated over HpSpec instances'
    __metaclass__ = ABCMeta

    @abstractmethod
    def __iter__(self):
        'yield sequence of HpSpec objects'
        pass


class TestHpChoices(unittest.TestCase):
    def test_construction(self):
        self.assertRaises(Exception, HpChoices, None)


if __name__ == '__main__':
    unittest.main()
