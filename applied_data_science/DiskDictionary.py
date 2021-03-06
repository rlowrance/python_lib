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
import os
import pdb
import pickle as pickle
import unittest


class DiskDictionary(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.f = None

    def append(self, key, value):
        'write key and value to disk'
        if self.f is None:
            self.f = open(self.filepath, 'wb')
        record = (key, value)
        pickle.dump(record, self.f)

    def close(self):
        if self.f is not None:
            self.f.close()

    def items(self):
        'generate (key, value) pairs that are in the disk file'
        if self.f is not None:
            raise RuntimeError('backing file already opened')
        self.f = open(self.filepath, 'rb')
        while True:
            try:
                record = pickle.load(self.f)
                key, value = record
                yield key, value
            except EOFError:
                self.f.close()
                break  # fall through and yield StopIteration
        self.f.close()
        self.f = None

    def file_exists(self):
        'return True iff backing file exists at the provided path'
        return os.path.exists(self.filepath)

    def keyset(self):
        'return set of keys in the disk file'
        result = set()
        if self.file_exists():
            for k, v in list(self.items()):
                # assert k not in result, 'duplicate key: %s' % str(k)
                result.add(k)
        return result

    # implement with DiskDictionary(path) as dd:
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.f is not None:
            self.f.close()


class Test(unittest.TestCase):
    def test1(self):
        path = '/tmp/DiskDictionary'
        os.system('rm %s' % path)
        dd = DiskDictionary('/tmp/DiskDictionary')
        dd.append('key1', 'rec1')
        dd.close()
        dd = DiskDictionary(path)
        found = 0
        for k, v in list(dd.items()):
            found += 1

            self.assertTrue(isinstance(k, str))
            self.assertEqual(k, 'key1')

            self.assertTrue(isinstance(v, str))
            self.assertEqual(v, 'rec1')
        self.assertEqual(found, 1)
        dd.close()

    def test_keyset(self):
        path = '/tmp/DiskDictionary'
        with DiskDictionary(path) as dd:
            dd.append('key1', ['value1', 1])
            dd.append('key2', ['value2', 2])
        with DiskDictionary(path) as dd:
            keyset = dd.keyset()
            self.assertEqual(len(keyset), 2)
            self.assertTrue('key1' in keyset)
            self.assertTrue('key2' in keyset)

    def test_file_exists(self):
        path = '/tmp/blah blah'
        with DiskDictionary(path) as dd:
            self.assertFalse(dd.file_exists())


if __name__ == '__main__':
    unittest.main()
    if False:
        pdb
