'framework for filter programs'

import argparse
import pdb
import sys
import unittest

import applied_data_science.Timer


class Filter(object):
    def __init__(
        self,
        input_file_names=None,     # these become the first positional args
        output_file_names=None,    # these become the last positional args
        settings_presence=None,    # these bcome keyword args with action=store_true
        settings_value=None,       # these become keywork args with action=store_value
        add_default_keyword_args=True,  # if True, add settings_presence --test and --trace
        executable_name=None,
    ):
        self.input_file_names = input_file_names
        self.output_file_names = output_file_names
        self.settings_presence = settings_presence
        self.settings_value = settings_value
        self.add_default_keyword_args = add_default_keyword_args
        self.executable_name = executable_name

        self.random_seed = 123
        self.timer = applied_data_science.Timer.Timer()

        # created by parse_invocation_args
        # the invocation is
        # python {executable_name}.py {in_path} ... {out_path} ... [options]
        self.file_dep = None  # paths to the input files
        self.targets = None   # paths to the output files

    def parse_invocation(self, invocation=None):
        'return argparse.NameSpace and populate filepaths and settings'

        # create the parser
        parser = argparse.ArgumentParser()

        for positional_arg_name in self.input_file_names:
            parser.add_argument(positional_arg_name)

        for positional_arg_name in self.output_file_names:
            parser.add_argument(positional_arg_name)

        for setting_name in self.settings_presence:
            parser.add_argument('--%s' % setting_name, action='store_true')

        for setting_name in self.settings_value:
            parser.add_argument('--%s' % setting_name, action='store')

        if self.add_default_keyword_args:
            for setting_name in ('test', 'trace'):
                parser.add_argument('--%s' % setting_name, action='store_true')

        # use the parser
        # ignore the program name from the invocation; instead use self.executable_name
        def all_but_first(s):
            'return string formed by dropping first word'
            pieces = invocation.split(' ')
            most_pieces = ' '.join(pieces[1:])
            return most_pieces

        argv = (
            sys.argv[1:] if invocation is None else
            invocation.split(' ')[1:]
        )
        arg = parser.parse_args(argv)

        # create side-effect attributes of self
        # NOTES regarding Doit:
        #  file_dep and targets are needed by Doit
        #  Doit's action is the invocation string if it was supplied
        self.file_dep = {}
        for input_file_name in self.input_file_names:
            self.file_dep[input_file_name] = getattr(arg, input_file_name)
        self.targets = {}
        for target in self.output_file_names:
            self.targets[target] = getattr(arg, target)
        self.action = (
            invocation if invocation is not None else
            ' '.join(sys.argv)
        )
        return arg


class Test(unittest.TestCase):
    def test_construction(self):
        Filter(
            input_file_names=('a', 'b'),
            output_file_names=('x', 'y'),
            settings_presence=('presence1',),
            settings_value=('value1',),
            executable_name='executable',
        )
        Filter()

    def test_parse_invocation(self):
        x = Filter(
            input_file_names=('a', 'b'),
            output_file_names=('x', 'y'),
            settings_presence=('presence1',),
            settings_value=('value1',),
            executable_name='executable',
        )

        invocation = 'executable ina inb outx outy --presence1 --value1 value1xxx'
        arg = x.parse_invocation(invocation)
        self.assertEqual(arg.a, 'ina')
        self.assertEqual(arg.b, 'inb')
        self.assertEqual(arg.x, 'outx')
        self.assertEqual(arg.y, 'outy')
        self.assertEqual(arg.presence1, True)
        self.assertEqual(arg.value1, 'value1xxx')
        self.assertEqual(x.file_dep, {'a': 'ina', 'b': 'inb'})
        self.assertEqual(x.targets, {'x': 'outx', 'y': 'outy'})
        self.assertEqual(x.action, x.action)


if __name__ == '__main__':
    unittest.main()
    if False:
        pdb
