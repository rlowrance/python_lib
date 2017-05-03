from abc import ABCMeta, abstractmethod


class Features(object):
    'create features file'
    __metaclass__ = ABCMeta

    @abstractmethod
    def process_input_file(self, yield_input_record):
        pass