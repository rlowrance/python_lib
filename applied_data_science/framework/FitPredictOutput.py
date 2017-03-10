from abc import ABCMeta, abstractmethod


class FitPredictOutput(object):
    'content of output file for program fit_predict.py'
    __metaclass__ = ABCMeta

    @abstractmethod
    def as_dict(self):
        'return a dict with all the fields'
        pass
