'''Report writer

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
''

import pdb


class Report(object):
    def __init__(self, also_print=True):
        self._also_print = also_print
        self._lines = []

    def append(self, line):
        self._lines.append(line)
        if self._also_print:
            print line

    def append_lines(self, lines):
        for line in lines:
            self.append(line)

    def append_report(self, other_report):
        for line in other_report.iterlines():
            self.append(line)

    def extend(self, lines):
        for line in lines:
            self.append(line)

    def write(self, path):
        f = open(path, 'w')
        for line in self._lines:
            try:
                f.write(str(line))
            except:
                print line
                print type(line)
                pdb.set_trace()
            f.write('\n')
        f.close()

    def iterlines(self):
        for line in self._lines:
            yield line

    def lines(self):
        return self._lines
