'Report writer'

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
