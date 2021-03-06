'''filter to produce Pandas description of a csv file

INVOCATION: python describe.py ARGS

INPUT FILES:
 stdin or FILES from command line

OUTPUT FILES:
 stdout  csv containing df.describe() results
 stderr  result of print statements

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

from __future__ import division
from __future__ import print_function

# python's library
import argparse
import datetime
import inspect
import numpy as np
import os
import pandas as pd
import pdb
from pprint import pprint
import random
import sys
import unittest

# roy's library
import Bunch
import dataframe
import dirutility
import Logger
import Timer


def eprint(*args, **kwargs):
    'print to stderr'
    print(*args, file=sys.stderr, **kwargs)


def make_control(argv):
    'return a Bunch of controls'
    eprint('argv', argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('--i', help='file to read, if not stdin')
    parser.add_argument('--o', help='path to output file, if not stdout')
    parser.add_argument('--unittest', action='store_true', help='run unit tests and exit')
    parser.add_argument('--test', action='store_true', help='if present, truncated input and enable test code')
    parser.add_argument('--trace', action='store_true', help='if present, call pdb.set_trace() early in run')
    arg = parser.parse_args(argv[1:])  # ignore invocation name
    arg.me = parser.prog.split('.')[0]

    if arg.trace:
        pdb.set_trace()

    return Bunch.Bunch(
        arg=arg,
        test=arg.test,
        )


def do_work(control):
    with (open(control.arg.i, 'r') if control.arg.i is not None else sys.stdin) as f:
        df = pd.read_csv(
            f,
            low_memory=False,
            nrows=100 if control.test else None,
            )
        eprint('df.columns')
        eprint(df.columns)
        eprint(df)
        eprint(type(df))
        description = df.describe(df)
        file_out = (
            control.arg.o if control.arg.o is not None else
            sys.stdout
            )
        description.to_csv(file_out)


class TestRegression(unittest.TestCase):
    def hig(self):
        pdb.set_trace()
        path_in_dir = os.path.expanduser('~/Dropbox/data/a-and-m-capital/proposal-payments-processing/input/')
        filename = 'HIG_Period_From_Mar2013_To_Nov2016.csv'
        path_in = path_in_dir + filename
        path_out = os.path.expanduser('~/Dropbox/ads/pythonlib/filter/describe-test-output.csv')
        pdb.set_trace()
        command_line = 'describe.py -i %s -o %s' % (path_in, path_out)
        main(command_line.split())


def main(argv):
    eprint('starting main', argv)
    control = make_control(argv)
    if control.arg.unittest:
        unittest.main()
        return

    if control.test:
        eprint(control)

    do_work(control)

    if control.test:
        eprint('DISCARD OUTPUT: test')
    return


# API starts here
# NOTE: design API so that it is I/O free
def describe(df, is_categorical=None):
    # return (numeric, categorical), 2 DataFrames describing the input'
    # optional is_categorical(column_name) returns True iff the column is categorical
    
    def try_describe(df, include):
        try:
            result = df.describe(include=include)
            return result
        except ValueError as e:
            if e.args[0] == 'No objects to concatenate':
                return pd.DataFrame()
            else:
                raise  # re-raise last exception

    if is_categorical is None:
        categorical = try_describe(df, [object])
        numeric = try_describe(df, [np.number])
        return categorical, numeric

    # classify columns
    columns_numeric = []
    columns_categorical = []
    for column_name in df.columns:
        if is_categorical is None:
            columns_numeric.append(column_name)
        else:
            if is_categorical(column):
                columns_categorical.append(column_name)
            else:
                columns_numeric.append(column_name)

    categorical = pd.DataFrame(include=columns_categorical)
    numeric = df.describe(include=columns_numeric)
    return categorical, numeric


if __name__ == '__main__':
    if False:
        # avoid pyflakes warnings
        pass

    # unittest.main()
    main(sys.argv)
