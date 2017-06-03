import pdb


def columns_table(column_specs, values, trace=False):
    'return [str]'
    # column_specs: iterable of dict that specify the columns
    # values: iterable of iterables, with the values for each row
    #
    # each columns spec is a dictionary with these strings as keys:
    #  'fill' 'align' 'sign' 'width' 'precision' 'type' '#' '0' ','  -- these are format_spec field names
    #  'heading': string with embedded \n to create multiple lines in the heading
    #  'legend':  string that explains the heading
    #
    # the required keys are: width, heading, legend
    #
    # formats: dict of standard format specifiers: ref https://docs.python.org/2.7/library/string.html#string-formatting
    # headings: list of 1 or more headings, with possible embedded \n characters separating the lines
    # values: iterable of row, each row is an iterable of values in same order as the headings
    # legends: list of zero or more legends (explanations of the headings)
    #
    # ex: columns_table((10, 20), (.2f, s), (('first', 'heading'), ('second', 'heading')), ((100.3, 'x'),), ('column 1 desc', 'c2 desc'))
    # ex: columns_table((10, 20), (.2f, s), ('first\nheading', 'second\nheading'), ((100.3, 'x'),), ('column 1 desc', 'c2 desc'))
    #
    # here are the standard format specifiers; present them as a dict[string, value]
    #  format_spec :: [[fill][align][sign][#][0][width][,][.precision][type]
    #  fill ::= <any character>
    #  align ::= '<' | '>' | '=' | '^'  -- left, right, padded after sign, centered
    #  sign  ::= '+' | '-' | " "
    #  width ::= <integer>
    #  precision ::= <integer>
    #  type  == 'b' | 'c' | 'd' | 'e' | 'E' | 'f' | 'F' | 'g' | 'G' | 'n' | 'o' | 's' | 'x' | 'X' | '%'
    def prepend_width(width, formatter):
        return '%%%d%s' % (width, formatter)

    def make_format_spec(d):
        'return a format_spec built from the dict d'
        def value(s):
            return str(d.get(s, ''))

        def presence(s):
            return s if s in d else ''

        return (
            '{:' +
            value('fill') +
            value('align') +
            value('sign') +
            presence('#') +
            presence('0') +
            value('width') +
            presence(',') +
            ('.' if 'precision' in d else '') +
            value('precision') +
            value('type') +
            '}'
        )


    def n_heading_rows():
        'return (int, heading_row_separator) and check all the headings'
        heading_row_separator = '\n'

        def heading(column_spec):
            return column_spec['heading']

        def n_rows(column_spec):
            return 1 + heading(column_spec).count(heading_row_separator)
        result = None
        for column_spec in column_specs:
            if result is None:
                result = n_rows(column_spec)
            else:
                n = n_rows(column_spec)
                assert n == result, 'heading %s does not have expected %d rows' % (heading(column_spec), result)
        return result, heading_row_separator

    result = []
    # create the headings
    if trace:
        pdb.set_trace()
    n_headings, heading_row_separator = n_heading_rows()
    for n in xrange(n_headings):
            heading_portions = []
            for column_spec in column_specs:
                formatter = '{:>%ds}' % column_spec['width']  # right justified
                heading_portion_str = column_spec['heading'].split(heading_row_separator)[n]
                heading_portion = formatter.format(heading_portion_str)
                heading_portions.append(heading_portion)
            result.append(' '.join(heading_portions))

    # append all the values
    if trace:
        pdb.set_trace()
    for value_iterable in values:
        row = []
        for n, column_spec in enumerate(column_specs):
            formatter = make_format_spec(column_spec)
            row.append(formatter.format(value_iterable[n]))
        result.append(' '.join(row))
    # append the legend
    result.append('')
    result.append('legend:')
    legends_format = '{:30s}: {:s}'
    for column_spec in column_specs:
        column_name = column_spec['heading'].replace('\n', ' ')
        formatted = legends_format.format(column_name, column_spec['legend'])
        result.append(formatted)
    return result
