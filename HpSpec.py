from abc import ABCMeta, abstractmethod
import unittest


class HpSpec(object):
    'specification of a model name and its associated hyperparamters'
    __metaclass__ = ABCMeta

    @abstractmethod
    def __str__(self):
        'return parsable string representation'
        pass

    @staticmethod
    @abstractmethod
    def make_from_str(s):
        'parse the representation returned by str(s) to create an instance'
        pass

    @abstractmethod
    def iteritems(self):
        'yield each (hyparameter name:str, hyperparameter value)'
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __lt__(self, other):
        pass


class TestHpSpeC(unittest.TestCase):
    def test_construction(self):
        self.assertRaises(Exception, HpSpec, None)


if __name__ == '__main__':
    unittest.main()
