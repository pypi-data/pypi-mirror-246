"""Entrypoint into tcat utility."""
import sys
import fileinput
import argparse

from tcatlib.printing import print_table

def main_program():
    parser = argparse.ArgumentParser(
        prog='tcat',
        description='For peeking at tabular data in the terminal. Accepts a file or standard input.',
    )
    parser.add_argument('filename', help='Tab-separated or comma-separated table file.', required=False)
    _ = parser.parse_args()
    if sys.stdin.isatty() and len(sys.argv) <= 1:
        sys.exit(0)
    lines = list(fileinput.input())
    try:
        print_table(lines)
    except BrokenPipeError:
        pass
