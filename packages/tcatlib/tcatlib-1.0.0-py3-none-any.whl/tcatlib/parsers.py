"""Table parsing logic."""
import pandas as pd


class Parser:
    def parse_line(self, line):
        raise RuntimeError('Abstract method unimplemented.')

    def ingest_all_lines(self, lines):
        rows = [self.parse_line(line) for line in lines if line != '']
        self.record_lengths(rows)
        self.rows = rows

    def record_lengths(self, rows):
        lengths = set([len(row) for row in rows])
        if len(lengths) == 1:
            self.row_length = list(lengths)[0]
        else:
            self.row_length = None

    def is_consistent(self):
        return not (self.row_length is None)

    def get_row_length(self):
        if not self.is_consistent():
            raise ValueError('Line lengths not equal.')
        return self.row_length

    def get_table(self):
        return pd.DataFrame(self.rows)


class FixedStringParser(Parser):
    def __init__(self, delimiter):
        self.delimiter = delimiter

    def parse_line(self, line):
        return line.split(self.delimiter)


class TabParser(FixedStringParser):
    def __init__(self):
        super(TabParser, self).__init__('\t')


class CommaParser(FixedStringParser):
    def __init__(self):
        super(CommaParser, self).__init__(',')
