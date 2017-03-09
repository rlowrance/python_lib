'Report writer'

import pdb

from ColumnsTable import ColumnsTable
from Report import Report


class ReportColumns(object):
    def __init__(self, column_defs, also_print=True):
        self.columns_table = ColumnsTable(column_defs)
        self.report = Report(also_print=also_print)

    def append_detail(self, **kwds):
        self.columns_table.append_detail(**kwds)

    def append_header(self, line):
        self.report.append(line)

    def write(self, path):
        self.columns_table.append_legend()
        for line in self.columns_table.iterlines():
            self.report.append(line)
        self.report.write(path)
