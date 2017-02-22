'''create ColumnsTable that can be printed in a txt file

    c = ColumnsTable(('colname', 6, '%6.2f', ('header1', 'header2'), 'legend'),)
    c.append_detail(colname=10)  # also other column name=value pairs
    ...
    c.append_legend()
    report = Report()
    report.append('title')
    for line in c.iterlines():
        report.append(line)
    report.write(path)
'''

import collections
import pdb
import unittest

ColumnsTableFields = collections.namedtuple('ColumnsTableFields', 'name width formatter headers legend')


class ColumnsTable(object):
    def __init__(self, columns, verbose=False):
        'columns is an iterable with elements (name, width, formatter, (header-list), legend)'
        self._columns = []
        self._number_of_header_lines = 0
        self._column_names = set()
        for column_def in columns:
            assert len(column_def) == 5, 'column_def must have length 5: %s' % str(column_def)
            ctf = ColumnsTableFields(*column_def)
            headers = ctf.headers
            # convert 'abc' to ('abc',)
            headers = (headers,) if isinstance(headers, str) else headers
            if self._number_of_header_lines != 0:
                if self._number_of_header_lines != len(headers):
                    print '+++++++++++++++++++++'
                    print 'inconsistent number of lines in header'
                    print 'have both %d and %d' % (self._number_of_header_lines, len(headers))
                    print 'found at header: %s' % headers
                    print '+++++++++++++++++++++'
                    pdb.set_trace()
            self._number_of_header_lines = len(headers)
            self._columns.append(ColumnsTableFields(ctf.name,
                                                    ctf.width,
                                                    ctf.formatter,
                                                    headers,
                                                    ctf.legend))
            if ctf.name in self._column_names:
                print '+++++++++++++++++++++'
                print 'column name already defined: %s' % ctf.name
                print '+++++++++++++++++++++'
                pdb.set_trace()
            self._column_names.add(ctf.name)
        self._lines = []
        self._verbose = verbose
        self._header()

    def append_legend(self, prefix_width=20):
        def cat_headers(headers):
            text = ''
            for header in headers:
                if len(text) > 0:
                    text += ' '
                text += header.strip()
            return text

        self.append_line(' ')
        self.append_line('column legend:')
        for cd in self._columns:
            # TODO: replace fix width below with value detemined from column headings
            format = '%%%ds -> %%s' % prefix_width
            line = format % (cat_headers(cd.headers), cd.legend)
            self.append_line(line)

    def iterlines(self):
        for line in self._lines:
            yield line

    def append_detail(self, **kwds):
        line = ''
        # detect and report extra arguments
        for k in kwds.keys():
            if k not in self._column_names:
                print 'Column %s is not defined in the ColumnTable' % k
                print 'defined column names are', self._column_names
                pdb.set_trace()
        # format values in kwds
        for cd in self._columns:
            if cd.name in kwds and kwds[cd.name] is not None:
                try:
                    glyph = cd.formatter % kwds[cd.name]
                except TypeError as e:
                    print '+++++++++++++++++++++++++'
                    print TypeError, e
                    print 'formatter  : %s' % cd.formatter
                    print 'field name : %s' % cd.name
                    print 'field value: %s' % kwds[cd.name]
                    print '+++++++++++++++++++++++++'
                    pdb.set_trace()
            else:
                # if missing or None, print spaces for the value
                glyph = ' ' * cd.width
            if len(line) > 0:
                line += ' '
            line += glyph
        self.append_line(line)

    def append_line(self, line):
        if self._verbose:
            print line
        self._lines.append(line)

    def _header(self):
        def append_header(index):
            line = ''
            for cd in self._columns:
                formatter = '%' + str(cd.width) + 's'
                formatted = formatter % cd.headers[index]
                line += (' ' if len(line) > 0 else '') + formatted
            self.append_line(line)

        for header_line_index in xrange(self._number_of_header_lines):
            append_header(header_line_index)

    def _print(self):
        for line in self._lines:
            print line


class TestColumnsTable(unittest.TestCase):
    def setUp(self,):
        self.verbose = False
        self.columns = ColumnsTable(
            (('a', 3, '%3d', ('one', 'num'), 'angstroms'),
             ('bcd', 10, '%10.2f', ('length', 'meters'), 'something really big'),
             ),
            verbose=self.verbose,
        )

    def test_construction(self):
        self.assertTrue(True)
        pass  # tested in setUp()

    def test_append_detail_line(self):
        c = self.columns
        c.append_detail(a=10, bcd=20)
        c.append_detail(bcd=30)
        c.append_detail(a=50)
        self.assertEqual(len(c._lines), 5)
        self.assertTrue(True)

    def test_iterlines(self):
        c = self.columns
        counter = collections.Counter()

        for line in c.iterlines():
            counter['line'] += 1
            if self.verbose:
                print line

        self.assertEqual(counter['line'], 2)  # only 2 column headers lines

    def test_append_legend_lines(self):
        c = self.columns
        c.append_legend()
        self.assertTrue(True)

    def test_one_header(self):
        c = ColumnsTable(
            (('a', 10, '%d', 'first', 'words'),
             ('b', 20, '%d', 'second', 'more words'),
             )
        )
        self.assertEqual(c._number_of_header_lines, 1)


if __name__ == '__main__':
    unittest.main()
    if False:
        pdb
