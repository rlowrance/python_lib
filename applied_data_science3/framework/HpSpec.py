from abc import ABCMeta, abstractmethod
import unittest


class HpSpec(object):
    'specification of a model name and its associated hyperparamters'
    __metaclass__ = ABCMeta

    @abstractmethod
    def __str__(self):
        'return parsable string representation'
        # Hint: Use method self._to_str(value) to convert individual values to strings
        # That will make all the string representations use the same encoding of values to strings
        pass

    @staticmethod
    @abstractmethod
    def make_from_str(s):
        'parse the representation returned by str(self) to create an instance'
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

    def _to_str(self, value):
        'internal method. Convert value to a string. Use me in your __str__ method'
        def remove_trailing_zeroes(s):
            return (
                s if s[-1] != '0' else
                remove_trailing_zeroes(s[:-1])
            )
        if value is None:
            return ''
        elif isinstance(value, float):
            return remove_trailing_zeroes(('%f' % value).replace('.', '_'))
        elif isinstance(value, int):
            return '%d' % value
        else:
            return str(value)


class TestHpSpeC(unittest.TestCase):
    def test_construction(self):
        self.assertRaises(Exception, HpSpec, None)


if __name__ == '__main__':
    unittest.main()
