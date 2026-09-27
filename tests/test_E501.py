"""E501 should measure tab-indented lines using indent-size."""
import unittest

from pycodestyle import StyleGuide
from testing.support import InMemoryReport


def _errors(src, **kwargs):
    guide = StyleGuide(select=('E501',), **kwargs)
    reporter = guide.init_report(InMemoryReport)
    guide.input_file(
        filename='in-memory-test-file.py',
        lines=src.splitlines(True),
    )
    return reporter.in_memory_errors


class E501Test(unittest.TestCase):
    def test_tabs_counted_as_indent_size(self):
        # One tab + 76 'a's is 77 raw characters (under the default 79)
        # but 80 columns once the tab is expanded with indent-size 4.
        too_long = '\t' + 'a' * 76 + '\n'
        just_ok = '\t' + 'a' * 75 + '\n'

        self.assertEqual(
            _errors(too_long, max_line_length=79, indent_size=4),
            ['E501:1:80'],
        )
        self.assertEqual(
            _errors(just_ok, max_line_length=79, indent_size=4),
            [],
        )

    def test_issue_1189_reproducer(self):
        src = (
            'if True:  # noqa: E501\n'
            '\t# aa\n'
            '\t# aaa\n'
            '\tif True:  # noqa: E501\n'
            '\t\t# a\n'
            '\t\t# aa\n'
        )
        self.assertEqual(
            _errors(src, max_line_length=5, indent_size=4),
            ['E501:2:6', 'E501:3:6', 'E501:5:6', 'E501:6:6'],
        )
