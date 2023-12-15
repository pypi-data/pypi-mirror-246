"""String formation functionality from table data."""
from textwrap import wrap
from os import get_terminal_size
from os import environ
import subprocess

from tabulate import tabulate

from tcatlib.parsers import TabParser
from tcatlib.parsers import CommaParser


def print_table(lines):
    try:
        desired = get_terminal_size().columns
    except OSError:
        if 'COLUMNS' in environ:
            desired = int(environ['COLUMNS'])
        else:
            desired = int(subprocess.check_output(['tput', 'cols']))
    add_line_breaks = desired

    table = recover_table(lines, add_line_breaks=add_line_breaks)
    text = tabulate(table, tablefmt='fancy_grid', showindex=False)

    while get_longest_line_length(text) > desired - 1:
        add_line_breaks = add_line_breaks - 1
        if add_line_breaks == 4:
            print(text)
            raise RuntimeError('Cannot find reasonable column size. Too long lines?')
        table = recover_table(lines, add_line_breaks=add_line_breaks)
        text = tabulate(table, tablefmt='fancy_grid', showindex=False)
    print(text)

def recover_table(lines, add_line_breaks=None):
    parsers_priority = [TabParser, CommaParser]
    for Parser in parsers_priority:
        parser = Parser()
        parser.ingest_all_lines(lines)
        if parser.is_consistent():
            if parser.get_row_length() > 1:
                table = parser.get_table()
                if add_line_breaks is not None:
                    return add_line_breaks_to_table(table, add_line_breaks)
                return table
    options = '  '.join([Parser.__name__ for Parser in parsers_priority])
    raise ValueError(f'All table parsers failed:  {options}')

def add_line_breaks_to_table(table, max_length=80):
    def add_line_breaks(cell):
        return add_line_breaks_to_str(cell, max_length)
    new_columns = [add_line_breaks(c) for c in table.columns]
    table.columns = new_columns
    return table.applymap(add_line_breaks)

def add_line_breaks_to_str(string, max_length):
    return '\n'.join(wrap(str(string), max_length))

def get_longest_line_length(text):
    return max(len(l) for l in text.split('\n'))
