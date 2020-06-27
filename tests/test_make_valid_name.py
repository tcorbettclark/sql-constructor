import unittest

from sqlcon import make_valid_name


class TestMakeValidName(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(make_valid_name(""), "")

    def test_already_valid(self):
        self.assertEqual(make_valid_name("abc"), "abc")
        self.assertEqual(make_valid_name("aBc"), "aBc")
        self.assertEqual(make_valid_name("ABc"), "ABc")
        self.assertEqual(make_valid_name("ABc123"), "ABc123")
        self.assertEqual(make_valid_name("ABc_123"), "ABc_123")

    def test_leading_numbers(self):
        self.assertEqual(make_valid_name("12abc"), "abc")
        self.assertEqual(make_valid_name("012abc"), "abc")
        self.assertEqual(make_valid_name("012abc345"), "abc345")

    def test_hypens(self):
        self.assertEqual(make_valid_name("ABc-123"), "ABc_123")
        self.assertEqual(make_valid_name("-ABc-123"), "_ABc_123")
        self.assertEqual(make_valid_name("-ABc-123-"), "_ABc_123_")

    def test_spaces(self):
        self.assertEqual(make_valid_name("abc def"), "abc_def")
        self.assertEqual(make_valid_name("  abc def"), "__abc_def")
        self.assertEqual(make_valid_name("  abc def "), "__abc_def_")

    def test_newlines(self):
        self.assertEqual(make_valid_name("abc\ndef"), "abcdef")
        self.assertEqual(make_valid_name("\n\nabc\ndef"), "abcdef")
        self.assertEqual(make_valid_name("\n\nabc\ndef\n"), "abcdef")
