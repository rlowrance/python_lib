'''framework for  Control programs

Copyright 2017 Roy E. Lowrance

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on as "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing premission and
limitation under the license.
'''

import argparse
import pdb
import sys
import unittest

import applied_data_science.Timer


class Control(object):
    def __init__(
        self,
        input_file_names=None,     # these become the first positional args
        output_file_names=None,    # these become the last positional args
        settings_presence=None,    # these bcome keyword args with action=store_true
        settings_value=None,       # these become keywork args with action=store_value
        add_default_keyword_args=True,  # if True, add settings_presence --test and --trace
        executable_name=None,
    ):
        self.input_file_names = [] if input_file_names is None else input_file_names
        self.output_file_names = [] if output_file_names is None else output_file_names
        self.settings_presence = [] if settings_presence is None else settings_presence
        self.settings_value = [] if settings_value is None else settings_value
        self.add_default_keyword_args = add_default_keyword_args
        self.executable_name = executable_name

        self.random_seed = 123
        self.timer = None

        # created by parse_invocation_args
        # the invocation is
        # python {executable_name}.py {in_path} ... {out_path} ... [options]
        self.file_dep = None  # paths to the input files
        self.targets = None   # paths to the output files

    def parse_invocation(self, invocation=None):
        'set instance vars: arg timer file_dep targets action'

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
            for setting_name in ('test', 'timer', 'trace', 'verbose'):
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
        self.arg = parser.parse_args(argv)

        self.timer = applied_data_science.Timer.Timer() if self.arg.timer else None

        # create side-effect attributes of self
        # NOTES regarding Doit:
        #  file_dep and targets are needed by Doit
        #  Doit's action is the invocation string if it was supplied
        self.file_dep = {}
        for input_file_name in self.input_file_names:
            self.file_dep[input_file_name] = getattr(self.arg, input_file_name)
        self.targets = {}
        for target in self.output_file_names:
            self.targets[target] = getattr(self.arg, target)
        self.action = (
            invocation if invocation is not None else
            ' '.join(sys.argv)
        )
        return self.arg

    def p(self):
        'print'
        for k in sorted(self.__dict__.keys()):
            v = self.__dict__[k]
            if k == 'arg':
                for k1 in sorted(v.__dict__.keys()):
                    print '%s.%s' % (k, k1), v.__dict__[k1]
            else:
                print k, v

    def do_work(self, worker_function):
        if self.arg.verbose:
            self.p()
        return worker_function(self)


class Test(unittest.TestCase):
    def setUp(self):
        self.one = Control(
            input_file_names=('a', 'b'),
            output_file_names=('x', 'y'),
            settings_presence=('presence1',),
            settings_value=('value1',),
            executable_name='executable',
        )

    def test_construction(self):
        Control(
            input_file_names=('a', 'b'),
            output_file_names=('x', 'y'),
            settings_presence=('presence1',),
            settings_value=('value1',),
            executable_name='executable',
        )
        Control()

    def test_parse_invocation(self):
        x = Control(
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

    def test_print(self):
        verbose = False
        invocation = 'executable ina inb outx outy --presence1 --value1 value1xxx'
        self.one.parse_invocation(invocation)
        if verbose:
            self.one.p()


if __name__ == '__main__':
    unittest.main()
    if False:
        pdb
