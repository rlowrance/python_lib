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
'''

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
