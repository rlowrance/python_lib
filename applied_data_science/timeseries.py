'''time series prediction'''
from abc import ABCMeta, abstractmethod
import collections
import pdb
import numbers
import unittest


class CreateFeatures(object):
    'create features file from a master file and possibly many associated information files'
    def __init__(self):
        self.n_input_records = None
        self.n_output_records = None
        self.skipped = None  # collections.Counter for reasons input records were skipped
        pass

    def create(
        self,
        feature_makers=None,
        master_file_records=None,
        selected=None,   # lambda index, master_record: (use_record, maybe_error_message)
        # start optional arguments
        verbose=False,
    ):
        'yield sequence (features:Dict, index, master_record) of output records with features derived from the master file'
        def skip(msg):
            entire_msg = ('skipping %d %s; %s' % (self.n_input_records, index, msg))
            self.skipped[msg] += 1
            if verbose:
                print entire_msg

        def error(msg):
            print 'error in feature maker %s feature_name %s feature_value %s' % (
                feature_maker.name,
                feature_name,
                feature_value,
            )
            print msg
            print 'entering pdb'
            pdb.set_trace()

        assert feature_makers is not None
        assert master_file_records is not None
        assert selected is not None
        self.n_input_records = 0
        self.n_output_records = 0
        self.skipped = collections.Counter()
        for index, master_record in master_file_records:
            # maybe mutate d based on index and ticker_record
            self.n_input_records += 1
            if verbose and self.n_input_records % 1000 == 1:
                print 'creating features from master record %d index %s' % (self.n_input_records, index)
            (use_record, msg) = selected(index, master_record)
            if not use_record:
                skip(msg)
                continue
            # create features from the master_record
            # the feature makers may incorporate data from other records
            features_made = {}
            stopped_early = False
            # concatenate all the features from the feature makers
            # check for errors on the way
            for feature_maker in feature_makers:
                maybe_features = feature_maker.make_features(index, master_record)
                if isinstance(maybe_features, str):
                    skip('no features from feature maker %s' % feature_maker.name)
                    stopped_early = True
                    break
                elif isinstance(maybe_features, dict):
                    for feature_name, feature_value in maybe_features.iteritems():
                        print feature_name, feature_value
                        if feature_name in features_made:
                            error('duplicate feature name')
                        elif not feature_name.startswith('id_') and not isinstance(feature_value, numbers.Number):
                            error('feature value is not numeric')
                        elif feature_name.endswith('_size') and feature_value < 0.0:
                            error('size feature is negative')
                        else:
                            features_made[feature_name] = feature_value
                else:
                    error('unexpected return type from a feature_maker')
            if stopped_early:
                continue
            self.n_output_records += 1
            yield features_made, index, master_record


class FeatureMaker(object):
    __metaclass__ = ABCMeta

    def __init__(self, name=None):
        self.name = name  # used in error message; informal name of the feature maker

    @abstractmethod
    def make_features(ticker_index, tickercusip, ticker_record):
        'return errors:str or Dict[feature_name:str, feature_value:nmber]'
        pass


class FitPredict(object):
    'fit models and predict targets'
    __metaclass__ = ABCMeta

    @abstractmethod
    def fit_predict(self, df_targets=None, df_features=None, df_new_targets=None, hp_spec=None):
        'return result of fitting the model to df_targets and df_features using the HPs, and then predicting'
        pass


class FitPredictOutput(object):
    'content of output file for program fit_predict.py'
    __metaclass__ = ABCMeta

    @abstractmethod
    def as_dict(self):
        'return a dict with all the fields'
        pass


class HpChoices(object):
    'iterated over HpSpec instances'
    __metaclass__ = ABCMeta

    @abstractmethod
    def __iter__(self):
        'yield sequence of HpSpec objects'
        pass


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


class Model(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __str__(self):
        'return parsable string representation of self'

    @staticmethod
    @abstractmethod
    def make_from_str(self, s):
        'return instance of Model'


class TestHpChoices(unittest.TestCase):
    def test_construction(self):
        self.assertRaises(Exception, HpChoices, None)


class TestHpSpeC(unittest.TestCase):
    def test_construction(self):
        self.assertRaises(Exception, HpSpec, None)


if __name__ == '__main__':
    unittest.main()
