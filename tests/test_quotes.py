import unittest

from sqlcon import single_quote as sq
from sqlcon import double_quote as dq


class TestSingleQuotes(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(sq(""), "''")

    def test_single_quote(self):
        self.assertEqual(sq("'"), "''''")

    def test_single_quote_x2(self):
        self.assertEqual(sq("''"), "''''''")

    def test_start_single_quote(self):
        self.assertEqual(sq("'asdf"), "'''asdf'")

    def test_start_single_quote_x2(self):
        self.assertEqual(sq("''asdf"), "'''''asdf'")

    def test_end_single_quote(self):
        self.assertEqual(sq("asdf'"), "'asdf'''")

    def test_end_single_quote_x2(self):
        self.assertEqual(sq("asdf''"), "'asdf'''''")

    def test_newline(self):
        self.assertEqual(sq("fred\nbloggs"), "'fred\nbloggs'")

    def test_backslash(self):
        self.assertEqual(sq(r"fred\bloggs"), r" E'fred\\bloggs'")

    def test_double_quote(self):
        self.assertEqual(sq('"'), """'"'""")

    def test_double_quote_x2(self):
        self.assertEqual(sq('""'), """'""'""")

    def test_start_double_quote(self):
        self.assertEqual(sq('"asdf'), """'"asdf'""")

    def test_start_double_quote_x2(self):
        self.assertEqual(sq('""asdf'), """'""asdf'""")


class TestDoubleQuotes(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(dq(""), '""')

    def test_double_quote(self):
        self.assertEqual(dq('"'), '""""')

    def test_double_quote_x2(self):
        self.assertEqual(dq('""'), '""""""')

    def test_start_double_quote(self):
        self.assertEqual(dq('"asdf'), '"""asdf"')

    def test_start_double_quote_x2(self):
        self.assertEqual(dq('""asdf'), '"""""asdf"')

    def test_end_double_quote(self):
        self.assertEqual(dq('asdf"'), '"asdf"""')

    def test_end_double_quote_x2(self):
        self.assertEqual(dq('asdf""'), '"asdf"""""')

    def test_newline(self):
        self.assertEqual(dq("fred\nbloggs"), '"fred\nbloggs"')

    def test_backslash(self):
        self.assertEqual(dq(r"fred\bloggs"), r'"fred\bloggs"')

    def test_single_quote(self):
        self.assertEqual(dq("'"), '''"'"''')

    def test_single_quote_x2(self):
        self.assertEqual(dq("''"), '''"''"''')

    def test_start_single_quote(self):
        self.assertEqual(dq("'asdf"), '''"'asdf"''')

    def test_start_single_quote_x2(self):
        self.assertEqual(dq("''asdf"), '''"''asdf"''')
