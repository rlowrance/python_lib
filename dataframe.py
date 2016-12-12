'''function that operator on pandas DataFrame instances

create_report_categorical(df, ...)
create_report_numeric(df, ...)
replace(df, old_name, new_name, new_value)
'''
import collections
import numpy as np

import ColumnsTable
import Report


def create_report_categorical(df, excluded_columns=[], include_types=[object]):
    'return tuple (Report instance, names of columns in the report)'
    description = df.describe(
        include=include_types,
    )
    print description
    r = ReportCategorical()
    included_columns = []
    for column_name in description.columns:
        print column_name, len(column_name)
        if column_name in excluded_columns:
            print 'create_report_categorical: excluding column:', column_name
            continue
        else:
            r.append_detail(description[column_name])
            included_columns.append(column_name)
    return r, included_columns


def create_report_numeric(df, excluded_columns=[], include_types=[np.number, object]):
    'return tuple (Report instance, names of columns in the report)'
    description = df.describe(
        include=include_types,
    )
    print description
    r = ReportNumeric()
    included_columns = []
    for column_name in description.columns:
        print column_name
        if column_name in excluded_columns:
            print 'create_report_numeric: excluding column:', column_name
            continue
        else:
            r.append_detail(description[column_name])
            included_columns.append(column_name)
    return r, included_columns


def replace(df, old_name, new_name, new_value):
    'return new DataFrame with one column replaced'
    df1 = df.copy()
    df2 = df1.drop(old_name, 1)  # 1 ==> drop column (as opposed to row)
    df2.insert(0, new_name, new_value)
    return df2


ColumnSpec = collections.namedtuple(
    'ColumnSpec',
    'print_width formatter heading1 heading2 legend',
    )


def categorical(size, header1, header2, definition):
    return ColumnSpec(size, '%%%ds' % size, header1, header2, definition)


def numeric(header1, header2, definition):
    return ColumnSpec(12, '%12.2f', header1, header2, definition)


def count(header1, header2, definition):
    return ColumnSpec(7, '%7d', header1, header2, definition)


all_column_specs = {  # each with a 2-row header
    'count': count('count', 'not NA', 'number of non-missing values'),
    'datacol': ColumnSpec(30, '%30s', 'data', 'column', 'name of column in input file'),
    'mean': numeric(' ', 'mean', 'mean value'),
    'max': numeric(' ', 'max', 'maximum value'),
    'min': numeric(' ', 'min', 'minimum value'),
    'p25': numeric('25th', 'percentile', 'value that is the 25th percentile'),
    'p50': numeric('50th', 'percentile', 'value that is the 50th percentile'),
    'p75': numeric('75th', 'percentile', 'value that is the 75th percentile'),
    'std': numeric('standard', 'deviation', 'standard deviation'),
    'unique': numeric('num', 'unique', 'number of distinct values'),
    'top': categorical(30, 'top', '(most common)', 'most common value'),
    'freq': count('top', 'freq', 'frequency of the most common value'),
    }


def column_def(column_name):
    print column_name
    assert column_name in all_column_specs, ('%s not defined in all_column_specs' % column_name)
    column_spec = all_column_specs[column_name]
    return [
        column_name,
        column_spec.print_width,
        column_spec.formatter,
        [column_spec.heading1, column_spec.heading2],
        column_spec.legend,
        ]


def column_defs(*column_names):
    return [
        column_def(column_name)
        for column_name in column_names
        ]


class ReportAnalysis(object):
    def __init__(self, verbose=True):
        self.report = Report.Report(also_print=verbose)

    def write(self, path):
        self.ct.append_legend()
        for line in self.ct.iterlines():
            self.report.append(line)
        self.report.write(path)


class ReportCategorical(ReportAnalysis):
    def __init__(self, verbose=True):
        super(self.__class__, self).__init__()  # create self.report
        self.ct = ColumnsTable.ColumnsTable(
            column_defs('datacol', 'unique', 'top', 'freq',),
            )
        self.report.append('Statistics on Categorical Columns')
        self.report.append(' ')

    def append_detail(self, col):
        self.ct.append_detail(
            datacol='Period' if col.name[:6] == 'Period' else col.name,
            unique=col['unique'],
            top=col['top'],
            freq=col['freq'],
            )
        # timestamps include first and last, but this code doesn't handle them
        assert 'first' not in col.index, col
        assert 'last' not in col.index, col


class ReportNumeric(ReportAnalysis):
    def __init__(self, verbose=True):
        super(self.__class__, self).__init__()  # create self.report
        self.ct = ColumnsTable.ColumnsTable(
            column_defs('datacol', 'count', 'mean', 'std', 'min', 'p25', 'p50', 'p75', 'max',)
            )
        self.report.append('Statistics on Numeric Columns')
        self.report.append(' ')

    def append_detail(self, col):
        self.ct.append_detail(
            datacol='Period' if col.name[:6] == 'Period' else col.name,
            count=col['count'],
            mean=col['mean'],
            std=col['std'],
            min=col['min'],
            p25=col['25%'],
            p50=col['50%'],
            p75=col['75%'],
            max=col['max'],
            )
