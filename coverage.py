'''
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
import itertools
import pdb
from pprint import pprint
import unittest


def make_names(values):
    return sorted(values.keys())


def make_all_n_tuples(values):
    'return List[Dict[name,value]]'
    result = []
    for name1, name2, name3 in itertools.combinations(make_names(values), 3):
        for value1 in values[name1]:
            for value2 in values[name2]:
                for value3 in values[name3]:
                    d = {
                        name1: value1,
                        name2: value2,
                        name3: value3,
                    }
                    result.append(d)
    return result


def make_all_2_dicts(values):
    'return List[Dict[name, value]]'
    result = []
    for name1, name2 in itertools.combinations(make_names(values), 2):
        for value1 in values[name1]:
            for value2 in values[name2]:
                d = {
                    name1: value1,
                    name2: value2,
                }
                result.append(d)
    return result


def coverage_greedy_3_2(values):
    'return List[Dict[name, value]] that covers everything in make_all_2_dicts'
    pdb.set_trace()
    all_n_tuples = make_all_n_tuples(values)
    all_2_tuples = make_all_2_dicts(values)
    result = []
    print all_n_tuples, all_2_tuples, result


class Test(unittest.TestCase):
    def setUp(self):
        self.values = {
            'alpha': [1, 2, 3],
            'beta': [10, 20],
            'gamma': ['a', 'b', 'c', 'd'],
        }
        self.names = sorted(self.values.keys())

    def test_make_all_2_dicts(self):
        pdb.set_trace()
        x = make_all_2_dicts(self.names, self.values)
        expected_len = 26
        self.assertEqual(expected_len, len(x))

    def test_make_all_n_tuples(self):
        x = make_all_n_tuples(self.names, self.values)
        expected_len = (
            len(self.values['alpha']) *
            len(self.values['beta']) *
            len(self.values['gamma'])
        )
        self.assertEqual(expected_len, len(x))


if __name__ == '__main__':
    unittest.main()
    if False:
        pdb
        pprint
